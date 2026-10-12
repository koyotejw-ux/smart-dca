# USER FLOW CHART (사용자 여정 및 화면 전환 플로우차트)

**Project**: Smart Average Down Calculator (스마트 물타기 계산기)  
**Version**: 1.0.0+  
**Format**: Mermaid.js (`flowchart TD`)  

---

## 1. 전체 사용자 여정 다이어그램 (End-to-End User Flow)

```mermaid
flowchart TD
    %% 진입 및 온보딩 단계
    Start([앱 실행 Launch]) --> Splash[스플래시 화면 Splash Screen]
    Splash --> CheckFirst{최초 실행 여부?}
    CheckFirst -- 예 (First Run) --> Onboarding[온보딩 4단계 안내 OnboardingScreen]
    Onboarding --> FinishOnboard[온보딩 완료 처리] --> Home[홈 대시보드 HomeScreen]
    CheckFirst -- 아니오 --> Home

    %% 홈 대시보드 상태 및 분기
    Home --> AdOpenCheck{전면/오픈 광고 트리거}
    AdOpenCheck -- VIP 활성화 --> SkipAd[광고 생략 Pass]
    AdOpenCheck -- 일반 유저 --> ShowAppOpenAd[App Open Ad 노출] --> Dashboard[메인 화면 로드 완료]
    SkipAd --> Dashboard

    %% 주요 사용자 인터랙션 5대 분기
    Dashboard --> Action1[/1. AI 음성 어시스턴트 입력/]
    Dashboard --> Action2[/2. 보유 자산 카드 선택 또는 추가/]
    Dashboard --> Action3[/3. 다중 시뮬레이터 진입/]
    Dashboard --> Action4[/4. 포트폴리오 리포트 확인/]
    Dashboard --> Action5[/5. 환경설정 및 가이드 이동/]

    %% 1. AI 음성 입력 플로우
    Action1 --> VoicePanel[AI 음성 패널 오픈]
    VoicePanel --> MicTap{마이크 버튼 탭}
    MicTap --> Listen[STT 음성 수신 중 Waveform]
    Listen --> STTSuccess{자연어 인식 성공?}
    STTSuccess -- 성공 --> ParseData[단가/수량/종목 자동 추출]
    ParseData --> PreviewParsed[인식 결과 프리뷰 팝업]
    PreviewParsed --> ApplyToSim[시뮬레이터로 데이터 전달]
    STTSuccess -- 실패/권한없음 --> VoiceFallback[텍스트 추천 프리셋 칩 선택] --> PreviewParsed

    %% 2. 자산 관리 플로우
    Action2 --> AssetDialog{자산 추가/수정 다이얼로그}
    AssetDialog --> InputAsset[종목명, 평단가, 수량 입력]
    InputAsset --> SaveAsset[(로컬 SQLite DB 저장)]
    SaveAsset --> UpdateHomeList[홈 자산 카드 목록 갱신]

    %% 3. 시뮬레이터 플로우
    Action3 --> SimScreen[시뮬레이터 SimulatorScreen]
    ApplyToSim --> SimScreen
    SimScreen --> SelectMode{모드 선택}
    SelectMode -- 단일 물타기 --> SingleSim[기본 차수별 물타기 계산]
    SelectMode -- 시나리오 비교 --> CompareSim[시나리오 A vs B 동시 대조]
    SelectMode -- 목표가 역산 --> TargetSim[목표 평단가 도달 필요수량 계산]

    SingleSim --> DynamicCalc[실시간 가중평균 연산 엔진]
    CompareSim --> DynamicCalc
    TargetSim --> DynamicCalc

    DynamicCalc --> ViewResult[결과 요약 카드 표시\n- 신규 평단\n- 하락률 방어\n- 필요 자금]
    ViewResult --> SaveScenarioAction{시나리오 저장?}
    SaveScenarioAction -- 저장 --> SaveHistory[(시나리오 히스토리 DB 저장)]
    SaveScenarioAction -- 미저장 --> SimScreen

    %% 4. 리포트 플로우
    Action4 --> ReportScreen[포트폴리오 리포트 PortfolioReportScreen]
    ReportScreen --> TotalAnalysis[총 투자 원금 및 비중 분석 차트]
    TotalAnalysis --> UrgencyCheck[물타기 시급도 및 안전성 판정]
    UrgencyCheck --> ShareReport[결과 리포트 이미지 공유 / 저장]

    %% 5. 설정 및 가이드 플로우
    Action5 --> SettingsScreen[설정 SettingsScreen]
    SettingsScreen --> LangOption[언어 변경 KO / EN / JA / ZH / ES]
    SettingsScreen --> CurrencyOption[통화 변경 KRW / USD / JPY / EUR]
    SettingsScreen --> ThemeOption[다크/라이트 테마 전환]
    SettingsScreen --> HelpGuide[도움말 & 금융 전략 가이드 HelpScreen]
    HelpGuide --> BackToHome[홈으로 복귀]
    LangOption --> ApplyGlobal[전역 상태 Provider 즉시 반영] --> BackToHome
    CurrencyOption --> ApplyGlobal
    ThemeOption --> ApplyGlobal
```

---

## 2. 세부 코어 로직 플로우: 목표 평단가 역산 엔진 (Target Price Flow)

```mermaid
flowchart TD
    TP_Start([목표가 역산 진입]) --> InCurrent[현재 보유단가 P0 & 보유수량 Q0 입력]
    InCurrent --> InTarget[목표 희망단가 P_target 입력]
    InTarget --> InAdd[추가 매수단가 P_add 입력]
    InAdd --> ValidCheck{유효성 검증 P_add < P_target < P_0}
    ValidCheck -- 조건 불일치 (도달 불가) --> ErrMsg[경고 문구 표시: 목표 단가는 추가매수가보다 높고 현재단가보다 낮아야 합니다]
    ValidCheck -- 정상 범위 --> CalcQty["공식 적용: Q_add = Q0 * (P0 - P_target) / (P_target - P_add)"]
    CalcQty --> CalcAmount["필요 자금 산출: Total = Q_add * P_add"]
    CalcAmount --> RenderCard[결과 카드 렌더링: 필요 매수 주수 및 추가 투자 원금 표시]
```

---

## 3. VIP 24시간 광고 제거 및 라이프사이클 플로우

```mermaid
flowchart TD
    VIP_Entry([홈 화면 VIP 배너]) --> AdStatusCheck{현재 무광고 활성 상태?}
    AdStatusCheck -- 이미 활성화됨 --> LiveCountdown[잔여 시간 실시간 카운트다운 표시 D-N HH:mm:ss]
    AdStatusCheck -- 만료 또는 미활성 --> ShowRewardBtn[24시간 광고 제거 보상형 광고 시청 버튼 노출]
    ShowRewardBtn --> TapWatchAd[유저 시청 탭]
    TapWatchAd --> AdMobReward[AdMob 보상형 광고 재생]
    AdMobReward --> RewardSuccess{광고 완료 보상 콜백 수신?}
    RewardSuccess -- 성공 --> SetExpiry[현재 시각 + 24시간 만료일 SharedPreferences 저장]
    SetExpiry --> ActiveVIP[VIP 혜택 활성화: 전면/배너 광고 즉시 차단]
    ActiveVIP --> LiveCountdown
    RewardSuccess -- 유저 이탈/실패 --> ToastErr[광고 시청이 완료되지 않았습니다 토스트]
```
