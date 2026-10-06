import 'package:flutter_riverpod/flutter_riverpod.dart';

enum CurrencyType { krw, usd, jpy, eur, vnd, idr }

final currencyProvider = StateNotifierProvider<CurrencyNotifier, CurrencyType>((ref) {
  return CurrencyNotifier();
});

class CurrencyNotifier extends StateNotifier<CurrencyType> {
  CurrencyNotifier() : super(CurrencyType.krw);

  void toggle() {
    final values = CurrencyType.values;
    final nextIndex = (values.indexOf(state) + 1) % values.length;
    state = values[nextIndex];
  }

  void setCurrency(CurrencyType type) {
    state = type;
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
