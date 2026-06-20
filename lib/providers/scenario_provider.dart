import 'dart:convert';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/scenario_model.dart';
import '../services/calculator_service.dart';

class ScenarioNotifier extends StateNotifier<List<Scenario>> {
  ScenarioNotifier() : super([]) {
    loadScenarios();
  }

  Future<void> loadScenarios() async {
    final prefs = await SharedPreferences.getInstance();
    final String? data = prefs.getString('saved_scenarios');
    if (data != null) {
      final List<dynamic> list = json.decode(data);
      state = list.map((item) => Scenario(
        id: item['id'],
        name: item['name'],
        initialPrice: item['initialPrice'],
        initialQuantity: item['initialQuantity'],
        batches: (item['batches'] as List).map((b) => PurchaseBatch(
          price: b['price'],
          quantity: b['quantity'],
        )).toList(),
        createdAt: DateTime.parse(item['createdAt']),
      )).toList();
    }
  }

  Future<void> addScenario(Scenario scenario) async {
    state = [scenario, ...state];
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('saved_scenarios', json.encode(state.map((s) => s.toJson()).toList()));
  }

  Future<void> removeScenario(String id) async {
    state = state.where((s) => s.id != id).toList();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('saved_scenarios', json.encode(state.map((s) => s.toJson()).toList()));
  }
}

final scenarioProvider = StateNotifierProvider<ScenarioNotifier, List<Scenario>>((ref) {
  return ScenarioNotifier();
});
