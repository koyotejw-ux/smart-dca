import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../theme/neon_colors.dart';
import '../utils/l10n.dart';
import '../providers/language_provider.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class HelpScreen extends ConsumerWidget {
  const HelpScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(languageProvider);
    
    return Scaffold(
      backgroundColor: NeonColors.background,
      appBar: AppBar(
        backgroundColor: NeonColors.background,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.close_rounded, color: Colors.white),
          onPressed: () => Navigator.pop(context),
        ),
        title: Text(
          "GUIDE / 도움말",
          style: GoogleFonts.inter(color: NeonColors.cyan, fontWeight: FontWeight.w900, fontSize: 16, letterSpacing: 2),
        ),
      ),
      body: ListView(
        padding: const EdgeInsets.all(24),
        children: [
          _buildGuideSection(
            "물타기란?",
            "보유한 자산의 가격이 하락했을 때 추가로 매수하여 평균 단가를 낮추는 전략입니다. 이 앱은 신규 평단가와 수익권 도달을 위한 필요량을 정밀하게 계산해 줍니다.",
            Icons.trending_down_rounded,
            NeonColors.cyan,
          ),
          const SizedBox(height: 24),
          _buildGuideSection(
            "시뮬레이터 사용법",
            "1. 현재 보유 평단가와 수량을 입력하세요.\n2. 매수할 가격과 수량을 시나리오별로 입력하면 하단에 결과가 즉시 반영됩니다.\n3. 우측 하단의 AC 버튼으로 모든 입력을 초기화할 수 있습니다.",
            Icons.touch_app_rounded,
            NeonColors.pink,
          ),
          const SizedBox(height: 24),
          _buildGuideSection(
            "목표 수익률 전략",
            "특정 수익률(예: 본전, 5% 익절)에 도달하기 위해 필요한 추가 매수량을 역으로 계산해 주는 고급 기능입니다. 무리한 물타기를 방지하고 계획적인 탈출/익절을 돕습니다.",
            Icons.flag_rounded,
            NeonColors.green,
          ),
          const SizedBox(height: 48),
          Center(
            child: Text(
              "NEON STRATEGY v3.0\nPremium Financial Utility",
              textAlign: TextAlign.center,
              style: TextStyle(color: Colors.white24, fontSize: 12, fontWeight: FontWeight.bold),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildGuideSection(String title, String content, IconData icon, Color color) {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: NeonColors.glassyBorder(color.withOpacity(0.3)),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, color: color, size: 24),
              const SizedBox(width: 12),
              Text(title, style: TextStyle(color: color, fontWeight: FontWeight.w900, fontSize: 18)),
            ],
          ),
          const SizedBox(height: 16),
          Text(
            content,
            style: const TextStyle(color: Colors.white70, fontSize: 14, height: 1.6),
          ),
        ],
      ),
    );
  }
}
