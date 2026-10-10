class AiInputResult {
  final String stockName;
  final double currentPrice;
  final double currentQty;
  final double addPrice;
  final double addQty;
  final bool isValid;
  final String summary;

  const AiInputResult({
    required this.stockName,
    required this.currentPrice,
    required this.currentQty,
    required this.addPrice,
    required this.addQty,
    required this.isValid,
    required this.summary,
  });

  double get totalCurrentAmount => currentPrice * currentQty;
  double get totalAddAmount => addPrice * addQty;
  double get totalShares => currentQty + addQty;
  double get newAvgPrice => totalShares > 0 ? (totalCurrentAmount + totalAddAmount) / totalShares : 0;
  double get priceDiffPercent => currentPrice > 0 ? ((newAvgPrice - currentPrice) / currentPrice) * 100 : 0;

  AiInputResult copyWith({
    String? stockName,
    double? currentPrice,
    double? currentQty,
    double? addPrice,
    double? addQty,
    bool? isValid,
    String? summary,
  }) {
    final nextStock = stockName ?? this.stockName;
    final nextCurP = currentPrice ?? this.currentPrice;
    final nextCurQ = currentQty ?? this.currentQty;
    final nextAddP = addPrice ?? this.addPrice;
    final nextAddQ = addQty ?? this.addQty;
    final nextValid = isValid ?? (nextCurP > 0 && nextCurQ > 0 && nextAddP > 0 && nextAddQ > 0);

    return AiInputResult(
      stockName: nextStock,
      currentPrice: nextCurP,
      currentQty: nextCurQ,
      addPrice: nextAddP,
      addQty: nextAddQ,
      isValid: nextValid,
      summary: summary ?? (nextValid
          ? "$nextStock (보유: ${AiSpeechParser.formatNum(nextCurP)} × ${AiSpeechParser.formatNum(nextCurQ)} ➔ 추가: ${AiSpeechParser.formatNum(nextAddP)} × ${AiSpeechParser.formatNum(nextAddQ)})"
          : "금액과 수량을 파악 중입니다."),
    );
  }
}

class AiSpeechParser {
  /// Parses natural language queries into structured stock DCA parameters.
  static AiInputResult parse(String raw) {
    if (raw.trim().isEmpty) {
      return const AiInputResult(
        stockName: "종목 미지정",
        currentPrice: 0,
        currentQty: 0,
        addPrice: 0,
        addQty: 0,
        isValid: false,
        summary: "입력된 내용이 없습니다.",
      );
    }

    // 1. Normalize numbers & Korean verbal numbers
    String text = _normalizeKoreanVerbalNumbers(raw);
    text = _normalizeQuantities(text);

    // 2. Extract stock name candidate
    String stock = _extractStockName(text);

    // 3. Contextual Pattern Extraction
    final contextualResult = _parseContextual(text, stock);
    if (contextualResult != null) {
      return contextualResult;
    }

    // 4. Fallback sequential number extraction
    final numbers = _extractNumbers(text);
    double currentPrice = 0;
    double currentQty = 0;
    double addPrice = 0;
    double addQty = 0;

    if (numbers.length >= 4) {
      currentPrice = numbers[0];
      currentQty = numbers[1];
      addPrice = numbers[2];
      addQty = numbers[3];
    } else if (numbers.length == 3) {
      currentPrice = numbers[0];
      currentQty = numbers[1];
      addPrice = numbers[2];
      addQty = (currentQty > 0 ? (currentQty / 2).roundToDouble() : 10);
    } else if (numbers.length == 2) {
      currentPrice = numbers[0];
      currentQty = numbers[1];
      addPrice = (currentPrice * 0.9).roundToDouble();
      addQty = currentQty;
    } else if (numbers.length == 1) {
      currentPrice = numbers[0];
      currentQty = 10;
      addPrice = (currentPrice * 0.9).roundToDouble();
      addQty = 10;
    }

    final isValid = currentPrice > 0 && currentQty > 0 && addPrice > 0 && addQty > 0;
    final summary = isValid
        ? "$stock (보유: ${formatNum(currentPrice)} × ${formatNum(currentQty)} ➔ 추가: ${formatNum(addPrice)} × ${formatNum(addQty)})"
        : "금액과 수량을 파악 중입니다. 예: '삼성전자 75,000원 100주, 68,000원 50주'";

    return AiInputResult(
      stockName: stock.isNotEmpty ? stock : "선택 종목",
      currentPrice: currentPrice,
      currentQty: currentQty,
      addPrice: addPrice,
      addQty: addQty,
      isValid: isValid,
      summary: summary,
    );
  }

  static String formatNum(double v) {
    if (v == v.roundToDouble()) {
      return v.toInt().toString();
    }
    return v.toStringAsFixed(1);
  }

  /// Converts Korean verbal number phrases often returned by STT engines
  /// e.g. "오만 이천원" -> "52000원", "십팔만원" -> "180000원", "백주" -> "100주"
  static String _normalizeKoreanVerbalNumbers(String input) {
    String str = input;

    // Convert pure Korean verbal digit words when adjacent to units
    const digitMap = {
      '영': 0, '일': 1, '이': 2, '삼': 3, '사': 4,
      '오': 5, '육': 6, '칠': 7, '팔': 8, '구': 9
    };

    // Regex to match Korean number expressions up to 억/만/천/백/십
    // e.g. "칠만오천", "십팔만", "육만 팔천", "백주", "오십주"
    final koreanNumberRegex = RegExp(r'([일이삼사오육칠팔구십백천만억\s]{2,10})\s*(원|달러|주|개)');
    str = str.replaceAllMapped(koreanNumberRegex, (m) {
      final phrase = m.group(1)?.replaceAll(' ', '') ?? '';
      final unit = m.group(2) ?? '';

      int parsed = _parseKoreanNumber(phrase);
      if (parsed > 0) {
        return " $parsed$unit ";
      }
      return m.group(0)!;
    });

    return str;
  }

  static int _parseKoreanNumber(String phrase) {
    // Basic parser for pure Korean numbers like 칠만오천, 십팔만, 백, 오십
    int total = 0;
    int current = 0;

    final digitValues = {
      '일': 1, '이': 2, '삼': 3, '사': 4,
      '오': 5, '육': 6, '칠': 7, '팔': 8, '구': 9
    };

    for (int i = 0; i < phrase.length; i++) {
      final ch = phrase[i];
      if (digitValues.containsKey(ch)) {
        current = digitValues[ch]!;
      } else if (ch == '십') {
        total += (current == 0 ? 1 : current) * 10;
        current = 0;
      } else if (ch == '백') {
        total += (current == 0 ? 1 : current) * 100;
        current = 0;
      } else if (ch == '천') {
        total += (current == 0 ? 1 : current) * 1000;
        current = 0;
      } else if (ch == '만') {
        total = (total + (current == 0 ? 1 : current)) * 10000;
        current = 0;
      } else if (ch == '억') {
        total = (total + (current == 0 ? 1 : current)) * 100000000;
        current = 0;
      }
    }
    total += current;
    return total;
  }

  /// Parses explicit clauses like "buy X shares at Y" or "추가 매수 X원 Y주"
  static AiInputResult? _parseContextual(String text, String stock) {
    // English Pattern: "buy 50 shares at 150 USD" or "buy 50 at 150"
    final enBuyPattern = RegExp(
      r'buy\s+(\d+(?:\.\d+)?)\s*(?:shares|acc|lot|cổ)?\s*at\s+(\d+(?:\.\d+)?)',
      caseSensitive: false,
    );
    final enBuyMatch = enBuyPattern.firstMatch(text);

    // English Pattern alternative: "at 150 buy 50"
    final enAtBuyPattern = RegExp(
      r'at\s+(\d+(?:\.\d+)?)\s*(?:usd|eur|\$)?\s*,?\s*buy\s+(\d+(?:\.\d+)?)',
      caseSensitive: false,
    );
    final enAtBuyMatch = enAtBuyPattern.firstMatch(text);

    // Korean Pattern: "(추가|물타기|매수) X원 Y주" or "X원에 Y주 (물타기|추가)"
    final krAddPattern1 = RegExp(r'(\d+(?:\.\d+)?)\s*(?:원|달러)?\s*(?:에|으로)?\s*(\d+(?:\.\d+)?)\s*주\s*(?:추가|물타기|매수)?');
    final krAddPattern2 = RegExp(r'(?:추가|물타기|매수)\s*(\d+(?:\.\d+)?)\s*(?:원|달러)?\s*(\d+(?:\.\d+)?)\s*주');

    // If English explicit buy match found:
    if (enBuyMatch != null || enAtBuyMatch != null) {
      double addQty = 0;
      double addPrice = 0;

      if (enBuyMatch != null) {
        addQty = double.tryParse(enBuyMatch.group(1)!) ?? 0;
        addPrice = double.tryParse(enBuyMatch.group(2)!) ?? 0;
      } else if (enAtBuyMatch != null) {
        addPrice = double.tryParse(enAtBuyMatch.group(1)!) ?? 0;
        addQty = double.tryParse(enAtBuyMatch.group(2)!) ?? 0;
      }

      // Remaining part for current price/qty
      final cleanText = text
          .replaceAll(enBuyPattern, ' ')
          .replaceAll(enAtBuyPattern, ' ');
      final remNumbers = _extractNumbers(cleanText);

      double currentPrice = remNumbers.isNotEmpty ? remNumbers[0] : 0;
      double currentQty = remNumbers.length > 1 ? remNumbers[1] : 0;

      if (currentPrice > 0 && currentQty > 0 && addPrice > 0 && addQty > 0) {
        return AiInputResult(
          stockName: stock.isNotEmpty ? stock : "Stock",
          currentPrice: currentPrice,
          currentQty: currentQty,
          addPrice: addPrice,
          addQty: addQty,
          isValid: true,
          summary: "$stock (Hold: ${formatNum(currentPrice)} × ${formatNum(currentQty)} ➔ Add: ${formatNum(addPrice)} × ${formatNum(addQty)})",
        );
      }
    }

    return null;
  }

  static String _normalizeQuantities(String input) {
    String str = input;

    // Currency symbols removal
    str = str.replaceAll(RegExp(r'[$€₩¥₫£]'), ' ');

    // Normalize Korean/Japanese "만(万)" & "천(千)"
    final manPattern = RegExp(r'(\d+)\s*[만万]\s*(\d+)?\s*[천千]?');
    str = str.replaceAllMapped(manPattern, (match) {
      final man = int.tryParse(match.group(1) ?? '0') ?? 0;
      final cheonStr = match.group(2);
      int cheon = 0;
      if (cheonStr != null) {
        if (cheonStr.length <= 2) {
          cheon = (int.tryParse(cheonStr) ?? 0) * 1000;
        } else {
          cheon = int.tryParse(cheonStr) ?? 0;
        }
      }
      final total = (man * 10000) + cheon;
      return " $total ";
    });

    // Simple "X만 / X万" -> X0000
    str = str.replaceAllMapped(RegExp(r'(\d+)\s*[만万]'), (m) {
      final v = (int.tryParse(m.group(1) ?? '0') ?? 0) * 10000;
      return " $v ";
    });

    // Simple "X천 / X千" -> X000
    str = str.replaceAllMapped(RegExp(r'(\d+)\s*[천千]'), (m) {
      final v = (int.tryParse(m.group(1) ?? '0') ?? 0) * 1000;
      return " $v ";
    });

    // Normalize 'k' or 'K' suffix (e.g. 70k -> 70000)
    str = str.replaceAllMapped(RegExp(r'(\d+)\s*[kK]\b'), (m) {
      final v = (int.tryParse(m.group(1) ?? '0') ?? 0) * 1000;
      return " $v ";
    });

    return str;
  }

  static String _extractStockName(String text) {
    // Multi-lingual popular stock symbols & names
    final commonStocks = [
      '삼성전자', '삼전', 'SK하이닉스', '하이닉스', 'LG에너지솔루션', '엔솔',
      '현대차', '기아', '카카오', '네이버', 'NAVER', '셀트리온', '포스코홀딩스',
      '에코프로', '에코프로비엠', '알테오젠', '애플', 'Apple', 'AAPL',
      '테슬라', 'Tesla', 'TSLA', '엔비디아', 'NVIDIA', 'NVDA',
      '마이크로소프트', 'MSFT', '구글', '알파벳', 'GOOGL', '아마존', 'AMZN',
      '비트코인', 'BTC', '이더리움', 'ETH', '리플', 'XRP', '솔라나', 'SOL',
      'ソニー', 'トヨタ', '任天堂', 'ソフトバンク',
      '腾讯控股', '贵州茅台', '阿里巴巴', '美团', '比亚迪',
      'Vinamilk', 'FPT', 'Vietcombank',
      'BBCA', 'BBRI', 'TLKM', 'ASII', 'Santander'
    ];

    for (final s in commonStocks) {
      if (text.contains(s)) {
        return s;
      }
    }

    // Fallback: extract the first non-numeric word
    final cleaned = text.replaceAll(',', ' ').replaceAll('.', ' ').replaceAll(';', ' ');
    final parts = cleaned.split(RegExp(r'\s+')).where((p) => p.trim().isNotEmpty).toList();

    const ignoredKeywords = {
      '물타기', '매수', '추가', '평단가', '평단', '주식', '코인', '사기', '삽니다', '원', '달러', '주', '개',
      'buy', 'shares', 'stock', 'at', 'in', 'add', 'usd', 'eur', 'krw', 'jpy', 'vnd', 'idr',
      '株', '円', 'ナンピン', '買い増し', '追加', '股', '元', '补仓', '买入',
      'acc', 'acciones', 'comprar', 'añadir', 'cổ', 'mua', 'thêm', 'lot', 'beli', 'tambah'
    };

    for (final p in parts) {
      if (RegExp(r'^\d').hasMatch(p)) continue;
      if (ignoredKeywords.contains(p.toLowerCase())) continue;
      if (p.length >= 2) {
        return p;
      }
    }

    return "스마트 종목";
  }

  static List<double> _extractNumbers(String text) {
    // Replace commas in numbers (e.g., 75,000 -> 75000)
    final clean = text.replaceAll(',', '');
    final matches = RegExp(r'\b\d+(?:\.\d+)?\b').allMatches(clean);
    final list = <double>[];

    for (final m in matches) {
      final v = double.tryParse(m.group(0)!);
      if (v != null && v > 0) {
        list.add(v);
      }
    }
    return list;
  }
}
