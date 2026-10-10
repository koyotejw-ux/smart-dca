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
}

class AiSpeechParser {
  /// Parses natural language queries into structured stock DCA parameters.
  /// Handles global multi-lingual patterns:
  /// - Korean: "삼성전자 7만5천원 100주 6만8천원에 50주 물타기", "삼전 75000 100주"
  /// - English: "Apple 180 USD 100 shares, buy 50 shares at 150 USD", "Tesla 240 50 shares 200 30"
  /// - Japanese: "ソニー 12,000円 100株、10,500円で50株 ナンピン"
  /// - Chinese: "腾讯控股 380元 100股，340元补仓 50股"
  /// - Spanish: "Apple 180 USD 100 acc., 150 USD comprar 50 acc."
  /// - Vietnamese: "Vinamilk 75,000 VND 100 cổ, 65,000 mua 50 cổ"
  /// - Indonesian: "BBCA 9,500 IDR 100 lot, 8,500 beli 50 lot"
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

    // 1. Normalize numbers (Korean man/cheon, Japanese man/oku, k/m suffixes, currency symbols)
    String text = _normalizeQuantities(raw);

    // 2. Extract stock name candidate
    String stock = _extractStockName(text);

    // 3. Extract numbers
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
      // e.g. "삼성전자 70000원 100주 60000원 추가" -> default addQty = currentQty / 2 or 10
      currentPrice = numbers[0];
      currentQty = numbers[1];
      addPrice = numbers[2];
      addQty = (currentQty > 0 ? (currentQty / 2).roundToDouble() : 10);
    } else if (numbers.length == 2) {
      // e.g. "삼성전자 70000원 100주" -> default addPrice = -10%, addQty = currentQty
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
        ? "$stock (보유: ${_formatNum(currentPrice)} × ${_formatNum(currentQty)} ➔ 추가: ${_formatNum(addPrice)} × ${_formatNum(addQty)})"
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

  static String _formatNum(double v) {
    if (v == v.roundToDouble()) {
      return v.toInt().toString();
    }
    return v.toStringAsFixed(1);
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

