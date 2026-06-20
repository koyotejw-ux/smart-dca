import 'dart:math';

class MarketPrice {
  final String symbol;
  final double price;
  final double changePercentage;

  MarketPrice({
    required this.symbol,
    required this.price,
    required this.changePercentage,
  });
}

class MarketDataService {
  // Mocking real-time prices for demo purposes.
  // In a real app, this would call Alpha Vantage or Yahoo Finance API.
  Future<MarketPrice> getPrice(String symbol) async {
    await Future.delayed(const Duration(milliseconds: 800));
    
    // Simulate a random price change for the demo
    final random = Random();
    final mockPrice = 50000.0 + random.nextDouble() * 10000;
    final mockChange = -5.0 + random.nextDouble() * 10.0;

    return MarketPrice(
      symbol: symbol,
      price: mockPrice,
      changePercentage: mockChange,
    );
  }
}
