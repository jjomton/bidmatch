# 나라장터 1시간 자동 수집 운영 문서

이 문서는 Cloudtype 또는 서버 환경에서 나라장터 공고 수집 worker를 운영하는 기준을 정리합니다.

## 1. 실행 명령

```powershell
python -m jobs.hourly_collect_bid_notices_worker
```

worker는 종료되지 않고 계속 실행되며, 설정된 주기마다 공고 수집을 반복합니다.

## 2. 기본 동작

| 단계 | 설명 |
| --- | --- |
| 1 | 시작 시 스키마 자동 동기화 실행 |
| 2 | 최근 2시간의 용역/물품 공고 조회 |
| 3 | 열린 공고만 `bid_notices`에 업서트 |
| 4 | 마감된 기존 공고를 `CLOSED` 상태로 변경 |
| 5 | 설정이 켜져 있으면 업종/면허 제한 백필 실행 |
| 6 | 1시간 대기 후 반복 |

## 3. 운영 환경 변수

```env
G2B_LOOKBACK_HOURS=2
G2B_COLLECT_INTERVAL_SECONDS=3600
G2B_COLLECT_RUN_ON_START=true
G2B_BACKFILL_AFTER_COLLECT=true
G2B_LICENSE_BACKFILL_LIMIT=20
G2B_REQUEST_DELAY_SECONDS=1.0
G2B_MAX_RETRIES=3
G2B_RETRY_BASE_DELAY_SECONDS=5.0
```

## 4. API 한도 보호

업종/면허 보강 API는 공고별로 추가 호출되므로 API 키 소모가 큽니다.

권장 설정:

| 상황 | 설정 |
| --- | --- |
| 일반 운영 | `G2B_LICENSE_BACKFILL_LIMIT=20` |
| 429 발생 | `G2B_LICENSE_BACKFILL_LIMIT=10` |
| 429 반복 | `G2B_REQUEST_DELAY_SECONDS=2.0` |
| 백필 중지 | `G2B_BACKFILL_AFTER_COLLECT=false` |

## 5. Cloudtype 운영 방식

Cloudtype에서는 웹 서버와 worker를 분리해서 실행하는 구성을 권장합니다.

| 프로세스 | 명령 |
| --- | --- |
| Web API | `python app.py` |
| Collector Worker | `python -m jobs.hourly_collect_bid_notices_worker` |

## 6. 수동 점검 명령

수동 1회 수집:

```powershell
python -m jobs.collect_bid_notices_job
```

업종/면허 백필:

```powershell
python -m jobs.backfill_license_limits_job
```

특정 공고 면허제한 API 확인:

```powershell
python -m jobs.debug_license_limit_job R26BK01574802 000
```

## 7. 확인 포인트

worker 출력에서 확인할 값:

| 출력 값 | 의미 |
| --- | --- |
| `collection.collected` | API에서 가져온 공고 수 |
| `collection.saved_open` | 열린 공고 저장 수 |
| `collection.marked_closed` | 마감 처리된 공고 수 |
| `license_backfill.targets` | 보강 대상 수 |
| `license_backfill.enriched` | 보강 성공 수 |
| `license_backfill.errors` | 보강 실패 수 |

`errors`에 `HTTP Error 429`가 나오면 API 호출 한도에 걸린 것이므로 백필 건수와 요청 간격을 줄입니다.
