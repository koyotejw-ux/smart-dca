import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

class PriceChart extends StatelessWidget {
  final double initialPrice;
  final double newPrice;
  final double? currentPrice;

  const PriceChart({
    super.key,
    required this.initialPrice,
    required this.newPrice,
    this.currentPrice,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    
    // Determine bounds
    final maxP = [initialPrice, newPrice, currentPrice ?? 0].reduce((a, b) => a > b ? a : b);
    final minP = [initialPrice, newPrice, currentPrice ?? 0].where((p) => p > 0).reduce((a, b) => a < b ? a : b);
    final padding = (maxP - minP) * 0.2;

    return SizedBox(
      height: 200,
      child: LineChart(
        LineChartData(
          gridData: const FlGridData(show: false),
          titlesData: const FlTitlesData(show: false),
          borderData: FlBorderData(show: false),
          minY: minP - padding,
          maxY: maxP + padding,
          lineBarsData: [
            // Target/New Price (Green)
            LineChartBarData(
              spots: [const FlSpot(0, 0), const FlSpot(10, 0)].map((s) => FlSpot(s.x, newPrice)).toList(),
              isCurved: false,
              color: Colors.green.withOpacity(0.5),
              barWidth: 2,
              dotData: const FlDotData(show: false),
              belowBarData: BarAreaData(show: true, color: Colors.green.withOpacity(0.05)),
            ),
            // Initial Price (Red)
            LineChartBarData(
              spots: [const FlSpot(0, 0), const FlSpot(10, 0)].map((s) => FlSpot(s.x, initialPrice)).toList(),
              isCurved: false,
              color: Colors.red.withOpacity(0.3),
              dashArray: [5, 5],
              barWidth: 1,
              dotData: const FlDotData(show: false),
            ),
          ],
          extraLinesData: ExtraLinesData(
            horizontalLines: [
              if (currentPrice != null)
                HorizontalLine(
                  y: currentPrice!,
                  color: theme.colorScheme.primary,
                  strokeWidth: 2,
                  label: HorizontalLineLabel(
                    show: true,
                    alignment: Alignment.topRight,
                    labelResolver: (_) => 'Market',
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
