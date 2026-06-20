class PurchaseBatch {
  final double price;
  final double quantity;

  PurchaseBatch({required this.price, required this.quantity});
}

class CalculationResult {
  final double averagePrice;
  final double totalQuantity;
  final double totalInvestment;
  final double recoveryPercentage;

  CalculationResult({
    required this.averagePrice,
    required this.totalQuantity,
    required this.totalInvestment,
    required this.recoveryPercentage,
  });
}

class CalculatorService {
  static CalculationResult calculateMultiBatch({
    required double initialPrice,
    required double initialQuantity,
    required List<PurchaseBatch> newBatches,
    double feeRate = 0.0,
  }) {
    double totalInvestment = (initialPrice * initialQuantity) * (1 + feeRate);
    double totalQuantity = initialQuantity;

    for (var batch in newBatches) {
      if (batch.price > 0 && batch.quantity > 0) {
        totalInvestment += (batch.price * batch.quantity) * (1 + feeRate);
        totalQuantity += batch.quantity;
      }
    }

    final averagePrice = totalQuantity > 0 ? totalInvestment / totalQuantity : 0.0;
    final recoveryPercentage = initialPrice > 0 
        ? ((initialPrice - averagePrice) / initialPrice) * 100 
        : 0.0;

    return CalculationResult(
      averagePrice: averagePrice,
      totalQuantity: totalQuantity,
      totalInvestment: totalInvestment,
      recoveryPercentage: recoveryPercentage,
    );
  }

  static double calculateRequiredQuantity({
    required double currentPrice,
    required double currentQuantity,
    required double targetPrice,
    required double purchasePrice,
  }) {
    // Formula: (CurrentInv + ReqQty * PurchasePrice) / (CurrentQty + ReqQty) = TargetPrice
    // CurrentInv + ReqQty * PurchasePrice = TargetPrice * CurrentQty + TargetPrice * ReqQty
    // ReqQty * (PurchasePrice - TargetPrice) = TargetPrice * CurrentQty - CurrentInv
    // ReqQty = (TargetPrice * CurrentQty - CurrentInv) / (PurchasePrice - TargetPrice)
    
    final currentInvestment = currentPrice * currentQuantity;
    final numerator = (targetPrice * currentQuantity) - currentInvestment;
    final denominator = purchasePrice - targetPrice;
    
    if (denominator == 0) return 0;
    
    final reqQty = numerator / denominator;
    return reqQty > 0 ? reqQty : 0;
  }
}
