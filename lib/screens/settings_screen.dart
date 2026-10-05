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
        leading: IconButton(
          icon: Icon(Icons.arrow_back_ios_new_rounded, color: titleColor, size: 20),
          onPressed: () => Navigator.pop(context),
        ),
        title: Text(
          "설정 (Settings)",
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
              _buildSectionHeader("일반 설정", isDark),
              const SizedBox(height: 8),
              _buildSettingCard(
                isDark: isDark,
                children: [
                  _buildDropdownRow<CurrencyType>(
                    title: "기본 통화 (Currency)",
                    subtitle: "계산 및 포트폴리오 표기 화폐",
                    icon: Icons.payments_rounded,
                    value: currency,
                    items: [
                      DropdownMenuItem(
                        value: CurrencyType.krw,
                        child: Text("KRW (원, ₩)", style: TextStyle(color: TMembershipColors.primaryBlue, fontWeight: FontWeight.bold)),
                      ),
                      DropdownMenuItem(
                        value: CurrencyType.usd,
                        child: Text("USD (달러, \$)", style: TextStyle(color: TMembershipColors.primaryBlue, fontWeight: FontWeight.bold)),
                      ),
                    ],
                    onChanged: (val) {
                      if (val != null) ref.read(currencyProvider.notifier).setCurrency(val);
                    },
                    isDark: isDark,
                  ),
                  _buildDivider(isDark),
                  _buildDropdownRow<ThemeMode>(
                    title: "화면 모드 (Theme)",
                    subtitle: "라이트, 다크 또는 시스템 자동",
                    icon: Icons.palette_outlined,
                    value: themeMode,
                    items: [
                      DropdownMenuItem(
                        value: ThemeMode.system,
                        child: Text("시스템 설정값", style: TextStyle(color: TMembershipColors.primaryBlue, fontWeight: FontWeight.bold)),
                      ),
                      DropdownMenuItem(
                        value: ThemeMode.light,
                        child: Text("T 라이트 모드", style: TextStyle(color: TMembershipColors.primaryBlue, fontWeight: FontWeight.bold)),
                      ),
                      DropdownMenuItem(
                        value: ThemeMode.dark,
                        child: Text("다크 네이비 모드", style: TextStyle(color: TMembershipColors.primaryBlue, fontWeight: FontWeight.bold)),
                      ),
                    ],
                    onChanged: (val) {
                      if (val != null) ref.read(themeModeProvider.notifier).setThemeMode(val);
                    },
                    isDark: isDark,
                  ),
                  _buildDivider(isDark),
                  _buildDropdownRow<LanguageType>(
                    title: "언어 설정 (Language)",
                    subtitle: "앱 내부 표시 언어",
                    icon: Icons.language_rounded,
                    value: lang,
                    items: [
                      DropdownMenuItem(
                        value: LanguageType.ko,
                        child: Text("한국어 (Korean)", style: TextStyle(color: TMembershipColors.accentMagenta, fontWeight: FontWeight.bold)),
                      ),
                      DropdownMenuItem(
                        value: LanguageType.en,
                        child: Text("English (영어)", style: TextStyle(color: TMembershipColors.accentMagenta, fontWeight: FontWeight.bold)),
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
              _buildSectionHeader("자산 & 데이터 관리", isDark),
              const SizedBox(height: 8),
              _buildSettingCard(
                isDark: isDark,
                children: [
                  _buildActionRow(
                    title: "계산 공식 및 가이드",
                    subtitle: "물타기 원리 및 목표가 계산 안내",
                    icon: Icons.menu_book_rounded,
                    trailing: const Icon(Icons.arrow_forward_ios_rounded, size: 16, color: Colors.grey),
                    onTap: () => Navigator.push(context, MaterialPageRoute(builder: (context) => const HelpScreen())),
                    isDark: isDark,
                  ),
                  _buildDivider(isDark),
                  _buildActionRow(
                    title: "데이터 초기화",
                    subtitle: "등록된 자산 및 저장된 계산 기록 삭제",
                    icon: Icons.delete_outline_rounded,
                    iconColor: TMembershipColors.accentCoral,
                    trailing: const Text("초기화", style: TextStyle(color: TMembershipColors.accentCoral, fontWeight: FontWeight.w800, fontSize: 13)),
                    onTap: () => _confirmDataReset(context, ref),
                    isDark: isDark,
                  ),
                ],
              ),
              const SizedBox(height: 24),
              _buildSectionHeader("멤버십 혜택 & 광고", isDark),
              const SizedBox(height: 8),
              _buildSettingCard(
                isDark: isDark,
                children: [
                  _buildActionRow(
                    title: "1달 광고 제거 혜택 확인",
                    subtitle: "100 다운로드 돌파 감사 무료 이벤트",
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
                            active ? "적용 중 (VIP)" : "미적용",
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
                            content: Text("현재 광고 제거 혜택이 D-$days일 남아있습니다."),
                            behavior: SnackBarBehavior.floating,
                          ),
                        );
                      }
                    },
                    isDark: isDark,
                  ),
                  _buildDivider(isDark),
                  _buildActionRow(
                    title: "광고 기능 테스트 (AdMob)",
                    subtitle: "전면 광고 및 보상형 광고 점검",
                    icon: Icons.ads_click_rounded,
                    onTap: () {
                      AdmobService.showInterstitial(
                        onDismissed: () {
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(content: Text("광고가 정상 종료되었습니다.")),
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
                              const SnackBar(content: Text("광고가 정상 종료되었습니다.")),
                            );
                          },
                          onFailed: (err) {
                            ScaffoldMessenger.of(context).showSnackBar(
                              SnackBar(content: Text("광고 로드 상태: ${err.message}")),
                            );
                          },
                        );
                      },
                      child: const Text("광고 테스트", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
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
                      "T-Membership Clean UI • 100% On-Device Local Security",
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
                Text(title, style: GoogleFonts.inter(fontWeight: FontWeight.w700, fontSize: 14, color: titleColor)),
                Text(subtitle, style: TextStyle(color: subColor, fontSize: 11)),
              ],
            ),
          ),
          DropdownButton<T>(
            value: value,
            underline: const SizedBox(),
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
    showDialog(
      context: context,
      builder: (dialogCtx) => AlertDialog(
        title: const Text("데이터 초기화", style: TextStyle(fontWeight: FontWeight.w900)),
        content: const Text("등록된 모든 자산 및 계산 시나리오 내역을 완전히 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다."),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(dialogCtx),
            child: const Text("취소"),
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
                  const SnackBar(
                    content: Text("모든 데이터가 초기화되었습니다."),
                    behavior: SnackBarBehavior.floating,
                  ),
                );
              }
            },
            child: const Text("초기화", style: TextStyle(fontWeight: FontWeight.bold)),
          ),
        ],
      ),
    );
  }
}
