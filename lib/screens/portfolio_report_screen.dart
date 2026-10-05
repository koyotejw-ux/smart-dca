import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import 'package:google_fonts/google_fonts.dart';

import '../providers/asset_provider.dart';
import '../providers/currency_provider.dart';
import '../providers/market_provider.dart';
import '../models/asset_model.dart';
import '../theme/t_membership_colors.dart';

class PortfolioReportScreen extends ConsumerWidget {
  const PortfolioReportScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final assets = ref.watch(assetsProvider);
    final currency = ref.watch(currencyProvider);
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
    for (var a in assets) {
      totalInvested += a.initialPrice * a.initialQuantity;
    }

    return Scaffold(
      backgroundColor: bgColor,
      appBar: AppBar(
        backgroundColor: bgColor,
        elevation: 0,
        leading: IconButton(
          icon: Icon(Icons.arrow_back_ios_new_rounded, color: textPrimary, size: 20),
          onPressed: () => Navigator.pop(context),
        ),
        title: Text(
          "포트폴리오 리포트 (Report)",
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
              // T-Membership Total Value Gradient Card
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
                        const Text(
                          "TOTAL PORTFOLIO VALUE",
                          style: TextStyle(
                            color: Colors.white70,
                            fontWeight: FontWeight.w800,
                            fontSize: 11,
                            letterSpacing: 1.5,
                          ),
                        ),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                          decoration: BoxDecoration(
                            color: Colors.white.withOpacity(0.2),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Text(
                            "${assets.length}개 종목",
                            style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 11),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Text(
                      formatter.format(totalInvested),
                      style: GoogleFonts.inter(
                        color: Colors.white,
                        fontWeight: FontWeight.w900,
                        fontSize: 32,
                        letterSpacing: -0.5,
                      ),
                    ),
                    const SizedBox(height: 12),
                    const Divider(color: Colors.white24, height: 1),
                    const SizedBox(height: 10),
                    const Text(
                      "분할 매수 전략으로 체계적인 평단가 관리가 진행 중입니다.",
                      style: TextStyle(color: Colors.white, fontWeight: FontWeight.w600, fontSize: 12),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 28),

              // Risk Heatmap
              Text(
                "종목별 손익 및 회복 현황 (Status)",
                style: GoogleFonts.inter(fontWeight: FontWeight.w900, fontSize: 15, color: textPrimary),
              ),
              const SizedBox(height: 12),
              _buildRiskHeatmap(context, ref, assets, isDark),
              const SizedBox(height: 28),

              // Asset Strategy List
              Text(
                "보유 자산 상세 내역 (Assets)",
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
                    child: Text("등록된 보유 자산이 없습니다.", style: TextStyle(color: textSecondary)),
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
                    final priceAsync = ref.watch(priceProvider(a.symbol));

                    return priceAsync.when(
                      data: (price) {
                        final pnl = ((price.price - a.initialPrice) / a.initialPrice * 100);
                        final isPlus = pnl >= 0;
                        final pnlColor = isPlus ? TMembershipColors.accentMint : TMembershipColors.accentCoral;

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
                                width: 42,
                                height: 42,
                                decoration: BoxDecoration(
                                  color: TMembershipColors.primaryBlue.withOpacity(0.1),
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                child: Center(
                                  child: Text(
                                    a.symbol.length > 2 ? a.symbol.substring(0, 2) : a.symbol,
                                    style: const TextStyle(fontWeight: FontWeight.w900, color: TMembershipColors.primaryBlue),
                                  ),
                                ),
                              ),
                              const SizedBox(width: 14),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(a.name, style: GoogleFonts.inter(fontWeight: FontWeight.w800, fontSize: 14, color: textPrimary)),
                                    const SizedBox(height: 4),
                                    Text(
                                      "${a.initialQuantity.toStringAsFixed(0)}주 • 평단 ${formatter.format(a.initialPrice)}",
                                      style: TextStyle(color: textSecondary, fontSize: 11),
                                    ),
                                  ],
                                ),
                              ),
                              Column(
                                crossAxisAlignment: CrossAxisAlignment.end,
                                children: [
                                  Text(formatter.format(value), style: GoogleFonts.inter(fontWeight: FontWeight.w800, fontSize: 14, color: textPrimary)),
                                  const SizedBox(height: 4),
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                    decoration: BoxDecoration(
                                      color: pnlColor.withOpacity(0.12),
                                      borderRadius: BorderRadius.circular(6),
                                    ),
                                    child: Text(
                                      "${isPlus ? '+' : ''}${pnl.toStringAsFixed(2)}%",
                                      style: TextStyle(color: pnlColor, fontWeight: FontWeight.w900, fontSize: 11),
                                    ),
                                  ),
                                ],
                              ),
                            ],
                          ),
                        );
                      },
                      loading: () => const SizedBox.shrink(),
                      error: (_, __) => const SizedBox.shrink(),
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

  Widget _buildRiskHeatmap(BuildContext context, WidgetRef ref, List<Asset> assets, bool isDark) {
    if (assets.isEmpty) return const SizedBox.shrink();

    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 3,
        crossAxisSpacing: 10,
        mainAxisSpacing: 10,
        childAspectRatio: 1.1,
      ),
      itemCount: assets.length,
      itemBuilder: (context, index) {
        final a = assets[index];
        final priceAsync = ref.watch(priceProvider(a.symbol));

        return priceAsync.when(
          data: (price) {
            final recovery = ((price.price - a.initialPrice) / a.initialPrice * 100);
            final isPlus = recovery >= 0;
            final chipColor = isPlus ? TMembershipColors.accentMint : (recovery > -15 ? TMembershipColors.gold : TMembershipColors.accentCoral);

            return Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: chipColor.withOpacity(isDark ? 0.12 : 0.08),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: chipColor.withOpacity(0.4), width: 1.2),
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    a.symbol,
                    style: TextStyle(
                      color: isDark ? Colors.white70 : Colors.black87,
                      fontWeight: FontWeight.w800,
                      fontSize: 11,
                    ),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                  const SizedBox(height: 6),
                  Text(
                    "${isPlus ? '+' : ''}${recovery.toStringAsFixed(1)}%",
                    style: TextStyle(color: chipColor, fontWeight: FontWeight.w900, fontSize: 15),
                  ),
                ],
              ),
            );
          },
          loading: () => Container(decoration: BoxDecoration(color: Colors.grey.withOpacity(0.1), borderRadius: BorderRadius.circular(16))),
          error: (_, __) => const SizedBox.shrink(),
        );
      },
    );
  }
}
