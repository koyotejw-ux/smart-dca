import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import 'package:uuid/uuid.dart';

import '../services/calculator_service.dart';
import '../providers/language_provider.dart';
import '../utils/l10n.dart';
import '../providers/asset_provider.dart';
import '../models/asset_model.dart';
import '../models/scenario_model.dart';
import '../providers/scenario_provider.dart';
import '../theme/t_membership_colors.dart';
import '../services/admob_service.dart';
import '../providers/currency_provider.dart';

class SimulatorScreen extends ConsumerStatefulWidget {
  final Scenario? initialScenario;
  const SimulatorScreen({super.key, this.initialScenario});

  @override
  ConsumerState<SimulatorScreen> createState() => _SimulatorScreenState();
}

class _SimulatorScreenState extends ConsumerState<SimulatorScreen> {
  final _assetNameController = TextEditingController(text: '보유 종목');
  final _assetSymbolController = TextEditingController(text: 'STOCK');
  final _initialPriceController = TextEditingController();
  final _initialQtyController = TextEditingController();

  // Scenario A
  final List<TextEditingController> _priceControllersA = [TextEditingController()];
  final List<TextEditingController> _qtyControllersA = [TextEditingController()];

  // Scenario B (Comparison)
  final List<TextEditingController> _priceControllersB = [TextEditingController()];
  final List<TextEditingController> _qtyControllersB = [TextEditingController()];

  final TextEditingController _targetPriceController = TextEditingController();
  final TextEditingController _purchasePriceController = TextEditingController();

  bool _isCompareMode = false;
  bool _isTargetMode = false;
  final bool _isFeeEnabled = false;
  double _simulatedPriceFactor = 1.0;
  CalculationResult? _resultA;
  CalculationResult? _resultB;
  double? _requiredQty;
  final _currencyFormat = NumberFormat.currency(symbol: '', decimalDigits: 0);

  @override
  void initState() {
    super.initState();
    _initialPriceController.addListener(_calculate);
    _initialQtyController.addListener(_calculate);
    _targetPriceController.addListener(_calculate);
    _purchasePriceController.addListener(_calculate);
    _priceControllersA[0].addListener(_calculate);
    _qtyControllersA[0].addListener(_calculate);
    _priceControllersB[0].addListener(_calculate);
    _qtyControllersB[0].addListener(_calculate);

    if (widget.initialScenario != null) {
      final s = widget.initialScenario!;
      _initialPriceController.text = s.initialPrice.toStringAsFixed(0);
      _initialQtyController.text = s.initialQuantity.toStringAsFixed(0);

      _priceControllersA[0].text = '';
      _qtyControllersA[0].text = '';

      for (int i = 0; i < s.batches.length; i++) {
        if (i == 0) {
          _priceControllersA[0].text = s.batches[i].price.toStringAsFixed(0);
          _qtyControllersA[0].text = s.batches[i].quantity.toStringAsFixed(0);
        } else {
          final p = TextEditingController(text: s.batches[i].price.toStringAsFixed(0));
          final q = TextEditingController(text: s.batches[i].quantity.toStringAsFixed(0));
          p.addListener(_calculate);
          q.addListener(_calculate);
          _priceControllersA.add(p);
          _qtyControllersA.add(q);
        }
      }
      _calculate();
    }
  }

  void _addBatch(bool isB) {
    setState(() {
      final p = TextEditingController();
      final q = TextEditingController();
      p.addListener(_calculate);
      q.addListener(_calculate);
      if (isB) {
        _priceControllersB.add(p);
        _qtyControllersB.add(q);
      } else {
        _priceControllersA.add(p);
        _qtyControllersA.add(q);
      }
    });
    HapticFeedback.lightImpact();
  }

  void _removeBatch(int index, bool isB) {
    final prices = isB ? _priceControllersB : _priceControllersA;
    final qtys = isB ? _qtyControllersB : _qtyControllersA;
    if (prices.length > 1) {
      setState(() {
        prices.removeAt(index);
        qtys.removeAt(index);
      });
      _calculate();
    }
  }

  double _parseVal(String text) {
    return double.tryParse(text.replaceAll(',', '')) ?? 0;
  }

  void _calculate() {
    final ip = _parseVal(_initialPriceController.text);
    final iq = _parseVal(_initialQtyController.text);

    if (ip <= 0 || iq <= 0) return;

    final basePrice = ip * _simulatedPriceFactor;

    if (_isTargetMode) {
      final tp = _targetPriceController.text.isEmpty ? 0.0 : _parseVal(_targetPriceController.text);
      final pp = _purchasePriceController.text.isEmpty ? basePrice : _parseVal(_purchasePriceController.text);
      if (tp > 0 && pp > 0) {
        final req = CalculatorService.calculateRequiredQuantity(
          currentPrice: basePrice,
          currentQuantity: iq,
          targetPrice: tp,
          purchasePrice: pp,
        );
        setState(() {
          _requiredQty = req;
          _resultA = CalculatorService.calculateMultiBatch(
            initialPrice: basePrice,
            initialQuantity: iq,
            newBatches: [PurchaseBatch(price: pp, quantity: req)],
            feeRate: _isFeeEnabled ? 0.00015 : 0.0,
          );
        });
        return;
      }
    }

    _resultA = _calcBatch(basePrice, iq, _priceControllersA, _qtyControllersA);
    if (_isCompareMode) {
      _resultB = _calcBatch(basePrice, iq, _priceControllersB, _qtyControllersB);
    }
    setState(() {});
  }

  void _adjustPrice(TextEditingController controller, double percent) {
    final val = _parseVal(controller.text);
    double newVal;
    if (val <= 0) {
      newVal = percent > 0 ? 10000 : 0;
    } else {
      newVal = (val * (1 + percent)).roundToDouble();
      if (newVal == val) {
        newVal = percent > 0 ? val + 100 : val - 100;
      }
    }
    newVal = newVal.clamp(0, double.infinity);
    controller.text = _currencyFormat.format(newVal).trim();
    _calculate();
    HapticFeedback.selectionClick();
  }

  void _adjustQty(TextEditingController controller, double amount) {
    final val = _parseVal(controller.text);
    double newVal;
    if (val <= 0 && amount > 0) {
      newVal = amount;
    } else {
      newVal = (val + amount).clamp(0, double.infinity);
    }
    controller.text = _currencyFormat.format(newVal).trim();
    _calculate();
    HapticFeedback.selectionClick();
  }

  CalculationResult? _calcBatch(double ip, double iq, List<TextEditingController> prices, List<TextEditingController> qtys) {
    final List<PurchaseBatch> batches = [];
    for (int i = 0; i < prices.length; i++) {
      final pp = _parseVal(prices[i].text);
      final pq = _parseVal(qtys[i].text);
      if (pp > 0 && pq > 0) {
        batches.add(PurchaseBatch(price: pp, quantity: pq));
      }
    }
    return CalculatorService.calculateMultiBatch(
      initialPrice: ip,
      initialQuantity: iq,
      newBatches: batches,
      feeRate: _isFeeEnabled ? 0.00015 : 0.0,
    );
  }

  List<PurchaseBatch> _calcBatches(bool isB) {
    final List<PurchaseBatch> batches = [];
    final prices = isB ? _priceControllersB : _priceControllersA;
    final qtys = isB ? _qtyControllersB : _qtyControllersA;
    for (int i = 0; i < prices.length; i++) {
      final pp = _parseVal(prices[i].text);
      final pq = _parseVal(qtys[i].text);
      if (pp > 0 && pq > 0) {
        batches.add(PurchaseBatch(price: pp, quantity: pq));
      }
    }
    return batches;
  }

  Future<void> _saveToPortfolio() async {
    HapticFeedback.mediumImpact();
    final lang = ref.read(languageProvider);
    final ip = _parseVal(_initialPriceController.text);
    final iq = _parseVal(_initialQtyController.text);

    if (ip <= 0 || iq <= 0) {
      if (mounted) {
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
      return;
    }

    AdmobService.showInterstitial(
      onDismissed: () async {
        await ref.read(assetsProvider.notifier).addAsset(Asset(
          name: _assetNameController.text.trim().isEmpty ? 'Asset' : _assetNameController.text.trim(),
          symbol: _assetSymbolController.text.trim().isEmpty ? 'STOCK' : _assetSymbolController.text.trim(),
          initialPrice: ip,
          initialQuantity: iq,
          type: 'stock',
        ));
        if (mounted) {
          HapticFeedback.heavyImpact();
          ScaffoldMessenger.of(context).hideCurrentSnackBar();
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Row(
                children: [
                  const Icon(Icons.check_circle_rounded, color: Colors.white, size: 20),
                  const SizedBox(width: 10),
                  Expanded(child: Text(L10n.s(lang, 'save_to_portfolio_success'))),
                ],
              ),
              backgroundColor: TMembershipColors.primaryBlue,
              behavior: SnackBarBehavior.floating,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            ),
          );
        }
      },
    );
  }

  Future<void> _saveScenario() async {
    HapticFeedback.mediumImpact();
    final lang = ref.read(languageProvider);
    final ip = _parseVal(_initialPriceController.text);
    final iq = _parseVal(_initialQtyController.text);

    if (ip <= 0 || iq <= 0) {
      if (mounted) {
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
      return;
    }

    final batches = _calcBatches(false);
    final scenario = Scenario(
      id: const Uuid().v4(),
      name: "${L10n.s(lang, 'default_scenario_name')} ${DateFormat('MM.dd HH:mm').format(DateTime.now())}",
      initialPrice: ip,
      initialQuantity: iq,
      batches: batches,
      createdAt: DateTime.now(),
    );

    await ref.read(scenarioProvider.notifier).addScenario(scenario);

    AdmobService.showInterstitial(
      onDismissed: () {},
      onFailed: (err) {},
    );

    if (mounted) {
      HapticFeedback.heavyImpact();
      ScaffoldMessenger.of(context).hideCurrentSnackBar();
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Row(
            children: [
              const Icon(Icons.bookmark_added_rounded, color: Colors.white, size: 20),
              const SizedBox(width: 10),
              Expanded(child: Text(L10n.s(lang, 'scenario_saved_msg'))),
            ],
          ),
          backgroundColor: const Color(0xFF7928CA),
          behavior: SnackBarBehavior.floating,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        ),
      );
    }
  }

  void _resetInputs() {
    HapticFeedback.mediumImpact();
    final lang = ref.read(languageProvider);
    setState(() {
      _initialPriceController.clear();
      _initialQtyController.clear();
      _targetPriceController.clear();
      _purchasePriceController.clear();
      for (var c in _priceControllersA) {
        c.clear();
      }
      for (var c in _qtyControllersA) {
        c.clear();
      }
      _resultA = null;
      _resultB = null;
      _requiredQty = null;
    });

    if (mounted) {
      ScaffoldMessenger.of(context).hideCurrentSnackBar();
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Row(
            children: [
              const Icon(Icons.refresh_rounded, color: Colors.white, size: 20),
              const SizedBox(width: 10),
              Expanded(child: Text(L10n.s(lang, 'reset_done_msg'))),
            ],
          ),
          backgroundColor: TMembershipColors.accentOrange,
          behavior: SnackBarBehavior.floating,
          duration: const Duration(seconds: 2),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final lang = ref.watch(languageProvider);
    final width = MediaQuery.of(context).size.width;

    final bgColor = isDark ? TMembershipColors.darkBg : TMembershipColors.lightBg;

    return Scaffold(
      backgroundColor: bgColor,
      appBar: PreferredSize(
        preferredSize: const Size.fromHeight(64),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: _buildHeader(context, isDark, lang),
          ),
        ),
      ),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 960),
          child: ListView(
            padding: const EdgeInsets.symmetric(horizontal: 20),
            children: [
              const SizedBox(height: 8),
              _buildResultCard(context, isDark, lang)
                  .animate().fadeIn(duration: 400.ms).slideY(begin: 0.08, end: 0),
              const SizedBox(height: 16),
              _buildModeSelector(context, isDark, lang),
              const SizedBox(height: 16),
              _buildInitialStepCard(context, isDark, lang)
                  .animate().fadeIn(duration: 450.ms, delay: 50.ms).slideY(begin: 0.08, end: 0),
              const SizedBox(height: 16),
              if (_isTargetMode)
                _buildTargetCalculatorCard(context, isDark, lang)
              else if (_isCompareMode && width > 768)
                Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Expanded(child: _buildPurchasePlanCard(context, isDark, lang, false)),
                    const SizedBox(width: 16),
                    Expanded(child: _buildPurchasePlanCard(context, isDark, lang, true)),
                  ],
                )
              else ...[
                _buildPurchasePlanCard(context, isDark, lang, false),
                if (_isCompareMode) ...[
                  const SizedBox(height: 16),
                  _buildPurchasePlanCard(context, isDark, lang, true),
                ],
              ],
              const SizedBox(height: 16),
              _buildSensitivityCard(context, isDark, lang),
              const SizedBox(height: 20),
              _buildBottomActionButtons(context, isDark, lang),
              SizedBox(height: 36 + MediaQuery.paddingOf(context).bottom),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildHeader(BuildContext context, bool isDark, LanguageType lang) {
    final titleColor = isDark ? TMembershipColors.darkTextPrimary : TMembershipColors.lightTextPrimary;

    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Expanded(
          child: Row(
            children: [
              Material(
                color: Colors.transparent,
                child: InkWell(
                  onTap: () => Navigator.pop(context),
                  borderRadius: BorderRadius.circular(12),
                  child: Container(
                    width: 40,
                    height: 40,
                    decoration: BoxDecoration(
                      color: isDark ? TMembershipColors.darkSurface : Colors.white,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(
                        color: isDark ? TMembershipColors.darkCardBorder : TMembershipColors.lightCardBorder,
                        width: 1.2,
                      ),
                      boxShadow: isDark ? [] : TMembershipColors.softShadow(blur: 6, dy: 2),
                    ),
                    child: Center(
                      child: Icon(Icons.arrow_back_ios_new_rounded, color: titleColor, size: 18),
                    ),
                  ),
                ),
              ),
              const SizedBox(width: 10),
              Flexible(
                child: FittedBox(
                  fit: BoxFit.scaleDown,
                  alignment: Alignment.centerLeft,
                  child: Text(
                    L10n.s(lang, 'sim_title'),
                    style: GoogleFonts.inter(
                      color: titleColor,
                      fontWeight: FontWeight.w900,
                      fontSize: 18,
                      letterSpacing: -0.4,
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
        const SizedBox(width: 8),
        Row(
          children: [
            Material(
              color: Colors.transparent,
              child: InkWell(
                onTap: _resetInputs,
                borderRadius: BorderRadius.circular(10),
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 7),
                  decoration: BoxDecoration(
                    color: TMembershipColors.accentOrange.withOpacity(0.12),
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(color: TMembershipColors.accentOrange.withOpacity(0.3), width: 1),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Icon(Icons.refresh_rounded, size: 16, color: TMembershipColors.accentOrange),
                      const SizedBox(width: 4),
                      Text(
                        L10n.s(lang, 'reset'),
                        style: const TextStyle(
                          color: TMembershipColors.accentOrange,
                          fontWeight: FontWeight.w800,
                          fontSize: 12,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ],
    );
  }

  /// Top Highlight: Smart Vivid Result Card
  Widget _buildResultCard(BuildContext context, bool isDark, LanguageType lang) {
    final currency = ref.watch(currencyProvider);
    final val = _resultA?.averagePrice ?? 0;
    final recovery = _resultA?.recoveryPercentage ?? 0;
    final totalInvested = _resultA?.totalInvestment ?? 0;
    final totalQty = _resultA?.totalQuantity ?? 0;

    final currFormatter = NumberFormat.currency(
      symbol: currency.symbol,
      decimalDigits: currency.decimalDigits,
    );

    return Container(
      width: double.infinity,
      decoration: BoxDecoration(
        gradient: TMembershipColors.primaryGradient,
        borderRadius: BorderRadius.circular(28),
        boxShadow: TMembershipColors.colorfulGlow(TMembershipColors.primaryBlue, opacity: 0.35),
      ),
      child: Stack(
        children: [
          Positioned(
            right: -20,
            top: -20,
            child: Container(
              width: 140,
              height: 140,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: Colors.white.withOpacity(0.08),
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Flexible(
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                        decoration: BoxDecoration(
                          color: Colors.white.withOpacity(0.2),
                          borderRadius: BorderRadius.circular(20),
                        ),
                        child: FittedBox(
                          fit: BoxFit.scaleDown,
                          child: Text(
                            lang == LanguageType.ko ? "계산 결과 리포트" : "RESULT REPORT",
                            style: const TextStyle(
                              color: Colors.white,
                              fontWeight: FontWeight.w900,
                              fontSize: 10,
                              letterSpacing: 0.8,
                            ),
                          ),
                        ),
                      ),
                    ),
                    if (_resultA != null) ...[
                      const SizedBox(width: 8),
                      Flexible(
                        child: Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                          decoration: BoxDecoration(
                            color: Colors.black.withOpacity(0.25),
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: FittedBox(
                            fit: BoxFit.scaleDown,
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Icon(
                                  recovery <= 0 ? Icons.arrow_downward_rounded : Icons.arrow_upward_rounded,
                                  color: recovery <= 0 ? const Color(0xFF69F0AE) : const Color(0xFFFF8A80),
                                  size: 13,
                                ),
                                const SizedBox(width: 4),
                                Text(
                                  "${lang == LanguageType.ko ? '평단가 ' : 'Cost '}${recovery.abs().toStringAsFixed(1)}% ${recovery <= 0 ? (lang == LanguageType.ko ? '낮춤' : 'Lowered') : (lang == LanguageType.ko ? '상승' : 'Raised')}",
                                  style: TextStyle(
                                    color: recovery <= 0 ? const Color(0xFF69F0AE) : const Color(0xFFFF8A80),
                                    fontWeight: FontWeight.w900,
                                    fontSize: 11,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                      ),
                    ],
                  ],
                ),
                const SizedBox(height: 16),
                Text(
                  L10n.s(lang, 'new_avg_price'),
                  style: TextStyle(
                    color: Colors.white.withOpacity(0.8),
                    fontSize: 13,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                const SizedBox(height: 4),
                FittedBox(
                  child: Text(
                    val > 0 ? currFormatter.format(val) : "${currency.symbol}0",
                    style: GoogleFonts.inter(
                      color: Colors.white,
                      fontWeight: FontWeight.w900,
                      fontSize: 48,
                      letterSpacing: -1.5,
                    ),
                  ),
                ),
                const SizedBox(height: 16),
                // Compact specs strip
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                  decoration: BoxDecoration(
                    color: Colors.black.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: FittedBox(
                    fit: BoxFit.scaleDown,
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        Column(
                          children: [
                            Text(L10n.s(lang, 'total_qty'), style: const TextStyle(color: Colors.white70, fontSize: 11)),
                            const SizedBox(height: 4),
                            Text(
                              "${totalQty.toStringAsFixed(0)} ${L10n.s(lang, 'unit_share')}",
                              style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 14),
                            ),
                          ],
                        ),
                        const SizedBox(width: 18),
                        Container(height: 22, width: 1, color: Colors.white24),
                        const SizedBox(width: 18),
                        Column(
                          children: [
                            Text(L10n.s(lang, 'total_investment'), style: const TextStyle(color: Colors.white70, fontSize: 11)),
                            const SizedBox(height: 4),
                            Text(
                              currFormatter.format(totalInvested),
                              style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 14),
                            ),
                          ],
                        ),
                        if (_isCompareMode && _resultB != null) ...[
                          const SizedBox(width: 18),
                          Container(height: 22, width: 1, color: Colors.white24),
                          const SizedBox(width: 18),
                          Column(
                            children: [
                              Text(lang == LanguageType.ko ? "시나리오 B" : "Scenario B", style: const TextStyle(color: Color(0xFFFFB74D), fontSize: 11, fontWeight: FontWeight.bold)),
                              const SizedBox(height: 4),
                              Text(
                                currFormatter.format(_resultB!.averagePrice),
                                style: const TextStyle(color: Color(0xFFFFB74D), fontWeight: FontWeight.w900, fontSize: 14),
                              ),
                            ],
                          ),
                        ],
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  /// Segmented Tab Switcher
  Widget _buildModeSelector(BuildContext context, bool isDark, LanguageType lang) {
    final cardBg = isDark ? TMembershipColors.darkSurface : TMembershipColors.lightSurface;
    final cardBorder = isDark ? TMembershipColors.darkCardBorder : TMembershipColors.lightCardBorder;

    return Container(
      padding: const EdgeInsets.all(4),
      decoration: BoxDecoration(
        color: cardBg,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: cardBorder, width: 1.2),
        boxShadow: isDark ? [] : TMembershipColors.softShadow(blur: 8, dy: 2),
      ),
      child: Row(
        children: [
          Expanded(
            child: _buildModeTab(
              label: L10n.s(lang, 'simulator'),
              isSelected: !_isTargetMode && !_isCompareMode,
              onTap: () => setState(() {
                _isTargetMode = false;
                _isCompareMode = false;
                _calculate();
              }),
            ),
          ),
          Expanded(
            child: _buildModeTab(
              label: L10n.s(lang, 'scenario_compare'),
              isSelected: _isCompareMode,
              onTap: () => setState(() {
                _isCompareMode = !_isCompareMode;
                if (_isCompareMode) _isTargetMode = false;
                _calculate();
              }),
            ),
          ),
          Expanded(
            child: _buildModeTab(
              label: L10n.s(lang, 'target_price'),
              isSelected: _isTargetMode,
              onTap: () => setState(() {
                _isTargetMode = !_isTargetMode;
                if (_isTargetMode) _isCompareMode = false;
                _calculate();
              }),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildModeTab({required String label, required bool isSelected, required VoidCallback onTap}) {
    return InkWell(
      onTap: () {
        HapticFeedback.selectionClick();
        onTap();
      },
      borderRadius: BorderRadius.circular(12),
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 10),
        decoration: BoxDecoration(
          color: isSelected ? TMembershipColors.primaryBlue : Colors.transparent,
          borderRadius: BorderRadius.circular(12),
        ),
        child: Center(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 4),
            child: FittedBox(
              fit: BoxFit.scaleDown,
              child: Text(
                label,
                style: GoogleFonts.inter(
                  color: isSelected ? Colors.white : (Theme.of(context).brightness == Brightness.dark ? Colors.white60 : TMembershipColors.lightTextSecondary),
                  fontWeight: isSelected ? FontWeight.w800 : FontWeight.w600,
                  fontSize: 12,
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }

  /// Step 1: Currently Held Asset
  Widget _buildInitialStepCard(BuildContext context, bool isDark, LanguageType lang) {
    final currency = ref.watch(currencyProvider);
    final cardBg = isDark ? TMembershipColors.darkSurface : TMembershipColors.lightSurface;
    final cardBorder = isDark ? TMembershipColors.darkCardBorder : TMembershipColors.lightCardBorder;
    final titleColor = isDark ? TMembershipColors.darkTextPrimary : TMembershipColors.lightTextPrimary;

    return Container(
      padding: const EdgeInsets.all(20),
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
                width: 26,
                height: 26,
                decoration: const BoxDecoration(
                  color: TMembershipColors.primaryBlue,
                  shape: BoxShape.circle,
                ),
                child: const Center(
                  child: Text("1", style: TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 13)),
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: FittedBox(
                  fit: BoxFit.scaleDown,
                  alignment: Alignment.centerLeft,
                  child: Text(
                    L10n.s(lang, 'step_1_title'),
                    style: GoogleFonts.inter(
                      color: titleColor,
                      fontWeight: FontWeight.w800,
                      fontSize: 15,
                    ),
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 18),
          LayoutBuilder(
            builder: (context, constraints) {
              final isNarrow = constraints.maxWidth < 340;
              final priceBox = _buildInputBox(
                controller: _initialPriceController,
                label: L10n.s(lang, 'current_avg_label'),
                unit: currency.symbol,
                icon: Icons.payments_outlined,
                isDark: isDark,
                onQuickMinus: () => _adjustPrice(_initialPriceController, -0.01),
                onQuickPlus: () => _adjustPrice(_initialPriceController, 0.01),
              );
              final qtyBox = _buildInputBox(
                controller: _initialQtyController,
                label: L10n.s(lang, 'current_qty_label'),
                unit: L10n.s(lang, 'unit_share'),
                icon: Icons.pin_outlined,
                isDark: isDark,
                onQuickMinus: () => _adjustQty(_initialQtyController, -10),
                onQuickPlus: () => _adjustQty(_initialQtyController, 10),
              );

              if (isNarrow) {
                return Column(
                  children: [
                    priceBox,
                    const SizedBox(height: 14),
                    qtyBox,
                  ],
                );
              }

              return Row(
                children: [
                  Expanded(child: priceBox),
                  const SizedBox(width: 14),
                  Expanded(child: qtyBox),
                ],
              );
            },
          ),
        ],
      ),
    );
  }

  /// Step 2: Additional Buy Plan Card
  Widget _buildPurchasePlanCard(BuildContext context, bool isDark, LanguageType lang, bool isB) {
    final currency = ref.watch(currencyProvider);
    final cardBg = isDark ? TMembershipColors.darkSurface : TMembershipColors.lightSurface;
    final cardBorder = isDark ? TMembershipColors.darkCardBorder : TMembershipColors.lightCardBorder;
    final titleColor = isDark ? TMembershipColors.darkTextPrimary : TMembershipColors.lightTextPrimary;

    final prices = isB ? _priceControllersB : _priceControllersA;
    final qtys = isB ? _qtyControllersB : _qtyControllersA;
    final planColor = isB ? TMembershipColors.accentOrange : TMembershipColors.accentPurple;

    return Container(
      padding: const EdgeInsets.all(20),
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
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Expanded(
                child: Row(
                  children: [
                    Container(
                      width: 26,
                      height: 26,
                      decoration: BoxDecoration(
                        color: planColor,
                        shape: BoxShape.circle,
                      ),
                      child: Center(
                        child: Text(isB ? "B" : "2", style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 13)),
                      ),
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: FittedBox(
                        fit: BoxFit.scaleDown,
                        alignment: Alignment.centerLeft,
                        child: Text(
                          isB ? (lang == LanguageType.ko ? "비교 시나리오 B" : "Scenario B") : L10n.s(lang, 'step_2_title'),
                          style: GoogleFonts.inter(
                            color: titleColor,
                            fontWeight: FontWeight.w800,
                            fontSize: 15,
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(width: 8),
              FittedBox(
                fit: BoxFit.scaleDown,
                child: TextButton.icon(
                  onPressed: () => _addBatch(isB),
                  icon: const Icon(Icons.add_rounded, size: 14, color: Colors.white),
                  label: Text(
                    L10n.s(lang, 'add_batch'),
                    style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w800, fontSize: 11),
                  ),
                  style: TextButton.styleFrom(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 5),
                    backgroundColor: planColor,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          ListView.separated(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            itemCount: prices.length,
            separatorBuilder: (context, index) => const SizedBox(height: 14),
            itemBuilder: (context, index) {
              return LayoutBuilder(
                builder: (context, constraints) {
                  final isNarrow = constraints.maxWidth < 360;
                  final priceBox = _buildInputBox(
                    controller: prices[index],
                    label: "${index + 1} • ${L10n.s(lang, 'batch_price_label')}",
                    unit: currency.symbol,
                    icon: Icons.add_shopping_cart_rounded,
                    isDark: isDark,
                    onQuickMinus: () => _adjustPrice(prices[index], -0.01),
                    onQuickPlus: () => _adjustPrice(prices[index], 0.01),
                  );
                  final qtyBox = _buildInputBox(
                    controller: qtys[index],
                    label: "${index + 1} • ${L10n.s(lang, 'batch_qty_label')}",
                    unit: L10n.s(lang, 'unit_share'),
                    icon: Icons.numbers_rounded,
                    isDark: isDark,
                    onQuickMinus: () => _adjustQty(qtys[index], -10),
                    onQuickPlus: () => _adjustQty(qtys[index], 10),
                  );

                  final deleteButton = prices.length > 1
                      ? InkWell(
                          onTap: () => _removeBatch(index, isB),
                          borderRadius: BorderRadius.circular(10),
                          child: Container(
                            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 7),
                            decoration: BoxDecoration(
                              color: TMembershipColors.accentCoral.withValues(alpha: 0.1),
                              borderRadius: BorderRadius.circular(10),
                              border: Border.all(color: TMembershipColors.accentCoral.withValues(alpha: 0.3), width: 1),
                            ),
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                const Icon(Icons.delete_outline_rounded, color: TMembershipColors.accentCoral, size: 16),
                                const SizedBox(width: 4),
                                Text(
                                  L10n.s(lang, 'delete_btn'),
                                  style: const TextStyle(
                                    color: TMembershipColors.accentCoral,
                                    fontWeight: FontWeight.w700,
                                    fontSize: 12,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        )
                      : const SizedBox.shrink();

                  if (isNarrow) {
                    return Container(
                      padding: const EdgeInsets.all(14),
                      decoration: BoxDecoration(
                        color: isDark ? const Color(0xFF161E2C) : const Color(0xFFF3F6FB),
                        borderRadius: BorderRadius.circular(18),
                        border: Border.all(
                          color: isDark ? const Color(0xFF222D3E) : const Color(0xFFE2E7F0),
                          width: 1,
                        ),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          priceBox,
                          const SizedBox(height: 14),
                          qtyBox,
                          if (prices.length > 1) ...[
                            const SizedBox(height: 12),
                            Align(
                              alignment: Alignment.centerRight,
                              child: deleteButton,
                            ),
                          ],
                        ],
                      ),
                    );
                  }

                  return Row(
                    crossAxisAlignment: CrossAxisAlignment.end,
                    children: [
                      Expanded(child: priceBox),
                      const SizedBox(width: 14),
                      Expanded(child: qtyBox),
                      if (prices.length > 1) ...[
                        const SizedBox(width: 10),
                        Padding(
                          padding: const EdgeInsets.only(bottom: 4),
                          child: IconButton(
                            icon: const Icon(Icons.remove_circle_outline_rounded, color: TMembershipColors.accentCoral, size: 24),
                            onPressed: () => _removeBatch(index, isB),
                            padding: EdgeInsets.zero,
                            constraints: const BoxConstraints(minWidth: 36, minHeight: 48),
                          ),
                        ),
                      ],
                    ],
                  );
                },
              );
            },
          ),
        ],
      ),
    );
  }

  /// Target Price Mode Card
  Widget _buildTargetCalculatorCard(BuildContext context, bool isDark, LanguageType lang) {
    final currency = ref.watch(currencyProvider);
    final cardBg = isDark ? TMembershipColors.darkSurface : TMembershipColors.lightSurface;
    final cardBorder = isDark ? TMembershipColors.darkCardBorder : TMembershipColors.lightCardBorder;
    final titleColor = isDark ? TMembershipColors.darkTextPrimary : TMembershipColors.lightTextPrimary;

    return Container(
      padding: const EdgeInsets.all(20),
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
                width: 26,
                height: 26,
                decoration: const BoxDecoration(
                  color: TMembershipColors.accentMagenta,
                  shape: BoxShape.circle,
                ),
                child: const Center(
                  child: Text("🎯", style: TextStyle(fontSize: 12)),
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: FittedBox(
                  fit: BoxFit.scaleDown,
                  alignment: Alignment.centerLeft,
                  child: Text(
                    L10n.s(lang, 'step_3_title'),
                    style: GoogleFonts.inter(
                      color: titleColor,
                      fontWeight: FontWeight.w800,
                      fontSize: 15,
                    ),
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 18),
          LayoutBuilder(
            builder: (context, constraints) {
              final isNarrow = constraints.maxWidth < 340;
              final targetPriceBox = _buildInputBox(
                controller: _targetPriceController,
                label: L10n.s(lang, 'target_goal_price'),
                unit: currency.symbol,
                icon: Icons.flag_rounded,
                isDark: isDark,
                onQuickMinus: () => _adjustPrice(_targetPriceController, -0.01),
                onQuickPlus: () => _adjustPrice(_targetPriceController, 0.01),
              );
              final purchasePriceBox = _buildInputBox(
                controller: _purchasePriceController,
                label: L10n.s(lang, 'target_buy_price'),
                unit: currency.symbol,
                icon: Icons.shopping_bag_outlined,
                isDark: isDark,
                onQuickMinus: () => _adjustPrice(_purchasePriceController, -0.01),
                onQuickPlus: () => _adjustPrice(_purchasePriceController, 0.01),
              );

              if (isNarrow) {
                return Column(
                  children: [
                    targetPriceBox,
                    const SizedBox(height: 14),
                    purchasePriceBox,
                  ],
                );
              }

              return Row(
                children: [
                  Expanded(child: targetPriceBox),
                  const SizedBox(width: 14),
                  Expanded(child: purchasePriceBox),
                ],
              );
            },
          ),
          if (_requiredQty != null && _requiredQty! > 0) ...[
            const SizedBox(height: 16),
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: TMembershipColors.accentMagenta.withOpacity(0.1),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: TMembershipColors.accentMagenta.withOpacity(0.3)),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(L10n.s(lang, 'required_qty'), style: const TextStyle(color: TMembershipColors.accentMagenta, fontWeight: FontWeight.bold, fontSize: 12)),
                  const SizedBox(height: 4),
                  Text(
                    "${_currencyFormat.format(_requiredQty)} ${L10n.s(lang, 'unit_share')}",
                    style: GoogleFonts.inter(
                      fontSize: 24,
                      fontWeight: FontWeight.w900,
                      color: isDark ? Colors.white : TMembershipColors.lightTextPrimary,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ],
      ),
    );
  }

  /// Clean, Modern Input Box with Roomy Quick Steppers & Touch Friendly Controls
  Widget _buildInputBox({
    required TextEditingController controller,
    required String label,
    required String unit,
    required IconData icon,
    required bool isDark,
    VoidCallback? onQuickMinus,
    VoidCallback? onQuickPlus,
  }) {
    final subColor = isDark ? TMembershipColors.darkTextTertiary : TMembershipColors.lightTextTertiary;
    final textColor = isDark ? Colors.white : TMembershipColors.lightTextPrimary;
    final boxBg = isDark ? const Color(0xFF131923) : const Color(0xFFF8FAFD);
    final boxBorder = isDark ? TMembershipColors.darkCardBorder : const Color(0xFFE4E9F2);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(bottom: 8),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Flexible(
                child: FittedBox(
                  fit: BoxFit.scaleDown,
                  alignment: Alignment.centerLeft,
                  child: Text(
                    label,
                    style: TextStyle(
                      color: subColor,
                      fontWeight: FontWeight.w700,
                      fontSize: 12.5,
                    ),
                  ),
                ),
              ),
              if (onQuickMinus != null && onQuickPlus != null)
                Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Material(
                      color: Colors.transparent,
                      child: InkWell(
                        onTap: onQuickMinus,
                        borderRadius: BorderRadius.circular(10),
                        child: Container(
                          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                          decoration: BoxDecoration(
                            color: TMembershipColors.primaryBlue.withValues(alpha: 0.12),
                            borderRadius: BorderRadius.circular(10),
                            border: Border.all(color: TMembershipColors.primaryBlue.withValues(alpha: 0.28), width: 1),
                          ),
                          child: const Text(
                            "−",
                            style: TextStyle(
                              color: TMembershipColors.primaryBlue,
                              fontWeight: FontWeight.w900,
                              fontSize: 15,
                              height: 1,
                            ),
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(width: 8),
                    Material(
                      color: Colors.transparent,
                      child: InkWell(
                        onTap: onQuickPlus,
                        borderRadius: BorderRadius.circular(10),
                        child: Container(
                          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                          decoration: BoxDecoration(
                            color: TMembershipColors.primaryBlue.withValues(alpha: 0.12),
                            borderRadius: BorderRadius.circular(10),
                            border: Border.all(color: TMembershipColors.primaryBlue.withValues(alpha: 0.28), width: 1),
                          ),
                          child: const Text(
                            "+",
                            style: TextStyle(
                              color: TMembershipColors.primaryBlue,
                              fontWeight: FontWeight.w900,
                              fontSize: 15,
                              height: 1,
                            ),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
            ],
          ),
        ),
        Container(
          decoration: BoxDecoration(
            color: boxBg,
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: boxBorder, width: 1.4),
          ),
          child: TextField(
            controller: controller,
            keyboardType: const TextInputType.numberWithOptions(decimal: true),
            textAlign: TextAlign.right,
            style: GoogleFonts.inter(
              color: textColor,
              fontWeight: FontWeight.w800,
              fontSize: 17,
            ),
            inputFormatters: [ThousandsSeparatorInputFormatter()],
            decoration: InputDecoration(
              isDense: true,
              prefixIcon: Padding(
                padding: const EdgeInsets.only(left: 14, right: 8),
                child: Icon(icon, color: TMembershipColors.primaryBlue, size: 20),
              ),
              prefixIconConstraints: const BoxConstraints(minWidth: 42, minHeight: 42),
              suffixText: " $unit",
              suffixStyle: TextStyle(color: subColor, fontWeight: FontWeight.w700, fontSize: 13.5),
              border: InputBorder.none,
              contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 16),
            ),
          ),
        ),
      ],
    );
  }

  /// What-if Sensitivity Slider
  Widget _buildSensitivityCard(BuildContext context, bool isDark, LanguageType lang) {
    final cardBg = isDark ? TMembershipColors.darkSurface : TMembershipColors.lightSurface;
    final cardBorder = isDark ? TMembershipColors.darkCardBorder : TMembershipColors.lightCardBorder;
    final titleColor = isDark ? TMembershipColors.darkTextPrimary : TMembershipColors.lightTextPrimary;

    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: cardBg,
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: cardBorder, width: 1.2),
        boxShadow: isDark ? [] : TMembershipColors.softShadow(blur: 10, dy: 3),
      ),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  const Icon(Icons.insights_rounded, color: TMembershipColors.primaryBlue, size: 20),
                  const SizedBox(width: 8),
                  Text(
                    L10n.s(lang, 'sensitivity_title'),
                    style: GoogleFonts.inter(
                      color: titleColor,
                      fontWeight: FontWeight.w700,
                      fontSize: 13,
                    ),
                  ),
                ],
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                decoration: BoxDecoration(
                  color: TMembershipColors.primaryBlue.withOpacity(0.12),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  "${(_simulatedPriceFactor * 100).toStringAsFixed(0)}%",
                  style: const TextStyle(
                    color: TMembershipColors.primaryBlue,
                    fontWeight: FontWeight.w900,
                    fontSize: 12,
                  ),
                ),
              ),
            ],
          ),
          SliderTheme(
            data: SliderTheme.of(context).copyWith(
              activeTrackColor: TMembershipColors.primaryBlue,
              inactiveTrackColor: isDark ? Colors.white12 : const Color(0xFFE2E8F0),
              thumbColor: TMembershipColors.primaryBlue,
              overlayColor: TMembershipColors.primaryBlue.withOpacity(0.15),
            ),
            child: Slider(
              value: _simulatedPriceFactor,
              min: 0.5,
              max: 1.5,
              onChanged: (val) {
                setState(() => _simulatedPriceFactor = val);
                _calculate();
                HapticFeedback.selectionClick();
              },
            ),
          ),
        ],
      ),
    );
  }

  /// Bottom Actions: Save Scenario, Save to Portfolio
  Widget _buildBottomActionButtons(BuildContext context, bool isDark, LanguageType lang) {
    return LayoutBuilder(
      builder: (context, constraints) {
        final isNarrow = constraints.maxWidth < 340;
        final saveBtn = ElevatedButton.icon(
          onPressed: _saveScenario,
          icon: const Icon(Icons.bookmark_border_rounded, size: 18),
          label: FittedBox(
            fit: BoxFit.scaleDown,
            child: Text(
              L10n.s(lang, 'save_scenario_btn'),
              maxLines: 1,
              style: const TextStyle(fontWeight: FontWeight.w800),
            ),
          ),
          style: ElevatedButton.styleFrom(
            backgroundColor: isDark ? TMembershipColors.darkSurface : Colors.white,
            foregroundColor: TMembershipColors.primaryBlue,
            elevation: 0,
            minimumSize: const Size(double.infinity, 52),
            side: BorderSide(
              color: isDark ? TMembershipColors.darkCardBorder : TMembershipColors.lightCardBorder,
              width: 1.2,
            ),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          ),
        );

        final portfolioBtn = ElevatedButton.icon(
          onPressed: _saveToPortfolio,
          icon: const Icon(Icons.account_balance_wallet_outlined, size: 18),
          label: FittedBox(
            fit: BoxFit.scaleDown,
            child: Text(
              L10n.s(lang, 'save_to_portfolio_btn'),
              maxLines: 1,
              style: const TextStyle(fontWeight: FontWeight.w900),
            ),
          ),
          style: ElevatedButton.styleFrom(
            backgroundColor: TMembershipColors.primaryBlue,
            foregroundColor: Colors.white,
            elevation: 0,
            minimumSize: const Size(double.infinity, 52),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          ),
        );

        if (isNarrow) {
          return Column(
            children: [
              portfolioBtn,
              const SizedBox(height: 10),
              saveBtn,
            ],
          );
        }

        return Row(
          children: [
            Expanded(child: saveBtn),
            const SizedBox(width: 12),
            Expanded(child: portfolioBtn),
          ],
        );
      },
    );
  }
}

class ThousandsSeparatorInputFormatter extends TextInputFormatter {
  final NumberFormat _formatter = NumberFormat.decimalPattern();

  @override
  TextEditingValue formatEditUpdate(TextEditingValue oldValue, TextEditingValue newValue) {
    if (newValue.text.isEmpty) return newValue;

    final String baseText = newValue.text.replaceAll(',', '');
    final double? value = double.tryParse(baseText);
    if (value == null) return oldValue;

    final String formattedText = _formatter.format(value);

    int selectionIndex = newValue.selection.end;
    int commaCountBefore = oldValue.text.split(',').length - 1;
    int commaCountAfter = formattedText.split(',').length - 1;
    selectionIndex += (commaCountAfter - commaCountBefore);

    return TextEditingValue(
      text: formattedText,
      selection: TextSelection.collapsed(offset: selectionIndex.clamp(0, formattedText.length)),
    );
  }
}
