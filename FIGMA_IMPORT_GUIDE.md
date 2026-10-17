# FIGMA IMPORT GUIDE (피그마 1초 완성 가이드)

본 프로젝트의 디자인 시스템, 아키텍처 플로우차트, 역기획 기능 명세서를 피그마(Figma)에 1초 만에 그대로 이식하는 3단계 가이드입니다.

---

## 1. 디자인 시스템 토큰 이식 (Tokens Studio for Figma)
피그마에 컬러 변수(Variables), 타이포그래피 스타일(Styles)을 코딩된 원본 그대로 한 번에 생성합니다.

1. 피그마에서 빈 캔버스를 엽니다.
2. 상단 메뉴 `Plugins` ➔ **`Tokens Studio for Figma`** 검색 및 실행 (무료)
3. 플러그인 하단 `Settings` ➔ `Load from file/folder` (또는 `Tools` ➔ `Import JSON`) 선택
4. 프로젝트 루트에 있는 **`tokens.json`** 파일을 선택하여 Import
5. **결과**: 피그마 우측 패널의 Color, Typography, Surface, Semantic 스타일이 100% 자동 생성됩니다.

---

## 2. 1920x1080 고해상도 아키텍처 플로우차트 (Vector SVG)
깨지지 않는 벡터(Vector) 형태로 피그마 캔버스에 바로 올리는 방법입니다.

1. 프로젝트 루트의 **`flowchart_vector.svg`** 파일을 피그마 캔버스로 **그냥 드래그 앤 드롭(Drag & Drop)** 합니다.
2. **결과**: 모든 텍스트, 박스, 선(Line)이 피그마의 완전한 벡터 레이어로 분리되어 들어가며, 크기 조절이나 폰트 수정이 자유자재로 가능합니다.
3. 슬라이드 프레임(`Frame 1920x1080`)을 생성한 뒤 그 안에 중앙 정렬로 배치하시면 됩니다.

---

## 3. 화면별 1:1 기능 명세서 레이아웃 (Reverse PRD)
피그마 캔버스에 실물 스크린샷과 함께 매핑할 마크다운 레이아웃입니다.

### [피그마 레이아웃 구조 추천]
- **Frame A (Home Dashboard)**:
  - 이미지: `lib/../live_screen.png`
  - 기능 명세 카드:
    - `01. AI Voice Ingestion`: STT 자연어 파싱을 통한 단가/수량 자동 감지
    - `02. Multi-Currency`: KRW, USD, JPY, EUR 실시간 통화 기호 및 포맷팅
    - `03. VIP Monetization`: 24시간 무광고 보상형 인터랙션 수명 주기 관리
- **Frame B (Simulation Engine)**:
  - 이미지: `real_screen_verified.png`
  - 기능 명세 카드:
    - `01. Weighted Average Formula`: 가중평균 분할 매수 연산
    - `02. Goal Seeking Model`: 목표 평단가 도달을 위한 필수 매수 수량 역산
    - `03. A/B Scenario Matrix`: 자금 배분 최적화 전략 대조

---

## 4. 포함된 파일 목록
- [tokens.json](file:///d:/097.flutter_project/average_down_calculator/tokens.json): W3C 디자인 토큰 규격 파일
- [flowchart_vector.svg](file:///d:/097.flutter_project/average_down_calculator/flowchart_vector.svg): 피그마 전용 벡터 플로우차트
- [REVERSE_PRD_SPEC.md](file:///d:/097.flutter_project/average_down_calculator/REVERSE_PRD_SPEC.md): 상세 기능 정의서
- [USER_FLOW_CHART.md](file:///d:/097.flutter_project/average_down_calculator/USER_FLOW_CHART.md): Mermaid 원본 코드
