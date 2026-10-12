# REVERSE PRD & FUNCTIONAL SPECIFICATION (역기획 기능 정의서)

**Project**: Smart Average Down Calculator (스마트 물타기 계산기)  
**Version**: 1.0.0+ (Design System Integrated)  
**Role**: Senior Flutter & Design System Engineer / Lead Product Manager  
**Last Updated**: 2026-10-12  

---

## 1. Executive Summary & Product Objective
**스마트 물타기 계산기**는 주식 및 가상자산 투자자가 급격한 시세 변동 시 자신의 평균 단가(평단가)와 보유 비중을 방어·개선하기 위해 사용하는 **고성능 전략 시뮬레이션 및 자산 관리 툴**입니다.
복잡한 수식을 원터치 및 AI 음성 인식으로 단순화하고, 시나리오별 비교 분석, 목표 평단가 도달을 위한 필요 수량 역산, 포트폴리오 자산 리포트 기능까지 일원화된 모바일 경험으로 제공합니다.

---

## 2. Information Architecture (IA)

```
[App Entry]
 ├── Splash Screen
 └── Onboarding Flow (최초 진입 시)
      ├── Step 1: 빠른 평단 계산 및 물타기 전략
      ├── Step 2: 다중 시나리오 A vs B 비교
      ├── Step 3: AI 스마트 음성 비서 입력
      └── Step 4: 목표 단가 역산 및 포트폴리오 보호

[Main Architecture]
 ├── 1. 홈 화면 (Home Dashboard)
 │    ├── 상단 App Bar (앱 로고, 타이틀, 도움말, 설정)
 │    ├── VIP / 광고 제거 현황 카드 (실시간 카운트다운 타이머)
 │    ├── AI 음성 어시스턴트 패널 (AI Voice Assistant)
 │    ├── 보유 자산 리스트 (Asset Cards - 수정/삭제/시뮬레이터 연동)
 │    ├── 하단 액션 독 (새 자산 등록, 시뮬레이터 바로가기, 리포트 확인)
 │    └── 네이티브 광고 / 전면 광고 브리지
 │
 ├── 2. 시뮬레이터 화면 (Multi-Scenario Simulator)
 │    ├── 종목 정보 헤더 (종목명, 심볼, 현재 평단/수량)
 │    ├── 모드 셀렉터 (일반 물타기 / 시나리오 A vs B 비교 / 목표가 역산)
 │    ├── 분할 매수 차수 빌더 (1차~N차 매수 단가 및 수량 동적 추가)
 │    ├── 수수료(증권사/거래소 거래세) 온/오프 토글
 │    ├── 결과 비교 카드 (새로운 평단, 총 투자금, 단가 변동률)
 │    └── 시나리오 저장 (SQLite/Provider 영속화)
 │
 ├── 3. 목표가 역산 화면 (Target Price Calculator)
 │    ├── 보유 현황 입력 (현재 단가, 현재 수량)
 │    ├── 목표 희망 단가 및 추가 매수 단가 입력
 │    ├── 필수 추가 매수 수량 실시간 산출
 │    └── 필요 추가 자금(총 매수금액) 계산 결과 카드
 │
 ├── 4. 포트폴리오 리포트 화면 (Portfolio Report)
 │    ├── 총 자산 평가 및 총 매수 원금 요약
 │    ├── 종목별 자산 비중 차트 및 상세 현황
 │    ├── 물타기 필요 긴급도 판정 지표
 │    └── 리포트 공유/저장 기능
 │
 ├── 5. 시나리오 히스토리 화면 (Scenario History)
 │    ├── 저장된 과거 시뮬레이션 목록
 │    ├── 시나리오 상세 보기 및 시뮬레이터로 복원(Re-simulate)
 │    └── 히스토리 단건 삭제 및 전체 비우기
 │
 ├── 6. 도움말 & 금융 가이드 (Help & Guide)
 │    ├── 물타기(Average Down) vs 불타기(Pyramiding) 원리
 │    ├── MDD 방어 및 분할 매수 황금 비율 전략 가이드
 │    ├── AI 음성 명령어 템플릿 안내
 │    └── FAQ 아코디언
 │
 └── 7. 설정 화면 (Settings)
      ├── 언어 변경 (한국어, 영어, 일본어, 중국어, 스페인어 등)
      ├── 통화 단위 설정 (KRW ₩, USD $, JPY ¥, EUR €, 등 자동 환산 포맷)
      ├── 테마 모드 전환 (다크 모드 / 라이트 모드)
      ├── 온보딩 다시 보기
      └── 앱 버전 및 법률 정책 (개인정보처리방침, 오픈소스 라이선스)
```

---

## 3. Wireframe 1:1 Mapping Functional Specifications (화면별 기능 명세서)

### 3.1 [Screen 1] 홈 화면 (Home Dashboard)
* **Wireframe 컴포넌트 매핑**:
  1. `AppBar`: 좌측 앱 타이틀 + 우측 `[도움말(?)]`, `[설정(⚙️)]` 아이콘 버튼
  2. `AdFreeBanner`: VIP 24시간 광고제거 상태 및 잔여 시간 카운트다운(`D-0 23:59:58`) 배너
  3. `AIVoiceAssistantPanel`: 마이크 웨이브폼 애니메이션, 프리셋 칩, 음성 인식 트리거
  4. `AssetListSection`: 등록된 보유 종목 카드 캐러셀/리스트뷰
  5. `FloatingActionDock`: `[+ 자산 추가]`, `[📊 시뮬레이터 바로가기]`, `[📑 자산 리포트]`
* **Functional Specs (상세 로직)**:
  - **음성 인식 연동**: `speech_to_text`를 통해 유저 음성("삼성전자 7만 원에 100주, 6만 5천 원에 50주 물타기")을 자연어 파싱하여 종목명, 초기 단가/수량, 추가 매수 단가/수량을 자동 추출.
  - **통화 및 언어 포맷팅**: `CurrencyNotifier` 및 `AppLocalizations`와 결합하여 콤마(,) 3자리 단위 분리와 통화 심볼 자동 반영.
  - **광고 제어**: 앱 진입 시 `AdmobService.showAppOpenAd()` 호출(VIP 무광고 활성 시 차단).
* **예외 처리 & Edge Cases**:
  - `음성 인식 권한 거부`: 마이크 접근 권한 없을 시 설정 이동 안내 다이얼로그 노출 및 텍스트 직접 입력 모드로 Fallback.
  - `네트워크 단절`: 오프라인 상태에서도 SQLite 로컬 DB 기반 자산 조회 및 계산 100% 정상 작동.
  - `0원 또는 음수 입력`: 단가/수량 입력 시 0 이하의 값은 유효성 검사 실패 토스트("0보다 큰 값을 입력하세요") 출력.

---

### 3.2 [Screen 2] 시뮬레이터 화면 (Simulator Screen)
* **Wireframe 컴포넌트 매핑**:
  1. `HeaderSection`: 종목명(`AssetName`), 종목코드(`AssetSymbol`), 현재 평단가/수량 인풋
  2. `ModeToggleSegment`: `[단일 물타기]`, `[A vs B 시나리오 비교]`, `[목표 단가 모드]`
  3. `BatchListBuilder`: 1차, 2차, 3차... 매수 단가/수량 행 및 `[+ 차수 추가]` 버튼
  4. `ResultSummaryCard`: 기존 평단 vs 변경 평단, 평단 인하율(`-%`), 필요 추가 금액, 총 보유 수량
  5. `BottomActionBar`: `[시나리오 저장]`, `[자산으로 등록]`
* **Functional Specs (상세 로직)**:
  - **가중 평균 계산 공식**:
    $$\text{New Average} = \frac{(P_0 \times Q_0) + \sum (P_i \times Q_i)}{Q_0 + \sum Q_i}$$
  - **비교 모드 (A vs B)**:
    동일한 원금 또는 다른 조건에서 시나리오 A와 B를 좌우/상하로 대조하여 평단 인하 효율이 더 높은 시나리오에 하이라이트 배지 부여.
  - **실시간 반응형 렌더링**: 텍스트 필드 변경 시 `addListener`를 통해 즉시 계산 결과 재렌더링 (디바운스 150ms).
* **예외 처리 & Edge Cases**:
  - `매수 단가가 현재가보다 높은 경우`: 물타기가 아닌 '불타기(평단 상승)' 상태가 됨을 경고 아이콘과 함께 안내.
  - `최대 입력 제한`: 정수 12자리 초과 입력 시 오버플로 방지를 위한 `MaxLengthEnforcement`.

---

### 3.3 [Screen 3] 목표가 역산 화면 (Target Price Screen)
* **Wireframe 컴포넌트 매핑**:
  1. `InputCard`: 현재 보유 단가, 현재 보유 수량
  2. `TargetCard`: 희망 목표 평단가, 추가 매수 예정 단가
  3. `CalculationResultCard`: 필수 추가 매수 수량(주), 총 필요 자금, 매수 후 총 비중
* **Functional Specs (상세 로직)**:
  - **필요 수량 산출 공식**:
    $$Q_{add} = \frac{Q_0 \times (P_0 - P_{target})}{P_{target} - P_{add}}$$
  - **도달 불가능 조건 감지**: 목표 단가가 추가 매수 단가 이하이거나, 현재 단가보다 높을 때 수학적으로 불가능함을 감지.
* **예외 처리 & Edge Cases**:
  - `분모가 0이 되는 경우 ($P_{target} == P_{add}$)`: 계산 불가 상태를 방지하고 "추가 매수가격과 목표가격은 같을 수 없습니다" 안내 표시.
  - `계산된 수량이 음수인 경우`: 목표 단가가 현재 단가보다 높아 매수가 아닌 매도가 필요한 상태임을 안내.

---

### 3.4 [Screen 4] 포트폴리오 리포트 화면 (Portfolio Report)
* **Wireframe 컴포넌트 매핑**:
  1. `TotalWealthCard`: 총 투자 금액, 총 보유 종목 수
  2. `AssetAllocationChart`: 종목별 투자 비중 프로그레스 바 및 도넛 차트
  3. `UrgencyIndicator`: 평단 괴리율에 따른 물타기 시급도(관망 / 추가 매수 적기 / 비중 과다 경고)
  4. `ShareButton`: 리포트 이미지 캡처 및 공유 액션
* **Functional Specs (상세 로직)**:
  - `AssetProvider`의 전체 자산 데이터를 집계하여 가중치 계산.
* **예외 처리 & Edge Cases**:
  - `자산이 0개일 때`: Empty State 뷰 노출 및 "첫 자산을 등록해 보세요" CTA 버튼 제공.

---

### 3.5 [Screen 5] 도움말 & 퀴즈 가이드 (Help & Guide)
* **Wireframe 컴포넌트 매핑**:
  1. `StrategyCards`: 분할 매수 테크닉 (3분할법, 피보나치 비율 매수법)
  2. `InteractiveSimulatorMini`: 탭하여 즉시 체감하는 미니 인터랙션 위젯
  3. `FAQList`: 탭 시 펼쳐지는 ExpansionTile 아코디언
* **Functional Specs (상세 로직)**:
  - 금융 초보자도 쉽게 분할 매수의 수학적 원리를 이해할 수 있도록 직관적인 카드형 UI 제공.

---

## 4. Design System Compliance Matrix
모든 화면은 이번에 구축된 디자인 시스템 토큰을 100% 준수합니다:
* **Color System**: [lib/core/theme/app_colors.dart](file:///d:/097.flutter_project/average_down_calculator/lib/core/theme/app_colors.dart)
  - Dark Surface: `#0F141C` (Bg), `#1A212E` (Card), `#2B3648` (Border)
  - Light Surface: `#F6F8FC` (Bg), `#FFFFFF` (Card), `#EEF2F8` (Border)
  - Key Accents: Electric Blue `#0051FF`, Mint Green `#00E676` (수익/성공), Coral Red `#FF5252` (손실/위험)
* **Typography System**: [lib/core/theme/app_text_styles.dart](file:///d:/097.flutter_project/average_down_calculator/lib/core/theme/app_text_styles.dart)
  - GoogleFonts Inter 고정, 가변 숫자(Monospace/NumericValue) 적용.
