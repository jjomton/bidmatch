import json
import os
import sys

from services.g2b_collector_service import G2BCollectorService


def run():
    bid_notice_no = os.getenv("G2B_DEBUG_BID_NOTICE_NO")
    bid_notice_ord = os.getenv("G2B_DEBUG_BID_NOTICE_ORD", "000")

    if len(sys.argv) >= 2:
        bid_notice_no = sys.argv[1]
    if len(sys.argv) >= 3:
        bid_notice_ord = sys.argv[2]

    if not bid_notice_no:
        raise ValueError("bid notice number is required. pass argv or G2B_DEBUG_BID_NOTICE_NO.")

    collector = G2BCollectorService()
    bid_notice_ord = collector._normalize_notice_order(bid_notice_ord)
    payload = collector._fetch_by_notice_key(
        "getBidPblancListInfoLicenseLimit",
        bid_notice_no,
        bid_notice_ord,
    )
    items = collector._extract_items(payload)
    parsed = collector._extract_license_limit_items(items)

    return {
        "bid_notice_no": bid_notice_no,
        "bid_notice_ord": bid_notice_ord,
        "meta": collector._extract_meta(payload),
        "items_count": len(items),
        "item_keys": [list(item.keys()) for item in items[:3]],
        "items_sample": items[:3],
        "parsed": parsed,
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2, default=str))
