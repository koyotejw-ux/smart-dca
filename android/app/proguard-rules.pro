# Flutter Proguard & R8 Rules

# Flutter core
-keep class io.flutter.app.** { *; }
-keep class io.flutter.plugin.**  { *; }
-keep class io.flutter.util.**  { *; }
-keep class io.flutter.view.**  { *; }
-keep class io.flutter.** { *; }
-keep class io.flutter.plugins.** { *; }
-dontwarn io.flutter.embedding.**

# Google Mobile Ads
-keep public class com.google.android.gms.ads.** { public *; }
-keep public class com.google.ads.** { public *; }
-keepattributes *Annotation*

# Speech To Text
-keep class com.csdcorp.speech_to_text.** { *; }

# Sqflite
-keep class com.tekartik.sqflite.** { *; }

# SharedPreferences
-keep class io.flutter.plugins.sharedpreferences.** { *; }

# General optimizations
-dontwarn **
-ignorewarnings
