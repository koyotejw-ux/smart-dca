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
# SLIDE 04: Information Architecture & Customer Journey (Stealth Dark)
# ==============================================================
def make_slide_04():
    base = Image.new('RGBA', (W, H), (9, 13, 22, 255))
    draw = ImageDraw.Draw(base)
    
    draw.line([(120, 100), (1800, 100)], fill=(255, 255, 255, 20), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(255, 255, 255, 20), width=1)
    
    draw.text((120, 130), "03  /  DOMAIN-DRIVEN IA & SERVICE BLUEPRINT (CJM)", font=get_font(13, 'bold'), fill=(0, 210, 255))
    draw.text((120, 165), "도메인 주도 설계(DDD) 기반 5대 IA & 서비스 블루프린트", font=get_font(50, 'black'), fill=(255, 255, 255))
    draw.text((120, 240), "변동성 충격 인지부터 멀티모달 인제스천, 폐쇄형 퀀트 역산, 포트폴리오 감사 및 Local-First ACID 영속화까지의 완결형 아키텍처", font=get_font(18, 'regular'), fill=(148, 163, 184))
    
    # Top: 5-Stage Customer Journey Pipeline (Service Blueprint)
    cjm_stages = [
        ("01. MARKET SHOCK", "변동성 충격 & 공포", "급락 장세(-10%) 진입으로\n처분 효과(Disposition Bias) 자극", "심리적 앵커링 차단 & 즉각 앱 진입", (0, 114, 255)),
        ("02. INGESTION", "멀티모달 인제스천", "호가 급변 중 키패드 입력 지연\n슬리피지(Slip Risk) 발생 위기", "0.2s 음성 AST 파서 & 호가 칩", (0, 210, 255)),
        ("03. QUANT SIM", "알고리즘 시뮬레이션", "사후 평단 합산에 머문 불확실성\n예수금 고갈 리스크 직면", "Closed-Form 역산 & A/B 대조", (139, 92, 246)),
        ("04. RISK AUDIT", "포트폴리오 감사", "특정 종목 80% 편중 고착화\n포트폴리오 왜곡(Allocation Drift)", "3단계 시급도 & 계좌 비중 가드", (245, 158, 11)),
        ("05. ZERO-LOSS", "ACID 영속화", "네트워크 단절 시 데이터 소실\n실매매 집행 불안감 증폭", "Local-First NoSQL 암호화 저장", (16, 185, 129))
    ]
    
    # Connecting pipeline line
    draw.line([(120 + 155, 305), (120 + 4 * 340 + 155, 305)], fill=(0, 87, 255, 120), width=2)
    
    jx = 120
    jw = 320
    jgap = 20
    for p_code, p_title, p_desc, p_sol, p_col in cjm_stages:
        draw.rounded_rectangle([jx, 275, jx + jw, 400], radius=14, fill=(16, 22, 34), outline=(p_col[0], p_col[1], p_col[2], 90), width=1)
        
        # Dynamic Badge Width to prevent any text collision
        code_w = int(draw.textlength(p_code, font=get_font(10, 'bold')) + 16)
        draw.rounded_rectangle([jx + 14, 289, jx + 14 + code_w, 313], radius=4, fill=(p_col[0], p_col[1], p_col[2], 40))
        draw.text((jx + 22, 293), p_code, font=get_font(10, 'bold'), fill=p_col)
        
        draw.text((jx + 14 + code_w + 8, 292), p_title, font=get_font(14, 'bold'), fill=(255, 255, 255))
        
        draw.text((jx + 16, 325), p_desc, font=get_font(12, 'regular'), fill=(148, 163, 184), spacing=3)
        draw.text((jx + 16, 370), "SOL: " + p_sol, font=get_font(11.5, 'bold'), fill=p_col)
        jx += jw + jgap
        
    # Bottom: 5-Domain Hierarchical IA Tree (DDD Architecture)
    domains = [
        ("01. BOOT & LOCAL KERNEL", "시스템 인프라 코어", [
            ("1.1 Cold Boot Orchestrator", "비동기 부팅 & 24h VIP 세션 유효성 검증"),
            ("1.2 Interactive Tutorial", "DCA 수식 및 역산 알고리즘 온보딩 가이드"),
            ("1.3 Local ACID Storage", "SQLite & Hive NoSQL 100% 온디바이스 암호화"),
            ("1.4 Global Locale Provider", "7개국 L10n 및 4대 통화 표준 자동 바인딩")
        ], (0, 114, 255)),
        
        ("02. ASSET DASHBOARD", "포트폴리오 대시보드 도메인", [
            ("2.1 Portfolio Telemetry", "총 평가액, 손익률, 종합 위험도 실시간 집계"),
            ("2.2 24h VIP Ad-Free Token", "보상형 광고 1회 기반 전면 무광고 세션 제어"),
            ("2.3 Multimodal Ingestion", "Google STT 마이크 & ±5%·±10% 호가 프리셋"),
            ("2.4 Quick 2x2 Action Dock", "새 계산 / A-B 비교 / 목표 역산 / 리포트 진입")
        ], (0, 210, 255)),
        
        ("03. QUANT CORE ENGINE", "퀀트 시뮬레이션 알고리즘 코어", [
            ("3.1 Multi-Batch DCA", "1~N차 분할 매수 가중평균 Closed-Form 연산"),
            ("3.2 Dual-Scenario Comparator", "공격적 vs 보수적 전략 방어율 동시 대조"),
            ("3.3 Goal-Seeking Inversion", "손익분기점(BEP) 도달 필요 수량 폐쇄형 역산"),
            ("3.4 Capital Constraint Opt", "가용 예수금 제약 조건 내 최적 평단 도출")
        ], (139, 92, 246)),
        
        ("04. RISK DIAGNOSTICS", "리스크 진단 & 포트폴리오 감사", [
            ("4.1 Asset Concentration Donut", "종목별 자산 비중 및 단일 종목 집중도 가시화"),
            ("4.2 3-Tier Volatility Matrix", "안전 / 주의 / 위험 3단계 정밀 리스크 판정"),
            ("4.3 Simulation Ledger", "저장된 시뮬레이션 시나리오 로드/편집/CSV"),
            ("4.4 Diagnostic Export", "PNG 리포트 카드 원클릭 클립보드 공유")
        ], (245, 158, 11)),
        
        ("05. GLOBAL GOVERNANCE", "글로벌 거버넌스 & 컴플라이언스", [
            ("5.1 Dynamic I18n / L10n", "한국어, 영어, 일본어, 중국어 등 7개국어 지원"),
            ("5.2 Multi-Currency FX Engine", "KRW(₩), USD($), JPY(¥), EUR(€) 통화 체계"),
            ("5.3 OLED High-Contrast Theme", "야간 트레이더 WCAG 2.1 AAA 고대비 토큰"),
            ("5.4 Privacy & Compliance Guard", "GDPR/CCPA 준수 100% 로컬 프라이버시 보호")
        ], (16, 185, 129))
    ]
    
    cx = 120
    cw = 320
    cgap = 20
    for d_code, d_name, items, d_col in domains:
        draw.rounded_rectangle([cx, 425, cx + cw, 945], radius=16, fill=(16, 22, 34), outline=(255, 255, 255, 20), width=1)
        
        # Domain Header
        draw.rounded_rectangle([cx + 12, 437, cx + cw - 12, 487], radius=10, fill=(9, 13, 22), outline=(d_col[0], d_col[1], d_col[2], 70), width=1)
        draw.text((cx + 22, 444), d_code, font=get_font(11, 'bold'), fill=d_col)
        draw.text((cx + 22, 463), d_name, font=get_font(14.5, 'bold'), fill=(255, 255, 255))
        
        iy = 500
        for ititle, idesc in items:
            draw.rounded_rectangle([cx + 12, iy, cx + cw - 12, iy + 98], radius=10, fill=(9, 13, 22), outline=(255, 255, 255, 15), width=1)
            draw.ellipse([cx + 24, iy + 17, cx + 32, iy + 25], fill=d_col)
            draw.text((cx + 40, iy + 13), ititle, font=get_font(13, 'bold'), fill=(255, 255, 255))
            draw.text((cx + 24, iy + 42), idesc, font=get_font(12, 'regular'), fill=(148, 163, 184))
            iy += 108
            
        cx += cw + cgap
        
    base.save(f'{OUT_DIR}/slide_04.png')
    print("SAVED slide_04.png")

# SLIDE 05: True User Flowchart Schematic Diagram
# ==============================================================
def make_slide_05():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Hairline Top/Bottom Boundaries
    draw.line([(120, 100), (1800, 100)], fill=(226, 232, 240), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(226, 232, 240), width=1)
    
    # Header
    draw.text((120, 130), "04  /  END-TO-END INTERACTION STATE MACHINE & ACTIVITY FLOW", font=get_font(13, 'bold'), fill=(0, 87, 255))
    draw.text((120, 165), "엔드투엔드 인터랙션 상태 전이도 & 액티비티 플로우", font=get_font(50, 'black'), fill=(15, 23, 42))
    draw.text((120, 240), "시스템 부팅부터 온디바이스 음성 AST 토크나이저, Goal-Seeking 경계 불변식(Invariant) 검증, 트랜잭션 롤백 및 로컬 영속화까지의 정밀 플로우", font=get_font(18, 'regular'), fill=(100, 116, 139))
    
    # Diagram Legend (Top-Right)
    legends = [
        ("시작/종료 (Node)", (16, 185, 129)),
        ("화면 상태 (State)", (0, 87, 255)),
        ("조건 분기 (Guard)", (217, 119, 6)),
        ("멀티모달 (Action)", (122, 34, 255)),
        ("ACID 영속화 (DB)", (71, 85, 105))
    ]
    leg_x = 1100
    for l_text, l_col in legends:
        draw.ellipse([leg_x, 134, leg_x + 10, 144], fill=l_col)
        draw.text((leg_x + 16, 131), l_text, font=get_font(12, 'bold'), fill=(71, 85, 105))
        leg_x += draw.textlength(l_text, font=get_font(12, 'bold')) + 28
        
    # 4 Chronological Flow Columns (Lanes)
    col_w = 390
    col_gap = 35
    cols_x = [120 + i * (col_w + col_gap) for i in range(4)]
    
    # Column Headers (Lanes)
    lanes = [
        ("PHASE 01 : 부팅 & 세션 검증", "BOOT & SESSION STATE"),
        ("PHASE 02 : 인제스천 디스패처", "INGESTION DISPATCHER"),
        ("PHASE 03 : 퀀트 알고리즘 코어", "QUANT ALGORITHMIC CORE"),
        ("PHASE 04 : 리스크 감사 & 영속화", "AUDIT & ACID PERSISTENCE")
    ]
    
    for i, (l_title, l_code) in enumerate(lanes):
        cx = cols_x[i]
        draw.rounded_rectangle([cx, 280, cx + col_w, 324], radius=8, fill=(241, 245, 249), outline=(226, 232, 240), width=1)
        draw.text((cx + 14, 288), l_code, font=get_font(10.5, 'bold'), fill=(0, 87, 255))
        draw.text((cx + 14, 303), l_title.split(' : ')[-1], font=get_font(13.5, 'bold'), fill=(15, 23, 42))
        
    # Helper to draw arrows
    def draw_down_arrow(x, y1, y2, col=(148, 163, 184)):
        draw.line([(x, y1), (x, y2)], fill=col, width=2)
        draw.polygon([(x - 4, y2 - 6), (x + 4, y2 - 6), (x, y2)], fill=col)
        
    def draw_right_arrow(x1, x2, y, col=(0, 87, 255)):
        draw.line([(x1, y), (x2, y)], fill=col, width=2)
        draw.polygon([(x2 - 6, y - 4), (x2 - 6, y + 4), (x2, y)], fill=col)

    # -------------------------------------------------------------
    # LANE 1: Boot & Session State (x = cols_x[0])
    # -------------------------------------------------------------
    c0 = cols_x[0]
    # Node 1: Start Pill
    draw.rounded_rectangle([c0 + 90, 345, c0 + col_w - 90, 385], radius=20, fill=(236, 253, 245), outline=(16, 185, 129), width=2)
    draw.ellipse([c0 + 105, 360, c0 + 115, 370], fill=(16, 185, 129))
    draw.text((c0 + 125, 355), "앱 콜드 스타트 (Cold Launch)", font=get_font(12.5, 'bold'), fill=(6, 95, 70))
    
    draw_down_arrow(c0 + col_w // 2, 385, 410)
    
    # Node 2: Splash & Kernel Init
    draw.rounded_rectangle([c0 + 20, 410, c0 + col_w - 20, 465], radius=10, fill=(255, 255, 255), outline=(0, 87, 255), width=1)
    draw.rounded_rectangle([c0 + 20, 410, c0 + 26, 465], radius=2, fill=(0, 87, 255))
    draw.text((c0 + 38, 418), "커널 초기화 (Kernel Initialization)", font=get_font(13.5, 'bold'), fill=(15, 23, 42))
    draw.text((c0 + 38, 440), "비동기 부팅 & SQLite/Hive 캐시 복원", font=get_font(11.5, 'regular'), fill=(100, 116, 139))
    
    draw_down_arrow(c0 + col_w // 2, 465, 490)
    
    # Node 3: Decision - First Run?
    draw.rounded_rectangle([c0 + 15, 490, c0 + col_w - 15, 595], radius=12, fill=(255, 251, 235), outline=(245, 158, 11), width=1)
    draw.rounded_rectangle([c0 + 25, 500, c0 + 95, 524], radius=6, fill=(254, 243, 199))
    draw.text((c0 + 33, 504), "◆ GUARD", font=get_font(10, 'bold'), fill=(180, 83, 9))
    draw.text((c0 + 105, 503), "최초 실행 여부? [isFirstLaunch]", font=get_font(12.5, 'bold'), fill=(15, 23, 42))
    
    # Branch YES
    draw.rounded_rectangle([c0 + 25, 532, c0 + col_w - 25, 558], radius=6, fill=(255, 255, 255), outline=(253, 230, 138), width=1)
    draw.text((c0 + 35, 536), "TRUE", font=get_font(10, 'bold'), fill=(217, 119, 6))
    draw.text((c0 + 75, 536), "4단계 인터랙티브 온보딩 가이드 실행", font=get_font(11.5, 'semibold'), fill=(30, 41, 59))
    
    # Branch NO
    draw.rounded_rectangle([c0 + 25, 564, c0 + col_w - 25, 590], radius=6, fill=(255, 255, 255), outline=(253, 230, 138), width=1)
    draw.text((c0 + 35, 568), "FALSE", font=get_font(10, 'bold'), fill=(21, 128, 61))
    draw.text((c0 + 75, 568), "Fast Hydration (세션 스냅샷 즉시 복원)", font=get_font(11.5, 'semibold'), fill=(30, 41, 59))
    
    draw_down_arrow(c0 + col_w // 2, 595, 625)
    
    # Node 4: Decision - 24h VIP Status?
    draw.rounded_rectangle([c0 + 15, 625, c0 + col_w - 15, 730], radius=12, fill=(255, 251, 235), outline=(245, 158, 11), width=1)
    draw.rounded_rectangle([c0 + 25, 635, c0 + 95, 659], radius=6, fill=(254, 243, 199))
    draw.text((c0 + 33, 639), "◆ GUARD", font=get_font(10, 'bold'), fill=(180, 83, 9))
    draw.text((c0 + 105, 638), "24h VIP 유효성? [expire_at > now]", font=get_font(12, 'bold'), fill=(15, 23, 42))
    
    draw.rounded_rectangle([c0 + 25, 668, c0 + col_w - 25, 694], radius=6, fill=(255, 255, 255), outline=(253, 230, 138), width=1)
    draw.text((c0 + 35, 672), "VALID", font=get_font(10, 'bold'), fill=(21, 128, 61))
    draw.text((c0 + 75, 672), "Ad-Free Pass (전면 광고 100% 바이패스)", font=get_font(11.5, 'semibold'), fill=(30, 41, 59))
    
    draw.rounded_rectangle([c0 + 25, 700, c0 + col_w - 25, 726], radius=6, fill=(255, 255, 255), outline=(253, 230, 138), width=1)
    draw.text((c0 + 35, 704), "EXPIRED", font=get_font(9.5, 'bold'), fill=(220, 38, 38))
    draw.text((c0 + 82, 704), "VIP 리워드 갱신 슬롯 대시보드 노출", font=get_font(11.5, 'semibold'), fill=(30, 41, 59))
    
    draw_down_arrow(c0 + col_w // 2, 730, 755)
    
    # Path into Lane 2 connector
    draw.rounded_rectangle([c0 + 20, 755, c0 + col_w - 20, 805], radius=10, fill=(240, 246, 255), outline=(186, 215, 255), width=1)
    draw.text((c0 + 38, 764), "HomeScreen 라우팅 & 바인딩", font=get_font(13, 'bold'), fill=(0, 87, 255))
    draw.text((c0 + 38, 784), "대시보드 텔레메트리 상태 주입 완료", font=get_font(11.5, 'regular'), fill=(71, 85, 105))

    # Connector Arrow from Lane 1 to Lane 2
    draw.line([(c0 + col_w - 20, 780), (cols_x[1] + 20, 780)], fill=(0, 87, 255), width=2)
    draw.polygon([(cols_x[1] + 14, 776), (cols_x[1] + 14, 784), (cols_x[1] + 20, 780)], fill=(0, 87, 255))

    # -------------------------------------------------------------
    # LANE 2: Ingestion Dispatcher (x = cols_x[1])
    # -------------------------------------------------------------
    c1 = cols_x[1]
    # Primary Screen Node
    draw.rounded_rectangle([c1 + 15, 345, c1 + col_w - 15, 415], radius=12, fill=(255, 255, 255), outline=(0, 87, 255), width=2)
    draw.rounded_rectangle([c1 + 15, 345, c1 + col_w - 15, 375], radius=12, fill=(0, 87, 255))
    draw.text((c1 + 30, 352), "STATE : 홈 대시보드 (HomeScreen)", font=get_font(12, 'bold'), fill=(255, 255, 255))
    draw.text((c1 + 30, 385), "• 총 자산 텔레메트리   • 2x2 액션 도크\n• 24h VIP 세션 타이머  • 보유 자산 실시간 리스트", font=get_font(11.5, 'regular'), fill=(51, 65, 85))
    
    draw_down_arrow(c1 + col_w // 2, 415, 440)
    
    # Multimodal Interaction Node
    draw.rounded_rectangle([c1 + 15, 440, c1 + col_w - 15, 515], radius=12, fill=(245, 243, 255), outline=(122, 34, 255), width=1)
    draw.rounded_rectangle([c1 + 25, 450, c1 + 120, 474], radius=6, fill=(237, 233, 254))
    draw.text((c1 + 33, 454), "▱ MULTIMODAL", font=get_font(10, 'bold'), fill=(109, 40, 217))
    draw.text((c1 + 130, 453), "AI 음성 스트림 수신 (STT)", font=get_font(13, 'bold'), fill=(15, 23, 42))
    draw.text((c1 + 30, 482), "마이크 활성화 시 60fps 오디오 파형 바인딩\n\"삼성전자 7만원에 50주\" 복합 자연어 수신", font=get_font(11.5, 'regular'), fill=(71, 85, 105))
    
    draw_down_arrow(c1 + col_w // 2, 515, 540)
    
    # Decision: STT Recognized?
    draw.rounded_rectangle([c1 + 15, 540, c1 + col_w - 15, 645], radius=12, fill=(255, 251, 235), outline=(245, 158, 11), width=1)
    draw.rounded_rectangle([c1 + 25, 550, c1 + 95, 574], radius=6, fill=(254, 243, 199))
    draw.text((c1 + 33, 554), "◆ GUARD", font=get_font(10, 'bold'), fill=(180, 83, 9))
    draw.text((c1 + 105, 553), "AST 토크나이저 파싱 성공?", font=get_font(12.5, 'bold'), fill=(15, 23, 42))
    
    # Branch Success
    draw.rounded_rectangle([c1 + 25, 582, c1 + col_w - 25, 608], radius=6, fill=(255, 255, 255), outline=(253, 230, 138), width=1)
    draw.text((c1 + 35, 586), "성공", font=get_font(10.5, 'bold'), fill=(21, 128, 61))
    draw.text((c1 + 75, 586), "정규식 AST 매칭: [종목, 단가, 수량] 분리", font=get_font(11.5, 'semibold'), fill=(30, 41, 59))
    
    # Branch Fail/Fallback
    draw.rounded_rectangle([c1 + 25, 614, c1 + col_w - 25, 640], radius=6, fill=(255, 255, 255), outline=(253, 230, 138), width=1)
    draw.text((c1 + 35, 618), "예외", font=get_font(10.5, 'bold'), fill=(220, 38, 38))
    draw.text((c1 + 75, 618), "원터치 호가 프리셋 칩(±5%, ±10%) 즉시 대체", font=get_font(11.5, 'semibold'), fill=(30, 41, 59))
    
    draw_down_arrow(c1 + col_w // 2, 645, 670)
    
    # Data Forwarding Node
    draw.rounded_rectangle([c1 + 20, 670, c1 + col_w - 20, 720], radius=10, fill=(240, 246, 255), outline=(186, 215, 255), width=1)
    draw.text((c1 + 38, 679), "SimulatorScreen 파라미터 주입", font=get_font(13, 'bold'), fill=(0, 87, 255))
    draw.text((c1 + 38, 699), "입력 지연 0.2초 미만 무손실 상태 전이", font=get_font(11.5, 'regular'), fill=(71, 85, 105))
    
    # Secondary Path: Local Asset DB
    draw.rounded_rectangle([c1 + 20, 740, c1 + col_w - 20, 805], radius=10, fill=(248, 250, 252), outline=(100, 116, 139), width=1)
    draw.rounded_rectangle([c1 + 30, 750, c1 + 105, 772], radius=4, fill=(226, 232, 240))
    draw.text((c1 + 38, 754), "⛃ LOCAL DB", font=get_font(9.5, 'bold'), fill=(51, 65, 85))
    draw.text((c1 + 115, 753), "Async SQLite 자산 영속화", font=get_font(12, 'bold'), fill=(15, 23, 42))
    draw.text((c1 + 30, 778), "포트폴리오 비중 및 보유 현황 로컬 동기화", font=get_font(11, 'regular'), fill=(100, 116, 139))

    # Connector Arrow from Lane 2 to Lane 3
    draw.line([(c1 + col_w - 20, 695), (cols_x[2] + 20, 695)], fill=(0, 87, 255), width=2)
    draw.polygon([(cols_x[2] + 14, 691), (cols_x[2] + 14, 699), (cols_x[2] + 20, 695)], fill=(0, 87, 255))

    # -------------------------------------------------------------
    # LANE 3: Quant Algorithmic Core (x = cols_x[2])
    # -------------------------------------------------------------
    c2 = cols_x[2]
    # Primary Screen Node
    draw.rounded_rectangle([c2 + 15, 345, c2 + col_w - 15, 415], radius=12, fill=(255, 255, 255), outline=(0, 87, 255), width=2)
    draw.rounded_rectangle([c2 + 15, 345, c2 + col_w - 15, 375], radius=12, fill=(0, 87, 255))
    draw.text((c2 + 30, 352), "STATE : 퀀트 시뮬레이터 (SimulatorScreen)", font=get_font(12, 'bold'), fill=(255, 255, 255))
    draw.text((c2 + 30, 385), "• 3-Way 전략 세그먼트   • 양방향 수치 스텝퍼\n• 차수별 분할 매수 입력  • 가용 예수금 슬라이더", font=get_font(11.5, 'regular'), fill=(51, 65, 85))
    
    draw_down_arrow(c2 + col_w // 2, 415, 440)
    
    # Decision: Mode Selection
    draw.rounded_rectangle([c2 + 15, 440, c2 + col_w - 15, 545], radius=12, fill=(255, 251, 235), outline=(245, 158, 11), width=1)
    draw.rounded_rectangle([c2 + 25, 450, c2 + 95, 474], radius=6, fill=(254, 243, 199))
    draw.text((c2 + 33, 454), "◆ GUARD", font=get_font(10, 'bold'), fill=(180, 83, 9))
    draw.text((c2 + 105, 453), "시뮬레이션 알고리즘 선택?", font=get_font(12.5, 'bold'), fill=(15, 23, 42))
    
    draw.text((c2 + 30, 482), "① Multi-Batch DCA : 1~N차 가중평균 폐쇄형 연산\n② Scenario A vs B : 공격적 vs 보수적 전략 매트릭스\n③ Goal-Seeking Engine : 손익분기점(BEP) 역산 도출", font=get_font(11.5, 'regular'), fill=(71, 85, 105), spacing=3)
    
    draw_down_arrow(c2 + col_w // 2, 545, 570)
    
    # Boundary Defense Decision
    draw.rounded_rectangle([c2 + 15, 570, c2 + col_w - 15, 675], radius=12, fill=(255, 251, 235), outline=(245, 158, 11), width=1)
    draw.rounded_rectangle([c2 + 25, 580, c2 + 95, 604], radius=6, fill=(254, 243, 199))
    draw.text((c2 + 33, 584), "◆ GUARD", font=get_font(10, 'bold'), fill=(180, 83, 9))
    draw.text((c2 + 105, 583), "경계 불변식(Invariant) 검증?", font=get_font(12.5, 'bold'), fill=(15, 23, 42))
    
    # Branch Invalid
    draw.rounded_rectangle([c2 + 25, 612, c2 + col_w - 25, 638], radius=6, fill=(255, 255, 255), outline=(253, 230, 138), width=1)
    draw.text((c2 + 35, 616), "위반", font=get_font(10.5, 'bold'), fill=(220, 38, 38))
    draw.text((c2 + 82, 616), "P_add < P_target < P_0 위반: 에러 토스트", font=get_font(11, 'semibold'), fill=(30, 41, 59))
    
    # Branch Valid
    draw.rounded_rectangle([c2 + 25, 644, c2 + col_w - 25, 670], radius=6, fill=(255, 255, 255), outline=(253, 230, 138), width=1)
    draw.text((c2 + 35, 648), "통과", font=get_font(10.5, 'bold'), fill=(21, 128, 61))
    draw.text((c2 + 82, 648), "Closed-Form Q_add = Q_0(P_0-Pt)/(Pt-Pa) 연산", font=get_font(11, 'semibold'), fill=(30, 41, 59))
    
    draw_down_arrow(c2 + col_w // 2, 675, 700)
    
    # Output Card
    draw.rounded_rectangle([c2 + 20, 700, c2 + col_w - 20, 805], radius=10, fill=(240, 246, 255), outline=(186, 215, 255), width=1)
    draw.rounded_rectangle([c2 + 30, 710, c2 + 105, 732], radius=4, fill=(0, 87, 255))
    draw.text((c2 + 38, 714), "TELEMETRY", font=get_font(9.5, 'bold'), fill=(255, 255, 255))
    draw.text((c2 + 115, 713), "실시간 정량 연산 텔레메트리 출력", font=get_font(12, 'bold'), fill=(15, 23, 42))
    draw.text((c2 + 30, 742), "• 신규 평단가 : ₩ 74,666 (-4.3% 인하)\n• 필요 추가 수량 : +42.5주 (부동소수점 오차 0%)\n• 소요 예수금 : ₩ 2,125,000 (한도 제약 검증)", font=get_font(11.5, 'regular'), fill=(51, 65, 85), spacing=2)

    # Connector Arrow from Lane 3 to Lane 4
    draw.line([(c2 + col_w - 20, 750), (cols_x[3] + 20, 750)], fill=(0, 87, 255), width=2)
    draw.polygon([(cols_x[3] + 14, 746), (cols_x[3] + 14, 754), (cols_x[3] + 20, 750)], fill=(0, 87, 255))

    # -------------------------------------------------------------
    # LANE 4: Audit & ACID Persistence (x = cols_x[3])
    # -------------------------------------------------------------
    c3 = cols_x[3]
    # Primary Screen Node
    draw.rounded_rectangle([c3 + 15, 345, c3 + col_w - 15, 415], radius=12, fill=(255, 255, 255), outline=(0, 87, 255), width=2)
    draw.rounded_rectangle([c3 + 15, 345, c3 + col_w - 15, 375], radius=12, fill=(0, 87, 255))
    draw.text((c3 + 30, 352), "STATE : 포트폴리오 감사 리포트 (ReportScreen)", font=get_font(12, 'bold'), fill=(255, 255, 255))
    draw.text((c3 + 30, 385), "• 자산 비중 도넛 차트  • 물타기 시급도 3단계 판정\n• 비중 편중 리스크 경보 • 클립보드 원클릭 공유", font=get_font(11.5, 'regular'), fill=(51, 65, 85))
    
    draw_down_arrow(c3 + col_w // 2, 415, 440)
    
    # Risk Decision
    draw.rounded_rectangle([c3 + 15, 440, c3 + col_w - 15, 545], radius=12, fill=(255, 251, 235), outline=(245, 158, 11), width=1)
    draw.rounded_rectangle([c3 + 25, 450, c3 + 95, 474], radius=6, fill=(254, 243, 199))
    draw.text((c3 + 33, 454), "◆ GUARD", font=get_font(10, 'bold'), fill=(180, 83, 9))
    draw.text((c3 + 105, 453), "단일 종목 계좌 비중 > 50%?", font=get_font(12.5, 'bold'), fill=(15, 23, 42))
    
    # Branch Risk High
    draw.rounded_rectangle([c3 + 25, 482, c3 + col_w - 25, 508], radius=6, fill=(255, 255, 255), outline=(253, 230, 138), width=1)
    draw.text((c3 + 35, 486), "위험", font=get_font(10.5, 'bold'), fill=(220, 38, 38))
    draw.text((c3 + 75, 486), "Allocation Drift 경보 & 포트폴리오 분산 가이드", font=get_font(11, 'semibold'), fill=(30, 41, 59))
    
    # Branch Safe
    draw.rounded_rectangle([c3 + 25, 514, c3 + col_w - 25, 540], radius=6, fill=(255, 255, 255), outline=(253, 230, 138), width=1)
    draw.text((c3 + 35, 518), "안전", font=get_font(10.5, 'bold'), fill=(21, 128, 61))
    draw.text((c3 + 75, 518), "적정 자산 분산 상태 확인 & 리포트 통과", font=get_font(11.5, 'semibold'), fill=(30, 41, 59))
    
    draw_down_arrow(c3 + col_w // 2, 545, 570)
    
    # Persistence Action
    draw.rounded_rectangle([c3 + 15, 570, c3 + col_w - 15, 675], radius=12, fill=(255, 251, 235), outline=(245, 158, 11), width=1)
    draw.rounded_rectangle([c3 + 25, 580, c3 + 95, 604], radius=6, fill=(254, 243, 199))
    draw.text((c3 + 33, 584), "◆ GUARD", font=get_font(10, 'bold'), fill=(180, 83, 9))
    draw.text((c3 + 105, 583), "시나리오 영속화 & 공유?", font=get_font(12.5, 'bold'), fill=(15, 23, 42))
    
    draw.rounded_rectangle([c3 + 25, 612, c3 + col_w - 25, 638], radius=6, fill=(255, 255, 255), outline=(253, 230, 138), width=1)
    draw.text((c3 + 35, 616), "저장", font=get_font(10.5, 'bold'), fill=(21, 128, 61))
    draw.text((c3 + 75, 616), "Hive NoSQL ACID Write (0ms 로컬 영구 보관)", font=get_font(11, 'semibold'), fill=(30, 41, 59))
    
    draw.rounded_rectangle([c3 + 25, 644, c3 + col_w - 25, 670], radius=6, fill=(255, 255, 255), outline=(253, 230, 138), width=1)
    draw.text((c3 + 35, 648), "공유", font=get_font(10.5, 'bold'), fill=(0, 87, 255))
    draw.text((c3 + 75, 648), "1-Click 스냅샷 클립보드 복사 & 리포트 카드", font=get_font(11, 'semibold'), fill=(30, 41, 59))
    
    draw_down_arrow(c3 + col_w // 2, 675, 710)
    
    # End Pill
    draw.rounded_rectangle([c3 + 80, 710, c3 + col_w - 80, 755], radius=22, fill=(236, 253, 245), outline=(16, 185, 129), width=2)
    draw.ellipse([c3 + 100, 727, c3 + 112, 739], fill=(16, 185, 129))
    draw.text((c3 + 124, 722), "의사결정 완결 (Zero Bias)", font=get_font(13.5, 'bold'), fill=(6, 95, 70))
    
    # Status Complete Tag
    draw.rounded_rectangle([c3 + 20, 775, c3 + col_w - 20, 805], radius=8, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
    draw.text((c3 + 30, 783), "✓ 휴리스틱 오류 차단 완료 & 24h VIP 세션 유지", font=get_font(11, 'bold'), fill=(71, 85, 105))

    # -------------------------------------------------------------
    # Bottom Technical Edge Bar
    # -------------------------------------------------------------
    by = 835
    bh = 115
    draw.rounded_rectangle([120, by, 1800, by + bh], radius=14, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
    draw.rounded_rectangle([136, by + 18, 308, by + 46], radius=6, fill=(0, 87, 255))
    draw.text((146, by + 25), "CORE ARCHITECTURE SPEC", font=get_font(9.5, 'bold'), fill=(255, 255, 255))
    
    specs = [
        ("0.2s 음성 예외 방어 (Fail-Safe)", "STT 권한 거부 또는 소음 환경 시 즉각 원터치 호가 프리셋(±5%, ±10%) 칩으로 전환되어 입력 레이턴시 0초 유지"),
        ("수학적 경계 불변식 (Invariant)", "Closed-Form 역산 공식 적용 전 경계 조건(P_add < P_target < P_0)을 선제 검증하여 부동소수점 오차 및 음수값 원천 차단"),
        ("Local-First ACID 무결성", "통신 두절/오프라인 환경에서도 Hive NoSQL 0ms 인메모리 직렬화 캐싱을 통해 시나리오 및 포트폴리오 데이터 유실 0% 보장")
    ]
    
    sx = 328
    for stitle, sdesc in specs:
        draw.text((sx, by + 18), "• " + stitle, font=get_font(12.5, 'bold'), fill=(15, 23, 42))
        lines = wrap_text_by_words(sdesc, get_font(11.5, 'regular'), 460, draw)
        draw.text((sx, by + 42), lines[0], font=get_font(11.5, 'regular'), fill=(71, 85, 105))
        if len(lines) > 1:
            draw.text((sx, by + 62), lines[1], font=get_font(11.5, 'regular'), fill=(71, 85, 105))
        sx += 485

    base.save(f'{OUT_DIR}/slide_05.png')
    print("SAVED slide_05.png (True User Flowchart Schematic)")


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
    phone_y = 280
    ph = 476  # 236 * 2.0167
    pgap = 53
    px = 120
    
    # Pre-draw unified stage pedestal line
    draw.line([(120, phone_y + ph + 8), (1800, phone_y + ph + 8)], fill=(0, 210, 255, 40), width=1)
    
    for img_path, title, role in screens:
        phone = Image.open(img_path).convert('RGBA')
        phone = phone.resize((pw, ph), Image.Resampling.LANCZOS)
        
        # Soft Drop Shadow directly under phone chin
        sh = Image.new('RGBA', (W, H), (0,0,0,0))
        shd = ImageDraw.Draw(sh)
        shd.ellipse([px - 6, phone_y + ph - 14, px + pw + 6, phone_y + ph + 24], fill=(0, 0, 0, 220))
        sh = sh.filter(ImageFilter.GaussianBlur(16))
        base = Image.alpha_composite(base, sh)
        base.paste(phone, (px, phone_y), phone)
        
        draw = ImageDraw.Draw(base)
        
        # Title Pill Badge: y = 780..816
        pill_y = phone_y + ph + 24
        draw.rounded_rectangle([px, pill_y, px + pw, pill_y + 36], radius=8, fill=(16, 22, 34, 240), outline=(255, 255, 255, 25), width=1)
        draw.rounded_rectangle([px, pill_y + 8, px + 3, pill_y + 28], radius=1, fill=(0, 210, 255))
        draw.text((px + 14, pill_y + 9), title, font=get_font(12, 'bold'), fill=(255, 255, 255))
        
        # Role description: y = 826..844
        draw.text((px + 14, pill_y + 44), role, font=get_font(11, 'regular'), fill=(148, 163, 184))
        
        px += pw + pgap
        
    # Flow Pipeline Arrows across the bottom (y=880..948)
    draw.rounded_rectangle([120, 880, 1800, 948], radius=12, fill=(16, 22, 34, 220), outline=(255, 255, 255, 20), width=1)
    draw.rounded_rectangle([136, 896, 252, 932], radius=6, fill=(0, 87, 255, 40))
    draw.text((148, 905), "USER PIPELINE", font=get_font(11, 'bold'), fill=(0, 210, 255))
    
    flow_steps = [
        ("01 자산 텔레메트리", 260),
        ("02 멀티모달 인제스천", 510),
        ("03 폐쇄형 역산 도출", 780),
        ("04 리스크 감사 진단", 1040),
        ("05 야간 장세 매매", 1300),
        ("06 글로벌 규격 전환", 1550)
    ]
    for step_txt, sx in flow_steps:
        draw.text((sx, 905), step_txt, font=get_font(12.5, 'bold'), fill=(255, 255, 255))
        if sx < 1500:
            draw.text((sx + 150, 903), "→", font=get_font(16, 'bold'), fill=(0, 210, 255))
            
    base.save(f'{OUT_DIR}/slide_10.png')
    print("SAVED slide_10.png")

# ==============================================================
# SLIDE 11: OLED Deep Dark Theme & Accessibility (Pitch Black)
# ==============================================================
def make_slide_11():
    base = Image.new('RGBA', (W, H), (5, 7, 11, 255))
    
    # Ambient Deep Indigo Glow behind dark mockup
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([150, 150, 650, 900], fill=(0, 87, 255, 40))
    gw.ellipse([900, 250, 1700, 950], fill=(0, 210, 255, 18))
    glow = glow.filter(ImageFilter.GaussianBlur(140))
    base = Image.alpha_composite(base, glow)
    draw = ImageDraw.Draw(base)
    
    # Hairline Boundaries
    draw.line([(120, 100), (1800, 100)], fill=(255, 255, 255, 20), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(255, 255, 255, 20), width=1)
    
    # Center-Left Phone Mockup (Sleek Samsung Galaxy S24 Ultra Dark Frame)
    phone = Image.open('portfolio/galaxy_mockups/galaxy_05_dark_home.png').convert('RGBA')
    pw = 330
    ph = int(round(phone.height * (pw / phone.width)))
    phone = phone.resize((pw, ph), Image.Resampling.LANCZOS)
    
    px = 220
    py = 205
    sh = Image.new('RGBA', (W, H), (0,0,0,0))
    shd = ImageDraw.Draw(sh)
    shd.ellipse([px, py + ph - 20, px + pw, py + ph + 35], fill=(0, 0, 0, 255))
    sh = sh.filter(ImageFilter.GaussianBlur(28))
    base = Image.alpha_composite(base, sh)
    base.paste(phone, (px, py), phone)
    
    draw = ImageDraw.Draw(base)
    
    # Right Column Content: tx = 660..1800
    tx = 660
    draw.text((tx, 130), "10  /  OLED DEEP DARK & ACCESSIBILITY SYSTEM", font=get_font(13, 'bold'), fill=(0, 210, 255))
    draw.text((tx, 168), "야간 장세 트레이더를 위한\n초고대비 OLED 다크 테마 시스템", font=get_font(44, 'black'), fill=(255, 255, 255), spacing=8)
    draw.text((tx, 275), "Designed for high-volatility night trading · WCAG 2.1 AAA 7:1 명도 대비 100% 충족\n급박한 야간 미국주식·가상자산 장세에서도 눈 피로 없이 0ms 오독 없는 수치 가독성 보장", font=get_font(15, 'regular'), fill=(148, 163, 184), spacing=5)
    
    specs = [
        ("시맨틱 다크 팔레트 아키텍처 (Semantic Dark Palette)", "순수 블랙(#05070B) 서피스 위에 Electric Blue(#0057FF), Mint(#00E676), Coral(#FF5252), Amber(#FFB300)\n시맨틱 컬러를 정밀 매핑하여 야간 눈부심을 완벽히 차단하고 OLED 디스플레이 배터리 소모 34% 절감", (0, 87, 255)),
        ("Tabular Numbers 고정폭 글꼴 규격 (Anti-Jitter Typography)", "Pretendard OpenType `tnum` 속성을 전역 강제 적용하여 실시간 가격 틱 변동 및 환율 재계산 시\n텍스트 레이아웃의 흔들림(Jitter)을 100% 차단하고 금융 호가 데이터 신뢰도 극대화", (0, 210, 255)),
        ("24시간 VIP 광고 제어 라이프사이클 (User-Centric Monetization)", "보상형 동영상 1회 시청 시 24시간 동안 배너 및 전면 팝업 광고를 전면 제거하여,\n긴박한 야간 매매 호가 변동 순간에 광고 방해 없는 쾌적한 퀀트 계산 환경 제공", (255, 179, 0))
    ]
    
    sy = 365
    for title, desc, col in specs:
        draw.rounded_rectangle([tx, sy, 1800, sy + 155], radius=14, fill=(16, 22, 34, 230), outline=(255, 255, 255, 20), width=1)
        draw.rounded_rectangle([tx, sy + 16, tx + 4, sy + 139], radius=2, fill=col)
        draw.text((tx + 28, sy + 22), title, font=get_font(17, 'bold'), fill=(255, 255, 255))
        draw.text((tx + 28, sy + 62), desc, font=get_font(13.5, 'regular'), fill=(148, 163, 184), spacing=4)
        sy += 180
        
    base.save(f'{OUT_DIR}/slide_11.png')
    print("SAVED slide_11.png")

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
