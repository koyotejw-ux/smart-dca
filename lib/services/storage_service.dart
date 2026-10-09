import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import '../models/asset_model.dart';

class StorageService {
  static Database? _database;

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDB();
    return _database!;
  }

  Future<Database> _initDB() async {
    String path = join(await getDatabasesPath(), 'assets.db');
    return await openDatabase(
      path,
      version: 3,
      onCreate: (db, version) async {
        await db.execute('''
          CREATE TABLE assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            symbol TEXT,
            initialPrice REAL,
            initialQuantity REAL,
            type TEXT
          )
        ''');
        await db.execute('''
          CREATE TABLE settings (
            key TEXT PRIMARY KEY,
            value TEXT
          )
        ''');
      },
      onUpgrade: (db, oldVersion, newVersion) async {
        if (oldVersion < 2) {
          await db.execute('ALTER TABLE assets ADD COLUMN symbol TEXT DEFAULT ""');
        }
        if (oldVersion < 3) {
          await db.execute('''
            CREATE TABLE IF NOT EXISTS settings (
              key TEXT PRIMARY KEY,
              value TEXT
            )
          ''');
        }
      },
    );
  }

  Future<bool> hasSeenOnboarding() async {
    final db = await database;
    final List<Map<String, dynamic>> maps = await db.query(
      'settings',
      where: 'key = ?',
      whereArgs: ['hasSeenOnboarding'],
    );
    if (maps.isEmpty) return false;
    return maps.first['value'] == 'true';
  }

  Future<void> setSeenOnboarding() async {
    await setSetting('hasSeenOnboarding', 'true');
  }

  Future<String?> getSetting(String key) async {
    final db = await database;
    final List<Map<String, dynamic>> maps = await db.query(
      'settings',
      where: 'key = ?',
      whereArgs: [key],
    );
    if (maps.isEmpty) return null;
    return maps.first['value'] as String?;
  }

  Future<void> setSetting(String key, String value) async {
    final db = await database;
    await db.insert(
      'settings',
      {'key': key, 'value': value},
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
  }

  Future<void> removeSetting(String key) async {
    final db = await database;
    await db.delete(
      'settings',
      where: 'key = ?',
      whereArgs: [key],
    );
  }

  Future<int> insertAsset(Asset asset) async {
    final db = await database;
    return await db.insert('assets', asset.toMap());
  }

  Future<List<Asset>> getAssets() async {
    final db = await database;
    // Auto-migrate legacy mock/crypto placeholder data
    await db.rawUpdate('''
      UPDATE assets 
      SET name = '보유 종목', symbol = 'STOCK' 
      WHERE (name = 'New Asset' OR symbol = 'BTC' OR symbol = 'BTCUSDT')
    ''');
    final List<Map<String, dynamic>> maps = await db.query('assets');
    return List.generate(maps.length, (i) => Asset.fromMap(maps[i]));
  }

  Future<void> deleteAsset(int id) async {
    final db = await database;
    await db.delete('assets', where: 'id = ?', whereArgs: [id]);
  }

  Future<void> clearAllAssets() async {
    final db = await database;
    await db.delete('assets');
  }
}
