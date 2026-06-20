import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../services/market_data_service.dart';

final marketDataServiceProvider = Provider((ref) => MarketDataService());

final priceProvider = FutureProvider.family<MarketPrice, String>((ref, symbol) async {
  final service = ref.watch(marketDataServiceProvider);
  return service.getPrice(symbol);
});
