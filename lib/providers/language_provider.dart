import 'package:flutter_riverpod/flutter_riverpod.dart';

enum LanguageType { ko, en }

final languageProvider = StateNotifierProvider<LanguageNotifier, LanguageType>((ref) {
  return LanguageNotifier();
});

class LanguageNotifier extends StateNotifier<LanguageType> {
  LanguageNotifier() : super(LanguageType.ko); // Default to Korean

  void toggleLanguage() {
    state = state == LanguageType.ko ? LanguageType.en : LanguageType.ko;
  }

  void setLanguage(LanguageType type) {
    state = type;
  }
}
