import 'package:flutter/material.dart';

class OneUIColors {
  // Kakao Specific Colors
  static const Color kakaoYellow = Color(0xFFFEE500);
  static const Color kakaoGold = Color(0xFFFFD700);
  static const Color kakaoBrown = Color(0xFF3C1E1E);
  static const Color kakaoLightGrey = Color(0xFFFAFAFA);
  static const Color kakaoDarkGrey = Color(0xFF707070);

  // Calculator Specific Colors
  static const Color lcdBackground = Color(0xFF1A1A1A); // Deep Slate
  static const Color lcdText = Color(0xFF00FF41); // Fluorescent Green
  static const Color calcOrange = Color(0xFFFF9500); // Standard Calc Orange
  static const Color calcGrey = Color(0xFFD4D4D2); // Standard Calc Grey
  static const Color calcDarkGrey = Color(0xFF505050);

  // Light Mode Colors
  static const Color lightBackground = kakaoLightGrey;
  static const Color lightSurface = Colors.white;
  static const Color lightPrimary = kakaoYellow;
  static const Color lightSecondary = kakaoBrown;
  static const Color lightTextPrimary = kakaoBrown;
  static const Color lightTextSecondary = kakaoDarkGrey;
  static const Color lightAccent = Color(0xFFFF3B30);

  // Dark Mode Colors
  static const Color darkBackground = Color(0xFF121212);
  static const Color darkSurface = Color(0xFF1E1E1E);
  static const Color darkPrimary = kakaoYellow;
  static const Color darkSecondary = Color(0xFFAEAEC0);
  static const Color darkTextPrimary = Color(0xFFE5E5E5);
  static const Color darkTextSecondary = Color(0xFF8E8E93);
  static const Color darkAccent = Color(0xFFFF453A);

  // Status Colors
  static const Color success = Color(0xFF34C759);
  static const Color warning = Color(0xFFFF9F0A);
  static const Color info = Color(0xFF5856D6);
}
