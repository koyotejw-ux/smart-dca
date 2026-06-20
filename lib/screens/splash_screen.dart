import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
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
    await Future.delayed(const Duration(milliseconds: 2500));
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
    final theme = Theme.of(context);

    return Scaffold(
      body: Stack(
        children: [
          // Background Gradient Image
          Positioned.fill(
            child: Image.asset(
              'assets/splash_bg.png',
              fit: BoxFit.cover,
            ).animate().fadeIn(duration: 1000.ms),
          ),
          // Logo & Title
          Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Container(
                  width: 120,
                  height: 120,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(30),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.3),
                        blurRadius: 20,
                        offset: const Offset(0, 10),
                      ),
                    ],
                  ),
                  child: ClipRRect(
                    borderRadius: BorderRadius.circular(30),
                    child: Image.asset('assets/app_icon.png'),
                  ),
                ).animate()
                  .scale(duration: 800.ms, curve: Curves.easeOutBack)
                  .shimmer(delay: 1000.ms, duration: 1500.ms),
                const SizedBox(height: 32),
                Text(
                  L10n.s(lang, 'app_title'),
                  style: theme.textTheme.headlineMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                    letterSpacing: 1.2,
                  ),
                ).animate().fadeIn(delay: 400.ms).slideY(begin: 0.2, end: 0),
              ],
            ),
          ),
          // Bottom Version or Credits
          Positioned(
            bottom: 40,
            left: 0,
            right: 0,
            child: Center(
              child: Text(
                'v1.0.0 Elite Edition',
                style: theme.textTheme.labelMedium?.copyWith(
                  color: Colors.white.withOpacity(0.5),
                ),
              ).animate().fadeIn(delay: 1500.ms),
            ),
          ),
        ],
      ),
    );
  }
}
