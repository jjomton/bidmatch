# 나라장터 입찰공고정보서비스 OpenAPI 분석

원본 문서: `01-requirements/조달청_OpenAPI참고자료_나라장터_입찰공고정보서비스_1.2.docx`

## 1. 문서 요약

- 서비스명: 나라장터 입찰공고정보서비스
- 서비스 ID: `BidPublicInfoService`
- 인증 방식: 공공데이터포털 `ServiceKey`
- 응답 형식: 기본 XML, `type=json` 지정 시 JSON 응답 가능
- 주요 제공 정보:
  - 물품, 용역, 공사, 외자 입찰공고 목록
  - 나라장터 검색조건 기반 입찰공고 조회
  - 기초금액 정보
  - 면허제한 정보
  - 참가가능지역 정보
  - 구매대상물품 정보
  - 첨부파일 정보
  - 변경이력 정보
- 문서 버전: `1.2`
- 문서상 주요 변경일: `2026.04.10`

## 2. 공통 요청 파라미터

대부분의 오퍼레이션에서 공통적으로 사용하는 요청값입니다.

| 파라미터 | 설명 | 필수 | 활용 |
| --- | --- | --- | --- |
| `ServiceKey` | 공공데이터포털 인증키 | 필수 | 백엔드 환경 변수로만 관리 |
| `numOfRows` | 한 페이지 결과 수 | 필수 | 배치 수집 페이지 크기 |
| `pageNo` | 페이지 번호 | 필수 | 페이지네이션 수집 |
| `type` | 응답 타입. JSON 사용 시 `json` | 선택 | 백엔드 파싱 단순화를 위해 `json` 사용 권장 |
| `inqryDiv` | 조회 구분 | 필수 | 등록일시, 변경일시, 공고게시일시, 개찰일시, 입찰공고번호 조회 구분 |
| `inqryBgnDt` | 조회 시작 일시 `YYYYMMDDHHMM` | 조건부 | 일 1회/시간별/보정 수집 시작값 |
| `inqryEndDt` | 조회 종료 일시 `YYYYMMDDHHMM` | 조건부 | 일 1회/시간별/보정 수집 종료값 |
| `bidNtceNo` | 입찰공고번호 | 조건부 | 상세/연관 정보 조회 키 |
| `bidNtceOrd` | 입찰공고차수 | 조건부 | 공고별 보조 정보 조회 키 |

## 3. 검색조건 계열 주요 파라미터

`나라장터검색조건에 의한 입찰공고*조회` 계열에서 사용자 검색/필터에 활용하기 좋은 값입니다.

| 파라미터 | 설명 | BidMatch 활용 |
| --- | --- | --- |
| `bidNtceNm` | 입찰공고명 | 키워드 검색, 관심 조건 매칭 |
| `ntceInsttCd` | 공고기관코드 | 기관 코드 필터 |
| `ntceInsttNm` | 공고기관명 | 기관명 검색/필터 |
| `dminsttCd` | 수요기관코드 | 수요기관 필터 |
| `dminsttNm` | 수요기관명 | 수요기관명 검색 |
| `refNo` | 참조번호 | 관리자/상세 검색 보조 |
| `prtcptLmtRgnCd` | 참가제한지역코드 | 지역 필터, 기업 지역 조건 매칭 |
| `prtcptLmtRgnNm` | 참가제한지역명 | 지역명 검색/표시 |
| `indstrytyCd` | 업종코드 | 업종 조건 매칭 |
| `indstrytyNm` | 업종명 | 업종명 검색/표시 |
| `presmptPrceBgn` | 추정가격 시작 | 예산/금액 범위 검색 |
| `presmptPrceEnd` | 추정가격 종료 | 예산/금액 범위 검색 |
| `dtilPrdctClsfcNo` | 세부품명번호 | 물품분류 기반 매칭 |
| `bidClseExcpYn` | 입찰마감제외여부 | 마감된 공고 제외 |
| `intrntnlDivCd` | 국제입찰구분코드 | 국내/국제 공고 구분 |

## 4. 오퍼레이션별 활용 가능성

활용 구분:

- `핵심`: MVP 또는 1차 개발에 직접 필요
- `높음`: MVP 직후 바로 붙이면 가치가 큼
- `보조`: 운영/정합성/상세 품질을 위해 필요
- `낮음`: 현재 요구사항과 거리가 있어 후순위
- `보류`: 필요성이 생기면 재검토

| 번호 | 오퍼레이션 | 국문명 | 활용 가능성 | 활용 판단 |
| --- | --- | --- | --- | --- |
| 1 | `getBidPblancListInfoCnstwk` | 입찰공고목록 정보에 대한 공사조회 | 보조 | 공사 공고까지 포함하려면 필요. 초기 타겟이 IT/용역 중심이면 후순위 |
| 2 | `getBidPblancListInfoServc` | 입찰공고목록 정보에 대한 용역조회 | 핵심 | SI, 개발, 운영, 컨설팅 등 BidMatch 주요 타겟과 가장 잘 맞음 |
| 3 | `getBidPblancListInfoFrgcpt` | 입찰공고목록 정보에 대한 외자조회 | 낮음 | 외자 공고는 초기 사용자 니즈와 거리가 있어 후순위 |
| 4 | `getBidPblancListInfoThng` | 입찰공고목록 정보에 대한 물품조회 | 핵심 | 요구사항에 입찰물품공고서와 물품분류체계 활용이 있어 필요 |
| 5 | `getBidPblancListInfoThngBsisAmount` | 입찰공고목록 정보에 대한 물품기초금액조회 | 높음 | 예산/입찰금액 검색, 금액 범위 필터, 상세 화면에 활용 가능 |
| 6 | `getBidPblancListInfoCnstwkBsisAmount` | 입찰공고목록 정보에 대한 공사기초금액조회 | 보조 | 공사 공고를 수집할 때 금액 보강용으로 활용 |
| 7 | `getBidPblancListInfoServcBsisAmount` | 입찰공고목록 정보에 대한 용역기초금액조회 | 높음 | 용역 공고 예산/금액 필터 정확도 개선에 활용 |
| 8 | `getBidPblancListInfoChgHstryThng` | 입찰공고목록 정보에 대한 물품변경이력조회 | 보조 | 공고 정정/변경 감지, 보정 수집에 활용 |
| 9 | `getBidPblancListInfoChgHstryCnstwk` | 입찰공고목록 정보에 대한 공사변경이력조회 | 보조 | 공사 공고 변경 감지에 활용 |
| 10 | `getBidPblancListInfoChgHstryServc` | 입찰공고목록 정보에 대한 용역변경이력조회 | 보조 | 용역 공고 변경 감지와 알림 정합성 개선에 활용 |
| 11 | `getBidPblancListInfoCnstwkPPSSrch` | 나라장터검색조건에 의한 입찰공고공사조회 | 보조 | 사용자가 공사까지 검색할 경우 필요 |
| 12 | `getBidPblancListInfoServcPPSSrch` | 나라장터검색조건에 의한 입찰공고용역조회 | 핵심 | 공고명, 기관, 지역, 업종, 금액 조건 검색에 직접 활용 |
| 13 | `getBidPblancListInfoFrgcptPPSSrch` | 나라장터검색조건에 의한 입찰공고외자조회 | 낮음 | 외자 검색은 후순위 |
| 14 | `getBidPblancListInfoThngPPSSrch` | 나라장터검색조건에 의한 입찰공고물품조회 | 핵심 | 물품분류, 세부품명번호, 금액 조건 검색에 직접 활용 |
| 15 | `getBidPblancListInfoLicenseLimit` | 입찰공고목록 정보에 대한 면허제한정보조회 | 높음 | 사용자의 보유 면허와 공고 참가 조건 매칭에 활용 가능 |
| 16 | `getBidPblancListInfoPrtcptPsblRgn` | 입찰공고목록 정보에 대한 참가가능지역정보조회 | 높음 | 사용자 지역/기업 소재지 기반 추천과 필터링에 활용 |
| 17 | `getBidPblancListInfoThngPurchsObjPrdct` | 입찰공고목록 정보에 대한 물품 구매대상물품조회 | 높음 | 물품분류체계, 세부품명번호, 품목 키워드 매칭에 활용 |
| 18 | `getBidPblancListInfoServcPurchsObjPrdct` | 입찰공고목록 정보에 대한 용역 구매대상물품조회 | 보조 | 용역 공고에도 구매대상 품목이 있는 경우 분류/태깅 보강 가능 |
| 19 | `getBidPblancListInfoFrgcptPurchsObjPrdct` | 입찰공고목록 정보에 대한 외자 구매대상물품조회 | 낮음 | 외자 공고 후순위에 따라 낮음 |
| 20 | `getBidPblancListInfoEorderAtchFileInfo` | 입찰공고목록 정보에 대한 e발주 첨부파일정보조회 | 보조 | 상세 화면에서 제안요청서/첨부파일 링크 제공 시 활용 |
| 21 | `getBidPblancListInfoEtc` | 입찰공고목록 정보에 대한 기타공고조회 | 보조 | 주요 공고 유형 밖의 데이터 누락 방지용 |
| 22 | `getBidPblancListInfoEtcPPSSrch` | 나라장터검색조건에 의한 입찰공고 기타조회 | 보조 | 기타공고 검색 보완용 |
| 23 | `getBidPblancListPPIFnlRfpIssAtchFileInfo` | 혁신장터 최종제안요청서 교부 첨부파일정보조회 | 낮음 | 혁신장터/RFP 특화 기능이 필요할 때 검토 |
| 24 | `getBidPblancListBidPrceCalclAInfo` | 입찰가격산식A정보조회 | 보류 | 가격 산식 분석 기능을 만들 때 필요. MVP에는 불필요 |
| 25 | `getBidPblancListEvaluationIndstrytyMfrcInfo` | 평가대상주력분야 조회 | 보조 | 업종/주력분야 기반 참가 가능성 판단에 활용 가능 |

## 5. BidMatch 1차 개발 추천 API

MVP와 현재 요구사항을 기준으로 우선순위를 나누면 다음과 같습니다.

### 5.1 1순위: 수집과 검색 핵심

- `getBidPblancListInfoServc`
- `getBidPblancListInfoThng`
- `getBidPblancListInfoServcPPSSrch`
- `getBidPblancListInfoThngPPSSrch`

활용 이유:

- 용역/물품 공고는 BidMatch의 주요 사용자인 SI 기업, 스타트업, 프리랜서, 공공사업 담당자와 가장 잘 맞습니다.
- 공고명, 기관명, 지역, 업종, 금액, 세부품명번호 검색 요구사항을 충족할 수 있습니다.
- 사용자 관심 키워드, 물품분류, 기관 조건 매칭의 기반 데이터가 됩니다.

### 5.2 2순위: 매칭 품질 보강

- `getBidPblancListInfoServcBsisAmount`
- `getBidPblancListInfoThngBsisAmount`
- `getBidPblancListInfoLicenseLimit`
- `getBidPblancListInfoPrtcptPsblRgn`
- `getBidPblancListInfoThngPurchsObjPrdct`

활용 이유:

- 예산/금액 범위 검색을 정교하게 만들 수 있습니다.
- 사용자 보유 면허와 참가 가능 지역 조건을 공고 추천에 반영할 수 있습니다.
- 물품분류체계를 이용한 품목 키워드 매칭을 강화할 수 있습니다.

### 5.3 3순위: 운영 정합성

- `getBidPblancListInfoChgHstryServc`
- `getBidPblancListInfoChgHstryThng`
- `getBidPblancListInfoEorderAtchFileInfo`
- `getBidPblancListInfoEtc`
- `getBidPblancListInfoEtcPPSSrch`

활용 이유:

- 공고 변경/정정 이력을 반영해 알림 신뢰도를 높일 수 있습니다.
- 상세 화면에서 첨부파일 정보를 제공할 수 있습니다.
- 기타공고를 포함해 데이터 누락을 줄일 수 있습니다.

## 6. 백엔드 수집 설계 반영안

### 6.1 환경 변수

```env
G2B_API_KEY=공공데이터포털_서비스키
G2B_API_BASE_URL=http://apis.data.go.kr/1230000/ad/BidPublicInfoService
```

주의:

- `ServiceKey`는 프론트엔드에 절대 노출하지 않습니다.
- API 호출은 백엔드 수집기 또는 백엔드 API 서버에서만 수행합니다.
- 원본 응답은 Raw 테이블에 저장해 파싱 오류와 응답 변경을 추적합니다.

### 6.2 수집 방식

- 기본 수집:
  - `inqryDiv=1`
  - 공고게시일시 또는 등록일시 기준
  - `inqryBgnDt`, `inqryEndDt`로 시간 범위 지정
- 보정 수집:
  - 최근 1~3일 범위 재수집
  - 변경이력 API로 정정/취소/변경 여부 확인
- 상세 보강:
  - `bidNtceNo`, `bidNtceOrd` 기준으로 기초금액, 면허제한, 참가가능지역, 구매대상물품 조회
- 중복 방지:
  - 최소 유니크 키: `bidNtceNo + bidNtceOrd + 업무구분`

### 6.3 DB 필드 후보

공고 기본 테이블에 우선 반영할 필드:

- `bidNtceNo`: 입찰공고번호
- `bidNtceOrd`: 입찰공고차수
- `bidNtceNm`: 입찰공고명
- `ntceInsttCd`: 공고기관코드
- `ntceInsttNm`: 공고기관명
- `dminsttCd`: 수요기관코드
- `dminsttNm`: 수요기관명
- `prtcptLmtRgnCd`: 참가제한지역코드
- `prtcptLmtRgnNm`: 참가제한지역명
- `indstrytyCd`: 업종코드
- `indstrytyNm`: 업종명
- `presmptPrce`: 추정가격 또는 관련 금액
- `dtilPrdctClsfcNo`: 세부품명번호
- `bidClseDt`: 입찰마감일시
- `opengDt`: 개찰일시
- `bizType`: 업무구분. 예: `SERVC`, `THNG`, `CNSTWK`, `FRGCPT`, `ETC`

## 7. 결론

BidMatch MVP에서는 모든 25개 오퍼레이션을 한 번에 붙이지 않고, 용역/물품 중심으로 시작하는 것이 좋습니다.

우선 구현 대상:

1. 용역 공고 목록/검색
2. 물품 공고 목록/검색
3. 용역/물품 기초금액
4. 면허제한
5. 참가가능지역
6. 물품 구매대상물품

후속 구현 대상:

1. 변경이력
2. 첨부파일
3. 기타공고
4. 공사/외자 공고
5. 입찰가격산식/평가대상주력분야
