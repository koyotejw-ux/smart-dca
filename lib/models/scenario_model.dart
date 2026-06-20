import '../services/calculator_service.dart';

class Scenario {
  final String id;
  final String name;
  final double initialPrice;
  final double initialQuantity;
  final List<PurchaseBatch> batches;
  final DateTime createdAt;

  Scenario({
    required this.id,
    required this.name,
    required this.initialPrice,
    required this.initialQuantity,
    required this.batches,
    required this.createdAt,
  });

  Map<String, dynamic> toJson() => {
    'id': id,
    'name': name,
    'initialPrice': initialPrice,
    'initialQuantity': initialQuantity,
    'batches': batches.map((b) => {'price': b.price, 'quantity': b.quantity}).toList(),
    'createdAt': createdAt.toIso8601String(),
  };
}
