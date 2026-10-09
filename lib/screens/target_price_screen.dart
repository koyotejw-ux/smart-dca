import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import 'package:google_fonts/google_fonts.dart';

import '../services/calculator_service.dart';
import '../services/admob_service.dart';
import '../providers/language_provider.dart';
import '../providers/currency_provider.dart';
import '../theme/t_membership_colors.dart';
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

  @override
  void initState() {
    super.initState();
    _currentPriceController.addListener(_calculate);
    _currentQtyController.addListener(_calculate);
    _targetPriceController.addListener(_calculate);
    _purchasePriceController.addListener(_calculate);
  }

  @override
  void dispose() {
    _currentPriceController.dispose();
    _currentQtyController.dispose();
    _targetPriceController.dispose();
    _purchasePriceController.dispose();
    super.dispose();
  }

  static int _calcCounter = 0;

  void _calculate() {
    final cp = double.tryParse(_currentPriceController.text.replaceAll(',', '')) ?? 0;
    final cq = double.tryParse(_currentQtyController.text.replaceAll(',', '')) ?? 0;
    final tp = double.tryParse(_targetPriceController.text.replaceAll(',', '')) ?? 0;
    final pp = double.tryParse(_purchasePriceController.text.replaceAll(',', '')) ?? 0;

    if (cp > 0 && cq > 0 && tp > 0 && pp > 0) {
      HapticFeedback.heavyImpact();
      setState(() {
        _requiredQty = CalculatorService.calculateRequiredQuantity(
          currentPrice: cp,
          currentQuantity: cq,
          targetPrice: tp,
          purchasePrice: pp,
        );
      });
      _calcCounter++;
      if (_calcCounter % 2 == 0) {
        AdmobService.showInterstitial(
          onDismissed: () {},
          onFailed: (err) {},
        );
      }
    } else {
      HapticFeedback.mediumImpact();
      if (_requiredQty != 0) setState(() => _requiredQty = 0);
      if (mounted) {
        final lang = ref.read(languageProvider);
        ScaffoldMessenger.of(context).hideCurrentSnackBar();
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Row(
              children: [
                const Icon(Icons.info_outline_rounded, color: Colors.white, size: 20),
                const SizedBox(width: 10),
                Expanded(child: Text(L10n.s(lang, 'input_required_msg'))),
              ],
            ),
            backgroundColor: TMembershipColors.accentOrange,
            behavior: SnackBarBehavior.floating,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(languageProvider);
    final currency = ref.watch(currencyProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    final bgColor = isDark ? TMembershipColors.darkBg : TMembershipColors.lightBg;
    final cardBg = isDark ? TMembershipColors.darkSurface : TMembershipColors.lightSurface;
    final cardBorder = isDark ? TMembershipColors.darkCardBorder : TMembershipColors.lightCardBorder;
    final textPrimary = isDark ? TMembershipColors.darkTextPrimary : TMembershipColors.lightTextPrimary;
    final textSecondary = isDark ? TMembershipColors.darkTextSecondary : TMembershipColors.lightTextSecondary;
    final currSymbol = currency == CurrencyType.krw ? '원' : '\$';

    final pp = double.tryParse(_purchasePriceController.text.replaceAll(',', '')) ?? 0;
    final totalCost = _requiredQty > 0 ? _requiredQty * pp : 0;

    return Scaffold(
      backgroundColor: bgColor,
      appBar: AppBar(
        backgroundColor: bgColor,
        elevation: 0,
        leading: IconButton(
          icon: Icon(Icons.arrow_back_ios_new_rounded, color: textPrimary, size: 20),
          onPressed: () => Navigator.pop(context),
        ),
        title: Text(
          L10n.s(lang, 'target_price'),
          style: GoogleFonts.inter(
            color: textPrimary,
            fontWeight: FontWeight.w900,
            fontSize: 18,
            letterSpacing: -0.4,
          ),
        ),
      ),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 800),
          child: ListView(
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
            children: [
              // Result Card (T-Membership style)
              if (_requiredQty > 0)
                Container(
                  margin: const EdgeInsets.only(bottom: 20),
                  padding: const EdgeInsets.all(24),
                  decoration: BoxDecoration(
                    gradient: TMembershipColors.primaryGradient,
                    borderRadius: BorderRadius.circular(24),
                    boxShadow: TMembershipColors.colorfulGlow(TMembershipColors.primaryBlue, opacity: 0.35),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(
                            L10n.s(lang, 'required_qty').toUpperCase(),
                            style: const TextStyle(
                              color: Colors.white70,
                              fontWeight: FontWeight.w800,
                              fontSize: 11,
                              letterSpacing: 1.2,
                            ),
                          ),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                            decoration: BoxDecoration(
                              color: Colors.white.withOpacity(0.2),
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: const Text("TARGET ACHIEVED", style: TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold)),
                          ),
                        ],
                      ),
                      const SizedBox(height: 12),
                      Row(
                        crossAxisAlignment: CrossAxisAlignment.baseline,
                        textBaseline: TextBaseline.alphabetic,
                        children: [
                          Text(
                            _requiredQty.toStringAsFixed(0),
                            style: GoogleFonts.inter(
                              color: Colors.white,
                              fontWeight: FontWeight.w900,
                              fontSize: 36,
                              letterSpacing: -0.5,
                            ),
                          ),
                          const SizedBox(width: 6),
                          const Text(
                            "주 필요",
                            style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 18),
                          ),
                        ],
                      ),
                      const SizedBox(height: 14),
                      const Divider(color: Colors.white24, height: 1),
                      const SizedBox(height: 12),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(
                            L10n.s(lang, 'total_cost'),
                            style: const TextStyle(color: Colors.white70, fontSize: 13, fontWeight: FontWeight.w600),
                          ),
                          Text(
                            "${_currencyFormat.format(totalCost)}$currSymbol",
                            style: GoogleFonts.inter(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 16),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),

              // Inputs Card
              Container(
                padding: const EdgeInsets.all(22),
                decoration: BoxDecoration(
                  color: cardBg,
                  borderRadius: BorderRadius.circular(24),
                  border: Border.all(color: cardBorder, width: 1.2),
                  boxShadow: isDark ? [] : TMembershipColors.softShadow(blur: 14, dy: 4),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Container(
                          padding: const EdgeInsets.all(8),
                          decoration: BoxDecoration(
                            color: TMembershipColors.primaryBlue.withOpacity(0.1),
                            borderRadius: BorderRadius.circular(10),
                          ),
                          child: const Icon(Icons.track_changes_rounded, color: TMembershipColors.primaryBlue, size: 20),
                        ),
                        const SizedBox(width: 10),
                        Text(
                          L10n.s(lang, 'target_settings'),
                          style: GoogleFonts.inter(fontWeight: FontWeight.w900, fontSize: 16, color: textPrimary),
                        ),
                      ],
                    ),
                    const SizedBox(height: 20),
                    Text(
                      lang == LanguageType.ko ? "현재 보유 정보" : "Currently Held",
                      style: TextStyle(fontSize: 13, fontWeight: FontWeight.w800, color: textSecondary),
                    ),
                    const SizedBox(height: 10),
                    LayoutBuilder(
                      builder: (context, constraints) {
                        final isNarrow = constraints.maxWidth < 340;
                        final priceField = _buildInputField(_currentPriceController, L10n.s(lang, 'avg_price'), '예: 75,000', isDark);
                        final qtyField = _buildInputField(_currentQtyController, L10n.s(lang, 'quantity'), '예: 100', isDark);
                        if (isNarrow) {
                          return Column(children: [priceField, const SizedBox(height: 12), qtyField]);
                        }
                        return Row(
                          children: [
                            Expanded(child: priceField),
                            const SizedBox(width: 14),
                            Expanded(child: qtyField),
                          ],
                        );
                      },
                    ),
                    const SizedBox(height: 22),
                    Divider(height: 1, color: isDark ? TMembershipColors.darkDivider : TMembershipColors.lightDivider),
                    const SizedBox(height: 22),
                    Text(
                      lang == LanguageType.ko ? "목표 및 추가 매수 계획" : "Target & Buy Plan",
                      style: TextStyle(fontSize: 13, fontWeight: FontWeight.w800, color: textSecondary),
                    ),
                    const SizedBox(height: 10),
                    LayoutBuilder(
                      builder: (context, constraints) {
                        final isNarrow = constraints.maxWidth < 340;
                        final targetField = _buildInputField(_targetPriceController, L10n.s(lang, 'target_avg_price'), '예: 70,000', isDark);
                        final purchaseField = _buildInputField(_purchasePriceController, L10n.s(lang, 'purchase_price'), '예: 65,000', isDark);
                        if (isNarrow) {
                          return Column(children: [targetField, const SizedBox(height: 12), purchaseField]);
                        }
                        return Row(
                          children: [
                            Expanded(child: targetField),
                            const SizedBox(width: 14),
                            Expanded(child: purchaseField),
                          ],
                        );
                      },
                    ),
                    const SizedBox(height: 26),
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton(
                        onPressed: () {
                          HapticFeedback.mediumImpact();
                          _calculate();
                        },
                        style: ElevatedButton.styleFrom(
                          backgroundColor: TMembershipColors.primaryBlue,
                          padding: const EdgeInsets.symmetric(vertical: 18),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                          elevation: 4,
                        ),
                        child: FittedBox(
                          fit: BoxFit.scaleDown,
                          child: Text(
                            L10n.s(lang, 'find_amount'),
                            maxLines: 1,
                            style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 16),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 36),
            ],
          ),
        ),
      ),
      bottomNavigationBar: const SafeArea(
        child: SizedBox(
          height: 50,
          child: AdmobBannerWidget(),
        ),
      ),
    );
  }

  Widget _buildInputField(TextEditingController controller, String label, String hint, bool isDark) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(bottom: 8),
          child: Text(
            label,
            style: TextStyle(
              fontSize: 12.5,
              fontWeight: FontWeight.w700,
              color: isDark ? Colors.white70 : Colors.black87,
            ),
          ),
        ),
        TextField(
          controller: controller,
          keyboardType: TextInputType.number,
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w800,
            color: isDark ? Colors.white : Colors.black87,
          ),
          decoration: InputDecoration(
            hintText: hint,
            hintStyle: TextStyle(color: isDark ? Colors.white24 : Colors.black26, fontSize: 14),
            filled: true,
            fillColor: isDark ? const Color(0xFF131923) : const Color(0xFFF8FAFD),
            contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(16),
              borderSide: BorderSide(
                color: isDark ? TMembershipColors.darkCardBorder : const Color(0xFFE4E9F2),
                width: 1.2,
              ),
            ),
            enabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(16),
              borderSide: BorderSide(
                color: isDark ? TMembershipColors.darkCardBorder : const Color(0xFFE4E9F2),
                width: 1.2,
              ),
            ),
            focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(16),
              borderSide: const BorderSide(
                color: TMembershipColors.primaryBlue,
                width: 1.6,
              ),
            ),
          ),
        ),
      ],
    );
  }
}
