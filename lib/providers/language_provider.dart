import 'package:flutter_riverpod/flutter_riverpod.dart';

enum LanguageType {
  ko,
  en,
  ja,
  zh,
  es,
  vi,
  id,
}

extension LanguageTypeExtension on LanguageType {
  String get displayName {
    switch (this) {
      case LanguageType.ko:
        return '한국어';
      case LanguageType.en:
        return 'English';
      case LanguageType.ja:
        return '日本語';
      case LanguageType.zh:
        return '中文';
      case LanguageType.es:
        return 'Español';
      case LanguageType.vi:
        return 'Tiếng Việt';
      case LanguageType.id:
        return 'Bahasa Indonesia';
    }
  }

  String get flag {
    switch (this) {
      case LanguageType.ko:
        return '🇰🇷';
      case LanguageType.en:
        return '🇺🇸';
      case LanguageType.ja:
        return '🇯🇵';
      case LanguageType.zh:
        return '🇨🇳';
      case LanguageType.es:
        return '🇪🇸';
      case LanguageType.vi:
        return '🇻🇳';
      case LanguageType.id:
        return '🇮🇩';
    }
  }
}

final languageProvider = StateNotifierProvider<LanguageNotifier, LanguageType>((ref) {
  return LanguageNotifier();
});

class LanguageNotifier extends StateNotifier<LanguageType> {
  LanguageNotifier() : super(LanguageType.ko); // Default to Korean

  void toggleLanguage() {
    final values = LanguageType.values;
    final nextIndex = (values.indexOf(state) + 1) % values.length;
    state = values[nextIndex];
  }

  void setLanguage(LanguageType type) {
    state = type;
  }
}
