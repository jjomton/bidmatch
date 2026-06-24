# PRD v0.3 — 나라장터 입찰정보 수집·추천·알림 서비스 (포트폴리오형 MVP)

## 0) 문서 정보
- **버전**: v0.3
- **목표**: 4일 내 배포 가능한 MVP + 상시 접속 가능한 포트폴리오 서비스
- **운영 원칙**: 무료 클라우드 우선, 서버리스/스케줄 분리, 최소 기능 우선

## 1) 문제 정의
나라장터 입찰공고는 공식 시스템에서 확인 가능하지만, 실무자는 반복 조회·조건 관리·누락 방지에 시간을 많이 소모한다.  
본 서비스는 공고 데이터를 자동 수집·적재하고 사용자 맞춤 조건으로 선별하여 이메일 알림으로 제공한다.

## 2) 제품 목표
- 나라장터 공고 데이터의 안정적 동기화(일 1회 + 보정 수집)
- 사용자별 맞춤 공고 탐색 비용 절감
- 이메일 알림 자동화
- 관리자 화면을 통한 운영 가시성 확보
- 취업 포트폴리오 관점에서 상시 접속 가능한 배포 상태 유지

## 3) 사용자
- **일반 사용자**
  - 회원가입 후 관심 키워드/조건을 등록하고 이메일 알림 수신
- **관리자**
  - 수집/알림 운영 상태 점검
  - 데이터 품질 및 사용자 현황 모니터링
  - (옵션) AI 분석 기능 활용

## 4) 범위

### In Scope (MVP)
- 회원가입/로그인/구독관리
- 나라장터 데이터 수집/적재/보정
- 필터 기반 공고 매칭
- 이메일 일간 알림
- 관리자 운영 대시보드(기본)

### Out of Scope (MVP 제외)
- 카카오 알림톡 정식 발송
- 고도 추천 모델
- 팀 협업/권한 세분화
- 다중 외부 조달원 대규모 통합

## 5) 시스템 스택 및 아키텍처
- **Frontend**: React + Vite + Netlify
- **DB/Auth**: Supabase (Postgres + Auth)
- **API/서버리스**: Supabase Edge Functions
- **배치 워커**: GitHub Actions (스케줄 크론)
- **알림**: 이메일 (Resend 또는 SendGrid free tier)
- **모니터링**: GitHub Actions 로그 + Supabase 로그

### 데이터 흐름
1. GitHub Actions 스케줄 실행
2. 나라장터 API 호출
3. `raw_api_payload` 저장
4. 정규화/업서트(`bid_notice`)
5. 사용자 필터 매칭
6. 이메일 발송 및 발송 로그 저장
7. 웹/관리자 화면에서 조회

## 6) 요구사항

### 6.1 핵심 요구사항 (Must Have)

#### A. 인증/회원
- **AUTH-01** 이메일 회원가입/로그인/로그아웃
- **AUTH-02** 이메일 인증(verification)
- **AUTH-03** 비밀번호 재설정
- **AUTH-04** 기본 프로필 조회/수정
- **AUTH-05** 약관/개인정보/마케팅(이메일) 동의 이력 저장

#### B. 구독/필터
- **SUB-01** 구독 설정 CRUD (포함/제외 키워드, 업무구분, 기관)
- **SUB-02** 알림 빈도 설정(초기: 일 1회)
- **SUB-03** 구독 해지/재개
- **SUB-04** 내 알림 이력 조회

#### C. 데이터 수집/적재
- **ING-01** 일 1회 배치 수집
- **ING-02** 최근 1~3일 보정 수집
- **ING-03** Raw + 정규화 저장 분리
- **ING-04** 유니크키 기반 Upsert(중복 방지)
- **ING-05** 수집 실행 로그 저장(시작/종료/건수/오류)

#### D. 매칭/알림
- **NOTI-01** 사용자 필터 매칭 로직
- **NOTI-02** 이메일 일간 Digest 발송
- **NOTI-03** 발송 결과 로깅(성공/실패/오류사유)
- **NOTI-04** 실패 건 재시도(최소 1회)

#### E. 관리자
- **ADM-01** 사용자 목록/구독 상태 조회
- **ADM-02** 배치 실행 현황 조회
- **ADM-03** 데이터 품질 지표 조회(중복/누락 의심/파싱 실패)
- **ADM-04** 알림 발송 현황 조회
- **ADM-05** 운영 공지 관리(간단 텍스트)

### 6.2 옵션 요구사항 (Could Have)

#### A. 사용자 기능
- **OPT-U1** 소셜 로그인
- **OPT-U2** 키워드 추천/템플릿
- **OPT-U3** 알림 주기 세분화(실시간/주간)

#### B. 관리자 AI/데이터 활용
- **OPT-AI1 공고 요약**
  - 공고문 핵심 3줄 요약 자동 생성
- **OPT-AI2 자동 태깅/분류**
  - 예: 홍보/마케팅/IT/디자인 등 카테고리 분류
- **OPT-AI3 관련도 점수(relevance)**
  - 사용자 필터 대비 적합도 점수화
- **OPT-AI4 트렌드 인사이트**
  - 기관·업무구분·키워드 증감 리포트
- **OPT-AI5 유사 공고 군집화**
  - 중복/유사 공고 묶음으로 노이즈 감소

## 7) 데이터 모델 (MVP 최소)
- `raw_api_payload`
  - `id`, `source_service`, `endpoint`, `request_params`, `response_json`, `response_hash`, `fetched_at`
- `bid_notice`
  - `id`, `bid_notice_no`, `bid_notice_ord`, `biz_type`, `title`, `notice_org`, `demand_org`, `notice_status`, `notice_at`, `close_at`, `open_at`, `amount_fields`, `raw_payload_id`, `created_at`, `updated_at`
  - Unique: `(bid_notice_no, bid_notice_ord, biz_type)`
- `ingestion_run_log`
  - `id`, `started_at`, `finished_at`, `status`, `fetched_count`, `upsert_count`, `error_message`
- `user_profile`
  - `id`, `email`, `display_name`, `company_name`, `created_at`
- `user_filter_rule`
  - `id`, `user_id`, `include_keywords`, `exclude_keywords`, `biz_types`, `organizations`, `is_active`
- `notification_log`
  - `id`, `user_id`, `channel`, `sent_at`, `matched_count`, `status`, `error_message`
- `consent_log`
  - `id`, `user_id`, `consent_type`, `agreed`, `agreed_at`

## 8) 비기능 요구사항
- **가용성**: 배포 URL 상시 접속 가능
- **신뢰성**: 배치 실패 시 원인 확인 가능
- **정확성**: 논리적 중복 0 목표, 누락 의심 탐지 가능
- **보안**: 키/시크릿은 환경변수(Secrets)로만 관리
- **감사추적**: raw ↔ 정규화 ↔ 알림 로그 연결 가능

## 9) KPI
- 배치 성공률
- 일간 수집 건수
- 중복 삽입 건수(목표 0)
- 알림 발송 성공률
- 알림 오픈율/클릭률(가능 시)
- 활성 구독 사용자 수
- 관리자 처리 시간(오류 인지→조치)

## 10) 일정 (4일 배포 기준)

### Day 1
- Supabase 스키마/권한
- Auth 기본 플로우
- 수집 스크립트 초안(raw 저장)

### Day 2
- 정규화/upsert + ingestion 로그
- GitHub Actions 스케줄 설정
- 사용자 필터 테이블/API

### Day 3
- React UI(회원/필터/공고목록)
- Netlify 배포
- 관리자 기본 화면(배치/발송 상태)

### Day 4
- 이메일 Digest 발송
- 통합 테스트/버그픽스
- README/아키텍처/시연 시나리오 정리

## 11) 리스크 및 대응
- **카카오 알림톡 미적용**: MVP는 이메일 우선, 알림톡은 옵션 기능으로 분리
- **무료 플랜 제한**: 일 1회 수집 + 보정 범위 제한으로 비용/쿼터 관리
- **API 응답 변형**: raw 저장 및 파서 예외 처리
- **배치 실패**: Actions 재실행 + 로그 기반 복구

## 12) 향후 확장 (포트폴리오 강화 포인트)
1. AI 요약 + 자동 태깅(관리자 검수 포함)
2. 관련도 점수 기반 개인화 정렬
3. 트렌드 대시보드(주간 리포트 자동 생성)
4. 카카오 알림톡 정식 연동(승인 절차 완료 후)

