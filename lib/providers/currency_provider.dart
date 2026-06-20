import 'package:flutter_riverpod/flutter_riverpod.dart';

enum CurrencyType { krw, usd }

final currencyProvider = StateNotifierProvider<CurrencyNotifier, CurrencyType>((ref) {
  return CurrencyNotifier();
});

class CurrencyNotifier extends StateNotifier<CurrencyType> {
  CurrencyNotifier() : super(CurrencyType.krw);

  void toggle() {
    state = state == CurrencyType.krw ? CurrencyType.usd : CurrencyType.krw;
  }

  void setCurrency(CurrencyType type) {
    state = type;
  }

  String get symbol => state == CurrencyType.krw ? '\u20a9' : '\$';
  int get decimalDigits => state == CurrencyType.krw ? 0 : 2;
}
