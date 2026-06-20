import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';
import '../theme/neon_colors.dart';
import '../providers/language_provider.dart';
import '../providers/currency_provider.dart';
import '../utils/l10n.dart';
import '../services/unity_ad_service.dart';
import '../services/admob_service.dart';

class SettingsScreen extends ConsumerWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(languageProvider);
    final currency = ref.watch(currencyProvider);
    
    return Scaffold(
      backgroundColor: NeonColors.background,
      appBar: AppBar(
        backgroundColor: NeonColors.background,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios_new_rounded, color: Colors.white),
          onPressed: () => Navigator.pop(context),
        ),
        title: Text(
          "SETTINGS / 설정",
          style: GoogleFonts.inter(color: NeonColors.cyan, fontWeight: FontWeight.w900, fontSize: 16, letterSpacing: 2),
        ),
      ),
      body: ListView(
        padding: const EdgeInsets.all(24),
        children: [
          _buildSettingSection(
            context,
            "기본 화폐 (Currency)",
            Icons.payments_rounded,
            DropdownButton<CurrencyType>(
              value: currency,
              dropdownColor: Colors.black,
              underline: const SizedBox(),
              items: CurrencyType.values.map((c) {
                return DropdownMenuItem(
                  value: c,
                  child: Text(c.name.toUpperCase(), style: const TextStyle(color: NeonColors.cyan, fontWeight: FontWeight.bold)),
                );
              }).toList(),
              onChanged: (val) {
                if (val != null) ref.read(currencyProvider.notifier).setCurrency(val);
              },
            ),
          ),
          const SizedBox(height: 16),
          _buildSettingSection(
            context,
            "언어 (Language)",
            Icons.language_rounded,
            DropdownButton<LanguageType>(
              value: lang,
              dropdownColor: Colors.black,
              underline: const SizedBox(),
              items: LanguageType.values.map((l) {
                return DropdownMenuItem(
                  value: l,
                  child: Text(l == LanguageType.ko ? "한국어" : "ENGLISH", style: const TextStyle(color: NeonColors.pink, fontWeight: FontWeight.bold)),
                );
              }).toList(),
              onChanged: (val) {
                if (val != null) ref.read(languageProvider.notifier).setLanguage(val);
              },
            ),
          ),
          const SizedBox(height: 16),
          _buildSettingSection(
            context,
            "전면 광고 테스트 (AdMob)",
            Icons.ads_click_rounded,
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: NeonColors.cyan.withOpacity(0.2),
                foregroundColor: NeonColors.cyan,
                side: const BorderSide(color: NeonColors.cyan),
              ),
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text("전면 광고를 불러오는 중...")),
                );
                AdmobService.showInterstitial(
                  onDismissed: () {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text("전면 광고 완료/종료!")),
                    );
                  },
                  onFailed: (error) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text("광고 로드 실패: ${error.message}")),
                    );
                  },
                );
              },
              child: const Text("실행", style: TextStyle(fontWeight: FontWeight.bold)),
            ),
          ),
          const SizedBox(height: 16),
          _buildSettingSection(
            context,
            "보상형 광고 테스트 (AdMob)",
            Icons.card_giftcard_rounded,
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: NeonColors.pink.withOpacity(0.2),
                foregroundColor: NeonColors.pink,
                side: const BorderSide(color: NeonColors.pink),
              ),
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text("보상형 광고를 불러오는 중...")),
                );
                AdmobService.showRewarded(
                  onUserEarnedReward: (reward) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text("보상 획득! Type: ${reward.type}, Amount: ${reward.amount}")),
                    );
                  },
                  onDismissed: () {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text("보상형 광고 종료")),
                    );
                  },
                  onFailed: (error) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text("광고 로드 실패: ${error.message}")),
                    );
                  },
                );
              },
              child: const Text("실행", style: TextStyle(fontWeight: FontWeight.bold)),
            ),
          ),
          const SizedBox(height: 32),
          Container(
            padding: const EdgeInsets.all(24),
            decoration: NeonColors.glassyBorder(Colors.white10),
            child: const Column(
              children: [
                Text("NEON STRATEGY v3.0", style: TextStyle(color: Colors.white54, fontWeight: FontWeight.bold)),
                SizedBox(height: 8),
                Text("데이터는 기기에만 안전하게 저장됩니다.", style: TextStyle(color: Colors.white24, fontSize: 11)),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSettingSection(BuildContext context, String title, IconData icon, Widget trailing) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
      decoration: NeonColors.glassyBorder(Colors.white10),
      child: Row(
        children: [
          Icon(icon, color: Colors.white54, size: 20),
          const SizedBox(width: 16),
          Expanded(child: Text(title, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold))),
          trailing,
        ],
      ),
    );
  }
}
