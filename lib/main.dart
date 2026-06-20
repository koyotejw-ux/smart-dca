import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'theme/one_ui_theme.dart';
import 'screens/splash_screen.dart';
import 'providers/language_provider.dart';
import 'utils/l10n.dart';
import 'screens/onboarding_screen.dart';
import 'services/storage_service.dart';
import 'package:flutter/services.dart';
import 'services/unity_ad_service.dart';
import 'services/admob_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  await SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
  ]);

  // Initialize Unity Ads
  await UnityAdService.init(testMode: true);

  // Initialize Google AdMob
  await AdmobService.initialize();
  
  runApp(
    const ProviderScope(
      child: MyApp(),
    ),
  );
}


class MyApp extends ConsumerWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(languageProvider);
    
    return MaterialApp(
      title: L10n.s(lang, 'app_title'),
      debugShowCheckedModeBanner: false,
      theme: OneUITheme.lightTheme,
      darkTheme: OneUITheme.darkTheme,
      themeMode: ThemeMode.system,
      home: const CustomSplashScreen(),
    );
  }
}
