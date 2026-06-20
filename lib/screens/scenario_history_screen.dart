import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../providers/scenario_provider.dart';
import '../providers/language_provider.dart';
import '../utils/l10n.dart';
import '../theme/neon_colors.dart';
import '../widgets/one_ui_scroll_view.dart';
import 'package:google_fonts/google_fonts.dart';

class ScenarioHistoryScreen extends ConsumerWidget {
  const ScenarioHistoryScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final scenarios = ref.watch(scenarioProvider);
    final lang = ref.watch(languageProvider);
    final dateFormat = DateFormat('yyyy-MM-dd HH:mm');
    final currencyFormat = NumberFormat.currency(symbol: '', decimalDigits: 0);

    return Scaffold(
      backgroundColor: NeonColors.background,
      body: OneUIScrollView(
        title: "Simulation History",
        titleStyle: NeonColors.textGlow(NeonColors.pink).copyWith(fontWeight: FontWeight.w900),
        backgroundColor: NeonColors.background,
        children: [
          if (scenarios.isEmpty)
            Center(
              child: Padding(
                padding: const EdgeInsets.all(48.0),
                child: Column(
                  children: [
                    Icon(Icons.history_rounded, size: 64, color: Colors.grey[300]),
                    const SizedBox(height: 16),
                    const Text("저장된 시나리오가 없습니다.", style: TextStyle(color: Colors.grey, fontWeight: FontWeight.bold)),
                  ],
                ),
              ),
            )
          else
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: scenarios.length,
              itemBuilder: (context, index) {
                final s = scenarios[index];
                return Padding(
                  padding: const EdgeInsets.only(bottom: 12.0),
                  child: Container(
                    padding: const EdgeInsets.all(20),
                    decoration: NeonColors.borderGlow(NeonColors.pink).copyWith(color: NeonColors.surface),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(s.name, style: NeonColors.textGlow(NeonColors.pink).copyWith(fontWeight: FontWeight.w900, fontSize: 16)),
                            Text(dateFormat.format(s.createdAt), style: const TextStyle(color: Colors.white24, fontSize: 12)),
                          ],
                        ),
                        const SizedBox(height: 16),
                        Row(
                          children: [
                            _buildInfo("Initial", currencyFormat.format(s.initialPrice)),
                            const SizedBox(width: 24),
                            _buildInfo("Batches", s.batches.length.toString()),
                          ],
                        ),
                        const Divider(height: 32),
                        Row(
                          children: [
                            Expanded(
                              child: TextButton.icon(
                                onPressed: () {
                                  // TODO: Add logic to load back to Simulator
                                  Navigator.pop(context, s);
                                },
                                icon: const Icon(Icons.refresh_rounded, color: Colors.blue),
                                label: const Text("불러오기", style: TextStyle(color: NeonColors.cyan, fontWeight: FontWeight.w900)),
                              ),
                            ),
                            IconButton(
                              onPressed: () => ref.read(scenarioProvider.notifier).removeScenario(s.id),
                              icon: const Icon(Icons.delete_outline_rounded, color: Colors.redAccent),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
          const SizedBox(height: 48),
        ],
      ),
    );
  }

  Widget _buildInfo(String label, String value) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: const TextStyle(fontSize: 10, color: Colors.white30, fontWeight: FontWeight.bold)),
        Text(value, style: GoogleFonts.notoSansMono(fontWeight: FontWeight.w900, fontSize: 14, color: Colors.white70)),
      ],
    );
  }
}
