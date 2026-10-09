import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
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
import 'target_price_screen.dart';
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
      AdmobService.showAppOpenAd();
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
        preferredSize: const Size.fromHeight(68),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: _buildHeader(context, isDark, lang),
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => _showAiPanel(context),
        backgroundColor: TMembershipColors.primaryBlue,
        foregroundColor: Colors.white,
        elevation: 6,
        icon: const Icon(Icons.mic_rounded, size: 22),
        label: Text(
          L10n.s(lang, 'ai_assistant_btn'),
          style: GoogleFonts.inter(fontWeight: FontWeight.w800, fontSize: 14),
        ),
      ),
      body: LayoutBuilder(
        builder: (context, constraints) {
          final isWide = constraints.maxWidth > 768;
          final padding = isWide ? 32.0 : 16.0;

          return Center(
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 860),
              child: ListView(
                padding: EdgeInsets.symmetric(horizontal: padding, vertical: 12),
                children: [
                  // 1. VIP 혜택 적용 상태 배너 (활성화 시 상단 알림)
                  if (_isAdFree) ...[
                    _buildAdFreeVipBadge(isDark, lang),
                    const SizedBox(height: 14),
                  ],

                  // 2. 스마트 포트폴리오 메인 카드
                  _buildMembershipCard(context, ref, assets, currency, currencyNotifier, lang, isDark)
                      .animate().fadeIn(duration: 400.ms).slideY(begin: 0.06, end: 0),
                  const SizedBox(height: 14),

                  // 3. 광고보고 VIP 24시간 광고제거 한줄 배너 (요청사항: 따로 한줄 배너)
                  _buildWatchAdVipOneLineBanner(context, lang, isDark)
                      .animate().fadeIn(duration: 450.ms, delay: 50.ms).slideY(begin: 0.06, end: 0),
                  const SizedBox(height: 16),

                  // 4. 물타기 시뮬레이터 긴 1줄 히어로 버튼 (요청사항: 길게 1줄로 빼기)
                  _buildSimulatorHeroButton(context, lang, isDark)
                      .animate().fadeIn(duration: 500.ms, delay: 100.ms).slideY(begin: 0.06, end: 0),
                  const SizedBox(height: 20),

                  // 5. 짝수(2x2=4개) 퀵 액션 그리드 (요청사항: 하단 버튼 그리드를 짝수로 맞춰줘)
                  _buildQuickActions(context, lang, isDark)
                      .animate().fadeIn(duration: 550.ms, delay: 150.ms).slideY(begin: 0.06, end: 0),
                  const SizedBox(height: 20),

                  // 6. 네이티브 광고 카드 (광고제거 아닐 때)
                  if (!_isAdFree) ...[
                    const AdmobNativeAdCard(),
                    const SizedBox(height: 20),
                  ],

                  // 7. 내 등록 자산 리스트
                  _buildAssetList(context, assets, currency, lang, isDark)
                      .animate().fadeIn(duration: 600.ms, delay: 200.ms).slideY(begin: 0.06, end: 0),
                  const SizedBox(height: 20),

                  // 8. 100% 로컬 보안 보장 카드
                  _buildSecurityNoticeCard(context, isDark, lang),
                  const SizedBox(height: 80),
                ],
              ),
            ),
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
        Expanded(
          child: Row(
            children: [
              Container(
                width: 42,
                height: 42,
                alignment: Alignment.center,
                child: Image.asset(
                  'assets/app_icon.png',
                  fit: BoxFit.contain,
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    L10n.s(lang, 'app_title'),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: GoogleFonts.inter(
                      color: textColor,
                      fontWeight: FontWeight.w900,
                      fontSize: 18,
                      letterSpacing: -0.4,
                    ),
                  ),
                  const SizedBox(height: 3),
                  Text(
                    L10n.s(lang, 'app_subtitle'),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(
                      color: TMembershipColors.primaryBlue,
                      fontWeight: FontWeight.w800,
                      fontSize: 11,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
        ),
        const SizedBox(width: 12),
        Row(
          mainAxisSize: MainAxisSize.min,
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
    String? tooltip,
  }) {
    final bg = isDark ? TMembershipColors.darkSurface : Colors.white;
    final border = isDark ? TMembershipColors.darkCardBorder : TMembershipColors.lightCardBorder;
    final color = isDark ? Colors.white : TMembershipColors.lightTextPrimary;

    return Tooltip(
      message: tooltip ?? '',
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: onTap,
          borderRadius: BorderRadius.circular(12),
          child: Container(
            width: 42,
            height: 42,
            decoration: BoxDecoration(
              color: bg,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: border, width: 1.2),
              boxShadow: isDark ? [] : TMembershipColors.softShadow(blur: 8, dy: 2),
            ),
            child: Center(
              child: Icon(icon, color: color, size: 21),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildAdFreeVipBadge(bool isDark, LanguageType lang) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            TMembershipColors.gold.withOpacity(0.16),
            TMembershipColors.accentOrange.withOpacity(0.16),
          ],
        ),
        borderRadius: BorderRadius.circular(14),
        border: Border.all(
          color: TMembershipColors.gold.withOpacity(0.55),
          width: 1.2,
        ),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(4),
            decoration: BoxDecoration(
              color: TMembershipColors.gold.withOpacity(0.2),
              shape: BoxShape.circle,
            ),
            child: const Icon(Icons.stars_rounded, color: TMembershipColors.gold, size: 18),
          ),
          const SizedBox(width: 8),
          Expanded(
            child: FittedBox(
              fit: BoxFit.scaleDown,
              alignment: Alignment.centerLeft,
              child: Text(
                lang == LanguageType.ko ? 'VIP 혜택: 1달 광고 제거 적용 중' : 'VIP Benefit: Ad-Free Active',
                style: TextStyle(
                  color: isDark ? Colors.white : TMembershipColors.lightTextPrimary,
                  fontWeight: FontWeight.w800,
                  fontSize: 12,
                ),
              ),
            ),
          ),
          const SizedBox(width: 8),
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

  /// 스마트 포트폴리오 메인 카드
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
                    Flexible(
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                        decoration: BoxDecoration(
                          color: Colors.white.withOpacity(0.2),
                          borderRadius: BorderRadius.circular(20),
                          border: Border.all(color: Colors.white.withOpacity(0.3), width: 1),
                        ),
                        child: FittedBox(
                          fit: BoxFit.scaleDown,
                          child: Text(
                            L10n.s(lang, 'smart_portfolio').toUpperCase(),
                            style: const TextStyle(
                              color: Colors.white,
                              fontWeight: FontWeight.w900,
                              fontSize: 10,
                              letterSpacing: 1.0,
                            ),
                          ),
                        ),
                      ),
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
                              currency.label,
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
                  fit: BoxFit.scaleDown,
                  alignment: Alignment.centerLeft,
                  child: Text(
                    NumberFormat.currency(
                      symbol: currency.symbol,
                      decimalDigits: currency.decimalDigits,
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
                // Bottom stats strip
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                  decoration: BoxDecoration(
                    color: Colors.black.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: FittedBox(
                    fit: BoxFit.scaleDown,
                    alignment: Alignment.centerLeft,
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              L10n.s(lang, 'my_assets'),
                              style: const TextStyle(color: Colors.white70, fontSize: 11, fontWeight: FontWeight.w500),
                            ),
                            const SizedBox(height: 6),
                            Text(
                              "${assets.length} ${L10n.s(lang, 'asset_count_suffix')}",
                              style: const TextStyle(color: Colors.white, fontSize: 15, fontWeight: FontWeight.w900),
                            ),
                          ],
                        ),
                        const SizedBox(width: 18),
                        Container(height: 26, width: 1, color: Colors.white24),
                        const SizedBox(width: 18),
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              L10n.s(lang, 'pnl'),
                              style: const TextStyle(color: Colors.white70, fontSize: 11, fontWeight: FontWeight.w500),
                            ),
                            const SizedBox(height: 6),
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
                        const SizedBox(width: 18),
                        Container(height: 26, width: 1, color: Colors.white24),
                        const SizedBox(width: 18),
                        ElevatedButton(
                          onPressed: () {
                            HapticFeedback.lightImpact();
                            Navigator.push(context, MaterialPageRoute(builder: (context) => const SimulatorScreen()));
                          },
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.white,
                            foregroundColor: TMembershipColors.primaryBlue,
                            elevation: 0,
                            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                            minimumSize: Size.zero,
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                          ),
                          child: Row(
                            children: [
                              Text(L10n.s(lang, 'calculate_btn'), style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 12)),
                              const SizedBox(width: 4),
                              const Icon(Icons.arrow_forward_rounded, size: 14),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  /// 광고보고 VIP 24시간 광고제거 단독 한줄 배너
  Widget _buildWatchAdVipOneLineBanner(BuildContext context, LanguageType lang, bool isDark) {
    final border = isDark ? const Color(0xFF5D4037) : const Color(0xFFFFD54F);
    final isKo = lang == LanguageType.ko;

    return Container(
      width: double.infinity,
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: isDark
              ? [const Color(0xFF2E1C0C), const Color(0xFF1E1E24)]
              : [const Color(0xFFFFF8E1), const Color(0xFFFFF3E0)],
          begin: Alignment.centerLeft,
          end: Alignment.centerRight,
        ),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: border.withValues(alpha: 0.6), width: 1.2),
        boxShadow: isDark ? [] : TMembershipColors.softShadow(blur: 10, dy: 3),
      ),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: () => _showRewardedAdForVip(context, lang),
          borderRadius: BorderRadius.circular(16),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
            child: Row(
              children: [
                Container(
                  width: 36,
                  height: 36,
                  decoration: BoxDecoration(
                    gradient: const LinearGradient(
                      colors: [Color(0xFFF7971E), Color(0xFFFFD200)],
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                    ),
                    borderRadius: BorderRadius.circular(11),
                    boxShadow: [
                      BoxShadow(
                        color: const Color(0xFFFFD200).withValues(alpha: 0.4),
                        blurRadius: 8,
                        offset: const Offset(0, 2),
                      ),
                    ],
                  ),
                  child: const Center(
                    child: Icon(Icons.stars_rounded, color: Colors.white, size: 20),
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      FittedBox(
                        fit: BoxFit.scaleDown,
                        alignment: Alignment.centerLeft,
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Text(
                              isKo ? '광고 보고 VIP 24시간 광고 제거' : 'Watch Ad for 24h VIP Ad-Free',
                              style: GoogleFonts.inter(
                                fontWeight: FontWeight.w800,
                                fontSize: 13,
                                color: isDark ? Colors.amber.shade200 : const Color(0xFFB78103),
                              ),
                            ),
                            const SizedBox(width: 6),
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 5, vertical: 1.5),
                              decoration: BoxDecoration(
                                color: const Color(0xFFFF9800).withValues(alpha: 0.2),
                                borderRadius: BorderRadius.circular(5),
                              ),
                              child: const Text(
                                'FREE',
                                style: TextStyle(
                                  color: Color(0xFFFF9800),
                                  fontWeight: FontWeight.w900,
                                  fontSize: 9,
                                  letterSpacing: 0.5,
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(height: 2),
                      FittedBox(
                        fit: BoxFit.scaleDown,
                        alignment: Alignment.centerLeft,
                        child: Text(
                          isKo ? '짧은 영상 1편 시청 시 24시간 동안 모든 광고 완전 제거' : 'Watch 1 short video to remove all ads for 24h',
                          style: TextStyle(
                            color: isDark ? Colors.white60 : Colors.black54,
                            fontSize: 10.5,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(width: 8),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                  decoration: BoxDecoration(
                    gradient: TMembershipColors.vipGoldGradient,
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        isKo ? '받기' : 'Claim',
                        style: const TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.w800,
                          fontSize: 11,
                        ),
                      ),
                      const SizedBox(width: 2),
                      const Icon(Icons.arrow_forward_ios_rounded, color: Colors.white, size: 9),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  /// 물타기 시뮬레이터 긴 1줄 히어로 버튼
  Widget _buildSimulatorHeroButton(BuildContext context, LanguageType lang, bool isDark) {
    return Container(
      width: double.infinity,
      decoration: BoxDecoration(
        gradient: TMembershipColors.actionPurpleGradient,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: const Color(0xFF6B4226).withValues(alpha: 0.35),
            blurRadius: 16,
            offset: const Offset(0, 6),
          ),
        ],
      ),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: () {
            HapticFeedback.lightImpact();
            Navigator.push(context, MaterialPageRoute(builder: (context) => const SimulatorScreen()));
          },
          borderRadius: BorderRadius.circular(20),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
            child: Row(
              children: [
                Container(
                  width: 46,
                  height: 46,
                  decoration: BoxDecoration(
                    color: Colors.white.withValues(alpha: 0.18),
                    borderRadius: BorderRadius.circular(14),
                    border: Border.all(color: Colors.white.withValues(alpha: 0.3)),
                  ),
                  child: const Center(
                    child: Icon(Icons.calculate_rounded, color: Colors.white, size: 26),
                  ),
                ),
                const SizedBox(width: 14),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      FittedBox(
                        fit: BoxFit.scaleDown,
                        alignment: Alignment.centerLeft,
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Text(
                              L10n.s(lang, 'simulator'),
                              style: GoogleFonts.inter(
                                color: Colors.white,
                                fontWeight: FontWeight.w900,
                                fontSize: 16,
                                letterSpacing: -0.3,
                              ),
                            ),
                            const SizedBox(width: 8),
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                              decoration: BoxDecoration(
                                color: Colors.white.withValues(alpha: 0.22),
                                borderRadius: BorderRadius.circular(6),
                              ),
                              child: const Text(
                                'CORE',
                                style: TextStyle(
                                  color: Colors.white,
                                  fontWeight: FontWeight.w900,
                                  fontSize: 9,
                                  letterSpacing: 0.6,
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(height: 3),
                      FittedBox(
                        fit: BoxFit.scaleDown,
                        alignment: Alignment.centerLeft,
                        child: Text(
                          L10n.s(lang, 'sim_sub'),
                          style: TextStyle(
                            color: Colors.white.withValues(alpha: 0.85),
                            fontWeight: FontWeight.w600,
                            fontSize: 11.5,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(width: 10),
                Container(
                  width: 36,
                  height: 36,
                  decoration: BoxDecoration(
                    color: Colors.white,
                    shape: BoxShape.circle,
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withValues(alpha: 0.12),
                        blurRadius: 8,
                        offset: const Offset(0, 2),
                      ),
                    ],
                  ),
                  child: const Center(
                    child: Icon(Icons.arrow_forward_rounded, color: Color(0xFF6B4226), size: 18),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  /// T-Membership Style Quick Action Grid (짝수 4개 구성)
  Widget _buildQuickActions(BuildContext context, LanguageType lang, bool isDark) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(left: 4, bottom: 12),
          child: Text(
            L10n.s(lang, 'quick_actions'),
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
                title: L10n.s(lang, 'scenario_history'),
                subtitle: L10n.s(lang, 'scenario_sub'),
                icon: Icons.history_toggle_off_rounded,
                gradient: TMembershipColors.cardTealBlueGradient,
                isDark: isDark,
                onTap: () => Navigator.push(context, MaterialPageRoute(builder: (context) => const ScenarioHistoryScreen())),
              ),
            ),
            const SizedBox(width: 14),
            Expanded(
              child: _buildActionTile(
                context: context,
                title: L10n.s(lang, 'portfolio_report'),
                subtitle: L10n.s(lang, 'report_sub'),
                icon: Icons.pie_chart_outline_rounded,
                gradient: TMembershipColors.vipGoldGradient,
                isDark: isDark,
                onTap: () => Navigator.push(context, MaterialPageRoute(builder: (context) => const PortfolioReportScreen())),
              ),
            ),
          ],
        ),
        const SizedBox(height: 14),
        Row(
          children: [
            Expanded(
              child: _buildActionTile(
                context: context,
                title: L10n.s(lang, 'voice_ai'),
                subtitle: L10n.s(lang, 'voice_sub'),
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
            const SizedBox(width: 14),
            Expanded(
              child: _buildActionTile(
                context: context,
                title: L10n.s(lang, 'how_to_use_guide'),
                subtitle: L10n.s(lang, 'guide_sub'),
                icon: Icons.menu_book_rounded,
                gradient: const LinearGradient(
                  colors: [Color(0xFF00C6FF), Color(0xFF0072FF)],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                isDark: isDark,
                onTap: () => Navigator.push(context, MaterialPageRoute(builder: (context) => const HelpScreen())),
              ),
            ),
          ],
        ),
      ],
    );
  }

  void _showRewardedAdForVip(BuildContext context, LanguageType lang) {
    HapticFeedback.mediumImpact();
    AdmobService.showRewarded(
      onUserEarnedReward: (reward) async {
        await EventService.addAdFreeHours(24);
        _checkAdFreeStatus();
        if (context.mounted) {
          HapticFeedback.heavyImpact();
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Row(
                children: [
                  const Icon(Icons.stars_rounded, color: Colors.amber, size: 24),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Text(
                      L10n.s(lang, 'vip_reward_unlocked'),
                      style: const TextStyle(fontWeight: FontWeight.w800),
                    ),
                  ),
                ],
              ),
              backgroundColor: const Color(0xFF1A1F2C),
              behavior: SnackBarBehavior.floating,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
            ),
          );
        }
      },
      onDismissed: () {},
      onFailed: (err) {
        if (context.mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text("Ad loading failed. Please try again shortly."),
              behavior: SnackBarBehavior.floating,
            ),
          );
        }
      },
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
          onTap: () {
            HapticFeedback.lightImpact();
            onTap();
          },
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
                FittedBox(
                  fit: BoxFit.scaleDown,
                  alignment: Alignment.centerLeft,
                  child: Text(
                    title,
                    style: GoogleFonts.inter(
                      fontWeight: FontWeight.w800,
                      fontSize: 14,
                      color: titleColor,
                    ),
                  ),
                ),
                const SizedBox(height: 9),
                FittedBox(
                  fit: BoxFit.scaleDown,
                  alignment: Alignment.centerLeft,
                  child: Text(
                    subtitle,
                    style: GoogleFonts.inter(
                      fontWeight: FontWeight.w600,
                      fontSize: 11,
                      color: subColor,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  /// T-Membership clean asset list
  Widget _buildAssetList(
    BuildContext context,
    List<Asset> assets,
    CurrencyType currency,
    LanguageType lang,
    bool isDark,
  ) {
    final cardBg = isDark ? TMembershipColors.darkSurface : TMembershipColors.lightSurface;
    final cardBorder = isDark ? TMembershipColors.darkCardBorder : TMembershipColors.lightCardBorder;
    final titleColor = isDark ? TMembershipColors.darkTextPrimary : TMembershipColors.lightTextPrimary;
    final subColor = isDark ? TMembershipColors.darkTextTertiary : TMembershipColors.lightTextTertiary;
    final isKo = lang == LanguageType.ko;

    final formatter = NumberFormat.currency(
      symbol: currency.symbol,
      decimalDigits: currency.decimalDigits,
    );

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              L10n.s(lang, 'my_assets_header'),
              style: GoogleFonts.inter(
                fontWeight: FontWeight.w800,
                fontSize: 16,
                color: titleColor,
              ),
            ),
            if (assets.isNotEmpty)
              Text(
                "${assets.length} ${L10n.s(lang, 'asset_count_suffix')}",
                style: const TextStyle(color: TMembershipColors.primaryBlue, fontWeight: FontWeight.bold, fontSize: 13),
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
                  L10n.s(lang, 'no_assets'),
                  style: TextStyle(color: titleColor, fontWeight: FontWeight.w700, fontSize: 14),
                ),
                const SizedBox(height: 4),
                Text(
                  isKo ? "시뮬레이터에서 계산 후 자산으로 저장해보세요." : "Calculate in simulator and save as assets.",
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
                final totalVal = asset.initialPrice * asset.initialQuantity;
                final displayName = (asset.name == 'New Asset' || asset.name.trim().isEmpty)
                    ? (isKo ? '보유 종목' : 'Stock Asset')
                    : asset.name;

                return Dismissible(
                  key: Key("home_asset_${asset.id ?? index}"),
                  direction: DismissDirection.endToStart,
                  background: Container(
                    color: TMembershipColors.accentCoral,
                    alignment: Alignment.centerRight,
                    padding: const EdgeInsets.only(right: 20),
                    child: const Icon(Icons.delete_outline_rounded, color: Colors.white, size: 24),
                  ),
                  onDismissed: (_) {
                    if (asset.id != null) {
                      ref.read(assetsProvider.notifier).removeAsset(asset.id!);
                      HapticFeedback.mediumImpact();
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text(isKo ? "$displayName이(가) 삭제되었습니다." : "$displayName deleted."),
                          behavior: SnackBarBehavior.floating,
                        ),
                      );
                    }
                  },
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 15),
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
                        const SizedBox(width: 14),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                displayName,
                                maxLines: 1,
                                overflow: TextOverflow.ellipsis,
                                style: GoogleFonts.inter(
                                  fontWeight: FontWeight.w800,
                                  fontSize: 14.5,
                                  color: titleColor,
                                  letterSpacing: -0.2,
                                ),
                              ),
                              const SizedBox(height: 4),
                              Text(
                                "${asset.initialQuantity.toStringAsFixed(0)}${isKo ? '주' : ' shares'} • ${isKo ? '평단' : 'Avg'} ${formatter.format(asset.initialPrice)}",
                                maxLines: 1,
                                overflow: TextOverflow.ellipsis,
                                style: TextStyle(
                                  color: subColor,
                                  fontWeight: FontWeight.w600,
                                  fontSize: 12,
                                ),
                              ),
                            ],
                          ),
                        ),
                        const SizedBox(width: 12),
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.end,
                          children: [
                            Text(
                              formatter.format(totalVal),
                              style: GoogleFonts.inter(
                                color: titleColor,
                                fontWeight: FontWeight.w800,
                                fontSize: 14.5,
                                letterSpacing: -0.3,
                              ),
                            ),
                            const SizedBox(height: 3),
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                              decoration: BoxDecoration(
                                color: TMembershipColors.primaryBlue.withOpacity(0.08),
                                borderRadius: BorderRadius.circular(5),
                              ),
                              child: Text(
                                isKo ? "보유 자산" : "Holding",
                                style: const TextStyle(
                                  color: TMembershipColors.primaryBlue,
                                  fontWeight: FontWeight.w700,
                                  fontSize: 10,
                                ),
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
      ],
    );
  }

  /// Security Notice Card
  Widget _buildSecurityNoticeCard(BuildContext context, bool isDark, LanguageType lang) {
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
                  L10n.s(lang, 'security_title'),
                  style: GoogleFonts.inter(fontWeight: FontWeight.w800, fontSize: 13, color: titleColor),
                ),
                const SizedBox(height: 8),
                Text(
                  L10n.s(lang, 'security_sub'),
                  style: TextStyle(color: subColor, fontSize: 11, height: 1.4),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
