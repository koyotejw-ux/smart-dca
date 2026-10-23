import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
OUT_DIR = 'portfolio/behance_slides'
os.makedirs(OUT_DIR, exist_ok=True)

FONT_DIR = "C:/Windows/Fonts"
WEIGHT_MAP = {
    'black': 'Pretendard-Black.ttf',
    'extrabold': 'Pretendard-ExtraBold.ttf',
    'bold': 'Pretendard-Bold.ttf',
    'semibold': 'Pretendard-SemiBold.ttf',
    'medium': 'Pretendard-Medium.ttf',
    'regular': 'Pretendard-Regular.ttf',
    'light': 'Pretendard-Light.ttf',
}

def get_font(size, weight='bold'):
    w_name = 'bold' if isinstance(weight, bool) and weight else ('regular' if isinstance(weight, bool) else str(weight).lower())
    font_file = WEIGHT_MAP.get(w_name, 'Pretendard-Regular.ttf')
    font_path = os.path.join(FONT_DIR, font_file)
    try:
        return ImageFont.truetype(font_path, int(round(size)))
    except:
        return ImageFont.load_default()

def get_num_font(size, weight='black'):
    return get_font(size, weight)

def wrap_text_by_words(text, font, max_width, draw):
    lines = []
    paragraphs = text.split('\n')
    for p in paragraphs:
        if not p:
            lines.append('')
            continue
        words = p.split(' ')
        current_line = ''
        for word in words:
            test_line = (current_line + ' ' + word).strip()
            bbox = draw.textbbox((0, 0), test_line, font=font)
            w = bbox[2] - bbox[0]
            if w <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
    return lines

# ==============================================================
# Helper: Draw Diamond for Flowchart
def draw_diamond(draw, cx, cy, w, h, fill, outline, width=2):
    pts = [
        (cx, cy - h // 2),
        (cx + w // 2, cy),
        (cx, cy + h // 2),
        (cx - w // 2, cy)
    ]
    draw.polygon(pts, fill=fill, outline=outline)

# Helper: Draw Directional Arrow
def draw_arrow(draw, p1, p2, col=(100, 116, 139), width=2, arrow_size=6):
    x1, y1 = p1
    x2, y2 = p2
    draw.line([(x1, y1), (x2, y2)], fill=col, width=width)
    if x1 == x2: # Vertical
        if y2 > y1: # Down
            draw.polygon([(x2 - arrow_size, y2 - arrow_size * 1.5), (x2 + arrow_size, y2 - arrow_size * 1.5), (x2, y2)], fill=col)
        else: # Up
            draw.polygon([(x2 - arrow_size, y2 + arrow_size * 1.5), (x2 + arrow_size, y2 + arrow_size * 1.5), (x2, y2)], fill=col)
    elif y1 == y2: # Horizontal
        if x2 > x1: # Right
            draw.polygon([(x2 - arrow_size * 1.5, y2 - arrow_size), (x2 - arrow_size * 1.5, y2 + arrow_size), (x2, y2)], fill=col)
        else: # Left
            draw.polygon([(x2 + arrow_size * 1.5, y2 - arrow_size), (x2 + arrow_size * 1.5, y2 + arrow_size), (x2, y2)], fill=col)

# Helper: Draw L-shaped Orthogonal Arrow
def draw_l_arrow(draw, corner, p2, col=(100, 116, 139), width=2, arrow_size=6):
    x_c, y_c = corner
    x2, y2 = p2
    draw.line([(x_c, y_c), (x2, y2)], fill=col, width=width)
    if x_c == x2: # Vertical end
        if y2 > y_c:
            draw.polygon([(x2 - arrow_size, y2 - arrow_size * 1.5), (x2 + arrow_size, y2 - arrow_size * 1.5), (x2, y2)], fill=col)
        else:
            draw.polygon([(x2 - arrow_size, y2 + arrow_size * 1.5), (x2 + arrow_size, y2 + arrow_size * 1.5), (x2, y2)], fill=col)
    elif y_c == y2: # Horizontal end
        if x2 > x_c:
            draw.polygon([(x2 - arrow_size * 1.5, y2 - arrow_size), (x2 - arrow_size * 1.5, y2 + arrow_size), (x2, y2)], fill=col)
        else:
            draw.polygon([(x2 + arrow_size * 1.5, y2 - arrow_size), (x2 + arrow_size * 1.5, y2 + arrow_size), (x2, y2)], fill=col)

# SLIDE 01: Hero Cover & Value Proposition (Stealth Masculine Keynote)
# ==============================================================
def make_slide_01():
    base = Image.new('RGBA', (W, H), (9, 13, 22, 255))
    
    # Ambient Lighting (Samsung Galaxy Blue Atmosphere)
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([1000, 150, 1850, 950], fill=(0, 87, 255, 50))
    gw.ellipse([1200, 300, 1700, 850], fill=(0, 210, 255, 30))
    glow = glow.filter(ImageFilter.GaussianBlur(140))
    base = Image.alpha_composite(base, glow)
    draw = ImageDraw.Draw(base)
    
    # Hairline Boundaries
    draw.line([(120, 100), (1800, 100)], fill=(255, 255, 255, 25), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(255, 255, 255, 25), width=1)
    
    # Kicker
    draw.text((120, 132), "ENTERPRISE FINTECH CASE STUDY", font=get_font(13, 'bold'), fill=(0, 210, 255))
    draw.text((365, 132), "·", font=get_font(13, 'bold'), fill=(100, 116, 139))
    draw.text((385, 132), "ALGORITHMIC QUANT DCA SOLUTION", font=get_font(13, 'bold'), fill=(148, 163, 184))
    
    # Live Store Badge (Samsung Style Clean Pill)
    draw.rounded_rectangle([1590, 122, 1800, 154], radius=16, fill=(16, 185, 129, 25), outline=(16, 185, 129, 90), width=1)
    draw.ellipse([1608, 135, 1616, 143], fill=(16, 185, 129))
    draw.text((1628, 131), "PLAY STORE LIVE", font=get_font(11, 'bold'), fill=(52, 211, 153))
    
    # Headline
    draw.text((120, 210), "하락장 인지 편향을 극복하는\n정량적 분할매수(DCA) 퀀트 솔루션", font=get_font(56, 'black'), fill=(255, 255, 255), spacing=16)
    
    # Subtitle
    draw.text((120, 380), "Overcoming Panic Selling with Algorithmic Position Sizing & Real-time Goal-Seeking", font=get_font(18, 'bold'), fill=(0, 210, 255))
    draw.text((120, 418), "극단적 변동성 장세에서 휴리스틱 오류와 뇌동매매를 차단하고, 0.2초 온디바이스 음성 멀티모달 파서와\nClosed-Form 역산 엔진으로 계좌 방어율을 극대화하는 모바일 퀀트 코어", font=get_font(16.5, 'regular'), fill=(148, 163, 184), spacing=8)
    
    # 3 High-Impact Metric Cards (Left: x=120..920, y=515..885)
    metrics = [
        ("0.2s", "MULTIMODAL INGESTION", "호가 급변 시 0.2초 음성 발화로 정규식 AST 토크나이저 즉각 파싱"),
        ("100%", "GOAL-SEEKING INVERSION", "손익분기점(BEP) 도달에 필요한 추가 매수 수량 폐쇄형 역산"),
        ("24h", "VIP AD-FREE CYCLE", "보상형 광고 1회 시청 기반 24시간 전면 무광고 세션 라이프사이클")
    ]
    
    my = 515
    for val, tag, desc in metrics:
        draw.rounded_rectangle([120, my, 900, my + 110], radius=14, fill=(16, 22, 34, 230), outline=(255, 255, 255, 20), width=1)
        draw.rounded_rectangle([120, my + 16, 124, my + 94], radius=2, fill=(0, 114, 255))
        
        draw.text((148, my + 20), val, font=get_num_font(40, 'black'), fill=(255, 255, 255))
        vw = draw.textlength(val, font=get_num_font(40, 'black'))
        
        tw = draw.textlength(tag, font=get_font(10.5, 'bold'))
        draw.rounded_rectangle([148 + vw + 18, my + 25, 148 + vw + 30 + tw, my + 49], radius=4, fill=(0, 87, 255, 40))
        draw.text((148 + vw + 24, my + 29), tag, font=get_font(10.5, 'bold'), fill=(0, 210, 255))
        
        draw.text((148, my + 72), desc, font=get_font(13.5, 'regular'), fill=(148, 163, 184))
        my += 128
        
    # Right Side: Dual Flagship Galaxy Devices
    # Background phone (Simulator screen)
    phone_back = Image.open('portfolio/galaxy_mockups/galaxy_02_sim.png').convert('RGBA')
    pb_w = 325
    pb_h = int(round(phone_back.height * (pb_w / phone_back.width)))
    phone_back = phone_back.resize((pb_w, pb_h), Image.Resampling.LANCZOS)
    
    # Foreground phone (Home dashboard screen)
    phone_front = Image.open('portfolio/galaxy_mockups/galaxy_01_home.png').convert('RGBA')
    pf_w = 350
    pf_h = int(round(phone_front.height * (pf_w / phone_front.width)))
    phone_front = phone_front.resize((pf_w, pf_h), Image.Resampling.LANCZOS)
    
    # Soft realistic depth shadow
    sh = Image.new('RGBA', (W, H), (0,0,0,0))
    shd = ImageDraw.Draw(sh)
    shd.ellipse([1320, 840, 1320 + pb_w, 910], fill=(0, 0, 0, 180))
    shd.ellipse([1040, 870, 1040 + pf_w, 945], fill=(0, 0, 0, 240))
    sh = sh.filter(ImageFilter.GaussianBlur(32))
    base = Image.alpha_composite(base, sh)
    
    # Paste phones with balanced margins
    base.paste(phone_back, (1320, 220), phone_back)
    base.paste(phone_front, (1040, 185), phone_front)
    
    # Floating App Icon Squircle (Samsung Galaxy Style)
    icon = Image.open('assets/app_icon_clean_squircle.png').convert('RGBA')
    icon_w = 175
    icon = icon.resize((icon_w, icon_w), Image.Resampling.LANCZOS)
    
    icon_sh = Image.new('RGBA', (W, H), (0,0,0,0))
    isd = ImageDraw.Draw(icon_sh)
    isd.ellipse([1400, 715, 1400 + icon_w, 715 + 40], fill=(0, 0, 0, 220))
    icon_sh = icon_sh.filter(ImageFilter.GaussianBlur(24))
    base = Image.alpha_composite(base, icon_sh)
    base.paste(icon, (1400, 565), icon)
    
    base.save(f'{OUT_DIR}/slide_01.png')
    print("SAVED slide_01.png")

# ==============================================================
# SLIDE 02: Discovery & User Research (Stark High-Contrast Editorial)
# ==============================================================
def make_slide_02():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Hairline Grid Accents
    draw.line([(120, 100), (1800, 100)], fill=(226, 232, 240), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(226, 232, 240), width=1)
    
    # Header
    draw.text((120, 130), "01  /  BEHAVIORAL FINANCE RESEARCH & HEURISTIC DISCOVERY", font=get_font(13, 'bold'), fill=(0, 87, 255))
    draw.text((120, 165), "행동재무학적 투자 실패 패턴 분석과 3대 인지 병목", font=get_font(50, 'black'), fill=(15, 23, 42))
    draw.text((120, 240), "리테일 트레이더 428명 정량 설문 및 12명 심층 인터뷰(IDI)를 통해 규명한 하락장 손실 증폭 메커니즘", font=get_font(18, 'regular'), fill=(100, 116, 139))
    
    # Left Column: 3 Massive Stat Cards (Architectural & Masculine)
    stats = [
        ("82.6%", "손실 회피 및 처분 효과 (Disposition Bias)", "수학적 출구 전략 부재로 인한 비이성적 물타기 집행", (220, 38, 38)),
        ("240s→4.2s", "호가 급변 시 입력 레이턴시 (Slip Risk)", "8자리 소수점 키패드 타이핑 중 호가 이탈 및 슬리피지 발생", (217, 119, 6)),
        ("0 / 14개", "주요 증권사 MTS 목표 역산 기능 부재", "단순 사후 평단 합산에 국한되어 목표가 역산 경로 전무", (0, 87, 255))
    ]
    
    sy = 300
    for val, stitle, sdesc, col in stats:
        draw.rounded_rectangle([120, sy, 620, sy + 195], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw.rounded_rectangle([120, sy + 18, 125, sy + 177], radius=2, fill=col)
        
        # Check text length to adjust font size dynamically
        f_size = 42 if len(val) > 6 else 50
        draw.text((155, sy + 26), val, font=get_num_font(f_size, 'black'), fill=col)
        draw.text((155, sy + 105), stitle, font=get_font(16, 'bold'), fill=(15, 23, 42))
        draw.text((155, sy + 138), sdesc, font=get_font(13, 'regular'), fill=(100, 116, 139))
        sy += 225
        
    # Right Column: 3 Concrete IDI Reality Cards
    cards = [
        ("01", "Allocation Drift : 포트폴리오 비중 잠식 & 한계효용 체감",
         "\"단가를 낮추려 4차까지 추가 매수했지만, 예수금 78%가 단일 종목에 고착되고 평단 방어율은 1.8%에 불과했습니다.\"\n— 3년 차 스윙 투자자 IDI (심층 인터뷰)",
         "포트폴리오 비중 왜곡(Allocation Drift) 경보 & 차수별 방어 한계효용(Marginal Utility) 실시간 가시화", (220, 38, 38)),
         
        ("02", "Execution Friction : UI 조작 부하로 인한 슬리피지(Slippage) 손실",
         "\"초 단위로 호가가 무너지는 패닉셀 장세에서 키보드로 단가와 수량을 치다 지지선을 놓쳐 -6.4% 추가 슬리피지가 발생했습니다.\"\n— 크립토 / 모멘텀 단타 트레이더 IDI (심층 인터뷰)",
         "0.2s 온디바이스 STT 멀티모달 파서 & ±5%·±10% 호가 칩 즉시 주입으로 타이핑 레이턴시 98% 제거", (217, 119, 6)),
         
        ("03", "No Exit Strategy : 목표 탈출 단가 도달 필요 수량의 불확실성",
         "\"희망 매도가(예: -3% 손실권)로 탈출하기 위해 정확히 몇 주를 얼마에 사야 하는지 계산할 수 없어 맹목적으로 매수했습니다.\"\n— 5년 차 퀀트 투자자 IDI (심층 인터뷰)",
         "Goal Seeking Closed-Form 수식을 통한 필요 예수금 및 수량의 폐쇄형 역산 알고리즘 탑재", (0, 87, 255))
    ]
    
    ry = 300
    for num, ptitle, pquote, psol, pcol in cards:
        draw.rounded_rectangle([660, ry, 1800, ry + 195], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        
        # Number badge
        draw.rounded_rectangle([695, ry + 24, 735, ry + 56], radius=6, fill=(15, 23, 42))
        draw.text((702, ry + 29), num, font=get_num_font(15, 'bold'), fill=(255, 255, 255))
        draw.text((750, ry + 28), ptitle, font=get_font(17.5, 'bold'), fill=(15, 23, 42))
        
        # Quote Card
        draw.rounded_rectangle([695, ry + 68, 1765, ry + 128], radius=8, fill=(248, 250, 252))
        lines = wrap_text_by_words(pquote, get_font(13.5, 'regular'), 1030, draw)
        qy = ry + 76
        for line in lines[:2]:
            draw.text((715, qy), line, font=get_font(13.5, 'regular'), fill=(71, 85, 105))
            qy += 22
            
        # Solution Tag
        draw.rounded_rectangle([695, ry + 144, 760, ry + 172], radius=4, fill=(0, 87, 255, 20))
        draw.text((703, ry + 148), "SOL", font=get_font(11, 'bold'), fill=(0, 87, 255))
        draw.text((775, ry + 147), psol, font=get_font(13.5, 'semibold'), fill=(30, 41, 59))
        
        ry += 225
        
    base.save(f'{OUT_DIR}/slide_02.png')
    print("SAVED slide_02.png")

# ==============================================================
# SLIDE 03: Benchmark Matrix & Personas (Quantitative Architecture)
# ==============================================================
def make_slide_03():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    draw.line([(120, 100), (1800, 100)], fill=(226, 232, 240), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(226, 232, 240), width=1)
    
    draw.text((120, 130), "02  /  COMPETITIVE BENCHMARK & JTBD BEHAVIORAL PERSONAS", font=get_font(13, 'bold'), fill=(0, 87, 255))
    draw.text((120, 165), "피처 패리티(Feature Parity) 매트릭스 & 핵심 JTBD 페르소나", font=get_font(50, 'black'), fill=(15, 23, 42))
    draw.text((120, 240), "Kano Model 기반 품질 분석(Must-Be vs Delighter)과 퀀트 트레이더 멘탈 모델 기반 페르소나 설계", font=get_font(18, 'regular'), fill=(100, 116, 139))
    
    # Left: High-Precision Comparison Matrix
    tx = 120
    ty = 300
    tw = 960
    draw.rounded_rectangle([tx, ty, tx + tw, ty + 645], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    # Table Header
    draw.rounded_rectangle([tx, ty, tx + tw, ty + 56], radius=16, fill=(241, 245, 249))
    draw.text((tx + 28, ty + 18), "평가 차원 (Dimensions)", font=get_font(14, 'bold'), fill=(71, 85, 105))
    draw.text((tx + 200, ty + 18), "증권사 MTS 내장 (Legacy)", font=get_font(13.5, 'bold'), fill=(71, 85, 105))
    draw.text((tx + 410, ty + 18), "일반 유틸 계산기 (Ad-Heavy)", font=get_font(13.5, 'bold'), fill=(71, 85, 105))
    
    col4_l = tx + 620
    col4_r = tx + tw - 10
    draw.rounded_rectangle([col4_l, ty + 6, col4_r, ty + 639], radius=12, fill=(240, 246, 255), outline=(186, 215, 255), width=2)
    draw.rounded_rectangle([col4_l + 12, ty + 12, col4_r - 12, ty + 50], radius=8, fill=(0, 87, 255))
    draw.text((col4_l + 38, ty + 20), "SMART DCA CALCULATOR", font=get_font(12, 'bold'), fill=(255, 255, 255))
    
    matrix = [
        ("입력 인터랙션 (Modality)", "단일 키패드 (Keypad Only)", "광고 지연 키패드 (Heavy Ad)", "멀티모달 (AI 음성 + 호가 칩)"),
        ("연산 코어 (Math Engine)", "단순 가중평균 (사후 합산)", "1회성 단일 수식 (휘발성)", "Goal-Seeking 폐쇄형 역산 엔진"),
        ("의사결정 지원 (Decision)", "미지원 (단일 결과값)", "미지원", "A vs B 전략 실시간 대조 매트릭스"),
        ("포트폴리오 가드 (Risk)", "계좌 평가액 단순 나열", "미지원", "비중 왜곡(Allocation Drift) 경보"),
        ("데이터 보안 (Privacy)", "중앙 서버 종속 (공인인증)", "임시 세션 (앱 종료 시 리셋)", "Local-First SQLite 100% On-Device"),
        ("수익화 모델 (Monetization)", "타사 금융 상품 배너 혼재", "무차별 전면 팝업 (피로도 극심)", "24h 무광고 VIP 리워드 사이클"),
        ("접근성 & 테마 (A11y)", "다크모드 미흡 / 저대비", "단순 그레이스케일 반전", "OLED WCAG 2.1 AAA 고대비 토큰")
    ]
    
    row_y = ty + 65
    for item, c1, c2, c3 in matrix:
        draw.line([(tx + 20, row_y), (col4_l - 15, row_y)], fill=(241, 245, 249), width=1)
        draw.text((tx + 28, row_y + 20), item, font=get_font(13.5, 'bold'), fill=(15, 23, 42))
        draw.text((tx + 200, row_y + 20), c1, font=get_font(12.5, 'regular'), fill=(100, 116, 139))
        draw.text((tx + 410, row_y + 20), c2, font=get_font(12.5, 'regular'), fill=(100, 116, 139))
        
        draw.ellipse([col4_l + 16, row_y + 24, col4_l + 24, row_y + 32], fill=(0, 87, 255))
        draw.text((col4_l + 32, row_y + 19), c3, font=get_font(12, 'bold'), fill=(0, 87, 255))
        row_y += 81
        
    # Right: 2 High-Impact Persona Cards
    px = 1120
    py = 300
    pw = 680
    
    # Persona A
    draw.rounded_rectangle([px, py, px + pw, py + 308], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([px + 28, py + 22, px + 170, py + 50], radius=6, fill=(240, 246, 255))
    draw.text((px + 36, py + 27), "JTBD ARCHETYPE A", font=get_font(10.5, 'bold'), fill=(0, 87, 255))
    draw.text((px + 185, py + 25), "김투자 (34세, 적립식 퀀트 / 직장인 스윙)", font=get_font(17, 'bold'), fill=(15, 23, 42))
    
    draw.text((px + 28, py + 66), "\"예수금 고갈 없이 6개월 내 손익분기점(BEP)을 탈출할 분할 매수 비율을 원합니다.\"", font=get_font(14, 'bold'), fill=(0, 87, 255))
    desc_a = [
        "• 멘탈 모델 : 엑셀 기반 정량 시뮬레이션을 지향하나 모바일 수식 관리의 한계에 봉착",
        "• 인지 고통 : 추가 매수 차수 누적으로 특정 종목 비중이 80%까지 비대화 (Allocation Drift)",
        "• 핵심 OKR : 시나리오 계산 소요 시간 < 5초 달성 및 가용 예수금 제약 내 최적 평단 도출"
    ]
    dy = py + 106
    for d in desc_a:
        draw.text((px + 28, dy), d, font=get_font(12.5, 'regular'), fill=(71, 85, 105))
        dy += 32
        
    # Persona B
    py += 337
    draw.rounded_rectangle([px, py, px + pw, py + 308], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([px + 28, py + 22, px + 170, py + 50], radius=6, fill=(254, 243, 199))
    draw.text((px + 36, py + 27), "JTBD ARCHETYPE B", font=get_font(10.5, 'bold'), fill=(217, 119, 6))
    draw.text((px + 185, py + 25), "박스캘퍼 (28세, 모멘텀 단타 / 크립토 트레이더)", font=get_font(17, 'bold'), fill=(15, 23, 42))
    
    draw.text((px + 28, py + 66), "\"초단위 급락 빔이 쏟아질 때 키패드 입력 없이 지지선 평단을 0.2초 안에 뽑아야 합니다.\"", font=get_font(14, 'bold'), fill=(217, 119, 6))
    desc_b = [
        "• 멘탈 모델 : 1초 이내 호가 체결이 생명이며 감정적 패닉셀에 휩쓸리지 않는 자동화 도구 필요",
        "• 인지 고통 : 8자리 소수점 단가 타이핑 중 호가 이탈로 인한 지연 슬리피지(Slippage) 발생",
        "• 핵심 OKR : 0.2s 음성 STT 인제스천 및 목표 탈출가 도달 필요 매수량 폐쇄형 역산 주입"
    ]
    dy = py + 106
    for d in desc_b:
        draw.text((px + 28, dy), d, font=get_font(12.5, 'regular'), fill=(71, 85, 105))
        dy += 32
        
    base.save(f'{OUT_DIR}/slide_03.png')
    print("SAVED slide_03.png")

# ==============================================================
# ==============================================================
# SLIDE 04: True Hierarchical Information Architecture (IA Tree)
# ==============================================================
def make_slide_04():
    base = Image.new('RGBA', (W, H), (9, 13, 22, 255))
    draw = ImageDraw.Draw(base)
    
    # Ambient Glow
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([300, 150, 1600, 850], fill=(0, 87, 255, 30))
    gw.ellipse([700, 200, 1220, 600], fill=(0, 210, 255, 20))
    glow = glow.filter(ImageFilter.GaussianBlur(130))
    base = Image.alpha_composite(base, glow)
    draw = ImageDraw.Draw(base)
    
    # Hairline Boundaries
    draw.line([(120, 100), (1800, 100)], fill=(255, 255, 255, 20), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(255, 255, 255, 20), width=1)
    
    # Header
    draw.text((120, 130), "03  /  DOMAIN-DRIVEN INFORMATION ARCHITECTURE (IA TREE)", font=get_font(13, 'bold'), fill=(0, 210, 255))
    draw.text((120, 165), "도메인 주도 설계(DDD) 기반 계층적 정보 구조(IA) 트리", font=get_font(46, 'black'), fill=(255, 255, 255))
    draw.text((120, 230), "시스템 루트(L0)부터 핵심 5대 도메인(L1), 화면 컨테이너(L2), 원자 데이터 토큰 및 인터랙션 액션(L3)까지의 계층적 구조 설계", font=get_font(16, 'regular'), fill=(148, 163, 184))
    
    # IA Level Legend (Top-Right)
    legends = [
        ("L0: 루트 허브 (Root Hub)", (0, 210, 255)),
        ("L1: 핵심 도메인 (Core Domain)", (0, 114, 255)),
        ("L2: 화면/기능 컨테이너 (Container)", (139, 92, 246)),
        ("L3: 원자 토큰 & 액션 (Atomic)", (100, 116, 139))
    ]
    leg_x = 940
    for l_txt, l_col in legends:
        draw.ellipse([leg_x, 134, leg_x + 10, 144], fill=l_col)
        draw.text((leg_x + 16, 131), l_txt, font=get_font(11.5, 'bold'), fill=(148, 163, 184))
        leg_x += draw.textlength(l_txt, font=get_font(11.5, 'bold')) + 24
        
    # ---------------------------------------------------------
    # LEVEL 0: ROOT NODE (System Master Hub)
    # ---------------------------------------------------------
    root_x1, root_y1, root_x2, root_y2 = 710, 260, 1210, 316
    draw.rounded_rectangle([root_x1, root_y1, root_x2, root_y2], radius=14, fill=(16, 22, 34), outline=(0, 210, 255, 180), width=2)
    
    # L0 Badge
    draw.rounded_rectangle([root_x1 + 16, root_y1 + 14, root_x1 + 84, root_y1 + 42], radius=6, fill=(0, 210, 255, 40), outline=(0, 210, 255, 120), width=1)
    draw.text((root_x1 + 25, root_y1 + 19), "L0 ROOT", font=get_font(11, 'bold'), fill=(0, 210, 255))
    
    draw.text((root_x1 + 96, root_y1 + 14), "SMART DCA QUANT PLATFORM", font=get_font(14.5, 'bold'), fill=(255, 255, 255))
    draw.text((root_x1 + 96, root_y1 + 34), "Client-Side DDD Monorepo Architecture", font=get_font(11.5, 'regular'), fill=(148, 163, 184))
    
    # ---------------------------------------------------------
    # ORTHOGONAL TREE CONNECTOR BUS
    # ---------------------------------------------------------
    # Vertical trunk from L0
    draw.line([(960, root_y2), (960, 350)], fill=(0, 210, 255, 180), width=2)
    draw.ellipse([956, 346, 964, 354], fill=(0, 210, 255)) # Trunk junction
    
    # Horizontal master bus across all 5 columns (from 280 to 1640)
    col_centers = [280, 620, 960, 1300, 1640]
    draw.line([(col_centers[0], 350), (col_centers[-1], 350)], fill=(0, 210, 255, 120), width=2)
    
    # 5 Drop branches into L1 domains
    for cx in col_centers:
        draw.ellipse([cx - 4, 350 - 4, cx + 4, 350 + 4], fill=(0, 210, 255)) # Bus junction
        draw_arrow(draw, (cx, 350), (cx, 382), col=(0, 210, 255, 180), width=2, arrow_size=5)
        
    # ---------------------------------------------------------
    # LEVEL 1 & 2 & 3: 5 DOMAIN PILLARS
    # ---------------------------------------------------------
    cw = 320
    cgap = 20
    cols_x = [120 + i * (cw + cgap) for i in range(5)]
    
    domains_data = [
        ("01. BOOT & KERNEL", "시스템 부팅 & 세션 거버넌스", (0, 114, 255), [
            ("L2.1 Cold Boot Orchestrator", "비동기 부팅 & SQLite/Hive 캐시 복원", "$kernel_init · $async_boot_timer · $l10n_bind"),
            ("L2.2 24h VIP Ad-Free Token", "보상형 광고 1회 기반 전면 무광고 세션 제어", "$reward_token · $expire_timestamp · $bypass_flag"),
            ("L2.3 Local ACID Storage Engine", "SQLite & Hive NoSQL 100% 온디바이스 암호화", "$sqlite_cipher · $hive_nosql_box · $schema_v3"),
            ("L2.4 Interactive Onboarding Guide", "DCA 수식 및 역산 알고리즘 튜토리얼", "$step_index · $bep_formula_card · $touch_hint")
        ]),
        
        ("02. ASSET TELEMETRY", "포트폴리오 대시보드 도메인", (0, 210, 255), [
            ("L2.1 Portfolio Telemetry Card", "총 평가액, 실시간 손익률, 종합 위험도 조망", "$total_asset · $unrealized_pnl · $gain_ratio"),
            ("L2.2 Multimodal AI Voice Ingestion", "Google STT 마이크 '종목+단가+수량' 파싱", "$stt_stream · $ast_regex_token · $waveform_fps"),
            ("L2.3 One-Touch Orderbook Presets", "±5%, ±10% 호가 칩으로 키패드 피로도 78% 절감", "$preset_chip_p5 · $preset_chip_p10 · $clear_btn"),
            ("L2.4 2x2 Quick Action Dock", "Fitts' Law 기반 엄지 영역 원클릭 내비게이션", "$route_sim · $route_target · $route_report")
        ]),
        
        ("03. QUANT DCA CORE", "퀀트 시뮬레이션 알고리즘 코어", (139, 92, 246), [
            ("L2.1 Multi-Batch DCA Calculator", "1~N차 분할매수 가중평균 Closed-Form 연산", "$P_0 · $Q_0 · $P_add_1..N · $Q_add_1..N"),
            ("L2.2 Dual-Scenario Comparator", "공격적 vs 보수적 전략 하락률 방어 동시 대조", "$scenario_A_curve · $scenario_B_curve · $bep_gap"),
            ("L2.3 Dynamic Stepper Control", "소프트 키보드 가림 없는 양방향 미세 증감", "$stepper_plus · $stepper_minus · $haptic_tick"),
            ("L2.4 Zero-Latency Feedback Card", "입력 즉시 0ms 신규 평단 및 방어율 렌더링", "$new_avg_price · $drop_defense · $req_cash")
        ]),
        
        ("04. GOAL-SEEKING INVERSION", "목표단가 역산 & 예수금 최적화", (245, 158, 11), [
            ("L2.1 Closed-Form Inversion Engine", "손익분기점(BEP) 도달 필요 주수 폐쇄형 역산", "$calc_Q_add = Q_0(P_0-P_t)/(P_t-P_add)"),
            ("L2.2 Mathematical Invariant Guard", "P_add < P_target < P_0 불변식 위반 실시간 방어", "$invariant_check · $toast_err · $bep_fallback"),
            ("L2.3 Interactive Capital Slider (60fps)", "가용 예수금 제약 한도 내 최적 평단 실시간 도출", "$cash_budget_slider · $achievable_target_bep"),
            ("L2.4 Zero-Loss Parameter Handoff", "도출된 최적 주수를 1탭으로 시뮬레이터 자동 주입", "$handoff_cta · $auto_inject_payload")
        ]),
        
        ("05. RISK AUDIT & GOVERNANCE", "리스크 진단 & 글로벌 규격", (16, 185, 129), [
            ("L2.1 Portfolio Allocation Donut", "종목별 자산 비중 및 단일 종목 집중도 가시화", "$donut_chart · $hhi_concentration · $weight_pct"),
            ("L2.2 3-Tier Volatility Matrix", "안전 / 주의 / 위험 3단계 정밀 리스크 판정", "$safe_badge · $warning_badge · $critical_badge"),
            ("L2.3 Dynamic Locale & FX Currency", "7개국어 L10n 및 KRW/USD/JPY/EUR 통화 체계", "$l10n_7langs · $fx_currency_KRW_USD_JPY_EUR"),
            ("L2.4 Diagnostic Report Export", "종합 진단 리포트 카드 원클릭 클립보드 공유", "$export_png · $clipboard_share · $audit_log")
        ])
    ]
    
    for i, (d_code, d_name, d_col, containers) in enumerate(domains_data):
        cx = cols_x[i]
        
        # Pillar Outer Card
        draw.rounded_rectangle([cx, 385, cx + cw, 955], radius=16, fill=(16, 22, 34), outline=(255, 255, 255, 20), width=1)
        
        # L1 Domain Header Box
        draw.rounded_rectangle([cx + 10, 395, cx + cw - 10, 460], radius=10, fill=(9, 13, 22), outline=(d_col[0], d_col[1], d_col[2], 120), width=1)
        draw.rounded_rectangle([cx + 18, 405, cx + 80, 427], radius=4, fill=(d_col[0], d_col[1], d_col[2], 40))
        draw.text((cx + 25, 409), "L1 DOMAIN", font=get_font(9.5, 'bold'), fill=d_col)
        draw.text((cx + 88, 408), d_code.split('. ')[-1], font=get_font(12, 'bold'), fill=(255, 255, 255))
        draw.text((cx + 18, 435), d_name, font=get_font(13.5, 'bold'), fill=(255, 255, 255))
        
        # Tree branch vertical line within pillar
        tree_x = cx + 24
        draw.line([(tree_x, 460), (tree_x, 930)], fill=(d_col[0], d_col[1], d_col[2], 80), width=2)
        
        # 4 L2 Containers with L3 Tokens
        cy = 475
        for l2_title, l2_desc, l3_tokens in containers:
            # Sub-branch connector from tree vertical line to container card
            draw.line([(tree_x, cy + 24), (cx + 36, cy + 24)], fill=(d_col[0], d_col[1], d_col[2], 120), width=2)
            draw.ellipse([tree_x - 3, cy + 24 - 3, tree_x + 3, cy + 24 + 3], fill=d_col)
            
            # Container Card (L2)
            card_x = cx + 36
            card_w = cw - 46
            draw.rounded_rectangle([card_x, cy, card_x + card_w, cy + 105], radius=10, fill=(9, 13, 22), outline=(255, 255, 255, 15), width=1)
            
            # L2 Title & Badge
            draw.text((card_x + 12, cy + 10), l2_title, font=get_font(12.5, 'bold'), fill=(255, 255, 255))
            draw.text((card_x + 12, cy + 32), l2_desc, font=get_font(11, 'regular'), fill=(148, 163, 184))
            
            # L3 Atomic Token Box
            draw.rounded_rectangle([card_x + 10, cy + 62, card_x + card_w - 10, cy + 95], radius=6, fill=(16, 22, 34), outline=(d_col[0], d_col[1], d_col[2], 50), width=1)
            draw.text((card_x + 16, cy + 68), "• L3 TOKENS:", font=get_font(9.5, 'bold'), fill=d_col)
            draw.text((card_x + 16, cy + 81), l3_tokens, font=get_font(9.5, 'regular'), fill=(148, 163, 184))
            
            cy += 118
            
    base.save(f'{OUT_DIR}/slide_04.png')
    print("SAVED slide_04.png (True Hierarchical IA Tree Architecture)")


# ==============================================================
# SLIDE 05: True UX User Flow & Decision Flowchart
# ==============================================================
def make_slide_05():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Hairline Top/Bottom Boundaries
    draw.line([(120, 100), (1800, 100)], fill=(226, 232, 240), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(226, 232, 240), width=1)
    
    # Header
    draw.text((120, 130), "04  /  END-TO-END USER JOURNEY & DECISION FLOWCHART", font=get_font(13, 'bold'), fill=(0, 87, 255))
    draw.text((120, 165), "사용자 핵심 여정 및 정량적 의사결정 플로우차트", font=get_font(46, 'black'), fill=(15, 23, 42))
    draw.text((120, 230), "위기 감지부터 음성 인제스천, 수학적 불변식 가드, 실시간 슬라이더 최적화 및 영속화까지의 정량적 플로우차트", font=get_font(16, 'regular'), fill=(100, 116, 139))
    
    # Flowchart Legend (Top-Right)
    legends = [
        ("● 시작/종료 (Terminal)", (16, 185, 129)),
        ("■ 화면 상태 (Screen)", (0, 87, 255)),
        ("▬ 사용자 액션 (Action)", (122, 34, 255)),
        ("◆ 조건 분기 (Decision)", (217, 119, 6)),
        ("▱ 시스템/DB (ACID)", (71, 85, 105))
    ]
    leg_x = 980
    for l_txt, l_col in legends:
        draw.ellipse([leg_x, 134, leg_x + 10, 144], fill=l_col)
        draw.text((leg_x + 16, 131), l_txt, font=get_font(11, 'bold'), fill=(71, 85, 105))
        leg_x += draw.textlength(l_txt, font=get_font(11, 'bold')) + 20
        
    # 4 Chronological Lanes
    lw = 390
    lgap = 40
    cols_x = [120 + i * (lw + lgap) for i in range(4)]
    
    lane_headers = [
        ("PHASE 01 : 위기 감지 & 음성 인제스천", "INGESTION PIPELINE", (0, 87, 255)),
        ("PHASE 02 : 퀀트 시뮬레이션 & 역산 진입", "QUANT DCA ENGINE", (0, 160, 255)),
        ("PHASE 03 : 예수금 슬라이더 최적화", "CAPITAL CONSTRAINT", (245, 158, 11)),
        ("PHASE 04 : 리스크 감사 & ACID 영속화", "AUDIT & PERSISTENCE", (16, 185, 129))
    ]
    
    for i, (l_title, l_sub, l_col) in enumerate(lane_headers):
        cx = cols_x[i]
        draw.rounded_rectangle([cx, 275, cx + lw, 318], radius=8, fill=(241, 245, 249), outline=(226, 232, 240), width=1)
        draw.text((cx + 14, 283), l_sub, font=get_font(10, 'bold'), fill=l_col)
        draw.text((cx + 14, 298), l_title, font=get_font(12.5, 'bold'), fill=(15, 23, 42))
        
    # -------------------------------------------------------------
    # LANE 1: Phase 01 - Ingestion Pipeline (cx = cols_x[0])
    # -------------------------------------------------------------
    c0 = cols_x[0]
    mid0 = c0 + lw // 2
    
    # 1.1 Start Pill
    draw.rounded_rectangle([mid0 - 130, 335, mid0 + 130, 375], radius=20, fill=(236, 253, 245), outline=(16, 185, 129), width=2)
    draw.ellipse([mid0 - 115, 350, mid0 - 105, 360], fill=(16, 185, 129))
    draw.text((mid0 - 95, 346), "시장 급락(-23%) 포착 / 앱 실행", font=get_font(12, 'bold'), fill=(6, 95, 70))
    
    draw_arrow(draw, (mid0, 375), (mid0, 400), col=(0, 87, 255))
    
    # 1.2 Screen 01: Home Dashboard
    draw.rounded_rectangle([c0 + 16, 400, c0 + lw - 16, 475], radius=10, fill=(255, 255, 255), outline=(0, 87, 255), width=2)
    draw.rounded_rectangle([c0 + 16, 400, c0 + lw - 16, 426], radius=10, fill=(0, 87, 255))
    draw.text((c0 + 28, 406), "Screen 01. 홈 대시보드 (HomeScreen)", font=get_font(11.5, 'bold'), fill=(255, 255, 255))
    draw.text((c0 + 26, 434), "• 총 평가액 & 실시간 손익률 텔레메트리 조망\n• 24h VIP 세션 유효성 자동 검증 (광고 프리)", font=get_font(11, 'regular'), fill=(51, 65, 85), spacing=3)
    
    draw_arrow(draw, (mid0, 475), (mid0, 500), col=(122, 34, 255))
    
    # 1.3 User Action: Mic Tap
    draw.rounded_rectangle([c0 + 24, 500, c0 + lw - 24, 552], radius=10, fill=(245, 243, 255), outline=(122, 34, 255), width=1)
    draw.text((c0 + 36, 508), "▱ User Action: AI 음성 마이크 탭 (STT)", font=get_font(11.5, 'bold'), fill=(109, 40, 217))
    draw.text((c0 + 36, 528), "\"삼성전자 7만 원에 50주\" 복합 자연어 발화", font=get_font(10.5, 'regular'), fill=(71, 85, 105))
    
    draw_arrow(draw, (mid0, 552), (mid0, 580), col=(217, 119, 6))
    
    # 1.4 Decision Diamond 1: STT Parsed?
    dia1_cy = 635
    draw_diamond(draw, mid0, dia1_cy, 260, 95, fill=(255, 251, 235), outline=(245, 158, 11), width=2)
    draw.text((mid0 - 65, dia1_cy - 16), "자연어 STT 파싱 성공?", font=get_font(12, 'bold'), fill=(180, 83, 9))
    draw.text((mid0 - 58, dia1_cy + 4), "[isSTTParsed == true]", font=get_font(10, 'regular'), fill=(146, 64, 14))
    
    # Diamond 1 - YES Branch (Down)
    draw.text((mid0 + 8, dia1_cy + 52), "YES", font=get_font(10, 'bold'), fill=(21, 128, 61))
    draw_arrow(draw, (mid0, dia1_cy + 48), (mid0, 725), col=(21, 128, 61))
    
    # 1.5 System AST Tokenizer
    draw.rounded_rectangle([c0 + 16, 725, c0 + lw - 16, 795], radius=10, fill=(240, 253, 244), outline=(34, 197, 94), width=1)
    draw.text((c0 + 26, 734), "✓ 0.2s AST 토크나이저 파싱 성공", font=get_font(12, 'bold'), fill=(21, 128, 61))
    draw.text((c0 + 26, 756), "정규식 매칭: [종목: 삼성전자, 단가: 70000, 수량: 50]\n타입 캐스팅 완료 후 시뮬레이터로 즉각 주입", font=get_font(10.5, 'regular'), fill=(22, 101, 52), spacing=2)
    
    # Diamond 1 - NO Branch (Right to Bottom Fallback)
    draw.text((mid0 + 135, dia1_cy - 16), "NO", font=get_font(10, 'bold'), fill=(220, 38, 38))
    # Line from diamond right vertex (mid0 + 130, dia1_cy) -> (c0 + lw - 6, dia1_cy) -> (c0 + lw - 6, 815) -> into Fallback
    draw.line([(mid0 + 130, dia1_cy), (c0 + lw - 6, dia1_cy)], fill=(220, 38, 38), width=2)
    draw.line([(c0 + lw - 6, dia1_cy), (c0 + lw - 6, 840)], fill=(220, 38, 38), width=2)
    draw_arrow(draw, (c0 + lw - 6, 840), (mid0 + 130, 840), col=(220, 38, 38))
    
    # 1.6 Fallback Node
    draw.rounded_rectangle([c0 + 16, 815, c0 + lw - 16, 885], radius=10, fill=(254, 242, 242), outline=(239, 68, 68), width=1)
    draw.text((c0 + 26, 824), "✕ STT 실패 / 권한 거부 시 오프라인 폴백", font=get_font(11.5, 'bold'), fill=(185, 28, 28))
    draw.text((c0 + 26, 846), "±5%, ±10% 호가 프리셋 칩 즉시 대체 노출\n소프트 키패드 수동 입력 모드로 안전 전환", font=get_font(10.5, 'regular'), fill=(153, 27, 27), spacing=2)
    
    # Connector Arrow from Lane 1 to Lane 2:
    draw.line([(c0 + lw - 16, 760), (cols_x[1] - 8, 760)], fill=(0, 87, 255), width=2)
    draw.line([(cols_x[1] - 8, 760), (cols_x[1] - 8, 375)], fill=(0, 87, 255), width=2)
    draw_arrow(draw, (cols_x[1] - 8, 375), (cols_x[1] + 16, 375), col=(0, 87, 255))
    
    # -------------------------------------------------------------
    # LANE 2: Phase 02 - Quant DCA Engine (cx = cols_x[1])
    # -------------------------------------------------------------
    c1 = cols_x[1]
    mid1 = c1 + lw // 2
    
    # 2.1 Screen 02: Simulator
    draw.rounded_rectangle([c1 + 16, 335, c1 + lw - 16, 420], radius=10, fill=(255, 255, 255), outline=(0, 87, 255), width=2)
    draw.rounded_rectangle([c1 + 16, 335, c1 + lw - 16, 361], radius=10, fill=(0, 87, 255))
    draw.text((c1 + 28, 341), "Screen 02. 시뮬레이터 (SimulatorScreen)", font=get_font(11.5, 'bold'), fill=(255, 255, 255))
    draw.text((c1 + 26, 369), "• 3대 세그먼트: 단일 물타기 / 시나리오 A-B / 목표 역산\n• 주입된 현재 포지션(P_0: 78,000원, Q_0: 100주) 로드", font=get_font(11, 'regular'), fill=(51, 65, 85), spacing=3)
    
    draw_arrow(draw, (mid1, 420), (mid1, 445), col=(122, 34, 255))
    
    # 2.2 User Action: Select Goal-Seeking
    draw.rounded_rectangle([c1 + 24, 445, c1 + lw - 24, 495], radius=10, fill=(245, 243, 255), outline=(122, 34, 255), width=1)
    draw.text((c1 + 36, 453), "▱ User Action: '목표 평단가 역산' 모드 선택", font=get_font(11.5, 'bold'), fill=(109, 40, 217))
    draw.text((c1 + 36, 473), "손익분기점(BEP) 탈출 희망 평단 설정 모드 진입", font=get_font(10.5, 'regular'), fill=(71, 85, 105))
    
    draw_arrow(draw, (mid1, 495), (mid1, 520), col=(0, 87, 255))
    
    # 2.3 Input State
    draw.rounded_rectangle([c1 + 20, 520, c1 + lw - 20, 580], radius=8, fill=(248, 250, 252), outline=(203, 213, 225), width=1)
    draw.text((c1 + 30, 528), "파라미터 입력 바인딩:", font=get_font(11, 'bold'), fill=(15, 23, 42))
    draw.text((c1 + 30, 548), "• 희망 목표 평단가 (P_target) : ₩ 70,000\n• 추가 매수 희망가 (P_add) : ₩ 65,000", font=get_font(10.5, 'regular'), fill=(51, 65, 85), spacing=2)
    
    draw_arrow(draw, (mid1, 580), (mid1, 605), col=(217, 119, 6))
    
    # 2.4 Decision Diamond 2: Invariant Check
    dia2_cy = 660
    draw_diamond(draw, mid1, dia2_cy, 270, 95, fill=(255, 251, 235), outline=(245, 158, 11), width=2)
    draw.text((mid1 - 80, dia2_cy - 16), "수학적 경계 불변식 만족?", font=get_font(12, 'bold'), fill=(180, 83, 9))
    draw.text((mid1 - 72, dia2_cy + 4), "[P_add < P_target < P_0]", font=get_font(10, 'bold'), fill=(146, 64, 14))
    
    # Diamond 2 - NO Branch (Invariant Violation)
    draw.text((mid1 - 150, dia2_cy - 16), "NO", font=get_font(10, 'bold'), fill=(220, 38, 38))
    # Line branching left from diamond vertex to Error Toast
    draw.line([(mid1 - 135, dia2_cy), (c1 + 6, dia2_cy)], fill=(220, 38, 38), width=2)
    draw.line([(c1 + 6, dia2_cy), (c1 + 6, 745)], fill=(220, 38, 38), width=2)
    draw_arrow(draw, (c1 + 6, 745), (c1 + 16, 745), col=(220, 38, 38))
    
    # 2.5 Error Toast Guard
    draw.rounded_rectangle([c1 + 16, 720, c1 + lw - 16, 785], radius=8, fill=(254, 242, 242), outline=(239, 68, 68), width=1)
    draw.text((c1 + 26, 729), "⚠️ 경계 불변식 위반 (도달 불가 목표가)", font=get_font(11.5, 'bold'), fill=(185, 28, 28))
    draw.text((c1 + 26, 751), "에러 가이드 토스트 호출 & 입력 버튼 비활성화\n현재 투입 가능 현실적 목표가 실시간 역추천", font=get_font(10.5, 'regular'), fill=(153, 27, 27), spacing=2)
    
    # Diamond 2 - YES Branch (Down)
    draw.text((mid1 + 8, dia2_cy + 52), "YES", font=get_font(10, 'bold'), fill=(21, 128, 61))
    draw_arrow(draw, (mid1, dia2_cy + 48), (mid1, 815), col=(21, 128, 61))
    
    # 2.6 Closed-Form Formula Engine
    draw.rounded_rectangle([c1 + 16, 815, c1 + lw - 16, 915], radius=10, fill=(240, 246, 255), outline=(0, 87, 255), width=2)
    draw.text((c1 + 26, 824), "Closed-Form 역산 연산 엔진 가동", font=get_font(12, 'bold'), fill=(0, 87, 255))
    draw.text((c1 + 26, 846), "Q_add = Q_0 × (P_0 - P_t) / (P_t - P_add)", font=get_num_font(11.5, 'bold'), fill=(15, 23, 42))
    draw.text((c1 + 26, 872), "• 필요 추가 매수 주수 : +42.5 주 (정밀 소수점)\n• 총 소요 자금 : ₩ 2,125,000 (0.001초 산출)", font=get_font(10.5, 'regular'), fill=(51, 65, 85), spacing=2)
    
    # Connector Arrow from Lane 2 to Lane 3:
    draw.line([(c1 + lw - 16, 865), (cols_x[2] - 8, 865)], fill=(0, 87, 255), width=2)
    draw.line([(cols_x[2] - 8, 865), (cols_x[2] - 8, 375)], fill=(0, 87, 255), width=2)
    draw_arrow(draw, (cols_x[2] - 8, 375), (cols_x[2] + 16, 375), col=(0, 87, 255))
    
    # -------------------------------------------------------------
    # LANE 3: Phase 03 - Capital Constraint (cx = cols_x[2])
    # -------------------------------------------------------------
    c2 = cols_x[2]
    mid2 = c2 + lw // 2
    
    # 3.1 Result Card
    draw.rounded_rectangle([c2 + 16, 335, c2 + lw - 16, 420], radius=10, fill=(255, 255, 255), outline=(0, 87, 255), width=2)
    draw.rounded_rectangle([c2 + 16, 335, c2 + lw - 16, 361], radius=10, fill=(0, 87, 255))
    draw.text((c2 + 28, 341), "State: 역산 산출 결과 피드백 카드", font=get_font(11.5, 'bold'), fill=(255, 255, 255))
    draw.text((c2 + 26, 369), "• 산출 목표: ₩70,000 도달 (+42.5주 추가 매수 필요)\n• 총 필요 자금: ₩ 2,125,000 도출 완료", font=get_font(11, 'regular'), fill=(51, 65, 85), spacing=3)
    
    draw_arrow(draw, (mid2, 420), (mid2, 445), col=(122, 34, 255))
    
    # 3.2 User Action: Slider Drag
    draw.rounded_rectangle([c2 + 24, 445, c2 + lw - 24, 505], radius=10, fill=(245, 243, 255), outline=(122, 34, 255), width=1)
    draw.text((c2 + 36, 453), "▱ User Action: 가용 예수금 슬라이더 조절", font=get_font(11.5, 'bold'), fill=(109, 40, 217))
    draw.text((c2 + 36, 473), "Capital Constraint Optimizer (60fps 실시간)\n현재 계좌 가용 현금(₩1,500,000) 한도 드래그", font=get_font(10.5, 'regular'), fill=(71, 85, 105), spacing=2)
    
    draw_arrow(draw, (mid2, 505), (mid2, 530), col=(217, 119, 6))
    
    # 3.3 Decision Diamond 3: Budget Limit?
    dia3_cy = 585
    draw_diamond(draw, mid2, dia3_cy, 270, 95, fill=(255, 251, 235), outline=(245, 158, 11), width=2)
    draw.text((mid2 - 76, dia3_cy - 16), "필요 자금 <= 가용 예수금?", font=get_font(12, 'bold'), fill=(180, 83, 9))
    draw.text((mid2 - 68, dia3_cy + 4), "[Total_Cash <= Budget]", font=get_font(10, 'bold'), fill=(146, 64, 14))
    
    # Diamond 3 - NO Branch (Budget Exceeded Optimizer)
    draw.text((mid2 + 135, dia3_cy - 16), "NO", font=get_font(10, 'bold'), fill=(217, 119, 6))
    draw.line([(mid2 + 135, dia3_cy), (c2 + lw - 6, dia3_cy)], fill=(217, 119, 6), width=2)
    draw.line([(c2 + lw - 6, dia3_cy), (c2 + lw - 6, 665)], fill=(217, 119, 6), width=2)
    draw_arrow(draw, (c2 + lw - 6, 665), (mid2 + 130, 665), col=(217, 119, 6))
    
    # 3.4 Constraint Adjustment Feedback
    draw.rounded_rectangle([c2 + 16, 645, c2 + lw - 16, 715], radius=8, fill=(255, 251, 235), outline=(245, 158, 11), width=1)
    draw.text((c2 + 26, 654), "예수금 한도 내 매수 가능 주수 피드백", font=get_font(11.5, 'bold'), fill=(180, 83, 9))
    draw.text((c2 + 26, 676), "150만 원 한도 내 최대 매수: +23주 (₩1,495,000)\n도달 가능 최적 조정 평단: ₩72,439 실시간 제안", font=get_font(10.5, 'regular'), fill=(146, 64, 14), spacing=2)
    
    # Diamond 3 - YES Branch (Down)
    draw.text((mid2 + 8, dia3_cy + 52), "YES", font=get_font(10, 'bold'), fill=(21, 128, 61))
    draw_arrow(draw, (mid2, dia3_cy + 48), (mid2, 745), col=(21, 128, 61))
    
    # 3.5 Execution Confirmation Plan
    draw.rounded_rectangle([c2 + 16, 745, c2 + lw - 16, 825], radius=10, fill=(240, 253, 244), outline=(34, 197, 94), width=1)
    draw.text((c2 + 26, 754), "✓ 최적 분할매수 계획 확정", font=get_font(12, 'bold'), fill=(21, 128, 61))
    draw.text((c2 + 26, 776), "• 확정 매수: +42.5주 (소요 ₩2,125,000)\n• 신규 방어 평단: ₩70,000 (하락률 방어 +11.4%p)", font=get_font(10.5, 'regular'), fill=(22, 101, 52), spacing=2)
    
    draw_arrow(draw, (mid2, 825), (mid2, 855), col=(0, 87, 255))
    
    # 3.6 User Action: Handoff
    draw.rounded_rectangle([c2 + 20, 855, c2 + lw - 20, 915], radius=10, fill=(0, 87, 255), outline=(0, 87, 255), width=1)
    draw.text((c2 + 32, 866), "▱ 1-Tap 시뮬레이터 파라미터 인계", font=get_font(12, 'bold'), fill=(255, 255, 255))
    draw.text((c2 + 32, 888), "산출 결과를 1초 내 시뮬레이터로 자동 주입", font=get_font(10.5, 'regular'), fill=(220, 235, 255))
    
    # Connector Arrow from Lane 3 to Lane 4:
    draw.line([(c2 + lw - 20, 885), (cols_x[3] - 8, 885)], fill=(0, 87, 255), width=2)
    draw.line([(cols_x[3] - 8, 885), (cols_x[3] - 8, 375)], fill=(0, 87, 255), width=2)
    draw_arrow(draw, (cols_x[3] - 8, 375), (cols_x[3] + 16, 375), col=(0, 87, 255))
    
    # -------------------------------------------------------------
    # LANE 4: Phase 04 - Audit & Persistence (cx = cols_x[3])
    # -------------------------------------------------------------
    c3 = cols_x[3]
    mid3 = c3 + lw // 2
    
    # 4.1 Screen 03: Risk Report
    draw.rounded_rectangle([c3 + 16, 335, c3 + lw - 16, 420], radius=10, fill=(255, 255, 255), outline=(0, 87, 255), width=2)
    draw.rounded_rectangle([c3 + 16, 335, c3 + lw - 16, 361], radius=10, fill=(0, 87, 255))
    draw.text((c3 + 28, 341), "Screen 03. 리스크 감사 (RiskReportScreen)", font=get_font(11.5, 'bold'), fill=(255, 255, 255))
    draw.text((c3 + 26, 369), "• 종목별 자산 비중 도넛 차트 실시간 가시화\n• 단일 종목 집중도(HHI) 및 포트폴리오 왜곡 진단", font=get_font(11, 'regular'), fill=(51, 65, 85), spacing=3)
    
    draw_arrow(draw, (mid3, 420), (mid3, 445), col=(217, 119, 6))
    
    # 4.2 Decision Diamond 4: Concentration Risk?
    dia4_cy = 495
    draw_diamond(draw, mid3, dia4_cy, 270, 90, fill=(255, 251, 235), outline=(245, 158, 11), width=2)
    draw.text((mid3 - 75, dia4_cy - 16), "단일 종목 과밀 편중 위험?", font=get_font(12, 'bold'), fill=(180, 83, 9))
    draw.text((mid3 - 70, dia4_cy + 4), "[Asset_Weight > 40%]", font=get_font(10, 'bold'), fill=(146, 64, 14))
    
    # Diamond 4 - YES (Concentration Alert)
    draw.text((mid3 + 8, dia4_cy + 48), "YES", font=get_font(10, 'bold'), fill=(217, 119, 6))
    draw_arrow(draw, (mid3, dia4_cy + 45), (mid3, 570), col=(217, 119, 6))
    
    # 4.3 Warning Badge Node
    draw.rounded_rectangle([c3 + 16, 570, c3 + lw - 16, 630], radius=8, fill=(254, 243, 199), outline=(245, 158, 11), width=1)
    draw.text((c3 + 26, 578), "⚠️ 3-Tier 위험 판정: 단일 종목 65% 편중 경고", font=get_font(11, 'bold'), fill=(180, 83, 9))
    draw.text((c3 + 26, 598), "물타기 집행 후 집중도 과밀 방지 분산 권고 배지 노출", font=get_font(10, 'regular'), fill=(146, 64, 14))
    
    draw_arrow(draw, (mid3, 630), (mid3, 655), col=(71, 85, 105))
    
    # 4.4 Local ACID Storage Engine Node
    draw.rounded_rectangle([c3 + 16, 655, c3 + lw - 16, 745], radius=10, fill=(241, 245, 249), outline=(71, 85, 105), width=2)
    draw.text((c3 + 26, 664), "▱ 로컬 SQLite & Hive ACID 영속화", font=get_font(12, 'bold'), fill=(30, 41, 59))
    draw.text((c3 + 26, 686), "• 온디바이스 암호화 DB 트랜잭션 0ms 커밋\n• 네트워크 오프라인 상태에서도 100% 무손실 보존\n• 시나리오 히스토리 장부 자동 기록 완료", font=get_font(10.5, 'regular'), fill=(71, 85, 105), spacing=2)
    
    draw_arrow(draw, (mid3, 745), (mid3, 775), col=(16, 185, 129))
    
    # 4.5 End Terminal Capsule
    draw.rounded_rectangle([mid3 - 135, 775, mid3 + 135, 825], radius=24, fill=(236, 253, 245), outline=(16, 185, 129), width=2)
    draw.ellipse([mid3 - 120, 794, mid3 - 110, 804], fill=(16, 185, 129))
    draw.text((mid3 - 98, 792), "최적 분할매수 확정 & 계좌 방어 완료", font=get_font(12, 'bold'), fill=(6, 95, 70))
    
    draw_arrow(draw, (mid3, 825), (mid3, 855), col=(0, 87, 255))
    
    # 4.6 Share / Export Action
    draw.rounded_rectangle([c3 + 24, 855, c3 + lw - 24, 915], radius=10, fill=(255, 255, 255), outline=(0, 87, 255), width=1)
    draw.text((c3 + 36, 866), "진단 리포트 PNG 원클릭 클립보드 공유", font=get_font(11.5, 'bold'), fill=(0, 87, 255))
    draw.text((c3 + 36, 888), "고화질 요약 카드 이미지 갤러리 저장 및 공유", font=get_font(10.5, 'regular'), fill=(71, 85, 105))
    
    base.save(f'{OUT_DIR}/slide_05.png')
    print("SAVED slide_05.png (True UX User Flow & Decision Flowchart)")


# SLIDE 06: 3 Real Mobile Wireframe CAD Blueprints
# ==============================================================
def make_slide_06():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Hairline Top/Bottom Boundaries
    draw.line([(120, 100), (1800, 100)], fill=(226, 232, 240), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(226, 232, 240), width=1)
    
    # Header
    draw.text((120, 130), "05  /  WIREFRAME & STRUCTURAL RATIONALE", font=get_font(13, 'bold'), fill=(0, 87, 255))
    draw.text((120, 165), "와이어프레임 구조 설계 및 기능 1:1 매핑 명세", font=get_font(50, 'black'), fill=(15, 23, 42))
    draw.text((120, 240), "Fitts' Law, 48dp 터치 타깃, 엄지 영역(Thumb Zone) 최적화로 인지 부하(Cognitive Load)를 최소화한 3대 핵심 모바일 와이어프레임", font=get_font(18, 'regular'), fill=(100, 116, 139))
    
    # 3 Screen Columns
    cols_data = [
        ("Screen 01. 홈 대시보드 골격", 120, 430, [
            ("① 인지 부하 0% 집약", "총 투자 원금과 실시간 손익률을 최상단 단일 카드에 집약하여 계좌 현황 0초 조망"),
            ("② 0.2s 음성 인제스천", "호가 급변 시 즉각 발화할 수 있는 원터치 STT 버튼 및 오디오 파형 도크 배치"),
            ("③ 원터치 호가 프리셋", "키패드 8자리 소수점 입력 피로도를 78% 줄이는 ±5%, ±10% 호가 칩 제공"),
            ("④ Thumb Zone 도크", "Fitts' Law 기반 엄지손가락 터치 반경 내 시뮬레이터 진입 및 리포트 열람 CTA 배치")
        ]),
        ("Screen 02. 시뮬레이터 골격", 680, 990, [
            ("① Segmented Control", "단일 계산 / 시나리오 A vs B / 목표 역산 탭을 상단에 두어 0초 모드 전환"),
            ("② 양방향 스텝퍼 컨트롤", "소프트 키보드 가림 현상을 방지하는 +/- 스텝퍼 증감 인터랙션 지원"),
            ("③ Zero-Latency 피드백", "입력 즉시 신규 평단가와 하락률 방어폭을 하단 결과 카드에 0ms 렌더링"),
            ("④ ACID 로컬 영속화 CTA", "시뮬레이션 완료 결과를 로컬 DB에 영구 저장하고 리포트로 1초 인계")
        ]),
        ("Screen 03. 목표 역산 엔진 골격", 1240, 1550, [
            ("① Context 고정 앵커", "현재 보유 평단과 수량을 상단에 고정하여 목표 평단과의 갭 직관적 인지"),
            ("② 경계 불변식 가드", "도달 불가 목표가(Target <= Current) 입력 시 실시간 유효성 에러 가드"),
            ("③ Capital Constraint", "가용 예수금 제약 한도 내에서 도달 가능한 최적 평단을 60fps 인터랙티브 조절"),
            ("④ Zero-Loss 파라미터 인계", "Closed-Form으로 도출된 필요 매수 수량을 시뮬레이터로 1초 자동 주입")
        ])
    ]
    
    pw = 285
    ph = 550
    py = 325
    
    for s_title, px, cx, rationales in cols_data:
        # Screen Title Badge (Dynamic Width, positioned at y=275..307)
        tw = draw.textlength(s_title, font=get_font(13.5, 'bold'))
        draw.rounded_rectangle([px, 275, px + int(tw + 36), 307], radius=6, fill=(241, 245, 249), outline=(226, 232, 240), width=1)
        draw.text((px + 18, 283), s_title, font=get_font(13.5, 'bold'), fill=(15, 23, 42))
        
        # Phone Chassis Frame (CAD Lo-Fi Blueprint Style)
        draw.rounded_rectangle([px, py, px + pw, py + ph], radius=24, fill=(255, 255, 255), outline=(15, 23, 42), width=2)
        
        # Phone Status Bar
        draw.rounded_rectangle([px + (pw - 60) // 2, py + 10, px + (pw + 60) // 2, py + 22], radius=6, fill=(15, 23, 42))
        draw.text((px + 18, py + 11), "9:41", font=get_font(10, 'bold'), fill=(15, 23, 42))
        draw.rounded_rectangle([px + pw - 34, py + 13, px + pw - 18, py + 21], radius=2, outline=(15, 23, 42), width=1)
        draw.line([(px + pw - 18, py + 15), (px + pw - 18, py + 19)], fill=(15, 23, 42), width=1)
        
        # Internal Wireframe Components based on screen
        if "홈 대시보드" in s_title:
            # App Bar
            draw.text((px + 18, py + 34), "Smart DCA", font=get_font(13, 'bold'), fill=(15, 23, 42))
            draw.ellipse([px + pw - 42, py + 36, px + pw - 30, py + 48], outline=(100, 116, 139), width=1)
            draw.text((px + pw - 38, py + 36), "?", font=get_font(10, 'bold'), fill=(100, 116, 139))
            draw.ellipse([px + pw - 24, py + 36, px + pw - 12, py + 48], outline=(100, 116, 139), width=1)
            
            # VIP Status Banner (Clean Text Badge without emoji)
            draw.rounded_rectangle([px + 14, py + 60, px + pw - 14, py + 94], radius=6, fill=(255, 251, 235), outline=(245, 158, 11), width=1)
            draw.rounded_rectangle([px + 22, py + 67, px + 74, py + 87], radius=3, fill=(245, 158, 11))
            draw.text((px + 28, py + 71), "VIP 24h", font=get_font(9, 'bold'), fill=(255, 255, 255))
            draw.text((px + 82, py + 71), "무광고 활성 (18:24)", font=get_font(10, 'bold'), fill=(180, 83, 9))
            draw.rounded_rectangle([px + pw - 56, py + 66, px + pw - 20, py + 88], radius=4, fill=(245, 158, 11))
            draw.text((px + pw - 48, py + 71), "연장", font=get_font(9.5, 'bold'), fill=(255, 255, 255))
            
            # Hero Total Asset Card
            draw.rounded_rectangle([px + 14, py + 104, px + pw - 14, py + 186], radius=10, fill=(248, 250, 252), outline=(203, 213, 225), width=1)
            draw.text((px + 24, py + 114), "총 투자금액 (Total Assets)", font=get_font(10.5, 'regular'), fill=(100, 116, 139))
            draw.text((px + 24, py + 132), "₩ 3,082,500", font=get_num_font(19, 'black'), fill=(15, 23, 42))
            draw.rounded_rectangle([px + 24, py + 160, px + 76, py + 178], radius=4, fill=(220, 252, 231))
            draw.text((px + 32, py + 163), "+0.0%", font=get_font(9.5, 'bold'), fill=(21, 128, 61))
            draw.rounded_rectangle([px + pw - 78, py + 156, px + pw - 22, py + 180], radius=4, fill=(0, 87, 255))
            draw.text((px + pw - 70, py + 160), "계산하기 >", font=get_font(9.5, 'bold'), fill=(255, 255, 255))
            
            # AI Voice Dock
            draw.rounded_rectangle([px + 14, py + 196, px + pw - 14, py + 288], radius=10, fill=(245, 243, 255), outline=(122, 34, 255), width=1)
            draw.ellipse([px + 24, py + 208, px + 48, py + 232], fill=(122, 34, 255))
            draw.text((px + 31, py + 212), "🎙", font=get_font(12, 'bold'), fill=(255, 255, 255))
            draw.text((px + 56, py + 214), "AI 음성 비서 (0.2s 파싱)", font=get_font(11, 'bold'), fill=(15, 23, 42))
            
            # Waveform Bars Wireframe
            wave_x = px + 24
            wave_heights = [6, 12, 18, 14, 22, 16, 10, 20, 15, 8, 14, 18, 10]
            for wh in wave_heights:
                draw.line([(wave_x, py + 252 - wh // 2), (wave_x, py + 252 + wh // 2)], fill=(122, 34, 255), width=2)
                wave_x += 7
            draw.text((px + 120, py + 244), "\"7만원에 50주\"", font=get_font(10, 'regular'), fill=(109, 40, 217))
            
            # Preset Chips
            chips = ["+5%", "+10%", "-20%", "초기화"]
            cx_pos = px + 22
            for ch in chips:
                cw = int(draw.textlength(ch, font=get_font(9, 'bold')) + 14)
                draw.rounded_rectangle([cx_pos, py + 266, cx_pos + cw, py + 282], radius=4, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
                draw.text((cx_pos + 7, py + 268), ch, font=get_font(9, 'bold'), fill=(71, 85, 105))
                cx_pos += cw + 6
                
            # Asset Item Card
            draw.rounded_rectangle([px + 14, py + 298, px + pw - 14, py + 380], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
            draw.rounded_rectangle([px + 24, py + 308, px + 52, py + 336], radius=6, fill=(241, 245, 249))
            draw.text((px + 30, py + 314), "삼", font=get_font(11, 'bold'), fill=(0, 87, 255))
            draw.text((px + 60, py + 310), "삼성전자 (005930)", font=get_font(11, 'bold'), fill=(15, 23, 42))
            draw.text((px + 60, py + 326), "100주 · 평단 ₩75,000", font=get_font(10, 'regular'), fill=(100, 116, 139))
            draw.rounded_rectangle([px + 24, py + 350, px + pw - 24, py + 356], radius=3, fill=(241, 245, 249))
            draw.rounded_rectangle([px + 24, py + 350, px + 170, py + 356], radius=3, fill=(0, 87, 255))
            draw.text((px + 24, py + 362), "비중 65% (포트폴리오 중심 자산)", font=get_font(9.5, 'regular'), fill=(100, 116, 139))
            
            # Bottom Action Dock
            draw.rounded_rectangle([px + 14, py + 490, px + pw - 14, py + 528], radius=8, fill=(0, 87, 255))
            draw.text((px + 62, py + 501), "⚡ 물타기 시뮬레이터 진입", font=get_font(11, 'bold'), fill=(255, 255, 255))
            
        elif "시뮬레이터" in s_title:
            # App Bar
            draw.text((px + 18, py + 34), "< 물타기 시뮬레이터", font=get_font(12, 'bold'), fill=(15, 23, 42))
            draw.text((px + pw - 48, py + 35), "↺ 초기화", font=get_font(10, 'bold'), fill=(220, 38, 38))
            
            # 3-Tab Segmented Control
            draw.rounded_rectangle([px + 14, py + 58, px + pw - 14, py + 88], radius=6, fill=(241, 245, 249))
            draw.rounded_rectangle([px + 16, py + 60, px + 98, py + 86], radius=5, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
            draw.text((px + 34, py + 67), "단일 계산", font=get_font(10, 'bold'), fill=(0, 87, 255))
            draw.text((px + 115, py + 67), "시나리오 A/B", font=get_font(10, 'regular'), fill=(100, 116, 139))
            draw.text((px + 208, py + 67), "목표 역산", font=get_font(10, 'regular'), fill=(100, 116, 139))
            
            # Current Position Card
            draw.rounded_rectangle([px + 14, py + 98, px + pw - 14, py + 186], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
            draw.text((px + 24, py + 106), "1. 현재 보유 평단가 및 수량", font=get_font(11, 'bold'), fill=(15, 23, 42))
            
            # Input Field 1
            draw.rounded_rectangle([px + 24, py + 124, px + pw - 24, py + 150], radius=5, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
            draw.text((px + 32, py + 130), "보유 평단 : 78,000 원", font=get_font(10, 'bold'), fill=(15, 23, 42))
            draw.text((px + pw - 58, py + 130), "[-]  [+]", font=get_font(10, 'bold'), fill=(0, 87, 255))
            
            # Input Field 2
            draw.rounded_rectangle([px + 24, py + 156, px + pw - 24, py + 182], radius=5, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
            draw.text((px + 32, py + 162), "보유 수량 : 100 주", font=get_font(10, 'bold'), fill=(15, 23, 42))
            draw.text((px + pw - 58, py + 162), "[-]  [+]", font=get_font(10, 'bold'), fill=(0, 87, 255))
            
            # Additional Purchase Rows
            draw.rounded_rectangle([px + 14, py + 196, px + pw - 14, py + 288], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
            draw.text((px + 24, py + 204), "2. 차수별 추가 매수 계획", font=get_font(11, 'bold'), fill=(15, 23, 42))
            
            draw.rounded_rectangle([px + 24, py + 222, px + pw - 24, py + 252], radius=5, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
            draw.text((px + 32, py + 230), "1차 추가 매수: 68,000원 · 50주", font=get_font(10, 'regular'), fill=(15, 23, 42))
            
            draw.rounded_rectangle([px + 24, py + 258, px + pw - 24, py + 280], radius=5, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
            draw.text((px + 85, py + 263), "+ 2차 추가 매수 생성", font=get_font(10, 'bold'), fill=(0, 87, 255))
            
            # Realtime Result Card (Highlighted)
            draw.rounded_rectangle([px + 14, py + 298, px + pw - 14, py + 410], radius=10, fill=(240, 246, 255), outline=(0, 87, 255), width=1)
            draw.text((px + 24, py + 308), "3. 실시간 연산 결과 피드백", font=get_font(11, 'bold'), fill=(0, 87, 255))
            draw.text((px + 24, py + 328), "신규 평단가 : ₩ 74,666", font=get_num_font(15, 'black'), fill=(15, 23, 42))
            draw.text((px + 24, py + 352), "• 평단 인하폭 : -4.3% (₩ 3,334 하향)\n• 총 보유 수량 : 150 주\n• 추가 투입 자금 : ₩ 3,400,000", font=get_font(10, 'regular'), fill=(51, 65, 85), spacing=2)
            draw.rounded_rectangle([px + 24, py + 388, px + pw - 24, py + 404], radius=4, fill=(219, 234, 254))
            draw.text((px + 32, py + 391), "✓ 목표 예수금 범위 내 안정적 분할", font=get_font(9, 'bold'), fill=(29, 78, 216))
            
            # Bottom Action CTA
            draw.rounded_rectangle([px + 14, py + 490, px + pw - 14, py + 528], radius=8, fill=(0, 87, 255))
            draw.text((px + 72, py + 501), "💾 시나리오 로컬 DB 저장", font=get_font(11, 'bold'), fill=(255, 255, 255))
            
        elif "목표 역산" in s_title:
            # App Bar
            draw.text((px + 18, py + 34), "< 목표 평단가 역산 엔진", font=get_font(12, 'bold'), fill=(15, 23, 42))
            draw.ellipse([px + pw - 24, py + 36, px + pw - 12, py + 48], outline=(100, 116, 139), width=1)
            draw.text((px + pw - 20, py + 36), "i", font=get_font(10, 'bold'), fill=(100, 116, 139))
            
            # Fixed Context Card
            draw.rounded_rectangle([px + 14, py + 58, px + pw - 14, py + 120], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
            draw.text((px + 24, py + 66), "🔒 현재 고정 컨텍스트 (Locked)", font=get_font(10.5, 'bold'), fill=(100, 116, 139))
            draw.text((px + 24, py + 84), "현재 평단 ₩78,000  ·  보유 100주", font=get_font(11, 'bold'), fill=(15, 23, 42))
            draw.text((px + 24, py + 102), "현재가 (추가 매수가) : ₩ 65,000", font=get_font(9.5, 'regular'), fill=(71, 85, 105))
            
            # Goal Target Price Input
            draw.rounded_rectangle([px + 14, py + 130, px + pw - 14, py + 214], radius=10, fill=(255, 255, 255), outline=(0, 87, 255), width=1)
            draw.text((px + 24, py + 138), "희망 목표 평단가 입력", font=get_font(11, 'bold'), fill=(0, 87, 255))
            
            draw.rounded_rectangle([px + 24, py + 158, px + pw - 24, py + 188], radius=6, fill=(240, 246, 255), outline=(186, 215, 255), width=1)
            draw.text((px + 32, py + 165), "₩ 70,000 원", font=get_num_font(14, 'black'), fill=(0, 87, 255))
            draw.text((px + pw - 58, py + 165), "[-]  [+]", font=get_font(10, 'bold'), fill=(0, 87, 255))
            
            # Boundary Defense Chip
            draw.rounded_rectangle([px + 24, py + 194, px + pw - 24, py + 208], radius=3, fill=(220, 252, 231))
            draw.text((px + 30, py + 196), "✓ 유효: 65,000원 < 목표 70,000원 < 78,000원", font=get_font(8.5, 'bold'), fill=(21, 128, 61))
            
            # Interactive Cash Constraint Slider
            draw.rounded_rectangle([px + 14, py + 224, px + pw - 14, py + 296], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
            draw.text((px + 24, py + 232), "가용 예수금 인터랙티브 슬라이더", font=get_font(10.5, 'bold'), fill=(15, 23, 42))
            
            # Slider Track
            draw.rounded_rectangle([px + 24, py + 258, px + pw - 24, py + 264], radius=3, fill=(226, 232, 240))
            draw.rounded_rectangle([px + 24, py + 258, px + 160, py + 264], radius=3, fill=(16, 185, 129))
            draw.ellipse([px + 154, py + 255, px + 166, py + 267], fill=(16, 185, 129), outline=(255, 255, 255), width=2)
            draw.text((px + 24, py + 274), "한도: ₩ 2,500,000 (도달 가능 최선 평단)", font=get_font(9.5, 'regular'), fill=(71, 85, 105))
            
            # Closed-Form Output Card
            draw.rounded_rectangle([px + 14, py + 306, px + pw - 14, py + 410], radius=10, fill=(255, 251, 235), outline=(245, 158, 11), width=1)
            draw.text((px + 24, py + 316), "수학적 목표 도달 수량 산출", font=get_font(10.5, 'bold'), fill=(180, 83, 9))
            draw.text((px + 24, py + 336), "+42.5 주 추가 매수", font=get_num_font(17, 'black'), fill=(15, 23, 42))
            draw.text((px + 24, py + 364), "• 공식: Q_add = Q_0(P_0-Pt)/(Pt-Pa)\n• 필요 총 예수금 : ₩ 2,125,000\n• 연산 소요 시간 : 0.001초", font=get_font(9.5, 'regular'), fill=(71, 85, 105), spacing=2)
            
            # Bottom Action CTA
            draw.rounded_rectangle([px + 14, py + 490, px + pw - 14, py + 528], radius=8, fill=(16, 185, 129))
            draw.text((px + 52, py + 501), "✓ 시뮬레이터로 1초 자동 주입", font=get_font(11, 'bold'), fill=(255, 255, 255))
            
        # Home Bar Indicator
        draw.rounded_rectangle([px + (pw - 80) // 2, py + ph - 14, px + (pw + 80) // 2, py + ph - 10], radius=2, fill=(15, 23, 42))
        
        # 4 Rationales Beside Phone
        ry = py + 10
        for r_num_title, r_desc in rationales:
            draw.rounded_rectangle([cx, ry, cx + 225, ry + 125], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
            draw.rounded_rectangle([cx, ry + 14, cx + 4, ry + 111], radius=2, fill=(0, 87, 255))
            draw.text((cx + 16, ry + 16), r_num_title, font=get_font(13.5, 'bold'), fill=(15, 23, 42))
            
            lines = wrap_text_by_words(r_desc, get_font(11.5, 'regular'), 190, draw)
            ly = ry + 42
            for line in lines[:3]:
                draw.text((cx + 16, ly), line, font=get_font(11.5, 'regular'), fill=(71, 85, 105))
                ly += 20
                
            ry += 145
            
    # Bottom Architecture Spec Bar
    by = 905
    bh = 55
    draw.rounded_rectangle([120, by, 1800, by + bh], radius=10, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
    draw.rounded_rectangle([135, by + 12, 275, by + 42], radius=5, fill=(15, 23, 42))
    draw.text((147, by + 18), "CAD BLUEPRINT SPEC", font=get_font(10.5, 'bold'), fill=(255, 255, 255))
    draw.text((295, by + 18), "• 8pt 그리드 시스템 및 Material/HIG 48dp 터치 타깃 준수   • Fitts' Law 기반 Thumb-Zone 최적화   • 인지 부하 0% 모바일 퀀트 아키텍처", font=get_font(12.5, 'semibold'), fill=(51, 65, 85))

    base.save(f'{OUT_DIR}/slide_06.png')
    print("SAVED slide_06.png (3 Real Mobile Wireframe CAD Blueprints)")


# SLIDE 07: Enterprise Design System & Token Naming Architecture
# ==============================================================
def make_slide_07():
    base = Image.new('RGBA', (W, H), (9, 13, 22, 255))
    draw = ImageDraw.Draw(base)
    
    # Hairline Grid Accents
    draw.line([(120, 100), (1800, 100)], fill=(255, 255, 255, 20), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(255, 255, 255, 20), width=1)
    
    # Header
    draw.text((120, 130), "06  /  DESIGN SYSTEM FOUNDATIONS & TOKEN ARCHITECTURE", font=get_font(13, 'bold'), fill=(0, 210, 255))
    draw.text((120, 165), "디자인 시스템 파운데이션 및 토큰 네이밍 규격", font=get_font(52, 'black'), fill=(255, 255, 255))
    draw.text((120, 240), "W3C Design Token Community Group (DTCG) 표준, 시맨틱 네이밍 규칙, WCAG 2.1 AAA 고대비 및 Tabular Numbers 체계", font=get_font(18, 'regular'), fill=(148, 163, 184))
    
    # 3 Structured Technical Panels
    col_w = 535
    col_gap = 37
    p1_x = 120
    p2_x = p1_x + col_w + col_gap
    p3_x = p2_x + col_w + col_gap
    
    # =========================================================
    # PANEL 1: Token Architecture & DTCG Naming Rules (Left)
    # =========================================================
    draw.rounded_rectangle([p1_x, 280, p1_x + col_w, 940], radius=16, fill=(16, 22, 34), outline=(255, 255, 255, 20), width=1)
    draw.text((p1_x + 28, 304), "Token Taxonomy & Naming Conventions", font=get_font(18, 'bold'), fill=(255, 255, 255))
    draw.text((p1_x + 28, 330), "W3C DTCG 표준 기반 3계층 (3-Tier) 토큰 체계", font=get_font(13, 'regular'), fill=(148, 163, 184))
    
    # Syntax Code Box
    draw.rounded_rectangle([p1_x + 24, 358, p1_x + col_w - 24, 424], radius=8, fill=(9, 13, 22), outline=(0, 210, 255, 60), width=1)
    draw.text((p1_x + 36, 368), "TOKEN SYNTAX SPECIFICATION", font=get_font(10, 'bold'), fill=(0, 210, 255))
    draw.text((p1_x + 36, 388), "$[Scope] . [Category] . [Concept] . [Property] . [State]", font=get_num_font(13.5, 'bold'), fill=(255, 255, 255))
    
    # Tier 1 Card
    draw.rounded_rectangle([p1_x + 24, 436, p1_x + col_w - 24, 536], radius=10, fill=(9, 13, 22), outline=(255, 255, 255, 15), width=1)
    draw.rounded_rectangle([p1_x + 36, 448, p1_x + 96, 470], radius=4, fill=(0, 87, 255, 40))
    draw.text((p1_x + 44, 452), "TIER 01", font=get_font(9.5, 'bold'), fill=(0, 210, 255))
    draw.text((p1_x + 106, 450), "Primitive / Global Tokens (원시 토큰)", font=get_font(13, 'bold'), fill=(255, 255, 255))
    draw.text((p1_x + 36, 478), "• palette.blue.600 : #0057FF       • font.family.base : Pretendard\n• space.scale.4 : 4px               • radius.container.lg : 16px", font=get_font(11.5, 'regular'), fill=(148, 163, 184), spacing=3)
    
    # Tier 2 Card
    draw.rounded_rectangle([p1_x + 24, 546, p1_x + col_w - 24, 680], radius=10, fill=(9, 13, 22), outline=(255, 255, 255, 15), width=1)
    draw.rounded_rectangle([p1_x + 36, 558, p1_x + 96, 580], radius=4, fill=(16, 185, 129, 40))
    draw.text((p1_x + 44, 562), "TIER 02", font=get_font(9.5, 'bold'), fill=(52, 211, 153))
    draw.text((p1_x + 106, 560), "System / Semantic Tokens (의미론적 토큰)", font=get_font(13, 'bold'), fill=(255, 255, 255))
    draw.text((p1_x + 36, 588), "• $sys.color.brand.primary : #0057FF (메인 액션 / CTA 버튼)\n• $sys.color.status.gain : #00E676 (수익률 / 안전 진단)\n• $sys.color.status.loss : #FF5252 (하락률 / 경계 방어 에러)\n• $sys.color.surface.dark : #05070B (OLED 칠흑 21:1 암흑 표면)", font=get_font(11.5, 'regular'), fill=(148, 163, 184), spacing=4)
    
    # Tier 3 Card
    draw.rounded_rectangle([p1_x + 24, 690, p1_x + col_w - 24, 795], radius=10, fill=(9, 13, 22), outline=(255, 255, 255, 15), width=1)
    draw.rounded_rectangle([p1_x + 36, 702, p1_x + 96, 724], radius=4, fill=(245, 158, 11, 40))
    draw.text((p1_x + 44, 706), "TIER 03", font=get_font(9.5, 'bold'), fill=(251, 191, 36))
    draw.text((p1_x + 106, 704), "Component Tokens (컴포넌트 토큰)", font=get_font(13, 'bold'), fill=(255, 255, 255))
    draw.text((p1_x + 36, 732), "• $comp.btn.primary.bg.default : $sys.color.brand.primary\n• $comp.btn.primary.bg.pressed : #0040CC\n• $comp.card.container.radius : $sys.radius.container.lg", font=get_font(11.5, 'regular'), fill=(148, 163, 184), spacing=3)
    
    # Single Source of Truth Callout
    draw.rounded_rectangle([p1_x + 24, 805, p1_x + col_w - 24, 915], radius=10, fill=(9, 13, 22), outline=(0, 87, 255, 50), width=1)
    draw.text((p1_x + 36, 818), "단일 진실 공급원 (Single Source of Truth)", font=get_font(12.5, 'bold'), fill=(0, 210, 255))
    draw.text((p1_x + 36, 842), "Figma Tokens 플러그인과 Flutter `.dart` 디자인 토큰 클래스를\nJSON으로 100% 자동 동기화하여 디자인-엔지니어링 간\n커뮤니케이션 오차 및 디자인 드리프트(Drift)를 원천 차단", font=get_font(11.5, 'regular'), fill=(148, 163, 184), spacing=4)
    
    # =========================================================
    # PANEL 2: Semantic Color Tokens & WCAG 2.1 AAA (Center)
    # =========================================================
    draw.rounded_rectangle([p2_x, 280, p2_x + col_w, 940], radius=16, fill=(16, 22, 34), outline=(255, 255, 255, 20), width=1)
    draw.text((p2_x + 28, 304), "Semantic Palette & WCAG 2.1 AAA Contrast", font=get_font(18, 'bold'), fill=(255, 255, 255))
    draw.text((p2_x + 28, 330), "야간 장세 시인성 극대화를 위한 초고대비 토큰 매핑", font=get_font(13, 'regular'), fill=(148, 163, 184))
    
    color_tokens = [
        ("sys.color.brand.primary", "#0057FF", "Brand Primary CTA · Active Tab", (0, 87, 255), "7.4:1 AAA"),
        ("sys.color.status.gain", "#00E676", "Profit Yield · Safe State Health", (0, 230, 118), "8.2:1 AAA"),
        ("sys.color.status.loss", "#FF5252", "Loss Rate · Boundary Error Guard", (255, 82, 82), "7.1:1 AAA"),
        ("sys.color.status.vip", "#FFB300", "24h VIP Ad-Free Token", (255, 179, 0), "7.8:1 AAA"),
        ("sys.color.accent.voice", "#7A22FF", "AI Multimodal STT Waveform", (122, 34, 255), "6.5:1 AA+"),
        ("sys.color.accent.quant", "#00D2FF", "Goal Seeking Algorithm Core", (0, 210, 255), "8.9:1 AAA"),
        ("sys.color.surface.canvas", "#05070B", "Pitch Black OLED Background", (5, 7, 11), "21:1 AAA"),
        ("sys.color.surface.card", "#101622", "Elevated Card Container Surface", (16, 22, 34), "18:1 AAA")
    ]
    
    cy = 358
    for tname, chex, crole, crgb, ccontrast in color_tokens:
        draw.rounded_rectangle([p2_x + 24, cy, p2_x + col_w - 24, cy + 58], radius=8, fill=(9, 13, 22), outline=(255, 255, 255, 12), width=1)
        
        # Swatch Box
        draw.rounded_rectangle([p2_x + 34, cy + 11, p2_x + 70, cy + 47], radius=6, fill=crgb, outline=(255, 255, 255, 40), width=1)
        
        # Token Name & Role
        draw.text((p2_x + 82, cy + 10), tname, font=get_font(12, 'bold'), fill=(255, 255, 255))
        draw.text((p2_x + 82, cy + 32), f"{chex}  ·  {crole}", font=get_font(10.5, 'regular'), fill=(148, 163, 184))
        
        # Contrast Pill
        draw.rounded_rectangle([p2_x + col_w - 105, cy + 16, p2_x + col_w - 34, cy + 42], radius=4, fill=(16, 185, 129, 25), outline=(16, 185, 129, 70), width=1)
        draw.text((p2_x + col_w - 97, cy + 21), ccontrast, font=get_font(9.5, 'bold'), fill=(52, 211, 153))
        
        cy += 64
        
    # WCAG Banner
    draw.rounded_rectangle([p2_x + 24, 876, p2_x + col_w - 24, 916], radius=8, fill=(16, 185, 129, 20), outline=(16, 185, 129, 80), width=1)
    draw.text((p2_x + 40, 886), "✓ 국제 웹 접근성 가이드라인 WCAG 2.1 AAA 7:1 명도 대비 100% 충족", font=get_font(11.5, 'bold'), fill=(52, 211, 153))
    
    # =========================================================
    # PANEL 3: Typography Hierarchy, Layout & Spacing (Right)
    # =========================================================
    draw.rounded_rectangle([p3_x, 280, p3_x + col_w, 940], radius=16, fill=(16, 22, 34), outline=(255, 255, 255, 20), width=1)
    draw.text((p3_x + 28, 304), "Typography Hierarchy, Layout & Spacing", font=get_font(18, 'bold'), fill=(255, 255, 255))
    draw.text((p3_x + 28, 330), "숫자 흔들림 방지 Tabular Numbers & 4px/8px 그리드", font=get_font(13, 'regular'), fill=(148, 163, 184))
    
    typos = [
        ("sys.font.display.hero", "₩ 3,082,500", "32pt / Black / tnum (총 자산 및 평단)"),
        ("sys.font.headline.bold", "+42.5주 추가 매수", "24pt / Bold / tnum (역산 산출 결과)"),
        ("sys.font.title.medium", "호가 급락 시 원터치 분할 매수", "18pt / Bold (섹션 헤더 및 주요 카드)"),
        ("sys.font.body.regular", "실시간 가중평균 연산 엔진 가이드", "14pt / Regular (본문 설명 및 툴팁)")
    ]
    
    ty = 358
    for t_token, t_sample, t_desc in typos:
        draw.rounded_rectangle([p3_x + 24, ty, p3_x + col_w - 24, ty + 70], radius=8, fill=(9, 13, 22), outline=(255, 255, 255, 12), width=1)
        draw.text((p3_x + 36, ty + 12), t_token, font=get_font(12, 'bold'), fill=(0, 210, 255))
        draw.text((p3_x + 230, ty + 10), t_sample, font=get_font(14, 'bold'), fill=(255, 255, 255))
        draw.text((p3_x + 36, ty + 40), t_desc, font=get_font(11, 'regular'), fill=(148, 163, 184))
        ty += 77
        
    # Tabular Numbers Feature Callout Box
    draw.rounded_rectangle([p3_x + 24, 675, p3_x + col_w - 24, 785], radius=10, fill=(9, 13, 22), outline=(0, 210, 255, 70), width=1)
    draw.text((p3_x + 36, 688), "TABULAR NUMBERS SPECIFICATION (tnum)", font=get_font(11, 'bold'), fill=(0, 210, 255))
    draw.text((p3_x + 36, 712), "실시간 호가 및 자산 금액 변동 시 글자 폭 변화로 인한\n레이아웃 지터(Jitter)를 방지하기 위해 OpenType `tnum` 속성을\n전역 강제 적용하여 금융 데이터 가독성과 신뢰도 100% 보장", font=get_font(11.5, 'regular'), fill=(148, 163, 184), spacing=4)
    
    # Atomic Spacing & Radius & Elevation
    draw.rounded_rectangle([p3_x + 24, 795, p3_x + col_w - 24, 918], radius=10, fill=(9, 13, 22), outline=(255, 255, 255, 15), width=1)
    draw.text((p3_x + 36, 808), "Atomic Spacing · Corner Radius · Elevation Tokens", font=get_font(12, 'bold'), fill=(255, 255, 255))
    
    tokens_sub = [
        ("Spacing Grid", "space.xs (4px) · space.sm (8px) · space.md (16px) · space.lg (24px)"),
        ("Corner Radius", "radius.xs (4px) · radius.sm (8px) · radius.md (16px) · radius.full (999px)"),
        ("Elevation Shadow", "elevation.0 (Flat) · elevation.1 (Card: 0 4px 12px) · elevation.2 (Modal: 0 12px 28px)")
    ]
    tsy = 832
    for s_name, s_val in tokens_sub:
        draw.text((p3_x + 36, tsy), f"• {s_name} : ", font=get_font(10.5, 'bold'), fill=(0, 210, 255))
        draw.text((p3_x + 140, tsy), s_val, font=get_font(10.5, 'regular'), fill=(148, 163, 184))
        tsy += 25

    base.save(f'{OUT_DIR}/slide_07.png')
    print("SAVED slide_07.png (Enterprise Design System with DTCG Tokens)")


# ==============================================================
# SLIDE 08: Feature Spotlight 01 - 0.2s STT (Stealth Hardware Reveal)
# ==============================================================
def make_slide_08():
    base = Image.new('RGBA', (W, H), (9, 13, 22, 255))
    
    # Ambient Lighting
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([650, 200, 1350, 900], fill=(0, 87, 255, 45))
    glow = glow.filter(ImageFilter.GaussianBlur(130))
    base = Image.alpha_composite(base, glow)
    draw = ImageDraw.Draw(base)
    
    # Hairline Boundaries
    draw.line([(120, 100), (1800, 100)], fill=(255, 255, 255, 20), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(255, 255, 255, 20), width=1)
    
    # Left Header
    draw.text((120, 130), "07  /  FEATURE SPOTLIGHT 01 · ON-DEVICE MULTIMODAL INGESTION", font=get_font(13, 'bold'), fill=(0, 210, 255))
    draw.text((120, 168), "0.2s 하이브리드 음성\n인제스천 파이프라인", font=get_font(44, 'black'), fill=(255, 255, 255), spacing=8)
    draw.text((120, 275), "Google STT 온디바이스 엔진과 정규식 AST 토크나이저 결합\n'종목명+단가+수량' 복합 자연어 발화를 0.2초 내 분류 및 타입 캐스팅", font=get_font(15, 'regular'), fill=(148, 163, 184), spacing=5)
    
    # Left 3 Cards: x=120..710, y=365..875
    cards_l = [
        ("자연어 음성 파형 감지 & AST 파싱", "\"삼성전자 7만 원에 50주\"\n발화 즉시 0.2초 내 토큰 분리 및 정규화"),
        ("키패드 타이핑 레이턴시 98.2% 제거", "소수점 단가 8자리 입력 시간을 240초에서 4.2초로 단축하여\n매수 골든타임 슬리피지(Slip Risk) 방어"),
        ("Local-First 0ms ACID 영속화", "Hive NoSQL 인메모리 캐싱으로 오프라인 환경에서도\n시뮬레이터 코어로 파라미터 즉각 주입")
    ]
    ly = 365
    for title, desc in cards_l:
        draw.rounded_rectangle([120, ly, 710, ly + 155], radius=14, fill=(16, 22, 34, 230), outline=(255, 255, 255, 20), width=1)
        draw.rounded_rectangle([120, ly + 16, 124, ly + 139], radius=2, fill=(0, 114, 255))
        draw.text((148, ly + 22), title, font=get_font(17, 'bold'), fill=(255, 255, 255))
        draw.text((148, ly + 62), desc, font=get_font(13.5, 'regular'), fill=(148, 163, 184), spacing=4)
        ly += 180
        
    # Center Phone Mockup (Sleek Samsung Galaxy S24 Ultra Frame)
    phone = Image.open('portfolio/galaxy_mockups/galaxy_08_voice.png').convert('RGBA')
    pw = 330
    ph = int(round(phone.height * (pw / phone.width)))
    phone = phone.resize((pw, ph), Image.Resampling.LANCZOS)
    
    # Realistic Shadow underneath Phone
    px = 795
    py = 205
    sh = Image.new('RGBA', (W, H), (0,0,0,0))
    shd = ImageDraw.Draw(sh)
    shd.ellipse([px, py + ph - 20, px + pw, py + ph + 35], fill=(0, 0, 0, 240))
    sh = sh.filter(ImageFilter.GaussianBlur(28))
    base = Image.alpha_composite(base, sh)
    base.paste(phone, (px, py), phone)
    
    draw = ImageDraw.Draw(base)
    
    # Right Column Cards: x=1210..1800, ry=145..880
    cards_r = [
        ("0-딜레이 오프라인 호가 프리셋", "STT 권한 거부 또는 소음 환경 시\n±5%, ±10% 원터치 프리셋 칩 즉시 대체 주입", (0, 210, 255)),
        ("실시간 음성 토큰 정규화 엔진", "한국어 수치 어휘(일, 십, 백, 천, 만)를\n아라비아 정수 및 실수로 무손실 AST 변환", (0, 230, 118)),
        ("급락장 호가 오차 차단 가드", "종목 매핑과 단가·수량 경계 조건을 검증하여\n비정상 수치(음수, 비현실 호가) 원천 차단", (255, 179, 0)),
        ("60fps 실시간 음성 파형 텔레메트리", "마이크 인풋 시 실시간 Waveform 렌더링으로\n사용자에게 즉각적인 오디오 스트림 피드백 제공", (147, 51, 234))
    ]
    ry = 145
    for title, desc, col in cards_r:
        draw.rounded_rectangle([1210, ry, 1800, ry + 160], radius=14, fill=(16, 22, 34, 230), outline=(255, 255, 255, 20), width=1)
        draw.rounded_rectangle([1210, ry + 16, 1214, ry + 144], radius=2, fill=col)
        draw.text((1240, ry + 22), title, font=get_font(17, 'bold'), fill=(255, 255, 255))
        draw.text((1240, ry + 62), desc, font=get_font(13.5, 'regular'), fill=(148, 163, 184), spacing=4)
        ry += 190
        
    base.save(f'{OUT_DIR}/slide_08.png')
    print("SAVED slide_08.png")

# ==============================================================
# SLIDE 09: Feature Spotlight 02 - Goal-Seeking Math (Wall Street Quant)
# ==============================================================
def make_slide_09():
    base = Image.new('RGBA', (W, H), (9, 13, 22, 255))
    
    # Ambient Lighting
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([1100, 150, 1850, 950], fill=(0, 114, 255, 50))
    gw.ellipse([300, 300, 900, 900], fill=(0, 210, 255, 18))
    glow = glow.filter(ImageFilter.GaussianBlur(140))
    base = Image.alpha_composite(base, glow)
    draw = ImageDraw.Draw(base)
    
    # Hairline Boundaries
    draw.line([(120, 100), (1800, 100)], fill=(255, 255, 255, 20), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(255, 255, 255, 20), width=1)
    
    # Header
    draw.text((120, 130), "08  /  FEATURE SPOTLIGHT 02 · QUANTITATIVE ALGORITHM", font=get_font(13, 'bold'), fill=(0, 210, 255))
    draw.text((120, 165), "Goal Seeking 폐쇄형 목표 평단가 역산 엔진", font=get_font(46, 'black'), fill=(255, 255, 255))
    draw.text((120, 235), "목표 탈출가 도달에 필요한 추가 매수 수량을 Closed-Form 수식으로 0.001초 만에 산출", font=get_font(17, 'regular'), fill=(148, 163, 184))
    
    # Left: Mathematical Formulation & Algorithm Spec (x=120..1180)
    # Formula Card: y=285..465
    draw.rounded_rectangle([120, 285, 1180, 465], radius=16, fill=(16, 22, 34, 240), outline=(0, 210, 255, 70), width=1)
    draw.rounded_rectangle([150, 305, 305, 331], radius=4, fill=(0, 210, 255, 30))
    draw.text((160, 310), "MATHEMATICAL FORMULA", font=get_font(10.5, 'bold'), fill=(0, 210, 255))
    
    # Closed Form Formula
    draw.text((150, 350), "Q_add  =  Q_0  ×  ( P_0 - P_target )  /  ( P_target - P_add )", font=get_num_font(23, 'bold'), fill=(255, 255, 255))
    draw.text((150, 402), "• Q_0: 현재 보유 수량 (100주)        • P_0: 현재 평균 단가 (₩78,000)\n• P_target: 희망 목표 평단 (₩70,000)   • P_add: 추가 매수 희망가 / 현재가 (₩65,000)", font=get_font(13.5, 'regular'), fill=(148, 163, 184), spacing=6)
    
    # Quant Feature Cards: y=490..875
    quant_cards = [
        ("수학적 경계 불변식 가드 (Boundary Invariant Defense)", "P_add < P_target < P_0 불변식 위반 시 즉시 에러 토스트를 호출하고,\n현재 투입 가능한 현실적 목표 평단가를 역으로 실시간 제안합니다.", (0, 114, 255)),
        ("가용 예수금 인터랙티브 제약 최적화 (Capital Constraint Optimizer)", "예수금이 한정된 투자자를 위해 보유 현금 한도 내에서\n도달 가능한 최선의 방어 평단을 슬라이더로 60fps 즉각 피드백합니다.", (16, 185, 129)),
        ("Zero-Loss 파라미터 인계 파이프라인 (Parameter Handoff)", "수학적으로 산출된 최적 매수 수량과 자금 규모를 1탭으로 시뮬레이터에 즉시 인계하여\n급박한 실시간 장세에서 주문 집행 슬리피지를 원천 차단합니다.", (245, 158, 11))
    ]
    
    qy = 490
    for title, desc, col in quant_cards:
        draw.rounded_rectangle([120, qy, 1180, qy + 115], radius=14, fill=(16, 22, 34, 230), outline=(255, 255, 255, 20), width=1)
        draw.rounded_rectangle([120, qy + 16, 124, qy + 99], radius=2, fill=col)
        draw.text((150, qy + 22), title, font=get_font(17, 'bold'), fill=(255, 255, 255))
        draw.text((150, qy + 58), desc, font=get_font(13.5, 'regular'), fill=(148, 163, 184), spacing=3)
        qy += 135
        
    # Right: Samsung Galaxy S24 Ultra Phone Mockup (x=1360, y=205..870)
    phone = Image.open('portfolio/galaxy_mockups/galaxy_03_target.png').convert('RGBA')
    pw = 330
    ph = int(round(phone.height * (pw / phone.width)))
    phone = phone.resize((pw, ph), Image.Resampling.LANCZOS)
    
    px = 1360
    py = 205
    sh = Image.new('RGBA', (W, H), (0,0,0,0))
    shd = ImageDraw.Draw(sh)
    shd.ellipse([px, py + ph - 20, px + pw, py + ph + 35], fill=(0, 0, 0, 240))
    sh = sh.filter(ImageFilter.GaussianBlur(28))
    base = Image.alpha_composite(base, sh)
    base.paste(phone, (px, py), phone)
    
    # Floating Result Badge Card (Staged gracefully next to phone)
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle([1120, 690, 1560, 845], radius=16, fill=(12, 17, 28, 245), outline=(0, 210, 255, 180), width=2)
    draw.text((1148, 712), "수학적 목표 도달 수량 산출 완료", font=get_font(13.5, 'bold'), fill=(0, 210, 255))
    draw.text((1148, 740), "+42.5주 추가 매수 필요", font=get_num_font(28, 'black'), fill=(255, 255, 255))
    draw.text((1148, 792), "총 투입 필요 예수금 : ₩ 2,125,000 (소요 0.001초)", font=get_font(14, 'regular'), fill=(180, 215, 220))
    
    base.save(f'{OUT_DIR}/slide_09.png')
    print("SAVED slide_09.png")

# ==============================================================
# SLIDE 10: High-Fidelity 6 Screens Showcase (Studio Showcase)
# ==============================================================
def make_slide_10():
    base = Image.new('RGBA', (W, H), (9, 13, 22, 255))
    
    # Ambient Stage Lighting underneath the devices
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([200, 300, 1720, 850], fill=(0, 87, 255, 38))
    gw.ellipse([600, 450, 1320, 800], fill=(0, 210, 255, 25))
    glow = glow.filter(ImageFilter.GaussianBlur(150))
    base = Image.alpha_composite(base, glow)
    draw = ImageDraw.Draw(base)
    
    # Hairline Boundaries
    draw.line([(120, 100), (1800, 100)], fill=(255, 255, 255, 20), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(255, 255, 255, 20), width=1)
    
    # Header
    draw.text((120, 130), "09  /  HIGH-FIDELITY SCREENS & USER FLOW ARCHITECTURE", font=get_font(13, 'bold'), fill=(0, 210, 255))
    draw.text((120, 165), "6개 핵심 모바일 인터페이스 쇼케이스", font=get_font(46, 'black'), fill=(255, 255, 255))
    draw.text((120, 230), "진입(홈) → 시뮬레이션 → 목표 역산 → 리포트 분석 → OLED 야간 다크모드 → 글로벌 설정으로 이어지는 유기적 사용자 흐름", font=get_font(16, 'regular'), fill=(148, 163, 184))
    
    # 6 Screens Specifications
    screens = [
        ('portfolio/galaxy_mockups/galaxy_01_home.png', '01. 홈 대시보드', '자산 텔레메트리 & 음성 도크'),
        ('portfolio/galaxy_mockups/galaxy_02_sim.png', '02. 퀀트 계산기', '가중평균 & A/B 전략 대조'),
        ('portfolio/galaxy_mockups/galaxy_03_target.png', '03. 목표 역산 엔진', '손익분기점(BEP) 폐쇄형 역산'),
        ('portfolio/galaxy_mockups/galaxy_04_report.png', '04. 리스크 감사 리포트', '비중 왜곡 진단 & 3단계 시급도'),
        ('portfolio/galaxy_mockups/galaxy_05_dark_home.png', '05. OLED 다크 테마', '야간 트레이더 WCAG AAA 고대비'),
        ('portfolio/galaxy_mockups/galaxy_06_dark_settings.png', '06. 글로벌 거버넌스', '7개국 L10n & 24h VIP 제어')
    ]
    
    pw = 236
    phone_y = 270
    pgap = 53
    px = 120
    
    # Reference phone height calculation (native ratio preserved)
    ref_phone = Image.open(screens[0][0])
    ph = int(round(pw * (ref_phone.height / ref_phone.width)))
    
    # Stage line
    draw.line([(120, phone_y + ph + 8), (1800, phone_y + ph + 8)], fill=(0, 210, 255, 40), width=1)
    
    for img_path, title, role in screens:
        phone = Image.open(img_path).convert('RGBA')
        cur_ph = int(round(pw * (phone.height / phone.width)))
        phone = phone.resize((pw, cur_ph), Image.Resampling.LANCZOS)
        
        # Soft Drop Shadow directly under phone chin
        sh = Image.new('RGBA', (W, H), (0,0,0,0))
        shd = ImageDraw.Draw(sh)
        shd.ellipse([px - 6, phone_y + cur_ph - 14, px + pw + 6, phone_y + cur_ph + 24], fill=(0, 0, 0, 220))
        sh = sh.filter(ImageFilter.GaussianBlur(16))
        base = Image.alpha_composite(base, sh)
        base.paste(phone, (px, phone_y), phone)
        
        draw = ImageDraw.Draw(base)
        
        # Title Pill Badge
        pill_y = phone_y + cur_ph + 18
        draw.rounded_rectangle([px, pill_y, px + pw, pill_y + 32], radius=8, fill=(16, 22, 34, 240), outline=(255, 255, 255, 25), width=1)
        draw.rounded_rectangle([px, pill_y + 7, px + 3, pill_y + 25], radius=1, fill=(0, 210, 255))
        draw.text((px + 12, pill_y + 8), title, font=get_font(12, 'bold'), fill=(255, 255, 255))
        
        # Role description
        draw.text((px + 12, pill_y + 40), role, font=get_font(11, 'regular'), fill=(148, 163, 184))
        
        px += pw + pgap
        
    # Flow Pipeline Arrows across the bottom (y=875..945)
    draw.rounded_rectangle([120, 875, 1800, 945], radius=12, fill=(16, 22, 34, 220), outline=(255, 255, 255, 20), width=1)
    draw.rounded_rectangle([136, 891, 252, 927], radius=6, fill=(0, 87, 255, 40))
    draw.text((148, 900), "USER PIPELINE", font=get_font(11, 'bold'), fill=(0, 210, 255))
    
    flow_steps = [
        ("01 자산 텔레메트리", 270),
        ("02 멀티모달 인제스천", 520),
        ("03 폐쇄형 역산 도출", 790),
        ("04 리스크 감사 진단", 1050),
        ("05 야간 장세 매매", 1310),
        ("06 글로벌 규격 전환", 1560)
    ]
    for step_txt, sx in flow_steps:
        draw.text((sx, 900), step_txt, font=get_font(12.5, 'bold'), fill=(255, 255, 255))
        if sx < 1500:
            draw.text((sx + 155, 898), "→", font=get_font(16, 'bold'), fill=(0, 210, 255))
            
    base.save(f'{OUT_DIR}/slide_10.png')
    print("SAVED slide_10.png (100% Native Aspect Ratio Preserved)")


# ==============================================================
# SLIDE 11: Core User Flow Interactive Prototype Walkthrough
# ==============================================================
def make_slide_11():
    base = Image.new('RGBA', (W, H), (9, 13, 22, 255))
    
    # Ambient Lighting
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([100, 150, 700, 950], fill=(0, 87, 255, 45))
    gw.ellipse([1000, 200, 1750, 900], fill=(0, 210, 255, 20))
    glow = glow.filter(ImageFilter.GaussianBlur(140))
    base = Image.alpha_composite(base, glow)
    draw = ImageDraw.Draw(base)
    
    # Hairline Boundaries
    draw.line([(120, 100), (1800, 100)], fill=(255, 255, 255, 20), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(255, 255, 255, 20), width=1)
    
    # Left: Galaxy S24 Ultra Phone Mockup (Interactive Simulation)
    phone = Image.open('portfolio/galaxy_mockups/galaxy_03_target.png').convert('RGBA')
    pw = 340
    ph = int(round(phone.height * (pw / phone.width)))
    phone = phone.resize((pw, ph), Image.Resampling.LANCZOS)
    
    px = 160
    py = 185
    sh = Image.new('RGBA', (W, H), (0,0,0,0))
    shd = ImageDraw.Draw(sh)
    shd.ellipse([px, py + ph - 20, px + pw, py + ph + 35], fill=(0, 0, 0, 240))
    sh = sh.filter(ImageFilter.GaussianBlur(28))
    base = Image.alpha_composite(base, sh)
    base.paste(phone, (px, py), phone)
    
    draw = ImageDraw.Draw(base)
    
    # Interactive Touch Hotspot Overlay on Phone (Slider Touch Indicator)
    touch_cx = px + pw // 2 + 35
    touch_cy = py + 485
    draw.ellipse([touch_cx - 28, touch_cy - 28, touch_cx + 28, touch_cy + 28], outline=(0, 210, 255, 120), width=2)
    draw.ellipse([touch_cx - 18, touch_cy - 18, touch_cx + 18, touch_cy + 18], fill=(0, 210, 255, 60), outline=(0, 210, 255, 200), width=2)
    draw.ellipse([touch_cx - 6, touch_cy - 6, touch_cx + 6, touch_cy + 6], fill=(255, 255, 255))
    
    # Hotspot Callout Tag
    draw.rounded_rectangle([px + pw - 20, touch_cy - 16, px + pw + 180, touch_cy + 16], radius=6, fill=(16, 22, 34, 240), outline=(0, 210, 255, 180), width=1)
    draw.text((px + pw - 8, touch_cy - 8), "⌾ 60fps Interactive Slider", font=get_font(11, 'bold'), fill=(0, 210, 255))
    
    # Mathematical Guard Badge above Target input
    draw.rounded_rectangle([px - 40, py + 230, px + pw + 40, py + 266], radius=8, fill=(12, 22, 18, 240), outline=(16, 185, 129, 180), width=1)
    draw.ellipse([px - 26, py + 244, px - 18, py + 252], fill=(16, 185, 129))
    draw.text((px - 10, py + 241), "✓ Invariant Guard: P_add < P_target < P_0 [VALID]", font=get_font(11.5, 'bold'), fill=(52, 211, 153))
    
    # Floating Computed Result Card (Staged at bottom left)
    draw.rounded_rectangle([px - 20, py + ph - 65, px + pw + 80, py + ph + 35], radius=14, fill=(12, 17, 28, 245), outline=(0, 210, 255, 180), width=2)
    draw.text((px, py + ph - 52), "수학적 최적 매수 수량 실시간 산출", font=get_font(12, 'bold'), fill=(0, 210, 255))
    draw.text((px, py + ph - 28), "+42.5주 추가 매수 (₩2,125,000)", font=get_num_font(20, 'black'), fill=(255, 255, 255))
    draw.text((px, py + ph + 6), "방어 평단: ₩70,000  ·  하락률 방어 +11.4%p", font=get_font(12, 'regular'), fill=(148, 163, 184))
    
    # Right Column: 4 Progressive Interactive Scenario Walkthrough
    tx = 680
    draw.text((tx, 130), "10  /  CORE USER FLOW INTERACTIVE PROTOTYPE WALKTHROUGH", font=get_font(13, 'bold'), fill=(0, 210, 255))
    draw.text((tx, 165), "핵심 플로우: 퀀트 역산 & 실시간 슬라이더\n인터랙티브 프로토타입 시나리오", font=get_font(40, 'black'), fill=(255, 255, 255), spacing=8)
    draw.text((tx, 275), "급락장 패닉 셀링을 0.2초 내 이성적 퀀트 집행으로 전환하는 4단계 인터랙티브 사용자 여정 워크스루", font=get_font(16, 'regular'), fill=(148, 163, 184))
    
    steps_data = [
        ("STEP 01", "변동성 위기 감지 & 0.2s 음성 인제스천 (Multimodal Ingestion)",
         "시장 급락(-23%) 직면 시 0.2초 온디바이스 음성 발화(\"삼성전자 7만 원에 50주\") 또는 원터치 프리셋 칩으로\n현재 보유 평단(₩78,000)과 수량(100주)을 키패드 입력 지연 없이 즉각 로드합니다.",
         "• 60fps 오디오 파형 바인딩  • 키패드 타이핑 98.2% 생략  • AST 자동 정규화", (0, 114, 255)),
         
        ("STEP 02", "탈출 목표 평단 설정 & 수학적 불변식 가드 (Boundary Invariant)",
         "손익분기점(BEP) 탈출 희망 평단(₩70,000) 입력 시 P_add < P_target < P_0 경계 조건을 실시간 검증합니다.\n불가능한 목표가 입력 시 에러 토스트를 호출하고 현재 예산으로 달성 가능한 현실적 목표를 역제안합니다.",
         "• 폐쇄형 Closed-Form 검증  • 비정상 입력 원천 차단  • 현실적 목표가 실시간 피드백", (0, 210, 255)),
         
        ("STEP 03", "가용 예수금 인터랙티브 제약 슬라이더 조절 (60fps Interactive Slider)",
         "한정된 현금 자산 내에서 슬라이더를 좌우로 드래그하면, 가용 예수금 한도 내에서 도달 가능한 최적 추가 매수 주수(+42.5주)와\n방어 평단을 60fps로 실시간 피드백합니다. OpenType tnum 속성으로 숫자 지터(Jitter)를 100% 방지합니다.",
         "• 60fps 드래그 햅틱 인터랙션  • Tabular Numbers 숫자 흔들림 방지  • 즉각적 방어율 렌더링", (245, 158, 11)),
         
        ("STEP 04", "1탭 파라미터 인계 & 최적 주문 집행 (One-Tap Zero-Loss Handoff)",
         "수학적으로 산출된 최적 매수 수량과 소요 자금(₩2,125,000)을 1탭으로 시뮬레이터에 즉시 인계하여\n급박한 실시간 장세에서 주문 집행 슬리피지(Slip Risk)를 0% 차단하고 SQLite/Hive에 안전하게 암호화 저장합니다.",
         "• 원터치 제로-로스 인계  • 0ms ACID 로컬 영속화  • 진단 리포트 원클릭 공유", (16, 185, 129))
    ]
    
    sy = 330
    for s_badge, s_title, s_desc, s_micro, s_col in steps_data:
        draw.rounded_rectangle([tx, sy, 1800, sy + 130], radius=14, fill=(16, 22, 34, 230), outline=(255, 255, 255, 20), width=1)
        draw.rounded_rectangle([tx, sy + 14, tx + 4, sy + 116], radius=2, fill=s_col)
        
        # Step Badge
        draw.rounded_rectangle([tx + 20, sy + 14, tx + 88, sy + 38], radius=4, fill=(s_col[0], s_col[1], s_col[2], 40))
        draw.text((tx + 28, sy + 18), s_badge, font=get_font(10, 'bold'), fill=s_col)
        
        # Step Title
        draw.text((tx + 98, sy + 16), s_title, font=get_font(14.5, 'bold'), fill=(255, 255, 255))
        
        # Step Desc
        draw.text((tx + 20, sy + 46), s_desc, font=get_font(12, 'regular'), fill=(148, 163, 184), spacing=3)
        
        # Micro Interaction Pill
        draw.rounded_rectangle([tx + 20, sy + 94, 1780, sy + 118], radius=6, fill=(9, 13, 22), outline=(s_col[0], s_col[1], s_col[2], 60), width=1)
        draw.text((tx + 30, sy + 99), s_micro, font=get_font(10.5, 'bold'), fill=s_col)
        
        sy += 144
        
    # Bottom Prototype Live Test Callout
    draw.rounded_rectangle([tx, 915, 1800, 955], radius=10, fill=(0, 87, 255, 25), outline=(0, 210, 255, 90), width=1)
    draw.text((tx + 20, 925), "💡 LIVE INTERACTIVE PROTOTYPE AVAILABLE ON WEB : 아래 포트폴리오 웹에서 직접 슬라이더를 드래그하여 실시간 수식 연산을 체험할 수 있습니다.", font=get_font(12, 'bold'), fill=(0, 210, 255))
    
    base.save(f'{OUT_DIR}/slide_11.png')
    print("SAVED slide_11.png (Core Flow Interactive Prototype Walkthrough)")


# ==============================================================
# SLIDE 12: Business Impact & STAR Retrospective (Executive)
# ==============================================================
def make_slide_12():
    base = Image.new('RGBA', (W, H), (9, 13, 22, 255))
    
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([1100, 200, 1850, 900], fill=(0, 87, 255, 60))
    gw.ellipse([150, 400, 750, 1000], fill=(0, 230, 118, 40))
    glow = glow.filter(ImageFilter.GaussianBlur(130))
    base = Image.alpha_composite(base, glow)
    draw = ImageDraw.Draw(base)
    
    draw.line([(120, 100), (1800, 100)], fill=(255, 255, 255, 20), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(255, 255, 255, 20), width=1)
    
    draw.text((120, 130), "11  /  BUSINESS IMPACT & STAR RETROSPECTIVE", font=get_font(13, 'bold'), fill=(0, 210, 255))
    draw.text((120, 165), "정량적 비즈니스 임팩트 & 시니어 PM/퀀트 STAR 회고", font=get_font(48, 'black'), fill=(255, 255, 255))
    
    metrics = [
        ("98.2%", "Time-To-Calculation (TTC) 단축", "복합 시뮬레이션 소요 시간 240초 → 4.2초로 대폭 단축"),
        ("0.0%", "부동소수점 오차율 (Zero Float Error)", "Closed-Form 역산 수식 및 경계 불변식(Invariant) 100% 무결성"),
        ("42.0%", "Day-30 리텐션 & 99.98% Crash-Free", "24h VIP 무광고 라이프사이클 및 로컬 영속화 기반 고착도")
    ]
    mx = 120
    mw = 533
    mgap = 40
    for val, title, desc in metrics:
        draw.rounded_rectangle([mx, 245, mx + mw, 375], radius=16, fill=(16, 22, 34), outline=(255, 255, 255, 20), width=1)
        draw.text((mx + 28, 260), val, font=get_num_font(46, 'black'), fill=(0, 210, 255))
        draw.text((mx + 28, 314), title, font=get_font(16, 'bold'), fill=(255, 255, 255))
        draw.text((mx + 28, 342), desc, font=get_font(12.5, 'regular'), fill=(148, 163, 184))
        mx += mw + mgap
        
    star_items = [
        ("Situation (상황 & 시장 기회)", "리테일 트레이더 82.6%가 급락 장세에서 처분 효과(Disposition Bias)와 손실 회피 편향으로 비이성적 물타기를 집행하여 예수금 고갈 및 포트폴리오 비중 왜곡(Allocation Drift)을 겪음. 기존 증권사 MTS는 사후적 평단 합산에 머물러 목표 탈출 단가 도달에 필요한 정량적 수량을 역산하지 못하며, 8자리 소수점 키패드 타이핑 중 호가 이탈(Slip Risk)이 빈발함.", (255, 107, 107)),
        ("Task (핵심 과제 & OKR)", "1) [Ingestion OKR] 호가 급변 시 0.2초 이내 음성 발화로 단가/수량을 자동 파싱하는 무입력 멀티모달 파이프라인 구축.\n2) [Quant Engine OKR] 목표 탈출가 도달 필요 매수량을 도출하는 Goal-Seeking 폐쇄형 역산 알고리즘 및 경계 불변식 가드 탑재.\n3) [Local-First OKR] 통신 두절 환경에서도 100% 안전하게 시나리오를 영속화하는 Hive NoSQL ACID 아키텍처 설계.", (255, 193, 7)),
        ("Action (설계 및 엔지니어링 실행)", "STT 음성 스트림에서 정규식 AST 토크나이저를 구축해 자연어 수치 어휘를 아라비아 숫자로 무손실 변환하고, 실패 시 원터치 호가 프리셋(±5%, ±10%)으로 즉각 대체하는 페일세이프 구현. 폐쇄형 역산 엔진에 부동소수점 오차 방지 불변식(P_add < P_target < P_0)을 적용하고, RepaintBoundary 최적화로 60fps 반응형 예수금 슬라이더 개발. W3C DTCG 3계층 디자인 토큰 및 WCAG 2.1 AAA 다크모드 시스템 완성.", (33, 150, 243)),
        ("Result (정량적 성과 & 임팩트)", "시뮬레이션 계산 소요 시간(TTC)을 240초에서 4.2초로 98.2% 단축하고, 수치 연산 오차율 0.0% 달성. 보상형 광고 1회 시청 기반 '24시간 VIP 무광고 세션' 모델로 광고 피로도를 제거하여 Day-30 리텐션 42.0% 및 Crash-Free 세션율 99.98% 확보. Google Play Console 글로벌 7개국 프로덕션 배포 및 글로벌 금융 표준 완결.", (76, 175, 80))
    ]
    
    sx = 120
    sw = 395
    sgap = 33
    f_body = get_font(12.5, 'regular')
    for phase, content, color in star_items:
        draw.rounded_rectangle([sx, 410, sx + sw, 940], radius=16, fill=(16, 22, 34), outline=(255, 255, 255, 20), width=1)
        draw.rounded_rectangle([sx + 18, 428, sx + sw - 18, 468], radius=8, fill=color)
        draw.text((sx + 30, 438), phase, font=get_font(13.5, 'bold'), fill=(255, 255, 255))
        
        wrapped_lines = wrap_text_by_words(content, f_body, sw - 48, draw)
        text_y = 488
        for line in wrapped_lines:
            draw.text((sx + 24, text_y), line, font=f_body, fill=(203, 213, 225))
            text_y += 24
        sx += sw + sgap
        
    base.save(f'{OUT_DIR}/slide_12.png')
    print("SAVED slide_12.png")

if __name__ == '__main__':
    for i in range(1, 13):
        func_name = f'make_slide_{i:02d}'
        if func_name in globals():
            globals()[func_name]()
    print("ALL 12 SLIDES GENERATED WITH MASCULINE EDITORIAL AESTHETIC!")
