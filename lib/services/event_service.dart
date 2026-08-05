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

  /// Check if 1-month ad-free period is currently active
  static Future<bool> isAdFreeActive() async {
    if (_cachedIsAdFree != null) {
      return _cachedIsAdFree!;
    }
    
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
      final isActive = DateTime.now().isBefore(expiryDate);
      _cachedIsAdFree = isActive;
      return isActive;
    } catch (_) {
      _cachedIsAdFree = false;
      return false;
    }
  }

  /// Gets remaining ad-free days
  static Future<int> getRemainingAdFreeDays() async {
    final dateStr = await _storage.getSetting(_key100ClaimedDate);
    if (dateStr == null) return 0;
    try {
      final claimDate = DateTime.parse(dateStr);
      final expiryDate = claimDate.add(const Duration(days: 30));
      final diff = expiryDate.difference(DateTime.now()).inDays;
      return diff < 0 ? 0 : diff + 1;
    } catch (_) {
      return 0;
    }
  }
}
