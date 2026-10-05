import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';
import '../theme/t_membership_colors.dart';
import '../providers/language_provider.dart';
import '../providers/currency_provider.dart';
import '../providers/theme_provider.dart';
import '../providers/asset_provider.dart';
import '../providers/scenario_provider.dart';
import '../services/admob_service.dart';
import '../services/event_service.dart';
import 'help_screen.dart';

class SettingsScreen extends ConsumerWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
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
              _buildSectionHeader(lang == LanguageType.ko ? "일반 설정" : "General Settings", isDark),
              const SizedBox(height: 8),
              _buildSettingCard(
                isDark: isDark,
                children: [
                  _buildDropdownRow<CurrencyType>(
                    title: lang == LanguageType.ko ? "기본 통화" : "Currency",
                    subtitle: lang == LanguageType.ko ? "계산 및 포트폴리오 기준" : "Calculation & Portfolio",
                    icon: Icons.payments_rounded,
                    value: currency,
                    items: [
                      DropdownMenuItem(
                        value: CurrencyType.krw,
                        child: Text("KRW (₩)", style: TextStyle(color: TMembershipColors.primaryBlue, fontWeight: FontWeight.bold, fontSize: 13)),
                      ),
                      DropdownMenuItem(
                        value: CurrencyType.usd,
                        child: Text("USD (\$)", style: TextStyle(color: TMembershipColors.primaryBlue, fontWeight: FontWeight.bold, fontSize: 13)),
                      ),
                    ],
                    onChanged: (val) {
                      if (val != null) ref.read(currencyProvider.notifier).setCurrency(val);
                    },
                    isDark: isDark,
                  ),
                  _buildDivider(isDark),
                  _buildDropdownRow<ThemeMode>(
                    title: lang == LanguageType.ko ? "화면 모드" : "Appearance",
                    subtitle: lang == LanguageType.ko ? "라이트 / 다크 테마" : "Light / Dark Theme",
                    icon: Icons.palette_outlined,
                    value: themeMode,
                    items: [
                      DropdownMenuItem(
                        value: ThemeMode.system,
                        child: Text(lang == LanguageType.ko ? "시스템" : "System", style: TextStyle(color: TMembershipColors.primaryBlue, fontWeight: FontWeight.bold, fontSize: 13)),
                      ),
                      DropdownMenuItem(
                        value: ThemeMode.light,
                        child: Text(lang == LanguageType.ko ? "라이트" : "Light", style: TextStyle(color: TMembershipColors.primaryBlue, fontWeight: FontWeight.bold, fontSize: 13)),
                      ),
                      DropdownMenuItem(
                        value: ThemeMode.dark,
                        child: Text(lang == LanguageType.ko ? "다크" : "Dark", style: TextStyle(color: TMembershipColors.primaryBlue, fontWeight: FontWeight.bold, fontSize: 13)),
                      ),
                    ],
                    onChanged: (val) {
                      if (val != null) ref.read(themeModeProvider.notifier).setThemeMode(val);
                    },
                    isDark: isDark,
                  ),
                  _buildDivider(isDark),
                  _buildDropdownRow<LanguageType>(
                    title: lang == LanguageType.ko ? "언어 설정" : "Language",
                    subtitle: "한국어 / English",
                    icon: Icons.language_rounded,
                    value: lang,
                    items: [
                      DropdownMenuItem(
                        value: LanguageType.ko,
                        child: Text("한국어", style: TextStyle(color: TMembershipColors.accentMagenta, fontWeight: FontWeight.bold, fontSize: 13)),
                      ),
                      DropdownMenuItem(
                        value: LanguageType.en,
                        child: Text("English", style: TextStyle(color: TMembershipColors.accentMagenta, fontWeight: FontWeight.bold, fontSize: 13)),
                      ),
                    ],
                    onChanged: (val) {
                      if (val != null) ref.read(languageProvider.notifier).setLanguage(val);
                    },
                    isDark: isDark,
                  ),
                ],
              ),
              const SizedBox(height: 24),
              _buildSectionHeader(lang == LanguageType.ko ? "자산 & 데이터 관리" : "Data Management", isDark),
              const SizedBox(height: 8),
              _buildSettingCard(
                isDark: isDark,
                children: [
                  _buildActionRow(
                    title: lang == LanguageType.ko ? "계산 공식 및 가이드" : "Guide & Formula",
                    subtitle: lang == LanguageType.ko ? "물타기 원리 및 목표가 계산 안내" : "Strategy Principles & Tips",
                    icon: Icons.menu_book_rounded,
                    trailing: const Icon(Icons.arrow_forward_ios_rounded, size: 16, color: Colors.grey),
                    onTap: () => Navigator.push(context, MaterialPageRoute(builder: (context) => const HelpScreen())),
                    isDark: isDark,
                  ),
                  _buildDivider(isDark),
                  _buildActionRow(
                    title: lang == LanguageType.ko ? "데이터 초기화" : "Reset Data",
                    subtitle: lang == LanguageType.ko ? "등록된 자산 및 저장된 계산 기록 삭제" : "Clear all assets & history",
                    icon: Icons.delete_outline_rounded,
                    iconColor: TMembershipColors.accentCoral,
                    trailing: Text(lang == LanguageType.ko ? "초기화" : "Reset", style: const TextStyle(color: TMembershipColors.accentCoral, fontWeight: FontWeight.w800, fontSize: 13)),
                    onTap: () => _confirmDataReset(context, ref),
                    isDark: isDark,
                  ),
                ],
              ),
              const SizedBox(height: 24),
              _buildSectionHeader(lang == LanguageType.ko ? "이벤트 혜택 & 광고" : "VIP Events & Ads", isDark),
              const SizedBox(height: 8),
              _buildSettingCard(
                isDark: isDark,
                children: [
                  _buildActionRow(
                    title: lang == LanguageType.ko ? "1달 광고 제거 혜택 확인" : "Ad-Free VIP Status",
                    subtitle: lang == LanguageType.ko ? "100 다운로드 돌파 감사 무료 이벤트" : "Special Launch Benefit",
                    icon: Icons.stars_rounded,
                    iconColor: TMembershipColors.gold,
                    trailing: FutureBuilder<bool>(
                      future: EventService.isAdFreeActive(),
                      builder: (context, snapshot) {
                        final active = snapshot.data ?? false;
                        return Container(
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                          decoration: BoxDecoration(
                            color: active ? TMembershipColors.accentMint.withOpacity(0.15) : Colors.grey.withOpacity(0.15),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Text(
                            active ? (lang == LanguageType.ko ? "적용 중 (VIP)" : "Active (VIP)") : (lang == LanguageType.ko ? "미적용" : "Inactive"),
                            style: TextStyle(
                              color: active ? TMembershipColors.accentMint : Colors.grey,
                              fontWeight: FontWeight.w900,
                              fontSize: 11,
                            ),
                          ),
                        );
                      },
                    ),
                    onTap: () async {
                      final days = await EventService.getRemainingAdFreeDays();
                      if (context.mounted) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(
                            content: Text(lang == LanguageType.ko ? "현재 광고 제거 혜택이 D-$days일 남아있습니다." : "VIP Ad-Free benefit remaining: D-$days"),
                            behavior: SnackBarBehavior.floating,
                          ),
                        );
                      }
                    },
                    isDark: isDark,
                  ),
                  _buildDivider(isDark),
                  _buildActionRow(
                    title: lang == LanguageType.ko ? "광고 기능 테스트 (AdMob)" : "AdMob Function Test",
                    subtitle: lang == LanguageType.ko ? "전면 광고 및 보상형 광고 점검" : "Check Interstitial & Reward ads",
                    icon: Icons.ads_click_rounded,
                    onTap: () {
                      AdmobService.showInterstitial(
                        onDismissed: () {
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(content: Text(lang == LanguageType.ko ? "광고가 정상 종료되었습니다." : "Ad finished successfully.")),
                          );
                        },
                        onFailed: (err) {
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(content: Text("광고 로드 상태: ${err.message}")),
                          );
                        },
                      );
                    },
                    trailing: OutlinedButton(
                      style: OutlinedButton.styleFrom(
                        foregroundColor: TMembershipColors.primaryBlue,
                        side: const BorderSide(color: TMembershipColors.primaryBlue),
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                        minimumSize: Size.zero,
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                      ),
                      onPressed: () {
                        AdmobService.showInterstitial(
                          onDismissed: () {
                            ScaffoldMessenger.of(context).showSnackBar(
                              SnackBar(content: Text(lang == LanguageType.ko ? "광고가 정상 종료되었습니다." : "Ad finished successfully.")),
                            );
                          },
                          onFailed: (err) {
                            ScaffoldMessenger.of(context).showSnackBar(
                              SnackBar(content: Text("광고 로드 상태: ${err.message}")),
                            );
                          },
                        );
                      },
                      child: Text(lang == LanguageType.ko ? "광고 테스트" : "Test Ad", style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 12)),
                    ),
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
                      "스마트 물타기 계산기 v3.2",
                      style: GoogleFonts.inter(
                        fontWeight: FontWeight.w800,
                        fontSize: 14,
                        color: titleColor,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      "Smart Clean UI • 100% On-Device Local Security",
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
