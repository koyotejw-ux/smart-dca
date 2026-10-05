import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../theme/t_membership_colors.dart';
import '../utils/l10n.dart';
import '../providers/language_provider.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class HelpScreen extends ConsumerWidget {
  const HelpScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final lang = ref.watch(languageProvider);
    final bgColor = isDark ? TMembershipColors.darkBg : TMembershipColors.lightBg;
    final titleColor = isDark ? TMembershipColors.darkTextPrimary : TMembershipColors.lightTextPrimary;

    return Scaffold(
      backgroundColor: bgColor,
      appBar: AppBar(
        backgroundColor: bgColor,
        elevation: 0,
        leadingWidth: 56,
        leading: Padding(
          padding: const EdgeInsets.only(left: 16),
          child: Center(
            child: Material(
              color: Colors.transparent,
              child: InkWell(
                onTap: () => Navigator.pop(context),
                borderRadius: BorderRadius.circular(12),
                child: Container(
                  width: 38,
                  height: 38,
                  decoration: BoxDecoration(
                    color: isDark ? TMembershipColors.darkSurface : Colors.white,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(
                      color: isDark ? TMembershipColors.darkCardBorder : TMembershipColors.lightCardBorder,
                      width: 1.2,
                    ),
                    boxShadow: isDark ? [] : TMembershipColors.softShadow(blur: 6, dy: 2),
                  ),
                  child: Center(
                    child: Icon(Icons.close_rounded, color: titleColor, size: 20),
                  ),
                ),
              ),
            ),
          ),
        ),
        title: Text(
          lang == LanguageType.ko ? "도움말 및 가이드" : "Help & Guide",
          style: GoogleFonts.inter(
            color: titleColor,
            fontWeight: FontWeight.w900,
            fontSize: 18,
            letterSpacing: -0.4,
          ),
        ),
      ),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 800),
          child: ListView(
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
            children: [
              _buildGuideCard(
                title: lang == LanguageType.ko ? "물타기(Average Down)란?" : "What is Average Down?",
                content: lang == LanguageType.ko
                    ? "보유한 주식/코인의 가격이 하락했을 때 추가로 분할 매수하여 평균 매수가격을 낮추는 투자 기법입니다. 이후 반등 시 빠르게 원금을 회복하고 수익권으로 전환할 수 있습니다."
                    : "A strategy of buying additional shares as the price drops to lower your overall average purchase price, allowing faster break-even and profit recovery upon rebound.",
                icon: Icons.trending_down_rounded,
                color: TMembershipColors.primaryBlue,
                isDark: isDark,
              ),
              const SizedBox(height: 16),
              _buildGuideCard(
                title: lang == LanguageType.ko ? "스마트 시뮬레이터 사용법" : "How to Use Simulator",
                content: lang == LanguageType.ko
                    ? "1. 현재 보유 중인 평단가와 수량을 입력하세요.\n2. 추가 매수할 가격과 수량을 차수별로 계획합니다.\n3. 상단 대시보드에서 실시간으로 합산된 신규 평단가와 총 투자 원금을 확인하세요.\n4. '시나리오 저장'으로 나중에 언제든 다시 불러올 수 있습니다."
                    : "1. Enter your current average price and quantity.\n2. Plan additional purchase batches (price and shares).\n3. Check real-time calculated average price & total capital on top.\n4. Save scenarios for comparison anytime.",
                icon: Icons.calculate_rounded,
                color: TMembershipColors.accentPurple,
                isDark: isDark,
              ),
              const SizedBox(height: 16),
              _buildGuideCard(
                title: lang == LanguageType.ko ? "목표가 역산 전략 (Target Mode)" : "Target Price Mode",
                content: lang == LanguageType.ko
                    ? "내가 원하는 목표 평단가(예: 본전 또는 특정 가격)를 입력하면, 현재 추가 매수가 기준으로 '정확히 몇 주를 사야 하는지' 역으로 계산해 줍니다. 과도한 무리수를 방지하고 계획적인 비중 관리가 가능합니다."
                    : "Enter your desired target average price, and it automatically calculates exactly how many shares you need to buy at current price. Prevents over-investing and maintains systematic position sizing.",
                icon: Icons.flag_rounded,
                color: TMembershipColors.accentMagenta,
                isDark: isDark,
              ),
              const SizedBox(height: 16),
              _buildGuideCard(
                title: lang == LanguageType.ko ? "AI 음성 비서 사용법" : "Voice AI Assistant",
                content: lang == LanguageType.ko
                    ? "하단의 'AI 비서' 버튼을 누르고 예시 카드를 탭하거나 자연어로 입력하면, 종목명과 평단가, 수량을 자동으로 파싱하여 계산기에 채워 넣고 즉시 계산합니다."
                    : "Tap the floating 'AI Assistant' button and speak or select sample prompts. It parses asset names, prices, and quantities automatically into the calculator.",
                icon: Icons.mic_rounded,
                color: TMembershipColors.accentMint,
                isDark: isDark,
              ),
              const SizedBox(height: 32),
              Center(
                child: Text(
                  lang == LanguageType.ko
                      ? "스마트 물타기 계산기 v3.2\nSmart Clean Design System"
                      : "Smart Average Down Calculator v3.2\nSmart Clean Design System",
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    color: isDark ? TMembershipColors.darkTextTertiary : TMembershipColors.lightTextTertiary,
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              const SizedBox(height: 32),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildGuideCard({
    required String title,
    required String content,
    required IconData icon,
    required Color color,
    required bool isDark,
  }) {
    final cardBg = isDark ? TMembershipColors.darkSurface : TMembershipColors.lightSurface;
    final cardBorder = isDark ? TMembershipColors.darkCardBorder : TMembershipColors.lightCardBorder;
    final titleColor = isDark ? TMembershipColors.darkTextPrimary : TMembershipColors.lightTextPrimary;
    final bodyColor = isDark ? TMembershipColors.darkTextSecondary : TMembershipColors.lightTextSecondary;

    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: cardBg,
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: cardBorder, width: 1.2),
        boxShadow: isDark ? [] : TMembershipColors.softShadow(blur: 12, dy: 3),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: color.withOpacity(0.12),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Icon(icon, color: color, size: 22),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Text(
                  title,
                  style: GoogleFonts.inter(fontWeight: FontWeight.w800, fontSize: 16, color: titleColor),
                ),
              ),
            ],
          ),
          const SizedBox(height: 14),
          Text(
            content,
            style: TextStyle(color: bodyColor, fontSize: 13, height: 1.6),
          ),
        ],
      ),
    );
  }
}
