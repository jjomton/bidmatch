# Services

백엔드 API 호출과 외부 연동 코드를 보관합니다.

## 예정 파일

- `apiClient.js`: 공통 fetch 래퍼, base URL, 공통 에러 처리
- `noticeService.js`: 공고 목록/상세/검색 API
- `matchRuleService.js`: 관심 조건 CRUD API
- `notificationService.js`: 알림 이력 API
- `adminService.js`: 관리자 수집/발송 로그 API
- `authService.js`: 로그인, 회원가입, 토큰 검증 API

## 보안 기준

- API Key, DB 비밀번호, SMTP 비밀번호를 프론트 코드에 넣지 않습니다.
- 브라우저에 노출되어도 되는 값만 `VITE_` 환경 변수로 사용합니다.
- 인증 토큰 처리 방식은 실제 인증 구현 시 별도 정책으로 확정합니다.
