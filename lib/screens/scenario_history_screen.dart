import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import 'package:google_fonts/google_fonts.dart';

import '../providers/scenario_provider.dart';
import '../providers/language_provider.dart';
import '../providers/currency_provider.dart';
import '../theme/t_membership_colors.dart';
import 'simulator_screen.dart';

class ScenarioHistoryScreen extends ConsumerWidget {
  const ScenarioHistoryScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final scenarios = ref.watch(scenarioProvider);
    final currency = ref.watch(currencyProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final dateFormat = DateFormat('yyyy.MM.dd HH:mm');
    final currencyFormat = NumberFormat.currency(
      symbol: currency.symbol,
      decimalDigits: currency.decimalDigits,
    );

    final bgColor = isDark ? TMembershipColors.darkBg : TMembershipColors.lightBg;
    final cardBg = isDark ? TMembershipColors.darkSurface : TMembershipColors.lightSurface;
    final cardBorder = isDark ? TMembershipColors.darkCardBorder : TMembershipColors.lightCardBorder;
    final textPrimary = isDark ? TMembershipColors.darkTextPrimary : TMembershipColors.lightTextPrimary;
    final textSecondary = isDark ? TMembershipColors.darkTextSecondary : TMembershipColors.lightTextSecondary;

    final lang = ref.watch(languageProvider);
    final isKo = lang == LanguageType.ko;

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
                    child: Icon(Icons.arrow_back_ios_new_rounded, color: textPrimary, size: 16),
                  ),
                ),
              ),
            ),
          ),
        ),
        title: Text(
          isKo ? "계산 기록 (History)" : "Calculation History",
          style: GoogleFonts.inter(
            color: textPrimary,
            fontWeight: FontWeight.w900,
            fontSize: 18,
            letterSpacing: -0.4,
          ),
        ),
      ),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 800),
          child: scenarios.isEmpty
              ? Center(
                  child: Padding(
                    padding: const EdgeInsets.all(48.0),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Container(
                          width: 80,
                          height: 80,
                          decoration: BoxDecoration(
                            color: TMembershipColors.primaryBlue.withOpacity(0.08),
                            shape: BoxShape.circle,
                          ),
                          child: const Icon(Icons.history_rounded, size: 40, color: TMembershipColors.primaryBlue),
                        ),
                        const SizedBox(height: 20),
                        Text(
                          isKo ? "저장된 물타기 시나리오가 없습니다." : "No saved scenarios yet.",
                          style: TextStyle(color: textPrimary, fontWeight: FontWeight.w800, fontSize: 16),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          isKo ? "시뮬레이터에서 계산 후 시나리오를 저장해 보세요." : "Calculate in the simulator and save scenarios.",
                          style: TextStyle(color: textSecondary, fontSize: 13),
                        ),
                      ],
                    ),
                  ),
                )
              : ListView.builder(
                  padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
                  itemCount: scenarios.length,
                  itemBuilder: (context, index) {
                    final s = scenarios[index];
                    return Container(
                      margin: const EdgeInsets.only(bottom: 14),
                      padding: const EdgeInsets.all(20),
                      decoration: BoxDecoration(
                        color: cardBg,
                        borderRadius: BorderRadius.circular(22),
                        border: Border.all(color: cardBorder, width: 1.2),
                        boxShadow: isDark ? [] : TMembershipColors.softShadow(blur: 14, dy: 4),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Expanded(
                                child: Row(
                                  children: [
                                    Container(
                                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                      decoration: BoxDecoration(
                                        gradient: TMembershipColors.primaryGradient,
                                        borderRadius: BorderRadius.circular(8),
                                      ),
                                      child: const Text("STRATEGY", style: TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold)),
                                    ),
                                    const SizedBox(width: 8),
                                    Expanded(
                                      child: FittedBox(
                                        fit: BoxFit.scaleDown,
                                        alignment: Alignment.centerLeft,
                                        child: Text(
                                          s.name,
                                          style: GoogleFonts.inter(fontWeight: FontWeight.w900, fontSize: 15, color: textPrimary),
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                              const SizedBox(width: 8),
                              Text(dateFormat.format(s.createdAt), style: TextStyle(color: textSecondary, fontSize: 11)),
                            ],
                          ),
                          const SizedBox(height: 16),
                          Row(
                            children: [
                              Expanded(
                                child: _buildInfoItem(isKo ? "초기 단가" : "Init Price", "${currencyFormat.format(s.initialPrice)}", textSecondary, textPrimary),
                              ),
                              Expanded(
                                child: _buildInfoItem(isKo ? "초기 수량" : "Init Qty", "${s.initialQuantity.toStringAsFixed(0)}", textSecondary, textPrimary),
                              ),
                              Expanded(
                                child: _buildInfoItem(isKo ? "추가 매수" : "Batches", "${s.batches.length}${isKo ? '회' : 'x'}", textSecondary, TMembershipColors.accentMagenta),
                              ),
                            ],
                          ),
                          const SizedBox(height: 16),
                          Divider(height: 1, color: isDark ? TMembershipColors.darkDivider : TMembershipColors.lightDivider),
                          const SizedBox(height: 10),
                          Row(
                            children: [
                              Expanded(
                                child: ElevatedButton.icon(
                                  onPressed: () {
                                    HapticFeedback.lightImpact();
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder: (context) => SimulatorScreen(initialScenario: s),
                                      ),
                                    );
                                  },
                                  icon: const Icon(Icons.play_arrow_rounded, color: Colors.white, size: 18),
                                  label: FittedBox(
                                    fit: BoxFit.scaleDown,
                                    child: Text(
                                      isKo ? "시뮬레이터로 불러오기" : "Load in Simulator",
                                      style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w800, fontSize: 13),
                                    ),
                                  ),
                                  style: ElevatedButton.styleFrom(
                                    backgroundColor: TMembershipColors.primaryBlue,
                                    padding: const EdgeInsets.symmetric(vertical: 10),
                                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                                    elevation: 0,
                                  ),
                                ),
                              ),
                              const SizedBox(width: 8),
                              IconButton(
                                onPressed: () {
                                  ref.read(scenarioProvider.notifier).removeScenario(s.id);
                                  ScaffoldMessenger.of(context).showSnackBar(
                                    SnackBar(content: Text(isKo ? "시나리오가 삭제되었습니다." : "Scenario deleted."), behavior: SnackBarBehavior.floating),
                                  );
                                },
                                icon: const Icon(Icons.delete_outline_rounded, color: TMembershipColors.accentCoral, size: 22),
                              ),
                            ],
                          ),
                        ],
                      ),
                    );
                  },
                ),
        ),
      ),
    );
  }

  Widget _buildInfoItem(String label, String value, Color labelColor, Color valueColor) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: TextStyle(fontSize: 11, color: labelColor, fontWeight: FontWeight.w600)),
        const SizedBox(height: 4),
        FittedBox(
          fit: BoxFit.scaleDown,
          alignment: Alignment.centerLeft,
          child: Text(value, style: GoogleFonts.inter(fontWeight: FontWeight.w800, fontSize: 14, color: valueColor)),
        ),
      ],
    );
  }
}
