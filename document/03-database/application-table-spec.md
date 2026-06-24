# 기능 확장 테이블 설계안

이 문서는 BidMatch의 회원, 관심 조건, 매칭, 이메일, 수집 로그, 관리자 기능을 구현하기 위한 테이블 설계안입니다.

## 1. 설계 기준

| 기준 | 내용 |
| --- | --- |
| DB | MariaDB |
| 스키마 동기화 | `back-end/core/schema.py` 기준 자동 보강 |
| 공고 원본 | `bid_notices.raw_payload`에 보관 |
| 공고 검색 | 정규화 컬럼 + 인덱스 사용 |
| 물품 카테고리 | `product_categories`에 분리 저장하고 공고는 분류 키만 참조 |
| 업종/면허 보강 | 공고 수집과 분리된 백필 Job 사용 |
| 알림 중복 방지 | 사용자 + 공고 + 관심조건 기준 |

## 2. 물품 분류

### `product_categories`

나라장터 공고의 조달분류번호와 대/중/소분류명을 저장합니다. 공고 테이블에는 분류 키만 저장하고, 프론트엔드 필터에서는 이 테이블과 조인해 직관적인 카테고리 검색을 제공합니다.

| 컬럼 | 타입 | 설명 |
| --- | --- | --- |
| `id` | `BIGINT` | 카테고리 ID |
| `source_type` | `VARCHAR(30)` | 분류 출처. `PUBLIC_PROCUREMENT`, `PRODUCT`, `CUSTOM` |
| `product_class_no` | `VARCHAR(100)` | 조달분류번호 또는 세부품명번호 |
| `category_depth_1` | `VARCHAR(100)` | 대분류 |
| `category_depth_2` | `VARCHAR(100)` | 중분류 |
| `category_depth_3` | `VARCHAR(100)` | 소분류 |
| `description` | `TEXT` | 부가 설명 |
| `created_at` | `DATETIME` | 생성 시각 |
| `updated_at` | `DATETIME` | 수정 시각 |

유니크 키는 `(source_type, product_class_no)`로 잡습니다.

## 3. 회원/프로필

### `users`

| 컬럼 | 타입 | 설명 |
| --- | --- | --- |
| `id` | `BIGINT` | 사용자 ID |
| `email` | `VARCHAR(255)` | 로그인 이메일 |
| `password_hash` | `VARCHAR(255)` | 비밀번호 해시 |
| `name` | `VARCHAR(100)` | 사용자명 |
| `role` | `VARCHAR(30)` | `USER`, `ADMIN` |
| `status` | `VARCHAR(30)` | `active`, `inactive`, `locked`, `deleted` |
| `email_verified_at` | `DATETIME` | 이메일 인증 시각 |
| `last_login_at` | `DATETIME` | 마지막 로그인 시각 |
| `created_at` | `DATETIME` | 생성 시각 |
| `updated_at` | `DATETIME` | 수정 시각 |

### `user_profiles`

| 컬럼 | 타입 | 설명 |
| --- | --- | --- |
| `id` | `BIGINT` | 프로필 ID |
| `user_id` | `BIGINT` | 사용자 FK |
| `phone_number` | `VARCHAR(50)` | 연락처 |
| `birth_year` | `SMALLINT` | 출생연도 |
| `gender` | `VARCHAR(20)` | 성별 |
| `region_code` | `VARCHAR(50)` | 사용자 지역 코드 |
| `region_name` | `VARCHAR(100)` | 사용자 지역명 |
| `interests` | `JSON` | 관심분야 |
| `notification_email_enabled` | `BOOLEAN` | 이메일 알림 수신 여부 |
| `created_at` | `DATETIME` | 생성 시각 |
| `updated_at` | `DATETIME` | 수정 시각 |

### `company_profiles`

| 컬럼 | 타입 | 설명 |
| --- | --- | --- |
| `id` | `BIGINT` | 기업 프로필 ID |
| `user_id` | `BIGINT` | 사용자 FK |
| `company_name` | `VARCHAR(255)` | 회사명/표시명 |
| `business_registration_no` | `VARCHAR(50)` | 사업자등록번호 |
| `business_type` | `VARCHAR(100)` | 기업 유형 |
| `region_code` | `VARCHAR(50)` | 기업 소재지 코드 |
| `region_name` | `VARCHAR(100)` | 기업 소재지명 |
| `industry_codes` | `TEXT` | 보유 업종코드 목록 |
| `industry_names` | `TEXT` | 보유 업종명 목록 |
| `license_codes` | `TEXT` | 보유 면허코드 목록 |
| `license_names` | `TEXT` | 보유 면허명 목록 |
| `is_youth_company` | `BOOLEAN` | 청년기업 여부 |
| `is_woman_company` | `BOOLEAN` | 여성기업 여부 |
| `is_disabled_company` | `BOOLEAN` | 장애인기업 여부 |
| `created_at` | `DATETIME` | 생성 시각 |
| `updated_at` | `DATETIME` | 수정 시각 |

## 4. 관심 조건/구독

### `user_match_rules`

기존 테이블을 확장해 사용자가 등록한 관심 조건을 저장합니다.

| 컬럼 | 타입 | 설명 |
| --- | --- | --- |
| `id` | `BIGINT` | 조건 ID |
| `user_id` | `BIGINT` | 사용자 FK |
| `rule_name` | `VARCHAR(100)` | 조건명 |
| `include_keywords` | `TEXT` | 포함 키워드 |
| `exclude_keywords` | `TEXT` | 제외 키워드 |
| `biz_types` | `VARCHAR(255)` | 업무 구분 목록 |
| `regions` | `TEXT` | 지역 조건 |
| `industries` | `TEXT` | 업종/면허 조건 |
| `organizations` | `TEXT` | 기관 조건 |
| `product_class_nos` | `TEXT` | 물품/공공조달 분류번호 조건 |
| `min_amount` | `DECIMAL(18,2)` | 최소 금액 |
| `max_amount` | `DECIMAL(18,2)` | 최대 금액 |
| `deadline_days` | `INT` | 마감일까지 남은 일수 조건 |
| `notification_enabled` | `BOOLEAN` | 이 조건으로 알림 발송 여부 |
| `is_active` | `BOOLEAN` | 활성 여부 |
| `created_at` | `DATETIME` | 생성 시각 |
| `updated_at` | `DATETIME` | 수정 시각 |

### `user_search_histories`

| 컬럼 | 타입 | 설명 |
| --- | --- | --- |
| `id` | `BIGINT` | 검색 이력 ID |
| `user_id` | `BIGINT` | 사용자 FK |
| `keyword` | `VARCHAR(255)` | 검색어 |
| `filters` | `JSON` | 사용한 필터 |
| `result_count` | `INT` | 결과 건수 |
| `searched_at` | `DATETIME` | 검색 시각 |

### `saved_bid_notices`

| 컬럼 | 타입 | 설명 |
| --- | --- | --- |
| `id` | `BIGINT` | 관심 공고 ID |
| `user_id` | `BIGINT` | 사용자 FK |
| `bid_notice_id` | `BIGINT` | 공고 FK |
| `memo` | `VARCHAR(500)` | 사용자 메모 |
| `created_at` | `DATETIME` | 저장 시각 |

## 5. 수집/백필 로그

### `collection_run_logs`

| 컬럼 | 타입 | 설명 |
| --- | --- | --- |
| `id` | `BIGINT` | 수집 실행 ID |
| `job_name` | `VARCHAR(100)` | Job 이름 |
| `status` | `VARCHAR(30)` | `RUNNING`, `SUCCESS`, `FAILED`, `PARTIAL` |
| `started_at` | `DATETIME` | 시작 시각 |
| `ended_at` | `DATETIME` | 종료 시각 |
| `query_from` | `DATETIME` | 조회 시작 시각 |
| `query_to` | `DATETIME` | 조회 종료 시각 |
| `fetched_count` | `INT` | 조회 건수 |
| `saved_count` | `INT` | 저장 건수 |
| `skipped_count` | `INT` | 제외 건수 |
| `error_count` | `INT` | 오류 건수 |
| `error_message` | `TEXT` | 오류 메시지 |
| `metadata` | `JSON` | API별 결과 등 부가 정보 |

### `license_backfill_logs`

| 컬럼 | 타입 | 설명 |
| --- | --- | --- |
| `id` | `BIGINT` | 백필 실행 ID |
| `status` | `VARCHAR(30)` | `SUCCESS`, `FAILED`, `PARTIAL` |
| `started_at` | `DATETIME` | 시작 시각 |
| `ended_at` | `DATETIME` | 종료 시각 |
| `target_count` | `INT` | 대상 건수 |
| `enriched_count` | `INT` | 보강 성공 건수 |
| `no_data_count` | `INT` | API 응답 데이터 없음 |
| `error_count` | `INT` | 오류 건수 |
| `sample_errors` | `JSON` | 샘플 오류 |

## 6. 매칭

### `match_results`

| 컬럼 | 타입 | 설명 |
| --- | --- | --- |
| `id` | `BIGINT` | 매칭 결과 ID |
| `bid_notice_id` | `BIGINT` | 공고 FK |
| `user_match_rule_id` | `BIGINT` | 조건 FK |
| `user_id` | `BIGINT` | 사용자 FK |
| `match_score` | `DECIMAL(5,2)` | 일치도 점수 |
| `match_status` | `VARCHAR(30)` | `MATCHED`, `EXCLUDED`, `SENT`, `DISMISSED` |
| `matched_keywords` | `TEXT` | 일치한 키워드 |
| `excluded_keywords` | `TEXT` | 제외 키워드 |
| `match_reason` | `VARCHAR(500)` | 매칭 이유 |
| `matched_at` | `DATETIME` | 매칭 시각 |
| `created_at` | `DATETIME` | 생성 시각 |
| `updated_at` | `DATETIME` | 수정 시각 |

## 7. 이메일 알림

### `email_notification_batches`

| 컬럼 | 타입 | 설명 |
| --- | --- | --- |
| `id` | `BIGINT` | 이메일 배치 ID |
| `user_id` | `BIGINT` | 사용자 FK |
| `subject` | `VARCHAR(255)` | 메일 제목 |
| `total_count` | `INT` | 포함 공고 수 |
| `send_status` | `VARCHAR(30)` | `PENDING`, `SENT`, `FAILED`, `RETRYING` |
| `scheduled_at` | `DATETIME` | 발송 예정 시각 |
| `sent_at` | `DATETIME` | 발송 시각 |
| `error_message` | `TEXT` | 오류 메시지 |
| `created_at` | `DATETIME` | 생성 시각 |

### `email_send_histories`

기존 테이블을 확장해 공고 단위 발송 이력을 저장합니다.

| 컬럼 | 타입 | 설명 |
| --- | --- | --- |
| `id` | `BIGINT` | 발송 이력 ID |
| `user_id` | `BIGINT` | 사용자 FK |
| `match_result_id` | `BIGINT` | 매칭 결과 FK |
| `email_batch_id` | `BIGINT` | 이메일 배치 FK |
| `recipient_email` | `VARCHAR(255)` | 수신 이메일 |
| `subject` | `VARCHAR(255)` | 제목 |
| `send_status` | `VARCHAR(30)` | 발송 상태 |
| `retry_count` | `INT` | 재시도 횟수 |
| `error_message` | `TEXT` | 실패 사유 |
| `sent_at` | `DATETIME` | 발송 시각 |
| `created_at` | `DATETIME` | 생성 시각 |

## 8. 사용자 동의/관리자

### `user_consents`

| 컬럼 | 타입 | 설명 |
| --- | --- | --- |
| `id` | `BIGINT` | 동의 ID |
| `user_id` | `BIGINT` | 사용자 FK |
| `consent_type` | `VARCHAR(50)` | 개인정보, 이메일 수신 등 |
| `is_agreed` | `BOOLEAN` | 동의 여부 |
| `agreed_at` | `DATETIME` | 동의 시각 |
| `revoked_at` | `DATETIME` | 철회 시각 |

### `admin_announcements`

| 컬럼 | 타입 | 설명 |
| --- | --- | --- |
| `id` | `BIGINT` | 공지 ID |
| `title` | `VARCHAR(255)` | 공지 제목 |
| `content` | `TEXT` | 공지 내용 |
| `is_visible` | `BOOLEAN` | 노출 여부 |
| `created_by` | `BIGINT` | 작성자 사용자 ID |
| `created_at` | `DATETIME` | 생성 시각 |
| `updated_at` | `DATETIME` | 수정 시각 |

## 9. 핵심 인덱스

| 테이블 | 인덱스 | 목적 |
| --- | --- | --- |
| `users` | `email` unique | 로그인/중복 가입 방지 |
| `user_match_rules` | `user_id`, `is_active` | 사용자별 활성 조건 조회 |
| `bid_notices` | `biz_type`, `status`, `deadline_at` | 열린 공고 목록/마감 필터 |
| `bid_notices` | `notice_org_name`, `demand_org_name` | 기관 검색 |
| `bid_notices` | `industry_code`, `industry_name` | 업종 필터 |
| `product_categories` | `category_depth_1`, `category_depth_2`, `category_depth_3` | 물품 카테고리 필터 |
| `bid_notices` | `product_category_source_type`, `product_class_no` | 카테고리 조인 |
| `match_results` | `user_id`, `match_status`, `matched_at` | 사용자별 매칭 결과 조회 |
| `email_send_histories` | `user_id`, `send_status` | 알림 이력 조회 |
| `collection_run_logs` | `job_name`, `started_at` | 관리자 수집 로그 조회 |

## 10. 구현 우선순위

1. `users`, `user_profiles`, `company_profiles`
2. `product_categories`, `user_match_rules`
3. `collection_run_logs`, `license_backfill_logs`
4. `match_results`
5. `email_notification_batches`, `email_send_histories`
6. `user_search_histories`, `saved_bid_notices`
7. `user_consents`, `admin_announcements`
