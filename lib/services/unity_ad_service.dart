import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:unity_ads_plugin/unity_ads_plugin.dart';

class UnityAdService {
  static const String _androidGameId = '4347587';
  static const String _iosGameId = '4347586';

  static String get gameId {
    if (defaultTargetPlatform == TargetPlatform.android) {
      return _androidGameId;
    } else if (defaultTargetPlatform == TargetPlatform.iOS) {
      return _iosGameId;
    }
    return '';
  }

  static String get bannerPlacementId {
    return defaultTargetPlatform == TargetPlatform.iOS ? 'Banner_iOS' : 'Banner_Android';
  }

  static String get interstitialPlacementId {
    return defaultTargetPlatform == TargetPlatform.iOS ? 'Interstitial_iOS' : 'Interstitial_Android';
  }

  static String get rewardedPlacementId {
    return defaultTargetPlatform == TargetPlatform.iOS ? 'Rewarded_iOS' : 'Rewarded_Android';
  }

  static bool _isInitialized = false;
  static bool get isInitialized => _isInitialized;

  /// Initializes Unity Ads SDK
  static Future<void> init({bool testMode = true}) async {
    final id = gameId;
    if (id.isEmpty) {
      debugPrint('Unity Ads: Unsupported platform');
      return;
    }

    try {
      await UnityAds.init(
        gameId: id,
        testMode: testMode,
        onComplete: () {
          _isInitialized = true;
          debugPrint('Unity Ads: Initialization Complete');
        },
        onFailed: (error, message) {
          _isInitialized = false;
          debugPrint('Unity Ads: Initialization Failed: $error - $message');
        },
      );
    } catch (e) {
      debugPrint('Unity Ads Init Exception: $e');
    }
  }

  /// Loads and shows an Interstitial Ad
  static Future<void> showInterstitial({
    VoidCallback? onStart,
    VoidCallback? onComplete,
    VoidCallback? onSkipped,
    Function(String, String)? onFailed,
  }) async {
    final placementId = interstitialPlacementId;
    
    try {
      await UnityAds.load(
        placementId: placementId,
        onComplete: (id) {
          debugPrint('Unity Ads: Loaded Interstitial $id');
          UnityAds.showVideoAd(
            placementId: placementId,
            onStart: (id) => onStart?.call(),
            onComplete: (id) => onComplete?.call(),
            onFailed: (id, error, message) => onFailed?.call(error.toString(), message),
            onSkipped: (id) => onSkipped?.call(),
          );
        },
        onFailed: (id, error, message) {
          debugPrint('Unity Ads: Load Interstitial Failed: $error - $message');
          onFailed?.call(error.toString(), message);
        },
      );
    } catch (e) {
      debugPrint('Unity Ads Show Interstitial Exception: $e');
      onFailed?.call('EXCEPTION', e.toString());
    }
  }

  /// Loads and shows a Rewarded Ad
  static Future<void> showRewarded({
    VoidCallback? onStart,
    VoidCallback? onComplete,
    VoidCallback? onSkipped,
    Function(String, String)? onFailed,
  }) async {
    final placementId = rewardedPlacementId;

    try {
      await UnityAds.load(
        placementId: placementId,
        onComplete: (id) {
          debugPrint('Unity Ads: Loaded Rewarded $id');
          UnityAds.showVideoAd(
            placementId: placementId,
            onStart: (id) => onStart?.call(),
            onComplete: (id) => onComplete?.call(),
            onFailed: (id, error, message) => onFailed?.call(error.toString(), message),
            onSkipped: (id) => onSkipped?.call(),
          );
        },
        onFailed: (id, error, message) {
          debugPrint('Unity Ads: Load Rewarded Failed: $error - $message');
          onFailed?.call(error.toString(), message);
        },
      );
    } catch (e) {
      debugPrint('Unity Ads Show Rewarded Exception: $e');
      onFailed?.call('EXCEPTION', e.toString());
    }
  }

  /// Builds a Banner Ad widget
  static Widget bannerAd({
    VoidCallback? onLoad,
    VoidCallback? onClick,
    Function(String, String)? onFailed,
  }) {
    if (kIsWeb || (defaultTargetPlatform != TargetPlatform.android && defaultTargetPlatform != TargetPlatform.iOS)) {
      return const SizedBox.shrink();
    }
    
    return UnityBannerAd(
      placementId: bannerPlacementId,
      onLoad: (id) {
        debugPrint('Unity Ads: Banner Loaded');
        onLoad?.call();
      },
      onClick: (id) {
        debugPrint('Unity Ads: Banner Clicked');
        onClick?.call();
      },
      onFailed: (id, error, message) {
        debugPrint('Unity Ads: Banner Load Failed: $error - $message');
        onFailed?.call(error.toString(), message);
      },
    );
  }
}
