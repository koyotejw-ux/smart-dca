import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# -------------------------------------------------------------
# Color Palettes & Themes per Screen Page
# -------------------------------------------------------------
PAGE_THEMES = [
    {
        'page_idx': 1,
        'id': '01_smart_portfolio',
        'badge_en': 'ALL-IN-ONE SMART PORTFOLIO',
        'badge_ko': '올인원 스마트 포트폴리오',
        'badge_ja': 'オールインワン・スマート資産管理',
        'badge_zh': '一站式智能投资组合',
        'badge_es': 'PORTAFOLIO INTELIGENTE TODO EN UNO',
        'badge_vi': 'DANH MỤC ĐẦU TƯ TẤT CẢ TRONG MỘT',
        'badge_id': 'PORTOFOLIO PINTAR ALL-IN-ONE',
        'title': {
            'ko': ('실시간 자산 & 물타기', '통합 포트폴리오 관리'),
            'en': ('Smart Stock & Crypto', 'DCA Portfolio Hub'),
            'ja': ('リアルタイム資産＆ナンピン', '統合ポートフォリオ管理'),
            'zh': ('实时资产与智能补仓', '一站式持仓成本管理'),
            'es': ('Gestión Inteligente DCA', 'y Portafolio en Tiempo Real'),
            'vi': ('Quản lý Danh mục & DCA', 'Thông minh theo Thời gian thực'),
            'id': ('Portofolio Cerdas & DCA', 'Manajemen Terintegrasi'),
        },
        'sub': {
            'ko': '보유 종목별 실시간 평단가 · 수익률 · 총 투자금을 한눈에',
            'en': 'Track Real-Time Average Price, P&L, and Multi-Asset Capital',
            'ja': '銘柄ごとのリアルタイム平均取得単価・損益・総投資額を一目で把握',
            'zh': '一目了然掌握各持仓标的的实时均价、盈亏率与总投入本金',
            'es': 'Monitorea el precio promedio, ganancias/pérdidas y capital total',
            'vi': 'Theo dõi giá vốn trung bình, lãi/lỗ và tổng vốn đầu tư tức thì',
            'id': 'Pantau harga rata-rata, P&L, dan modal investasi secara instan',
        },
        'grad_top': (8, 18, 42),
        'grad_bottom': (4, 8, 20),
        'glow_color': (0, 130, 255, 90),
        'badge_bg': (15, 45, 95, 230),
        'badge_border': (50, 140, 255, 255),
        'badge_text': (140, 210, 255, 255),
        'raw_img': 'raw_screen_app.png',
        'raw_img_en': 'en_home_screen.png',
    },
    {
        'page_idx': 2,
        'id': '02_dca_simulator',
        'badge_en': '3-STAGE DCA SIMULATOR',
        'badge_ko': '3단계 정밀 물타기 시뮬레이터',
        'badge_ja': '3段階高精度ナンピン計算機',
        'badge_zh': '3阶段高精度智能补仓计算',
        'badge_es': 'SIMULADOR DCA DE 3 ETAPAS',
        'badge_vi': 'MÔ PHỎNG DCA 3 GIAI ĐOẠN',
        'badge_id': 'SIMULATOR DCA 3 TAHAP',
        'title': {
            'ko': ('3단계 정밀 물타기', '평단가 즉시 시뮬레이션'),
            'en': ('3-Stage DCA Simulator', 'Instant Breakeven Calc'),
            'ja': ('3段階の精密ナンピン計算', '平均単価を瞬時にシミュレーション'),
            'zh': ('3阶段精准补仓测算', '实时均价与成本推演'),
            'es': ('Simulación DCA Precisa', 'Cálculo Inmediato de Promedio'),
            'vi': ('Mô phỏng DCA 3 Giai đoạn', 'Tính Giá Trung bình Tức thì'),
            'id': ('Simulator DCA 3 Tahap', 'Hitung Cepat Rata-rata Baru'),
        },
        'sub': {
            'ko': '추가 매수 시 변화하는 최종 평단가와 총 매수 금액 완벽 계산',
            'en': 'Simulate Multi-Batch Buys to Drop Your Cost Basis Perfectly',
            'ja': '追加購入時に変動する最終平均取得単価と所要資金を正確に算出',
            'zh': '精准测算追加买入后的最终持仓均价与所需补仓资金',
            'es': 'Calcula con exactitud el nuevo precio promedio tras compras adicionales',
            'vi': 'Tính toán chính xác giá vốn mới và số vốn cần khi mua thêm',
            'id': 'Kalkulasi akurat harga rata-rata baru setelah pembelian bertahap',
        },
        'grad_top': (6, 28, 38),
        'grad_bottom': (3, 14, 20),
        'glow_color': (0, 220, 170, 85),
        'badge_bg': (10, 60, 60, 230),
        'badge_border': (0, 220, 170, 255),
        'badge_text': (120, 255, 220, 255),
        'raw_img': 'sim_filled_real.png',
        'raw_img_en': 'sim_filled_real.png',
    },
    {
        'page_idx': 3,
        'id': '03_target_calculator',
        'badge_en': 'TARGET PRICE PLANNER',
        'badge_ko': '목표 평단가 역산 플래너',
        'badge_ja': '目標単価・脱出逆算プランナー',
        'badge_zh': '目标均价逆向测算助手',
        'badge_es': 'PLANIFICADOR DE PRECIO OBJETIVO',
        'badge_vi': 'BỘ TÍNH TOÁN GIÁ MỤC TIÊU',
        'badge_id': 'PERENCANA TARGET RATA-RATA',
        'title': {
            'ko': ('목표 평단가 탈출', '역산 플래너 솔루션'),
            'en': ('Target Exit Price Planner', 'Reverse Quantity Calc'),
            'ja': ('希望脱出単価への到達', '必要数量の逆算プランナー'),
            'zh': ('目标解套均价达成', '所需买入数量逆向测算'),
            'es': ('Alcanza tu Precio Objetivo', 'Cálculo Inverso de Cantidad'),
            'vi': ('Đạt Giá Mục tiêu Mong muốn', 'Tính Ngược Khối lượng Cần mua'),
            'id': ('Capai Target Harga Keluar', 'Hitung Mundur Jumlah Beli'),
        },
        'sub': {
            'ko': '원하는 탈출 단가 입력 시 필요한 매수 수량과 자금을 자동 산출',
            'en': 'Enter Your Goal Price: Auto-Calculate Exact Shares & Capital Needed',
            'ja': '希望する脱出単価を入力するだけで、必要な購入株数と資金を自動算出',
            'zh': '输入期望的解套目标价，系统自动反推所需买入的股数与金额',
            'es': 'Ingresa tu precio deseado y obtén la cantidad exacta que debes comprar',
            'vi': 'Nhập giá mục tiêu để biết ngay khối lượng và số vốn cần mua thêm',
            'id': 'Masukkan target harga, dapatkan jumlah lot dan modal yang dibutuhkan',
        },
        'grad_top': (28, 14, 45),
        'grad_bottom': (14, 7, 24),
        'glow_color': (190, 70, 255, 85),
        'badge_bg': (65, 20, 95, 230),
        'badge_border': (200, 80, 255, 255),
        'badge_text': (235, 180, 255, 255),
        'raw_img': 'sim_target_actual.png',
        'raw_img_en': 'sim_target_actual.png',
    },
    {
        'page_idx': 4,
        'id': '04_detailed_report',
        'badge_en': 'PORTFOLIO REPORT & STRATEGY',
        'badge_ko': '자산 배분 리포트 & 전략',
        'badge_ja': '資産配分レポート＆分析',
        'badge_zh': '资产配置分析与报告',
        'badge_es': 'REPORTE Y ESTRATEGIA DE CARTERA',
        'badge_vi': 'BÁO CÁO PHÂN BỔ & CHIẾN LƯỢC',
        'badge_id': 'LAPORAN PORTOFOLIO & STRATEGI',
        'title': {
            'ko': ('상세 자산 배분 리포트', '& 스마트 매매 가이드'),
            'en': ('Asset Allocation Report', '& Smart Trading Insights'),
            'ja': ('詳細な資産配分レポート', '＆スマート投資インサイト'),
            'zh': ('多维度资产分布报告', '与科学交易决策指引'),
            'es': ('Informe Detallado de Cartera', 'y Asignación de Activos'),
            'vi': ('Báo cáo Phân bổ Danh mục', '& Phân tích Lợi nhuận Chuyên sâu'),
            'id': ('Laporan Alokasi Aset', '& Analisis Risiko Portofolio'),
        },
        'sub': {
            'ko': '종목별 투자 비중과 다각화 수준을 분석하여 안전한 분할매수 지원',
            'en': 'Deep Breakdown of Asset Weights and Intelligent Risk Management',
            'ja': '銘柄別の投資比率と分散状況を分析し、安全な分割投資をサポート',
            'zh': '全方位分析各标的持仓权重与分散程度，辅助稳健分批建仓',
            'es': 'Analiza la ponderación de activos y optimiza la diversificación de riesgo',
            'vi': 'Phân tích tỷ trọng danh mục và mức độ đa dạng hóa để giảm thiểu rủi ro',
            'id': 'Analisis bobot investasi aset dan diversifikasi untuk mitigasi risiko',
        },
        'grad_top': (16, 26, 52),
        'grad_bottom': (8, 13, 26),
        'glow_color': (255, 150, 20, 85),
        'badge_bg': (75, 45, 10, 230),
        'badge_border': (255, 165, 30, 255),
        'badge_text': (255, 215, 130, 255),
        'raw_img': 'report_test.png',
        'raw_img_en': 'report_test.png',
    },
    {
        'page_idx': 5,
        'id': '05_global_multi_currency',
        'badge_en': '7 CURRENCIES & 100% PRIVATE',
        'badge_ko': '글로벌 7개국 통화 & 100% 보안',
        'badge_ja': '7通貨対応＆完全ローカル保護',
        'badge_zh': '支持7国货币与本地隐私安全',
        'badge_es': '7 MONEDAS Y 100% PRIVACIDAD',
        'badge_vi': '7 LOẠI TIỀN TỆ & BẢO MẬT 100%',
        'badge_id': '7 MATA UANG & 100% AMAN',
        'title': {
            'ko': ('글로벌 7개 통화 자동 감지', '& 100% 로컬 안심 보안'),
            'en': ('Auto-Detect 7 Currencies', '& 100% On-Device Safe'),
            'ja': ('7カ国通貨・言語に自動対応', '＆完全端末内ローカル保存'),
            'zh': ('自动适配全球主流货币', '与100%设备本地隐私保护'),
            'es': ('Detección de Moneda Local', 'y 100% Seguro Sin Servidor'),
            'vi': ('Tự động Nhận diện Tiền tệ', '& Bảo mật Dữ liệu Tuyệt đối'),
            'id': ('Deteksi Mata Uang Otomatis', '& 100% Aman di Perangkat'),
        },
        'sub': {
            'ko': 'KRW(₩) · USD($) · JPY(¥) · EUR(€) | 서버 전송 없는 철저한 개인정보 보호',
            'en': 'KRW(₩) · USD($) · JPY(¥) · EUR(€) | Zero Server Transmission, Pure Privacy',
            'ja': 'KRW(₩) · USD($) · JPY(¥) · EUR(€) | 外部サーバー送信ゼロの安心セキュリティ',
            'zh': 'KRW(₩) · USD($) · JPY(¥) · EUR(€) | 零服务器上传，纯本地加密储存',
            'es': 'KRW(₩) · USD($) · JPY(¥) · EUR(€) | Tus datos nunca salen de tu dispositivo',
            'vi': 'KRW(₩) · USD($) · JPY(¥) · EUR(€) | Dữ liệu tài sản không gửi lên máy chủ',
            'id': 'KRW(₩) · USD($) · JPY(¥) · EUR(€) | Privasi penuh tanpa pengiriman server',
        },
        'grad_top': (10, 22, 42),
        'grad_bottom': (5, 10, 20),
        'glow_color': (0, 160, 255, 90),
        'badge_bg': (15, 55, 100, 230),
        'badge_border': (60, 170, 255, 255),
        'badge_text': (160, 225, 255, 255),
        'raw_img': 'settings_real.png',
        'raw_img_en': 'settings_real.png',
    }
]

# Supported Languages Definition
SUPPORTED_LANGS = [
    {'code': 'ko', 'name': 'Korean', 'flag': '🇰🇷'},
    {'code': 'en', 'name': 'English', 'flag': '🇺🇸'},
    {'code': 'ja', 'name': 'Japanese', 'flag': '🇯🇵'},
    {'code': 'zh', 'name': 'Chinese', 'flag': '🇨🇳'},
    {'code': 'es', 'name': 'Spanish', 'flag': '🇪🇸'},
    {'code': 'vi', 'name': 'Vietnamese', 'flag': '🇻🇳'},
    {'code': 'id', 'name': 'Indonesian', 'flag': '🇮🇩'},
]

# Device Form Factors
DEVICE_TARGETS = [
    ('phone', (1080, 1920), 0.82),
    ('tablet_7inch', (1200, 1920), 0.74),
    ('tablet_10inch', (1600, 2560), 0.70),
]

def create_rounded_mask(size, radius):
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), size], radius=radius, fill=255)
    return mask

def draw_vertical_gradient(draw, width, height, top_color, bottom_color):
    for y in range(height):
        ratio = y / float(height)
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * ratio)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * ratio)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

def draw_soft_glow(image, center_x, center_y, radius, color):
    glow = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)
    steps = 12
    for i in range(steps, 0, -1):
        cur_radius = int(radius * (i / steps))
        alpha = int(color[3] * ((steps - i + 1) / steps) * 0.45)
        draw.ellipse([
            center_x - cur_radius, center_y - cur_radius,
            center_x + cur_radius, center_y + cur_radius
        ], fill=(color[0], color[1], color[2], alpha))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=radius // 3))
    image.paste(glow, (0, 0), glow)

def get_font_for_lang(lang_code, is_bold=True):
    # Windows system font mapping
    if lang_code == 'ko':
        f = "C:\\Windows\\Fonts\\malgunbd.ttf" if is_bold else "C:\\Windows\\Fonts\\malgun.ttf"
    elif lang_code in ('ja', 'zh'):
        f = "C:\\Windows\\Fonts\\msyhbd.ttc" if is_bold else "C:\\Windows\\Fonts\\msyh.ttc"
        if not os.path.exists(f):
            f = "C:\\Windows\\Fonts\\msgothic.ttc"
    else:
        # Western / European / Vietnamese / Indonesian
        f = "C:\\Windows\\Fonts\\segoeuib.ttf" if is_bold else "C:\\Windows\\Fonts\\segoeui.ttf"
        if not os.path.exists(f):
            f = "C:\\Windows\\Fonts\\arialbd.ttf" if is_bold else "C:\\Windows\\Fonts\\arial.ttf"
            
    if not os.path.exists(f):
        f = "C:\\Windows\\Fonts\\arial.ttf"
    return f

def render_ultra_screenshot(page_cfg, lang_code, device_name, size, frame_ratio, out_path, image_lookup):
    W, H = size
    scale = W / 1080.0
    
    # 1. Base Gradient Canvas
    base = Image.new('RGB', (W, H))
    b_draw = ImageDraw.Draw(base)
    draw_vertical_gradient(b_draw, W, H, page_cfg['grad_top'], page_cfg['grad_bottom'])
    
    # Atmospheric glows (Luxury Neon effect)
    draw_soft_glow(base, int(W * 0.25), int(H * 0.15), int(340 * scale), page_cfg['glow_color'])
    draw_soft_glow(base, int(W * 0.8), int(H * 0.82), int(380 * scale), (30, 70, 140, 65))
    
    canvas = base.convert('RGBA')
    draw = ImageDraw.Draw(canvas)
    
    # 2. Typography Setup
    font_bold = get_font_for_lang(lang_code, is_bold=True)
    font_reg = get_font_for_lang(lang_code, is_bold=False)
    font_western_bold = "C:\\Windows\\Fonts\\segoeuib.ttf"
    
    title_size = int(58 * scale)
    subtitle_size = int(30 * scale)
    badge_size = int(23 * scale)
    
    title_font = ImageFont.truetype(font_bold, title_size)
    sub_font = ImageFont.truetype(font_reg, subtitle_size)
    badge_font = ImageFont.truetype(font_bold, badge_size)
    
    # 3. Badge (Category / Feature Pill)
    badge_key = f"badge_{lang_code}" if f"badge_{lang_code}" in page_cfg else "badge_en"
    badge_text = page_cfg.get(badge_key, page_cfg['badge_en'])
    b_bbox = badge_font.getbbox(badge_text)
    bw = b_bbox[2] - b_bbox[0]
    bh = b_bbox[3] - b_bbox[1]
    
    badge_pad_x = int(24 * scale)
    badge_pad_y = int(9 * scale)
    badge_w = bw + badge_pad_x * 2
    badge_h = bh + badge_pad_y * 2
    badge_x = (W - badge_w) // 2
    badge_y = int(68 * scale)
    
    # Badge Pill with Neon Glow outline
    draw.rounded_rectangle(
        [(badge_x, badge_y), (badge_x + badge_w, badge_y + badge_h)],
        radius=int(badge_h // 2),
        fill=page_cfg['badge_bg'],
        outline=page_cfg['badge_border'],
        width=int(2.5 * scale)
    )
    draw.text(
        (badge_x + badge_pad_x, badge_y + badge_pad_y - int(1.5 * scale)),
        badge_text,
        font=badge_font,
        fill=page_cfg['badge_text']
    )
    
    # 4. Main Titles (Localized)
    titles = page_cfg['title'].get(lang_code, page_cfg['title']['en'])
    title_y = badge_y + badge_h + int(32 * scale)
    for line in titles:
        t_bbox = title_font.getbbox(line)
        tw = t_bbox[2] - t_bbox[0]
        tx = (W - tw) // 2
        
        # Subtle Drop shadow for Title text
        draw.text((tx, title_y + int(2.5 * scale)), line, font=title_font, fill=(0, 0, 0, 140))
        draw.text((tx, title_y), line, font=title_font, fill=(255, 255, 255, 255))
        title_y += int(title_size * 1.26)
        
    # 5. Subtitle (Localized)
    sub_text = page_cfg['sub'].get(lang_code, page_cfg['sub']['en'])
    sub_y = title_y + int(6 * scale)
    s_bbox = sub_font.getbbox(sub_text)
    sw = s_bbox[2] - s_bbox[0]
    sx = (W - sw) // 2
    
    # If subtitle is too long, wrap or constrain
    if sw > W * 0.92:
        sub_size_adj = int(subtitle_size * (W * 0.90 / sw))
        sub_font_adj = ImageFont.truetype(font_reg, max(sub_size_adj, int(20 * scale)))
        s_bbox = sub_font_adj.getbbox(sub_text)
        sw = s_bbox[2] - s_bbox[0]
        sx = (W - sw) // 2
        draw.text((sx, sub_y), sub_text, font=sub_font_adj, fill=(195, 215, 245, 235))
    else:
        draw.text((sx, sub_y), sub_text, font=sub_font, fill=(195, 215, 245, 235))
        
    # 6. Real Screen Selection & Cropping
    # Real Localized Screen selection:
    # 1:1 matching raw screenshot captured on device for each specific language & currency
    root_dir = r"d:\097.flutter_project\average_down_calculator"
    raw_path = os.path.join(root_dir, "store", "raw_screens", lang_code, f"{page_cfg['id']}.png")
    if not os.path.exists(raw_path):
        # Fallback to general lookup if missing
        raw_key = page_cfg['raw_img_en'] if lang_code != 'ko' and 'raw_img_en' in page_cfg else page_cfg['raw_img']
        raw_path = image_lookup.get(raw_key, image_lookup.get(page_cfg['raw_img']))
    
    screen_img = Image.open(raw_path).convert('RGBA')
    
    # Clean bottom crop: remove bottom status/nav buttons or validator popup if present
    # Usually popup starts around y=1900 on 904x2316 screen
    if screen_img.height > 2200:
        crop_h = 1910
        screen_img = screen_img.crop((0, 0, screen_img.width, crop_h))
        
    # Frame sizing
    frame_w = int(W * frame_ratio)
    aspect = screen_img.height / float(screen_img.width)
    frame_h = int(frame_w * aspect)
    
    device_top = sub_y + int(52 * scale)
    max_h = H - device_top + int(120 * scale)
    if frame_h > max_h:
        frame_h = max_h
        frame_w = int(frame_h / aspect)
        
    device_x = (W - frame_w) // 2
    device_y = device_top
    
    # Resize screen
    screen_resized = screen_img.resize((frame_w, frame_h), Image.Resampling.LANCZOS)
    corner_radius = int(36 * scale)
    mask = create_rounded_mask((frame_w, frame_h), corner_radius)
    
    # Outer device bezel/shadow layer (Luxury 3D Floating Mockup)
    shadow_pad = int(48 * scale)
    shadow_img = Image.new('RGBA', (frame_w + shadow_pad * 2, frame_h + shadow_pad * 2), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_img)
    s_draw.rounded_rectangle(
        [(shadow_pad, shadow_pad), (shadow_pad + frame_w, shadow_pad + frame_h)],
        radius=corner_radius,
        fill=(0, 0, 0, 195)
    )
    shadow_blurred = shadow_img.filter(ImageFilter.GaussianBlur(radius=int(32 * scale)))
    canvas.paste(shadow_blurred, (device_x - shadow_pad, device_y - shadow_pad + int(18 * scale)), shadow_blurred)
    
    # Bezel border line (Metallic Dark Titanium finish)
    bezel_pad = int(8 * scale)
    bezel = Image.new('RGBA', (frame_w + bezel_pad * 2, frame_h + bezel_pad * 2), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(bezel)
    b_draw.rounded_rectangle(
        [(0, 0), (frame_w + bezel_pad * 2, frame_h + bezel_pad * 2)],
        radius=corner_radius + bezel_pad,
        fill=(16, 22, 34, 255),
        outline=(65, 90, 135, 230),
        width=int(3.5 * scale)
    )
    canvas.paste(bezel, (device_x - bezel_pad, device_y - bezel_pad), bezel)
    
    # Paste actual real screen
    canvas.paste(screen_resized, (device_x, device_y), mask)
    
    # Save Output
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    canvas.convert('RGB').save(out_path, format='PNG', quality=95)

def main():
    root = r"d:\097.flutter_project\average_down_calculator"
    brain = r"C:\Users\coyot\.gemini\antigravity-ide\brain\11b28641-b715-459c-b556-fc7ec3944b3f"
    brain_temp = os.path.join(brain, ".tempmediaStorage")
    
    # Image Lookup table
    image_lookup = {
        'en_home_screen.png': os.path.join(root, 'en_home_screen.png'),
        'raw_screen_app.png': os.path.join(brain, 'raw_screen_app.png'),
        'sim_filled_real.png': os.path.join(brain, 'sim_filled_real.png'),
        'sim_target_actual.png': os.path.join(root, 'sim_target_actual.png'),
        'report_test.png': os.path.join(root, 'report_test.png'),
        'settings_real.png': os.path.join(brain_temp, 'settings_real.png'),
    }
    
    total_generated = 0
    
    # Generate for all 7 languages and all 3 device form factors
    for lang in SUPPORTED_LANGS:
        lang_code = lang['code']
        print(f"Generating screenshots for Language: {lang['name']} ({lang_code}) ...")
        
        for dev_name, size, ratio in DEVICE_TARGETS:
            out_dir = os.path.join(root, "store", "screenshots", lang_code, dev_name)
            
            for page in PAGE_THEMES:
                out_file = os.path.join(out_dir, f"{page['id']}.png")
                render_ultra_screenshot(
                    page, lang_code, dev_name, size, ratio, out_file, image_lookup
                )
                total_generated += 1
                
    print(f"\n==========================================")
    print(f"SUCCESS: Generated {total_generated} store screenshots across 7 languages and 3 device form factors!")
    print(f"==========================================")

if __name__ == '__main__':
    main()
