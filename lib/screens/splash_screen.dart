import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';

import '../utils/l10n.dart';
import '../providers/language_provider.dart';
import '../services/storage_service.dart';
import 'onboarding_screen.dart';
import 'home_screen.dart';
import '../services/admob_service.dart';

class CustomSplashScreen extends ConsumerStatefulWidget {
  const CustomSplashScreen({super.key});

  @override
  ConsumerState<CustomSplashScreen> createState() => _CustomSplashScreenState();
}

class _CustomSplashScreenState extends ConsumerState<CustomSplashScreen> {
  @override
  void initState() {
    super.initState();
    _navigateToNext();
  }

  Future<void> _navigateToNext() async {
    await Future.delayed(const Duration(milliseconds: 1200));
    final storage = StorageService();
    final hasSeenOnboarding = await storage.hasSeenOnboarding();

    if (mounted) {
      AdmobService.showAppOpenAd(
        onDismiss: () {
          if (mounted) {
            Navigator.pushReplacement(
              context,
              MaterialPageRoute(
                builder: (context) => hasSeenOnboarding ? const HomeScreen() : const OnboardingScreen(),
              ),
            );
          }
        },
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(languageProvider);

    return Scaffold(
      backgroundColor: const Color(0xFF0F141C),
      body: Stack(
        children: [
          // Background Gradient Image
          Positioned.fill(
            child: Image.asset(
              'assets/splash_bg.png',
              fit: BoxFit.cover,
            ).animate().fadeIn(duration: 800.ms),
          ),

          // Central Floating Glass Logo & Branding
          Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Container(
                  width: 140,
                  height: 140,
                  alignment: Alignment.center,
                  child: Image.asset(
                    'assets/app_icon.png',
                    fit: BoxFit.contain,
                  ),
                ).animate()
                  .scale(duration: 600.ms, curve: Curves.easeOutBack),
                const SizedBox(height: 28),
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 24),
                  child: FittedBox(
                    fit: BoxFit.scaleDown,
                    child: Text(
                      L10n.s(lang, 'app_title'),
                      style: GoogleFonts.inter(
                        fontWeight: FontWeight.w900,
                        fontSize: 27,
                        color: Colors.white,
                        letterSpacing: -0.5,
                      ),
                    ),
                  ),
                ).animate().fadeIn(delay: 300.ms).slideY(begin: 0.15, end: 0),
                const SizedBox(height: 12),
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 32),
                  child: FittedBox(
                    fit: BoxFit.scaleDown,
                    child: Text(
                      L10n.s(lang, 'app_subtitle'),
                      style: TextStyle(
                        color: Colors.white.withValues(alpha: 0.85),
                        fontWeight: FontWeight.w600,
                        fontSize: 13.5,
                        letterSpacing: 0.2,
                      ),
                    ),
                  ),
                ).animate().fadeIn(delay: 450.ms),
              ],
            ),
          ),

          // Bottom Credits
          Positioned(
            bottom: 40,
            left: 0,
            right: 0,
            child: Center(
              child: Text(
                'v3.2.0 • 100% On-Device Safe',
                style: TextStyle(
                  color: Colors.white.withOpacity(0.4),
                  fontSize: 11,
                  fontWeight: FontWeight.w600,
                ),
              ).animate().fadeIn(delay: 1000.ms),
            ),
          ),
        ],
      ),
    );
  }
}
