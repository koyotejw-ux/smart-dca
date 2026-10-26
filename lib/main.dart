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
import 'services/admob_service.dart';

import 'screens/portfolio_report_screen.dart';
import 'screens/settings_screen.dart';
import 'providers/currency_provider.dart';

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

  // Check onboarding & saved settings
  final storage = StorageService();
  final hasSeenOnboarding = await storage.hasSeenOnboarding();
  final savedLang = await storage.getSetting('selected_language');
  final savedCurr = await storage.getSetting('selected_currency');
  final savedTheme = await storage.getSetting('theme_mode');
  final savedFlow = await storage.getSetting('initial_flow');

  // Initialize Google AdMob
  await AdmobService.initialize();

  // Check for web query parameter flow (e.g. ?flow=voice, ?flow=target, ?flow=sim, ?flow=report, ?flow=settings)
  String? initialFlow;
  if (kIsWeb) {
    try {
      initialFlow = Uri.base.queryParameters['flow'];
    } catch (_) {}
  }
  
  runApp(
    ProviderScope(
      overrides: [
        if (savedLang != null && savedLang.isNotEmpty)
          languageProvider.overrideWith((ref) => LanguageNotifier()..setLanguage(LanguageTypeExtension.fromCode(savedLang))),
        if (savedCurr != null && savedCurr.isNotEmpty)
          currencyProvider.overrideWith((ref) => CurrencyNotifier()..setCurrency(CurrencyType.values.firstWhere((c) => c.name.toLowerCase() == savedCurr.toLowerCase(), orElse: () => CurrencyType.krw))),
        if (savedTheme != null && savedTheme.isNotEmpty)
          themeModeProvider.overrideWith((ref) => ThemeModeNotifier()..setThemeMode(savedTheme == 'dark' ? ThemeMode.dark : ThemeMode.light)),
      ],
      child: MyApp(
        hasSeenOnboarding: kIsWeb ? true : hasSeenOnboarding,
        initialFlow: initialFlow ?? savedFlow,
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
    } else if (initialFlow == 'report') {
      initialScreen = const PortfolioReportScreen();
    } else if (initialFlow == 'settings') {
      initialScreen = const SettingsScreen();
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


