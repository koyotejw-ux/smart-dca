import 'dart:ui' as ui;
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../services/storage_service.dart';

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

  String get code {
    switch (this) {
      case LanguageType.ko:
        return 'ko';
      case LanguageType.en:
        return 'en';
      case LanguageType.ja:
        return 'ja';
      case LanguageType.zh:
        return 'zh';
      case LanguageType.es:
        return 'es';
      case LanguageType.vi:
        return 'vi';
      case LanguageType.id:
        return 'id';
    }
  }

  static LanguageType fromCode(String code) {
    switch (code.toLowerCase()) {
      case 'ko':
        return LanguageType.ko;
      case 'ja':
        return LanguageType.ja;
      case 'zh':
        return LanguageType.zh;
      case 'es':
        return LanguageType.es;
      case 'vi':
        return LanguageType.vi;
      case 'id':
      case 'in':
        return LanguageType.id;
      default:
        return LanguageType.en;
    }
  }
}

final languageProvider = StateNotifierProvider<LanguageNotifier, LanguageType>((ref) {
  return LanguageNotifier();
});

class LanguageNotifier extends StateNotifier<LanguageType> {
  static const String _prefKey = 'selected_language';

  LanguageNotifier() : super(_resolveInitialLanguage()) {
    _loadSavedLanguage();
  }

  /// Automatically resolves the user's system device locale
  static LanguageType _resolveInitialLanguage() {
    try {
      final deviceLocale = ui.PlatformDispatcher.instance.locale;
      final langCode = deviceLocale.languageCode.toLowerCase();
      
      switch (langCode) {
        case 'ko':
          return LanguageType.ko;
        case 'ja':
          return LanguageType.ja;
        case 'zh':
          return LanguageType.zh;
        case 'es':
          return LanguageType.es;
        case 'vi':
          return LanguageType.vi;
        case 'id':
        case 'in': // Some Android versions use 'in' for Indonesian
          return LanguageType.id;
        default:
          return LanguageType.en;
      }
    } catch (_) {
      return LanguageType.ko;
    }
  }

  Future<void> _loadSavedLanguage() async {
    try {
      final savedCode = await StorageService().getSetting(_prefKey);
      if (savedCode != null && savedCode.isNotEmpty) {
        state = LanguageTypeExtension.fromCode(savedCode);
      }
    } catch (_) {}
  }

  void toggleLanguage() {
    final values = LanguageType.values;
    final nextIndex = (values.indexOf(state) + 1) % values.length;
    setLanguage(values[nextIndex]);
  }

  void setLanguage(LanguageType type) {
    state = type;
    StorageService().setSetting(_prefKey, type.code);
  }
}

