import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../theme/t_membership_colors.dart';
import '../utils/l10n.dart';
import '../providers/language_provider.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../services/admob_service.dart';

class HelpScreen extends ConsumerWidget {
  const HelpScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final lang = ref.watch(languageProvider);
    final bgColor = isDark ? TMembershipColors.darkBg : TMembershipColors.lightBg;
    final titleColor = isDark ? TMembershipColors.darkTextPrimary : TMembershipColors.lightTextPrimary;

    return Scaffold(
      backgroundColor: bgColor,
      appBar: AppBar(
        backgroundColor: bgColor,
        elevation: 0,
        leadingWidth: 56,
        leading: Padding(
          padding: const EdgeInsets.only(left: 16),
          child: Center(
            child: Material(
              color: Colors.transparent,
              child: InkWell(
                onTap: () => Navigator.pop(context),
                borderRadius: BorderRadius.circular(12),
                child: Container(
                  width: 38,
                  height: 38,
                  decoration: BoxDecoration(
                    color: isDark ? TMembershipColors.darkSurface : Colors.white,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(
                      color: isDark ? TMembershipColors.darkCardBorder : TMembershipColors.lightCardBorder,
                      width: 1.2,
                    ),
                    boxShadow: isDark ? [] : TMembershipColors.softShadow(blur: 6, dy: 2),
                  ),
                  child: Center(
                    child: Icon(Icons.close_rounded, color: titleColor, size: 20),
                  ),
                ),
              ),
            ),
          ),
        ),
        title: Text(
          _getHelpTitle(lang),
          style: GoogleFonts.inter(
            color: titleColor,
            fontWeight: FontWeight.w900,
            fontSize: 18,
            letterSpacing: -0.4,
          ),
        ),
      ),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 800),
          child: ListView(
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
            children: [
              _buildGuideCard(
                title: _getCard1Title(lang),
                content: _getCard1Content(lang),
                icon: Icons.trending_down_rounded,
                color: TMembershipColors.primaryBlue,
                isDark: isDark,
              ),
              const SizedBox(height: 16),
              _buildGuideCard(
                title: _getCard2Title(lang),
                content: _getCard2Content(lang),
                icon: Icons.calculate_rounded,
                color: TMembershipColors.accentPurple,
                isDark: isDark,
              ),
              const SizedBox(height: 16),
              _buildGuideCard(
                title: _getCard3Title(lang),
                content: _getCard3Content(lang),
                icon: Icons.flag_rounded,
                color: TMembershipColors.accentMagenta,
                isDark: isDark,
              ),
              const SizedBox(height: 16),
              _buildGuideCard(
                title: _getCard4Title(lang),
                content: _getCard4Content(lang),
                icon: Icons.mic_rounded,
                color: TMembershipColors.accentMint,
                isDark: isDark,
              ),
              const SizedBox(height: 16),
              _buildGuideCard(
                title: _getCard5Title(lang),
                content: _getCard5Content(lang),
                icon: Icons.domain_rounded,
                color: TMembershipColors.accentOrange,
                isDark: isDark,
              ),
              const SizedBox(height: 24),
              const Center(
                child: SizedBox(
                  height: 50,
                  child: AdmobBannerWidget(),
                ),
              ),
              const SizedBox(height: 20),
              Center(
                child: Text(
                  "Smart Average Down Calculator v3.2\nGlobal Multi-Language Engine Active",
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    color: isDark ? TMembershipColors.darkTextTertiary : TMembershipColors.lightTextTertiary,
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              const SizedBox(height: 32),
            ],
          ),
        ),
      ),
    );
  }

  String _getHelpTitle(LanguageType lang) {
    switch (lang) {
      case LanguageType.ko: return "도움말 및 가이드";
      case LanguageType.ja: return "ヘルプ＆ガイド";
      case LanguageType.zh: return "帮助与指南";
      case LanguageType.es: return "Ayuda y Guía";
      case LanguageType.vi: return "Hướng dẫn & Trợ giúp";
      case LanguageType.id: return "Bantuan & Panduan";
      case LanguageType.en: return "Help & Guide";
    }
  }

  String _getCard1Title(LanguageType lang) {
    switch (lang) {
      case LanguageType.ko: return "물타기(Average Down)란?";
      case LanguageType.ja: return "ナンピン（Average Down）とは？";
      case LanguageType.zh: return "什么是补仓（DCA / 摊平）？";
      case LanguageType.es: return "¿Qué es el Promedio a la Baja?";
      case LanguageType.vi: return "Chiến lược DCA Trung bình giá là gì?";
      case LanguageType.id: return "Apa itu Average Down (DCA)?";
      case LanguageType.en: return "What is Average Down (DCA)?";
    }
  }

  String _getCard1Content(LanguageType lang) {
    switch (lang) {
      case LanguageType.ko:
        return "보유한 자산 가격이 하락했을 때 추가로 분할 매수하여 평균 매수가격을 낮추는 기법입니다. 이후 반등 시 빠르게 원금을 회복하고 수익으로 전환할 수 있습니다.";
      case LanguageType.ja:
        return "保有資産の価格が下落した際に追加買付を行い、平均取得単価を引き下げる投資手法です。反発時に素早く元本を回復し利益化を目指せます。";
      case LanguageType.zh:
        return "在持仓资产价格下跌时分批追加买入，以拉低整体平均持仓成本。价格反弹时可更快保本并转为盈利。";
      case LanguageType.es:
        return "Estrategia que consiste en comprar más acciones a medida que el precio cae para reducir el coste medio por acción, facilitando recuperar el capital y obtener ganancias ante un rebote.";
      case LanguageType.vi:
        return "Phương pháp mua thêm cổ phiếu khi giá giảm để hạ giá vốn trung bình, giúp nhanh chóng hòa vốn và sinh lời khi thị trường phục hồi.";
      case LanguageType.id:
        return "Strategi membeli aset tambahan saat harga turun guna menurunkan harga beli rata-rata, mempercepat pemulihan modal dan potensi cuan saat rebound.";
      case LanguageType.en:
        return "A strategy of buying additional shares as the price drops to lower your overall average purchase price, allowing faster break-even and profit recovery upon rebound.";
    }
  }

  String _getCard2Title(LanguageType lang) {
    switch (lang) {
      case LanguageType.ko: return "스마트 시뮬레이터 사용법";
      case LanguageType.ja: return "シミュレーターの使い方";
      case LanguageType.zh: return "智能计算器使用方法";
      case LanguageType.es: return "Cómo Usar el Simulador";
      case LanguageType.vi: return "Cách dùng máy tính mô phỏng";
      case LanguageType.id: return "Cara Menggunakan Simulator";
      case LanguageType.en: return "How to Use Simulator";
    }
  }

  String _getCard2Content(LanguageType lang) {
    switch (lang) {
      case LanguageType.ko:
        return "1. 현재 보유 중인 평단가와 수량을 입력하세요.\n2. 추가 매수할 가격과 수량을 계획합니다.\n3. 상단 대시보드에서 실시간 신규 평단가를 확인하세요.";
      case LanguageType.ja:
        return "1. 現在の平均取得単価と保有数量を入力します。\n2. 追加買付予定の価格と数量を入力します。\n3. 上部のカードでリアルタイムの新平均単価を確認します。";
      case LanguageType.zh:
        return "1. 输入当前持仓均价与数量。\n2. 设定拟追加补仓的价格与数量。\n3. 在上方卡片中即时查看计算出的新持仓均价。";
      case LanguageType.es:
        return "1. Ingrese su precio promedio actual y cantidad.\n2. Planifique el precio y cantidad de la compra adicional.\n3. Observe el nuevo precio promedio resultante en tiempo real.";
      case LanguageType.vi:
        return "1. Nhập giá vốn trung bình và số lượng hiện tại.\n2. Lên kế hoạch giá mua và số lượng đợt tiếp theo.\n3. Xem giá vốn mới được tính toán ngay lập tức.";
      case LanguageType.id:
        return "1. Masukkan harga rata-rata dan jumlah aset saat ini.\n2. Rencanakan harga dan jumlah pembelian baru.\n3. Lihat hasil harga rata-rata baru secara real-time.";
      case LanguageType.en:
        return "1. Enter your current average price and quantity.\n2. Plan additional buy prices and shares.\n3. Check your real-time updated average price on top.";
    }
  }

  String _getCard3Title(LanguageType lang) {
    switch (lang) {
      case LanguageType.ko: return "목표가 역산 전략 (Target Mode)";
      case LanguageType.ja: return "目標平均単価の逆算 (Target Mode)";
      case LanguageType.zh: return "目标均价逆向推算 (Target Mode)";
      case LanguageType.es: return "Modo Precio Objetivo (Target Mode)";
      case LanguageType.vi: return "Tính số lượng theo giá mục tiêu";
      case LanguageType.id: return "Hitung Target Rata-rata";
      case LanguageType.en: return "Target Price Goal Mode";
    }
  }

  String _getCard3Content(LanguageType lang) {
    switch (lang) {
      case LanguageType.ko:
        return "도달하고 싶은 목표 평단가를 입력하면, 현재 매수가 기준으로 필요한 추가 매수 수량을 자동으로 계산해 줍니다.";
      case LanguageType.ja:
        return "希望する目標の平均取得単価を入力すると、現在の買付価格で必要な購入数量を逆算して提示します。";
      case LanguageType.zh:
        return "设定期望的目标持仓均价，系统将依据当前补仓价格，自动精确逆向计算出所需买入的股数。";
      case LanguageType.es:
        return "Ingrese el precio promedio deseado y calcule automáticamente cuántas acciones exactas necesita comprar al precio actual.";
      case LanguageType.vi:
        return "Nhập giá vốn mong muốn, hệ thống sẽ tự động tính chính xác số lượng cổ phiếu cần mua thêm theo mức giá hiện tại.";
      case LanguageType.id:
        return "Tentukan target harga rata-rata yang diinginkan, sistem akan menghitung persis berapa jumlah aset yang perlu dibeli.";
      case LanguageType.en:
        return "Enter your desired target average price, and it automatically calculates exactly how many shares you need to buy at current price.";
    }
  }

  String _getCard4Title(LanguageType lang) {
    switch (lang) {
      case LanguageType.ko: return "AI 음성 비서 입력";
      case LanguageType.ja: return "AI音声アシスタント";
      case LanguageType.zh: return "AI语音快速录入";
      case LanguageType.es: return "Asistente de Voz AI";
      case LanguageType.vi: return "Trợ lý giọng nói AI";
      case LanguageType.id: return "Asisten Suara AI";
      case LanguageType.en: return "Voice AI Assistant";
    }
  }

  String _getCard4Content(LanguageType lang) {
    switch (lang) {
      case LanguageType.ko:
        return "화면 우측 하단의 AI 비서 버튼을 눌러 음성이나 텍스트로 자연스럽게 입력하면 계산기에 즉시 반영됩니다.";
      case LanguageType.ja:
        return "右下のAIアシスタントボタンをタップして音声やテキストで入力すると、銘柄や単価が自動入力されます。";
      case LanguageType.zh:
        return "点击右下角AI助理按钮，通过语音或文字描述即可快速将价格和数量自动填充至计算器。";
      case LanguageType.es:
        return "Presione el botón AI para dictar o escribir libremente; los datos se completarán automáticamente en el simulador.";
      case LanguageType.vi:
        return "Nhấn nút Trợ lý AI ở góc dưới để nhập bằng giọng nói hoặc văn bản, dữ liệu sẽ tự động điền vào máy tính.";
      case LanguageType.id:
        return "Tekan tombol Asisten AI di kanan bawah untuk input via suara atau teks, data langsung terisi otomatis.";
      case LanguageType.en:
        return "Tap the floating AI Assistant button and speak or type to parse prices and quantities into the calculator.";
    }
  }

  String _getCard5Title(LanguageType lang) {
    switch (lang) {
      case LanguageType.ko: return "주식 전용 계산기 (가상화폐/코인과의 차이점)";
      case LanguageType.ja: return "株式特化型計算（暗号資産との違い）";
      case LanguageType.zh: return "股票专业计算（与虚拟币的区别）";
      case LanguageType.es: return "Cálculo Exclusivo de Acciones (vs Cripto)";
      case LanguageType.vi: return "Công cụ chuyên biệt cho Cổ phiếu";
      case LanguageType.id: return "Kalkulator Khusus Saham (Bukan Kripto)";
      case LanguageType.en: return "Stock Dedicated Engine (vs Crypto)";
    }
  }

  String _getCard5Content(LanguageType lang) {
    switch (lang) {
      case LanguageType.ko:
        return "본 계산기는 비트코인 등 가상자산의 무한 분할 소수점 거래와 달리, 정수 주(Share) 단위 체결과 증권사 거래 수수료를 엄격히 감안하여 설계된 주식 투자자 전용 정밀 계산기입니다.";
      case LanguageType.ja:
        return "ビットコインなどの暗号資産（仮想通貨）の小数点取引とは異なり、1株単位の現物取引や証券会社の売買手数料を前提に設計された株式投資専用ツールです。";
      case LanguageType.zh:
        return "与比特币等虚拟货币支持无限小数位交易不同，本工具专为股票市场的整数股交易及券商佣金规则定制，精准可靠。";
      case LanguageType.es:
        return "Diseñado exclusivamente para el mercado de acciones tradicional (unidades enteras y comisiones de corretaje), diferenciándose de las fracciones de criptomonedas.";
      case LanguageType.vi:
        return "Được xây dựng chuẩn xác cho thị trường cổ phiếu với đơn vị cổ phiếu nguyên và phí giao dịch, không nhầm lẫn với tiền mã hoá.";
      case LanguageType.id:
        return "Dibuat khusus untuk pasar saham dengan satuan unit/lot riil serta memperhitungkan biaya broker, bukan untuk pecahan koin kripto.";
      case LanguageType.en:
        return "Specifically architected for stock equities with whole integer shares and broker fee structures, clearly differentiated from fractional crypto tokens.";
    }
  }

  Widget _buildGuideCard({
    required String title,
    required String content,
    required IconData icon,
    required Color color,
    required bool isDark,
  }) {
    final cardBg = isDark ? TMembershipColors.darkSurface : TMembershipColors.lightSurface;
    final cardBorder = isDark ? TMembershipColors.darkCardBorder : TMembershipColors.lightCardBorder;
    final titleColor = isDark ? TMembershipColors.darkTextPrimary : TMembershipColors.lightTextPrimary;
    final bodyColor = isDark ? TMembershipColors.darkTextSecondary : TMembershipColors.lightTextSecondary;

    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: cardBg,
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: cardBorder, width: 1.2),
        boxShadow: isDark ? [] : TMembershipColors.softShadow(blur: 12, dy: 3),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: color.withOpacity(0.12),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Icon(icon, color: color, size: 22),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Text(
                  title,
                  style: GoogleFonts.inter(fontWeight: FontWeight.w800, fontSize: 16, color: titleColor),
                ),
              ),
            ],
          ),
          const SizedBox(height: 14),
          Text(
            content,
            style: TextStyle(color: bodyColor, fontSize: 13, height: 1.6),
          ),
        ],
      ),
    );
  }
}
