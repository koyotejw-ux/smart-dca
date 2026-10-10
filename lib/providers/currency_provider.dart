import 'dart:ui' as ui;
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../services/storage_service.dart';

enum CurrencyType { krw, usd, jpy, eur, vnd, idr }

final currencyProvider = StateNotifierProvider<CurrencyNotifier, CurrencyType>((ref) {
  return CurrencyNotifier();
});

class CurrencyNotifier extends StateNotifier<CurrencyType> {
  static const String _prefKey = 'selected_currency';

  CurrencyNotifier() : super(_resolveInitialCurrency()) {
    _loadSavedCurrency();
  }

  /// Automatically resolves the user's currency according to system locale and country code
  static CurrencyType _resolveInitialCurrency() {
    try {
      final deviceLocale = ui.PlatformDispatcher.instance.locale;
      final country = (deviceLocale.countryCode ?? '').toUpperCase();
      final lang = deviceLocale.languageCode.toLowerCase();

      // Country code based match
      if (country == 'KR' || lang == 'ko') return CurrencyType.krw;
      if (country == 'JP' || lang == 'ja') return CurrencyType.jpy;
      if (country == 'VN' || lang == 'vi') return CurrencyType.vnd;
      if (country == 'ID' || lang == 'id' || lang == 'in') return CurrencyType.idr;
      if (['FR', 'DE', 'IT', 'ES', 'NL', 'BE', 'PT', 'AT', 'FI', 'IE', 'GR'].contains(country) || lang == 'es') {
        return CurrencyType.eur;
      }
      // Global default is USD
      return CurrencyType.usd;
    } catch (_) {
      return CurrencyType.usd;
    }
  }

  Future<void> _loadSavedCurrency() async {
    try {
      final saved = await StorageService().getSetting(_prefKey);
      if (saved != null && saved.isNotEmpty) {
        state = CurrencyType.values.firstWhere(
          (c) => c.name.toLowerCase() == saved.toLowerCase(),
          orElse: () => state,
        );
      }
    } catch (_) {}
  }

  void toggle() {
    final values = CurrencyType.values;
    final nextIndex = (values.indexOf(state) + 1) % values.length;
    setCurrency(values[nextIndex]);
  }

  void setCurrency(CurrencyType type) {
    state = type;
    StorageService().setSetting(_prefKey, type.name);
  }

  String get symbol {
    switch (state) {
      case CurrencyType.krw:
        return '₩';
      case CurrencyType.usd:
        return '\$';
      case CurrencyType.jpy:
        return '¥';
      case CurrencyType.eur:
        return '€';
      case CurrencyType.vnd:
        return '₫';
      case CurrencyType.idr:
        return 'Rp';
    }
  }

  String get label {
    switch (state) {
      case CurrencyType.krw:
        return 'KRW (₩)';
      case CurrencyType.usd:
        return 'USD (\$)';
      case CurrencyType.jpy:
        return 'JPY (¥)';
      case CurrencyType.eur:
        return 'EUR (€)';
      case CurrencyType.vnd:
        return 'VND (₫)';
      case CurrencyType.idr:
        return 'IDR (Rp)';
    }
  }

  int get decimalDigits {
    switch (state) {
      case CurrencyType.krw:
      case CurrencyType.jpy:
      case CurrencyType.vnd:
      case CurrencyType.idr:
        return 0;
      case CurrencyType.usd:
      case CurrencyType.eur:
        return 2;
    }
  }
}

extension CurrencyTypeExtension on CurrencyType {
  String get symbol {
    switch (this) {
      case CurrencyType.krw:
        return '₩';
      case CurrencyType.usd:
        return '\$';
      case CurrencyType.jpy:
        return '¥';
      case CurrencyType.eur:
        return '€';
      case CurrencyType.vnd:
        return '₫';
      case CurrencyType.idr:
        return 'Rp';
    }
  }

  String get label {
    switch (this) {
      case CurrencyType.krw:
        return 'KRW (₩)';
      case CurrencyType.usd:
        return 'USD (\$)';
      case CurrencyType.jpy:
        return 'JPY (¥)';
      case CurrencyType.eur:
        return 'EUR (€)';
      case CurrencyType.vnd:
        return 'VND (₫)';
      case CurrencyType.idr:
        return 'IDR (Rp)';
    }
  }

  int get decimalDigits {
    switch (this) {
      case CurrencyType.krw:
      case CurrencyType.jpy:
      case CurrencyType.vnd:
      case CurrencyType.idr:
        return 0;
      case CurrencyType.usd:
      case CurrencyType.eur:
        return 2;
    }
  }
}
