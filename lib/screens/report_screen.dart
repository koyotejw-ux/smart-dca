import 'package:flutter/material.dart';
import '../widgets/one_ui_scroll_view.dart';
import 'package:flutter_animate/flutter_animate.dart';

class ReportScreen extends StatelessWidget {
  final String assetName;
  final String reportText;

  const ReportScreen({
    super.key,
    required this.assetName,
    required this.reportText,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Generating premium strategy card...')),
          );
        },
        label: const Text('Share Strategy'),
        icon: const Icon(Icons.share_rounded),
      ),
      body: OneUIScrollView(
        title: 'AI Report',
        children: [
          Card(
            color: theme.colorScheme.primaryContainer.withOpacity(0.1),
            child: Padding(
              padding: const EdgeInsets.all(24.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Icon(Icons.description_rounded, color: Colors.blue),
                      const SizedBox(width: 8),
                      Text(assetName, style: theme.textTheme.titleLarge),
                    ],
                  ),
                  const Divider(height: 40),
                  Text(
                    reportText,
                    style: theme.textTheme.bodyLarge?.copyWith(height: 1.6),
                  ),
                  const SizedBox(height: 40),
                  Center(
                    child: Text(
                      'Powered by Google Gemini',
                      style: theme.textTheme.bodySmall,
                    ),
                  ),
                ],
              ),
            ),
          ).animate().fadeIn(duration: 600.ms).slideY(begin: 0.05, end: 0),
          const SizedBox(height: 80),
        ],
      ),
    );
  }
}
