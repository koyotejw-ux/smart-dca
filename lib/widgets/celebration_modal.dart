import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../theme/neon_colors.dart';
import '../services/event_service.dart';
import '../providers/language_provider.dart';
import '../utils/l10n.dart';

class CelebrationModal extends ConsumerWidget {
  final VoidCallback onClaimed;

  const CelebrationModal({
    super.key,
    required this.onClaimed,
  });

  static Future<void> show(BuildContext context, {required VoidCallback onClaimed}) async {
    return showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => CelebrationModal(onClaimed: onClaimed),
    );
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(languageProvider);
    return Dialog(
      backgroundColor: Colors.transparent,
      insetPadding: const EdgeInsets.symmetric(horizontal: 24, vertical: 40),
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 440),
        child: Container(
          decoration: BoxDecoration(
          color: const Color(0xFF161C24).withOpacity(0.95),
          borderRadius: BorderRadius.circular(28),
          border: Border.all(
            color: NeonColors.cyan.withOpacity(0.4),
            width: 1.5,
          ),
          boxShadow: [
            BoxShadow(
              color: NeonColors.cyan.withOpacity(0.25),
              blurRadius: 30,
              spreadRadius: 2,
            ),
          ],
        ),
        padding: const EdgeInsets.all(28),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            // Floating Celebration Icon Badge
            Container(
              width: 80,
              height: 80,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                gradient: LinearGradient(
                  colors: [NeonColors.cyan, Colors.blueAccent],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                boxShadow: [
                  BoxShadow(
                    color: NeonColors.cyan.withOpacity(0.5),
                    blurRadius: 20,
                    offset: const Offset(0, 6),
                  ),
                ],
              ),
              child: const Icon(
                Icons.card_giftcard_rounded,
                size: 42,
                color: Colors.black,
              ),
            )
                .animate()
                .scale(duration: 600.ms, curve: Curves.easeOutBack)
                .shimmer(delay: 700.ms, duration: 1200.ms),
            const SizedBox(height: 20),
            // Title
            ShaderMask(
              shaderCallback: (bounds) => LinearGradient(
                colors: [Colors.white, NeonColors.cyan],
              ).createShader(bounds),
              child: Text(
                '🎉 ${L10n.s(lang, 'event_modal_title')}',
                textAlign: TextAlign.center,
                style: const TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.w900,
                  color: Colors.white,
                  letterSpacing: -0.5,
                ),
              ),
            ).animate().fadeIn(delay: 200.ms).slideY(begin: 0.2, end: 0),
            const SizedBox(height: 10),
            Text(
              L10n.s(lang, 'event_modal_desc'),
              textAlign: TextAlign.center,
              style: const TextStyle(
                fontSize: 13,
                color: Colors.white70,
                height: 1.45,
              ),
            ).animate().fadeIn(delay: 300.ms),
            const SizedBox(height: 24),
            // Feature highlight box
            Container(
              padding: const EdgeInsets.all(18),
              decoration: BoxDecoration(
                color: Colors.white.withOpacity(0.05),
                borderRadius: BorderRadius.circular(18),
                border: Border.all(
                  color: Colors.white.withOpacity(0.1),
                ),
              ),
              child: Column(
                children: [
                  _buildBenefitRow(
                    icon: Icons.block_rounded,
                    color: Colors.amberAccent,
                    title: L10n.s(lang, 'event_benefit_1_title'),
                    subtitle: L10n.s(lang, 'event_benefit_1_sub'),
                  ),
                  const Divider(height: 24, color: Colors.white12),
                  _buildBenefitRow(
                    icon: Icons.bolt_rounded,
                    color: NeonColors.cyan,
                    title: L10n.s(lang, 'event_benefit_2_title'),
                    subtitle: L10n.s(lang, 'event_benefit_2_sub'),
                  ),
                ],
              ),
            ).animate().fadeIn(delay: 400.ms).scale(begin: const Offset(0.95, 0.95)),
            const SizedBox(height: 28),
            // Primary Action Button
            SizedBox(
              width: double.infinity,
              height: 52,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: NeonColors.cyan,
                  foregroundColor: Colors.black,
                  elevation: 8,
                  shadowColor: NeonColors.cyan.withOpacity(0.5),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(16),
                  ),
                ),
                onPressed: () async {
                  await EventService.claim100DownloadsEvent();
                  if (context.mounted) {
                    Navigator.of(context).pop();
                    onClaimed();
                  }
                },
                child: Text(
                  L10n.s(lang, 'event_claim_btn'),
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 0.2,
                  ),
                ),
              ),
            ).animate().fadeIn(delay: 500.ms).slideY(begin: 0.2, end: 0),
          ],
        ),
      ),
    ),
  );
}

  Widget _buildBenefitRow({
    required IconData icon,
    required Color color,
    required String title,
    required String subtitle,
  }) {
    return Row(
      children: [
        Container(
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(
            color: color.withOpacity(0.15),
            shape: BoxShape.circle,
          ),
          child: Icon(icon, color: color, size: 22),
        ),
        const SizedBox(width: 14),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                  fontSize: 14,
                ),
              ),
              const SizedBox(height: 2),
              Text(
                subtitle,
                style: const TextStyle(
                  color: Colors.white54,
                  fontSize: 11,
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}
