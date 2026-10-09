import 'storage_service.dart';

class EventService {
  static const String _key100Claimed = 'event_100_downloads_claimed';
  static const String _key100ClaimedDate = 'event_100_downloads_claimed_date';
  static const String _keyRewardedVipExpiry = 'rewarded_vip_expiry_date';

  static final StorageService _storage = StorageService();

  /// Reset old 100 downloads event benefit so only 24h pass takes effect
  static Future<void> resetOld100DownloadsEvent() async {
    await _storage.removeSetting(_key100Claimed);
    await _storage.removeSetting(_key100ClaimedDate);
  }

  /// Claim event benefit as 24-hour pass
  static Future<void> claim100DownloadsEvent() async {
    await addAdFreeHours(24);
  }

  /// Add ad-free hours earned from watching rewarded ads
  static Future<void> addAdFreeHours(int hours) async {
    final now = DateTime.now();
    DateTime currentExpiry = now;
    final stored = await _storage.getSetting(_keyRewardedVipExpiry);
    if (stored != null) {
      try {
        final parsed = DateTime.parse(stored);
        if (parsed.isAfter(now)) {
          currentExpiry = parsed;
        }
      } catch (_) {}
    }
    final newExpiry = currentExpiry.add(Duration(hours: hours));
    await _storage.setSetting(_keyRewardedVipExpiry, newExpiry.toIso8601String());
  }

  /// Check if ad-free period is currently active (Rewarded Ad VIP)
  static Future<bool> isAdFreeActive() async {
    final now = DateTime.now();
    final rewardedStored = await _storage.getSetting(_keyRewardedVipExpiry);
    if (rewardedStored != null) {
      try {
        final exp = DateTime.parse(rewardedStored);
        if (exp.isAfter(now)) {
          return true;
        }
      } catch (_) {}
    }
    return false;
  }

  /// Gets remaining ad-free days
  static Future<int> getRemainingAdFreeDays() async {
    final now = DateTime.now();
    final rewardedStored = await _storage.getSetting(_keyRewardedVipExpiry);
    if (rewardedStored != null) {
      try {
        final exp = DateTime.parse(rewardedStored);
        if (exp.isAfter(now)) {
          return exp.difference(now).inDays + 1;
        }
      } catch (_) {}
    }
    return 0;
  }

  /// Gets the latest expiry DateTime for active ad-free benefit
  static Future<DateTime?> getAdFreeExpiryDate() async {
    final now = DateTime.now();
    final rewardedStored = await _storage.getSetting(_keyRewardedVipExpiry);
    if (rewardedStored != null) {
      try {
        final exp = DateTime.parse(rewardedStored);
        if (exp.isAfter(now)) {
          return exp;
        }
      } catch (_) {}
    }
    return null;
  }
}
