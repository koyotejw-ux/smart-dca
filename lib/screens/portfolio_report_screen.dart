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
      symbol: currency.symbol,
      decimalDigits: currency.decimalDigits,
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
      body: LayoutBuilder(
        builder: (context, constraints) {
          final isWide = constraints.maxWidth > 550;

          return Center(
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 800),
              child: ListView(
                padding: EdgeInsets.symmetric(
                  horizontal: isWide ? 24 : 16,
                  vertical: 16,
                ),
                children: [
                  // Total Value Gradient Card
                  Container(
                    padding: EdgeInsets.all(isWide ? 24 : 18),
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
                            Expanded(
                              child: Text(
                                isKo ? "총 투자 원금 (PORTFOLIO VALUE)" : "TOTAL INVESTED VALUE",
                                maxLines: 1,
                                overflow: TextOverflow.ellipsis,
                                style: const TextStyle(
                                  color: Colors.white70,
                                  fontWeight: FontWeight.w800,
                                  fontSize: 11,
                                  letterSpacing: 1.1,
                                ),
                              ),
                            ),
                            const SizedBox(width: 8),
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
                              fontSize: isWide ? 34 : 28,
                              letterSpacing: -0.5,
                            ),
                          ),
                        ),
                        const SizedBox(height: 12),
                        const Divider(color: Colors.white24, height: 1),
                        const SizedBox(height: 10),
                        Wrap(
                          spacing: 12,
                          runSpacing: 4,
                          alignment: WrapAlignment.spaceBetween,
                          crossAxisAlignment: WrapCrossAlignment.center,
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
                  const SizedBox(height: 24),

                  // Stock Allocation Breakdown
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Expanded(
                        child: Text(
                          isKo ? "종목별 투자 비중 (Allocation)" : "Asset Allocation",
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                          style: GoogleFonts.inter(fontWeight: FontWeight.w900, fontSize: 15, color: textPrimary),
                        ),
                      ),
                      const SizedBox(width: 8),
                      Text(
                        isKo ? "포트폴리오 분산도" : "Diversification",
                        style: TextStyle(color: textSecondary, fontSize: 12, fontWeight: FontWeight.w600),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  _buildAllocationHeatmap(context, assets, totalInvested, isDark, isKo, constraints.maxWidth),
                  const SizedBox(height: 24),

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
                          margin: const EdgeInsets.only(bottom: 10),
                          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                          decoration: BoxDecoration(
                            color: cardBg,
                            borderRadius: BorderRadius.circular(16),
                            border: Border.all(color: cardBorder, width: 1.2),
                            boxShadow: isDark ? [] : TMembershipColors.softShadow(blur: 8, dy: 2),
                          ),
                          child: Row(
                            children: [
                              Container(
                                width: 40,
                                height: 40,
                                decoration: BoxDecoration(
                                  color: TMembershipColors.primaryBlue.withOpacity(0.1),
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                child: const Center(
                                  child: Icon(Icons.show_chart_rounded, color: TMembershipColors.primaryBlue, size: 22),
                                ),
                              ),
                              const SizedBox(width: 12),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  mainAxisSize: MainAxisSize.min,
                                  children: [
                                    Text(
                                      displayName,
                                      maxLines: 1,
                                      overflow: TextOverflow.ellipsis,
                                      style: GoogleFonts.inter(fontWeight: FontWeight.w800, fontSize: 14, color: textPrimary),
                                    ),
                                    const SizedBox(height: 3),
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
                              const SizedBox(width: 10),
                              Column(
                                crossAxisAlignment: CrossAxisAlignment.end,
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  FittedBox(
                                    fit: BoxFit.scaleDown,
                                    child: Text(
                                      formatter.format(value),
                                      style: GoogleFonts.inter(fontWeight: FontWeight.w800, fontSize: 13.5, color: textPrimary),
                                    ),
                                  ),
                                  const SizedBox(height: 3),
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                    decoration: BoxDecoration(
                                      color: TMembershipColors.primaryBlue.withOpacity(0.1),
                                      borderRadius: BorderRadius.circular(6),
                                    ),
                                    child: Text(
                                      "${isKo ? '비중 ' : ''}${weight.toStringAsFixed(1)}%",
                                      style: const TextStyle(
                                        color: TMembershipColors.primaryBlue,
                                        fontWeight: FontWeight.w800,
                                        fontSize: 10.5,
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
                  const SizedBox(height: 32),
                ],
              ),
            ),
          );
        },
      ),
    );
  }

  Widget _buildAllocationHeatmap(
    BuildContext context,
    List<Asset> assets,
    double totalInvested,
    bool isDark,
    bool isKo,
    double maxWidth,
  ) {
    if (assets.isEmpty) return const SizedBox.shrink();

    final colors = [
      TMembershipColors.primaryBlue,
      TMembershipColors.accentMint,
      TMembershipColors.gold,
      const Color(0xFF8B5CF6),
      const Color(0xFFEC4899),
    ];

    // Responsive columns and aspect ratio
    final int crossAxisCount = maxWidth > 650 ? 4 : (maxWidth < 360 ? 2 : 3);
    final double childAspectRatio = maxWidth > 650 ? 1.4 : (maxWidth < 360 ? 1.3 : 1.25);

    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: crossAxisCount,
        crossAxisSpacing: 8,
        mainAxisSpacing: 8,
        childAspectRatio: childAspectRatio,
      ),
      itemCount: assets.length,
      itemBuilder: (context, index) {
        final a = assets[index];
        final value = a.initialPrice * a.initialQuantity;
        final weight = totalInvested > 0 ? (value / totalInvested * 100) : 0.0;
        final color = colors[index % colors.length];
        final displayName = (a.name == 'New Asset' || a.name.trim().isEmpty) ? (isKo ? '보유 종목' : 'Stock') : a.name;

        return Container(
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
          decoration: BoxDecoration(
            color: color.withOpacity(isDark ? 0.12 : 0.08),
            borderRadius: BorderRadius.circular(14),
            border: Border.all(color: color.withOpacity(0.35), width: 1.2),
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            mainAxisSize: MainAxisSize.min,
            children: [
              Flexible(
                child: Text(
                  displayName,
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    color: isDark ? Colors.white70 : Colors.black87,
                    fontWeight: FontWeight.w800,
                    fontSize: 11.5,
                  ),
                ),
              ),
              const SizedBox(height: 3),
              FittedBox(
                fit: BoxFit.scaleDown,
                child: Text(
                  "${weight.toStringAsFixed(1)}%",
                  style: TextStyle(color: color, fontWeight: FontWeight.w900, fontSize: 15),
                ),
              ),
              const SizedBox(height: 2),
              FittedBox(
                fit: BoxFit.scaleDown,
                child: Text(
                  "${a.initialQuantity.toStringAsFixed(0)}${isKo ? '주' : ' shs'}",
                  style: TextStyle(
                    color: isDark ? Colors.white38 : Colors.black45,
                    fontWeight: FontWeight.w600,
                    fontSize: 9.5,
                  ),
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}
