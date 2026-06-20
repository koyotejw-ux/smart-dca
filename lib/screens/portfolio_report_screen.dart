import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../providers/asset_provider.dart';
import '../providers/currency_provider.dart';
import '../providers/language_provider.dart';
import '../utils/l10n.dart';
import '../theme/neon_colors.dart';
import '../providers/market_provider.dart';
import '../models/asset_model.dart';
import 'package:google_fonts/google_fonts.dart';
import '../widgets/one_ui_scroll_view.dart';

class PortfolioReportScreen extends ConsumerWidget {
  const PortfolioReportScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final assets = ref.watch(assetsProvider);
    final currency = ref.watch(currencyProvider);
    final lang = ref.watch(languageProvider);
    
    final formatter = NumberFormat.currency(
      symbol: currency == CurrencyType.krw ? '\u20a9' : '\$',
      decimalDigits: currency == CurrencyType.krw ? 0 : 2,
    );

    double totalInvested = 0;
    for (var a in assets) {
      totalInvested += a.initialPrice * a.initialQuantity;
    }

    return Scaffold(
      backgroundColor: NeonColors.background,
      appBar: AppBar(
        backgroundColor: NeonColors.background,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios_new_rounded, color: Colors.white),
          onPressed: () => Navigator.pop(context),
        ),
        title: Text(
          "DASHBOARD / 리포트",
          style: GoogleFonts.inter(color: NeonColors.cyan, fontWeight: FontWeight.w900, fontSize: 16, letterSpacing: 2),
        ),
      ),
      body: ListView(
        padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 24),
        children: [
          // Neon Summary Card
          Container(
            padding: const EdgeInsets.all(24),
            decoration: NeonColors.glassyBorder(NeonColors.pink),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text("TOTAL PORTFOLIO VALUE", style: NeonColors.textGlow(Colors.white54).copyWith(fontWeight: FontWeight.bold, fontSize: 10, letterSpacing: 2)),
                const SizedBox(height: 12),
                Text(
                  formatter.format(totalInvested),
                  style: GoogleFonts.notoSansMono(
                    color: NeonColors.pink,
                    fontWeight: FontWeight.w900,
                    fontSize: 32,
                    shadows: NeonColors.textGlow(NeonColors.pink).shadows,
                  ),
                ),
                const Divider(color: Colors.white12, height: 32),
                Text(
                  "총 ${assets.length}개의 종목을 실시간 모니터링 중입니다.",
                  style: const TextStyle(color: Colors.white70, fontWeight: FontWeight.bold, fontSize: 13),
                ),
              ],
            ),
          ),
          const SizedBox(height: 32),
          
          // Risk Heatmap Section
          const Text("RISK HEATMAP (안전 지수)", style: TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 16)),
          const SizedBox(height: 16),
          _buildRiskHeatmap(context, ref, assets),
          
          const SizedBox(height: 32),
          const Text("ASSET STRATEGY LIST", style: TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 16)),
          const SizedBox(height: 16),
          if (assets.isEmpty)
             const Center(child: Text("등록된 종목이 없습니다.", style: TextStyle(color: Colors.white24)))
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
                    final color = pnl >= 0 ? NeonColors.green : NeonColors.pink;
                    return Container(
                      margin: const EdgeInsets.only(bottom: 16),
                      decoration: NeonColors.glassyBorder(color).copyWith(
                        boxShadow: NeonColors.depthShadow(color.withOpacity(0.1)),
                      ),
                      child: ListTile(
                        contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
                        title: Text(a.name, style: NeonColors.textGlow(color).copyWith(fontWeight: FontWeight.w900)),
                        subtitle: Text(
                          "${a.initialQuantity}주 | 평균 ${formatter.format(a.initialPrice)}",
                          style: const TextStyle(color: Colors.white54, fontSize: 12),
                        ),
                        trailing: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          crossAxisAlignment: CrossAxisAlignment.end,
                          children: [
                            Text(formatter.format(value), style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                            Text(
                              "${pnl >= 0 ? '+' : ''}${pnl.toStringAsFixed(2)}%",
                              style: TextStyle(color: color, fontWeight: FontWeight.w900, fontSize: 12),
                            ),
                          ],
                        ),
                      ),
                    );
                  },
                  loading: () => const Center(child: CircularProgressIndicator()),
                  error: (_, __) => const SizedBox.shrink(),
                );
              },
            ),
          const SizedBox(height: 48),
        ],
      ),
    );
  }

  Widget _buildRiskHeatmap(BuildContext context, WidgetRef ref, List<Asset> assets) {
    if (assets.isEmpty) return const SizedBox.shrink();

    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 3,
        crossAxisSpacing: 8,
        mainAxisSpacing: 8,
        childAspectRatio: 1,
      ),
      itemCount: assets.length,
      itemBuilder: (context, index) {
        final a = assets[index];
        final priceAsync = ref.watch(priceProvider(a.symbol));
        
        return priceAsync.when(
           data: (price) {
             final recovery = ((price.price - a.initialPrice) / a.initialPrice * 100);
             final healthColor = recovery > -10 ? NeonColors.green : (recovery > -30 ? NeonColors.cyan : NeonColors.pink);
             
             return Container(
               decoration: BoxDecoration(
                 color: healthColor.withOpacity(0.1),
                 borderRadius: BorderRadius.circular(12),
                 border: Border.all(color: healthColor, width: 2),
                 boxShadow: NeonColors.depthShadow(healthColor),
               ),
               child: Column(
                 mainAxisAlignment: MainAxisAlignment.center,
                 children: [
                   Text(a.symbol, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 10)),
                   const SizedBox(height: 4),
                   Text(
                     "${recovery.toStringAsFixed(0)}%",
                     style: NeonColors.textGlow(healthColor).copyWith(fontSize: 14, fontWeight: FontWeight.w900),
                   ),
                 ],
               ),
             );
           },
           loading: () => Container(color: Colors.white10),
           error: (_, __) => Container(color: Colors.red.withOpacity(0.1)),
        );
      },
    );
  }
}
