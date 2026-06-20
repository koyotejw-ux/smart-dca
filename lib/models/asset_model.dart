class Asset {
  final int? id;
  final String name;
  final String symbol; // Added symbol (e.g. BTC, AAPL, 005930)
  final double initialPrice;
  final double initialQuantity;
  final String type; // 'stock' or 'crypto'

  Asset({
    this.id,
    required this.name,
    required this.symbol,
    required this.initialPrice,
    required this.initialQuantity,
    required this.type,
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'name': name,
      'symbol': symbol,
      'initialPrice': initialPrice,
      'initialQuantity': initialQuantity,
      'type': type,
    };
  }

  factory Asset.fromMap(Map<String, dynamic> map) {
    return Asset(
      id: map['id'],
      name: map['name'],
      symbol: map['symbol'] ?? '',
      initialPrice: map['initialPrice'],
      initialQuantity: map['initialQuantity'],
      type: map['type'],
    );
  }
}
