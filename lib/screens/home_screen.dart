import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:google_fonts/google_fonts.dart';

import '../widgets/ai_voice_panel.dart';
import '../widgets/celebration_modal.dart';
import '../providers/asset_provider.dart';
import '../providers/currency_provider.dart';
import '../providers/language_provider.dart';
import '../utils/l10n.dart';
import '../models/asset_model.dart';
import 'simulator_screen.dart';
import 'scenario_history_screen.dart';
import 'portfolio_report_screen.dart';
import 'help_screen.dart';
import 'settings_screen.dart';
import '../services/admob_service.dart';
import '../services/event_service.dart';
import '../theme/t_membership_colors.dart';

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
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final assets = ref.watch(assetsProvider);
    final currency = ref.watch(currencyProvider);
    final currencyNotifier = ref.read(currencyProvider.notifier);
    final lang = ref.watch(languageProvider);

    final bgColor = isDark ? TMembershipColors.darkBg : TMembershipColors.lightBg;

    return Scaffold(
      backgroundColor: bgColor,
      appBar: PreferredSize(
        preferredSize: Size.fromHeight(_isAdFree ? 120 : 80),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _buildHeader(context, isDark, lang),
                if (_isAdFree) ...[
                  const SizedBox(height: 8),
                  _buildAdFreeVipBadge(isDark),
                ],
              ],
            ),
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => _showAiPanel(context),
        backgroundColor: TMembershipColors.primaryBlue,
        foregroundColor: Colors.white,
        elevation: 6,
        icon: const Icon(Icons.mic_rounded),
        label: Text(
          "AI 비서",
          style: GoogleFonts.inter(fontWeight: FontWeight.w800, fontSize: 14),
        ),
      ),
      body: LayoutBuilder(
        builder: (context, constraints) {
          final isWide = constraints.maxWidth > 768;
          final padding = isWide ? 40.0 : 20.0;

          if (isWide) {
            return Center(
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 1080),
                child: ListView(
                  padding: EdgeInsets.symmetric(horizontal: padding, vertical: 12),
                  children: [
                    Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Expanded(
                          flex: 6,
                          child: Column(
                            children: [
                              _buildMembershipCard(context, ref, assets, currency, currencyNotifier, lang, isDark)
                                  .animate().fadeIn(duration: 400.ms).slideY(begin: 0.08, end: 0),
                              const SizedBox(height: 20),
                              _buildQuickActions(context, lang, isDark)
                                  .animate().fadeIn(duration: 500.ms, delay: 100.ms).slideY(begin: 0.08, end: 0),
                              const SizedBox(height: 20),
                              _buildSecurityNoticeCard(context, isDark),
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
                              _buildAssetList(context, assets, lang, isDark)
                                  .animate().fadeIn(duration: 600.ms, delay: 200.ms).slideY(begin: 0.08, end: 0),
                            ],
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 48),
                  ],
                ),
              ),
            );
          }

          return ListView(
            padding: EdgeInsets.symmetric(horizontal: padding, vertical: 8),
            children: [
              _buildMembershipCard(context, ref, assets, currency, currencyNotifier, lang, isDark)
                  .animate().fadeIn(duration: 400.ms).slideY(begin: 0.08, end: 0),
              const SizedBox(height: 16),
              if (!_isAdFree) ...[
                const AdmobNativeAdCard(),
                const SizedBox(height: 16),
              ],
              _buildQuickActions(context, lang, isDark)
                  .animate().fadeIn(duration: 500.ms, delay: 100.ms).slideY(begin: 0.08, end: 0),
              const SizedBox(height: 20),
              _buildAssetList(context, assets, lang, isDark)
                  .animate().fadeIn(duration: 600.ms, delay: 200.ms).slideY(begin: 0.08, end: 0),
              const SizedBox(height: 20),
              _buildSecurityNoticeCard(context, isDark),
              const SizedBox(height: 80),
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

  void _showAiPanel(BuildContext context) {
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.transparent,
      isScrollControlled: true,
      builder: (context) => const AiVoicePanel(),
    );
  }

  Widget _buildHeader(BuildContext context, bool isDark, LanguageType lang) {
    final textColor = isDark ? TMembershipColors.darkTextPrimary : TMembershipColors.lightTextPrimary;

    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Row(
          children: [
            Container(
              width: 38,
              height: 38,
              decoration: BoxDecoration(
                gradient: TMembershipColors.primaryGradient,
                borderRadius: BorderRadius.circular(12),
                boxShadow: TMembershipColors.colorfulGlow(TMembershipColors.primaryBlue, opacity: 0.3),
              ),
              child: const Center(
                child: Text(
                  "T",
                  style: TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.w900,
                    fontSize: 22,
                  ),
                ),
              ),
            ),
            const SizedBox(width: 12),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  "물타기 계산기",
                  style: GoogleFonts.inter(
                    color: textColor,
                    fontWeight: FontWeight.w900,
                    fontSize: 20,
                    letterSpacing: -0.5,
                  ),
                ),
                Text(
                  "SMART STRATEGY MANAGER",
                  style: GoogleFonts.inter(
                    color: TMembershipColors.primaryBlue,
                    fontWeight: FontWeight.w800,
                    fontSize: 10,
                    letterSpacing: 1.2,
                  ),
                ),
              ],
            ),
          ],
        ),
        Row(
          children: [
            _buildIconButton(
              icon: Icons.help_outline_rounded,
              isDark: isDark,
              onTap: () => Navigator.push(context, MaterialPageRoute(builder: (context) => HelpScreen())),
            ),
            const SizedBox(width: 8),
            _buildIconButton(
              icon: Icons.settings_outlined,
              isDark: isDark,
              onTap: () => Navigator.push(context, MaterialPageRoute(builder: (context) => SettingsScreen())),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildIconButton({
    required IconData icon,
    required bool isDark,
    required VoidCallback onTap,
  }) {
    final bg = isDark ? TMembershipColors.darkSurface : Colors.white;
    final border = isDark ? TMembershipColors.darkCardBorder : TMembershipColors.lightCardBorder;
    final color = isDark ? Colors.white70 : TMembershipColors.lightTextSecondary;

    return Container(
      decoration: BoxDecoration(
        color: bg,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: border, width: 1),
        boxShadow: isDark ? [] : TMembershipColors.softShadow(blur: 8, dy: 2),
      ),
      child: IconButton(
        icon: Icon(icon, color: color, size: 20),
        onPressed: onTap,
        padding: const EdgeInsets.all(8),
        constraints: const BoxConstraints(minWidth: 40, minHeight: 40),
      ),
    );
  }

  Widget _buildAdFreeVipBadge(bool isDark) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            TMembershipColors.gold.withOpacity(0.18),
            TMembershipColors.accentOrange.withOpacity(0.18),
          ],
        ),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: TMembershipColors.gold.withOpacity(0.6),
          width: 1,
        ),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            children: [
              const Icon(Icons.stars_rounded, color: TMembershipColors.gold, size: 18),
              const SizedBox(width: 8),
              Text(
                '100회 돌파 기념 VIP: 1달 광고 제거 적용 중',
                style: TextStyle(
                  color: isDark ? Colors.white : TMembershipColors.lightTextPrimary,
                  fontWeight: FontWeight.w700,
                  fontSize: 12,
                ),
              ),
            ],
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
            decoration: BoxDecoration(
              gradient: TMembershipColors.vipGoldGradient,
              borderRadius: BorderRadius.circular(8),
            ),
            child: Text(
              'D-$_remainingDays',
              style: const TextStyle(
                color: Colors.white,
                fontWeight: FontWeight.w900,
                fontSize: 11,
              ),
            ),
          ),
        ],
      ),
    ).animate().fadeIn(duration: 400.ms).shimmer(delay: 600.ms, duration: 1500.ms);
  }

  /// SK T-Membership Signature Card Widget
  Widget _buildMembershipCard(
    BuildContext context,
    WidgetRef ref,
    List<Asset> assets,
    CurrencyType currency,
    CurrencyNotifier currencyNotifier,
    LanguageType lang,
    bool isDark,
  ) {
    final totalInvested = assets.fold(0.0, (sum, item) => sum + (item.initialPrice * item.initialQuantity));
    final currentValue = assets.fold(0.0, (sum, item) => sum + (item.initialPrice * item.initialQuantity));
    final pnl = currentValue - totalInvested;
    final pnlPercent = totalInvested > 0 ? (pnl / totalInvested) * 100 : 0.0;

    return Container(
      width: double.infinity,
      decoration: BoxDecoration(
        gradient: TMembershipColors.primaryGradient,
        borderRadius: BorderRadius.circular(28),
        boxShadow: TMembershipColors.colorfulGlow(TMembershipColors.primaryBlue, opacity: 0.35),
      ),
      child: Stack(
        children: [
          // Background decorative circular shapes for depth
          Positioned(
            right: -30,
            top: -30,
            child: Container(
              width: 160,
              height: 160,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: Colors.white.withOpacity(0.08),
              ),
            ),
          ),
          Positioned(
            left: -40,
            bottom: -50,
            child: Container(
              width: 140,
              height: 140,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: Colors.white.withOpacity(0.06),
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Row(
                      children: [
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                          decoration: BoxDecoration(
                            color: Colors.white.withOpacity(0.2),
                            borderRadius: BorderRadius.circular(20),
                            border: Border.all(color: Colors.white.withOpacity(0.3), width: 1),
                          ),
                          child: const Text(
                            "T MEMBERSHIP PORTFOLIO",
                            style: TextStyle(
                              color: Colors.white,
                              fontWeight: FontWeight.w900,
                              fontSize: 10,
                              letterSpacing: 1.2,
                            ),
                          ),
                        ),
                      ],
                    ),
                    InkWell(
                      onTap: currencyNotifier.toggle,
                      borderRadius: BorderRadius.circular(20),
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                        decoration: BoxDecoration(
                          color: Colors.black.withOpacity(0.25),
                          borderRadius: BorderRadius.circular(20),
                          border: Border.all(color: Colors.white.withOpacity(0.25)),
                        ),
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Text(
                              currency == CurrencyType.krw ? 'KRW (\u20a9)' : 'USD (\$)',
                              style: const TextStyle(
                                color: Colors.white,
                                fontWeight: FontWeight.w800,
                                fontSize: 11,
                              ),
                            ),
                            const SizedBox(width: 4),
                            const Icon(Icons.sync_alt_rounded, color: Colors.white70, size: 12),
                          ],
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 20),
                Text(
                  L10n.s(lang, 'total_invested'),
                  style: TextStyle(
                    color: Colors.white.withOpacity(0.85),
                    fontSize: 13,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                const SizedBox(height: 4),
                FittedBox(
                  child: Text(
                    NumberFormat.currency(
                      symbol: currency == CurrencyType.krw ? '\u20a9' : '\$',
                      decimalDigits: 0,
                    ).format(totalInvested),
                    style: GoogleFonts.inter(
                      color: Colors.white,
                      fontSize: 34,
                      fontWeight: FontWeight.w900,
                      letterSpacing: -1,
                    ),
                  ),
                ),
                const SizedBox(height: 20),
                // Bottom stats strip & barcode imitation
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                  decoration: BoxDecoration(
                    color: Colors.black.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            "보유 자산 종목",
                            style: TextStyle(color: Colors.white70, fontSize: 11, fontWeight: FontWeight.w500),
                          ),
                          const SizedBox(height: 2),
                          Text(
                            "${assets.length}개 종목",
                            style: const TextStyle(color: Colors.white, fontSize: 15, fontWeight: FontWeight.w900),
                          ),
                        ],
                      ),
                      Container(height: 24, width: 1, color: Colors.white24),
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            L10n.s(lang, 'pnl'),
                            style: const TextStyle(color: Colors.white70, fontSize: 11, fontWeight: FontWeight.w500),
                          ),
                          const SizedBox(height: 2),
                          Text(
                            "${pnl >= 0 ? '+' : ''}${pnlPercent.toStringAsFixed(1)}%",
                            style: const TextStyle(
                              color: Color(0xFF69F0AE),
                              fontSize: 15,
                              fontWeight: FontWeight.w900,
                            ),
                          ),
                        ],
                      ),
                      Container(height: 24, width: 1, color: Colors.white24),
                      ElevatedButton(
                        onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (context) => const SimulatorScreen())),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.white,
                          foregroundColor: TMembershipColors.primaryBlue,
                          elevation: 0,
                          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                          minimumSize: Size.zero,
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                        ),
                        child: Row(
                          children: const [
                            Text("계산하기", style: TextStyle(fontWeight: FontWeight.w900, fontSize: 12)),
                            SizedBox(width: 4),
                            Icon(Icons.arrow_forward_rounded, size: 14),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  /// T-Membership Style Quick Action Grid
  Widget _buildQuickActions(BuildContext context, LanguageType lang, bool isDark) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(left: 4, bottom: 10),
          child: Text(
            "자주 찾는 기능",
            style: GoogleFonts.inter(
              fontWeight: FontWeight.w800,
              fontSize: 16,
              color: isDark ? TMembershipColors.darkTextPrimary : TMembershipColors.lightTextPrimary,
            ),
          ),
        ),
        Row(
          children: [
            Expanded(
              child: _buildActionTile(
                context: context,
                title: "물타기 시뮬레이터",
                subtitle: "신규 평단가 & 수익 계산",
                icon: Icons.calculate_rounded,
                gradient: TMembershipColors.actionPurpleGradient,
                isDark: isDark,
                onTap: () => Navigator.push(context, MaterialPageRoute(builder: (context) => const SimulatorScreen())),
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: _buildActionTile(
                context: context,
                title: "시나리오 기록",
                subtitle: "과거 계산 내역 비교",
                icon: Icons.history_toggle_off_rounded,
                gradient: TMembershipColors.cardTealBlueGradient,
                isDark: isDark,
                onTap: () => Navigator.push(context, MaterialPageRoute(builder: (context) => const ScenarioHistoryScreen())),
              ),
            ),
          ],
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            Expanded(
              child: _buildActionTile(
                context: context,
                title: "포트폴리오 리포트",
                subtitle: "자산 비중 및 회복력 분석",
                icon: Icons.pie_chart_outline_rounded,
                gradient: TMembershipColors.vipGoldGradient,
                isDark: isDark,
                onTap: () => Navigator.push(context, MaterialPageRoute(builder: (context) => const PortfolioReportScreen())),
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: _buildActionTile(
                context: context,
                title: "음성 비서 입력",
                subtitle: "말 한마디로 자동 계산",
                icon: Icons.graphic_eq_rounded,
                gradient: const LinearGradient(
                  colors: [Color(0xFFFF007F), Color(0xFFFF5252)],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                isDark: isDark,
                onTap: () => _showAiPanel(context),
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildActionTile({
    required BuildContext context,
    required String title,
    required String subtitle,
    required IconData icon,
    required Gradient gradient,
    required bool isDark,
    required VoidCallback onTap,
  }) {
    final cardBg = isDark ? TMembershipColors.darkSurface : TMembershipColors.lightSurface;
    final cardBorder = isDark ? TMembershipColors.darkCardBorder : TMembershipColors.lightCardBorder;
    final titleColor = isDark ? TMembershipColors.darkTextPrimary : TMembershipColors.lightTextPrimary;
    final subColor = isDark ? TMembershipColors.darkTextTertiary : TMembershipColors.lightTextTertiary;

    return Container(
      decoration: BoxDecoration(
        color: cardBg,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: cardBorder, width: 1.2),
        boxShadow: isDark ? [] : TMembershipColors.softShadow(blur: 14, dy: 4),
      ),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: onTap,
          borderRadius: BorderRadius.circular(20),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  width: 42,
                  height: 42,
                  decoration: BoxDecoration(
                    gradient: gradient,
                    borderRadius: BorderRadius.circular(14),
                  ),
                  child: Center(
                    child: Icon(icon, color: Colors.white, size: 22),
                  ),
                ),
                const SizedBox(height: 12),
                Text(
                  title,
                  style: GoogleFonts.inter(
                    fontWeight: FontWeight.w800,
                    fontSize: 14,
                    color: titleColor,
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  subtitle,
                  style: GoogleFonts.inter(
                    fontWeight: FontWeight.w500,
                    fontSize: 11,
                    color: subColor,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  /// T-Membership clean asset list
  Widget _buildAssetList(BuildContext context, List<Asset> assets, LanguageType lang, bool isDark) {
    final cardBg = isDark ? TMembershipColors.darkSurface : TMembershipColors.lightSurface;
    final cardBorder = isDark ? TMembershipColors.darkCardBorder : TMembershipColors.lightCardBorder;
    final titleColor = isDark ? TMembershipColors.darkTextPrimary : TMembershipColors.lightTextPrimary;
    final subColor = isDark ? TMembershipColors.darkTextTertiary : TMembershipColors.lightTextTertiary;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              "내 등록 자산",
              style: GoogleFonts.inter(
                fontWeight: FontWeight.w800,
                fontSize: 16,
                color: titleColor,
              ),
            ),
            if (assets.isNotEmpty)
              Text(
                "총 ${assets.length}개",
                style: TextStyle(color: TMembershipColors.primaryBlue, fontWeight: FontWeight.bold, fontSize: 13),
              ),
          ],
        ),
        const SizedBox(height: 12),
        if (assets.isEmpty)
          Container(
            width: double.infinity,
            padding: const EdgeInsets.symmetric(vertical: 36, horizontal: 20),
            decoration: BoxDecoration(
              color: cardBg,
              borderRadius: BorderRadius.circular(20),
              border: Border.all(color: cardBorder, width: 1.2),
              boxShadow: isDark ? [] : TMembershipColors.softShadow(blur: 10, dy: 3),
            ),
            child: Column(
              children: [
                Icon(Icons.inventory_2_outlined, color: subColor, size: 40),
                const SizedBox(height: 12),
                Text(
                  "등록된 자산이 없습니다",
                  style: TextStyle(color: titleColor, fontWeight: FontWeight.w700, fontSize: 14),
                ),
                const SizedBox(height: 4),
                Text(
                  "시뮬레이터에서 계산 후 자산으로 저장해보세요.",
                  style: TextStyle(color: subColor, fontSize: 12),
                ),
              ],
            ),
          )
        else
          Container(
            decoration: BoxDecoration(
              color: cardBg,
              borderRadius: BorderRadius.circular(20),
              border: Border.all(color: cardBorder, width: 1.2),
              boxShadow: isDark ? [] : TMembershipColors.softShadow(blur: 12, dy: 4),
            ),
            child: ListView.separated(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: assets.take(5).length,
              separatorBuilder: (context, index) => Divider(
                height: 1,
                thickness: 1,
                color: isDark ? TMembershipColors.darkDivider : TMembershipColors.lightDivider,
              ),
              itemBuilder: (context, index) {
                final asset = assets[index];
                return Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 14),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Row(
                        children: [
                          Container(
                            width: 36,
                            height: 36,
                            decoration: BoxDecoration(
                              color: TMembershipColors.primaryBlue.withOpacity(0.1),
                              borderRadius: BorderRadius.circular(10),
                            ),
                            child: const Center(
                              child: Icon(Icons.show_chart_rounded, color: TMembershipColors.primaryBlue, size: 20),
                            ),
                          ),
                          const SizedBox(width: 12),
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                asset.name,
                                style: GoogleFonts.inter(fontWeight: FontWeight.w700, fontSize: 14, color: titleColor),
                              ),
                              Text(
                                "${asset.initialQuantity.toStringAsFixed(0)} 주 / 코인",
                                style: TextStyle(color: subColor, fontSize: 12),
                              ),
                            ],
                          ),
                        ],
                      ),
                      Text(
                        NumberFormat.decimalPattern().format(asset.initialPrice),
                        style: GoogleFonts.notoSansMono(
                          color: titleColor,
                          fontWeight: FontWeight.w800,
                          fontSize: 15,
                        ),
                      ),
                    ],
                  ),
                );
              },
            ),
          ),
      ],
    );
  }

  /// Security Notice Card
  Widget _buildSecurityNoticeCard(BuildContext context, bool isDark) {
    final cardBg = isDark ? TMembershipColors.darkSurface : TMembershipColors.lightSurface;
    final cardBorder = isDark ? TMembershipColors.darkCardBorder : TMembershipColors.lightCardBorder;
    final titleColor = isDark ? TMembershipColors.darkTextPrimary : TMembershipColors.lightTextPrimary;
    final subColor = isDark ? TMembershipColors.darkTextSecondary : TMembershipColors.lightTextSecondary;

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: cardBg,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: cardBorder, width: 1.2),
        boxShadow: isDark ? [] : TMembershipColors.softShadow(blur: 10, dy: 3),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(
              color: TMembershipColors.accentMint.withOpacity(0.12),
              borderRadius: BorderRadius.circular(12),
            ),
            child: const Icon(Icons.shield_outlined, color: TMembershipColors.accentMint, size: 22),
          ),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  "100% 로컬 보안 보장",
                  style: GoogleFonts.inter(fontWeight: FontWeight.w800, fontSize: 13, color: titleColor),
                ),
                const SizedBox(height: 2),
                Text(
                  "외부 서버로 개인 자산 데이터를 절대 전송하지 않습니다.",
                  style: TextStyle(color: subColor, fontSize: 11),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
