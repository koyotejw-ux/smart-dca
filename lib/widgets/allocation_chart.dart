import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import '../models/asset_model.dart';

class AllocationChart extends StatelessWidget {
  final List<Asset> assets;

  const AllocationChart({super.key, required this.assets});

  @override
  Widget build(BuildContext context) {
    if (assets.isEmpty) return const SizedBox.shrink();

    final theme = Theme.of(context);
    final Map<String, double> typeTotals = {};
    for (var asset in assets) {
      final value = asset.initialPrice * asset.initialQuantity;
      typeTotals[asset.type] = (typeTotals[asset.type] ?? 0) + value;
    }

    final totalValue = typeTotals.values.fold(0.0, (sum, val) => sum + val);

    return SizedBox(
      height: 200,
      child: PieChart(
        PieChartData(
          pieTouchData: PieTouchData(
            touchCallback: (FlTouchEvent event, pieTouchResponse) {
              // Can add interactivity here if needed
            },
          ),
          sectionsSpace: 4,
          centerSpaceRadius: 60,
          sections: typeTotals.entries.map((entry) {
            final isStock = entry.key == 'stock';
            return PieChartSectionData(
              value: entry.value,
              title: '${(entry.value / totalValue * 100).toStringAsFixed(0)}%',
              color: isStock ? theme.colorScheme.primary : theme.colorScheme.tertiary,
              radius: 20,
              showTitle: true,
              titleStyle: theme.textTheme.labelSmall?.copyWith(color: Colors.white, fontWeight: FontWeight.bold),
            );
          }).toList(),
        ),
      ),
    );
  }
}
