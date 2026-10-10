import 'package:flutter/material.dart';
import '../core/theme/app_colors.dart';

/// Legacy alias mapping to centralized AppColors
/// Retained for smooth backward compatibility while delegating to AppColors.
class TMembershipColors {
  // Brand Signatures
  static const Color primaryBlue = AppColors.primaryBlue;
  static const Color primaryBlueDark = AppColors.primaryBlueDark;
  static const Color accentPurple = AppColors.accentPurple;
  static const Color accentMagenta = AppColors.accentMagenta;
  static const Color accentCoral = AppColors.accentCoral;
  static const Color accentCyan = AppColors.accentCyan;
  static const Color accentMint = AppColors.accentMint;
  static const Color accentOrange = AppColors.accentOrange;
  static const Color gold = AppColors.gold;

  // Gradients
  static const LinearGradient primaryGradient = AppColors.primaryGradient;
  static const LinearGradient cardTealBlueGradient = AppColors.cardTealBlueGradient;
  static const LinearGradient vipGoldGradient = AppColors.vipGoldGradient;
  static const LinearGradient actionPurpleGradient = AppColors.actionPurpleGradient;

  // Light Theme Colors
  static const Color lightBg = AppColors.lightBg;
  static const Color lightSurface = AppColors.lightSurface;
  static const Color lightCardBorder = AppColors.lightCardBorder;
  static const Color lightTextPrimary = AppColors.lightTextPrimary;
  static const Color lightTextSecondary = AppColors.lightTextSecondary;
  static const Color lightTextTertiary = AppColors.lightTextTertiary;
  static const Color lightDivider = AppColors.lightDivider;

  // Dark Theme Colors
  static const Color darkBg = AppColors.darkBg;
  static const Color darkSurface = AppColors.darkSurface;
  static const Color darkCardBorder = AppColors.darkCardBorder;
  static const Color darkTextPrimary = AppColors.darkTextPrimary;
  static const Color darkTextSecondary = AppColors.darkTextSecondary;
  static const Color darkTextTertiary = AppColors.darkTextTertiary;
  static const Color darkDivider = AppColors.darkDivider;

  // Shadows
  static List<BoxShadow> softShadow({Color? color, double blur = 16, double dy = 6}) =>
      AppColors.softShadow(color: color, blur: blur, dy: dy);

  static List<BoxShadow> colorfulGlow(Color glowColor, {double opacity = 0.28}) =>
      AppColors.colorfulGlow(glowColor, opacity: opacity);
}
