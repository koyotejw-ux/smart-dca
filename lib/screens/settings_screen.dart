import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';
import '../theme/t_membership_colors.dart';
import '../providers/language_provider.dart';
import '../providers/currency_provider.dart';
import '../providers/theme_provider.dart';
import '../providers/asset_provider.dart';
import '../providers/scenario_provider.dart';
import '../utils/l10n.dart';
import 'help_screen.dart';
import 'onboarding_screen.dart';

class SettingsScreen extends ConsumerStatefulWidget {
  const SettingsScreen({super.key});

  @override
  ConsumerState<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends ConsumerState<SettingsScreen> {
  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final lang = ref.watch(languageProvider);
    final currency = ref.watch(currencyProvider);
    final themeMode = ref.watch(themeModeProvider);

    final bgColor = isDark ? TMembershipColors.darkBg : TMembershipColors.lightBg;
    final titleColor = isDark ? TMembershipColors.darkTextPrimary : TMembershipColors.lightTextPrimary;

    return Scaffold(
      backgroundColor: bgColor,
      appBar: AppBar(
        backgroundColor: bgColor,
        elevation: 0,
        leadingWidth: 56,
        leading: Padding(
          padding: const EdgeInsets.only(left: 16),
          child: Center(
            child: Material(
              color: Colors.transparent,
              child: InkWell(
                onTap: () => Navigator.pop(context),
                borderRadius: BorderRadius.circular(12),
                child: Container(
                  width: 38,
                  height: 38,
                  decoration: BoxDecoration(
                    color: isDark ? TMembershipColors.darkSurface : Colors.white,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(
                      color: isDark ? TMembershipColors.darkCardBorder : TMembershipColors.lightCardBorder,
                      width: 1.2,
                    ),
                    boxShadow: isDark ? [] : TMembershipColors.softShadow(blur: 6, dy: 2),
                  ),
                  child: Center(
                    child: Icon(Icons.arrow_back_ios_new_rounded, color: titleColor, size: 16),
                  ),
                ),
              ),
            ),
          ),
        ),
        title: Text(
          lang == LanguageType.ko ? "설정" : "Settings",
          style: GoogleFonts.inter(
            color: titleColor,
            fontWeight: FontWeight.w900,
            fontSize: 18,
            letterSpacing: -0.4,
          ),
        ),
      ),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 800),
          child: ListView(
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
            children: [
              _buildSectionHeader(L10n.s(lang, 'general_settings'), isDark),
              const SizedBox(height: 8),
              _buildSettingCard(
                isDark: isDark,
                children: [
                  _buildDropdownRow<CurrencyType>(
                    title: L10n.s(lang, 'base_currency'),
                    subtitle: "${currency.label} • ${currency.symbol}",
                    icon: Icons.payments_rounded,
                    value: currency,
                    items: CurrencyType.values.map((c) {
                      return DropdownMenuItem(
                        value: c,
                        child: Text(
                          c.label,
                          style: const TextStyle(color: TMembershipColors.primaryBlue, fontWeight: FontWeight.bold, fontSize: 13),
                        ),
                      );
                    }).toList(),
                    onChanged: (val) {
                      if (val != null) ref.read(currencyProvider.notifier).setCurrency(val);
                    },
                    isDark: isDark,
                  ),
                  _buildDivider(isDark),
                  _buildDropdownRow<ThemeMode>(
                    title: L10n.s(lang, 'screen_mode'),
                    subtitle: themeMode == ThemeMode.system
                        ? L10n.s(lang, 'system_mode')
                        : (themeMode == ThemeMode.light ? L10n.s(lang, 'light_mode') : L10n.s(lang, 'dark_mode')),
                    icon: Icons.palette_outlined,
                    value: themeMode,
                    items: [
                      DropdownMenuItem(
                        value: ThemeMode.system,
                        child: Text(L10n.s(lang, 'system_mode'), style: const TextStyle(color: TMembershipColors.primaryBlue, fontWeight: FontWeight.bold, fontSize: 13)),
                      ),
                      DropdownMenuItem(
                        value: ThemeMode.light,
                        child: Text(L10n.s(lang, 'light_mode'), style: const TextStyle(color: TMembershipColors.primaryBlue, fontWeight: FontWeight.bold, fontSize: 13)),
                      ),
                      DropdownMenuItem(
                        value: ThemeMode.dark,
                        child: Text(L10n.s(lang, 'dark_mode'), style: const TextStyle(color: TMembershipColors.primaryBlue, fontWeight: FontWeight.bold, fontSize: 13)),
                      ),
                    ],
                    onChanged: (val) {
                      if (val != null) ref.read(themeModeProvider.notifier).setThemeMode(val);
                    },
                    isDark: isDark,
                  ),
                  _buildDivider(isDark),
                  _buildDropdownRow<LanguageType>(
                    title: L10n.s(lang, 'language_setting'),
                    subtitle: "${lang.flag} ${lang.displayName}",
                    icon: Icons.language_rounded,
                    value: lang,
                    items: LanguageType.values.map((lt) {
                      return DropdownMenuItem(
                        value: lt,
                        child: Text(
                          "${lt.flag} ${lt.displayName}",
                          style: const TextStyle(color: TMembershipColors.accentMagenta, fontWeight: FontWeight.bold, fontSize: 13),
                        ),
                      );
                    }).toList(),
                    onChanged: (val) {
                      if (val != null) ref.read(languageProvider.notifier).setLanguage(val);
                    },
                    isDark: isDark,
                  ),
                ],
              ),
              const SizedBox(height: 24),
              _buildSectionHeader(L10n.s(lang, 'data_mgmt'), isDark),
              const SizedBox(height: 8),
              _buildSettingCard(
                isDark: isDark,
                children: [
                  _buildActionRow(
                    title: L10n.s(lang, 'onboarding_tutorial_menu'),
                    subtitle: L10n.s(lang, 'onboarding_tutorial_menu_sub'),
                    icon: Icons.lightbulb_rounded,
                    trailing: const Icon(Icons.arrow_forward_ios_rounded, size: 16, color: Colors.grey),
                    onTap: () => Navigator.push(context, MaterialPageRoute(builder: (context) => const OnboardingScreen())),
                    isDark: isDark,
                  ),
                  _buildDivider(isDark),
                  _buildActionRow(
                    title: L10n.s(lang, 'guide_menu'),
                    subtitle: L10n.s(lang, 'guide_menu_sub'),
                    icon: Icons.menu_book_rounded,
                    trailing: const Icon(Icons.arrow_forward_ios_rounded, size: 16, color: Colors.grey),
                    onTap: () => Navigator.push(context, MaterialPageRoute(builder: (context) => const HelpScreen())),
                    isDark: isDark,
                  ),
                  _buildDivider(isDark),
                  _buildActionRow(
                    title: L10n.s(lang, 'data_reset_title'),
                    subtitle: L10n.s(lang, 'data_reset_sub'),
                    icon: Icons.delete_outline_rounded,
                    iconColor: TMembershipColors.accentCoral,
                    trailing: Text(L10n.s(lang, 'reset_btn'), style: const TextStyle(color: TMembershipColors.accentCoral, fontWeight: FontWeight.w800, fontSize: 13)),
                    onTap: () => _confirmDataReset(context, ref),
                    isDark: isDark,
                  ),
                ],
              ),
              const SizedBox(height: 32),
              // App Info Card
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  color: isDark ? TMembershipColors.darkSurface : TMembershipColors.lightSurface,
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(
                    color: isDark ? TMembershipColors.darkCardBorder : TMembershipColors.lightCardBorder,
                    width: 1.2,
                  ),
                  boxShadow: isDark ? [] : TMembershipColors.softShadow(blur: 10, dy: 3),
                ),
                child: Column(
                  children: [
                    Text(
                      L10n.s(lang, 'app_version_name'),
                      style: GoogleFonts.inter(
                        fontWeight: FontWeight.w800,
                        fontSize: 14,
                        color: titleColor,
                      ),
                    ),
                    const SizedBox(height: 6),
                    Text(
                      L10n.s(lang, 'app_version_desc'),
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        color: isDark ? TMembershipColors.darkTextTertiary : TMembershipColors.lightTextTertiary,
                        fontSize: 11,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 40),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildSectionHeader(String title, bool isDark) {
    return Padding(
      padding: const EdgeInsets.only(left: 4),
      child: Text(
        title,
        style: GoogleFonts.inter(
          fontWeight: FontWeight.w800,
          fontSize: 13,
          color: isDark ? TMembershipColors.darkTextSecondary : TMembershipColors.lightTextSecondary,
        ),
      ),
    );
  }

  Widget _buildSettingCard({required bool isDark, required List<Widget> children}) {
    return Container(
      decoration: BoxDecoration(
        color: isDark ? TMembershipColors.darkSurface : TMembershipColors.lightSurface,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(
          color: isDark ? TMembershipColors.darkCardBorder : TMembershipColors.lightCardBorder,
          width: 1.2,
        ),
        boxShadow: isDark ? [] : TMembershipColors.softShadow(blur: 12, dy: 3),
      ),
      child: Column(children: children),
    );
  }

  Widget _buildDropdownRow<T>({
    required String title,
    required String subtitle,
    required IconData icon,
    required T value,
    required List<DropdownMenuItem<T>> items,
    required ValueChanged<T?> onChanged,
    required bool isDark,
  }) {
    final titleColor = isDark ? TMembershipColors.darkTextPrimary : TMembershipColors.lightTextPrimary;
    final subColor = isDark ? TMembershipColors.darkTextTertiary : TMembershipColors.lightTextTertiary;

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: TMembershipColors.primaryBlue.withOpacity(0.1),
              borderRadius: BorderRadius.circular(10),
            ),
            child: Icon(icon, color: TMembershipColors.primaryBlue, size: 20),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: GoogleFonts.inter(fontWeight: FontWeight.w700, fontSize: 13, color: titleColor),
                  maxLines: 1,
                  overflow: TextOverflow.visible,
                ),
                Text(
                  subtitle,
                  style: TextStyle(color: subColor, fontSize: 11),
                  maxLines: 1,
                  overflow: TextOverflow.visible,
                ),
              ],
            ),
          ),
          const SizedBox(width: 8),
          DropdownButton<T>(
            value: value,
            underline: const SizedBox(),
            isDense: true,
            dropdownColor: isDark ? TMembershipColors.darkSurface : Colors.white,
            items: items,
            onChanged: onChanged,
          ),
        ],
      ),
    );
  }

  Widget _buildActionRow({
    required String title,
    required String subtitle,
    required IconData icon,
    Color? iconColor,
    required Widget trailing,
    required VoidCallback onTap,
    required bool isDark,
  }) {
    final titleColor = isDark ? TMembershipColors.darkTextPrimary : TMembershipColors.lightTextPrimary;
    final subColor = isDark ? TMembershipColors.darkTextTertiary : TMembershipColors.lightTextTertiary;
    final color = iconColor ?? TMembershipColors.primaryBlue;

    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(20),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: color.withOpacity(0.1),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Icon(icon, color: color, size: 20),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(title, style: GoogleFonts.inter(fontWeight: FontWeight.w700, fontSize: 14, color: titleColor)),
                  Text(subtitle, style: TextStyle(color: subColor, fontSize: 11)),
                ],
              ),
            ),
            trailing,
          ],
        ),
      ),
    );
  }

  Widget _buildDivider(bool isDark) {
    return Divider(
      height: 1,
      thickness: 1,
      color: isDark ? TMembershipColors.darkDivider : TMembershipColors.lightDivider,
    );
  }

  void _confirmDataReset(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(languageProvider);
    final isKo = lang == LanguageType.ko;
    showDialog(
      context: context,
      builder: (dialogCtx) => AlertDialog(
        title: Text(isKo ? "데이터 초기화" : "Reset All Data", style: const TextStyle(fontWeight: FontWeight.w900)),
        content: Text(isKo ? "등록된 모든 자산 및 계산 시나리오 내역을 완전히 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다." : "Are you sure you want to delete all saved assets and calculation scenarios? This action cannot be undone."),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(dialogCtx),
            child: Text(isKo ? "취소" : "Cancel"),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: TMembershipColors.accentCoral,
              foregroundColor: Colors.white,
            ),
            onPressed: () async {
              Navigator.pop(dialogCtx);
              await ref.read(assetsProvider.notifier).clearAll();
              await ref.read(scenarioProvider.notifier).clearAll();
              if (context.mounted) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text(isKo ? "모든 데이터가 초기화되었습니다." : "All data has been reset."),
                    behavior: SnackBarBehavior.floating,
                  ),
                );
              }
            },
            child: Text(isKo ? "초기화" : "Reset", style: const TextStyle(fontWeight: FontWeight.bold)),
          ),
        ],
      ),
    );
  }
}
