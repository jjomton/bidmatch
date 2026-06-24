from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import HTTPError
import json
import re
import time

from config import Config
from repositories.bid_notice_repository import BidNoticeRepository


class G2BCollectorService:
    """Collects open bid notices from 나라장터 public APIs."""

    def __init__(self, repository=None):
        self.repository = repository or BidNoticeRepository()

    def collect(self):
        if not Config.G2B_API_KEY:
            raise ValueError("G2B_API_KEY is required.")

        now = datetime.now()
        started_at = now - timedelta(hours=Config.G2B_LOOKBACK_HOURS)
        endpoints = self._configured_endpoints()

        collected_count = 0
        saved_count = 0
        skipped_closed_count = 0
        endpoint_results = []

        for endpoint in endpoints:
            items, meta = self._fetch_all(endpoint, started_at, now)
            normalized = []
            product_categories = []

            for item in items:
                notice = self._normalize_notice(endpoint, item, now)
                if notice is None:
                    skipped_closed_count += 1
                    continue
                normalized.append(notice)
                if notice.get("product_category"):
                    product_categories.append(notice.pop("product_category"))

            saved_categories = self.repository.upsert_product_categories(product_categories)
            saved = self.repository.upsert_many(normalized)
            collected_count += len(items)
            saved_count += saved
            endpoint_results.append(
                {
                    "endpoint": endpoint,
                    "result_code": meta.get("result_code"),
                    "result_message": meta.get("result_message"),
                    "total_count": meta.get("total_count"),
                    "inqry_div": Config.G2B_INQRY_DIV,
                    "query_from": started_at.strftime("%Y-%m-%d %H:%M"),
                    "query_to": now.strftime("%Y-%m-%d %H:%M"),
                    "fetched": len(items),
                    "saved_open": saved,
                    "saved_categories": saved_categories,
                    "skipped_closed": len(items) - saved,
                }
            )

        closed_count = self.repository.close_expired_notices()

        return {
            "collected": collected_count,
            "saved_open": saved_count,
            "skipped_closed": skipped_closed_count,
            "marked_closed": closed_count,
            "endpoints": endpoint_results,
        }

    def backfill_license_limits(self, limit=100):
        if not Config.G2B_API_KEY:
            raise ValueError("G2B_API_KEY is required.")

        targets = self.repository.list_license_limit_backfill_targets(limit)
        enriched_count = 0
        no_data_count = 0
        error_count = 0
        samples = []

        for target in targets:
            notice = {
                "id": target["id"],
                "bid_notice_no": target["bid_notice_no"],
                "bid_notice_ord": self._normalize_notice_order(target["bid_notice_ord"]),
                "industry_code": None,
                "industry_name": None,
                "match_keywords": target.get("title"),
            }
            self._enrich_license_limit(notice)

            if notice.get("license_limit_fetch_error"):
                error_count += 1
                samples.append(
                    {
                        "id": target["id"],
                        "bid_notice_no": target["bid_notice_no"],
                        "error": notice["license_limit_fetch_error"],
                    }
                )
                continue

            if not notice.get("license_limit_items"):
                no_data_count += 1
                if len(samples) < 5:
                    samples.append(
                        {
                            "id": target["id"],
                            "bid_notice_no": target["bid_notice_no"],
                            "message": "license limit API returned no parseable items",
                        }
                    )
                continue

            self.repository.update_license_limit(target["id"], notice)
            enriched_count += 1

        return {
            "targets": len(targets),
            "enriched": enriched_count,
            "no_data": no_data_count,
            "errors": error_count,
            "samples": samples[:5],
        }

    def _configured_endpoints(self):
        return [
            endpoint.strip()
            for endpoint in Config.G2B_COLLECT_ENDPOINTS.split(",")
            if endpoint.strip()
        ]

    def _fetch_all(self, endpoint, started_at, ended_at):
        page_no = 1
        all_items = []
        meta = {
            "result_code": None,
            "result_message": None,
            "total_count": 0,
        }

        while True:
            payload = self._fetch_page(endpoint, started_at, ended_at, page_no)
            meta = self._extract_meta(payload)
            items = self._extract_items(payload)
            if not items:
                break

            all_items.extend(items)

            total_count = self._extract_total_count(payload)
            if len(all_items) >= total_count or len(items) < Config.G2B_NUM_OF_ROWS:
                break
            page_no += 1

        return all_items, meta

    def _fetch_page(self, endpoint, started_at, ended_at, page_no):
        params = {
            "ServiceKey": Config.G2B_API_KEY,
            "type": "json",
            "numOfRows": Config.G2B_NUM_OF_ROWS,
            "pageNo": page_no,
            "inqryDiv": Config.G2B_INQRY_DIV,
            "inqryBgnDt": started_at.strftime("%Y%m%d%H%M"),
            "inqryEndDt": ended_at.strftime("%Y%m%d%H%M"),
        }
        url = f"{Config.G2B_API_BASE_URL.rstrip('/')}/{endpoint}?{urlencode(params, safe='%')}"

        return self._get_json(url)

    def _fetch_by_notice_key(self, endpoint, bid_notice_no, bid_notice_ord):
        params = {
            "ServiceKey": Config.G2B_API_KEY,
            "type": "json",
            "numOfRows": Config.G2B_NUM_OF_ROWS,
            "pageNo": 1,
            "inqryDiv": "2",
            "bidNtceNo": bid_notice_no,
            "bidNtceOrd": bid_notice_ord,
        }
        url = f"{Config.G2B_API_BASE_URL.rstrip('/')}/{endpoint}?{urlencode(params, safe='%')}"

        return self._get_json(url)

    def _get_json(self, url):
        last_error = None

        for attempt in range(Config.G2B_MAX_RETRIES + 1):
            if Config.G2B_REQUEST_DELAY_SECONDS > 0:
                time.sleep(Config.G2B_REQUEST_DELAY_SECONDS)

            try:
                with urlopen(url, timeout=30) as response:
                    body = response.read().decode("utf-8")
                return json.loads(body)
            except HTTPError as exc:
                last_error = exc
                if exc.code != 429 or attempt >= Config.G2B_MAX_RETRIES:
                    raise

                retry_delay = Config.G2B_RETRY_BASE_DELAY_SECONDS * (2 ** attempt)
                time.sleep(retry_delay)

        raise last_error

    def _extract_items(self, payload):
        body = payload.get("response", {}).get("body", {})
        items = body.get("items", [])

        if isinstance(items, dict):
            items = items.get("item", [])
        if isinstance(items, dict):
            return [items]
        if isinstance(items, list):
            return items
        return []

    def _extract_total_count(self, payload):
        total_count = payload.get("response", {}).get("body", {}).get("totalCount", 0)
        try:
            return int(total_count)
        except (TypeError, ValueError):
            return 0

    def _extract_meta(self, payload):
        header = payload.get("response", {}).get("header", {})
        return {
            "result_code": header.get("resultCode"),
            "result_message": header.get("resultMsg"),
            "total_count": self._extract_total_count(payload),
        }

    def _enrich_license_limit(self, notice):
        try:
            payload = self._fetch_by_notice_key(
                "getBidPblancListInfoLicenseLimit",
                notice["bid_notice_no"],
                notice["bid_notice_ord"],
            )
        except Exception as exc:
            notice["license_limit_fetch_error"] = str(exc)
            return notice

        meta = self._extract_meta(payload)
        notice["license_limit_raw_payload"] = payload
        notice["license_limit_result_code"] = meta.get("result_code")
        notice["license_limit_result_message"] = meta.get("result_message")

        items = self._extract_items(payload)
        if not items:
            return notice

        industries = self._extract_license_limit_items(items)
        if not industries:
            return notice

        notice["license_limit_items"] = industries
        notice["eligible_industry_codes"] = self._join_values(
            [industry["code"] for industry in industries]
        )
        notice["eligible_industry_names"] = self._join_values(
            [industry["name"] for industry in industries]
        )
        notice["industry_code"] = notice["industry_code"] or industries[0].get("code")
        notice["industry_name"] = notice["industry_name"] or industries[0].get("name")
        notice["license_limit_text"] = self._join_values(
            [
                value
                for industry in industries
                for value in (industry.get("code"), industry.get("name"))
                if value
            ]
        )

        notice["match_keywords"] = " ".join(
            value
            for value in [
                notice.get("match_keywords"),
                notice.get("eligible_industry_codes"),
                notice.get("eligible_industry_names"),
            ]
            if value
        )
        return notice

    def _normalize_notice(self, endpoint, item, now):
        deadline_at = self._parse_datetime(self._pick(item, "bidClseDt", "bidClseDate", "bidCloseDt"))
        if deadline_at is None or deadline_at <= now:
            return None

        bid_notice_no = self._pick(item, "bidNtceNo", "bidNoticeNo")
        if not bid_notice_no:
            return None

        bid_notice_ord = self._normalize_notice_order(
            self._pick(item, "bidNtceOrd", "bidNoticeOrd")
        )
        title = self._pick(item, "bidNtceNm", "bidNoticeNm", "ntceNm") or "(제목 없음)"
        detail_url = self._pick(
            item,
            "bidNtceDtlUrl",
            "bidNtceUrl",
            "ntceDtlUrl",
            "linkUrl",
        )
        biz_type = self._biz_type(endpoint)

        notice_org_name = self._pick(item, "ntceInsttNm", "noticeInsttNm")
        demand_org_name = self._pick(item, "dminsttNm", "demandInsttNm")
        region_name = self._pick(item, "prtcptLmtRgnNm", "rgstTyNm", "regionNm")
        industry_code = self._pick(
            item,
            "indstrytyCd",
            "industryCd",
            "bidprcPsblIndstrytyCd",
            "bidPsblIndstrytyCd",
            "lcnsLmtCd",
        )
        industry_name = self._pick(
            item,
            "indstrytyNm",
            "industryNm",
            "bidprcPsblIndstrytyNm",
            "bidPsblIndstrytyNm",
            "lcnsLmtNm",
        )
        eligible_industries = self._extract_eligible_industries(item, industry_code, industry_name)
        product_category = self._extract_product_category(item)
        product_class_no = (
            product_category.get("product_class_no")
            if product_category
            else self._pick(item, "dtilPrdctClsfcNo", "prdctClsfcNo", "pubPrcrmntClsfcNo")
        )
        product_category_source_type = (
            product_category.get("source_type")
            if product_category
            else ("PRODUCT" if product_class_no else "PUBLIC_PROCUREMENT")
        )
        product_name = self._pick(
            item,
            "dtilPrdctClsfcNoNm",
            "prdctClsfcNoNm",
            "productNm",
            "pubPrcrmntClsfcNm",
            "pubPrcrmntMidClsfcNm",
            "pubPrcrmntLrgClsfcNm",
        )

        match_keywords = " ".join(
            value
            for value in [
                title,
                notice_org_name,
                demand_org_name,
                region_name,
                industry_name,
                self._join_values([industry["code"] for industry in eligible_industries]),
                self._join_values([industry["name"] for industry in eligible_industries]),
                product_name,
            ]
            if value
        )

        return {
            "notice_no": bid_notice_no,
            "bid_notice_no": bid_notice_no,
            "bid_notice_ord": bid_notice_ord,
            "biz_type": biz_type,
            "notice_type": self._pick(item, "ntceKindNm", "bidNtceTypeNm"),
            "title": title,
            "organization": notice_org_name,
            "notice_org_code": self._pick(item, "ntceInsttCd", "noticeInsttCd"),
            "notice_org_name": notice_org_name,
            "demand_org_code": self._pick(item, "dminsttCd", "demandInsttCd"),
            "demand_org_name": demand_org_name,
            "region": region_name,
            "region_code": self._pick(item, "prtcptLmtRgnCd", "regionCd"),
            "region_name": region_name,
            "industry_code": industry_code,
            "industry_name": industry_name,
            "eligible_industry_codes": self._join_values(
                [industry["code"] for industry in eligible_industries]
            ),
            "eligible_industry_names": self._join_values(
                [industry["name"] for industry in eligible_industries]
            ),
            "license_limit_items": eligible_industries,
            "product_category_source_type": product_category_source_type,
            "product_class_no": product_class_no,
            "product_name": product_name,
            "base_amount": self._parse_decimal(self._pick(item, "bssamt", "baseAmount")),
            "estimated_price": self._parse_decimal(self._pick(item, "presmptPrce", "estimatedPrice")),
            "budget_amount": self._parse_decimal(self._pick(item, "asignBdgtAmt", "budgetAmount")),
            "posted_at": self._parse_datetime(self._pick(item, "bidNtceDt", "ntceDt", "postedAt")),
            "registered_at": self._parse_datetime(self._pick(item, "rgstDt", "registeredAt")),
            "deadline_at": deadline_at,
            "opening_at": self._parse_datetime(self._pick(item, "opengDt", "openingAt")),
            "status": "OPEN",
            "is_deadline_excluded": self._pick(item, "bidClseExcpYn") == "Y",
            "is_international": bool(self._pick(item, "intrntnlBidYn", "intrntnlDivCd")),
            "license_limit_text": self._pick(item, "lcnsLmtNm", "licenseLimitNm"),
            "match_keywords": match_keywords,
            "source_url": detail_url,
            "detail_url": detail_url,
            "raw_payload": item,
            "product_category": product_category,
        }

    def _biz_type(self, endpoint):
        if "Servc" in endpoint:
            return "SERVC"
        if "Thng" in endpoint:
            return "THNG"
        if "Etc" in endpoint:
            return "ETC"
        return "UNKNOWN"

    def _pick(self, source, *keys):
        for key in keys:
            value = source.get(key)
            if value not in (None, ""):
                return value
        return None

    def _extract_product_category(self, item):
        public_class_no = self._pick(item, "pubPrcrmntClsfcNo")
        if public_class_no:
            depth_1 = self._pick(item, "pubPrcrmntLrgClsfcNm")
            depth_2 = self._pick(item, "pubPrcrmntMidClsfcNm")
            depth_3 = self._pick(item, "pubPrcrmntClsfcNm")
            if depth_1 or depth_2 or depth_3:
                return {
                    "source_type": "PUBLIC_PROCUREMENT",
                    "product_class_no": public_class_no,
                    "category_depth_1": depth_1 or depth_2 or depth_3,
                    "category_depth_2": depth_2,
                    "category_depth_3": depth_3,
                    "description": None,
                }

        product_class_no = self._pick(item, "dtilPrdctClsfcNo", "prdctClsfcNo")
        product_name = self._pick(item, "dtilPrdctClsfcNoNm", "prdctClsfcNoNm", "productNm")
        if product_class_no and product_name:
            return {
                "source_type": "PRODUCT",
                "product_class_no": product_class_no,
                "category_depth_1": product_name,
                "category_depth_2": None,
                "category_depth_3": None,
                "description": "나라장터 물품분류명 기반 자동 생성",
            }

        return None

    def _normalize_notice_order(self, value):
        if value in (None, ""):
            return "000"

        text = str(value).strip()
        if text.isdigit():
            return text.zfill(3)
        return text

    def _extract_eligible_industries(self, item, fallback_code=None, fallback_name=None):
        code_text = self._pick(
            item,
            "indstrytyCd",
            "industryCd",
            "bidprcPsblIndstrytyCd",
            "bidPsblIndstrytyCd",
            "lcnsLmtCd",
        )
        name_text = self._pick(
            item,
            "indstrytyNm",
            "industryNm",
            "bidprcPsblIndstrytyNm",
            "bidPsblIndstrytyNm",
            "lcnsLmtNm",
        )

        codes = self._split_multi_value(code_text or fallback_code)
        names = self._split_multi_value(name_text or fallback_name)
        max_length = max(len(codes), len(names), 1 if fallback_code or fallback_name else 0)

        industries = []
        seen = set()
        for index in range(max_length):
            code = codes[index] if index < len(codes) else None
            name = names[index] if index < len(names) else None
            if not code and not name:
                continue

            key = (code, name)
            if key in seen:
                continue
            seen.add(key)
            industries.append({"code": code, "name": name})

        return industries

    def _extract_license_limit_items(self, items):
        industries = []
        seen = set()

        for item in items:
            parsed_items = []
            parsed_items.extend(
                self._parse_industry_text(
                    self._pick(item, "lcnsLmtNm"),
                    source="license_limit",
                    raw=item,
                )
            )
            parsed_items.extend(
                self._parse_industry_text(
                    self._pick(item, "permsnIndstrytyList"),
                    source="permitted_industry",
                    raw=item,
                )
            )

            if not parsed_items:
                parsed_items.extend(self._parse_industry_candidates(item))

            for industry in parsed_items:
                key = (industry.get("code"), industry.get("name"), industry.get("source"))
                if key in seen:
                    continue
                seen.add(key)
                industries.append(industry)

        return industries

    def _parse_industry_candidates(self, item):
        code = self._pick_by_candidates(item, "code")
        name = self._pick_by_candidates(item, "name")

        if not code:
            code = self._pick(
                item,
                "indstrytyCd",
                "industryCd",
                "bidprcPsblIndstrytyCd",
                "bidPsblIndstrytyCd",
                "lcnsLmtCd",
                "prtcptPsblIndstrytyCd",
            )
        if not name:
            name = self._pick(
                item,
                "indstrytyNm",
                "industryNm",
                "bidprcPsblIndstrytyNm",
                "bidPsblIndstrytyNm",
                "prtcptPsblIndstrytyNm",
            )

        codes = self._split_multi_value(code)
        names = self._split_multi_value(name)
        max_length = max(len(codes), len(names), 1 if code or name else 0)

        industries = []
        for index in range(max_length):
            industry = {
                "code": codes[index] if index < len(codes) else None,
                "name": names[index] if index < len(names) else None,
                "source": "candidate",
                "raw": item,
            }
            if industry["code"] or industry["name"]:
                industries.append(industry)
        return industries

    def _parse_industry_text(self, value, source, raw=None):
        if not value:
            return []

        text = str(value).strip()
        if not text:
            return []

        # API examples: [업종명/1234],[다른업종/5678], 국내여행업(1263)
        groups = re.findall(r"\[([^\]]+)\]", text)
        if not groups:
            groups = self._split_industry_groups(text)

        industries = []
        for group in groups:
            name, code = self._parse_industry_name_code(group)
            if not name and not code:
                continue
            industries.append(
                {
                    "code": code,
                    "name": name,
                    "source": source,
                    "raw": raw,
                }
            )
        return industries

    def _split_industry_groups(self, value):
        normalized = str(value)
        for delimiter in ["\n", ";", ","]:
            normalized = normalized.replace(delimiter, "^")
        return [part.strip() for part in normalized.split("^") if part.strip()]

    def _parse_industry_name_code(self, value):
        text = str(value).strip().strip("[]")
        if not text:
            return None, None

        paren_match = re.match(r"^(?P<name>.+?)\((?P<code>\d+)\)$", text)
        if paren_match:
            return paren_match.group("name").strip(), paren_match.group("code").strip()

        slash_match = re.match(r"^(?P<name>.+?)/(?P<code>\d+)$", text)
        if slash_match:
            return slash_match.group("name").strip(), slash_match.group("code").strip()

        if text.isdigit():
            return None, text
        return text, None

    def _pick_by_candidates(self, source, value_type):
        code_keywords = ("cd", "code")
        name_keywords = ("nm", "name")
        domain_keywords = ("indstr", "industry", "lcns", "license", "lmt", "업종", "면허")
        keywords = code_keywords if value_type == "code" else name_keywords

        for key, value in source.items():
            lowered_key = str(key).lower()
            if value in (None, ""):
                continue
            if not any(domain in lowered_key for domain in domain_keywords):
                continue
            if any(keyword in lowered_key for keyword in keywords):
                return value
        return None

    def _split_multi_value(self, value):
        if not value:
            return []

        normalized = str(value)
        for delimiter in ["|", "/", ",", ";", "\n"]:
            normalized = normalized.replace(delimiter, "^")
        return [part.strip() for part in normalized.split("^") if part.strip()]

    def _join_values(self, values):
        cleaned = []
        for value in values:
            if value and value not in cleaned:
                cleaned.append(value)
        return ",".join(cleaned) if cleaned else None

    def _parse_datetime(self, value):
        if not value:
            return None

        value = str(value).strip()
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y/%m/%d %H:%M:%S",
            "%Y/%m/%d %H:%M",
            "%Y%m%d%H%M%S",
            "%Y%m%d%H%M",
            "%Y-%m-%d",
            "%Y%m%d",
        ]

        for date_format in formats:
            try:
                return datetime.strptime(value, date_format)
            except ValueError:
                continue
        return None

    def _parse_decimal(self, value):
        if value in (None, ""):
            return None

        try:
            return Decimal(str(value).replace(",", ""))
        except (InvalidOperation, ValueError):
            return None
