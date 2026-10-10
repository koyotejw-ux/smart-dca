import 'package:flutter_test/flutter_test.dart';
import 'package:average_down_calculator/services/ai_speech_parser.dart';

void main() {
  group('AiSpeechParser Tests', () {
    test('Standard Korean DCA sentence', () {
      final res = AiSpeechParser.parse("삼성전자 75000원 100주 68000원에 50주 물타기");
      expect(res.stockName, "삼성전자");
      expect(res.currentPrice, 75000);
      expect(res.currentQty, 100);
      expect(res.addPrice, 68000);
      expect(res.addQty, 50);
      expect(res.isValid, true);
    });

    test('Korean man/cheon conversion', () {
      final res = AiSpeechParser.parse("SK하이닉스 18만원 30주, 16만원에 20주 추가");
      expect(res.stockName, "SK하이닉스");
      expect(res.currentPrice, 180000);
      expect(res.currentQty, 30);
      expect(res.addPrice, 160000);
      expect(res.addQty, 20);
      expect(res.isValid, true);
    });

    test('English prompt', () {
      final res = AiSpeechParser.parse("Apple 180 USD 100 shares, buy 50 shares at 150 USD");
      expect(res.stockName, "Apple");
      expect(res.currentPrice, 180);
      expect(res.currentQty, 100);
      expect(res.addPrice, 150);
      expect(res.addQty, 50);
      expect(res.isValid, true);
    });

    test('Verbal Korean numbers test', () {
      final res = AiSpeechParser.parse("삼성전자 칠만오천원 백주 육만팔천원에 오십주 물타기");
      expect(res.stockName, "삼성전자");
      expect(res.currentPrice, 75000);
      expect(res.currentQty, 100);
      expect(res.addPrice, 68000);
      expect(res.addQty, 50);
      expect(res.isValid, true);
    });
  });
}
