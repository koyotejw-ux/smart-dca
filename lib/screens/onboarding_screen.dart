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

  final List<OnboardingData> _onboardingData = [
    OnboardingData(
      titleKey: 'onboarding_title_1',
      descKey: 'onboarding_desc_1',
      icon: Icons.trending_up_rounded,
      gradient: TMembershipColors.primaryGradient,
    ),
    OnboardingData(
      titleKey: 'onboarding_title_2',
      descKey: 'onboarding_desc_2',
      icon: Icons.calculate_rounded,
      gradient: TMembershipColors.actionPurpleGradient,
    ),
    OnboardingData(
      titleKey: 'onboarding_title_3',
      descKey: 'onboarding_desc_3',
      icon: Icons.auto_awesome_rounded,
      gradient: TMembershipColors.cardTealBlueGradient,
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
  Widget build(BuildContext context) {
    final lang = ref.watch(languageProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final bgColor = isDark ? TMembershipColors.darkBg : TMembershipColors.lightBg;
    final textPrimary = isDark ? TMembershipColors.darkTextPrimary : TMembershipColors.lightTextPrimary;
    final textSecondary = isDark ? TMembershipColors.darkTextSecondary : TMembershipColors.lightTextSecondary;

    return Scaffold(
      backgroundColor: bgColor,
      body: SafeArea(
        child: Stack(
          children: [
            PageView.builder(
              controller: _pageController,
              onPageChanged: (index) => setState(() => _currentPage = index),
              itemCount: _onboardingData.length,
              itemBuilder: (context, index) {
                final data = _onboardingData[index];
                return Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 36),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Container(
                        width: 140,
                        height: 140,
                        decoration: BoxDecoration(
                          gradient: data.gradient,
                          borderRadius: BorderRadius.circular(36),
                          boxShadow: TMembershipColors.colorfulGlow(TMembershipColors.primaryBlue, opacity: 0.35),
                        ),
                        child: Center(
                          child: Icon(data.icon, size: 70, color: Colors.white),
                        ),
                      ).animate().scale(duration: 600.ms, curve: Curves.easeOutBack),
                      const SizedBox(height: 50),
                      Text(
                        L10n.s(lang, data.titleKey),
                        style: GoogleFonts.inter(
                          fontWeight: FontWeight.w900,
                          fontSize: 24,
                          color: textPrimary,
                          letterSpacing: -0.5,
                        ),
                        textAlign: TextAlign.center,
                      ).animate().fadeIn(delay: 200.ms).slideY(begin: 0.1, end: 0),
                      const SizedBox(height: 16),
                      Text(
                        L10n.s(lang, data.descKey),
                        style: TextStyle(
                          fontSize: 14,
                          height: 1.5,
                          color: textSecondary,
                          fontWeight: FontWeight.w500,
                        ),
                        textAlign: TextAlign.center,
                      ).animate().fadeIn(delay: 350.ms).slideY(begin: 0.1, end: 0),
                    ],
                  ),
                );
              },
            ),
            Positioned(
              bottom: 30,
              left: 24,
              right: 24,
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: List.generate(
                      _onboardingData.length,
                      (index) => AnimatedContainer(
                        duration: const Duration(milliseconds: 300),
                        margin: const EdgeInsets.symmetric(horizontal: 4),
                        height: 6,
                        width: _currentPage == index ? 24 : 6,
                        decoration: BoxDecoration(
                          color: _currentPage == index
                              ? TMembershipColors.primaryBlue
                              : (isDark ? Colors.white24 : Colors.black12),
                          borderRadius: BorderRadius.circular(3),
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(height: 32),
                  SizedBox(
                    width: double.infinity,
                    height: 56,
                    child: ElevatedButton(
                      onPressed: () {
                        if (_currentPage == _onboardingData.length - 1) {
                          _onFinish();
                        } else {
                          _pageController.nextPage(
                            duration: const Duration(milliseconds: 400),
                            curve: Curves.easeInOut,
                          );
                        }
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: TMembershipColors.primaryBlue,
                        elevation: 4,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(18),
                        ),
                      ),
                      child: Text(
                        _currentPage == _onboardingData.length - 1
                            ? L10n.s(lang, 'get_started')
                            : L10n.s(lang, 'next'),
                        style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w900, color: Colors.white),
                      ),
                    ),
                  ),
                  if (_currentPage < _onboardingData.length - 1)
                    TextButton(
                      onPressed: _onFinish,
                      child: Text(
                        L10n.s(lang, 'skip'),
                        style: TextStyle(color: textSecondary, fontWeight: FontWeight.bold),
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

class OnboardingData {
  final String titleKey;
  final String descKey;
  final IconData icon;
  final LinearGradient gradient;

  OnboardingData({
    required this.titleKey,
    required this.descKey,
    required this.icon,
    required this.gradient,
  });
}
