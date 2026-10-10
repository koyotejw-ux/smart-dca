import 'package:flutter/material.dart';

/// Centralized Design System Colors for the Application
/// Provides brand colors, semantic colors, neutral dark/light surfaces, and gradients.
class AppColors {
  // Brand Signatures (T-Blue, Magenta/Purple, Electric Coral, Mint)
  static const Color primaryBlue = Color(0xFF0051FF);      // Vibrant T Electric Blue
  static const Color primaryBlueDark = Color(0xFF0038B8);  // Deep Electric Blue
  static const Color accentPurple = Color(0xFF7A22FF);     // Deep Purple / Violet
  static const Color accentMagenta = Color(0xFFFF1493);    // Vibrant Magenta / Pink
  static const Color accentCoral = Color(0xFFFF5252);      // Coral Red
  static const Color accentCyan = Color(0xFF00D2FF);       // Bright Sky / Cyan
  static const Color accentMint = Color(0xFF00E676);       // Fresh Gain Mint / Green
  static const Color accentOrange = Color(0xFFFF6D00);     // Warning Orange
  static const Color gold = Color(0xFFFFB300);             // VIP Gold
  static const Color vipOrange = Color(0xFFFF9800);        // VIP Badge Orange

  // Gradients
  static const LinearGradient primaryGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [Color(0xFF0055FF), Color(0xFF7928CA), Color(0xFFFF0080)],
    stops: [0.0, 0.55, 1.0],
  );

  static const LinearGradient cardTealBlueGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [Color(0xFF00C6FF), Color(0xFF0072FF)],
  );

  static const LinearGradient vipGoldGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [Color(0xFFFF9900), Color(0xFFFF5E62)],
  );

  static const LinearGradient actionPurpleGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [Color(0xFF6A11CB), Color(0xFF2575FC)],
  );

  static const LinearGradient voiceWaveGradient = LinearGradient(
    colors: [Color(0xFF0051FF), Color(0xFF00D2FF), Color(0xFF7A22FF)],
  );

  // Light Theme Colors (SK / Modern Clean Style)
  static const Color lightBg = Color(0xFFF6F8FC);
  static const Color lightSurface = Colors.white;
  static const Color lightCardBorder = Color(0xFFEEF2F8);
  static const Color lightCardBorderAlt = Color(0xFFDCE4F2);
  static const Color lightTextPrimary = Color(0xFF191F28);
  static const Color lightTextSecondary = Color(0xFF4E5968);
  static const Color lightTextTertiary = Color(0xFF8B95A1);
  static const Color lightDivider = Color(0xFFF2F4F6);
  static const Color lightSubSurface = Color(0xFFF3F7FD);

  // Dark Theme Colors (Deep Charcoal / Navy)
  static const Color darkBg = Color(0xFF0F141C);
  static const Color darkSurface = Color(0xFF1A212E);
  static const Color darkSubSurface = Color(0xFF161E2E);
  static const Color darkCardBorder = Color(0xFF2B3648);
  static const Color darkCardBorderAlt = Color(0xFF2A364F);
  static const Color darkTextPrimary = Color(0xFFF9FAFB);
  static const Color darkTextSecondary = Color(0xFFD1D6DB);
  static const Color darkTextTertiary = Color(0xFF8B95A1);
  static const Color darkDivider = Color(0xFF242C3A);

  // Functional / Semantic Colors
  static const Color success = Color(0xFF00E676);
  static const Color error = Color(0xFFFF5252);
  static const Color warning = Color(0xFFFF6D00);
  static const Color info = Color(0xFF0051FF);

  // Surface Shadows & Glows
  static List<BoxShadow> softShadow({Color? color, double blur = 16, double dy = 6}) {
    return [
      BoxShadow(
        color: (color ?? primaryBlueDark).withOpacity(0.08),
        blurRadius: blur,
        offset: Offset(0, dy),
        spreadRadius: 0,
      ),
    ];
  }

  static List<BoxShadow> colorfulGlow(Color glowColor, {double opacity = 0.28}) {
    return [
      BoxShadow(
        color: glowColor.withOpacity(opacity),
        blurRadius: 20,
        offset: const Offset(0, 8),
        spreadRadius: -2,
      ),
    ];
  }
}
