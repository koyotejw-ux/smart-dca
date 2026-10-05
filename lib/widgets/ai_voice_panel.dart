import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';

import '../theme/t_membership_colors.dart';
import '../models/scenario_model.dart';
import '../services/calculator_service.dart';
import '../screens/simulator_screen.dart';

class AiVoicePanel extends ConsumerStatefulWidget {
  const AiVoicePanel({super.key});

  @override
  ConsumerState<AiVoicePanel> createState() => _AiVoicePanelState();
}

class _AiVoicePanelState extends ConsumerState<AiVoicePanel> with SingleTickerProviderStateMixin {
  late AnimationController _pulseController;
  final TextEditingController _inputController = TextEditingController();

  bool _isListening = false;
  String _recognizedText = "삼성전자 75,000원 100주, 68,000원에 50주 물타기";
  
  // Parsed simulation state
  String _parsedStock = "삼성전자";
  double _initialPrice = 75000;
  double _initialQty = 100;
  double _targetBuyPrice = 68000;
  double _targetBuyQty = 50;
  bool _isParsed = true;

  final List<String> _presetPrompts = [
    "삼성전자 75,000원 100주, 68,000원에 50주 물타기",
    "비트코인 95,000,000원 2개, 88,000,000원에 1개 추가",
    "애플 180달러 30주, 165달러에 20주 매수",
    "카카오 52,000원 80주, 43,000원에 40주 물타기",
  ];

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1400),
    )..repeat(reverse: true);

    _inputController.text = _recognizedText;
    _parsePrompt(_recognizedText);
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
      _recognizedText = "음성을 듣고 분석하는 중입니다...";
    });

    Future.delayed(const Duration(milliseconds: 900), () {
      if (!mounted) return;
      HapticFeedback.lightImpact();
      setState(() {
        _isListening = false;
        _recognizedText = prompt;
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
                color: Colors.grey.withOpacity(0.3),
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
                        const SizedBox(width: 8),
                        Text(
                          "스마트 음성 물타기 비서",
                          style: GoogleFonts.inter(
                            fontSize: 18,
                            fontWeight: FontWeight.w900,
                            color: isDark ? TMembershipColors.darkTextPrimary : TMembershipColors.lightTextPrimary,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 6),
                    Text(
                      "자산명, 현재 평단가/수량, 추가 매수 가격을 자연스럽게 말씀하세요.",
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        fontSize: 12,
                        color: isDark ? TMembershipColors.darkTextSecondary : TMembershipColors.lightTextSecondary,
                      ),
                    ),
                    const SizedBox(height: 20),

                    // Voice Wave / Mic Button
                    ScaleTransition(
                      scale: Tween<double>(begin: 0.95, end: 1.05).animate(
                        CurvedAnimation(parent: _pulseController, curve: Curves.easeInOut),
                      ),
                      child: GestureDetector(
                        onTap: () => _simulateVoiceListening(_presetPrompts[0]),
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
                    const SizedBox(height: 12),
                    Text(
                      _isListening ? "음성 청취 및 파싱 중..." : "마이크 터치하여 음성 인식 시작",
                      style: TextStyle(
                        fontSize: 13,
                        fontWeight: FontWeight.w700,
                        color: _isListening ? TMembershipColors.accentCoral : TMembershipColors.primaryBlue,
                      ),
                    ),
                    const SizedBox(height: 20),

                    // Preset Quick Chips
                    Align(
                      alignment: Alignment.centerLeft,
                      child: Text(
                        "자주 쓰는 음성 예시 터치하기",
                        style: TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.w800,
                          color: isDark ? TMembershipColors.darkTextTertiary : TMembershipColors.lightTextTertiary,
                        ),
                      ),
                    ),
                    const SizedBox(height: 8),
                    Wrap(
                      spacing: 8,
                      runSpacing: 8,
                      children: _presetPrompts.map((prompt) {
                        return ActionChip(
                          backgroundColor: isDark ? Colors.white.withOpacity(0.06) : Colors.black.withOpacity(0.04),
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
                    const SizedBox(height: 16),

                    // Editable Recognized Query
                    TextField(
                      controller: _inputController,
                      style: TextStyle(
                        fontSize: 13,
                        fontWeight: FontWeight.w600,
                        color: isDark ? Colors.white : Colors.black87,
                      ),
                      decoration: InputDecoration(
                        labelText: "인식된 명령문 (직접 수정 가능)",
                        prefixIcon: const Icon(Icons.edit_note_rounded, size: 20),
                        filled: true,
                        fillColor: isDark ? Colors.black26 : Colors.grey.withOpacity(0.08),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(16),
                          borderSide: BorderSide.none,
                        ),
                      ),
                      onChanged: (val) {
                        _recognizedText = val;
                        _parsePrompt(val);
                      },
                    ),
                    const SizedBox(height: 16),

                    // Parsed Data Preview Card
                    if (_isParsed)
                      Container(
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          gradient: LinearGradient(
                            colors: isDark
                                ? [TMembershipColors.darkSurface, const Color(0xFF1E2846)]
                                : [Colors.blue.shade50, Colors.purple.shade50],
                          ),
                          borderRadius: BorderRadius.circular(18),
                          border: Border.all(
                            color: TMembershipColors.primaryBlue.withOpacity(0.3),
                          ),
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                const Icon(Icons.check_circle_rounded, color: TMembershipColors.accentMint, size: 18),
                                const SizedBox(width: 6),
                                Text(
                                  "AI 파싱 완료: $_parsedStock",
                                  style: GoogleFonts.inter(fontWeight: FontWeight.w800, fontSize: 14),
                                ),
                              ],
                            ),
                            const SizedBox(height: 10),
                            Row(
                              children: [
                                Expanded(
                                  child: _buildParsedTag("현재 평단가", "${_initialPrice.toStringAsFixed(0)}원"),
                                ),
                                const SizedBox(width: 8),
                                Expanded(
                                  child: _buildParsedTag("보유 수량", "${_initialQty.toStringAsFixed(0)}주"),
                                ),
                              ],
                            ),
                            const SizedBox(height: 8),
                            Row(
                              children: [
                                Expanded(
                                  child: _buildParsedTag("추가 매수가", "${_targetBuyPrice.toStringAsFixed(0)}원"),
                                ),
                                const SizedBox(width: 8),
                                Expanded(
                                  child: _buildParsedTag("추가 수량", "${_targetBuyQty.toStringAsFixed(0)}주"),
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

            // Action Buttons
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
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
                    child: OutlinedButton(
                      onPressed: () => Navigator.pop(context),
                      style: OutlinedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 14),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                      ),
                      child: const Text("닫기", style: TextStyle(fontWeight: FontWeight.bold)),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    flex: 2,
                    child: ElevatedButton.icon(
                      onPressed: _isParsed ? _applyToSimulator : null,
                      icon: const Icon(Icons.calculate_rounded, color: Colors.white, size: 20),
                      label: const Text(
                        "시뮬레이터에 적용하기",
                        style: TextStyle(fontWeight: FontWeight.w900, color: Colors.white),
                      ),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: TMembershipColors.primaryBlue,
                        padding: const EdgeInsets.symmetric(vertical: 14),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                        elevation: 4,
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
