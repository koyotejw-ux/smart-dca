import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../theme/neon_colors.dart';

class MasterGuideOverlay extends StatefulWidget {
  final VoidCallback onFinish;
  const MasterGuideOverlay({super.key, required this.onFinish});

  @override
  State<MasterGuideOverlay> createState() => _MasterGuideOverlayState();
}

class _MasterGuideOverlayState extends State<MasterGuideOverlay> {
  int _step = 0;

  final List<GuideStep> _steps = [
    GuideStep(
      title: "1. 마스터 데이터 입력",
      description: "화면 최상단 [STEP 1] 카드에 현재 보유 중인\n평단가와 수량을 가장 먼저 입력하세요.\n이 값이 모든 손익 계산의 기준점이 됩니다.",
      icon: Icons.input_rounded,
    ),
    GuideStep(
      title: "2. 정교한 물타기 계획",
      description: "[STEP 2]의 그리드 시스템을 활용하여\n추가 평단과 수량을 입력하세요.\n여러 번의 분할 매수 시나리오도 완벽하게 지원합니다.",
      icon: Icons.grid_view_rounded,
    ),
    GuideStep(
      title: "3. 리스크 & 수익 시뮬레이션",
      description: "'What-If' 슬라이더를 움직여 주가 변동에 따른\n수익률을 실시간으로 확인하고,\n시나리오 B를 통해 최적의 탈출 지점을 찾으세요.",
      icon: Icons.analytics_rounded,
    ),
  ];

  @override
  Widget build(BuildContext context) {
    final currentStep = _steps[_step];

    return Container(
      color: Colors.black.withOpacity(0.8),
      width: double.infinity,
      height: double.infinity,
      child: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(32.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(currentStep.icon, size: 80, color: NeonColors.cyan)
                  .animate(key: ValueKey('icon_$_step'))
                  .scale(duration: 400.ms, curve: Curves.easeOutBack)
                  .shimmer(delay: 500.ms),
              const SizedBox(height: 32),
              Text(
                currentStep.title,
                textAlign: TextAlign.center,
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 28,
                  fontWeight: FontWeight.w900,
                ),
              ).animate(key: ValueKey('title_$_step')).fadeIn().slideY(begin: 0.2),
              const SizedBox(height: 16),
              Text(
                currentStep.description,
                textAlign: TextAlign.center,
                style: TextStyle(
                  color: Colors.white.withOpacity(0.8),
                  fontSize: 18,
                  height: 1.5,
                ),
              ).animate(key: ValueKey('desc_$_step')).fadeIn(delay: 200.ms),
              const SizedBox(height: 64),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: List.generate(_steps.length, (index) => Container(
                  width: 12,
                  height: 12,
                  margin: const EdgeInsets.all(4),
                  decoration: BoxDecoration(
                    color: _step == index ? NeonColors.cyan : Colors.white24,
                    shape: BoxShape.circle,
                  ),
                )),
              ),
              const SizedBox(height: 32),
              ElevatedButton(
                onPressed: () {
                  if (_step < _steps.length - 1) {
                    setState(() => _step++);
                  } else {
                    widget.onFinish();
                  }
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: NeonColors.cyan,
                  foregroundColor: Colors.black,
                  minimumSize: const Size(200, 64),
                ),
                child: Text(_step < _steps.length - 1 ? "다음" : "시작하기"),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class GuideStep {
  final String title;
  final String description;
  final IconData icon;
  GuideStep({required this.title, required this.description, required this.icon});
}
