import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/asset_model.dart';
import '../services/storage_service.dart';

final storageServiceProvider = Provider((ref) => StorageService());

final assetsProvider = StateNotifierProvider<AssetNotifier, List<Asset>>((ref) {
  return AssetNotifier(ref.read(storageServiceProvider));
});

class AssetNotifier extends StateNotifier<List<Asset>> {
  final StorageService _storage;

  AssetNotifier(this._storage) : super([]) {
    refresh();
  }

  Future<void> refresh() async {
    state = await _storage.getAssets();
  }

  Future<void> addAsset(Asset asset) async {
    await _storage.insertAsset(asset);
    await refresh();
  }

  Future<void> removeAsset(int id) async {
    await _storage.deleteAsset(id);
    await refresh();
  }
}
