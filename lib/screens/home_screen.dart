import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../widgets/ai_voice_panel.dart';
import '../widgets/allocation_chart.dart';
import '../widgets/recovery_gauge.dart';
import '../widgets/celebration_modal.dart';
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
import '../services/event_service.dart';

class HomeScreen extends ConsumerStatefulWidget {
  const HomeScreen({super.key});

  @override
  ConsumerState<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends ConsumerState<HomeScreen> {
  bool _isAdFree = false;
  int _remainingDays = 0;

  @override
  void initState() {
    super.initState();
    _checkAdFreeStatus();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _checkAndShow100EventModal();
    });
  }

  Future<void> _checkAdFreeStatus() async {
    final adFree = await EventService.isAdFreeActive();
    final remaining = await EventService.getRemainingAdFreeDays();
    if (mounted) {
      setState(() {
        _isAdFree = adFree;
        _remainingDays = remaining;
      });
    }
  }

  Future<void> _checkAndShow100EventModal() async {
    final claimed = await EventService.is100DownloadsEventClaimed();
    if (!claimed && mounted) {
      await CelebrationModal.show(
        context,
        onClaimed: () async {
          await _checkAdFreeStatus();
        },
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final assets = ref.watch(assetsProvider);
    final currency = ref.watch(currencyProvider);
    final currencyNotifier = ref.read(currencyProvider.notifier);
    final lang = ref.watch(languageProvider);

    return Scaffold(
      backgroundColor: NeonColors.background,
      appBar: PreferredSize(
        preferredSize: Size.fromHeight(_isAdFree ? 140 : 100),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _buildPureStaticHeader(context, lang),
                if (_isAdFree) ...[
                  const SizedBox(height: 10),
                  _buildAdFreeVipBadge(),
                ],
              ],
            ),
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton.large(
        onPressed: () => _showAiPanel(context),
        backgroundColor: NeonColors.cyan,
        foregroundColor: Colors.black,
        child: const Icon(Icons.mic_rounded, shadows: [Shadow(blurRadius: 10, color: Colors.blueAccent)]),
      ),
      body: LayoutBuilder(
        builder: (context, constraints) {
          final isWideScreen = constraints.maxWidth > 768;
          final contentPadding = isWideScreen ? 48.0 : 24.0;

          if (isWideScreen) {
            return Center(
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 1100),
                child: ListView(
                  padding: EdgeInsets.symmetric(horizontal: contentPadding),
                  children: [
                    const SizedBox(height: 16),
                    Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Expanded(
                          flex: 5,
                          child: Column(
                            children: [
                              _buildPortfolioSummaryBanner(context, ref, assets, currency, currencyNotifier, lang)
                                  .animate().fadeIn(duration: 400.ms).slideY(begin: 0.1, end: 0),
                              const SizedBox(height: 20),
                              _buildPrimaryActionLinear(context, lang)
                                  .animate().fadeIn(duration: 500.ms).slideY(begin: 0.1, end: 0),
                              const SizedBox(height: 20),
                              _buildPrivacyCard(context, lang),
                            ],
                          ),
                        ),
                        const SizedBox(width: 24),
                        Expanded(
                          flex: 5,
                          child: Column(
                            children: [
                              if (!_isAdFree) ...[
                                const AdmobNativeAdCard(),
                                const SizedBox(height: 20),
                              ],
                              _buildHistorySectionLinear(context, lang)
                                  .animate().fadeIn(duration: 600.ms).slideY(begin: 0.1, end: 0),
                              const SizedBox(height: 20),
                              _buildAssetListLinear(context, assets, lang)
                                  .animate().fadeIn(duration: 700.ms).slideY(begin: 0.1, end: 0),
                            ],
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 60),
                  ],
                ),
              ),
            );
          }

          return ListView(
            padding: EdgeInsets.symmetric(horizontal: contentPadding),
            children: [
              const SizedBox(height: 16),
              _buildPortfolioSummaryBanner(context, ref, assets, currency, currencyNotifier, lang)
                  .animate().fadeIn(duration: 400.ms).slideY(begin: 0.2, end: 0),
              const SizedBox(height: 20),
              if (!_isAdFree) ...[
                const AdmobNativeAdCard(),
                const SizedBox(height: 20),
              ],
              _buildPrimaryActionLinear(context, lang)
                  .animate().fadeIn(duration: 600.ms, delay: 100.ms).slideY(begin: 0.2, end: 0),
              const SizedBox(height: 24),
              _buildHistorySectionLinear(context, lang)
                  .animate().fadeIn(duration: 800.ms, delay: 200.ms).slideY(begin: 0.2, end: 0),
              const SizedBox(height: 24),
              _buildAssetListLinear(context, assets, lang)
                  .animate().fadeIn(duration: 1000.ms, delay: 300.ms).slideY(begin: 0.2, end: 0),
              const SizedBox(height: 60),
            ],
          );
        },
      ),
      bottomNavigationBar: _isAdFree
          ? null
          : const SafeArea(
              child: SizedBox(
                height: 50,
                child: AdmobBannerWidget(),
              ),
            ),
    );
  }

  Widget _buildAdFreeVipBadge() {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            NeonColors.cyan.withOpacity(0.2),
            Colors.purpleAccent.withOpacity(0.2),
          ],
        ),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: NeonColors.cyan.withOpacity(0.5),
          width: 1,
        ),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            children: [
              const Icon(Icons.bolt_rounded, color: NeonColors.cyan, size: 18),
              const SizedBox(width: 6),
              const Text(
                '100회 다운로드 기념: 1달 광고 제거 적용 중',
                style: TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                  fontSize: 12,
                ),
              ),
            ],
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
            decoration: BoxDecoration(
              color: NeonColors.cyan,
              borderRadius: BorderRadius.circular(8),
            ),
            child: Text(
              'D-$_remainingDays',
              style: const TextStyle(
                color: Colors.black,
                fontWeight: FontWeight.w900,
                fontSize: 11,
              ),
            ),
          ),
        ],
      ),
    ).animate().fadeIn(duration: 500.ms).shimmer(delay: 800.ms, duration: 1500.ms);
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
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              "물타기 계산기",
              style: GoogleFonts.inter(
                color: Colors.white,
                fontWeight: FontWeight.w900,
                fontSize: 32,
                letterSpacing: -1,
              ),
            ),
            const SizedBox(height: 2),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
              decoration: const BoxDecoration(color: NeonColors.cyan),
              child: const Text(
                "STRATEGY MANAGER",
                style: TextStyle(color: Colors.black, fontWeight: FontWeight.w900, fontSize: 9, letterSpacing: 2),
              ),
            ),
          ],
        ),
        Row(
          children: [
            IconButton(
              icon: const Icon(Icons.help_outline_rounded, color: Colors.white54, size: 26),
              onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (context) => HelpScreen())),
            ),
            IconButton(
              icon: const Icon(Icons.settings_outlined, color: Colors.white54, size: 26),
              onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (context) => SettingsScreen())),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildPortfolioSummaryBanner(
    BuildContext context,
    WidgetRef ref,
    List<Asset> assets,
    CurrencyType currency,
    CurrencyNotifier currencyNotifier,
    LanguageType lang,
  ) {
    final totalInvested = assets.fold(0.0, (sum, item) => sum + (item.initialPrice * item.initialQuantity));
    final currentValue = assets.fold(0.0, (sum, item) => sum + (item.initialPrice * item.initialQuantity));
    final pnl = currentValue - totalInvested;
    final pnlColor = pnl >= 0 ? NeonColors.green : Colors.redAccent;
    final pnlPercent = totalInvested > 0 ? (pnl / totalInvested) * 100 : 0.0;

    return Container(
      padding: const EdgeInsets.all(24),
      decoration: NeonColors.glassyBorder(NeonColors.cyan),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(L10n.s(lang, 'total_invested'), style: const TextStyle(color: Colors.white54, fontSize: 13, fontWeight: FontWeight.bold)),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: Colors.white10,
                  borderRadius: BorderRadius.circular(8),
                ),
                child: InkWell(
                  onTap: currencyNotifier.toggle,
                  child: Text(
                    currency == CurrencyType.krw ? 'KRW (\u20a9)' : 'USD (\$)',
                    style: const TextStyle(color: NeonColors.cyan, fontWeight: FontWeight.bold, fontSize: 11),
                  ),
                ),
              ),
            ],
          ),
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
        padding: const EdgeInsets.all(28),
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
            const Icon(Icons.arrow_forward_ios_rounded, color: Colors.black, size: 26),
          ],
        ),
      ),
    );
  }

  Widget _buildHistorySectionLinear(BuildContext context, LanguageType lang) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(L10n.s(lang, 'label_history').toUpperCase(), style: const TextStyle(color: Colors.white30, fontWeight: FontWeight.w900, fontSize: 13, letterSpacing: 1)),
        const SizedBox(height: 12),
        _buildActionCard(
          context,
          "최근 계산 내역 확인",
          Icons.history_rounded,
          Colors.white.withOpacity(0.08),
          () => Navigator.push(context, MaterialPageRoute(builder: (context) => const ScenarioHistoryScreen())),
        ),
        const SizedBox(height: 8),
        _buildActionCard(
          context,
          L10n.s(lang, 'label_portfolio'),
          Icons.pie_chart_rounded,
          NeonColors.cyan,
          () => Navigator.push(context, MaterialPageRoute(builder: (context) => const PortfolioReportScreen())),
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
        if (assets.isEmpty)
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.02),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: Colors.white10),
            ),
            child: const Text(
              "등록된 자산이 없습니다. 시뮬레이터에서 새로운 주식/코인을 계산하고 저장해보세요.",
              style: TextStyle(color: Colors.white38, fontSize: 12),
            ),
          )
        else
          ...assets.take(4).map((asset) => Padding(
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

  Widget _buildPrivacyCard(BuildContext context, LanguageType lang) {
    return Container(
      padding: const EdgeInsets.all(24),
      width: double.infinity,
      decoration: NeonColors.borderGlow(NeonColors.cyan).copyWith(color: NeonColors.surface),
      child: Column(
        children: const [
          Icon(Icons.security_rounded, color: NeonColors.cyan, size: 32),
          SizedBox(height: 12),
          Text(
            "Privacy & Security Guaranteed",
            style: TextStyle(fontWeight: FontWeight.w900, fontSize: 16, color: Colors.white, letterSpacing: -0.5),
          ),
          SizedBox(height: 8),
          Text(
            "모든 자산 및 계산 내역은 서버 전송 없이 100% 로컬 기기에 암호화 저장됩니다.",
            textAlign: TextAlign.center,
            style: TextStyle(color: Colors.white54, fontSize: 13, height: 1.4),
          ),
        ],
      ),
    );
  }

  Widget _buildActionCard(BuildContext context, String title, IconData icon, Color color, VoidCallback onTap) {
    return Container(
      decoration: NeonColors.borderGlow(color).copyWith(color: NeonColors.surface),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(20),
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
          child: Row(
            children: [
              Container(
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: color.withOpacity(0.12),
                  borderRadius: BorderRadius.circular(14),
                  border: Border.all(color: color, width: 1),
                ),
                child: Icon(icon, color: color, size: 24),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Text(
                  title,
                  style: TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                    fontSize: 15,
                  ),
                ),
              ),
              const Icon(Icons.arrow_forward_ios_rounded, size: 14, color: Colors.white38),
            ],
          ),
        ),
      ),
    );
  }
}
