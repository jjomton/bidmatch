# Trouble Logs 속성

Notion의 `Trouble Logs`는 하나의 데이터베이스 또는 표 형태로 관리합니다.

## 최소 속성

| 속성 | 타입 | 설명 |
| --- | --- | --- |
| `Title` | Title | 문제를 한 줄로 요약 |
| `Project` | Select | `Back-End`, `Front-End`, `Document`, `Infra`, `External-API` |
| `Status` | Select | `Open`, `Investigating`, `Resolved` |
| `Severity` | Select | `High`, `Medium`, `Low` |
| `Owner` | Person | 담당자 |
| `Detected At` | Date | 문제 발견일 |
| `Related PR` | URL | 관련 PR 링크 |

## 선택 속성

| 속성 | 타입 | 설명 |
| --- | --- | --- |
| `Area` | Multi-select | `DB`, `API`, `Email`, `Build`, `Deploy` 등 |
| `Resolved At` | Date | 해결일 |
| `Commit` | Text | 관련 커밋 해시 |
| `Related Files` | Text | 관련 파일 경로 |
| `Recurring` | Checkbox | 재발 문제 여부 |

## 상태 기준

| 상태 | 의미 |
| --- | --- |
| `Open` | 문제 접수 또는 확인 전 |
| `Investigating` | 원인 분석 중 |
| `Resolved` | 해결 및 검증 완료 |

## 심각도 기준

| 등급 | 기준 |
| --- | --- |
| `High` | 주요 기능 중단, 데이터 손실 위험, 배포 불가 |
| `Medium` | 일부 기능 오류, 우회 가능 |
| `Low` | 문서, 개발 편의, 경미한 오류 |
