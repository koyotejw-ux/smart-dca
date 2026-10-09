import 'storage_service.dart';

class EventService {
  static const String _key100Claimed = 'event_100_downloads_claimed';
  static const String _key100ClaimedDate = 'event_100_downloads_claimed_date';
  
  static final StorageService _storage = StorageService();
  static bool? _cachedIsAdFree;

  /// Check if 100-download event benefit is claimed
  static Future<bool> is100DownloadsEventClaimed() async {
    final val = await _storage.getSetting(_key100Claimed);
    return val == 'true';
  }

  /// Claim 100 downloads celebration benefit (1 month ad removal)
  static Future<void> claim100DownloadsEvent() async {
    final now = DateTime.now().toIso8601String();
    await _storage.setSetting(_key100Claimed, 'true');
    await _storage.setSetting(_key100ClaimedDate, now);
    _cachedIsAdFree = true;
  }

  static const String _keyRewardedVipExpiry = 'rewarded_vip_expiry_date';

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
    _cachedIsAdFree = true;
  }

  /// Check if ad-free period is currently active (Event or Rewarded Ad VIP)
  static Future<bool> isAdFreeActive() async {
    final now = DateTime.now();

    // 1. Check rewarded VIP
    final rewardedStored = await _storage.getSetting(_keyRewardedVipExpiry);
    if (rewardedStored != null) {
      try {
        final exp = DateTime.parse(rewardedStored);
        if (exp.isAfter(now)) {
          _cachedIsAdFree = true;
          return true;
        }
      } catch (_) {}
    }

    // 2. Check 100-download event
    final claimed = await is100DownloadsEventClaimed();
    if (!claimed) {
      _cachedIsAdFree = false;
      return false;
    }

    final dateStr = await _storage.getSetting(_key100ClaimedDate);
    if (dateStr == null) {
      _cachedIsAdFree = false;
      return false;
    }

    try {
      final claimDate = DateTime.parse(dateStr);
      final expiryDate = claimDate.add(const Duration(days: 30));
      final isActive = now.isBefore(expiryDate);
      _cachedIsAdFree = isActive;
      return isActive;
    } catch (_) {
      _cachedIsAdFree = false;
      return false;
    }
  }

  /// Gets remaining ad-free days
  static Future<int> getRemainingAdFreeDays() async {
    final now = DateTime.now();
    int maxDays = 0;

    // Check rewarded VIP
    final rewardedStored = await _storage.getSetting(_keyRewardedVipExpiry);
    if (rewardedStored != null) {
      try {
        final exp = DateTime.parse(rewardedStored);
        if (exp.isAfter(now)) {
          final diff = exp.difference(now).inDays + 1;
          if (diff > maxDays) maxDays = diff;
        }
      } catch (_) {}
    }

    final dateStr = await _storage.getSetting(_key100ClaimedDate);
    if (dateStr != null) {
      try {
        final claimDate = DateTime.parse(dateStr);
        final expiryDate = claimDate.add(const Duration(days: 30));
        final diff = expiryDate.difference(now).inDays + 1;
        if (diff > maxDays) maxDays = diff;
      } catch (_) {}
    }
    return maxDays;
  }
}
