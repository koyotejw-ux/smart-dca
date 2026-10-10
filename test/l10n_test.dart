import 'package:flutter_test/flutter_test.dart';
import 'package:average_down_calculator/providers/language_provider.dart';
import 'package:average_down_calculator/utils/l10n.dart';

void main() {
  test('L10n coverage test for all languages', () {
    final languages = LanguageType.values;
    expect(languages.length, 7);

    // Test essential keys across all languages
    final testKeys = [
      'app_title',
      'sim_title',
      'app_subtitle',
      'smart_portfolio',
      'ai_assistant_btn',
      'security_title',
      'my_portfolio',
      'total_invested',
      'language_setting',
      'onboarding_start_button',
      'onboarding_tutorial_menu',
      'watch_ad_btn',
      'vip_reward_unlocked',
    ];

    for (final lang in languages) {
      for (final key in testKeys) {
        final text = L10n.s(lang, key);
        expect(text.isNotEmpty, true, reason: 'Key $key must not be empty for $lang');
        expect(text != key, true, reason: 'Key $key should have a translation for $lang');
      }
    }
  });
}
