# Notion 트러블슈팅 구조 생성 템플릿

아래 내용을 복사해서 다른 프로젝트의 Notion 트러블슈팅 공간을 만들 때 사용합니다.

## 1. 최상위 페이지 생성

페이지 이름:

```text
[프로젝트명] Troubleshooting
```

페이지 내용:

```markdown
# Overview

[프로젝트명] 프로젝트의 트러블슈팅 기록 허브입니다.

실제 문제 기록은 Trouble Logs에 작성하고, 프로젝트 구분은 Project 속성으로 관리합니다.

# Structure

- Dashboard
- Trouble Logs
- Templates

# Operating Rules

- 문제 하나당 Trouble Log 하나를 생성합니다.
- 해결 전이라도 원인 분석, 시도한 방법, 결과를 남깁니다.
- 같은 문제가 반복되면 기존 기록에 발생 이력을 추가합니다.
- 반복 대응이 필요하면 Runbook 문서로 분리합니다.
- 코드 수정이 포함된 경우 커밋 해시, PR 링크, 관련 파일 경로를 함께 남깁니다.
```

## 2. 하위 페이지 생성

```text
Dashboard
Trouble Logs
Templates
```

## 3. Dashboard 내용

```markdown
# Dashboard

## Open Issues

아직 해결되지 않은 문제를 확인합니다.

## Recently Resolved

최근 해결된 문제를 확인합니다.

## Recurring Problems

반복 발생하는 문제를 확인합니다.

## By Project

프로젝트별 문제 현황을 확인합니다.
```

## 4. Trouble Logs 속성

Notion 데이터베이스로 만들 경우 아래 속성을 추가합니다.

| 속성 | 타입 | 값 |
| --- | --- | --- |
| `Title` | Title | 문제 제목 |
| `Project` | Select | `Back-End`, `Front-End`, `Document`, `Infra`, `External-API` |
| `Status` | Select | `Open`, `Investigating`, `Resolved` |
| `Severity` | Select | `High`, `Medium`, `Low` |
| `Owner` | Person | 담당자 |
| `Detected At` | Date | 발견일 |
| `Related PR` | URL | 관련 PR |

## 5. Templates 하위 문서

```text
Trouble Log Template
Runbook Template
```

## 6. Trouble Log Template

```markdown
# 1. 문제 요약

- 제목:
- 프로젝트:
- 심각도:
- 상태:
- 발견 시점:
- 담당자:

# 2. 발생 상황

# 3. 에러 메시지 또는 증상

# 4. 재현 방법

1. 
2. 
3. 

# 5. 원인 분석

# 6. 해결 방법

# 7. 검증 결과

# 8. 재발 방지

# 9. 참고 링크
```

## 7. Runbook Template

```markdown
# 목적

# 적용 대상

# 증상

# 빠른 확인

1. 로그 확인
2. 환경 변수 확인
3. DB 상태 확인
4. 외부 API 상태 확인

# 대응 절차

1. 임시 조치
2. 원인 확인
3. 수정 적용
4. 재시작 또는 재배포
5. 복구 확인

# 에스컬레이션 기준

# 변경 이력
```
