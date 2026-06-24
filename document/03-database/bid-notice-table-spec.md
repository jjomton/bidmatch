# 공고 테이블 설계안

이 문서는 나라장터 OpenAPI에서 수집한 공고를 저장하기 위한 `bid_notices` 테이블 기준안을 정리합니다.

목표는 공고 원본 데이터를 보관하면서도, 사용자 조건 매칭과 목록 조회가 느려지지 않도록 검색 필드를 함께 저장하는 것입니다.

## 1. 테이블 역할

| 테이블 | 역할 |
| --- | --- |
| `bid_notices` | 나라장터에서 수집한 공고의 기본 정보, 검색 필터, 매칭 판단용 데이터를 저장 |

## 2. 중복 방지 기준

| 기준 컬럼 | 설명 |
| --- | --- |
| `bid_notice_no` | 입찰공고번호 |
| `bid_notice_ord` | 입찰공고차수 |
| `biz_type` | 업무 구분. `SERVC`, `THNG`, `ETC` |

유니크 키는 `(bid_notice_no, bid_notice_ord, biz_type)`로 잡습니다.

## 3. 공고 테이블 컬럼

| 컬럼 | 타입 | 필수 | 인덱스 | 설명 |
| --- | --- | --- | --- | --- |
| `id` | `BIGINT` | Y | PK | 내부 식별자 |
| `bid_notice_no` | `VARCHAR(100)` | Y | Unique | 입찰공고번호 |
| `bid_notice_ord` | `VARCHAR(20)` | Y | Unique | 입찰공고차수 |
| `biz_type` | `VARCHAR(30)` | Y | Unique, Index | 업무 구분. 용역, 물품, 기타 |
| `notice_type` | `VARCHAR(50)` | N | Index | 공고 종류 |
| `title` | `VARCHAR(500)` | Y | Fulltext 후보 | 입찰공고명 |
| `notice_org_code` | `VARCHAR(50)` | N | Index | 공고기관코드 |
| `notice_org_name` | `VARCHAR(255)` | N | Index | 공고기관명 |
| `demand_org_code` | `VARCHAR(50)` | N | Index | 수요기관코드 |
| `demand_org_name` | `VARCHAR(255)` | N | Index | 수요기관명 |
| `region_code` | `VARCHAR(50)` | N | Index | 참가가능지역 또는 지역제한 코드 |
| `region_name` | `VARCHAR(100)` | N | Index | 참가가능지역 또는 지역제한명 |
| `industry_code` | `VARCHAR(50)` | N | Index | 업종코드 |
| `industry_name` | `VARCHAR(255)` | N | Index | 업종명 |
| `eligible_industry_codes` | `TEXT` | N | - | 입찰 가능한 업종코드 목록. 여러 값은 쉼표로 구분 |
| `eligible_industry_names` | `TEXT` | N | - | 입찰 가능한 업종명 목록. 여러 값은 쉼표로 구분 |
| `license_limit_items` | `JSON` | N | - | 입찰 가능 업종/면허 제한 원본 목록 |
| `license_limit_raw_payload` | `JSON` | N | - | 면허/업종 제한 보강 API 원본 응답 |
| `license_limit_result_code` | `VARCHAR(20)` | N | - | 면허/업종 제한 보강 API 결과 코드 |
| `license_limit_result_message` | `VARCHAR(255)` | N | - | 면허/업종 제한 보강 API 결과 메시지 |
| `product_category_source_type` | `VARCHAR(30)` | Y | Index | 물품 분류 출처. `PUBLIC_PROCUREMENT`, `PRODUCT`, `CUSTOM` 등 |
| `product_class_no` | `VARCHAR(100)` | N | Index | 세부품명번호 또는 물품분류번호 |
| `product_name` | `VARCHAR(255)` | N | Index | 구매대상물품명 |
| `base_amount` | `DECIMAL(18,2)` | N | Index | 기초금액 |
| `estimated_price` | `DECIMAL(18,2)` | N | Index | 추정가격 |
| `budget_amount` | `DECIMAL(18,2)` | N | Index | 배정예산 또는 공고 예산 |
| `posted_at` | `DATETIME` | N | Index | 공고게시일시 |
| `registered_at` | `DATETIME` | N | Index | 나라장터 등록일시 |
| `deadline_at` | `DATETIME` | N | Index | 입찰마감일시 |
| `opening_at` | `DATETIME` | N | Index | 개찰일시 |
| `status` | `VARCHAR(30)` | Y | Index | 공고 상태. `OPEN`, `CLOSED`, `CANCELED`, `CHANGED` 등 |
| `is_deadline_excluded` | `BOOLEAN` | Y | Index | 입찰마감 제외 여부 |
| `is_international` | `BOOLEAN` | Y | Index | 국제입찰 여부 |
| `license_limit_text` | `TEXT` | N | - | 면허제한 원문 또는 요약 |
| `match_keywords` | `TEXT` | N | Fulltext 후보 | 매칭용 통합 키워드. 공고명, 기관, 품목, 업종 등을 합친 값 |
| `detail_url` | `TEXT` | N | - | 나라장터 공고 상세 정보 URL. 화면에서 공고명 링크로 사용 |
| `raw_payload` | `JSON` | N | - | API 원본 응답 |
| `last_synced_at` | `DATETIME` | Y | Index | 마지막 동기화 시각 |
| `created_at` | `DATETIME` | Y | - | 생성 시각 |
| `updated_at` | `DATETIME` | Y | - | 수정 시각 |

## 4. 사용자 매칭에 바로 쓰는 데이터

| 사용자 조건 | 공고 컬럼 | 활용 방식 |
| --- | --- | --- |
| 포함 키워드 | `title`, `product_name`, `industry_name`, `match_keywords` | 포함 여부 확인 |
| 제외 키워드 | `title`, `product_name`, `industry_name`, `match_keywords` | 포함 시 제외 |
| 지역 | `region_code`, `region_name` | 참가가능지역/지역제한과 비교 |
| 업종/면허 | `industry_code`, `industry_name`, `eligible_industry_codes`, `eligible_industry_names`, `license_limit_text`, `license_limit_items` | 보유 업종/면허와 비교 |
| 기관 | `notice_org_name`, `demand_org_name` | 선호/제외 기관 비교 |
| 금액 범위 | `base_amount`, `estimated_price`, `budget_amount` | 최소/최대 금액 조건 비교 |
| 물품분류 | `product_class_no`, `product_name` | 물품분류번호 또는 품목명 비교 |
| 물품 카테고리 | `product_category_source_type`, `product_class_no` + `product_categories` 조인 | 대/중/소분류 필터 비교 |
| 마감 여부 | `deadline_at`, `status`, `is_deadline_excluded` | 마감 공고 제외 |

## 5. 인덱스 전략

| 인덱스 | 컬럼 | 목적 |
| --- | --- | --- |
| `uk_bid_notices_notice_ord_type` | `bid_notice_no`, `bid_notice_ord`, `biz_type` | 중복 저장 방지 |
| `idx_bid_notices_biz_status_deadline` | `biz_type`, `status`, `deadline_at` | 목록 조회, 마감 공고 제외 |
| `idx_bid_notices_posted_at` | `posted_at` | 최신순 목록 조회 |
| `idx_bid_notices_registered_at` | `registered_at` | 수집/보정 조회 기준 |
| `idx_bid_notices_org` | `notice_org_name` | 기관명 필터 |
| `idx_bid_notices_demand_org` | `demand_org_name` | 수요기관 필터 |
| `idx_bid_notices_region` | `region_code`, `region_name` | 지역 필터 |
| `idx_bid_notices_industry` | `industry_code`, `industry_name` | 업종/면허 필터 |
| `idx_bid_notices_product` | `product_class_no`, `product_name` | 물품분류/품목 필터 |
| `idx_bid_notices_product_category` | `product_category_source_type`, `product_class_no` | 물품 카테고리 조인 및 필터 |
| `idx_bid_notices_amount` | `estimated_price`, `base_amount`, `budget_amount` | 금액 범위 필터 |
| `idx_bid_notices_sync` | `last_synced_at` | 수집 상태 확인 |
| `ft_bid_notices_match_text` | `title`, `product_name`, `industry_name`, `match_keywords` | 키워드 검색. MySQL Fulltext 적용 후보 |

## 6. 예시 데이터

| 컬럼 | 예시 |
| --- | --- |
| `bid_notice_no` | `20260612001` |
| `bid_notice_ord` | `00` |
| `biz_type` | `SERVC` |
| `notice_type` | `일반용역` |
| `title` | `공공 클라우드 전환 및 운영관리 용역` |
| `notice_org_name` | `조달청` |
| `demand_org_name` | `한국정보화진흥원` |
| `region_name` | `서울특별시` |
| `industry_name` | `소프트웨어사업자` |
| `product_class_no` | `8111159901` |
| `product_name` | `정보시스템개발서비스` |
| `estimated_price` | `150000000.00` |
| `deadline_at` | `2026-06-18 18:00:00` |
| `status` | `OPEN` |
| `match_keywords` | `공공 클라우드 운영관리 용역 소프트웨어 정보시스템개발서비스` |
| `detail_url` | `https://www.g2b.go.kr/...` |

## 7. 구현 시 주의사항

- API 응답 필드명이 변경될 수 있으므로 원본 `raw_payload`를 함께 저장합니다.
- 면허/업종 제한 보강 API 응답은 장애 분석을 위해 `license_limit_raw_payload`에도 별도로 저장합니다.
- 검색에 자주 쓰는 값은 JSON에서 꺼내 별도 컬럼으로 저장합니다.
- 1시간 주기 수집에서는 신규/변경 공고를 업서트하고, `last_synced_at`을 갱신합니다.
- 공고 상세와 첨부파일 확인은 `detail_url`을 통해 나라장터 원본 화면으로 이동하게 합니다.
- 파일은 Cloudtype 로컬 저장소에 저장하지 않고, MVP에서는 별도 파일 테이블도 만들지 않습니다.
- 외자 공고는 수집 대상에서 제외하지만, 나중에 추가할 수 있도록 `biz_type` 값만 확장 가능하게 둡니다.
