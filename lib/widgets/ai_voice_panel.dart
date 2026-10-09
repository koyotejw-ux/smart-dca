import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';

import '../theme/t_membership_colors.dart';
import '../models/scenario_model.dart';
import '../services/calculator_service.dart';
import '../screens/simulator_screen.dart';
import '../providers/language_provider.dart';
import '../providers/currency_provider.dart';
import '../utils/l10n.dart';

class AiVoicePanel extends ConsumerStatefulWidget {
  const AiVoicePanel({super.key});

  @override
  ConsumerState<AiVoicePanel> createState() => _AiVoicePanelState();
}

class _AiVoicePanelState extends ConsumerState<AiVoicePanel> with SingleTickerProviderStateMixin {
  late AnimationController _pulseController;
  final TextEditingController _inputController = TextEditingController();

  bool _isListening = false;
  
  // Parsed simulation state
  String _parsedStock = "AAPL";
  double _initialPrice = 180;
  double _initialQty = 50;
  double _targetBuyPrice = 150;
  double _targetBuyQty = 30;
  bool _isParsed = true;

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1400),
    )..repeat(reverse: true);

    WidgetsBinding.instance.addPostFrameCallback((_) {
      final lang = ref.read(languageProvider);
      final initialPrompt = _getDefaultPrompt(lang);
      setState(() {
        _inputController.text = initialPrompt;
        _parsePrompt(initialPrompt);
      });
    });
  }

  String _getDefaultPrompt(LanguageType lang) {
    switch (lang) {
      case LanguageType.ko:
        return "삼성전자 75,000원 100주, 68,000원에 50주 물타기";
      case LanguageType.ja:
        return "ソニー 12,000円 100株、10,500円で50株 ナンピン";
      case LanguageType.zh:
        return "腾讯控股 380元 100股，340元补仓 50股";
      case LanguageType.es:
        return "Apple 180 USD 100 acc., 150 USD comprar 50 acc.";
      case LanguageType.vi:
        return "Vinamilk 75,000 VND 100 cổ, 65,000 mua 50 cổ";
      case LanguageType.id:
        return "BBCA 9,500 IDR 100 lot, 8,500 beli 50 lot";
      case LanguageType.en:
        return "Apple 180 USD 100 shares, buy 50 shares at 150 USD";
    }
  }

  List<String> _getPresets(LanguageType lang) {
    switch (lang) {
      case LanguageType.ko:
        return [
          "삼성전자 75,000원 100주, 68,000원에 50주 물타기",
          "현대차 240,000원 20주, 210,000원에 10주 추가",
          "애플 180달러 30주, 165달러에 20주 매수",
          "카카오 52,000원 80주, 43,000원에 40주 물타기",
        ];
      case LanguageType.ja:
        return [
          "ソニー 12,000円 100株、10,500円で50株 ナンピン",
          "トヨタ 2,800円 200株、2,400円で100株 買い増し",
          "任天堂 8,200円 50株、7,500円で20株 追加",
        ];
      case LanguageType.zh:
        return [
          "腾讯控股 380元 100股，340元补仓 50股",
          "贵州茅台 1600元 50股，1450元买入 30股",
          "特斯拉 240美元 50股，200美元补仓 40股",
        ];
      case LanguageType.es:
        return [
          "Apple 180 USD 100 acc., comprar 50 acc. a 150 USD",
          "Santander 4.5 EUR 500 acc., añadir 200 acc. a 4.0 EUR",
          "Tesla 220 USD 50 acc., comprar 30 acc. a 190 USD",
        ];
      case LanguageType.vi:
        return [
          "Vinamilk 75,000 VND 100 cổ, mua 50 cổ giá 65,000",
          "FPT 120,000 VND 200 cổ, mua thêm 100 cổ giá 110,000",
          "Vietcombank 90,000 VND 100 cổ, mua 50 cổ giá 82,000",
        ];
      case LanguageType.id:
        return [
          "BBCA 9,500 IDR 100 lot, beli 50 lot di 8,500",
          "BBRI 5,200 IDR 200 lot, tambah 100 lot di 4,600",
          "TLKM 3,800 IDR 150 lot, beli 50 lot di 3,400",
        ];
      case LanguageType.en:
        return [
          "Apple 180 USD 100 shares, buy 50 shares at 150 USD",
          "Tesla 240 USD 50 shares, buy 30 shares at 200 USD",
          "NVIDIA 120 USD 40 shares, add 20 shares at 105 USD",
          "Microsoft 420 USD 40 shares, buy 20 shares at 380 USD",
        ];
    }
  }

  @override
  void dispose() {
    _pulseController.dispose();
    _inputController.dispose();
    super.dispose();
  }

  void _simulateVoiceListening(String prompt) {
    HapticFeedback.mediumImpact();
    setState(() {
      _isListening = true;
    });

    Future.delayed(const Duration(milliseconds: 900), () {
      if (!mounted) return;
      HapticFeedback.lightImpact();
      setState(() {
        _isListening = false;
        _inputController.text = prompt;
        _parsePrompt(prompt);
      });
    });
  }

  void _parsePrompt(String text) {
    // Basic Korean natural language parsing for stock, price, qty, and second batch
    // Example: "삼성전자 75,000원 100주, 68,000원에 50주 물타기"
    try {
      final cleanText = text.replaceAll(',', '').replaceAll('원', ' ').replaceAll('달러', ' ').replaceAll('주', ' ').replaceAll('개', ' ');
      final tokens = cleanText.split(RegExp(r'\s+')).where((t) => t.trim().isNotEmpty).toList();

      String stock = "선택 종목";
      List<double> numbers = [];

      for (var token in tokens) {
        final parsed = double.tryParse(token);
        if (parsed != null) {
          numbers.add(parsed);
        } else if (stock == "선택 종목" && token.length > 1 && !token.contains('물타기') && !token.contains('매수') && !token.contains('추가')) {
          stock = token;
        }
      }

      setState(() {
        _parsedStock = stock;
        if (numbers.length >= 2) {
          _initialPrice = numbers[0];
          _initialQty = numbers[1];
        }
        if (numbers.length >= 4) {
          _targetBuyPrice = numbers[2];
          _targetBuyQty = numbers[3];
        } else if (numbers.length >= 3) {
          _targetBuyPrice = numbers[2];
          _targetBuyQty = 10;
        }
        _isParsed = numbers.length >= 2;
      });
    } catch (_) {
      setState(() => _isParsed = false);
    }
  }

  void _applyToSimulator() {
    HapticFeedback.heavyImpact();
    final batch = PurchaseBatch(
      price: _targetBuyPrice,
      quantity: _targetBuyQty,
    );

    final scenario = Scenario(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      name: 'AI: $_parsedStock 물타기 전략',
      initialPrice: _initialPrice,
      initialQuantity: _initialQty,
      batches: [batch],
      createdAt: DateTime.now(),
    );

    Navigator.pop(context); // close bottom sheet
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => SimulatorScreen(initialScenario: scenario),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(languageProvider);
    final currency = ref.watch(currencyProvider);
    final presets = _getPresets(lang);
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final bottomInset = MediaQuery.of(context).viewInsets.bottom;

    return AnimatedPadding(
      padding: EdgeInsets.only(bottom: bottomInset),
      duration: const Duration(milliseconds: 200),
      child: Container(
        constraints: BoxConstraints(
          maxHeight: MediaQuery.of(context).size.height * 0.88,
        ),
        decoration: BoxDecoration(
          color: isDark ? TMembershipColors.darkSurface : TMembershipColors.lightSurface,
          borderRadius: const BorderRadius.vertical(top: Radius.circular(32)),
          boxShadow: TMembershipColors.softShadow(blur: 24, dy: -4),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            // Handle bar
            const SizedBox(height: 12),
            Container(
              width: 44,
              height: 5,
              decoration: BoxDecoration(
                color: Colors.grey.withValues(alpha: 0.3),
                borderRadius: BorderRadius.circular(3),
              ),
            ),
            const SizedBox(height: 16),

            // Scrollable Content
            Flexible(
              child: SingleChildScrollView(
                padding: const EdgeInsets.symmetric(horizontal: 20),
                child: Column(
                  children: [
                    // Header title with AI gradient badge
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                          decoration: BoxDecoration(
                            gradient: TMembershipColors.primaryGradient,
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: const Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Icon(Icons.auto_awesome_rounded, color: Colors.white, size: 14),
                              SizedBox(width: 4),
                              Text("AI Assistant", style: TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.bold)),
                            ],
                          ),
                        ),
                        const SizedBox(width: 10),
                        Flexible(
                          child: FittedBox(
                            fit: BoxFit.scaleDown,
                            child: Text(
                              L10n.s(lang, 'voice_panel_title'),
                              style: GoogleFonts.inter(
                                fontSize: 17,
                                fontWeight: FontWeight.w900,
                                color: isDark ? TMembershipColors.darkTextPrimary : TMembershipColors.lightTextPrimary,
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 8),
                    Text(
                      L10n.s(lang, 'voice_panel_desc'),
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        fontSize: 12,
                        color: isDark ? TMembershipColors.darkTextSecondary : TMembershipColors.lightTextSecondary,
                      ),
                    ),
                    const SizedBox(height: 24),

                    // Voice Wave / Mic Button
                    ScaleTransition(
                      scale: Tween<double>(begin: 0.95, end: 1.05).animate(
                        CurvedAnimation(parent: _pulseController, curve: Curves.easeInOut),
                      ),
                      child: GestureDetector(
                        onTap: () => _simulateVoiceListening(presets.first),
                        child: Container(
                          width: 80,
                          height: 80,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            gradient: _isListening
                                ? const LinearGradient(colors: [Colors.deepOrange, Colors.redAccent])
                                : TMembershipColors.primaryGradient,
                            boxShadow: TMembershipColors.colorfulGlow(
                              _isListening ? Colors.redAccent : TMembershipColors.primaryBlue,
                              opacity: 0.5,
                            ),
                          ),
                          child: Icon(
                            _isListening ? Icons.graphic_eq_rounded : Icons.mic_rounded,
                            color: Colors.white,
                            size: 40,
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(height: 14),
                    Text(
                      _isListening ? L10n.s(lang, 'voice_listening') : L10n.s(lang, 'voice_tap_hint'),
                      style: TextStyle(
                        fontSize: 13,
                        fontWeight: FontWeight.w700,
                        color: _isListening ? TMembershipColors.accentCoral : TMembershipColors.primaryBlue,
                      ),
                    ),
                    const SizedBox(height: 24),

                    // Preset Quick Chips
                    Align(
                      alignment: Alignment.centerLeft,
                      child: Text(
                        L10n.s(lang, 'voice_quick_examples'),
                        style: TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.w800,
                          color: isDark ? TMembershipColors.darkTextTertiary : TMembershipColors.lightTextTertiary,
                        ),
                      ),
                    ),
                    const SizedBox(height: 10),
                    Wrap(
                      spacing: 8,
                      runSpacing: 8,
                      children: presets.map((prompt) {
                        return ActionChip(
                          backgroundColor: isDark ? Colors.white.withValues(alpha: 0.06) : Colors.black.withValues(alpha: 0.04),
                          side: BorderSide(
                            color: isDark ? TMembershipColors.darkCardBorder : TMembershipColors.lightCardBorder,
                          ),
                          label: Text(
                            prompt,
                            style: TextStyle(
                              fontSize: 12,
                              color: isDark ? Colors.white70 : Colors.black87,
                            ),
                          ),
                          onPressed: () => _simulateVoiceListening(prompt),
                        );
                      }).toList(),
                    ),
                    const SizedBox(height: 20),

                    // Editable Recognized Query
                    TextField(
                      controller: _inputController,
                      style: TextStyle(
                        fontSize: 13,
                        fontWeight: FontWeight.w600,
                        color: isDark ? Colors.white : Colors.black87,
                      ),
                      decoration: InputDecoration(
                        labelText: L10n.s(lang, 'voice_query_label'),
                        prefixIcon: const Icon(Icons.edit_note_rounded, size: 20),
                        filled: true,
                        fillColor: isDark ? Colors.black26 : Colors.grey.withValues(alpha: 0.08),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(16),
                          borderSide: BorderSide.none,
                        ),
                      ),
                      onChanged: (val) {
                        _parsePrompt(val);
                      },
                    ),
                    const SizedBox(height: 20),

                    // Parsed Data Preview Card
                    if (_isParsed)
                      Container(
                        padding: const EdgeInsets.all(18),
                        decoration: BoxDecoration(
                          gradient: LinearGradient(
                            colors: isDark
                                ? [TMembershipColors.darkSurface, const Color(0xFF1E2846)]
                                : [Colors.blue.shade50, Colors.purple.shade50],
                          ),
                          borderRadius: BorderRadius.circular(20),
                          border: Border.all(
                            color: TMembershipColors.primaryBlue.withValues(alpha: 0.3),
                          ),
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                const Icon(Icons.check_circle_rounded, color: TMembershipColors.accentMint, size: 18),
                                const SizedBox(width: 8),
                                Expanded(
                                  child: FittedBox(
                                    fit: BoxFit.scaleDown,
                                    alignment: Alignment.centerLeft,
                                    child: Text(
                                      "${L10n.s(lang, 'voice_parsed_success')}: $_parsedStock",
                                      style: GoogleFonts.inter(fontWeight: FontWeight.w800, fontSize: 14),
                                    ),
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 14),
                            Row(
                              children: [
                                Expanded(
                                  child: _buildParsedTag(L10n.s(lang, 'current_avg_label'), "${currency.symbol}${_initialPrice.toStringAsFixed(currency.decimalDigits)}"),
                                ),
                                const SizedBox(width: 12),
                                Expanded(
                                  child: _buildParsedTag(L10n.s(lang, 'current_qty_label'), "${_initialQty.toStringAsFixed(0)} ${L10n.s(lang, 'unit_share')}"),
                                ),
                              ],
                            ),
                            const SizedBox(height: 10),
                            Row(
                              children: [
                                Expanded(
                                  child: _buildParsedTag(L10n.s(lang, 'batch_price_label'), "${currency.symbol}${_targetBuyPrice.toStringAsFixed(currency.decimalDigits)}"),
                                ),
                                const SizedBox(width: 12),
                                Expanded(
                                  child: _buildParsedTag(L10n.s(lang, 'batch_qty_label'), "${_targetBuyQty.toStringAsFixed(0)} ${L10n.s(lang, 'unit_share')}"),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    const SizedBox(height: 24),
                  ],
                ),
              ),
            ),

            // Action Buttons with Safe Area for navigation bar
            Container(
              padding: EdgeInsets.fromLTRB(
                20,
                16,
                20,
                16 + MediaQuery.paddingOf(context).bottom,
              ),
              decoration: BoxDecoration(
                color: isDark ? TMembershipColors.darkSurface : TMembershipColors.lightSurface,
                border: Border(
                  top: BorderSide(
                    color: isDark ? TMembershipColors.darkDivider : TMembershipColors.lightDivider,
                  ),
                ),
              ),
              child: LayoutBuilder(
                builder: (context, constraints) {
                  final isNarrow = constraints.maxWidth < 320;
                  final closeBtn = OutlinedButton(
                    onPressed: () => Navigator.pop(context),
                    style: OutlinedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 14),
                      minimumSize: const Size(double.infinity, 48),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                    ),
                    child: FittedBox(
                      fit: BoxFit.scaleDown,
                      child: Text(
                        L10n.s(lang, 'close_btn'),
                        maxLines: 1,
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                    ),
                  );

                  final applyBtn = ElevatedButton.icon(
                    onPressed: _isParsed ? _applyToSimulator : null,
                    icon: const Icon(Icons.calculate_rounded, color: Colors.white, size: 20),
                    label: FittedBox(
                      fit: BoxFit.scaleDown,
                      child: Text(
                        L10n.s(lang, 'apply_to_sim_btn'),
                        maxLines: 1,
                        style: const TextStyle(fontWeight: FontWeight.w900, color: Colors.white),
                      ),
                    ),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: TMembershipColors.primaryBlue,
                      padding: const EdgeInsets.symmetric(vertical: 14),
                      minimumSize: const Size(double.infinity, 48),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                      elevation: 4,
                    ),
                  );

                  if (isNarrow) {
                    return Column(
                      children: [
                        applyBtn,
                        const SizedBox(height: 10),
                        closeBtn,
                      ],
                    );
                  }

                  return Row(
                    children: [
                      Expanded(flex: 1, child: closeBtn),
                      const SizedBox(width: 12),
                      Expanded(flex: 2, child: applyBtn),
                    ],
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildParsedTag(String label, String value) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.12),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(label, style: const TextStyle(fontSize: 10, color: Colors.grey)),
          const SizedBox(height: 2),
          Text(value, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }
}
