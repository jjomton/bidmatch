# Notion 구조

## 최상위 페이지

```text
BidMatch Troubleshooting
```

프로젝트 전체의 장애, 오류, 해결 기록을 모으는 허브 페이지입니다.

## 단순 구조

```text
BidMatch Troubleshooting
  Dashboard
  Trouble Logs
  Templates
```

## Dashboard

트러블슈팅 현황을 빠르게 확인하는 페이지입니다.

권장 섹션:

- Open Issues: 아직 해결되지 않은 문제
- Recently Resolved: 최근 해결한 문제
- Recurring Problems: 반복 발생한 문제
- By Project: 프로젝트별 문제 요약

## Trouble Logs

모든 문제 기록을 한 곳에 저장합니다.

프로젝트별 페이지를 따로 만들지 않고, `Project` 속성으로 구분합니다.

권장 `Project` 값:

- `Back-End`
- `Front-End`
- `Document`
- `Infra`
- `External-API`

## Templates

기록 작성에 사용할 템플릿을 모아둡니다.

권장 템플릿:

- Trouble Log Template
- Runbook Template

## 확장 기준

기록이 많아져서 한 페이지에서 관리하기 어려워지면 그때 프로젝트별 페이지를 분리합니다.

확장 예시:

```text
BidMatch Troubleshooting
  Dashboard
  Trouble Logs
  Templates
  Archive
  Back-End
  Front-End
```
