import 'package:flutter/material.dart';

class GlassCard extends StatelessWidget {
  final Widget child;
  final double blur; 
  final double opacity;
  final Color color;
  final Gradient? gradient;
  final BorderRadius? borderRadius;
  final Border? border;
  final List<BoxShadow>? boxShadow;

  const GlassCard({
    super.key,
    required this.child,
    this.blur = 0, // Disable blur for utility
    this.opacity = 1.0, // Solid by default
    this.color = Colors.white,
    this.gradient,
    this.borderRadius,
    this.border,
    this.boxShadow,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final effectiveRadius = borderRadius ?? BorderRadius.circular(24);
    
    return Container(
      decoration: BoxDecoration(
        color: gradient == null ? (isDark ? theme.colorScheme.surface : color) : null,
        gradient: gradient,
        borderRadius: effectiveRadius,
        border: border ?? Border.all(
          color: isDark ? Colors.white.withOpacity(0.12) : Colors.black.withOpacity(0.08),
          width: 1.5,
        ),
        boxShadow: boxShadow ?? [
          BoxShadow(
            color: Colors.black.withOpacity(0.04),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: child,
    );
  }
}
