# BidMatch Back-End

나라장터 공공 API 데이터를 수집하고, 사용자가 등록한 조건과 매칭한 뒤 이메일 알림을 보내기 위한 백엔드 API 서버입니다.

프론트엔드는 React/Vite 애플리케이션에서 담당하고, 백엔드는 JSON API와 배치 작업만 제공합니다.

## 기술 스택

- Python
- Flask
- Flask-CORS
- PyMySQL
- python-dotenv
- MariaDB

## 폴더 구조

```text
back-end/
  app.py                    # Flask 실행 진입점
  app_factory.py            # 앱 팩토리, CORS, Blueprint 등록
  config.py                 # 환경 변수 기반 설정
  requirements.txt          # Python 의존성
  .env.example              # 환경 변수 예시
  api/                      # React 프론트엔드가 호출할 REST API 라우트
  core/                     # DB 연결, 스키마 자동 동기화
  repositories/             # DB 접근 계층
  services/                 # 비즈니스 로직
  jobs/                     # 수집, 매칭, 이메일 발송 배치 작업
  schemas/                  # 요청/응답 검증 스키마
  utils/                    # 공통 유틸리티
```

## 실행 방법

```powershell
cd back-end
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

기본 서버 주소는 `http://localhost:5000`입니다.

## 주요 API

| Method | Path | 설명 |
| --- | --- | --- |
| `GET` | `/api/health` | 서버 상태 확인 |
| `GET` | `/api/bid-notices` | 수집된 열린 입찰 공고 목록 조회 |
| `GET` | `/api/bid-notices/{noticeId}` | 입찰 공고 상세 조회 |
| `GET` | `/api/match-rules` | 사용자 매칭 조건 목록 조회 |
| `POST` | `/api/match-rules` | 사용자 매칭 조건 생성 |
| `PUT` | `/api/match-rules/{ruleId}` | 사용자 매칭 조건 수정 |
| `DELETE` | `/api/match-rules/{ruleId}` | 사용자 매칭 조건 삭제 |
| `GET` | `/api/email-histories` | 이메일 발송 이력 조회 |

## DB 스키마 자동 동기화

백엔드는 `core/schema.py`에 정의된 스키마를 기준으로 현재 MariaDB 상태를 확인하고, 누락된 테이블, 컬럼, 유니크 키, 인덱스, 외래 키를 자동으로 보강할 수 있습니다.

앱 시작 시 자동 동기화를 켜려면 `.env`에 다음 값을 설정합니다.

```env
DB_AUTO_SYNC_SCHEMA=true
```

수동으로 한 번만 실행하려면 다음 명령을 사용합니다.

```powershell
cd back-end
python -m core.schema_manager
```

자동 동기화는 기존 컬럼 삭제, 기존 컬럼 타입 변경, 기존 데이터 삭제를 수행하지 않습니다.

## 나라장터 열린 공고 수집

백엔드에는 나라장터 입찰공고정보서비스에서 현재 열려있는 공고만 조회해 MariaDB에 저장하는 수집 Job이 포함되어 있습니다.

실행 명령:

```powershell
cd back-end
python -m jobs.collect_bid_notices_job
```

수집 기준:

- `G2B_API_KEY`로 나라장터 OpenAPI를 호출합니다.
- 기본 수집 API는 용역, 물품 공고입니다.
- `bidClseDt`가 현재 시각보다 미래인 공고만 `OPEN` 상태로 저장합니다.
- 이미 저장된 공고는 `bid_notice_no`, `bid_notice_ord`, `biz_type` 기준으로 갱신합니다.
- 기존에 저장된 공고 중 마감 시간이 지난 공고는 `CLOSED` 상태로 변경합니다.
- 프론트엔드는 `detail_url`을 공고명 링크로 사용해 나라장터 상세 화면으로 이동합니다.

1시간마다 수집하려면 Cloudtype의 스케줄 실행 기능 또는 외부 스케줄러에서 위 Job 명령을 주기적으로 실행하도록 설정합니다.

## 환경 변수

| 이름 | 설명 | 예시 |
| --- | --- | --- |
| `FLASK_ENV` | Flask 실행 환경 | `development` |
| `SECRET_KEY` | Flask secret key | `change-me` |
| `DB_HOST` | MariaDB 호스트 | `mariadb.example.com` |
| `DB_NAME` | MariaDB 데이터베이스 이름 | `bidmatch` |
| `DB_USER` | MariaDB 사용자 | `bidmatch_user` |
| `DB_PASSWORD` | MariaDB 비밀번호 | `strong-password` |
| `DB_PORT` | MariaDB 포트 | `3306` |
| `DB_AUTO_SYNC_SCHEMA` | 실행 시 스키마 자동 보강 여부 | `true` |
| `CORS_ORIGINS` | 허용할 React Origin 목록 | `http://localhost:5173,http://localhost:3000` |
| `G2B_API_KEY` | 공공데이터포털 나라장터 API 인증키 | `발급받은 ServiceKey` |
| `G2B_API_BASE_URL` | 나라장터 입찰공고정보서비스 기본 URL | `http://apis.data.go.kr/1230000/ad/BidPublicInfoService` |
| `G2B_COLLECT_ENDPOINTS` | 수집할 API 목록 | `getBidPblancListInfoServc,getBidPblancListInfoThng` |
| `G2B_LOOKBACK_HOURS` | 매 수집 시 다시 조회할 시간 범위 | `2` |
| `G2B_NUM_OF_ROWS` | API 페이지당 조회 건수 | `100` |
| `SMTP_HOST` | 이메일 SMTP 호스트 | `smtp.example.com` |
| `SMTP_PORT` | 이메일 SMTP 포트 | `587` |
| `SMTP_USER` | 이메일 발송 계정 | `noreply@example.com` |
| `SMTP_PASSWORD` | 이메일 발송 비밀번호 | `password` |
| `SMTP_FROM` | 발신 이메일 주소 | `noreply@example.com` |

## 브랜치 전략

이 프로젝트는 `master -> develop -> 개인 개발 브랜치` 흐름으로 관리합니다.

| 브랜치 | 용도 |
| --- | --- |
| `master` | 배포 가능한 안정 버전 |
| `develop` | 다음 배포를 준비하는 통합 개발 브랜치 |
| 개인 개발 브랜치 | 기능 구현, 버그 수정, 문서 작업 |

개인 브랜치 예시:

```text
feature/minsu-g2b-collector
fix/jiyoon-email-retry
docs/hana-branch-strategy
```

## G2B Collection Check Tips

If `python -m jobs.collect_bid_notices_job` returns `fetched: 0`, the API call may still be successful.

The default `G2B_LOOKBACK_HOURS=2` only searches notices registered in the last 2 hours. For the first integration test, increase the value:

```env
G2B_LOOKBACK_HOURS=24
```

If it is still 0, try:

```env
G2B_LOOKBACK_HOURS=72
G2B_LOOKBACK_HOURS=168
```

The collector output includes `result_code`, `result_message`, `total_count`, `query_from`, and `query_to` so you can distinguish a normal no-data response from an API error.

`G2B_INQRY_DIV` controls the 나라장터 query type. The default is:

```env
G2B_INQRY_DIV=1
```

## Hourly Collector Worker

기본 공고 수집은 업종/면허 백필과 분리해서 실행합니다. 아래 worker는 최근 2시간 데이터를 1시간마다 자동 수집합니다.

```powershell
python -m jobs.hourly_collect_bid_notices_worker
```

운영 환경 변수:

```env
G2B_LOOKBACK_HOURS=2
G2B_COLLECT_INTERVAL_SECONDS=3600
G2B_COLLECT_RUN_ON_START=true
G2B_EMBEDDED_WORKER_ENABLED=false
G2B_BACKFILL_AFTER_COLLECT=true
G2B_LICENSE_BACKFILL_LIMIT=20
```

동작 방식:

- 시작 시 `G2B_COLLECT_RUN_ON_START=true`이면 즉시 1회 수집합니다.
- 이후 `G2B_COLLECT_INTERVAL_SECONDS`마다 반복 실행합니다.
- 기본값은 3600초, 즉 1시간입니다.
- 각 실행은 현재 시각 기준 최근 `G2B_LOOKBACK_HOURS` 시간 범위를 조회합니다.
- `G2B_BACKFILL_AFTER_COLLECT=true`이면 기본 수집 후 업종/면허 보강도 함께 실행합니다.
- 보강은 API 한도를 고려해 `G2B_LICENSE_BACKFILL_LIMIT` 건수만 처리합니다.
- 보강을 완전히 분리하고 싶으면 `G2B_BACKFILL_AFTER_COLLECT=false`로 설정하고 `python -m jobs.backfill_license_limits_job`를 별도 실행합니다.

Cloudtype에서는 웹 서버 프로세스와 별도로 worker 프로세스 실행 명령을 분리해서 두는 방식을 권장합니다.

### Run Worker With `app.py`

개발 환경이나 단일 인스턴스 운영에서 웹 서버와 수집 worker를 같이 실행하고 싶으면 `.env`에 아래 값을 추가합니다.

```env
G2B_EMBEDDED_WORKER_ENABLED=true
```

그 다음 평소처럼 실행하면 됩니다.

```powershell
python app.py
```

이 옵션이 켜져 있으면 Flask 서버 시작 시 백그라운드 스레드로 `hourly_collect_bid_notices_worker`가 함께 실행됩니다. `G2B_COLLECT_RUN_ON_START=true`이면 서버 시작 직후 1회 수집하고, 이후 `G2B_COLLECT_INTERVAL_SECONDS`마다 반복합니다.

운영 서버를 여러 인스턴스로 늘릴 경우에는 각 인스턴스에서 worker가 중복 실행될 수 있으므로 `G2B_EMBEDDED_WORKER_ENABLED=false`로 두고 별도 worker 프로세스를 사용하는 방식을 권장합니다.
