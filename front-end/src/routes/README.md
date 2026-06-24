# Routes

라우팅 설정을 보관합니다.

## 예정 구조

React Router 도입 후 다음 경로를 기준으로 구성합니다.

```text
/login
/signup
/dashboard
/notices
/notices/:noticeId
/match-rules
/calendar
/notifications
/profile
/admin
/admin/ingestion-logs
/admin/notification-logs
```

## 현재 상태

아직 `react-router-dom` 의존성은 추가하지 않았습니다. 화면 분리 시점에 도입합니다.
