# 트러블슈팅 기록 운영

트러블슈팅 기록은 Notion을 기준 저장소로 사용합니다. 저장소에는 Notion 구조, 작성 규칙, 템플릿만 관리합니다.

초기에는 프로젝트별 폴더를 나누지 않고, 하나의 `Trouble Logs`에서 `Project` 속성으로 분류합니다.

## 추천 Notion 구조

```text
BidMatch Troubleshooting
  Dashboard
  Trouble Logs
  Templates
```

## 페이지 역할

| 페이지 | 목적 |
| --- | --- |
| `Dashboard` | 열려 있는 문제, 최근 해결한 문제, 반복 문제를 한눈에 확인 |
| `Trouble Logs` | 모든 트러블슈팅 기록을 한 곳에 저장 |
| `Templates` | 기록 작성에 사용할 공통 템플릿 보관 |

## 문서 구성

| 문서 | 목적 |
| --- | --- |
| `notion-structure.md` | 단순 Notion 구조와 운영 방식 |
| `database-properties.md` | Trouble Logs에 둘 최소 속성 |
| `trouble-log-template.md` | 개별 문제 기록 템플릿 |
| `runbook-template.md` | 반복 장애 대응 절차 템플릿 |
| `notion-setup-template.md` | 다른 사람이 같은 구조를 만들 때 사용할 템플릿 |
| `example-trouble-log.md` | 작성 예시 |

## 운영 원칙

- 문제 하나당 Trouble Log 하나를 생성합니다.
- 프로젝트 구분은 폴더가 아니라 `Project` 속성으로 관리합니다.
- 해결 전이라도 원인 분석, 시도한 방법, 결과를 남깁니다.
- 같은 문제가 반복되면 기존 기록에 발생 이력을 추가합니다.
- 반복 대응이 필요하면 `Templates`의 Runbook 형식으로 별도 문서를 만듭니다.
- 코드 수정이 포함된 경우 커밋 해시, PR 링크, 관련 파일 경로를 함께 남깁니다.
