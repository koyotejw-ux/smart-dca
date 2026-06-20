import 'package:flutter/material.dart';
import '../theme/neon_colors.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../theme/one_ui_colors.dart';
import '../utils/l10n.dart';
import '../providers/language_provider.dart';

class AiVoicePanel extends ConsumerStatefulWidget {
  const AiVoicePanel({super.key});

  @override
  ConsumerState<AiVoicePanel> createState() => _AiVoicePanelState();
}

class _AiVoicePanelState extends ConsumerState<AiVoicePanel> {
  String _status = '준비되셨나요? 말씀해 주세요.';

  void _simulate() {
    Future.delayed(const Duration(seconds: 1), () {
      if (mounted) setState(() => _status = '"삼성전자 75,000원 100주"');
    });
  }

  @override
  void initState() {
    super.initState();
    _simulate();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 32),
      decoration: BoxDecoration(
        color: theme.scaffoldBackgroundColor,
        borderRadius: const BorderRadius.vertical(top: Radius.circular(36)),
        border: const Border(top: BorderSide(color: Colors.black, width: 2)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(width: 40, height: 4, decoration: BoxDecoration(color: Colors.black.withOpacity(0.1), borderRadius: BorderRadius.circular(2))),
          const SizedBox(height: 32),
          Container(
            width: 80,
            height: 80,
            decoration: BoxDecoration(
              color: NeonColors.cyan,
              shape: BoxShape.circle,
              border: Border.all(color: Colors.black, width: 2),
            ),
            child: const Icon(Icons.mic_rounded, color: Colors.black, size: 40),
          ),
          const SizedBox(height: 32),
          Text(
            _status,
            textAlign: TextAlign.center,
            style: theme.textTheme.titleMedium?.copyWith(
              fontWeight: FontWeight.w900,
              color: Colors.white70,
            ),
          ),
          const SizedBox(height: 24),
          // Recognized Text Feedback Area
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
            decoration: BoxDecoration(
              color: Colors.black.withOpacity(0.05),
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: Colors.black12),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                const SizedBox(
                  width: 12,
                  height: 12,
                  child: CircularProgressIndicator(strokeWidth: 2, color: OneUIColors.kakaoBrown),
                ),
                const SizedBox(width: 12),
                Text(
                  "인식 중...",
                  style: theme.textTheme.bodySmall?.copyWith(fontWeight: FontWeight.w900, color: OneUIColors.kakaoBrown),
                ),
              ],
            ),
          ),
          const SizedBox(height: 12),
          Text(
            "자산명, 가격, 수량을 순서대로 말씀해 보세요.",
            style: theme.textTheme.bodySmall?.copyWith(color: Colors.black54, fontWeight: FontWeight.w800),
          ),
          const SizedBox(height: 48),
          Row(
            children: [
              Expanded(
                child: OutlinedButton(
                  onPressed: () => Navigator.pop(context),
                  style: OutlinedButton.styleFrom(
                    foregroundColor: OneUIColors.kakaoBrown,
                    side: const BorderSide(color: Colors.black, width: 2),
                    padding: const EdgeInsets.symmetric(vertical: 18),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
                  ),
                  child: const Text("닫기", style: TextStyle(fontWeight: FontWeight.w900)),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: ElevatedButton(
                  onPressed: () {},
                  style: ElevatedButton.styleFrom(
                    backgroundColor: NeonColors.cyan,
                    foregroundColor: Colors.black,
                    side: const BorderSide(color: Colors.black, width: 2),
                    padding: const EdgeInsets.symmetric(vertical: 18),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
                    elevation: 4,
                  ),
                  child: const Text("다시 듣기", style: TextStyle(fontWeight: FontWeight.w900)),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
