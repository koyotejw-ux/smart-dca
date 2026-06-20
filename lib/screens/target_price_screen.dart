import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../widgets/one_ui_scroll_view.dart';
import '../services/calculator_service.dart';
import '../providers/language_provider.dart';
import '../utils/l10n.dart';

class TargetPriceScreen extends ConsumerStatefulWidget {
  const TargetPriceScreen({super.key});

  @override
  ConsumerState<TargetPriceScreen> createState() => _TargetPriceScreenState();
}

class _TargetPriceScreenState extends ConsumerState<TargetPriceScreen> {
  final _currentPriceController = TextEditingController();
  final _currentQtyController = TextEditingController();
  final _targetPriceController = TextEditingController();
  final _purchasePriceController = TextEditingController();

  double _requiredQty = 0;
  final _currencyFormat = NumberFormat.currency(symbol: '', decimalDigits: 0);

  void _calculate() {
    final cp = double.tryParse(_currentPriceController.text) ?? 0;
    final cq = double.tryParse(_currentQtyController.text) ?? 0;
    final tp = double.tryParse(_targetPriceController.text) ?? 0;
    final pp = double.tryParse(_purchasePriceController.text) ?? 0;

    if (cp > 0 && cq > 0 && tp > 0 && pp > 0) {
      setState(() {
        _requiredQty = CalculatorService.calculateRequiredQuantity(
          currentPrice: cp,
          currentQuantity: cq,
          targetPrice: tp,
          purchasePrice: pp,
        );
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final lang = ref.watch(languageProvider);

    return OneUIScrollView(
      title: L10n.s(lang, 'target_price'),
      children: [
        if (_requiredQty > 0) ...[
          Card(
            color: theme.colorScheme.primaryContainer,
            child: Padding(
              padding: const EdgeInsets.all(24.0),
              child: Column(
                children: [
                  Text(L10n.s(lang, 'required_qty'), style: theme.textTheme.bodyMedium),
                  const SizedBox(height: 8),
                  Text(
                    _requiredQty.toStringAsFixed(2),
                    style: theme.textTheme.headlineLarge?.copyWith(
                      color: theme.colorScheme.onPrimaryContainer,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 16),
                  Text(
                    '${L10n.s(lang, 'total_cost')}: ${_currencyFormat.format(_requiredQty * (double.tryParse(_purchasePriceController.text) ?? 0))}',
                    style: theme.textTheme.bodyLarge,
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 20),
        ],
        _buildInputCard(context, lang),
      ],
    );
  }

  Widget _buildInputCard(BuildContext context, LanguageType lang) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(L10n.s(lang, 'target_settings'), style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 16),
            _buildTextField(_currentPriceController, L10n.s(lang, 'avg_price'), '0'),
            const SizedBox(height: 12),
            _buildTextField(_currentQtyController, L10n.s(lang, 'quantity'), '0'),
            const SizedBox(height: 16),
            const Divider(),
            const SizedBox(height: 16),
            _buildTextField(_targetPriceController, L10n.s(lang, 'target_avg_price'), '0'),
            const SizedBox(height: 12),
            _buildTextField(_purchasePriceController, L10n.s(lang, 'purchase_price'), '0'),
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              child: FilledButton(
                onPressed: _calculate,
                style: FilledButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                ),
                child: Text(L10n.s(lang, 'find_amount')),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildTextField(TextEditingController controller, String label, String hint) {
    return TextField(
      controller: controller,
      keyboardType: TextInputType.number,
      decoration: InputDecoration(
        labelText: label,
        hintText: hint,
        filled: true,
        fillColor: Theme.of(context).colorScheme.surfaceVariant.withOpacity(0.3),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(16),
          borderSide: BorderSide.none,
        ),
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
      ),
      onChanged: (_) => _calculate(),
    );
  }
}
