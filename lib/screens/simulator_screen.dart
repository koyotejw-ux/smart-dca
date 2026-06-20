import 'package:flutter/material.dart';
import 'package:flutter/services.dart'; 
import 'package:haptic_feedback/haptic_feedback.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../widgets/one_ui_scroll_view.dart';
import '../widgets/recovery_gauge.dart';
import '../widgets/price_chart.dart';
import '../services/calculator_service.dart';
import 'report_screen.dart';
import '../providers/language_provider.dart';
import '../utils/l10n.dart';
import '../providers/asset_provider.dart';
import '../models/asset_model.dart';
import '../widgets/glass_card.dart';
import '../theme/one_ui_colors.dart';
import '../widgets/master_guide_overlay.dart';
import '../models/scenario_model.dart';
import '../providers/scenario_provider.dart';
import 'scenario_history_screen.dart';
import '../theme/neon_colors.dart';
import 'package:uuid/uuid.dart';
import '../services/admob_service.dart';

class SimulatorScreen extends ConsumerStatefulWidget {
  final Scenario? initialScenario;
  const SimulatorScreen({super.key, this.initialScenario});

  @override
  ConsumerState<SimulatorScreen> createState() => _SimulatorScreenState();
}

class _SimulatorScreenState extends ConsumerState<SimulatorScreen> {
  final _assetNameController = TextEditingController(text: 'New Asset');
  final _assetSymbolController = TextEditingController(text: 'BTC');
  final _initialPriceController = TextEditingController();
  final _initialQtyController = TextEditingController();
  
  // Scenario A
  final List<TextEditingController> _priceControllersA = [TextEditingController()];
  final List<TextEditingController> _qtyControllersA = [TextEditingController()];
  
  // Scenario B (Comparison)
  final List<TextEditingController> _priceControllersB = [TextEditingController()];
  final List<TextEditingController> _qtyControllersB = [TextEditingController()];

  bool _showGuide = true; // Show on first load for now
  final TextEditingController _targetPriceController = TextEditingController();
  bool _isCompareMode = false;
  bool _isTargetMode = false;
  double _totalAvgPrice = 0.0;
  bool _isBullMode = false;
  bool _isFeeEnabled = false;
  double _simulatedPriceFactor = 1.0;
  CalculationResult? _resultA;
  CalculationResult? _resultB;
  double? _requiredQty;
  final _currencyFormat = NumberFormat.currency(symbol: '', decimalDigits: 0);

  final _purchasePriceController = TextEditingController();

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
      
      // Clear defaults
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

    // Calc Scenario A
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
      }
    } else {
      _resultA = _calcBatch(basePrice, iq, _priceControllersA, _qtyControllersA);
      if (_isCompareMode) {
        _resultB = _calcBatch(basePrice, iq, _priceControllersB, _qtyControllersB);
      }
      setState(() {});
    }
  }

  void _adjustPrice(TextEditingController controller, double percent) {
    final val = _parseVal(controller.text);
    if (val > 0) {
      final newVal = val * (1 + percent);
      controller.text = _currencyFormat.format(newVal).trim();
      _calculate();
      HapticFeedback.selectionClick();
    }
  }

  void _adjustQty(TextEditingController controller, double amount) {
    final val = _parseVal(controller.text);
    final newVal = (val + amount).clamp(0, double.infinity);
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

  Future<void> _saveToPortfolio() async {
    final ip = double.tryParse(_initialPriceController.text) ?? 0;
    final iq = double.tryParse(_initialQtyController.text) ?? 0;

    if (ip > 0 && iq > 0) {
      AdmobService.showInterstitial(
        onDismissed: () async {
          await ref.read(assetsProvider.notifier).addAsset(Asset(
            name: _assetNameController.text,
            symbol: _assetSymbolController.text,
            initialPrice: ip,
            initialQuantity: iq,
            type: 'stock',
          ));
          if (mounted) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text(L10n.s(ref.read(languageProvider), 'save_to_portfolio_success')),
                behavior: SnackBarBehavior.floating,
              ),
            );
          }
        },
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(languageProvider);
    final width = MediaQuery.of(context).size.width;

    return Scaffold(
      backgroundColor: NeonColors.background,
      appBar: PreferredSize(
        preferredSize: const Size.fromHeight(80),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 8),
            child: _buildSimulatorHeader(context, lang),
          ),
        ),
      ),
      body: ListView(
        padding: const EdgeInsets.symmetric(horizontal: 32),
        children: [
          const SizedBox(height: 16),
          _buildNeonPrimaryHeader(context, lang)
            .animate().fadeIn(duration: 400.ms).slideY(begin: 0.1, end: 0), // Huge Result LCD
          const SizedBox(height: 32),
          _buildMasterInputCard(context, lang)
            .animate().fadeIn(duration: 600.ms, delay: 100.ms).slideY(begin: 0.1, end: 0), // Step 1
          const SizedBox(height: 32),
          _buildSensitivitySlider(context, lang),
          const SizedBox(height: 24),
          _buildConcentrationWarning(context, lang),
          const SizedBox(height: 32),
          if (_isCompareMode)
            width > 900 
              ? Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Expanded(child: _buildInputSection(context, lang, false)),
                    const SizedBox(width: 24),
                    Expanded(child: _buildInputSection(context, lang, true)),
                  ],
                )
              : Column(
                  children: [
                    _buildInputSection(context, lang, false),
                    const SizedBox(height: 16),
                    _buildInputSection(context, lang, true),
                  ],
                )
          else
            _isTargetMode ? _buildTargetInputCard(context, lang) : _buildInputSection(context, lang, false),
          const SizedBox(height: 32),
          if (!_isCompareMode) _buildDropStrategyTable(context, lang),
          const SizedBox(height: 32),
          _buildStrategyToggles(context, lang),
          const SizedBox(height: 80),
        ],
      ),
    );
  }

  Widget _buildSimulatorHeader(BuildContext context, LanguageType lang) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Row(
          children: [
            IconButton(
              icon: const Icon(Icons.arrow_back_ios_new_rounded, color: Colors.white, size: 24),
              onPressed: () => Navigator.pop(context),
            ),
            const SizedBox(width: 12),
            Text(
              "물타기 계산기",
              style: GoogleFonts.inter(
                color: Colors.white,
                fontWeight: FontWeight.w900,
                fontSize: 28,
              ),
            ),
          ],
        ),
        Row(
          children: [
            IconButton(
              onPressed: () => setState(() => _isCompareMode = !_isCompareMode),
              icon: Icon(_isCompareMode ? Icons.view_day_outlined : Icons.compare_arrows_rounded, color: NeonColors.cyan),
            ),
            IconButton(
              onPressed: _resetInputs,
              icon: const Text("AC", style: TextStyle(color: Colors.orange, fontWeight: FontWeight.w900)),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildNeonPrimaryHeader(BuildContext context, LanguageType lang) {
    final theme = Theme.of(context);
    final val = _resultA?.averagePrice ?? 0;
    final pnl = _resultA?.recoveryPercentage ?? 0;
    final pnlColor = pnl >= 0 ? NeonColors.green : NeonColors.pink;

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(24),
      decoration: NeonColors.glassyBorder(NeonColors.cyan),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          Text(
            L10n.s(lang, 'new_avg_price').toUpperCase(),
            style: NeonColors.textGlow(Colors.white54).copyWith(
              fontWeight: FontWeight.bold,
              fontSize: 12,
              letterSpacing: 2,
            ),
          ),
          const SizedBox(height: 8),
          FittedBox(
            child: Text(
              _currencyFormat.format(val),
              style: GoogleFonts.notoSansMono(
                color: NeonColors.cyan,
                fontWeight: FontWeight.w900,
                fontSize: 64,
                letterSpacing: -2,
                shadows: [],
              ),
            ),
          ),
          if (_resultA != null)
            Text(
              _isBullMode 
                ? "PROFIT TARGET: ${pnl.abs().toStringAsFixed(1)}%" 
                : "RECOVERY: ${pnl.toStringAsFixed(1)}%",
              style: NeonColors.textGlow(pnlColor).copyWith(
                fontSize: 16, 
                fontWeight: FontWeight.w900,
              ),
            ),
            const SizedBox(height: 16),
            _buildBreakEvenProgress(context),
        ],
      ),
    );
  }

  Widget _buildBreakEvenProgress(BuildContext context) {
    if (_resultA == null) return const SizedBox.shrink();
    
    final ip = _parseVal(_initialPriceController.text);
    final currentPrice = ip * _simulatedPriceFactor;
    final avgPrice = _resultA!.averagePrice;
    
    // Progress is how close currentPrice is to avgPrice
    // 0% means currentPrice is very far, 100% means currentPrice >= avgPrice
    double progress = 0;
    if (avgPrice > 0) {
       progress = (currentPrice / avgPrice).clamp(0.0, 1.25) / 1.25;
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const Text("BREAK-EVEN PROXIMITY", style: TextStyle(color: Colors.white30, fontSize: 10, fontWeight: FontWeight.bold)),
            Text("${(progress * 125).toStringAsFixed(0)}%", style: const TextStyle(color: NeonColors.cyan, fontSize: 10, fontWeight: FontWeight.bold)),
          ],
        ),
        const SizedBox(height: 8),
        Container(
          height: 6,
          width: double.infinity,
          decoration: BoxDecoration(
            color: Colors.white10,
            borderRadius: BorderRadius.circular(3),
          ),
          child: FractionallySizedBox(
            alignment: Alignment.centerLeft,
            widthFactor: progress.clamp(0.0, 1.0),
            child: Container(
              decoration: BoxDecoration(
                color: NeonColors.cyan,
                borderRadius: BorderRadius.circular(3),
                border: Border.all(color: Colors.black, width: 1),
              ),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildSensitivitySlider(BuildContext context, LanguageType lang) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
      decoration: NeonColors.borderGlow(Colors.white10).copyWith(color: Colors.black),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text("WHAT-IF SENSITIVITY", style: TextStyle(color: Colors.white54, fontSize: 11, fontWeight: FontWeight.bold, letterSpacing: 1)),
              Text(
                "${(_simulatedPriceFactor * 100).toStringAsFixed(0)}% Price",
                style: const TextStyle(color: NeonColors.pink, fontWeight: FontWeight.w900, fontSize: 13),
              ),
            ],
          ),
          SliderTheme(
            data: SliderTheme.of(context).copyWith(
               activeTrackColor: NeonColors.pink,
               inactiveTrackColor: Colors.white12,
               thumbColor: NeonColors.pink,
               overlayColor: NeonColors.pink.withOpacity(0.2),
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
          const Text("주가 변동에 따른 실시간 수익률 시뮬레이션", style: TextStyle(color: Colors.white24, fontSize: 10)),
        ],
      ),
    );
  }

  Widget _buildNeonMetricGrid(BuildContext context, LanguageType lang) {
    if (_resultA == null) return const SizedBox.shrink();
    
    return GridView.count(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      crossAxisCount: 2,
      childAspectRatio: 2.2,
      crossAxisSpacing: 12,
      mainAxisSpacing: 12,
      children: [
        _buildNeonMetric(L10n.s(lang, 'total_quantity'), _resultA!.totalQuantity.toStringAsFixed(0), NeonColors.cyan),
        _buildNeonMetric(L10n.s(lang, 'total_invested'), _currencyFormat.format(_resultA!.totalInvestment), NeonColors.pink),
      ],
    );
  }

  Widget _buildNeonMetric(String label, String value, Color color) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: NeonColors.borderGlow(color),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          Text(label, style: const TextStyle(fontSize: 10, fontWeight: FontWeight.w900, color: Colors.white54)),
          const Spacer(),
          FittedBox(child: Text(value, style: GoogleFonts.notoSansMono(fontSize: 22, fontWeight: FontWeight.w900, color: color, shadows: []))),
        ],
      ),
    );
  }

  Widget _buildConcentrationWarning(BuildContext context, LanguageType lang) {
    if (_resultA == null) return const SizedBox.shrink();

    final assets = ref.watch(assetsProvider);
    double totalPortfolioValue = 0;
    for (var a in assets) {
      totalPortfolioValue += a.initialPrice * a.initialQuantity;
    }

    final currentInvestment = _resultA!.totalInvestment;
    final combinedTotal = totalPortfolioValue + currentInvestment;
    final percentage = combinedTotal > 0 ? (currentInvestment / combinedTotal) * 100 : 0.0;

    if (percentage < 30) return const SizedBox.shrink();

    return Container(
      margin: const EdgeInsets.only(top: 16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: percentage > 70 ? Colors.red.withOpacity(0.1) : Colors.orange.withOpacity(0.1),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: percentage > 70 ? Colors.red : Colors.orange, width: 2),
      ),
      child: Row(
        children: [
          Icon(Icons.warning_amber_rounded, color: percentage > 70 ? Colors.red : Colors.orange),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              "집중 투자 주의: 이 매수 시 전체 자산의 ${percentage.toStringAsFixed(1)}%가 이 종목에 집중됩니다.",
              style: TextStyle(
                fontWeight: FontWeight.w900, 
                fontSize: 13, 
                color: percentage > 70 ? Colors.red : Colors.orange
              ),
            ),
          ),
        ],
      ),
    );
  }

  void _resetInputs() {
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
  }

  Future<void> _saveScenario() async {
    if (_resultA == null) return;

    final ip = _parseVal(_initialPriceController.text);
    final iq = _parseVal(_initialQtyController.text);
    final batches = _calcBatches(false);

    final scenario = Scenario(
      id: const Uuid().v4(),
      name: "Scenario ${DateTime.now().hour}:${DateTime.now().minute}",
      initialPrice: ip,
      initialQuantity: iq,
      batches: batches,
      createdAt: DateTime.now(),
    );

    await ref.read(scenarioProvider.notifier).addScenario(scenario);
    
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("시나리오가 저장되었습니다. (History 확인 가능)")),
      );
    }
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

  Widget _buildMetricGrid(BuildContext context, LanguageType lang) {
    if (_resultA == null) return const SizedBox.shrink();
    
    return GridView.count(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      crossAxisCount: 2,
      childAspectRatio: 2.2,
      crossAxisSpacing: 12,
      mainAxisSpacing: 12,
      children: [
        _buildTactileMetric(L10n.s(lang, 'total_quantity'), _resultA!.totalQuantity.toStringAsFixed(0), Colors.blue),
        _buildTactileMetric(L10n.s(lang, 'total_invested'), _currencyFormat.format(_resultA!.totalInvestment), Colors.orange),
      ],
    );
  }

  Widget _buildTactileMetric(String label, String value, Color color) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.black, width: 2),
        boxShadow: const [BoxShadow(color: Colors.black12, offset: Offset(0, 4), blurRadius: 0)],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          Text(label, style: const TextStyle(fontSize: 10, fontWeight: FontWeight.w900, color: Colors.grey)),
          const Spacer(),
          FittedBox(child: Text(value, style: GoogleFonts.notoSansMono(fontSize: 18, fontWeight: FontWeight.w900, color: Colors.white70))),
        ],
      ),
    );
  }

  Widget _buildDropStrategyTable(BuildContext context, LanguageType lang) {
    final ip = double.tryParse(_initialPriceController.text) ?? 0;
    final iq = double.tryParse(_initialQtyController.text) ?? 0;
    if (ip <= 0 || iq <= 0) return const SizedBox.shrink();

    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.black, width: 2),
      ),
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(L10n.s(lang, 'drop_strategy'), style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 14)),
          const SizedBox(height: 16),
          Table(
            children: [
              TableRow(
                children: [
                  _buildHeaderCell(L10n.s(lang, 'drop_label')),
                  _buildHeaderCell(L10n.s(lang, 'target_label')),
                  _buildHeaderCell(L10n.s(lang, 'buy_qty_label')),
                ],
              ),
              ...[5.0, 10.0, 15.0, 20.0, 30.0].map((drop) {
                final targetPrice = ip * (1 - drop / 100);
                return TableRow(
                  children: [
                    _buildCell("-$drop%", color: Colors.redAccent),
                    _buildCell(_currencyFormat.format(targetPrice)),
                    _buildCell(_currencyFormat.format(iq * (drop/10))), 
                  ],
                );
              }),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildHeaderCell(String text) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Text(text, textAlign: TextAlign.center, style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 12, color: Colors.grey)),
    );
  }

  Widget _buildCell(String text, {Color? color}) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Text(
        text, 
        textAlign: TextAlign.center, 
        style: TextStyle(fontWeight: FontWeight.w900, fontSize: 14, color: color),
      ),
    );
  }

  Widget _buildScenarioLabel(String label, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
      decoration: BoxDecoration(color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(12)),
      child: Text(label, style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 12)),
    );
  }


  Widget _buildMetricCard(BuildContext context, String label, String value, IconData icon, Color color, {String? subtitle}) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return Container(
      decoration: BoxDecoration(
        color: isDark ? theme.colorScheme.surface : Colors.white,
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: Colors.black.withOpacity(0.12), width: 1.5),
      ),
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            children: [
              Icon(icon, size: 16, color: color),
              const SizedBox(width: 8),
              Expanded(
                child: Text(
                  label,
                  style: theme.textTheme.labelSmall?.copyWith(
                    color: isDark ? Colors.white70 : Colors.black54,
                    fontWeight: FontWeight.w800,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              ),
              if (subtitle != null)
                Text(
                  subtitle,
                  style: TextStyle(color: color, fontWeight: FontWeight.w900, fontSize: 12),
                ),
            ],
          ),
          const SizedBox(height: 4),
          Text(
            value,
            style: theme.textTheme.titleLarge?.copyWith(
              fontWeight: FontWeight.w900,
              color: isDark ? Colors.white : Colors.black,
            ),
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
        ],
      ),
    );
  }

  Widget _buildModeToggle(BuildContext context, LanguageType lang) {
    final theme = Theme.of(context);
    return Column(
      children: [
        SegmentedButton<bool>(
          segments: [
            ButtonSegment(value: false, label: Text(L10n.s(lang, 'simulator')), icon: const Icon(Icons.calculate_rounded)),
            ButtonSegment(value: true, label: Text(L10n.s(lang, 'target_calculator')), icon: const Icon(Icons.flag_rounded)),
          ],
          selected: {_isTargetMode},
          onSelectionChanged: (val) => setState(() {
            _isTargetMode = val.first;
            if (_isTargetMode) _isCompareMode = false;
            _calculate();
          }),
        ),
        if (!_isTargetMode) ...[
          const SizedBox(height: 16),
          _buildCompareSwitch(context, lang),
        ],
      ],
    );
  }

  Widget _buildCompareSwitch(BuildContext context, LanguageType lang) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
      decoration: BoxDecoration(
        color: _isCompareMode ? Colors.blue.withOpacity(0.08) : Colors.grey.withOpacity(0.05),
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: _isCompareMode ? Colors.blue.withOpacity(0.2) : Colors.transparent),
      ),
      child: Row(
        children: [
          _buildStepBadge("3"),
          const SizedBox(width: 12),
          const Icon(Icons.compare_arrows_rounded, color: Colors.blue, size: 24),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              L10n.s(lang, 'scenario_compare'), 
              style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w900, color: Colors.blue),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStrategyToggles(BuildContext context, LanguageType lang) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      decoration: NeonColors.glassyBorder(Colors.white10),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          _buildToggleItem(
            L10n.s(lang, 'scenario_compare'),
            _isCompareMode,
            (val) => setState(() {
              _isCompareMode = val;
              if (val) _isTargetMode = false;
              _calculate();
            }),
          ),
          Container(width: 1, height: 24, color: Colors.white10),
          _buildToggleItem(
            "목표가 전략",
            _isTargetMode,
            (val) => setState(() {
              _isTargetMode = val;
              if (val) _isCompareMode = false;
              _calculate();
            }),
          ),
        ],
      ),
    );
  }

  Widget _buildToggleItem(String label, bool value, Function(bool) onChanged) {
    return Row(
      children: [
        Text(label.toUpperCase(), style: GoogleFonts.inter(fontSize: 12, fontWeight: FontWeight.w900, color: value ? NeonColors.cyan : Colors.white38)),
        const SizedBox(width: 8),
        Switch.adaptive(
          value: value,
          activeColor: NeonColors.cyan,
          onChanged: onChanged,
        ),
      ],
    );
  }

  Widget _buildMasterInputCard(BuildContext context, LanguageType lang) {
     return Container(
       padding: const EdgeInsets.all(24),
       decoration: NeonColors.glassyBorder(Colors.white10).copyWith(
         color: Colors.black,
         boxShadow: NeonColors.depthShadow(NeonColors.pink.withOpacity(0.05)),
       ),
       child: Column(
         crossAxisAlignment: CrossAxisAlignment.start,
         children: [
            Row(
              children: [
                _buildStepBadge("1"),
                const SizedBox(width: 12),
                Text(L10n.s(lang, 'step_1_initial').toUpperCase(), style: const TextStyle(color: NeonColors.cyan, fontWeight: FontWeight.w900, fontSize: 13, letterSpacing: 1)),
                const Spacer(),
                IconButton(
                  icon: const Icon(Icons.mic_rounded, color: NeonColors.cyan, size: 24),
                  onPressed: () => _showVoiceInput(context),
                ),
              ],
            ),
            const SizedBox(height: 24),
            Row(
              children: [
                Expanded(child: _buildTextField(_initialPriceController, L10n.s(lang, 'avg_price'), Icons.attach_money_rounded)),
                const SizedBox(width: 16),
                Expanded(child: _buildTextField(_initialQtyController, L10n.s(lang, 'quantity'), Icons.numbers_rounded)),
              ],
            ),
         ],
       ),
     );
  }

  Widget _buildInputSection(BuildContext context, LanguageType lang, bool isB) {
    final prices = isB ? _priceControllersB : _priceControllersA;
    final theme = Theme.of(context);

    return Container(
      padding: const EdgeInsets.all(24),
      decoration: NeonColors.borderGlow(isB ? Colors.orange : NeonColors.pink).copyWith(color: Colors.black),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  _buildStepBadge("2"),
                  const SizedBox(width: 12),
                  Text(
                    isB ? L10n.s(lang, 'scenario_compare').toUpperCase() : L10n.s(lang, 'step_2_plan').split(' (')[0].toUpperCase(),
                    style: TextStyle(
                      color: isB ? Colors.orange : NeonColors.pink,
                      fontWeight: FontWeight.w900,
                      fontSize: 13,
                      letterSpacing: 1,
                    ),
                  ),
                ],
              ),
              ElevatedButton.icon(
                onPressed: () => _addBatch(isB), 
                icon: const Icon(Icons.add_rounded, size: 20, color: Colors.black),
                label: Text(L10n.s(lang, 'add_batch').split(' ')[0], style: const TextStyle(color: Colors.black, fontWeight: FontWeight.w900)),
                style: ElevatedButton.styleFrom(
                  backgroundColor: isB ? Colors.orange : NeonColors.pink,
                  minimumSize: const Size(100, 48),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                ),
              ),
            ],
          ),
          const SizedBox(height: 24),
          if (prices.isNotEmpty)
            Table(
              columnWidths: const {
                0: FlexColumnWidth(1.2),
                1: FlexColumnWidth(1.2),
                2: FixedColumnWidth(40),
              },
              children: List.generate(prices.length, (index) => _buildBatchTableRow(index, lang, isB)),
            ),
        ],
      ),
    );
  }

  TableRow _buildBatchTableRow(int index, LanguageType lang, bool isB) {
    final prices = isB ? _priceControllersB : _priceControllersA;
    final qtys = isB ? _qtyControllersB : _qtyControllersA;
    return TableRow(
      children: [
        Padding(
          padding: const EdgeInsets.only(right: 8, bottom: 12),
          child: _buildTextField(prices[index], L10n.s(lang, 'price'), Icons.price_check_rounded, small: true, accentColor: isB ? Colors.orange : NeonColors.pink),
        ),
        Padding(
          padding: const EdgeInsets.only(right: 8, bottom: 12),
          child: _buildTextField(qtys[index], L10n.s(lang, 'quantity'), Icons.plus_one_rounded, small: true, accentColor: isB ? Colors.orange : NeonColors.pink),
        ),
        if (prices.length > 1)
          Padding(
            padding: const EdgeInsets.only(bottom: 12),
            child: IconButton(
              icon: const Icon(Icons.remove_circle_outline_rounded, color: Colors.red, size: 24),
              onPressed: () => _removeBatch(index, isB),
            ),
          )
        else
          const SizedBox.shrink(),
      ],
    );
  }

  Widget _buildStepBadge(String step) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(color: Colors.white12, borderRadius: BorderRadius.circular(12)),
      child: Text(step, style: const TextStyle(color: NeonColors.cyan, fontWeight: FontWeight.w900, fontSize: 12)),
    );
  }

  Widget _buildBatchRow(int index, LanguageType lang, bool isB) {
    final prices = isB ? _priceControllersB : _priceControllersA;
    final qtys = isB ? _qtyControllersB : _qtyControllersA;
    return Padding(
      padding: const EdgeInsets.only(bottom: 12.0),
      child: Row(
        children: [
          Expanded(child: _buildTextField(prices[index], L10n.s(lang, 'price'), Icons.price_check_rounded, small: true)),
          const SizedBox(width: 8),
          Expanded(child: _buildTextField(qtys[index], L10n.s(lang, 'quantity'), Icons.plus_one_rounded, small: true)),
          if (prices.length > 1)
            IconButton(
              icon: const Icon(Icons.remove_circle_outline_rounded, color: Colors.red, size: 20),
              onPressed: () => _removeBatch(index, isB),
            ),
        ],
      ),
    );
  }

  Widget _buildTextField(TextEditingController controller, String label, IconData icon, {bool small = false, Color accentColor = NeonColors.cyan}) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(label.toUpperCase(), style: GoogleFonts.inter(fontWeight: FontWeight.w900, fontSize: 11, color: Colors.white38, letterSpacing: 1)),
            if (label.contains('가') || label.contains('Price'))
              Row(
                children: [
                  _buildQuickAdj(controller, "-1%", () => _adjustPrice(controller, -0.01), color: accentColor),
                  const SizedBox(width: 8),
                  _buildQuickAdj(controller, "+1%", () => _adjustPrice(controller, 0.01), color: accentColor),
                ],
              )
            else if (label.contains('량') || label.contains('Qty'))
              Row(
                children: [
                  _buildQuickAdj(controller, "-10", () => _adjustQty(controller, -10), color: accentColor),
                  const SizedBox(width: 8),
                  _buildQuickAdj(controller, "+100", () => _adjustQty(controller, 100), color: accentColor),
                ],
              ),
          ],
        ),
        const SizedBox(height: 12),
        Container(
          decoration: BoxDecoration(
            boxShadow: NeonColors.depthShadow(accentColor.withOpacity(0.1)),
          ),
          child: TextField(
            controller: controller,
            keyboardType: const TextInputType.numberWithOptions(decimal: true),
            textAlign: TextAlign.right,
            cursorColor: accentColor,
            inputFormatters: [ThousandsSeparatorInputFormatter()],
            style: GoogleFonts.notoSansMono(fontWeight: FontWeight.w900, fontSize: small ? 18 : 22, color: Colors.white),
            decoration: InputDecoration(
              prefixIcon: Icon(icon, size: small ? 18 : 22, color: accentColor.withOpacity(0.5)),
              filled: true,
              fillColor: const Color(0xFF0F0F0F),
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide(color: accentColor.withOpacity(0.3), width: 1.5)),
              enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide(color: accentColor.withOpacity(0.3), width: 1.5)),
              focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide(color: accentColor, width: 2)),
              contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: small ? 12 : 18),
            ),
            onChanged: (val) => _calculate(),
          ),
        ),
      ],
    );
  }

  Widget _buildQuickAdj(TextEditingController controller, String label, VoidCallback onTap, {Color color = NeonColors.cyan}) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(4),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
        decoration: BoxDecoration(
          color: color,
          borderRadius: BorderRadius.circular(4),
          boxShadow: NeonColors.depthShadow(color),
        ),
        child: Text(
          label, 
          style: const TextStyle(color: Colors.black, fontWeight: FontWeight.bold, fontSize: 10)
        ),
      ),
    );
  }

  Widget _buildTargetInputCard(BuildContext context, LanguageType lang) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(L10n.s(lang, 'target_settings'), style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold)),
                IconButton(
                  icon: const Icon(Icons.mic_rounded, color: Colors.blue),
                  onPressed: () => _showVoiceInput(context),
                ),
              ],
            ),
            const SizedBox(height: 16),
            _buildTextField(_initialPriceController, L10n.s(lang, 'avg_price'), Icons.attach_money_rounded),
            const SizedBox(height: 12),
            _buildTextField(_initialQtyController, L10n.s(lang, 'quantity'), Icons.numbers_rounded),
            const Divider(height: 48),
            _buildTextField(_targetPriceController, L10n.s(lang, 'target_avg_price'), Icons.flag_circle_rounded),
            const SizedBox(height: 12),
            _buildTextField(_purchasePriceController, L10n.s(lang, 'purchase_price'), Icons.shopping_cart_rounded),
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: _saveToPortfolio,
                style: ElevatedButton.styleFrom(
                  backgroundColor: NeonColors.cyan,
                  foregroundColor: Colors.black,
                  padding: const EdgeInsets.all(16),
                ),
                icon: const Icon(Icons.bookmark_add_rounded),
                label: Text(L10n.s(lang, 'save_to_portfolio')),
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _showVoiceInput(BuildContext context, {TextEditingController? targetController}) {
    final lang = ref.read(languageProvider);
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => Container(
        height: 300,
        decoration: const BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.only(topLeft: Radius.circular(32), topRight: Radius.circular(32)),
        ),
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            children: [
              Container(width: 40, height: 4, decoration: BoxDecoration(color: Colors.grey[300], borderRadius: BorderRadius.circular(2))),
              const SizedBox(height: 32),
              const Icon(Icons.mic_rounded, size: 64, color: OneUIColors.kakaoYellow),
              Text(L10n.s(lang, 'ready_msg'), style: Theme.of(context).textTheme.titleLarge?.copyWith(color: OneUIColors.kakaoBrown)),
              const SizedBox(height: 24),
              Text(L10n.s(lang, 'voice_price_hint'), style: Theme.of(context).textTheme.bodyMedium),
              const Spacer(),
              ElevatedButton(
                onPressed: () => Navigator.pop(context),
                style: ElevatedButton.styleFrom(backgroundColor: NeonColors.cyan, foregroundColor: Colors.black),
                child: Text(L10n.s(lang, 'close')),
              ),
            ],
          ),
        ),
      ),
    );
  }


  Widget _buildComparisonChart(BuildContext context, LanguageType lang) {
    if (_resultA == null) return const SizedBox.shrink();

    final ip = _parseVal(_initialPriceController.text);
    final np = _resultA!.averagePrice;
    
    final maxVal = (ip > np ? ip : np) * 1.1;

    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.black, width: 2),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(L10n.s(lang, 'comparison_view'), style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 13, color: Colors.grey)),
          const SizedBox(height: 24),
          _buildBar(context, L10n.s(lang, 'current_avg'), ip, maxVal, Colors.white12),
          const SizedBox(height: 16),
          _buildBar(context, L10n.s(lang, 'after_sim'), np, maxVal, NeonColors.cyan, isBold: true),
        ],
      ),
    );
  }

  Widget _buildBar(BuildContext context, String label, double value, double max, Color color, {bool isBold = false}) {
    final widthFactor = (value / max).clamp(0.05, 1.0);
    
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(label, style: TextStyle(fontWeight: isBold ? FontWeight.w900 : FontWeight.w700, fontSize: 12)),
            Text(_currencyFormat.format(value), style: GoogleFonts.notoSansMono(fontWeight: FontWeight.w900, fontSize: 12)),
          ],
        ),
        const SizedBox(height: 8),
        Stack(
          children: [
            Container(height: 12, width: double.infinity, decoration: BoxDecoration(color: Colors.grey[200], borderRadius: BorderRadius.circular(6))),
            FractionallySizedBox(
              widthFactor: widthFactor,
              child: Container(
                height: 12, 
                decoration: BoxDecoration(
                  color: color, 
                  borderRadius: BorderRadius.circular(6),
                  border: isBold ? Border.all(color: Colors.black, width: 1.5) : null,
                ),
              ),
            ),
          ],
        ),
      ],
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
    
    // Calculate cursor position
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
