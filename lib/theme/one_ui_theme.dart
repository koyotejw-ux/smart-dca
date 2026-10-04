import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 't_membership_colors.dart';

class OneUITheme {
  static ThemeData lightTheme = ThemeData(
    useMaterial3: true,
    brightness: Brightness.light,
    colorScheme: const ColorScheme.light(
      surface: TMembershipColors.lightSurface,
      primary: TMembershipColors.primaryBlue,
      secondary: TMembershipColors.accentPurple,
      tertiary: TMembershipColors.accentMagenta,
      error: TMembershipColors.accentCoral,
      onPrimary: Colors.white,
      onSurface: TMembershipColors.lightTextPrimary,
    ),
    scaffoldBackgroundColor: TMembershipColors.lightBg,
    textTheme: GoogleFonts.interTextTheme().copyWith(
      headlineLarge: GoogleFonts.inter(
        fontSize: 30,
        fontWeight: FontWeight.w900,
        color: TMembershipColors.lightTextPrimary,
        letterSpacing: -0.8,
      ),
      headlineMedium: GoogleFonts.inter(
        fontSize: 24,
        fontWeight: FontWeight.w800,
        color: TMembershipColors.lightTextPrimary,
        letterSpacing: -0.5,
      ),
      titleLarge: GoogleFonts.inter(
        fontSize: 20,
        fontWeight: FontWeight.w800,
        color: TMembershipColors.lightTextPrimary,
        letterSpacing: -0.3,
      ),
      titleMedium: GoogleFonts.inter(
        fontSize: 16,
        fontWeight: FontWeight.w700,
        color: TMembershipColors.lightTextPrimary,
      ),
      bodyLarge: GoogleFonts.inter(
        fontSize: 15,
        fontWeight: FontWeight.w500,
        color: TMembershipColors.lightTextSecondary,
      ),
      bodyMedium: GoogleFonts.inter(
        fontSize: 14,
        fontWeight: FontWeight.w400,
        color: TMembershipColors.lightTextSecondary,
      ),
      labelLarge: GoogleFonts.inter(
        fontSize: 14,
        fontWeight: FontWeight.w700,
        color: TMembershipColors.primaryBlue,
      ),
    ),
    cardTheme: CardThemeData(
      color: TMembershipColors.lightSurface,
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(24),
        side: const BorderSide(color: TMembershipColors.lightCardBorder, width: 1.2),
      ),
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: TMembershipColors.primaryBlue,
        foregroundColor: Colors.white,
        elevation: 0,
        minimumSize: const Size(double.infinity, 56),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
        ),
        textStyle: GoogleFonts.inter(
          fontWeight: FontWeight.w800,
          fontSize: 16,
          letterSpacing: -0.2,
        ),
      ),
    ),
  );

  static ThemeData darkTheme = ThemeData(
    useMaterial3: true,
    brightness: Brightness.dark,
    colorScheme: const ColorScheme.dark(
      surface: TMembershipColors.darkSurface,
      primary: TMembershipColors.primaryBlue,
      secondary: TMembershipColors.accentCyan,
      tertiary: TMembershipColors.accentMagenta,
      error: TMembershipColors.accentCoral,
      onPrimary: Colors.white,
      onSurface: TMembershipColors.darkTextPrimary,
    ),
    scaffoldBackgroundColor: TMembershipColors.darkBg,
    textTheme: GoogleFonts.interTextTheme().copyWith(
      headlineLarge: GoogleFonts.inter(
        fontSize: 30,
        fontWeight: FontWeight.w900,
        color: TMembershipColors.darkTextPrimary,
        letterSpacing: -0.8,
      ),
      headlineMedium: GoogleFonts.inter(
        fontSize: 24,
        fontWeight: FontWeight.w800,
        color: TMembershipColors.darkTextPrimary,
        letterSpacing: -0.5,
      ),
      titleLarge: GoogleFonts.inter(
        fontSize: 20,
        fontWeight: FontWeight.w800,
        color: TMembershipColors.darkTextPrimary,
        letterSpacing: -0.3,
      ),
      titleMedium: GoogleFonts.inter(
        fontSize: 16,
        fontWeight: FontWeight.w700,
        color: TMembershipColors.darkTextPrimary,
      ),
      bodyLarge: GoogleFonts.inter(
        fontSize: 15,
        fontWeight: FontWeight.w500,
        color: TMembershipColors.darkTextSecondary,
      ),
      bodyMedium: GoogleFonts.inter(
        fontSize: 14,
        fontWeight: FontWeight.w400,
        color: TMembershipColors.darkTextSecondary,
      ),
      labelLarge: GoogleFonts.inter(
        fontSize: 14,
        fontWeight: FontWeight.w700,
        color: TMembershipColors.accentCyan,
      ),
    ),
    cardTheme: CardThemeData(
      color: TMembershipColors.darkSurface,
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(24),
        side: const BorderSide(color: TMembershipColors.darkCardBorder, width: 1.2),
      ),
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: TMembershipColors.primaryBlue,
        foregroundColor: Colors.white,
        elevation: 0,
        minimumSize: const Size(double.infinity, 56),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
        ),
        textStyle: GoogleFonts.inter(
          fontWeight: FontWeight.w800,
          fontSize: 16,
          letterSpacing: -0.2,
        ),
      ),
    ),
  );
}
