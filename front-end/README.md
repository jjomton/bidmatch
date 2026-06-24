# BidMatch Front-End

BidMatch의 React 기반 프론트엔드 목업입니다. 현재는 요구사항과 디자인 시안을 바탕으로 만든 단일 대시보드 화면만 포함합니다.

## 버전 기준

| 항목 | 기준 |
| --- | --- |
| Node.js | `20.19.x LTS` 권장 |
| Build Tool | Vite `5.4.11` |
| UI Library | React `18.3.1` |
| Language | JavaScript JSX |
| Backend 연동 | Flask API 서버 `http://localhost:5000` 기준 |
| Python 호환 | 백엔드는 Python 3.12 계열을 기준으로 하며, 프론트엔드는 API 경로만 환경 변수로 연결 |

프론트엔드는 브라우저에서 실행되므로 Python 런타임과 직접 충돌하지 않습니다. 백엔드 Python 버전과의 호환은 API 경로, CORS, JSON 응답 형식을 기준으로 맞춥니다.

React 자체는 Node.js 버전에 직접 묶이지 않지만, Vite 개발 서버와 빌드 도구는 Node.js를 사용합니다. 팀 개발 환경은 안정성을 위해 Node.js `20.19.x LTS`를 권장합니다.

현재 Codex 번들 Node.js는 `v24.14.0`이지만, 실제 팀 개발과 배포 환경에서는 LTS 버전인 Node.js 20 계열을 기준으로 맞춥니다.

의존성은 재현 가능한 설치를 위해 정확한 버전으로 고정했습니다. `npm install` 후 생성되는 lock 파일을 기준으로 팀원이 동일한 버전을 사용합니다.

## 폴더 구조

```text
front-end/
  index.html
  package.json
  README.md
  .env.example
  .gitignore
  src/
    main.jsx
    App.jsx
    styles.css
    assets/
    components/
    constants/
    hooks/
    mocks/
    pages/
    routes/
    services/
    styles/
    types/
    utils/
```

## 확장용 폴더 역할

| 폴더 | 역할 |
| --- | --- |
| `src/assets` | 이미지, 아이콘, 정적 리소스 |
| `src/components` | 여러 화면에서 재사용하는 UI 컴포넌트 |
| `src/constants` | 라우트, 상태값, 필터 옵션 등 공통 상수 |
| `src/hooks` | API 호출 상태, 사용자 입력 상태 등 재사용 Hook |
| `src/mocks` | 백엔드 연동 전 사용할 샘플 데이터 |
| `src/pages` | 라우팅 단위 화면 컴포넌트 |
| `src/routes` | React Router 도입 후 라우트 설정 |
| `src/services` | 백엔드 API 호출 함수 |
| `src/styles` | 디자인 토큰, 레이아웃, 컴포넌트 스타일 |
| `src/types` | API 응답 구조와 데이터 타입 문서화 |
| `src/utils` | 날짜, 금액, 검증 등 순수 유틸리티 |

## 실행 방법

```powershell
cd front-end
npm install
npm run dev
```

기본 Vite 개발 서버는 보통 `http://localhost:5173`에서 실행됩니다.

## 환경 변수

실제 비밀값은 저장소에 올리지 않습니다. API 서버 주소만 `.env`에 설정합니다.

```env
VITE_API_BASE_URL=http://localhost:5000
```

`.env.example`을 참고해 로컬에서 `.env`를 생성합니다.

## 보안 기준

- `.env`와 실제 비밀값은 Git에 올리지 않습니다.
- 클라이언트 코드에는 API Key, DB 비밀번호, SMTP 비밀번호를 넣지 않습니다.
- 브라우저에서 노출되어도 되는 값만 `VITE_` 접두사 환경 변수로 사용합니다.
- 사용자 입력값은 화면에 직접 HTML로 삽입하지 않습니다.
- 현재 목업은 `dangerouslySetInnerHTML`을 사용하지 않습니다.
- 인증 토큰 저장 방식은 실제 인증 구현 단계에서 재검토합니다.

## 현재 목업 범위

- 사용자 대시보드
- 추천 공고 목록
- 관심 조건 요약
- 마감일 달력 요약
- 추천 검색어
- 관리자 운영 상태 요약

## 개발 방향

### 1단계: 목업 안정화

- 현재 `src/App.jsx`의 단일 화면을 유지하면서 디자인 톤을 확정합니다.
- 공고, 지표, 관심 조건 샘플 데이터는 `src/mocks`로 분리합니다.
- 반복되는 UI는 `src/components`로 분리합니다.

### 2단계: 화면 분리

- `src/pages`에 화면 단위 컴포넌트를 만듭니다.
- React Router 도입 후 `src/routes`에서 경로를 관리합니다.
- 우선순위 화면은 `Dashboard`, `NoticeSearch`, `MatchRules`, `NoticeDetail`, `AdminDashboard`입니다.

### 3단계: 백엔드 API 연동

- `src/services/apiClient.js`에서 `VITE_API_BASE_URL`을 기준으로 공통 fetch 함수를 만듭니다.
- 공고, 관심 조건, 알림 이력, 관리자 로그 API를 서비스별로 분리합니다.
- API 에러는 사용자 메시지와 개발 로그를 구분해 처리합니다.

### 4단계: 인증과 권한

- 로그인/회원가입 화면을 추가합니다.
- 인증 토큰 저장 위치와 만료 처리 정책을 확정합니다.
- 관리자 화면은 관리자 권한이 확인된 사용자만 접근하도록 제한합니다.

### 5단계: 품질 보강

- 주요 컴포넌트 접근성 속성을 점검합니다.
- 테이블, 필터, 폼의 모바일 레이아웃을 보완합니다.
- 빌드와 배포 전 `npm run build`를 통과해야 합니다.

## 다음 작업 체크리스트

1. React Router 도입 후 화면 분리
2. 공고 검색/목록 페이지 구현
3. 관심 조건 관리 페이지 구현
4. 로그인/회원가입 화면 구현
5. 백엔드 `/api/*` 연동
6. API 응답 타입과 에러 처리 정책 정리
