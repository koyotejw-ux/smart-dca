import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';
import '../theme/neon_colors.dart';
import 'event_service.dart';
import 'storage_service.dart';

class AdmobService {
  static final StorageService _storage = StorageService();

  // Registered Test Device Hashed IDs for Google AdMob
  // Test devices registered here will automatically receive test ads from Google,
  // while all real users receive production revenue ads!
  static final List<String> _testDeviceIds = [
    // Add known test device IDs; Google AdMob also accepts test device registration via MobileAds.instance.updateRequestConfiguration
  ];

  static bool _forceTestAds = false;
  static bool get forceTestAds => _forceTestAds;
  static set forceTestAds(bool value) => _forceTestAds = value;

  // Real Ad Unit IDs provided by the user
  static const String _realNativeAdUnitId = 'ca-app-pub-1377047377548020/2845475559';
  static const String _realBannerAdUnitId = 'ca-app-pub-1377047377548020/9662165345';
  static const String _realRewardedAdUnitId = 'ca-app-pub-1377047377548020/6784720565';
  static const String _realAppOpenAdUnitId = 'ca-app-pub-1377047377548020/9213912211';
  static const String _realInterstitialAdUnitId = 'ca-app-pub-1377047377548020/3037047246';

  // Standard Google AdMob Test Unit IDs (fallback when test mode is forced)
  static const String _testBannerAndroid = 'ca-app-pub-3940256099942544/6300978111';
  static const String _testBannerIos = 'ca-app-pub-3940256099942544/2934735716';
  static const String _testInterstitialAndroid = 'ca-app-pub-3940256099942544/1033173712';
  static const String _testInterstitialIos = 'ca-app-pub-3940256099942544/4411468910';
  static const String _testRewardedAndroid = 'ca-app-pub-3940256099942544/5224354917';
  static const String _testRewardedIos = 'ca-app-pub-3940256099942544/1712485313';
  static const String _testAppOpenAndroid = 'ca-app-pub-3940256099942544/9257395921';
  static const String _testAppOpenIos = 'ca-app-pub-3940256099942544/5575463023';
  static const String _testNativeAndroid = 'ca-app-pub-3940256099942544/2247696110';
  static const String _testNativeIos = 'ca-app-pub-3940256099942544/3986624511';

  static bool get _isAndroid => defaultTargetPlatform == TargetPlatform.android;

  /// Returns Real Ad Unit ID so production users generate revenue.
  /// When a device is added to testDeviceIds, AdMob automatically serves test ads for that device.
  static String get bannerAdUnitId {
    if (_forceTestAds) {
      return _isAndroid ? _testBannerAndroid : _testBannerIos;
    }
    return _realBannerAdUnitId;
  }

  static String get interstitialAdUnitId {
    if (_forceTestAds) {
      return _isAndroid ? _testInterstitialAndroid : _testInterstitialIos;
    }
    return _realInterstitialAdUnitId;
  }

  static String get rewardedAdUnitId {
    if (_forceTestAds) {
      return _isAndroid ? _testRewardedAndroid : _testRewardedIos;
    }
    return _realRewardedAdUnitId;
  }

  static String get appOpenAdUnitId {
    if (_forceTestAds) {
      return _isAndroid ? _testAppOpenAndroid : _testAppOpenIos;
    }
    return _realAppOpenAdUnitId;
  }

  static String get nativeAdUnitId {
    if (_forceTestAds) {
      return _isAndroid ? _testNativeAndroid : _testNativeIos;
    }
    return _realNativeAdUnitId;
  }

  static bool _isInitialized = false;
  static bool get isInitialized => _isInitialized;

  static AppOpenAd? _appOpenAd;
  static bool _isAppOpenAdLoading = false;

  /// Initialize Google Mobile Ads SDK
  static Future<void> initialize() async {
    if (kIsWeb) return;
    try {
      // By default, always use real production Ad Unit IDs.
      // Registered test devices on Google AdMob console or in testDeviceIds will automatically receive test ads from Google!
      _forceTestAds = false;

      await MobileAds.instance.initialize();
      _isInitialized = true;
      debugPrint("AdMob: Initialized Successfully (forceTestAds: $_forceTestAds)");

      // 2. Set test device configuration so registered devices automatically get test ads from Google!
      final RequestConfiguration requestConfiguration = RequestConfiguration(
        testDeviceIds: _testDeviceIds,
      );
      await MobileAds.instance.updateRequestConfiguration(requestConfiguration);

      loadAppOpenAd(); // Pre-load app open ad
    } catch (e) {
      debugPrint("AdMob Init Error: $e");
    }
  }

  static Future<void> setForceTestAds(bool enabled) async {
    _forceTestAds = enabled;
    await _storage.setSetting('admob_force_test_mode', enabled.toString());
  }

  /// Load App Open Ad
  static void loadAppOpenAd() {
    if (kIsWeb || _isAppOpenAdLoading) return;
    _isAppOpenAdLoading = true;
    AppOpenAd.load(
      adUnitId: appOpenAdUnitId,
      request: const AdRequest(),
      adLoadCallback: AppOpenAdLoadCallback(
        onAdLoaded: (ad) {
          _appOpenAd = ad;
          _isAppOpenAdLoading = false;
          debugPrint("AdMob: AppOpenAd Loaded");
        },
        onAdFailedToLoad: (error) {
          _isAppOpenAdLoading = false;
          debugPrint("AdMob: AppOpenAd load failed: $error");
        },
      ),
    );
  }

  /// Show App Open Ad if available
  static void showAppOpenAd({VoidCallback? onDismiss}) async {
    if (kIsWeb || await EventService.isAdFreeActive() || _appOpenAd == null) {
      onDismiss?.call();
      loadAppOpenAd();
      return;
    }
    _appOpenAd!.fullScreenContentCallback = FullScreenContentCallback(
      onAdDismissedFullScreenContent: (ad) {
        ad.dispose();
        _appOpenAd = null;
        onDismiss?.call();
        loadAppOpenAd(); // Load next one
      },
      onAdFailedToShowFullScreenContent: (ad, error) {
        ad.dispose();
        _appOpenAd = null;
        onDismiss?.call();
        loadAppOpenAd();
      },
    );
    _appOpenAd!.show();
  }

  /// Show Interstitial Ad
  static void showInterstitial({
    required VoidCallback onDismissed,
    Function(AdError)? onFailed,
  }) async {
    if (kIsWeb || await EventService.isAdFreeActive()) {
      onDismissed();
      return;
    }
    InterstitialAd.load(
      adUnitId: interstitialAdUnitId,
      request: const AdRequest(),
      adLoadCallback: InterstitialAdLoadCallback(
        onAdLoaded: (ad) {
          ad.fullScreenContentCallback = FullScreenContentCallback(
            onAdDismissedFullScreenContent: (ad) {
              ad.dispose();
              onDismissed();
            },
            onAdFailedToShowFullScreenContent: (ad, error) {
              ad.dispose();
              onDismissed();
            },
          );
          ad.show();
        },
        onAdFailedToLoad: (error) {
          debugPrint("AdMob: Interstitial Load Failed: $error");
          onFailed?.call(error);
          onDismissed();
        },
      ),
    );
  }

  /// Show Rewarded Ad
  static void showRewarded({
    required Function(RewardItem) onUserEarnedReward,
    required VoidCallback onDismissed,
    Function(AdError)? onFailed,
  }) async {
    if (kIsWeb || await EventService.isAdFreeActive()) {
      onDismissed();
      return;
    }
    RewardedAd.load(
      adUnitId: rewardedAdUnitId,
      request: const AdRequest(),
      rewardedAdLoadCallback: RewardedAdLoadCallback(
        onAdLoaded: (ad) {
          ad.fullScreenContentCallback = FullScreenContentCallback(
            onAdDismissedFullScreenContent: (ad) {
              ad.dispose();
              onDismissed();
            },
            onAdFailedToShowFullScreenContent: (ad, error) {
              ad.dispose();
              onDismissed();
            },
          );
          ad.show(onUserEarnedReward: (adWithoutView, reward) {
            onUserEarnedReward(reward);
          });
        },
        onAdFailedToLoad: (error) {
          debugPrint("AdMob: Rewarded Load Failed: $error");
          onFailed?.call(error);
          onDismissed();
        },
      ),
    );
  }
}

/// A standard inline Banner Ad widget
class AdmobBannerWidget extends StatefulWidget {
  const AdmobBannerWidget({super.key});

  @override
  State<AdmobBannerWidget> createState() => _AdmobBannerWidgetState();
}

class _AdmobBannerWidgetState extends State<AdmobBannerWidget> {
  BannerAd? _bannerAd;
  bool _isLoaded = false;

  @override
  void initState() {
    super.initState();
    if (!kIsWeb) {
      _loadAd();
    }
  }

  void _loadAd() async {
    if (await EventService.isAdFreeActive()) return;
    _bannerAd = BannerAd(
      adUnitId: AdmobService.bannerAdUnitId,
      size: AdSize.banner,
      request: const AdRequest(),
      listener: BannerAdListener(
        onAdLoaded: (ad) {
          if (mounted) {
            setState(() {
              _isLoaded = true;
            });
          }
        },
        onAdFailedToLoad: (ad, error) {
          ad.dispose();
          debugPrint("AdMob: Banner Ad Failed: $error");
        },
      ),
    )..load();
  }

  @override
  void dispose() {
    _bannerAd?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (kIsWeb || _bannerAd == null || !_isLoaded) {
      return const SizedBox.shrink();
    }
    return SizedBox(
      width: _bannerAd!.size.width.toDouble(),
      height: _bannerAd!.size.height.toDouble(),
      child: AdWidget(ad: _bannerAd!),
    );
  }
}

/// A custom styled Native Ad template card
class AdmobNativeAdCard extends StatefulWidget {
  const AdmobNativeAdCard({super.key});

  @override
  State<AdmobNativeAdCard> createState() => _AdmobNativeAdCardState();
}

class _AdmobNativeAdCardState extends State<AdmobNativeAdCard> {
  NativeAd? _nativeAd;
  bool _isLoaded = false;

  @override
  void initState() {
    super.initState();
    if (!kIsWeb) {
      _loadAd();
    }
  }

  void _loadAd() async {
    if (await EventService.isAdFreeActive()) return;
    _nativeAd = NativeAd(
      adUnitId: AdmobService.nativeAdUnitId,
      request: const AdRequest(),
      nativeTemplateStyle: NativeTemplateStyle(
        templateType: TemplateType.medium,
        mainBackgroundColor: NeonColors.surface,
        cornerRadius: 16.0,
        primaryTextStyle: NativeTemplateTextStyle(
          textColor: Colors.white,
          size: 16,
        ),
        secondaryTextStyle: NativeTemplateTextStyle(
          textColor: Colors.white54,
          size: 14,
        ),
        tertiaryTextStyle: NativeTemplateTextStyle(
          textColor: Colors.white38,
          size: 12,
        ),
        callToActionTextStyle: NativeTemplateTextStyle(
          textColor: Colors.black,
          backgroundColor: NeonColors.cyan,
          size: 15,
        ),
      ),
      listener: NativeAdListener(
        onAdLoaded: (ad) {
          if (mounted) {
            setState(() {
              _isLoaded = true;
            });
          }
        },
        onAdFailedToLoad: (ad, error) {
          ad.dispose();
          debugPrint("AdMob: Native Ad Failed: $error");
        },
      ),
    )..load();
  }

  @override
  void dispose() {
    _nativeAd?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (kIsWeb || _nativeAd == null || !_isLoaded) {
      return const SizedBox.shrink();
    }
    return Container(
      margin: const EdgeInsets.only(bottom: 24),
      height: 320,
      decoration: NeonColors.glassyBorder(NeonColors.cyan.withOpacity(0.2)),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(16),
        child: AdWidget(ad: _nativeAd!),
      ),
    );
  }
}
