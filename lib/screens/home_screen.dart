import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../widgets/ai_voice_panel.dart';
import '../widgets/allocation_chart.dart';
import '../widgets/recovery_gauge.dart';
import '../providers/asset_provider.dart';
import '../providers/currency_provider.dart';
import '../providers/market_provider.dart';
import '../providers/language_provider.dart';
import '../utils/l10n.dart';
import '../models/asset_model.dart';
import '../models/scenario_model.dart';
import 'simulator_screen.dart';
import 'target_price_screen.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../theme/neon_colors.dart';
import 'scenario_history_screen.dart';
import 'portfolio_report_screen.dart';
import 'help_screen.dart';
import 'settings_screen.dart';
import 'package:google_fonts/google_fonts.dart';
import '../services/unity_ad_service.dart';
import '../services/admob_service.dart';

class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final assets = ref.watch(assetsProvider);
    final currency = ref.watch(currencyProvider);
    final currencyNotifier = ref.read(currencyProvider.notifier);
    final lang = ref.watch(languageProvider);
    final langNotifier = ref.read(languageProvider.notifier);

    return Scaffold(
      backgroundColor: NeonColors.background,
      appBar: PreferredSize(
        preferredSize: const Size.fromHeight(100),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
            child: _buildPureStaticHeader(context, lang),
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton.large(
        onPressed: () => _showAiPanel(context),
        backgroundColor: NeonColors.cyan,
        foregroundColor: Colors.black,
        child: const Icon(Icons.mic_rounded, shadows: [Shadow(blurRadius: 10, color: Colors.blueAccent)]),
      ),
      body: ListView(
        padding: const EdgeInsets.symmetric(horizontal: 32),
        children: [
          const SizedBox(height: 16),
          _buildPortfolioSummaryBanner(context, ref, assets, currency, currencyNotifier, lang)
            .animate().fadeIn(duration: 400.ms).slideY(begin: 0.2, end: 0),
          const SizedBox(height: 24),
          const AdmobNativeAdCard(),
          const SizedBox(height: 24),
          _buildPrimaryActionLinear(context, lang)
            .animate().fadeIn(duration: 600.ms, delay: 100.ms).slideY(begin: 0.2, end: 0),
          const SizedBox(height: 32),
          _buildHistorySectionLinear(context, lang)
            .animate().fadeIn(duration: 800.ms, delay: 200.ms).slideY(begin: 0.2, end: 0),
          const SizedBox(height: 32),
          _buildAssetListLinear(context, assets, lang)
            .animate().fadeIn(duration: 1000.ms, delay: 300.ms).slideY(begin: 0.2, end: 0),
          const SizedBox(height: 60),
        ],
      ),
      bottomNavigationBar: const SafeArea(
        child: SizedBox(
          height: 50,
          child: AdmobBannerWidget(),
        ),
      ),
    );
  }

  Widget _buildMainActions(BuildContext context, List<Asset> assets, LanguageType lang) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(L10n.s(lang, 'quick_actions'), style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 16)),
        const SizedBox(height: 16),
        _buildActionCard(
          context,
          L10n.s(lang, 'label_sim'),
          Icons.calculate_rounded,
          NeonColors.cyan,
          () => Navigator.push(context, MaterialPageRoute(builder: (context) => const SimulatorScreen())),
        ),
        const SizedBox(height: 12),
        _buildActionCard(
          context,
          L10n.s(lang, 'label_history'),
          Icons.history_rounded,
          Colors.blue.withOpacity(0.1),
          () async {
            final s = await Navigator.push<Scenario>(
              context,
              MaterialPageRoute(builder: (context) => const ScenarioHistoryScreen()),
            );
            if (s != null && context.mounted) {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => SimulatorScreen(initialScenario: s)),
              );
            }
          },
        ),
        const SizedBox(height: 12),
        _buildActionCard(
          context,
          L10n.s(lang, 'label_portfolio'),
          Icons.pie_chart_rounded,
          NeonColors.green,
          () => Navigator.push(context, MaterialPageRoute(builder: (context) => const PortfolioReportScreen())),
        ),
        if (assets.isNotEmpty) ...[
          const SizedBox(height: 32),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(L10n.s(lang, 'my_assets'), style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 16)),
              TextButton(onPressed: () {}, child: Text(L10n.s(lang, 'view_all'))),
            ],
          ),
          const SizedBox(height: 12),
          ...assets.map((asset) => Consumer(builder: (context, ref, _) => _buildLiveAssetCard(context, ref, asset, lang))),
        ],
      ],
    );
  }

  Widget _buildPrivacyCard(BuildContext context, LanguageType lang) {
    return Container(
      padding: const EdgeInsets.all(24),
      width: double.infinity,
      decoration: NeonColors.borderGlow(NeonColors.pink).copyWith(color: NeonColors.surface),
      child: Column(
        children: [
          const Icon(Icons.security_rounded, color: NeonColors.pink, size: 32),
          const SizedBox(height: 12),
          const Text(
            "Privacy & Security",
            style: TextStyle(fontWeight: FontWeight.w900, fontSize: 18, color: Colors.white, letterSpacing: -0.5),
          ),
          const SizedBox(height: 12),
          const Text(
            "모든 데이터는 서버가 아닌 사용자 기기에만 로컬 저장됩니다.\n개인정보 유출 걱정 없이 안전하게 시뮬레이션하세요.",
            textAlign: TextAlign.center,
            maxLines: 2,
            overflow: TextOverflow.visible,
            style: TextStyle(color: Colors.white54, fontSize: 14, fontWeight: FontWeight.w400, height: 1.4),
          ),
        ],
      ),
    );
  }

  void _showAiPanel(BuildContext context) {
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.transparent,
      isScrollControlled: true,
      builder: (context) => const AiVoicePanel(),
    );
  }

  Widget _buildPureStaticHeader(BuildContext context, LanguageType lang) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              "물타기 계산기",
              style: GoogleFonts.inter(
                color: Colors.white,
                fontWeight: FontWeight.w900,
                fontSize: 36,
                letterSpacing: -1,
              ),
            ),
            Row(
              children: [
                IconButton(
                  icon: const Icon(Icons.help_outline_rounded, color: Colors.white30, size: 28),
                  onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (context) => HelpScreen())),
                ),
                IconButton(
                  icon: const Icon(Icons.settings_outlined, color: Colors.white30, size: 28),
                  onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (context) => SettingsScreen())),
                ),
              ],
            ),
          ],
        ),
        const SizedBox(height: 8),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
          decoration: const BoxDecoration(color: NeonColors.cyan),
          child: const Text(
            "STRATEGY MANAGER",
            style: TextStyle(color: Colors.black, fontWeight: FontWeight.w900, fontSize: 10, letterSpacing: 2),
          ),
        ),
      ],
    );
  }

  Widget _buildPureHeader(BuildContext context, bool isWide, LanguageType lang) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(vertical: 20, horizontal: 24),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            L10n.s(lang, 'app_title'),
            style: GoogleFonts.inter(
              color: Colors.white,
              fontWeight: FontWeight.w900,
              fontSize: 28,
            ),
          ),
          Row(
            children: [
              IconButton(
                icon: const Icon(Icons.help_outline_rounded, color: Colors.white54),
                onPressed: () {},
              ),
              IconButton(
                icon: const Icon(Icons.settings_outlined, color: Colors.white54),
                onPressed: () {},
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildPortfolioSummaryBanner(BuildContext context, WidgetRef ref, List<Asset> assets, CurrencyType currency, CurrencyNotifier currencyNotifier, LanguageType lang) {
    final totalInvested = assets.fold(0.0, (sum, item) => sum + (item.initialPrice * item.initialQuantity));
    final currentValue = assets.fold(0.0, (sum, item) => sum + (item.initialPrice * item.initialQuantity));
    final pnl = currentValue - totalInvested;
    final pnlColor = pnl >= 0 ? NeonColors.green : Colors.redAccent;
    final pnlPercent = totalInvested > 0 ? (pnl / totalInvested) * 100 : 0.0;

    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(24),
      decoration: NeonColors.glassyBorder(NeonColors.cyan),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(L10n.s(lang, 'total_invested'), style: const TextStyle(color: Colors.white54, fontSize: 13, fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          Text(
            NumberFormat.currency(symbol: currency == CurrencyType.krw ? '\u20a9' : '\$', decimalDigits: 0).format(totalInvested),
            style: GoogleFonts.notoSansMono(color: Colors.white, fontSize: 32, fontWeight: FontWeight.w900),
          ),
          const SizedBox(height: 16),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(L10n.s(lang, 'pnl'), style: const TextStyle(color: Colors.white38, fontSize: 11)),
                  Text(
                    "${pnl >= 0 ? '+' : ''}${NumberFormat.currency(symbol: currency == CurrencyType.krw ? '\u20a9' : '\$', decimalDigits: 0).format(pnl)}",
                    style: TextStyle(color: pnlColor, fontSize: 16, fontWeight: FontWeight.w900),
                  ),
                ],
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                decoration: BoxDecoration(color: pnlColor.withOpacity(0.1), borderRadius: BorderRadius.circular(8), border: Border.all(color: pnlColor, width: 1.5)),
                child: Text(
                  "${pnl >= 0 ? '+' : ''}${pnlPercent.toStringAsFixed(2)}%",
                  style: TextStyle(color: pnlColor, fontWeight: FontWeight.w900, fontSize: 13),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildPrimaryActionLinear(BuildContext context, LanguageType lang) {
    return InkWell(
      onTap: () => Navigator.push(context, MaterialPageRoute(builder: (context) => const SimulatorScreen())),
      child: Container(
        width: double.infinity,
        padding: const EdgeInsets.all(32),
        decoration: NeonColors.borderGlow(NeonColors.pink).copyWith(
          color: NeonColors.pink,
          boxShadow: NeonColors.depthShadow(NeonColors.pink.withOpacity(0.3)),
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(L10n.s(lang, 'label_sim').toUpperCase(), style: const TextStyle(color: Colors.black, fontWeight: FontWeight.w900, fontSize: 20)),
                const SizedBox(height: 4),
                const Text("예상 수익 및 신규 평단가 시뮬레이션", style: TextStyle(color: Colors.black54, fontSize: 12, fontWeight: FontWeight.bold)),
              ],
            ),
            const Icon(Icons.arrow_forward_ios_rounded, color: Colors.black, size: 28),
          ],
        ),
      ),
    );
  }

  Widget _buildHistorySectionLinear(BuildContext context, LanguageType lang) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 0),
          child: Text(L10n.s(lang, 'label_history').toUpperCase(), style: const TextStyle(color: Colors.white30, fontWeight: FontWeight.w900, fontSize: 13, letterSpacing: 1)),
        ),
        const SizedBox(height: 12),
        _buildActionCard(
          context,
          "최근 계산 내역 확인",
          Icons.history_rounded,
          Colors.white.withOpacity(0.05),
          () => Navigator.push(context, MaterialPageRoute(builder: (context) => const ScenarioHistoryScreen())),
        ),
      ],
    );
  }

  Widget _buildAssetListLinear(BuildContext context, List<Asset> assets, LanguageType lang) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(L10n.s(lang, 'my_assets').toUpperCase(), style: const TextStyle(color: Colors.white30, fontWeight: FontWeight.w900, fontSize: 13, letterSpacing: 1)),
        const SizedBox(height: 12),
        ...assets.take(3).map((asset) => Padding(
          padding: const EdgeInsets.only(bottom: 8.0),
          child: Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(color: Colors.white.withOpacity(0.03), border: Border.all(color: Colors.white12, width: 1), borderRadius: BorderRadius.circular(12)),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(asset.name, style: const TextStyle(color: Colors.white70, fontWeight: FontWeight.bold)),
                Text(NumberFormat.decimalPattern().format(asset.initialPrice), style: GoogleFonts.notoSansMono(color: Colors.white)),
              ],
            ),
          ),
        )).toList(),
      ],
    );
  }

  Widget _buildPortfolioSummary(BuildContext context, WidgetRef ref, List<Asset> assets, CurrencyType currency, CurrencyNotifier notifier, LanguageType lang) {
    final theme = Theme.of(context);
    double totalInvested = 0;
    double currentValue = 0;

    for (var asset in assets) {
      totalInvested += asset.initialPrice * asset.initialQuantity;
      final priceAsync = ref.watch(priceProvider(asset.symbol));
      priceAsync.whenData((price) {
        currentValue += price.price * asset.initialQuantity;
      });
    }

    final pnl = currentValue > 0 ? currentValue - totalInvested : 0.0;
    final pnlPercentage = totalInvested > 0 ? (pnl / totalInvested) * 100 : 0.0;

    final formatter = NumberFormat.currency(
      symbol: currency == CurrencyType.krw ? '\u20a9' : '\$',
      decimalDigits: currency == CurrencyType.krw ? 0 : 2,
    );

    return Container(
      decoration: NeonColors.borderGlow(NeonColors.cyan),
      padding: const EdgeInsets.all(24.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(L10n.s(lang, 'my_portfolio'), style: theme.textTheme.titleMedium?.copyWith(color: Colors.white70, fontWeight: FontWeight.w900)),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                decoration: BoxDecoration(
                  color: Colors.white10,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: InkWell(
                  onTap: notifier.toggle,
                  child: Text(
                    currency == CurrencyType.krw ? 'KRW' : 'USD',
                    style: const TextStyle(color: NeonColors.cyan, fontWeight: FontWeight.w900, fontSize: 12),
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Text(
            formatter.format(currentValue > 0 ? currentValue : totalInvested),
            style: GoogleFonts.notoSansMono(fontWeight: FontWeight.w900, color: NeonColors.cyan, fontSize: 42, shadows: NeonColors.textGlow(NeonColors.cyan).shadows),
          ),
          const SizedBox(height: 24),
          Row(
            children: [
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.05),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.white24, width: 1),
                ),
                child: Row(
                  children: [
                    Icon(
                      pnl >= 0 ? Icons.trending_up_rounded : Icons.trending_down_rounded,
                      size: 16,
                      color: pnl >= 0 ? Colors.redAccent : Colors.blueAccent,
                    ),
                    const SizedBox(width: 8),
                    Text(
                      '${pnl >= 0 ? '+' : ''}${formatter.format(pnl)} (${pnlPercentage.toStringAsFixed(2)}%)',
                      style: theme.textTheme.labelMedium?.copyWith(
                        color: pnl >= 0 ? Colors.redAccent : Colors.blueAccent,
                        fontWeight: FontWeight.w900,
                      ),
                    ),
                  ],
                ),
              ),
              const Spacer(),
              Text(
                '${formatter.format(totalInvested)}',
                style: theme.textTheme.bodySmall?.copyWith(color: Colors.white30, fontWeight: FontWeight.w900, fontSize: 16),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildHealthCard(BuildContext context, List<Asset> assets, WidgetRef ref, LanguageType lang) {
    if (assets.isEmpty) return const SizedBox.shrink();
    
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    double totalRecovery = 0;
    int count = 0;

    for (var asset in assets) {
      final priceAsync = ref.watch(priceProvider(asset.symbol));
      priceAsync.whenData((price) {
        final avg = asset.initialPrice;
        if (avg > 0) {
          final rec = ((price.price - avg) / avg * 100).clamp(-100.0, 100.0);
          totalRecovery += rec;
          count++;
        }
      });
    }

    final healthScore = count > 0 ? (totalRecovery / count + 100) / 2 : 100.0;
    final healthColor = healthScore > 70 ? Colors.green : (healthScore > 40 ? Colors.orange : Colors.red);

    return Container(
      decoration: NeonColors.borderGlow(healthColor).copyWith(color: NeonColors.surface),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Row(
          children: [
            SizedBox(
              height: 70,
              width: 70,
              child: RecoveryGauge(
                percentage: healthScore,
                color: healthColor,
              ),
            ),
            const SizedBox(width: 20),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    healthScore > 70 ? '포트폴리오 안정' : (healthScore > 40 ? '관리 필요' : '위험 수준'),
                    style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w900, color: healthColor),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    healthScore > 70 
                      ? '수익 실현 또는 보유' 
                      : '평단가 낮추기(물타기)를 고려하세요.',
                    style: theme.textTheme.bodySmall?.copyWith(fontWeight: FontWeight.w800),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildLiveAssetCard(BuildContext context, WidgetRef ref, dynamic asset, LanguageType lang) {
    final theme = Theme.of(context);
    final priceAsync = ref.watch(priceProvider(asset.symbol));
    final currency = ref.watch(currencyProvider);
    final formatter = NumberFormat.currency(
      symbol: currency == CurrencyType.krw ? '\u20a9' : '\$',
      decimalDigits: currency == CurrencyType.krw ? 0 : 2,
    );

    return Dismissible(
      key: Key(asset.id.toString()),
      direction: DismissDirection.endToStart,
      background: Container(
        alignment: Alignment.centerRight,
        padding: const EdgeInsets.only(right: 20),
        decoration: BoxDecoration(
          color: Colors.red.withOpacity(0.1),
          borderRadius: BorderRadius.circular(26),
        ),
        child: const Icon(Icons.delete_outline_rounded, color: Colors.red),
      ),
      onDismissed: (_) {
        ref.read(assetsProvider.notifier).removeAsset(asset.id!);
      },
      child: Container(
        margin: const EdgeInsets.only(bottom: 12),
        decoration: NeonColors.borderGlow(NeonColors.cyan).copyWith(color: NeonColors.surface),
        child: ListTile(
          contentPadding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
          title: Row(
            children: [
              Text(asset.name, style: NeonColors.textGlow(NeonColors.cyan).copyWith(fontWeight: FontWeight.w900)),
              const SizedBox(width: 8),
              if (asset.symbol.isNotEmpty)
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                  decoration: BoxDecoration(
                    color: Colors.white10,
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: Text(asset.symbol, style: const TextStyle(color: Colors.white70, fontSize: 10)),
                ),
            ],
          ),
          subtitle: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 4),
              Text('${L10n.s(lang, 'avg_price')}: ${formatter.format(asset.initialPrice)} | ${L10n.s(lang, 'quantity')}: ${asset.initialQuantity}', style: const TextStyle(color: Colors.white54, fontSize: 12)),
              const SizedBox(height: 4),
              priceAsync.when(
                data: (price) => Row(
                  children: [
                    Text('${L10n.s(lang, 'price')}: ${formatter.format(price.price)}', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                    const SizedBox(width: 8),
                    Text(
                      '${price.changePercentage > 0 ? '+' : ''}${price.changePercentage.toStringAsFixed(2)}%',
                      style: TextStyle(
                        color: price.changePercentage > 0 ? NeonColors.green : NeonColors.pink,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
                loading: () => const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(strokeWidth: 2)),
                error: (_, __) => const Text('Price Unavailable', style: TextStyle(color: Colors.white24)),
              ),
            ],
          ),
          trailing: const Icon(Icons.chevron_right_rounded, color: Colors.white54),
        ),
      ),
    );
  }

  Widget _buildActionCard(BuildContext context, String title, IconData icon, Color color, VoidCallback onTap) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      decoration: NeonColors.borderGlow(color).copyWith(color: NeonColors.surface),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(24),
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Row(
            children: [
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: color.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: color, width: 1.5),
                  boxShadow: NeonColors.depthShadow(color),
                ),
                child: Icon(icon, color: color, size: 28),
              ),
              const SizedBox(width: 20),
              Expanded(
                child: Text(
                  title,
                  style: NeonColors.textGlow(color).copyWith(
                    fontWeight: FontWeight.w900, 
                    fontSize: 18,
                    height: 1.1,
                  ),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
              ),
              const Icon(Icons.arrow_forward_ios_rounded, size: 16, color: Colors.white54),
            ],
          ),
        ),
      ),
    );
  }
}
