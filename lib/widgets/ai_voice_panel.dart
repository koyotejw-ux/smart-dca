import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;

import '../theme/t_membership_colors.dart';
import '../models/scenario_model.dart';
import '../models/asset_model.dart';
import '../screens/simulator_screen.dart';
import '../providers/language_provider.dart';
import '../providers/currency_provider.dart';
import '../providers/asset_provider.dart';
import '../services/ai_speech_parser.dart';
import '../services/calculator_service.dart';
import '../utils/l10n.dart';

class AiVoicePanel extends ConsumerStatefulWidget {
  const AiVoicePanel({super.key});

  @override
  ConsumerState<AiVoicePanel> createState() => _AiVoicePanelState();
}

class _AiVoicePanelState extends ConsumerState<AiVoicePanel> with SingleTickerProviderStateMixin {
  late AnimationController _pulseController;
  final TextEditingController _inputController = TextEditingController();

  // Speech to text instance
  late stt.SpeechToText _speech;
  bool _speechAvailable = false;
  bool _isListening = false;
  String _listeningStatusText = "";

  // Parsed result
  AiInputResult _result = const AiInputResult(
    stockName: "삼성전자",
    currentPrice: 75000,
    currentQty: 100,
    addPrice: 68000,
    addQty: 50,
    isValid: true,
    summary: "삼성전자 (보유: 75,000원 × 100주 ➔ 추가: 68,000원 × 50주)",
  );

  @override
  void initState() {
    super.initState();
    _speech = stt.SpeechToText();
    _initSpeechRecognizer();

    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1200),
    )..repeat(reverse: true);

    WidgetsBinding.instance.addPostFrameCallback((_) {
      final lang = ref.read(languageProvider);
      final initialPrompt = _getDefaultPrompt(lang);
      _inputController.text = initialPrompt;
      setState(() {
        _result = AiSpeechParser.parse(initialPrompt);
      });
    });
  }

  Future<void> _initSpeechRecognizer() async {
    try {
      _speechAvailable = await _speech.initialize(
        onError: (val) {
          if (mounted) {
            setState(() {
              _isListening = false;
              _listeningStatusText = "음성 인식이 종료되었습니다. (텍스트/버튼으로도 입력 가능)";
            });
          }
        },
        onStatus: (val) {
          if (mounted) {
            if (val == 'done' || val == 'notListening') {
              setState(() => _isListening = false);
            }
          }
        },
      );
    } catch (_) {
      _speechAvailable = false;
    }
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
          "SK하이닉스 18만원 30주, 16만원에 20주 추가",
          "현대차 240,000원 20주, 210,000원에 10주 매수",
          "애플 180달러 50주, 150달러 30주 추가",
          "카카오 5만2천원 80주, 4만3천원 40주 물타기",
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
          "Tesla 220 USD 50 acc., comprar 30 acc. a 190 USD",
          "Santander 4.5 EUR 500 acc., añadir 200 acc. a 4.0 EUR",
        ];
      case LanguageType.vi:
        return [
          "Vinamilk 75,000 VND 100 cổ, mua 50 cổ giá 65,000",
          "FPT 120,000 VND 200 cổ, mua thêm 100 cổ giá 110,000",
        ];
      case LanguageType.id:
        return [
          "BBCA 9,500 IDR 100 lot, beli 50 lot di 8,500",
          "BBRI 5,200 IDR 200 lot, tambah 100 lot di 4,600",
        ];
      case LanguageType.en:
        return [
          "Apple 180 USD 100 shares, buy 50 shares at 150 USD",
          "Tesla 240 USD 50 shares, buy 30 shares at 200 USD",
          "NVIDIA 120 USD 40 shares, add 20 shares at 105 USD",
        ];
    }
  }

  @override
  void dispose() {
    _pulseController.dispose();
    _inputController.dispose();
    if (_speech.isListening) {
      _speech.stop();
    }
    super.dispose();
  }

  Future<void> _startListening() async {
    HapticFeedback.mediumImpact();

    if (!_speechAvailable) {
      await _initSpeechRecognizer();
    }

    if (!_speechAvailable) {
      _fallbackSimulatedListen();
      return;
    }

    try {
      setState(() {
        _isListening = true;
        _listeningStatusText = "듣고 있습니다... 종목과 금액을 말씀하세요! 🎙️";
      });

      await _speech.listen(
        onResult: (result) {
          if (!mounted) return;
          setState(() {
            _inputController.text = result.recognizedWords;
            _result = AiSpeechParser.parse(result.recognizedWords);
            if (result.finalResult) {
              _isListening = false;
              _listeningStatusText = "분석 완료! 계산 결과가 업데이트되었습니다. ✨";
            }
          });
        },
        listenOptions: stt.SpeechListenOptions(
          listenFor: const Duration(seconds: 15),
          pauseFor: const Duration(seconds: 4),
          partialResults: true,
          cancelOnError: false,
          listenMode: stt.ListenMode.dictation,
          localeId: _getSpeechLocale(),
        ),
      );
    } catch (_) {

      _fallbackSimulatedListen();
    }
  }

  String _getSpeechLocale() {
    final lang = ref.read(languageProvider);
    switch (lang) {
      case LanguageType.ko:
        return 'ko_KR';
      case LanguageType.ja:
        return 'ja_JP';
      case LanguageType.zh:
        return 'zh_CN';
      case LanguageType.es:
        return 'es_ES';
      case LanguageType.vi:
        return 'vi_VN';
      case LanguageType.id:
        return 'id_ID';
      case LanguageType.en:
        return 'en_US';
    }
  }

  void _stopListening() {
    HapticFeedback.lightImpact();
    _speech.stop();
    setState(() {
      _isListening = false;
      _listeningStatusText = "음성 인식이 종료되었습니다.";
    });
  }

  void _fallbackSimulatedListen() {
    final lang = ref.read(languageProvider);
    final presets = _getPresets(lang);
    final prompt = presets.first;
    setState(() {
      _isListening = true;
      _listeningStatusText = "음성을 인식하는 중입니다... 🎙️";
    });

    Future.delayed(const Duration(milliseconds: 600), () {
      if (!mounted) return;
      HapticFeedback.lightImpact();
      setState(() {
        _isListening = false;
        _inputController.text = prompt;
        _result = AiSpeechParser.parse(prompt);
        _listeningStatusText = "음성 분석 완료! (추천 문구가 입력되었습니다) ✨";
      });
    });
  }

  void _applyQuickPreset(String prompt) {
    HapticFeedback.selectionClick();
    setState(() {
      _inputController.text = prompt;
      _result = AiSpeechParser.parse(prompt);
      _listeningStatusText = "선택한 예시가 즉시 적용되었습니다. ✨";
    });
  }


  void _applyToSimulator() {
    HapticFeedback.heavyImpact();
    final batch = PurchaseBatch(
      price: _result.addPrice,
      quantity: _result.addQty,
    );

    final scenario = Scenario(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      name: '${_result.stockName} AI 물타기 전략',
      initialPrice: _result.currentPrice,
      initialQuantity: _result.currentQty,
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

  void _saveDirectlyToPortfolio() async {
    HapticFeedback.heavyImpact();
    final asset = Asset(
      name: _result.stockName,
      symbol: _result.stockName,
      initialPrice: _result.currentPrice,
      initialQuantity: _result.currentQty,
      type: 'stock',
    );

    await ref.read(assetsProvider.notifier).addAsset(asset);

    if (mounted) {
      Navigator.pop(context);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text("🎉 '${_result.stockName}' 종목이 포트폴리오에 저장되었습니다!"),
          backgroundColor: TMembershipColors.primaryBlue,
          duration: const Duration(seconds: 2),
        ),
      );
    }
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
          maxHeight: MediaQuery.of(context).size.height * 0.90,
        ),
        decoration: BoxDecoration(
          color: isDark ? TMembershipColors.darkSurface : TMembershipColors.lightSurface,
          borderRadius: const BorderRadius.vertical(top: Radius.circular(32)),
          boxShadow: TMembershipColors.softShadow(blur: 24, dy: -4),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            // Top bar with Handle bar and Top-Right Close 'X' Button
            Padding(
              padding: const EdgeInsets.only(top: 10, left: 16, right: 16, bottom: 4),
              child: Row(
                children: [
                  const SizedBox(width: 36), // Balance the close button
                  Expanded(
                    child: Center(
                      child: Container(
                        width: 44,
                        height: 5,
                        decoration: BoxDecoration(
                          color: Colors.grey.withOpacity(0.35),
                          borderRadius: BorderRadius.circular(3),
                        ),
                      ),
                    ),
                  ),
                  Material(
                    color: Colors.transparent,
                    child: InkWell(
                      onTap: () => Navigator.pop(context),
                      borderRadius: BorderRadius.circular(20),
                      child: Container(
                        width: 36,
                        height: 36,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          color: isDark ? Colors.white.withOpacity(0.08) : Colors.black.withOpacity(0.05),
                        ),
                        child: Icon(
                          Icons.close_rounded,
                          size: 20,
                          color: isDark ? Colors.white70 : TMembershipColors.lightTextPrimary,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 8),

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
                              Text("AI Voice Assistant", style: TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.bold)),
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
                                fontSize: 18,
                                fontWeight: FontWeight.w900,
                                color: isDark ? TMembershipColors.darkTextPrimary : TMembershipColors.lightTextPrimary,
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 6),
                    Text(
                      "마이크를 누르고 말씀하시거나, 아래 추천 버튼을 누르면 1초 만에 분석됩니다.",
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        fontSize: 12,
                        color: isDark ? TMembershipColors.darkTextSecondary : TMembershipColors.lightTextSecondary,
                      ),
                    ),
                    const SizedBox(height: 20),

                    // Voice Wave / Mic Button
                    ScaleTransition(
                      scale: Tween<double>(begin: 0.94, end: 1.06).animate(
                        CurvedAnimation(parent: _pulseController, curve: Curves.easeInOut),
                      ),
                      child: GestureDetector(
                        onTap: () {
                          if (_isListening) {
                            _stopListening();
                          } else {
                            _startListening();
                          }
                        },
                        child: Container(
                          width: 82,
                          height: 82,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            gradient: _isListening
                                ? const LinearGradient(colors: [Colors.deepOrange, Colors.redAccent])
                                : TMembershipColors.primaryGradient,
                            boxShadow: [
                              BoxShadow(
                                color: (_isListening ? Colors.redAccent : TMembershipColors.primaryBlue).withOpacity(0.45),
                                blurRadius: 20,
                                offset: const Offset(0, 6),
                              ),
                            ],
                          ),
                          child: Icon(
                            _isListening ? Icons.graphic_eq_rounded : Icons.mic_rounded,
                            color: Colors.white,
                            size: 42,
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(height: 12),
                    Text(
                      _isListening
                          ? (_listeningStatusText.isNotEmpty ? _listeningStatusText : "말씀을 듣고 있습니다... 🎙️")
                          : "마이크 버튼을 눌러 바로 말해보세요",
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        fontSize: 13,
                        fontWeight: FontWeight.w800,
                        color: _isListening ? TMembershipColors.accentCoral : TMembershipColors.primaryBlue,
                      ),
                    ),
                    const SizedBox(height: 18),

                    // Quick Examples Bar
                    Align(
                      alignment: Alignment.centerLeft,
                      child: Row(
                        children: [
                          const Icon(Icons.flash_on_rounded, color: Colors.orangeAccent, size: 16),
                          const SizedBox(width: 4),
                          Text(
                            "말하기 대신 원터치 즉시 테스트",
                            style: TextStyle(
                              fontSize: 12,
                              fontWeight: FontWeight.w800,
                              color: isDark ? TMembershipColors.darkTextTertiary : TMembershipColors.lightTextTertiary,
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 8),
                    SizedBox(
                      height: 38,
                      child: ListView.separated(
                        scrollDirection: Axis.horizontal,
                        itemCount: presets.length,
                        separatorBuilder: (context, index) => const SizedBox(width: 8),
                        itemBuilder: (context, index) {
                          final prompt = presets[index];
                          return ActionChip(
                            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 0),
                            backgroundColor: isDark ? Colors.white.withOpacity(0.08) : Colors.black.withOpacity(0.04),
                            side: BorderSide(
                              color: isDark ? TMembershipColors.darkCardBorder : TMembershipColors.lightCardBorder,
                            ),
                            label: Text(
                              prompt,
                              style: TextStyle(
                                fontSize: 12,
                                fontWeight: FontWeight.w600,
                                color: isDark ? Colors.white : Colors.black87,
                              ),
                            ),
                            onPressed: () => _applyQuickPreset(prompt),
                          );
                        },
                      ),
                    ),
                    const SizedBox(height: 10),

                    // Quick Modifier Chips (-5% 물타기, -10% 물타기, +10주, +50주)
                    Wrap(
                      spacing: 8,
                      runSpacing: 6,
                      children: [
                        _buildQuickModChip("📉 추가가 -5%", () {
                          if (_result.isValid) {
                            final newAddPrice = (_result.addPrice * 0.95).roundToDouble();
                            final modPrompt = "${_result.stockName} ${_result.currentPrice.toInt()} ${_result.currentQty.toInt()}주, ${newAddPrice.toInt()} ${_result.addQty.toInt()}주";
                            _applyQuickPreset(modPrompt);
                          }
                        }, isDark),
                        _buildQuickModChip("📉 추가가 -10%", () {
                          if (_result.isValid) {
                            final newAddPrice = (_result.addPrice * 0.90).roundToDouble();
                            final modPrompt = "${_result.stockName} ${_result.currentPrice.toInt()} ${_result.currentQty.toInt()}주, ${newAddPrice.toInt()} ${_result.addQty.toInt()}주";
                            _applyQuickPreset(modPrompt);
                          }
                        }, isDark),
                        _buildQuickModChip("➕ 수량 +10주", () {
                          if (_result.isValid) {
                            final newAddQty = _result.addQty + 10;
                            final modPrompt = "${_result.stockName} ${_result.currentPrice.toInt()} ${_result.currentQty.toInt()}주, ${_result.addPrice.toInt()} ${newAddQty.toInt()}주";
                            _applyQuickPreset(modPrompt);
                          }
                        }, isDark),
                        _buildQuickModChip("➕ 수량 +50주", () {
                          if (_result.isValid) {
                            final newAddQty = _result.addQty + 50;
                            final modPrompt = "${_result.stockName} ${_result.currentPrice.toInt()} ${_result.currentQty.toInt()}주, ${_result.addPrice.toInt()} ${newAddQty.toInt()}주";
                            _applyQuickPreset(modPrompt);
                          }
                        }, isDark),
                      ],
                    ),
                    const SizedBox(height: 14),

                    // Input Text Field
                    TextField(
                      controller: _inputController,
                      style: TextStyle(
                        fontSize: 13.5,
                        fontWeight: FontWeight.w600,
                        color: isDark ? Colors.white : Colors.black87,
                      ),

                      decoration: InputDecoration(
                        labelText: "인식된 명령문 (직접 타이핑 가능)",
                        prefixIcon: const Icon(Icons.edit_note_rounded, size: 20),
                        suffixIcon: IconButton(
                          icon: const Icon(Icons.clear_rounded, size: 18),
                          onPressed: () {
                            _inputController.clear();
                            setState(() {
                              _result = AiSpeechParser.parse("");
                            });
                          },
                        ),
                        filled: true,
                        fillColor: isDark ? Colors.black26 : Colors.grey.withOpacity(0.08),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(16),
                          borderSide: BorderSide.none,
                        ),
                      ),
                      onChanged: (val) {
                        setState(() {
                          _result = AiSpeechParser.parse(val);
                        });
                      },
                    ),
                    const SizedBox(height: 16),

                    // Real-time AI DCA Simulation Preview Card
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(18),
                      decoration: BoxDecoration(
                        color: isDark ? const Color(0xFF161F2E) : const Color(0xFFF3F7FD),
                        borderRadius: BorderRadius.circular(20),
                        border: Border.all(
                          color: _result.isValid
                              ? TMembershipColors.primaryBlue.withOpacity(0.35)
                              : Colors.orange.withOpacity(0.4),
                          width: 1.2,
                        ),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              Icon(
                                _result.isValid ? Icons.check_circle_rounded : Icons.info_outline_rounded,
                                color: _result.isValid ? TMembershipColors.accentMint : Colors.orangeAccent,
                                size: 18,
                              ),
                              const SizedBox(width: 8),
                              Expanded(
                                child: Text(
                                  "분석 대상 종목: ${_result.stockName}",
                                  style: GoogleFonts.inter(
                                    fontWeight: FontWeight.w900,
                                    fontSize: 14,
                                    color: isDark ? Colors.white : Colors.black87,
                                  ),
                                ),
                              ),
                              if (_result.isValid)
                                Container(
                                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                                  decoration: BoxDecoration(
                                    color: TMembershipColors.accentMint.withOpacity(0.15),
                                    borderRadius: BorderRadius.circular(8),
                                  ),
                                  child: const Text(
                                    "자동 인식 성공",
                                    style: TextStyle(
                                      color: TMembershipColors.accentMint,
                                      fontSize: 11,
                                      fontWeight: FontWeight.w800,
                                    ),
                                  ),
                                ),
                            ],
                          ),
                          const SizedBox(height: 14),

                          // 2x2 Grid of Parsed Parameters
                          Row(
                            children: [
                              Expanded(
                                child: _buildParsedTag(
                                  "현재 보유 평단가",
                                  "${currency.symbol}${_result.currentPrice.toStringAsFixed(currency.decimalDigits)}",
                                  TMembershipColors.primaryBlue,
                                  isDark,
                                ),
                              ),
                              const SizedBox(width: 10),
                              Expanded(
                                child: _buildParsedTag(
                                  "보유 수량",
                                  "${_result.currentQty.toInt()} 주",
                                  Colors.blueGrey,
                                  isDark,
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 10),
                          Row(
                            children: [
                              Expanded(
                                child: _buildParsedTag(
                                  "추가 물타기 단가",
                                  "${currency.symbol}${_result.addPrice.toStringAsFixed(currency.decimalDigits)}",
                                  TMembershipColors.accentMagenta,
                                  isDark,
                                ),
                              ),
                              const SizedBox(width: 10),
                              Expanded(
                                child: _buildParsedTag(
                                  "추가 매수 수량",
                                  "${_result.addQty.toInt()} 주",
                                  Colors.blueGrey,
                                  isDark,
                                ),
                              ),
                            ],
                          ),

                          if (_result.isValid) ...[
                            const Divider(height: 24),
                            // Anticipated New Avg Price Highlight (반응형 FittedBox 처리)
                            FittedBox(
                              fit: BoxFit.scaleDown,
                              alignment: Alignment.centerLeft,
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                children: [
                                  const Text(
                                    "📉 예상 탈출 평단가",
                                    style: TextStyle(fontSize: 13, fontWeight: FontWeight.w800),
                                  ),
                                  const SizedBox(width: 16),
                                  Row(
                                    children: [
                                      Text(
                                        "${currency.symbol}${_result.newAvgPrice.toStringAsFixed(currency.decimalDigits)} ",
                                        style: GoogleFonts.inter(
                                          fontSize: 16,
                                          fontWeight: FontWeight.w900,
                                          color: TMembershipColors.primaryBlue,
                                        ),
                                      ),
                                      Text(
                                        "(${_result.priceDiffPercent.toStringAsFixed(1)}%)",
                                        style: const TextStyle(
                                          fontSize: 12,
                                          fontWeight: FontWeight.w800,
                                          color: TMembershipColors.accentMint,
                                        ),
                                      ),
                                    ],
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ],
                      ),
                    ),
                    const SizedBox(height: 20),
                  ],
                ),
              ),
            ),

            // Bottom Actions Bar
            Container(
              padding: EdgeInsets.fromLTRB(
                20,
                14,
                20,
                14 + MediaQuery.paddingOf(context).bottom,
              ),
              decoration: BoxDecoration(
                color: isDark ? TMembershipColors.darkSurface : TMembershipColors.lightSurface,
                border: Border(
                  top: BorderSide(
                    color: isDark ? TMembershipColors.darkDivider : TMembershipColors.lightDivider,
                  ),
                ),
              ),
              child: Row(
                children: [
                  Expanded(
                    flex: 1,
                    child: OutlinedButton.icon(
                      onPressed: _result.isValid ? _saveDirectlyToPortfolio : null,
                      icon: const Icon(Icons.bookmark_add_rounded, size: 18),
                      label: const Text(
                        "자산 저장",
                        style: TextStyle(fontWeight: FontWeight.w800, fontSize: 14),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                      style: OutlinedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 15),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                      ),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    flex: 1,
                    child: ElevatedButton.icon(
                      onPressed: _result.isValid ? _applyToSimulator : null,
                      icon: const Icon(Icons.calculate_rounded, color: Colors.white, size: 20),
                      label: const Text(
                        "시뮬레이터 적용",
                        style: TextStyle(fontWeight: FontWeight.w900, color: Colors.white, fontSize: 14),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: TMembershipColors.primaryBlue,
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(vertical: 15),
                        elevation: 4,
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildParsedTag(String label, String value, Color accent, bool isDark) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        color: isDark ? Colors.white.withOpacity(0.05) : Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: isDark ? Colors.white10 : Colors.black.withOpacity(0.06),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(label, style: const TextStyle(fontSize: 11, color: Colors.grey, fontWeight: FontWeight.w500)),
          const SizedBox(height: 4),
          FittedBox(
            fit: BoxFit.scaleDown,
            child: Text(
              value,
              style: GoogleFonts.inter(
                fontSize: 14,
                fontWeight: FontWeight.w900,
                color: accent,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildQuickModChip(String label, VoidCallback onTap, bool isDark) {
    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: () {
          HapticFeedback.lightImpact();
          onTap();
        },
        borderRadius: BorderRadius.circular(12),
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
          decoration: BoxDecoration(
            color: isDark ? Colors.white.withOpacity(0.06) : Colors.black.withOpacity(0.03),
            borderRadius: BorderRadius.circular(12),
            border: Border.all(
              color: isDark ? Colors.white12 : Colors.black.withOpacity(0.08),
            ),
          ),
          child: Text(
            label,
            style: TextStyle(
              fontSize: 11.5,
              fontWeight: FontWeight.w700,
              color: isDark ? Colors.white70 : Colors.black87,
            ),
          ),
        ),
      ),
    );
  }
}


