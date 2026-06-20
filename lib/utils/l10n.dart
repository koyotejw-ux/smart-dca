import '../providers/language_provider.dart';

class L10n {
  static const _data = {
    'app_title': {
      LanguageType.ko: '물타기 계산기',
      LanguageType.en: 'Avg Down Calculator',
    },
    'my_portfolio': {
      LanguageType.ko: '내 포트폴리오',
      LanguageType.en: 'My Portfolio',
    },
    'total_invested': {
      LanguageType.ko: '총 투자금',
      LanguageType.en: 'Total Invested',
    },
    'current_value': {
      LanguageType.ko: '현재 가치',
      LanguageType.en: 'Current Value',
    },
    'pnl': {
      LanguageType.ko: '수익금',
      LanguageType.en: 'P&L',
    },
    'allocation': {
      LanguageType.ko: '자산 비중',
      LanguageType.en: 'Allocation',
    },
    'quick_actions': {
      LanguageType.ko: '빠른 도구',
      LanguageType.en: 'Quick Actions',
    },
    'simulator': {
      LanguageType.ko: '물타기 계산기',
      LanguageType.en: 'Avg Calculator',
    },
    'target_price': {
      LanguageType.ko: '목표 단가 계산',
      LanguageType.en: 'Target Price',
    },
    'ai_analysis': {
      LanguageType.ko: '음성 입력 (AI)',
      LanguageType.en: 'Voice Input (AI)',
    },
    'my_assets': {
      LanguageType.ko: '내 자산',
      LanguageType.en: 'My Assets',
    },
    'view_all': {
      LanguageType.ko: '전체 보기',
      LanguageType.en: 'View All',
    },
    'sim_result': {
      LanguageType.ko: '시뮬레이션 결과',
      LanguageType.en: 'Simulation Result',
    },
    'new_avg_price': {
      LanguageType.ko: '예상 평균 단가',
      LanguageType.en: 'New Avg Price',
    },
    'total_qty': {
      LanguageType.ko: '총 수량',
      LanguageType.en: 'Total Quantity',
    },
    'total_investment': {
      LanguageType.ko: '최종 투자 금액',
      LanguageType.en: 'Total Investment',
    },
    'ai_insight_title': {
      LanguageType.ko: 'AI 전략 인사이트',
      LanguageType.en: 'AI Strategy Insight',
    },
    'full_report': {
      LanguageType.ko: '상세 리포트 보기',
      LanguageType.en: 'View Full Report',
    },
    'save_to_portfolio': {
      LanguageType.ko: '포트폴리오에 저장',
      LanguageType.en: 'Save to Portfolio',
    },
    'add_batch': {
      LanguageType.ko: '구매 내역 추가',
      LanguageType.en: 'Add Batch',
    },
    'simulate_all': {
      LanguageType.ko: '전체 시뮬레이션',
      LanguageType.en: 'Simulate All',
    },
    'current_position': {
      LanguageType.ko: '현재 보유 현황',
      LanguageType.en: 'Current Position',
    },
    'asset_name': {
      LanguageType.ko: '자산명',
      LanguageType.en: 'Asset Name',
    },
    'symbol': {
      LanguageType.ko: '심볼',
      LanguageType.en: 'Symbol',
    },
    'avg_price': {
      LanguageType.ko: '평단가',
      LanguageType.en: 'Avg Price',
    },
    'quantity': {
      LanguageType.ko: '수량',
      LanguageType.en: 'Quantity',
    },
    'price': {
      LanguageType.ko: '가격',
      LanguageType.en: 'Price',
    },
    'language': {
      LanguageType.ko: '언어 설정',
      LanguageType.en: 'Language',
    },
    'ai_header': {
      LanguageType.ko: '스크린샷 인식',
      LanguageType.en: 'Screenshot Recognition',
    },
    'ai_desc': {
      LanguageType.ko: 'MTS 계좌 화면을 업로드하세요.\nGemini가 정보를 자동으로 추출합니다.',
      LanguageType.en: 'Upload your MTS balance screen.\nGemini will extract the prices automatically.',
    },
    'pick_screenshot': {
      LanguageType.ko: '스크린샷 선택',
      LanguageType.en: 'Pick Screenshot',
    },
    'extracted_data': {
      LanguageType.ko: '추출된 데이터',
      LanguageType.en: 'Extracted Data',
    },
    'use_in_sim': {
      LanguageType.ko: '시뮬레이터에서 사용하기',
      LanguageType.en: 'Use this data in Simulator',
    },
    'parse_error': {
      LanguageType.ko: '데이터 분석에 실패했습니다. 더 선명한 스크린샷으로 시도해 주세요.',
      LanguageType.en: 'Failed to parse data. Try a clearer screenshot.',
    },
    'required_qty': {
      LanguageType.ko: '필요 매수 수량',
      LanguageType.en: 'Required Quantity',
    },
    'total_cost': {
      LanguageType.ko: '총 매수 비용',
      LanguageType.en: 'Total Cost',
    },
    'target_settings': {
      LanguageType.ko: '목표 설정',
      LanguageType.en: 'Target Settings',
    },
    'target_avg_price': {
      LanguageType.ko: '목표 단가',
      LanguageType.en: 'Target Avg Price',
    },
    'purchase_price': {
      LanguageType.ko: '현재 매매가',
      LanguageType.en: 'New Purchase Price',
    },
    'find_amount': {
      LanguageType.ko: '필요 수량 계산하기',
      LanguageType.en: 'Find Required Amount',
    },
    'onboarding_title_1': {
      LanguageType.ko: '물타기란 무엇인가요?',
      LanguageType.en: 'What is Average Down?',
    },
    'onboarding_desc_1': {
      LanguageType.ko: '평균 단가를 낮추는 것은 손실을 회복하는 가장 과학적인 방법입니다.',
      LanguageType.en: 'Lowering average price is the most scientific way to recover.',
    },
    'onboarding_title_2': {
      LanguageType.ko: '정밀한 계산',
      LanguageType.en: 'Precise Calculation',
    },
    'onboarding_desc_2': {
      LanguageType.ko: '목표 단가에 도달하기 위해 필요한 정확한 수량을 즉시 계산하세요.',
      LanguageType.en: 'Calculate the exact quantity needed to reach your target price.',
    },
    'onboarding_title_3': {
      LanguageType.ko: '포트폴리오 관리',
      LanguageType.en: 'Portfolio Management',
    },
    'onboarding_desc_3': {
      LanguageType.ko: '내 자산의 건전성을 확인하고 AI의 전략적 조언을 받으세요.',
      LanguageType.en: 'Check portfolio health and get strategic AI insights.',
    },
    'get_started': {
      LanguageType.ko: '시작하기',
      LanguageType.en: 'Get Started',
    },
    'next': {
      LanguageType.ko: '다음',
      LanguageType.en: 'Next',
    },
    'skip': {
      LanguageType.ko: '건너뛰기',
      LanguageType.en: 'Skip',
    },
    'outcome_metrics': {
      LanguageType.ko: '시뮬레이션 지표',
      LanguageType.en: 'Outcome Metrics',
    },
    'target_calculator': {
      LanguageType.ko: '목표 달성 계산기',
      LanguageType.en: 'Target Goal Calculator',
    },
    'scenario_compare': {
      LanguageType.ko: '시나리오 비교',
      LanguageType.en: 'Scenario Compare',
    },
    'step_1_initial': {
      LanguageType.ko: '1단계: 초기 진입 현황',
      LanguageType.en: 'Step 1: Initial Position',
    },
    'step_1_desc': {
      LanguageType.ko: '현재 보유 중인 자산의 평단가와 수량을 입력하세요.',
      LanguageType.en: 'Enter your current average price and quantity hold.',
    },
    'step_2_plan': {
      LanguageType.ko: '2단계: 추가 매수 계획',
      LanguageType.en: 'Step 2: Additional Buy Plan',
    },
    'step_2_desc': {
      LanguageType.ko: '희망하는 시나리오별 매수 가격과 수량을 설정하세요.',
      LanguageType.en: 'Set your desired buy prices and quantities for scenarios.',
    },
    'dashboard_banner': {
      LanguageType.ko: '전략 요약',
      LanguageType.en: 'Strategy Summary',
    },
    'label_sim': {
      LanguageType.ko: '시뮬레이션 시작',
      LanguageType.en: 'Start Simulation',
    },
    'label_history': {
      LanguageType.ko: '히스토리',
      LanguageType.en: 'History',
    },
    'label_portfolio': {
      LanguageType.ko: '포트폴리오',
      LanguageType.en: 'Portfolio',
    },
    'privacy_title': {
      LanguageType.ko: '보안 및 개인정보기록',
      LanguageType.en: 'Privacy & Security',
    },
    'privacy_desc': {
      LanguageType.ko: '모든 데이터는 기기에 로컬로만 저장되며 외부로 전송되지 않습니다.',
      LanguageType.en: 'All data is stored locally on device and never transmitted.',
    },
    'enter_position_msg': {
      LanguageType.ko: '보유 현황을 입력하여 시뮬레이션을 시작하세요.',
      LanguageType.en: 'Enter your position to start simulation.',
    },
    'save_to_portfolio_success': {
      LanguageType.ko: '포트폴리오에 성공적으로 저장되었습니다.',
      LanguageType.en: 'Saved to portfolio successfully.',
    },
    'ready_msg': {
      LanguageType.ko: '준비되셨나요?',
      LanguageType.en: 'Are you ready?',
    },
    'voice_price_hint': {
      LanguageType.ko: '가격을 말씀해 주세요 (예: "만 오천 원")',
      LanguageType.en: 'Please say the price (e.g. "One thousand dollars")',
    },
    'close': {
      LanguageType.ko: '닫기',
      LanguageType.en: 'Close',
    },
    'fee_include': {
      LanguageType.ko: '거래 수수료 포함 (0.015%)',
      LanguageType.en: 'Include Trading Fee (0.015%)',
    },
    'bull_mode_label': {
      LanguageType.ko: '불타기 시뮬레이션 (Bull Mode)',
      LanguageType.en: 'Bull Mode Simulation',
    },
    'save_scenario_label': {
      LanguageType.ko: '이 시나리오 저장하기 (히스토리)',
      LanguageType.en: 'Save this Scenario (History)',
    },
    'comparison_view': {
      LanguageType.ko: '평단가 비교 분석',
      LanguageType.en: 'Average Price Comparison',
    },
    'current_avg': {
      LanguageType.ko: '현재 평단',
      LanguageType.en: 'Current Avg',
    },
    'after_sim': {
      LanguageType.ko: '물타기 후',
      LanguageType.en: 'After Avg Down',
    },
    'drop_strategy': {
      LanguageType.ko: '추가 매수 전략 (Drop Strategy)',
      LanguageType.en: 'Additional Buy Strategy',
    },
    'drop_label': {
      LanguageType.ko: '하락',
      LanguageType.en: 'Drop',
    },
    'target_label': {
      LanguageType.ko: '목표가',
      LanguageType.en: 'Target',
    },
    'buy_qty_label': {
      LanguageType.ko: '매수량',
      LanguageType.en: 'Buy Qty',
    },
  };

  static String s(LanguageType lang, String key) {
    if (!_data.containsKey(key)) return key;
    return _data[key]![lang] ?? key;
  }
}
