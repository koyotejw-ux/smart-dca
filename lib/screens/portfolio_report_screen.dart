import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import 'package:google_fonts/google_fonts.dart';

import '../providers/asset_provider.dart';
import '../providers/currency_provider.dart';
import '../providers/language_provider.dart';
import '../models/asset_model.dart';
import '../theme/t_membership_colors.dart';

class PortfolioReportScreen extends ConsumerWidget {
  const PortfolioReportScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final assets = ref.watch(assetsProvider);
    final currency = ref.watch(currencyProvider);
    final lang = ref.watch(languageProvider);
    final isKo = lang == LanguageType.ko;
    final isDark = Theme.of(context).brightness == Brightness.dark;

    final bgColor = isDark ? TMembershipColors.darkBg : TMembershipColors.lightBg;
    final cardBg = isDark ? TMembershipColors.darkSurface : TMembershipColors.lightSurface;
    final cardBorder = isDark ? TMembershipColors.darkCardBorder : TMembershipColors.lightCardBorder;
    final textPrimary = isDark ? TMembershipColors.darkTextPrimary : TMembershipColors.lightTextPrimary;
    final textSecondary = isDark ? TMembershipColors.darkTextSecondary : TMembershipColors.lightTextSecondary;

    final formatter = NumberFormat.currency(
      symbol: currency == CurrencyType.krw ? '₩' : '\$',
      decimalDigits: currency == CurrencyType.krw ? 0 : 2,
    );

    double totalInvested = 0;
    double totalShares = 0;
    for (var a in assets) {
      totalInvested += a.initialPrice * a.initialQuantity;
      totalShares += a.initialQuantity;
    }

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
          isKo ? "포트폴리오 리포트" : "Portfolio Report",
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
          child: ListView(
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
            children: [
              // Total Value Gradient Card
              Container(
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  gradient: TMembershipColors.primaryGradient,
                  borderRadius: BorderRadius.circular(24),
                  boxShadow: TMembershipColors.colorfulGlow(TMembershipColors.primaryBlue, opacity: 0.35),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          isKo ? "총 투자 원금 (PORTFOLIO VALUE)" : "TOTAL INVESTED VALUE",
                          style: const TextStyle(
                            color: Colors.white70,
                            fontWeight: FontWeight.w800,
                            fontSize: 11,
                            letterSpacing: 1.2,
                          ),
                        ),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 9, vertical: 4),
                          decoration: BoxDecoration(
                            color: Colors.white.withOpacity(0.2),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Text(
                            "${assets.length}${isKo ? '개 관리 종목' : ' Stocks'}",
                            style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 11),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    FittedBox(
                      fit: BoxFit.scaleDown,
                      alignment: Alignment.centerLeft,
                      child: Text(
                        formatter.format(totalInvested),
                        style: GoogleFonts.inter(
                          color: Colors.white,
                          fontWeight: FontWeight.w900,
                          fontSize: 32,
                          letterSpacing: -0.5,
                        ),
                      ),
                    ),
                    const SizedBox(height: 12),
                    const Divider(color: Colors.white24, height: 1),
                    const SizedBox(height: 10),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          isKo ? "총 보유 수량: ${totalShares.toStringAsFixed(0)}주" : "Total shares: ${totalShares.toStringAsFixed(0)}",
                          style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w700, fontSize: 12),
                        ),
                        Text(
                          isKo ? "분할 매수 계획 수립 완료" : "DCA Plan Active",
                          style: const TextStyle(color: Colors.white70, fontWeight: FontWeight.w600, fontSize: 11),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 28),

              // Stock Allocation Breakdown
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    isKo ? "종목별 투자 비중 (Allocation)" : "Asset Allocation",
                    style: GoogleFonts.inter(fontWeight: FontWeight.w900, fontSize: 15, color: textPrimary),
                  ),
                  Text(
                    isKo ? "포트폴리오 분산도" : "Diversification",
                    style: TextStyle(color: textSecondary, fontSize: 12, fontWeight: FontWeight.w600),
                  ),
                ],
              ),
              const SizedBox(height: 12),
              _buildAllocationHeatmap(context, assets, totalInvested, isDark, isKo),
              const SizedBox(height: 28),

              // Asset Details List
              Text(
                isKo ? "보유 종목별 평단가 및 투자 내역" : "Stock Holdings & Average Prices",
                style: GoogleFonts.inter(fontWeight: FontWeight.w900, fontSize: 15, color: textPrimary),
              ),
              const SizedBox(height: 12),
              if (assets.isEmpty)
                Container(
                  padding: const EdgeInsets.all(32),
                  decoration: BoxDecoration(
                    color: cardBg,
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: cardBorder),
                  ),
                  child: Center(
                    child: Text(
                      isKo ? "등록된 보유 종목이 없습니다." : "No registered stock assets.",
                      style: TextStyle(color: textSecondary),
                    ),
                  ),
                )
              else
                ListView.builder(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  itemCount: assets.length,
                  itemBuilder: (context, index) {
                    final a = assets[index];
                    final value = a.initialPrice * a.initialQuantity;
                    final weight = totalInvested > 0 ? (value / totalInvested * 100) : 0.0;
                    final displayName = (a.name == 'New Asset' || a.name.trim().isEmpty) ? (isKo ? '보유 종목' : 'Stock') : a.name;

                    return Container(
                      margin: const EdgeInsets.only(bottom: 12),
                      padding: const EdgeInsets.all(18),
                      decoration: BoxDecoration(
                        color: cardBg,
                        borderRadius: BorderRadius.circular(18),
                        border: Border.all(color: cardBorder, width: 1.2),
                        boxShadow: isDark ? [] : TMembershipColors.softShadow(blur: 10, dy: 3),
                      ),
                      child: Row(
                        children: [
                          Container(
                            width: 44,
                            height: 44,
                            decoration: BoxDecoration(
                              color: TMembershipColors.primaryBlue.withOpacity(0.1),
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: const Center(
                              child: Icon(Icons.show_chart_rounded, color: TMembershipColors.primaryBlue, size: 24),
                            ),
                          ),
                          const SizedBox(width: 14),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                FittedBox(
                                  fit: BoxFit.scaleDown,
                                  alignment: Alignment.centerLeft,
                                  child: Text(
                                    displayName,
                                    style: GoogleFonts.inter(fontWeight: FontWeight.w800, fontSize: 14, color: textPrimary),
                                  ),
                                ),
                                const SizedBox(height: 4),
                                FittedBox(
                                  fit: BoxFit.scaleDown,
                                  alignment: Alignment.centerLeft,
                                  child: Text(
                                    "${a.initialQuantity.toStringAsFixed(0)}${isKo ? '주' : ' shares'} • ${isKo ? '평단' : 'Avg'} ${formatter.format(a.initialPrice)}",
                                    style: TextStyle(color: textSecondary, fontSize: 11, fontWeight: FontWeight.w500),
                                  ),
                                ),
                              ],
                            ),
                          ),
                          const SizedBox(width: 8),
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.end,
                            children: [
                              FittedBox(
                                fit: BoxFit.scaleDown,
                                child: Text(
                                  formatter.format(value),
                                  style: GoogleFonts.inter(fontWeight: FontWeight.w800, fontSize: 14, color: textPrimary),
                                ),
                              ),
                              const SizedBox(height: 4),
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 2),
                                decoration: BoxDecoration(
                                  color: TMembershipColors.primaryBlue.withOpacity(0.1),
                                  borderRadius: BorderRadius.circular(6),
                                ),
                                child: Text(
                                  "${isKo ? '비중 ' : ''}${weight.toStringAsFixed(1)}%",
                                  style: const TextStyle(
                                    color: TMembershipColors.primaryBlue,
                                    fontWeight: FontWeight.w800,
                                    fontSize: 11,
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    );
                  },
                ),
              const SizedBox(height: 40),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildAllocationHeatmap(BuildContext context, List<Asset> assets, double totalInvested, bool isDark, bool isKo) {
    if (assets.isEmpty) return const SizedBox.shrink();

    final colors = [
      TMembershipColors.primaryBlue,
      TMembershipColors.accentMint,
      TMembershipColors.gold,
      const Color(0xFF8B5CF6),
      const Color(0xFFEC4899),
    ];

    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 3,
        crossAxisSpacing: 10,
        mainAxisSpacing: 10,
        childAspectRatio: 1.15,
      ),
      itemCount: assets.length,
      itemBuilder: (context, index) {
        final a = assets[index];
        final value = a.initialPrice * a.initialQuantity;
        final weight = totalInvested > 0 ? (value / totalInvested * 100) : 0.0;
        final color = colors[index % colors.length];
        final displayName = (a.name == 'New Asset' || a.name.trim().isEmpty) ? (isKo ? '보유 종목' : 'Stock') : a.name;

        return Container(
          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 12),
          decoration: BoxDecoration(
            color: color.withOpacity(isDark ? 0.12 : 0.08),
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: color.withOpacity(0.35), width: 1.2),
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              FittedBox(
                fit: BoxFit.scaleDown,
                child: Text(
                  displayName,
                  style: TextStyle(
                    color: isDark ? Colors.white70 : Colors.black87,
                    fontWeight: FontWeight.w800,
                    fontSize: 12,
                  ),
                ),
              ),
              const SizedBox(height: 6),
              Text(
                "${weight.toStringAsFixed(1)}%",
                style: TextStyle(color: color, fontWeight: FontWeight.w900, fontSize: 16),
              ),
              const SizedBox(height: 2),
              Text(
                "${a.initialQuantity.toStringAsFixed(0)}${isKo ? '주' : ' shs'}",
                style: TextStyle(
                  color: isDark ? Colors.white38 : Colors.black45,
                  fontWeight: FontWeight.w600,
                  fontSize: 10,
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}
