# 내부 API 명세

## 사용자 조건

| Method | Path | 설명 |
| --- | --- | --- |
| `GET` | `/api/match-rules` | 사용자 관심 조건 목록 조회 |
| `POST` | `/api/match-rules` | 사용자 관심 조건 등록 |
| `PUT` | `/api/match-rules/{id}` | 사용자 관심 조건 수정 |
| `DELETE` | `/api/match-rules/{id}` | 사용자 관심 조건 삭제 |

## 입찰 공고

| Method | Path | 설명 |
| --- | --- | --- |
| `GET` | `/api/bid-notices` | 수집된 입찰 공고 조회 |
| `GET` | `/api/bid-notices/{id}` | 입찰 공고 상세 조회 |

## 알림 이력

| Method | Path | 설명 |
| --- | --- | --- |
| `GET` | `/api/email-histories` | 이메일 발송 이력 조회 |

## TBD

- 인증/인가 헤더
- 페이지네이션 형식
- 공통 응답 포맷
