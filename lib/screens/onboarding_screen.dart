import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';

import '../theme/t_membership_colors.dart';
import '../utils/l10n.dart';
import '../providers/language_provider.dart';
import '../services/storage_service.dart';
import 'home_screen.dart';

class OnboardingScreen extends ConsumerStatefulWidget {
  const OnboardingScreen({super.key});

  @override
  ConsumerState<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends ConsumerState<OnboardingScreen> {
  final PageController _pageController = PageController();
  int _currentPage = 0;

  final List<OnboardingStepData> _steps = [
    OnboardingStepData(
      badgeKey: 'onboarding_step_badge_1',
      titleKey: 'onboarding_title_1',
      descKey: 'onboarding_desc_1',
      icon: Icons.account_balance_wallet_rounded,
      tag: '01',
      gradient: TMembershipColors.primaryGradient,
      accentColor: TMembershipColors.primaryBlue,
      previewWidget: const _Step1Preview(),
    ),
    OnboardingStepData(
      badgeKey: 'onboarding_step_badge_2',
      titleKey: 'onboarding_title_2',
      descKey: 'onboarding_desc_2',
      icon: Icons.calculate_rounded,
      tag: '02',
      gradient: TMembershipColors.actionPurpleGradient,
      accentColor: TMembershipColors.accentMagenta,
      previewWidget: const _Step2Preview(),
    ),
    OnboardingStepData(
      badgeKey: 'onboarding_step_badge_3',
      titleKey: 'onboarding_title_3',
      descKey: 'onboarding_desc_3',
      icon: Icons.mic_rounded,
      tag: '03',
      gradient: TMembershipColors.cardTealBlueGradient,
      accentColor: const Color(0xFF00C6FF),
      previewWidget: const _Step3Preview(),
    ),
    OnboardingStepData(
      badgeKey: 'onboarding_step_badge_4',
      titleKey: 'onboarding_title_4',
      descKey: 'onboarding_desc_4',
      icon: Icons.security_rounded,
      tag: '04',
      gradient: TMembershipColors.vipGoldGradient,
      accentColor: const Color(0xFFFFB300),
      previewWidget: const _Step4Preview(),
    ),
  ];

  void _onFinish() async {
    await StorageService().setSeenOnboarding();
    if (mounted) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => const HomeScreen()),
      );
    }
  }

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(languageProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final bgColor = isDark ? TMembershipColors.darkBg : TMembershipColors.lightBg;
    final textPrimary = isDark ? TMembershipColors.darkTextPrimary : TMembershipColors.lightTextPrimary;
    final textSecondary = isDark ? TMembershipColors.darkTextSecondary : TMembershipColors.lightTextSecondary;

    return Scaffold(
      backgroundColor: bgColor,
      body: SafeArea(
        child: Column(
          children: [
            // Top Bar: Brand & Skip Button
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Row(
                      children: [
                        Container(
                          width: 28,
                          height: 28,
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(8),
                            boxShadow: [
                              BoxShadow(
                                color: TMembershipColors.primaryBlue.withOpacity(0.3),
                                blurRadius: 8,
                              ),
                            ],
                          ),
                          child: ClipRRect(
                            borderRadius: BorderRadius.circular(8),
                            child: Image.asset('assets/app_icon.png', fit: BoxFit.cover),
                          ),
                        ),
                        const SizedBox(width: 8),
                        Expanded(
                          child: Text(
                            L10n.s(lang, 'app_title'),
                            style: GoogleFonts.inter(
                              fontWeight: FontWeight.w900,
                              fontSize: 14,
                              color: textPrimary,
                              letterSpacing: -0.3,
                            ),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                      ],
                    ),
                  ),
                  TextButton(
                    onPressed: _onFinish,
                    style: TextButton.styleFrom(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                      minimumSize: Size.zero,
                      tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                    ),
                    child: Text(
                      L10n.s(lang, 'onboarding_skip_button'),
                      style: TextStyle(
                        color: textSecondary,
                        fontWeight: FontWeight.w700,
                        fontSize: 13,
                      ),
                    ),
                  ),
                ],
              ),
            ),

            // Main Content: PageView
            Expanded(
              child: PageView.builder(
                controller: _pageController,
                onPageChanged: (index) => setState(() => _currentPage = index),
                itemCount: _steps.length,
                itemBuilder: (context, index) {
                  final step = _steps[index];
                  return SingleChildScrollView(
                    physics: const BouncingScrollPhysics(),
                    padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 10),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        // Step Badge Pill
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
                          decoration: BoxDecoration(
                            color: step.accentColor.withOpacity(isDark ? 0.2 : 0.1),
                            borderRadius: BorderRadius.circular(20),
                            border: Border.all(
                              color: step.accentColor.withOpacity(0.4),
                              width: 1.2,
                            ),
                          ),
                          child: Text(
                            L10n.s(lang, step.badgeKey),
                            style: TextStyle(
                              color: step.accentColor,
                              fontSize: 12,
                              fontWeight: FontWeight.w800,
                              letterSpacing: 0.2,
                            ),
                          ),
                        ).animate(key: ValueKey('badge_$index')).fadeIn(duration: 300.ms).scale(begin: const Offset(0.9, 0.9)),

                        const SizedBox(height: 20),

                        // Interactive Visual Preview Card
                        Container(
                          width: double.infinity,
                          constraints: const BoxConstraints(maxWidth: 420),
                          padding: const EdgeInsets.all(20),
                          decoration: BoxDecoration(
                            color: isDark ? TMembershipColors.darkSurface : Colors.white,
                            borderRadius: BorderRadius.circular(28),
                            border: Border.all(
                              color: isDark ? TMembershipColors.darkCardBorder : TMembershipColors.lightCardBorder,
                              width: 1.2,
                            ),
                            boxShadow: [
                              BoxShadow(
                                color: step.accentColor.withOpacity(isDark ? 0.15 : 0.08),
                                blurRadius: 24,
                                offset: const Offset(0, 10),
                              ),
                            ],
                          ),
                          child: Column(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Row(
                                children: [
                                  Container(
                                    width: 44,
                                    height: 44,
                                    decoration: BoxDecoration(
                                      gradient: step.gradient,
                                      borderRadius: BorderRadius.circular(14),
                                      boxShadow: [
                                        BoxShadow(
                                          color: step.accentColor.withOpacity(0.4),
                                          blurRadius: 10,
                                          offset: const Offset(0, 4),
                                        ),
                                      ],
                                    ),
                                    child: Icon(step.icon, color: Colors.white, size: 24),
                                  ),
                                  const SizedBox(width: 12),
                                  Expanded(
                                    child: Column(
                                      crossAxisAlignment: CrossAxisAlignment.start,
                                      children: [
                                        Text(
                                          'GUIDE 0${index + 1} / 04',
                                          style: GoogleFonts.inter(
                                            fontSize: 11,
                                            fontWeight: FontWeight.w800,
                                            color: step.accentColor,
                                            letterSpacing: 1.0,
                                          ),
                                        ),
                                        const SizedBox(height: 2),
                                        Text(
                                          L10n.s(lang, 'app_subtitle'),
                                          style: TextStyle(
                                            fontSize: 12,
                                            fontWeight: FontWeight.w600,
                                            color: textSecondary,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                ],
                              ),
                              const SizedBox(height: 18),
                              step.previewWidget,
                            ],
                          ),
                        ).animate(key: ValueKey('preview_$index')).fadeIn(duration: 400.ms).slideY(begin: 0.08, end: 0),

                        const SizedBox(height: 28),

                        // Title
                        Text(
                          L10n.s(lang, step.titleKey),
                          textAlign: TextAlign.center,
                          style: GoogleFonts.inter(
                            fontSize: 21,
                            fontWeight: FontWeight.w900,
                            color: textPrimary,
                            letterSpacing: -0.6,
                            height: 1.35,
                          ),
                        ).animate(key: ValueKey('title_$index')).fadeIn(delay: 150.ms).slideY(begin: 0.1, end: 0),

                        const SizedBox(height: 12),

                        // Description
                        Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 10),
                          child: Text(
                            L10n.s(lang, step.descKey),
                            textAlign: TextAlign.center,
                            style: TextStyle(
                              fontSize: 13.5,
                              fontWeight: FontWeight.w500,
                              color: textSecondary,
                              height: 1.55,
                            ),
                          ),
                        ).animate(key: ValueKey('desc_$index')).fadeIn(delay: 250.ms).slideY(begin: 0.1, end: 0),
                      ],
                    ),
                  );
                },
              ),
            ),

            // Bottom Navigation Area: Dots & CTA Button
            Padding(
              padding: const EdgeInsets.fromLTRB(24, 12, 24, 24),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  // Step Indicator Dots
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: List.generate(_steps.length, (index) {
                      final isSelected = _currentPage == index;
                      return AnimatedContainer(
                        duration: const Duration(milliseconds: 300),
                        margin: const EdgeInsets.symmetric(horizontal: 4),
                        height: 7,
                        width: isSelected ? 28 : 7,
                        decoration: BoxDecoration(
                          color: isSelected
                              ? _steps[_currentPage].accentColor
                              : (isDark ? Colors.white24 : Colors.black12),
                          borderRadius: BorderRadius.circular(4),
                          boxShadow: isSelected
                              ? [
                                  BoxShadow(
                                    color: _steps[_currentPage].accentColor.withOpacity(0.4),
                                    blurRadius: 8,
                                    offset: const Offset(0, 2),
                                  ),
                                ]
                              : null,
                        ),
                      );
                    }),
                  ),

                  const SizedBox(height: 20),

                  // Action Button
                  SizedBox(
                    width: double.infinity,
                    height: 54,
                    child: ElevatedButton(
                      onPressed: () {
                        if (_currentPage == _steps.length - 1) {
                          _onFinish();
                        } else {
                          _pageController.nextPage(
                            duration: const Duration(milliseconds: 350),
                            curve: Curves.easeOutCubic,
                          );
                        }
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: _steps[_currentPage].accentColor,
                        foregroundColor: Colors.white,
                        elevation: 4,
                        shadowColor: _steps[_currentPage].accentColor.withOpacity(0.5),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(18),
                        ),
                      ),
                      child: Text(
                        _currentPage == _steps.length - 1
                            ? L10n.s(lang, 'onboarding_start_button')
                            : L10n.s(lang, 'onboarding_next_button'),
                        style: const TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w900,
                          letterSpacing: -0.2,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class OnboardingStepData {
  final String badgeKey;
  final String titleKey;
  final String descKey;
  final IconData icon;
  final String tag;
  final LinearGradient gradient;
  final Color accentColor;
  final Widget previewWidget;

  OnboardingStepData({
    required this.badgeKey,
    required this.titleKey,
    required this.descKey,
    required this.icon,
    required this.tag,
    required this.gradient,
    required this.accentColor,
    required this.previewWidget,
  });
}

// Visual Preview 1: Current Holdings & Calculation
class _Step1Preview extends StatelessWidget {
  const _Step1Preview();

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final rowBg = isDark ? const Color(0xFF1E2633) : const Color(0xFFF3F6FA);

    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: rowBg,
        borderRadius: BorderRadius.circular(18),
      ),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('보유 평단가', style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: Colors.grey)),
              Text('72,000 원', style: GoogleFonts.inter(fontSize: 14, fontWeight: FontWeight.w900, color: TMembershipColors.primaryBlue)),
            ],
          ),
          const SizedBox(height: 8),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('보유 수량', style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: Colors.grey)),
              Text('100 주', style: GoogleFonts.inter(fontSize: 14, fontWeight: FontWeight.w800)),
            ],
          ),
          const Divider(height: 18),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('총 매수 금액', style: TextStyle(fontSize: 12, fontWeight: FontWeight.w700)),
              Text('7,200,000 원', style: GoogleFonts.inter(fontSize: 14, fontWeight: FontWeight.w900, color: Colors.orangeAccent)),
            ],
          ),
        ],
      ),
    );
  }
}

// Visual Preview 2: Average Down & Target Price
class _Step2Preview extends StatelessWidget {
  const _Step2Preview();

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final rowBg = isDark ? const Color(0xFF1E2633) : const Color(0xFFF3F6FA);

    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: rowBg,
        borderRadius: BorderRadius.circular(18),
      ),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('추가 매수 계획', style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: Colors.grey)),
              Text('55,000원 × 100주', style: GoogleFonts.inter(fontSize: 13, fontWeight: FontWeight.w700, color: TMembershipColors.accentMagenta)),
            ],
          ),
          const SizedBox(height: 10),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            decoration: BoxDecoration(
              color: TMembershipColors.primaryBlue.withOpacity(0.12),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: TMembershipColors.primaryBlue.withOpacity(0.3)),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text('📉 탈출 평단가', style: TextStyle(fontSize: 12, fontWeight: FontWeight.w800, color: TMembershipColors.primaryBlue)),
                Text('63,500 원 (-11.8%)', style: GoogleFonts.inter(fontSize: 14, fontWeight: FontWeight.w900, color: TMembershipColors.primaryBlue)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

// Visual Preview 3: AI Voice Assistant
class _Step3Preview extends StatelessWidget {
  const _Step3Preview();

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final rowBg = isDark ? const Color(0xFF1E2633) : const Color(0xFFF3F6FA);

    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: rowBg,
        borderRadius: BorderRadius.circular(18),
      ),
      child: Row(
        children: [
          Container(
            width: 40,
            height: 40,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: const Color(0xFF00C6FF).withOpacity(0.2),
              border: Border.all(color: const Color(0xFF00C6FF), width: 1.5),
            ),
            child: const Icon(Icons.mic_rounded, color: Color(0xFF00C6FF), size: 22),
          ),
          const SizedBox(width: 12),
          const Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('🗣️ 음성 자동 인식', style: TextStyle(fontSize: 11, fontWeight: FontWeight.w700, color: Color(0xFF00C6FF))),
                SizedBox(height: 2),
                Text('"삼성전자 6만원에 50주 물타기"', style: TextStyle(fontSize: 13, fontWeight: FontWeight.w800)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

// Visual Preview 4: 100% On-Device Safe & Portfolio
class _Step4Preview extends StatelessWidget {
  const _Step4Preview();

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final rowBg = isDark ? const Color(0xFF1E2633) : const Color(0xFFF3F6FA);

    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: rowBg,
        borderRadius: BorderRadius.circular(18),
      ),
      child: Row(
        children: [
          Container(
            width: 40,
            height: 40,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: const Color(0xFFFFB300).withOpacity(0.2),
              border: Border.all(color: const Color(0xFFFFB300), width: 1.5),
            ),
            child: const Icon(Icons.lock_outline_rounded, color: Color(0xFFFFB300), size: 22),
          ),
          const SizedBox(width: 12),
          const Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('🔒 100% 로컬 암호화 보관', style: TextStyle(fontSize: 11, fontWeight: FontWeight.w700, color: Color(0xFFFFB300))),
                SizedBox(height: 2),
                Text('서버 전송 ZERO · 오프라인 완벽 작동', style: TextStyle(fontSize: 13, fontWeight: FontWeight.w800)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
