# 예시: DB 스키마 자동 동기화 중 외래 키 추가 실패

## 1. 문제 요약

- 제목: DB 스키마 자동 동기화 중 외래 키 추가 실패
- 프로젝트: Back-End
- 영역: DB, Schema
- 심각도: S3-Medium
- 상태: Resolved
- 발견 시점: TBD
- 담당자: TBD

## 2. 발생 상황

`DB_AUTO_SYNC_SCHEMA=true` 상태에서 백엔드 앱을 실행했을 때 기존 데이터와 새 외래 키 조건이 맞지 않아 외래 키 추가가 실패했습니다.

## 3. 에러 메시지 또는 증상

```text
[schema-sync] Foreign key `fk_match_results_bid_notice_id` was skipped.
```

## 4. 재현 방법

1. 기존 DB에 참조 대상이 없는 `match_results.bid_notice_id` 데이터를 추가합니다.
2. `.env`에 `DB_AUTO_SYNC_SCHEMA=true`를 설정합니다.
3. `python app.py`를 실행합니다.
4. 외래 키 추가가 건너뛰어지는 로그를 확인합니다.

## 5. 원인 분석

| 가설 | 확인 방법 | 결과 |
| --- | --- | --- |
| 기존 데이터가 참조 무결성을 위반함 | `match_results`와 `bid_notices`를 조인해 누락 데이터 확인 | 참조 대상 없는 데이터 발견 |

## 6. 해결 방법

- 잘못된 테스트 데이터를 정리합니다.
- 외래 키 추가 전 데이터 정합성 확인 쿼리를 실행합니다.
- 운영 DB에서는 자동 동기화 대신 수동 마이그레이션으로 처리합니다.

## 7. 검증 결과

```powershell
python -m core.schema_manager
```

스키마 동기화 완료 로그를 확인했습니다.

## 8. 재발 방지

- 스키마 변경 전 데이터 정합성 점검 쿼리 추가
- 운영 환경에서는 `DB_AUTO_SYNC_SCHEMA=false` 유지
- 반복 발생 시 Runbook으로 승격

## 9. 참고 링크

- 관련 파일: `back-end/core/schema_manager.py`
- 관련 설정: `DB_AUTO_SYNC_SCHEMA`
