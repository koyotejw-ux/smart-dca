import 'package:flutter/material.dart';

class NeonColors {
  static const Color background = Color(0xFF030303); // Ultra Black for OLED
  static const Color surface = Color(0xFF0A0A0A);
  static const Color cyan = Color(0xFF00E5FF);
  static const Color pink = Color(0xFFFF007F);
  static const Color yellow = Color(0xFFFFFF00);
  static const Color green = Color(0xFF00FF41);

  // 3D Glassy Border (Simulates light catching edges)
  static BoxDecoration glassyBorder(Color color, {double width = 1.5}) {
    return BoxDecoration(
      color: surface,
      borderRadius: BorderRadius.circular(16),
      border: Border.all(color: color.withOpacity(0.8), width: width),
      gradient: LinearGradient(
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
        colors: [
          Colors.white.withOpacity(0.05),
          Colors.transparent,
          Colors.black.withOpacity(0.2),
        ],
      ),
    );
  }

  // Linear Depth Shadow (Hard offset, multiple layers for 3D feel)
  static List<BoxShadow> depthShadow(Color color) {
    return [
      BoxShadow(
        color: color.withOpacity(0.2),
        offset: const Offset(4, 4),
        blurRadius: 0,
      ),
      BoxShadow(
        color: Colors.black.withOpacity(0.5),
        offset: const Offset(2, 2),
        blurRadius: 0,
      ),
    ];
  }

  // Sharp Solid Outlines
  static BoxDecoration borderGlow(Color color, {double width = 2.0}) {
    return BoxDecoration(
      color: surface,
      borderRadius: BorderRadius.circular(12),
      border: Border.all(color: color, width: width),
    );
  }

  // High Contrast Text
  static TextStyle textGlow(Color color) {
    return TextStyle(
      color: color,
      fontWeight: FontWeight.w900,
      letterSpacing: -0.5,
      shadows: [
        Shadow(
          blurRadius: 0,
          color: color.withOpacity(0.4),
          offset: const Offset(1, 1),
        ),
      ],
    );
  }
}
