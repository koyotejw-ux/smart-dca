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
  /// Handles patterns like:
  /// - "삼성전자 7만5천원 100주 6만8천원에 50주 물타기"
  /// - "삼전 75000 100주 68000 50주"
  /// - "애플 180달러 50주 150달러 30주 추가매수"
  /// - "카카오 평단 5만원 100주 현재가 4만원 100주 더사기"
  /// - "Tesla 240 50 shares buy 30 at 200"
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

    // 1. Normalize Korean number expressions: 7만5천 -> 75000, 10만 -> 100000, 1억 -> 100000000
    String text = _normalizeKoreanAmounts(raw);

    // 2. Extract stock name candidate
    String stock = _extractStockName(text);

    // 3. Extract numbers with units or context
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
      // e.g. "삼성전자 70000원 100주 60000원 추가" -> default addQty = 50 or 10
      currentPrice = numbers[0];
      currentQty = numbers[1];
      addPrice = numbers[2];
      addQty = (currentQty > 0 ? (currentQty / 2).roundToDouble() : 10);
    } else if (numbers.length == 2) {
      // e.g. "삼성전자 70000원 100주"
      currentPrice = numbers[0];
      currentQty = numbers[1];
      addPrice = (currentPrice * 0.9).roundToDouble(); // 10% dip default
      addQty = currentQty;
    } else if (numbers.length == 1) {
      currentPrice = numbers[0];
      currentQty = 10;
      addPrice = (currentPrice * 0.9).roundToDouble();
      addQty = 10;
    }

    final isValid = currentPrice > 0 && currentQty > 0 && addPrice > 0 && addQty > 0;
    final summary = isValid
        ? "$stock (보유: ${currentPrice.toInt()}원 × ${currentQty.toInt()}주 ➔ 추가: ${addPrice.toInt()}원 × ${addQty.toInt()}주)"
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

  static String _normalizeKoreanAmounts(String input) {
    String str = input;

    // 만/천 한글 복합 숫자 변환: e.g. "7만 5천", "7만5000", "7만"
    final manPattern = RegExp(r'(\d+)\s*만\s*(\d+)?\s*천?');
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

    // 단순 "X만" -> X0000
    str = str.replaceAllMapped(RegExp(r'(\d+)\s*만'), (m) {
      final v = (int.tryParse(m.group(1) ?? '0') ?? 0) * 10000;
      return " $v ";
    });

    // 단순 "X천" -> X000
    str = str.replaceAllMapped(RegExp(r'(\d+)\s*천'), (m) {
      final v = (int.tryParse(m.group(1) ?? '0') ?? 0) * 1000;
      return " $v ";
    });

    return str;
  }

  static String _extractStockName(String text) {
    // Known stock keywords or first non-number token
    final commonStocks = [
      '삼성전자', '삼전', 'SK하이닉스', '하이닉스', 'LG에너지솔루션', '엔솔',
      '현대차', '기아', '카카오', '네이버', 'NAVER', '셀트리온', '포스코홀딩스',
      '에코프로', '에코프로비엠', '알테오젠', '애플', 'Apple', 'AAPL',
      '테슬라', 'Tesla', 'TSLA', '엔비디아', 'NVIDIA', 'NVDA',
      '마이크로소프트', 'MSFT', '구글', '알파벳', 'GOOGL', '아마존', 'AMZN',
      '비트코인', 'BTC', '이더리움', 'ETH', '리플', 'XRP', '솔라나', 'SOL'
    ];

    for (final s in commonStocks) {
      if (text.contains(s)) {
        return s;
      }
    }

    // Fallback: extract the first word that doesn't look like an action or number
    final cleaned = text.replaceAll(',', ' ').replaceAll('.', ' ');
    final parts = cleaned.split(RegExp(r'\s+')).where((p) => p.trim().isNotEmpty).toList();

    for (final p in parts) {
      if (RegExp(r'^\d').hasMatch(p)) continue;
      if (['물타기', '매수', '추가', '평단가', '평단', '주식', '코인', '사기', '삽니다', '원', '달러', '주', '개', 'buy', 'shares', 'stock', 'at', 'in'].contains(p)) continue;
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
