import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'app_colors.dart';

/// Centralized Design System Typography and TextStyles
/// Standardized with GoogleFonts.inter for modern, clean, and consistent global typography.
class AppTextStyles {
  // Display & Hero Titles
  static TextStyle displayHero({Color? color}) => GoogleFonts.inter(
    fontSize: 32,
    fontWeight: FontWeight.w900,
    letterSpacing: -0.6,
    color: color ?? AppColors.lightTextPrimary,
  );

  static TextStyle displayLarge({Color? color}) => GoogleFonts.inter(
    fontSize: 28,
    fontWeight: FontWeight.w900,
    letterSpacing: -0.5,
    color: color ?? AppColors.lightTextPrimary,
  );

  static TextStyle displayMedium({Color? color}) => GoogleFonts.inter(
    fontSize: 24,
    fontWeight: FontWeight.w800,
    letterSpacing: -0.4,
    color: color ?? AppColors.lightTextPrimary,
  );

  // Headlines
  static TextStyle headlineLarge({Color? color}) => GoogleFonts.inter(
    fontSize: 20,
    fontWeight: FontWeight.w800,
    letterSpacing: -0.4,
    color: color ?? AppColors.lightTextPrimary,
  );

  static TextStyle headlineMedium({Color? color}) => GoogleFonts.inter(
    fontSize: 18,
    fontWeight: FontWeight.w800,
    letterSpacing: -0.3,
    color: color ?? AppColors.lightTextPrimary,
  );

  static TextStyle headlineSmall({Color? color}) => GoogleFonts.inter(
    fontSize: 16,
    fontWeight: FontWeight.w800,
    letterSpacing: -0.2,
    color: color ?? AppColors.lightTextPrimary,
  );

  // Titles
  static TextStyle titleLarge({Color? color}) => GoogleFonts.inter(
    fontSize: 16,
    fontWeight: FontWeight.w700,
    letterSpacing: -0.2,
    color: color ?? AppColors.lightTextPrimary,
  );

  static TextStyle titleMedium({Color? color}) => GoogleFonts.inter(
    fontSize: 15,
    fontWeight: FontWeight.w700,
    letterSpacing: -0.1,
    color: color ?? AppColors.lightTextPrimary,
  );

  static TextStyle titleSmall({Color? color}) => GoogleFonts.inter(
    fontSize: 14,
    fontWeight: FontWeight.w700,
    letterSpacing: 0,
    color: color ?? AppColors.lightTextPrimary,
  );

  // Body
  static TextStyle bodyLarge({Color? color, FontWeight? fontWeight}) => GoogleFonts.inter(
    fontSize: 15,
    fontWeight: fontWeight ?? FontWeight.w500,
    color: color ?? AppColors.lightTextPrimary,
  );

  static TextStyle bodyMedium({Color? color, FontWeight? fontWeight}) => GoogleFonts.inter(
    fontSize: 14,
    fontWeight: fontWeight ?? FontWeight.w500,
    color: color ?? AppColors.lightTextSecondary,
  );

  static TextStyle bodySmall({Color? color, FontWeight? fontWeight}) => GoogleFonts.inter(
    fontSize: 13,
    fontWeight: fontWeight ?? FontWeight.w500,
    color: color ?? AppColors.lightTextSecondary,
  );

  // Labels & Badges
  static TextStyle labelLarge({Color? color, FontWeight? fontWeight}) => GoogleFonts.inter(
    fontSize: 13,
    fontWeight: fontWeight ?? FontWeight.w700,
    letterSpacing: 0.2,
    color: color ?? AppColors.lightTextPrimary,
  );

  static TextStyle labelMedium({Color? color, FontWeight? fontWeight}) => GoogleFonts.inter(
    fontSize: 12,
    fontWeight: fontWeight ?? FontWeight.w600,
    letterSpacing: 0.2,
    color: color ?? AppColors.lightTextSecondary,
  );

  static TextStyle labelSmall({Color? color, FontWeight? fontWeight}) => GoogleFonts.inter(
    fontSize: 11,
    fontWeight: fontWeight ?? FontWeight.w700,
    letterSpacing: 0.4,
    color: color ?? AppColors.lightTextTertiary,
  );

  static TextStyle badge({Color? color}) => GoogleFonts.inter(
    fontSize: 10,
    fontWeight: FontWeight.w800,
    letterSpacing: 0.5,
    color: color ?? Colors.white,
  );

  // Monetary / Number Accents
  static TextStyle numericValue({double fontSize = 20, Color? color, FontWeight? fontWeight}) => GoogleFonts.inter(
    fontSize: fontSize,
    fontWeight: fontWeight ?? FontWeight.w900,
    letterSpacing: -0.5,
    color: color ?? AppColors.lightTextPrimary,
  );
}
