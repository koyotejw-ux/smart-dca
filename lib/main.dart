import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'theme/one_ui_theme.dart';
import 'screens/splash_screen.dart';
import 'screens/home_screen.dart';
import 'screens/simulator_screen.dart';
import 'screens/onboarding_screen.dart';
import 'services/storage_service.dart';
import 'providers/language_provider.dart';
import 'providers/theme_provider.dart';
import 'utils/l10n.dart';
import 'package:flutter/services.dart';
import 'services/unity_ad_service.dart';
import 'services/admob_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  if (!kIsWeb) {
    try {
      await SystemChrome.setPreferredOrientations([
        DeviceOrientation.portraitUp,
        DeviceOrientation.portraitDown,
        DeviceOrientation.landscapeLeft,
        DeviceOrientation.landscapeRight,
      ]);
    } catch (_) {}
  }

  // Check onboarding status
  final hasSeenOnboarding = await StorageService().hasSeenOnboarding();

  // Initialize Unity Ads
  await UnityAdService.init(testMode: true);

  // Initialize Google AdMob
  await AdmobService.initialize();

  // Check for web query parameter flow (e.g. ?flow=voice, ?flow=target, ?flow=sim)
  String? initialFlow;
  if (kIsWeb) {
    try {
      initialFlow = Uri.base.queryParameters['flow'];
    } catch (_) {}
  }
  
  runApp(
    ProviderScope(
      child: MyApp(
        hasSeenOnboarding: kIsWeb ? true : hasSeenOnboarding,
        initialFlow: initialFlow,
      ),
    ),
  );
}

class MyApp extends ConsumerWidget {
  final bool hasSeenOnboarding;
  final String? initialFlow;
  const MyApp({
    super.key,
    required this.hasSeenOnboarding,
    this.initialFlow,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(languageProvider);
    final themeMode = ref.watch(themeModeProvider);
    
    Widget initialScreen;
    if (initialFlow == 'target') {
      initialScreen = const SimulatorScreen(initialTargetMode: true);
    } else if (initialFlow == 'sim') {
      initialScreen = const SimulatorScreen();
    } else if (initialFlow == 'voice') {
      initialScreen = const HomeScreen(initialOpenVoice: true);
    } else {
      initialScreen = hasSeenOnboarding ? const HomeScreen() : const OnboardingScreen();
    }

    return MaterialApp(
      title: L10n.s(lang, 'app_title'),
      debugShowCheckedModeBanner: false,
      locale: Locale(lang.code),
      supportedLocales: LanguageType.values.map((lt) => Locale(lt.code)),
      localizationsDelegates: const [
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      theme: OneUITheme.lightTheme,
      darkTheme: OneUITheme.darkTheme,
      themeMode: themeMode,
      home: initialScreen,
    );
  }
}


