# PRODUCT REQUIREMENT DOCUMENT (PRD) & CASE STUDY
## Smart Average Down Calculator (스마트 물타기 계산기)

**Document Type**: End-to-End Product Case Study & Functional Specification  
**Version**: 2.0.0 (Full Research & Architecture Edition)  
**Role**: Lead Product Manager & Senior Design System Engineer  
**Last Updated**: 2026-10-17  

---

# CHAPTER 1. 시장 배경 및 문제 발견 (Discovery & Research)

## 1.1 시장 배경 (Market Background)
* **글로벌 거시경제 변동성 심화**: 
  고금리, 지정학적 리스크 등으로 주식 및 가상자산 시장의 변동성(Volatility)이 극대화되면서, 상승장 위주의 신규 매수보다 **"물려있는 기존 보유 종목의 손실 방어 및 평단가 관리(Average Down)"** 수요가 폭발적으로 증가함.
* **개인 투자자(Retail Investors)의 행동 편향**:
  행동경제학적 관점에서 개인 투자자는 손실 회피 성향(Loss Aversion)으로 인해 하락 종목을 손절하지 못하고 감정적 '물타기'를 감행하나, 수학적 자금 관리 계획이 없어 **비중만 비대해지고 추가 하락 시 회복 불가능한 치명적 MDD(최대 낙폭)**를 겪음.

---

## 1.2 사용자 조사 및 페인 포인트 (User Research & Pain Points)
실제 개인 투자자 심층 인터뷰(IDI, 12명) 및 기존 주식 커뮤니티 데이터 분석을 통해 3대 핵심 페인 포인트를 도출함.

| 분류 | 사용자 핵심 페인 포인트 (Pain Point) | 현업/기존 앱의 한계 |
| :--- | :--- | :--- |
| **Pain Point 1<br/>(전략 부재)** | **"단가를 낮추려고 계속 샀는데, 비중만 커지고 평단은 거의 안 내려가요."** | 기존 계산기들은 단순 1회성 합산만 제공하여, **추가 매수 차수별 평단 인하 효율(한계 효용)이나 비중 편중 위험**을 시각적으로 경고해주지 못함. |
| **Pain Point 2<br/>(조작 지연)** | **"급락하는 호가창 앞에서 계산기 두드리다가 매수 타이밍을 놓쳐요."** | 키패드로 단가 8자리, 수량 5자리를 일일이 치다가 호가가 변동됨. **초단위 신속 입력 수단(음성, 프리셋)**의 부재. |
| **Pain Point 3<br/>(목표 역산 불가)** | **"본전이나 -5% 탈출 목표가에 가려면 지금 대체 몇 주를 더 사야 하죠?"** | 대부분의 앱은 '결과 순방향 계산'만 지원하며, **"목표 단가 도달을 위한 필수 매수 수량 역산(Goal Seeking)"** 기능이 전무함. |

---

## 1.3 경쟁 제품 벤치마킹 (Competitive Benchmark)

| 비교 항목 | 네이버페이 증권 / MTS 내장 계산기 | 일반 앱스토어 주식 계산기 | **스마트 물타기 계산기 (본 제품)** |
| :--- | :--- | :--- | :--- |
| **입력 방식** | 키패드 수동 입력 (느림) | 키패드 수동 입력 (광고 다수) | **멀티모달 (원터치 프리셋 칩 + AI 음성 자연어 STT)** |
| **시나리오 비교** | 불가능 (단일 계산) | 불가능 (단일 계산) | **A vs B 전략 대조 매트릭스 제공** |
| **목표가 역산** | 미지원 | 미지원 | **지원 (Goal Seeking 수식 기반 필요 수량/자금 역산)** |
| **자산 관리** | 단순 종목 조회 | 세션 종료 시 초기화 | **로컬 SQLite 영속화 및 포트폴리오 리스크 진단** |
| **사용 환경** | 복잡한 금융 UI, 로딩 지연 | 화면을 가리는 배너 광고 | **24시간 VIP 무광고 모드 + 다크/라이트 디자인 시스템** |

---

## 1.4 핵심 가설 및 제품 솔루션 (Hypothesis & Solution Matrix)

* **가설 1**: "원터치 프리셋과 AI 음성 입력을 제공하면 데이터 입력 소요 시간을 기존 대비 70% 이상 단축할 것이다."
  ➔ **솔루션**: `AI Voice Ingestion Panel` 및 `±5%, ±10% 원터치 증감 칩` 탑재.
* **가설 2**: "목표 평단가 도달에 필요한 매수 수량을 즉시 역산해 주면 뇌동매매를 방지하고 체계적 자금 집행을 유도할 것이다."
  ➔ **솔루션**: `Goal Seeking Engine (목표가 역산 알고리즘)` 구현.
* **가설 3**: "A/B 시나리오를 한 화면에서 대조해 주면 자금 분할 효율이 극대화될 것이다."
  ➔ **솔루션**: `Scenario Comparison Matrix` 설계.

---

# CHAPTER 2. 타깃 페르소나 & 고객 여정 지도 (Persona & Journey Map)

## 2.1 타깃 페르소나 (Target Personas)

### 페르소나 A: 손실 방어형 직장인 투자자 (34세, 김투자)
* **투자 성향**: 국내 대형주 및 미국 테크주 위주, 업무 중 수시로 급락 알림을 확인.
* **목표**: 물려있는 종목을 무지성 매수하지 않고, 월급 날마다 분할 매수하여 6개월 내 본전 탈출.
* **니즈**: "이 종목에 내 총자산의 몇 %가 묶여있는지 한눈에 리포트로 보고 싶다."

### 페르소나 B: 고기동성 크립토/단타 트레이더 (28세, 박스캘퍼)
* **투자 성향**: 변동성이 극심한 가상자산 및 테마주 단타 매매.
* **목표**: 급락 빔 발생 시 3초 안에 추가 매수 평단을 산출하여 지지선에서 즉각 반등 탈출.
* **니즈**: "손가락으로 칠 시간도 없다. 말로 '100주 더 사면 평단 얼마야?'하면 바로 나와야 한다."

---

## 2.2 사용자 여정 지도 (Customer Journey Map)

```
[Phase 1. 급락 인지] ───> [Phase 2. 탐색 & 인제스천] ───> [Phase 3. 시뮬레이션] ───> [Phase 4. 의사결정]
- 보유 종목 -15% 급락     - 앱 실행 및 음성 입력      - A안(50주) vs B안(100주) 대조 - 최적 분할 매수 실행
- 공포감, 뇌동매매 충동     - 1초 만에 데이터 모델링     - 목표 탈출가 도달 가능성 검증 - 시나리오 DB 저장
- "탈출할 수 있을까?"     - "입력이 엄청 빠르네"      - "이 가격에선 40주만 사야겠다" - 심리적 안정감 확보
```

---

# CHAPTER 3. 정보 구조도 (Information Architecture)

```
[Smart Average Down Architecture]
 ├── 1.0 Splash & Onboarding (최초 실행 유저 학습)
 │    ├── 1.1 Strategy Onboarding (분할 매수 수학적 메커니즘 4단계)
 │    └── 1.2 Locale Sync (디바이스 기반 통화 ₩/$/¥/€ 및 언어 세팅)
 │
 ├── 2.0 Home Dashboard (자산 현황 및 퀵 액션)
 │    ├── 2.1 VIP Status Header (24h 무광고 카운트다운 타이머)
 │    ├── 2.2 AI Voice Panel (음성 인식 STT & 프리셋 칩)
 │    ├── 2.3 Asset Portfolio Carousel (등록 자산 카드 & 평단/수량 요약)
 │    └── 2.4 Quick Dock (자산 추가, 시뮬레이터 진입, 리포트 열기)
 │
 ├── 3.0 Simulation Engine (핵심 연산 모듈)
 │    ├── 3.1 Multi-Batch Simulator (1차~N차 가중평균 연산)
 │    ├── 3.2 A/B Scenario Comparator (전략 대조 분석)
 │    ├── 3.3 Goal Seeking Calculator (목표 평단가 도달 역산기)
 │    └── 3.4 Scenario History Persistence (로컬 히스토리 DB 저장)
 │
 ├── 4.0 Portfolio & Analytics (성과 분석)
 │    ├── 4.1 Asset Allocation Chart (종목별 투자 비중 도넛 차트)
 │    ├── 4.2 Urgency Risk Index (괴리율 기반 물타기 시급도 판정)
 │    └── 4.3 Report Artifact Export (이미지 캡처 및 공유)
 │
 └── 5.0 Settings & Utility (환경설정)
      ├── 5.1 Global Preferences (언어/통화/테마 모드)
      ├── 5.2 Financial Help Guide (MDD 방어 전략 FAQ)
      └── 5.3 Legal & Compliance (개인정보처리방침, 오픈소스 라이선스)
```

---

# CHAPTER 4. 와이어프레임 1:1 매핑 기능 정의서 (Lo-Fi Wireframe Functional Specs)

피그마 작업 시 **와이어프레임 화면 옆에 인덱스 핀(①, ②, ③)으로 붙일 수 있는 표준 기능 명세서**입니다.

---

### [Screen 01] 홈 대시보드 (Home Dashboard Wireframe)

```
┌──────────────────────────────────────────────┐
│ [Logo] 스마트 물타기 계산기         [?] [⚙]   │ ── ① Global Header
├──────────────────────────────────────────────┤
│ [⭐ 24시간 VIP 무광고 모드 활성중  D-0 23:59:58]│ ── ② VIP Status Banner
├──────────────────────────────────────────────┤
│ ┌──────────────────────────────────────────┐ │
│ │ 🎙️ AI Voice Assistant                   │ │
│ │ "음성을 듣는 중입니다... 말씀해 주세요"     │ │ ── ③ AI Ingestion Panel
│ │ [삼성전자 75,000원 100주, 68,000원에 50주]│ │
│ └──────────────────────────────────────────┘ │
├──────────────────────────────────────────────┤
│ 나의 보유 종목 (총 3개)           [+ 자산 추가]│ ── ④ Asset Header
│ ┌──────────────────┐ ┌──────────────────┐    │
│ │ 삼성전자          │ │ SK하이닉스       │    │ ── ⑤ Asset Cards
│ │ 평단: ₩75,000    │ │ 평단: ₩180,000   │    │    (Carousel / Grid)
│ │ 보유: 100주      │ │ 보유: 30주       │    │
│ └──────────────────┘ └──────────────────┘    │
├──────────────────────────────────────────────┤
│ [ 📊 시뮬레이터 바로가기 ]   [ 📑 포트폴리오 리포트 ] │ ── ⑥ Bottom Action Dock
└──────────────────────────────────────────────┘
```

#### 기능 명세 (Functional Specifications)
* **① Global Header**:
  - `[?]`: `HelpScreen`으로 라우팅 (물타기 원리 가이드).
  - `[⚙]`: `SettingsScreen`으로 라우팅 (다국어, 통화 변경).
* **② VIP Status Banner**:
  - `EventService.isAdFreeActive()`를 구독하여 상태 렌더링.
  - 활성 시 1초 단위 실시간 카운트다운(`D-N HH:mm:ss`) 표시.
  - 만료 시 보상형 광고 시청 유도 버튼 노출 (`AdmobService.showRewardedAd()`).
* **③ AI Ingestion Panel**:
  - 마이크 탭 시 `speech_to_text` 활성화 및 음성 파형 애니메이션 구동.
  - 정규표현식 파서(`RegExp`)를 통해 종목명, 단가, 수량을 분리 추출.
  - 추출 성공 시 하단 슬라이드 팝업을 띄워 `[자산 저장]` 또는 `[시뮬레이터 적용]` 선택 제공.
* **④ & ⑤ Asset Cards**:
  - `assetsProvider` (SQLite DB) 실시간 연동.
  - 카드 스와이프 시 수정/삭제 슬라이드 액션 제공.
  - 탭 시 해당 종목의 단가/수량을 시뮬레이터 기본값으로 주입하며 화면 이동.

---

### [Screen 02] 전략 시뮬레이터 (Simulator Screen Wireframe)

```
┌──────────────────────────────────────────────┐
│ [<] 전략 시뮬레이터               [초기화]     │ ── ① Navigation Bar
├──────────────────────────────────────────────┤
│ 종목: [ 삼성전자 ]    심볼: [ 005930 ]        │ ── ② Entity Meta
│ 현재 평단가: [ 75,000 ]    보유수량: [ 100 ]   │ ── ③ Initial State
├──────────────────────────────────────────────┤
│ [● 일반 물타기]  [○ A/B 비교]  [○ 목표가 역산] │ ── ④ Mode Segment
├──────────────────────────────────────────────┤
│ [1차 추가매수] 단가: [ 68,000 ] 수량: [ 50 ]  │ ── ⑤ Batch Inputs
│ [+ 추가 매수 차수 등록]                        │
├──────────────────────────────────────────────┤
│ ┌──────────────────────────────────────────┐ │
│ │ 연산 결과 요약 (Result Summary)           │ │ ── ⑥ Result Card
│ │ 예상 평단가: ₩72,666  (-3.11% 인하 방어)  │ │
│ │ 필요 추가 자금: ₩3,400,000                 │ │
│ │ 최종 보유 수량: 150주                     │ │
│ └──────────────────────────────────────────┘ │
├──────────────────────────────────────────────┤
│ [ 💾 시나리오 저장 ]     [ 📈 자산 데이터 갱신 ] │ ── ⑦ Commit Actions
└──────────────────────────────────────────────┘
```

#### 기능 명세 (Functional Specifications)
* **④ Mode Segment Control**:
  - `일반 물타기`: 단일 종목의 1~N차 분할 매수 누적 연산.
  - `A/B 비교`: 좌우 2분할 뷰를 열어 동일 자금 투입 시 분할 비율(5:5 vs 3:7)에 따른 평단 방어율 대조.
  - `목표가 역산`: 역산 전용 인풋 카드 노출.
* **⑤ Core Math Engine (가중평균 연산식)**:
  $$\text{Target Price} = \frac{(P_0 \times Q_0) + \sum_{i=1}^{n}(P_i \times Q_i)}{Q_0 + \sum_{i=1}^{n}Q_i}$$
  - 텍스트 필드 변경 감지 시 디바운스 150ms 후 무중단 실시간 재계산.
* **⑥ Result Card**:
  - 평단가 인하율에 따라 시맨틱 컬러 적용 (인하 성공 시 `AppColors.accentMint`, 평단 상승 시 `AppColors.accentCoral`).
* **⑦ Commit Actions**:
  - `시나리오 저장`: `scenarioProvider`를 통해 SQLite에 고유 ID(UUID)로 결과 스냅샷 영속화.

---

### [Screen 03] 목표가 역산기 (Goal Seeking Calculator Wireframe)

```
┌──────────────────────────────────────────────┐
│ 현재 보유 단가: [ 75,000 ]   현재 수량: [ 100 ]│ ── ① Current State
├──────────────────────────────────────────────┤
│ 희망 목표 단가: [ 70,000 ]                    │ ── ② Target Goal (Pt)
│ 추가 매수 예정가: [ 65,000 ]                  │ ── ③ Purchase Price (Pa)
├──────────────────────────────────────────────┤
│ ┌──────────────────────────────────────────┐ │
│ │ 🎯 필수 추가 매수 수량: 100 주             │ │ ── ④ Required Quantity
│ │ 💰 총 필요 매수 금액: ₩6,500,000          │ │ ── ⑤ Required Capital
│ │ 📊 매수 후 총 비중: 기존 대비 2.0배 확대    │ │
│ └──────────────────────────────────────────┘ │
└──────────────────────────────────────────────┘
```

#### 기능 명세 (Functional Specifications)
* **역산 수학 공식 (Goal Seeking Logic)**:
  $$Q_{add} = \frac{Q_0 \times (P_0 - P_{target})}{P_{target} - P_{add}}$$
* **유효성 검증 및 예외 처리 (Exception Handling)**:
  - `조건 1 (도달 불가)`: $P_{target} \le P_{add}$ 일 경우 ➔ "목표 평단가는 추가 매수가보다 높아야 달성 가능합니다" 경고 문구 출력 및 결과 블러 처리.
  - `조건 2 (불타기 조건)`: $P_{target} \ge P_0$ 일 경우 ➔ "목표 단가가 현재 평단보다 높습니다. 매수가 아닌 매도 계획을 세우세요" 피드백.
  - `조건 3 (0 나누기 방지)`: 분모가 0이 되는 연산은 사전에 차단.

---

### [Screen 04] 포트폴리오 분석 리포트 (Portfolio Report Wireframe)

```
┌──────────────────────────────────────────────┐
│ 총 투자 원금: ₩42,500,000     보유 종목: 4개 │ ── ① Wealth Overview
├──────────────────────────────────────────────┤
│ [      삼성전자 45%      ][ 하이닉스 30% ][기타]│ ── ② Allocation Bar
├──────────────────────────────────────────────┤
│ [종목별 상세 리스크 진단]                      │ ── ③ Risk Diagnostics
│ • 삼성전자: 비중 과다 경고 (권장 비중 30% 초과) │
│ • 카카오: 괴리율 -24% (물타기 시급도: 높음)   │
├──────────────────────────────────────────────┤
│ [ 📤 리포트 이미지 캡처 & 공유하기 ]          │ ── ④ Export Action
└──────────────────────────────────────────────┘
```

#### 기능 명세 (Functional Specifications)
* **② Allocation Bar & Chart**:
  - 전체 투자 원금 대비 종목별 가중치($\frac{P_i \times Q_i}{\text{Total Wealth}}$)를 계산하여 세련된 세그먼트 막대 및 도넛 차트 렌더링.
* **③ Risk Diagnostics (위험도 판정 알고리즘)**:
  - 단일 종목 비중이 전체 자산의 40% 초과 시 '비중 편중 주의' 배지 표시.
  - 현재가 대비 평단 괴리율이 -20% 이상 벌어질 경우 '물타기 우선순위 High'로 분류.
* **④ Export Action**:
  - `RepaintBoundary`를 통해 리포트 카드를 고해상도 PNG 이미지로 래스터라이징하여 시스템 공유 시트(`share_plus`) 호출.

---

# CHAPTER 5. 디자인 시스템 매핑 & 기술 아키텍처

## 5.1 디자인 토큰 매핑 규격 (Design Tokens Mapping)
모든 UI 컴포넌트는 W3C 및 Figma Tokens Studio 규격인 `tokens.json`과 1:1로 결합되어 있습니다.

| 디자인 영역 | Flutter 코드 토큰 (`AppColors`, `AppTextStyles`) | Figma Variable / Token |
| :--- | :--- | :--- |
| **Primary Brand** | `AppColors.primaryBlue` (`#0051FF`) | `color.brand.primaryBlue` |
| **Gain / Success** | `AppColors.accentMint` (`#00E676`) | `color.semantic.success` |
| **Loss / Danger** | `AppColors.accentCoral` (`#FF5252`) | `color.semantic.error` |
| **Dark Surface** | `AppColors.darkBg` (`#0F141C`) / `darkSurface` (`#1A212E`)| `color.surface.dark.background` |
| **Light Surface** | `AppColors.lightBg` (`#F6F8FC`) / `lightSurface` (`#FFFFFF`)| `color.surface.light.background` |
| **Display Font** | `AppTextStyles.displayLarge` (Inter, 28sp, w900) | `typography.display.large` |
| **Numeric Value** | `AppTextStyles.numericValue` (Inter, Tabular Numbers) | `typography.numeric.value` |

---

## 5.2 프로덕트 성공 지표 (Success Metrics & KPIs)
포트폴리오 심사 시 "데이터 기반으로 프로덕트를 운영하는 PO/엔지니어"임을 증명하는 핵심 지표 설계입니다.

1. **North Star Metric (북극성 지표)**:
   - **주간 전략 시뮬레이션 완료 횟수 (Weekly Completed Simulations)**
2. **OMTM (One Metric That Matters)**:
   - **AI 음성 입력 후 시나리오 저장으로 이어지는 전환율 (STT-to-Save Conversion Rate)**: 목표치 45% 이상.
3. **Retention & Monetization**:
   - **24시간 VIP 광고제거 보상형 광고 시청 유지율 (Reward-Ad Retention)**: 일 2회 이상 시청 비율 측정.
   - **D+7 재방문율**: 35% 이상 달성.
