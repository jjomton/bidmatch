# Hooks

화면 상태, API 호출 상태, 사용자 입력 상태를 재사용 가능한 React Hook으로 분리합니다.

## 예정 Hook

- `useNotices`: 공고 목록 조회와 검색 조건 상태
- `useMatchRules`: 관심 조건 목록과 CRUD 상태
- `useNotifications`: 알림 이력 조회 상태
- `useAuth`: 로그인 사용자와 인증 상태
- `useAdminLogs`: 관리자 로그 조회 상태

## 작성 기준

- Hook은 UI 렌더링보다 상태와 동작에 집중합니다.
- fetch 호출은 `services`를 통해 수행합니다.
- 에러 메시지는 사용자에게 보여줄 수 있는 형태로 정리합니다.
