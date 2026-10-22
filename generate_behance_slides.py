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
    
    # Ambient Lighting
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([1100, 80, 1950, 950], fill=(0, 87, 255, 45))
    gw.ellipse([800, 250, 1400, 900], fill=(0, 210, 255, 20))
    glow = glow.filter(ImageFilter.GaussianBlur(140))
    base = Image.alpha_composite(base, glow)
    draw = ImageDraw.Draw(base)
    
    # Hairline Grid Accents
    draw.line([(120, 100), (1800, 100)], fill=(255, 255, 255, 20), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(255, 255, 255, 20), width=1)
    
    # Top Kicker
    draw.text((120, 130), "SMART DCA CALCULATOR", font=get_font(13, 'bold'), fill=(0, 210, 255))
    draw.text((325, 130), "·", font=get_font(13, 'bold'), fill=(100, 116, 139))
    draw.text((345, 130), "ENTERPRISE FINTECH CASE STUDY", font=get_font(13, 'bold'), fill=(148, 163, 184))
    
    # Live Store Badge
    draw.rounded_rectangle([1580, 122, 1800, 154], radius=6, fill=(16, 185, 129, 25), outline=(16, 185, 129, 90), width=1)
    draw.ellipse([1598, 135, 1606, 143], fill=(16, 185, 129))
    draw.text((1618, 131), "PLAY STORE LIVE", font=get_font(11, 'bold'), fill=(52, 211, 153))
    
    # Giant Headline
    draw.text((120, 220), "하락장 속 뇌동매매를 끝내는\n수학적 분할매수 솔루션", font=get_font(60, 'black'), fill=(255, 255, 255), spacing=18)
    
    draw.text((120, 395), "Stop Panic Selling. Master Algorithmic Scaling.", font=get_font(20, 'bold'), fill=(0, 210, 255))
    draw.text((120, 435), "급격한 주가 하락 시 감정에 휘둘리지 않고, 0.2초 음성 인제스천과\nGoal Seeking 수학 역산으로 계좌를 방어하는 모바일 퀀트 비서", font=get_font(18, 'regular'), fill=(148, 163, 184), spacing=8)
    
    # 3 High-Impact Metric Cards
    metrics = [
        ("0.2s", "VOICE INGESTION", "호가 급락 시 0.2초 음성 발화로 단가·수량 즉각 파싱"),
        ("100%", "GOAL-SEEKING MATH", "희망 평단 도달에 필요한 추가 매수 수량 폐쇄형 역산"),
        ("24h", "VIP AD-FREE CYCLE", "보상형 광고 1회 시청으로 24시간 동안 전면 무광고")
    ]
    
    my = 560
    for val, tag, desc in metrics:
        draw.rounded_rectangle([120, my, 860, my + 105], radius=14, fill=(16, 22, 34, 230), outline=(255, 255, 255, 25), width=1)
        draw.rounded_rectangle([120, my + 16, 124, my + 89], radius=2, fill=(0, 114, 255))
        
        draw.text((150, my + 22), val, font=get_num_font(42, 'black'), fill=(255, 255, 255))
        vw = draw.textlength(val, font=get_num_font(42, 'black'))
        
        draw.rounded_rectangle([150 + vw + 18, my + 26, 150 + vw + 24 + draw.textlength(tag, font=get_font(11, 'bold')), my + 50], radius=4, fill=(0, 87, 255, 40))
        draw.text((150 + vw + 21, my + 30), tag, font=get_font(11, 'bold'), fill=(0, 210, 255))
        
        draw.text((150, my + 72), desc, font=get_font(13.5, 'regular'), fill=(148, 163, 184))
        my += 122
        
    # Dual Mockups
    phone_back = Image.open('portfolio/mockup_ko_02_sim.png').convert('RGBA')
    pb_w = 385
    pb_h = int(phone_back.height * (pb_w / phone_back.width))
    phone_back = phone_back.resize((pb_w, pb_h), Image.Resampling.LANCZOS)
    
    phone_front = Image.open('portfolio/mockup_ko_01_home.png').convert('RGBA')
    pf_w = 415
    pf_h = int(phone_front.height * (pf_w / phone_front.width))
    phone_front = phone_front.resize((pf_w, pf_h), Image.Resampling.LANCZOS)
    
    sh = Image.new('RGBA', (W, H), (0,0,0,0))
    shd = ImageDraw.Draw(sh)
    shd.ellipse([1260, 930, 1680, 1010], fill=(0, 0, 0, 230))
    shd.ellipse([980, 960, 1430, 1040], fill=(0, 0, 0, 255))
    sh = sh.filter(ImageFilter.GaussianBlur(32))
    base = Image.alpha_composite(base, sh)
    
    base.paste(phone_back, (1265, 170), phone_back)
    base.paste(phone_front, (990, 130), phone_front)
    
    icon = Image.open('assets/app_icon_clean_squircle.png').convert('RGBA')
    icon = icon.resize((210, 210), Image.Resampling.LANCZOS)
    icon_sh = Image.new('RGBA', (W, H), (0,0,0,0))
    isd = ImageDraw.Draw(icon_sh)
    isd.ellipse([1360, 680, 1590, 890], fill=(0, 0, 0, 220))
    icon_sh = icon_sh.filter(ImageFilter.GaussianBlur(28))
    base = Image.alpha_composite(base, icon_sh)
    base.paste(icon, (1375, 670), icon)
    
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
    draw.text((120, 130), "01  /  DISCOVERY & USER RESEARCH", font=get_font(13, 'bold'), fill=(0, 87, 255))
    draw.text((120, 165), "감정이 개입하는 순간, 투자는 실패합니다", font=get_font(52, 'black'), fill=(15, 23, 42))
    draw.text((120, 240), "개인 투자자 12명 심층 인터뷰(IDI)와 커뮤니티 데이터 분석을 통해 도출한 3대 뇌동매매 병목 현상", font=get_font(18, 'regular'), fill=(100, 116, 139))
    
    # Left Column: 3 Massive Stat Cards (Architectural & Masculine)
    stats = [
        ("78.4%", "하락장 뇌동매매 경험률", "수학적 계획 없는 감정적 추가 매수 집행", (220, 38, 38)),
        ("4.8분", "호가창 앞 키패드 입력 지연", "소수점 단가·수량 타이핑 중 호가 급변", (217, 119, 6)),
        ("0건", "MTS 내 목표 역산 기능 부재", "본전 탈출 필요 수량을 알지 못한 채 과매수", (0, 87, 255))
    ]
    
    sy = 300
    for val, stitle, sdesc, col in stats:
        draw.rounded_rectangle([120, sy, 620, sy + 195], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw.rounded_rectangle([120, sy + 18, 125, sy + 177], radius=2, fill=col)
        
        draw.text((155, sy + 26), val, font=get_num_font(50, 'black'), fill=col)
        draw.text((155, sy + 105), stitle, font=get_font(17, 'bold'), fill=(15, 23, 42))
        draw.text((155, sy + 138), sdesc, font=get_font(13.5, 'regular'), fill=(100, 116, 139))
        sy += 225
        
    # Right Column: 3 Concrete IDI Reality Cards
    cards = [
        ("01", "전략 부재 : 비중 과대 & 평단 고착",
         "\"단가를 낮추려고 추가 매수를 계속했는데, 나중에 보니 계좌의 80%가 한 종목에 묶여있고 평단은 겨우 2%밖에 안 내려왔습니다.\"\n— 3년 차 개인 투자자 IDI",
         "차수별 한계 효용 및 계좌 편중 위험도(Allocation) 실시간 가시화", (220, 38, 38)),
         
        ("02", "조작 지연 : 호가창 앞 골든타임 상실",
         "\"급락 빔이 쏟아질 때 평단 계산하려고 키패드로 8자리 단가를 치는 동안 이미 반등해버리거나 밑으로 뚫려버립니다.\"\n— 가상자산/단타 트레이더 IDI",
         "0.2초 온디바이스 STT 음성 자동 파싱 & 원터치 호가 프리셋 칩 즉시 주입", (217, 119, 6)),
         
        ("03", "출구 부재 : 탈출 필요 수량 미제공",
         "\"본전이나 -5% 선에서 정리하고 싶은데, 지금 얼마를 더 사야 그 평단이 만들어지는지 알려주는 MTS가 전혀 없습니다.\"\n— 5년 차 직장인 스윙 투자자 IDI",
         "Goal Seeking Closed-Form 수학 공식을 통한 목표 도달 필요 수량 정밀 역산", (0, 87, 255))
    ]
    
    ry = 300
    for num, ptitle, pquote, psol, pcol in cards:
        draw.rounded_rectangle([660, ry, 1800, ry + 195], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        
        # Number badge
        draw.rounded_rectangle([695, ry + 24, 735, ry + 56], radius=6, fill=(15, 23, 42))
        draw.text((702, ry + 29), num, font=get_num_font(15, 'bold'), fill=(255, 255, 255))
        draw.text((750, ry + 28), ptitle, font=get_font(18, 'bold'), fill=(15, 23, 42))
        
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
        draw.text((775, ry + 147), psol, font=get_font(14, 'semibold'), fill=(30, 41, 59))
        
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
    
    draw.text((120, 130), "02  /  BENCHMARK & TARGET PERSONAS", font=get_font(13, 'bold'), fill=(0, 87, 255))
    draw.text((120, 165), "경쟁사 벤치마킹 매트릭스 및 핵심 페르소나", font=get_font(52, 'black'), fill=(15, 23, 42))
    draw.text((120, 240), "기존 MTS 및 일반 앱스토어 계산기 대비 독보적인 사용자 편의성과 알고리즘 기능 우위", font=get_font(18, 'regular'), fill=(100, 116, 139))
    
    # Left: High-Precision Comparison Matrix
    tx = 120
    ty = 300
    tw = 960
    draw.rounded_rectangle([tx, ty, tx + tw, ty + 645], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    # Table Header
    draw.rounded_rectangle([tx, ty, tx + tw, ty + 56], radius=16, fill=(241, 245, 249))
    draw.text((tx + 28, ty + 18), "비교 분석 항목", font=get_font(14, 'bold'), fill=(71, 85, 105))
    draw.text((tx + 200, ty + 18), "증권사 MTS 내장", font=get_font(14, 'bold'), fill=(71, 85, 105))
    draw.text((tx + 410, ty + 18), "일반 앱 계산기", font=get_font(14, 'bold'), fill=(71, 85, 105))
    
    col4_l = tx + 620
    col4_r = tx + tw - 10
    draw.rounded_rectangle([col4_l, ty + 6, col4_r, ty + 639], radius=12, fill=(240, 246, 255), outline=(186, 215, 255), width=2)
    draw.rounded_rectangle([col4_l + 12, ty + 12, col4_r - 12, ty + 50], radius=8, fill=(0, 87, 255))
    draw.text((col4_l + 38, ty + 20), "SMART DCA CALCULATOR", font=get_font(12, 'bold'), fill=(255, 255, 255))
    
    matrix = [
        ("입력 방식", "키패드 수동 입력 (지연)", "키패드 수동 입력 (광고 다수)", "멀티모달 (AI 음성 + 원터치 칩)"),
        ("연산 속도", "3~5초 (복잡한 메뉴 이동)", "2~3초 (단순 합산)", "0.2초 즉시 파싱 및 자동 연산"),
        ("시나리오 비교", "불가능 (단일 계산)", "불가능 (1회성 소멸)", "A vs B 전략 대조 매트릭스"),
        ("목표가 역산", "미지원", "미지원", "Goal Seeking 폐쇄형 역산 알고리즘"),
        ("데이터 보안", "공인인증 로그인 필수", "세션 종료 시 초기화", "Local-First NoSQL 100% 암호화"),
        ("광고 모델", "금융 상품 배너 혼재", "전면 강제 팝업 (피로도 극심)", "24시간 VIP 무광고 라이프사이클"),
        ("다크 테마", "일부 지원 (가독성 낮음)", "단순 그레이스케일 반전", "OLED 고대비 WCAG AAA 토큰")
    ]
    
    row_y = ty + 65
    for item, c1, c2, c3 in matrix:
        draw.line([(tx + 20, row_y), (col4_l - 15, row_y)], fill=(241, 245, 249), width=1)
        draw.text((tx + 28, row_y + 20), item, font=get_font(14, 'bold'), fill=(15, 23, 42))
        draw.text((tx + 200, row_y + 20), c1, font=get_font(13, 'regular'), fill=(100, 116, 139))
        draw.text((tx + 410, row_y + 20), c2, font=get_font(13, 'regular'), fill=(100, 116, 139))
        
        draw.ellipse([col4_l + 16, row_y + 24, col4_l + 24, row_y + 32], fill=(0, 87, 255))
        draw.text((col4_l + 32, row_y + 19), c3, font=get_font(12.5, 'bold'), fill=(0, 87, 255))
        row_y += 81
        
    # Right: 2 High-Impact Persona Cards
    px = 1120
    py = 300
    pw = 680
    
    # Persona A
    draw.rounded_rectangle([px, py, px + pw, py + 308], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([px + 28, py + 24, px + 128, py + 52], radius=6, fill=(240, 246, 255))
    draw.text((px + 38, py + 29), "TRADER A", font=get_font(11, 'bold'), fill=(0, 87, 255))
    draw.text((px + 144, py + 26), "김투자 (34세, 직장인 퀀트/적립식)", font=get_font(19, 'bold'), fill=(15, 23, 42))
    
    draw.text((px + 28, py + 72), "\"월급날마다 분할 매수해서 6개월 안에 본전 탈출하고 싶습니다.\"", font=get_font(15, 'bold'), fill=(0, 87, 255))
    desc_a = [
        "• 투자 성향: 국내 대형 우량주 및 미국 지수 ETF 장기 분할 적립식 매수",
        "• 핵심 고통: 추가 매수 시 특정 종목 비중이 80%까지 비대해져 계좌가 잠식됨",
        "• 필요 기능: 총예산 제약 내 실시간 최적 평단 도출 및 A vs B 시나리오 동시 대조"
    ]
    dy = py + 115
    for d in desc_a:
        draw.text((px + 28, dy), d, font=get_font(13.5, 'regular'), fill=(71, 85, 105))
        dy += 34
        
    # Persona B
    py += 337
    draw.rounded_rectangle([px, py, px + pw, py + 308], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([px + 28, py + 24, px + 128, py + 52], radius=6, fill=(254, 243, 199))
    draw.text((px + 38, py + 29), "TRADER B", font=get_font(11, 'bold'), fill=(217, 119, 6))
    draw.text((px + 144, py + 26), "박스캘퍼 (28세, 크립토/단타 트레이더)", font=get_font(19, 'bold'), fill=(15, 23, 42))
    
    draw.text((px + 28, py + 72), "\"급락 빔 맞았을 때 3초 안에 평단 뽑아서 지지선에서 나와야 합니다.\"", font=get_font(15, 'bold'), fill=(217, 119, 6))
    desc_b = [
        "• 투자 성향: 고변동성 알트코인 및 테마주 단타/스캘핑 매매 집행",
        "• 핵심 고통: 호가창 급변 중 키패드로 소수점 단가를 칠 시간이 전혀 없음",
        "• 필요 기능: 0.2초 음성 즉각 주입 & 목표 탈출가 도달 필요 매수량 폐쇄형 역산"
    ]
    dy = py + 115
    for d in desc_b:
        draw.text((px + 28, dy), d, font=get_font(13.5, 'regular'), fill=(71, 85, 105))
        dy += 34
        
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
    
    draw.text((120, 130), "03  /  INFORMATION ARCHITECTURE & CUSTOMER JOURNEY (CJM)", font=get_font(13, 'bold'), fill=(0, 210, 255))
    draw.text((120, 165), "5대 핵심 도메인 정보 구조(IA) & 고객 여정 지도", font=get_font(52, 'black'), fill=(255, 255, 255))
    draw.text((120, 240), "급락 인지부터 0.2초 음성 인제스천, 알고리즘 시뮬레이션, 포트폴리오 안전 진단 및 로컬 영속화까지의 완결형 아키텍처", font=get_font(18, 'regular'), fill=(148, 163, 184))
    
    # Top: 5-Stage Customer Journey Pipeline
    cjm_stages = [
        ("01. CRISIS", "급락 인지", "보유 종목 급락 (-10%)\n손실 공포 & 뇌동매매 충동", "냉정 회복 & 1초 진입", (0, 114, 255)),
        ("02. INGEST", "초신속 인제스천", "호가 급변 중 타이핑 지연\n매수 골든타임 상실 위기", "0.2s 음성 STT & 호가 칩", (0, 210, 255)),
        ("03. SIMULATE", "알고리즘 시뮬", "추가 매수 시 평단 방어율 &\n필요 자금 불확실성", "가중평균 + A/B + 역산", (139, 92, 246)),
        ("04. DIAGNOSE", "포트폴리오 진단", "특정 종목 과매수로 인한\n계좌 잠식 & 비중 왜곡", "3단계 시급도 & 도넛 차트", (245, 158, 11)),
        ("05. PERSIST", "확신 영속화", "과거 시뮬레이션 소실 &\n실매매 집행 불안감", "Local DB 암호화 & 공유", (16, 185, 129))
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
        
    # Bottom: 5-Domain Hierarchical IA Tree
    domains = [
        ("01. ENTRY & INIT", "온보딩 & 초기화", [
            ("1.1 Splash Engine", "로고 모션 & 24h VIP 즉시 검증"),
            ("1.2 4-Step Guide", "분할 매수 & 역산 원리 인터랙티브 학습"),
            ("1.3 Local DB Engine", "SQLite & Hive NoSQL 100% 로컬 암호화"),
            ("1.4 Auto L10n Engine", "디바이스 언어(7국) 및 통화(4종) 자동 바인딩")
        ], (0, 114, 255)),
        
        ("02. SMART DASHBOARD", "홈 대시보드", [
            ("2.1 Portfolio Hero", "총 평가액, 평균 수익률, 위험도 시각화"),
            ("2.2 24h VIP Banner", "보상형 광고 시청 잔여시간 카운트다운"),
            ("2.3 Multimodal Dock", "Google STT 마이크 & ±5% 호가 칩"),
            ("2.4 Quick 2x2 Grid", "새 계산 / A-B 비교 / 목표 역산 / 리포트")
        ], (0, 210, 255)),
        
        ("03. SIMULATION CORE", "시뮬레이션 엔진", [
            ("3.1 Multi-Batch DCA", "1~N차 가중평균 Closed Form 연산"),
            ("3.2 A/B Comparator", "공격적 vs 보수적 전략 방어율 동시 대조"),
            ("3.3 Goal Seeking Calc", "희망 평단 도달 필수 추가 매수량 역산"),
            ("3.4 Interactive Slider", "가용 예수금 제약 내 실시간 최적 평단")
        ], (139, 92, 246)),
        
        ("04. PORTFOLIO DIAGNOSTICS", "정밀 진단 & 리포트", [
            ("4.1 Asset Donut Chart", "종목별 투자 원금 및 계좌 편중 비중"),
            ("4.2 3-Tier Urgency", "안전 / 주의 / 위험 3단계 시급도 판정"),
            ("4.3 Scenario Manager", "저장된 시뮬레이션 로드/편집/CSV"),
            ("4.4 Diagnostic Export", "PNG 리포트 카드 원클릭 클립보드 공유")
        ], (245, 158, 11)),
        
        ("05. GLOBAL GOVERNANCE", "글로벌 거버넌스", [
            ("5.1 7-Language L10n", "한국어, 영어, 일본어, 중국어, 스페인어 등"),
            ("5.2 4-Currency System", "KRW(₩), USD($), JPY(¥), EUR(€) 환산"),
            ("5.3 OLED Dark System", "야간 트레이더 고대비 WCAG AAA 토큰"),
            ("5.4 Compliance & FAQ", "GDPR 준수 로컬 암호화 & 금융 가이드")
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
        draw.text((cx + 22, 463), d_name, font=get_font(15, 'bold'), fill=(255, 255, 255))
        
        iy = 500
        for ititle, idesc in items:
            draw.rounded_rectangle([cx + 12, iy, cx + cw - 12, iy + 98], radius=10, fill=(9, 13, 22), outline=(255, 255, 255, 15), width=1)
            draw.ellipse([cx + 24, iy + 17, cx + 32, iy + 25], fill=d_col)
            draw.text((cx + 40, iy + 13), ititle, font=get_font(13.5, 'bold'), fill=(255, 255, 255))
            draw.text((cx + 24, iy + 42), idesc, font=get_font(12, 'regular'), fill=(148, 163, 184))
            iy += 108
            
        cx += cw + cgap
        
    base.save(f'{OUT_DIR}/slide_04.png')
    print("SAVED slide_04.png")

# ==============================================================
# SLIDE 05: User Decision Flowchart (Industrial System Architecture)
# ==============================================================
def make_slide_05():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    draw.line([(120, 100), (1800, 100)], fill=(226, 232, 240), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(226, 232, 240), width=1)
    
    draw.text((120, 130), "04  /  USER FLOWCHART & LOGIC BRANCH", font=get_font(13, 'bold'), fill=(0, 87, 255))
    draw.text((120, 165), "사용자 의사결정 경로 및 예외 방어 로직 플로우차트", font=get_font(52, 'black'), fill=(15, 23, 42))
    draw.text((120, 240), "앱 진입부터 STT 권한 거부, 역산 불가 엣지 케이스, VIP 광고 바이패스까지 실서비스 상태 전이 100% 매핑", font=get_font(18, 'regular'), fill=(100, 116, 139))
    
    # Canvas Box
    bx = 120
    by = 285
    bw = 1680
    bh = 665
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=20, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    stages = [
        ("STAGE 1 : 진입 & 분기", "Entry & Init", [
            ("Process", "앱 실행 (Splash Launch)", "앱 로고 모션 & 로컬 캐시 초기화", (0, 87, 255)),
            ("Decision", "최초 실행 여부?", "First Run Check 분기", (217, 119, 6), [
                ("YES", "4단계 온보딩 가이드"),
                ("NO", "24h VIP 토큰 검사")
            ]),
            ("Process", "VIP 광고 바이패스", "무광고 시 전면/오픈 광고 100% 스킵", (16, 185, 129))
        ]),
        
        ("STAGE 2 : 멀티모달 인제스천", "Multimodal Ingest", [
            ("Process", "스마트 대시보드 진입", "포트폴리오 카드 & 2x2 액션 도크", (0, 87, 255)),
            ("Decision", "입력 방식 선택?", "음성 STT vs 수동 키패드", (217, 119, 6), [
                ("STT", "마이크 탭 (Waveform 활성)"),
                ("Manual", "키패드 / 최근 자산 로드")
            ]),
            ("Process", "자연어 파싱 완료", "0.2s 단가·수량 분리 (실패 시 호가 칩)", (16, 185, 129))
        ]),
        
        ("STAGE 3 : 알고리즘 코어", "Simulation Core", [
            ("Process", "시뮬레이터 코어 화면", "단일 DCA / A-B 비교 / 목표 역산", (122, 34, 255)),
            ("Decision", "목표가 유효성 검증?", "P_add < Target < P_0 여부 판정", (217, 119, 6), [
                ("불일치", "경고 토스트 & 달성가능 평단 추천"),
                ("정상", "Closed-Form Q_add 산출")
            ]),
            ("Process", "실시간 수식 연산", "가중평균 & 하락률 방어폭 계산", (16, 185, 129))
        ]),
        
        ("STAGE 4 : 포트폴리오 진단", "Portfolio Diagnostics", [
            ("Process", "실시간 결과 요약 카드", "신규 평단, 평단 인하폭, 필요 총자금", (0, 87, 255)),
            ("Decision", "특정 종목 비중 > 50%?", "포트폴리오 편중 위험 진단", (217, 119, 6), [
                ("YES", "위험 배지 표시 & 분산 권고"),
                ("NO", "안전 포트폴리오 판정")
            ]),
            ("Process", "진단 리포트 생성", "도넛 차트 & 시나리오 분석 매트릭스", (16, 185, 129))
        ]),
        
        ("STAGE 5 : 영속화 & 완결", "Persistence & Decision", [
            ("Process", "진단 리포트 데이터 수신", "포트폴리오 및 시뮬레이션 완료 수치", (0, 87, 255)),
            ("Decision", "시나리오 로컬 저장?", "Local-First NoSQL 영속화", (217, 119, 6), [
                ("저장", "SQLite / Hive 암호화 저장"),
                ("공유", "1-Click 진단 이미지 공유")
            ]),
            ("Complete", "의사결정 완결 & 24h VIP", "뇌동매매 방어 완료 & VIP 타이머 가동", (16, 185, 129))
        ])
    ]
    
    col_w = 305
    col_gap = 32
    cx = bx + 22
    
    for s_idx, (s_title, s_sub, steps) in enumerate(stages):
        # Header
        draw.rounded_rectangle([cx, by + 16, cx + col_w, by + 60], radius=8, fill=(241, 245, 249), outline=(226, 232, 240), width=1)
        draw.text((cx + 14, by + 22), s_sub.upper(), font=get_font(10.5, 'bold'), fill=(0, 87, 255))
        draw.text((cx + 14, by + 38), s_title.split(' : ')[-1], font=get_font(13.5, 'bold'), fill=(15, 23, 42))
        
        # Row 1: Process
        step1 = steps[0]
        y1 = by + 74
        h1 = 88
        draw.rounded_rectangle([cx, y1, cx + col_w, y1 + h1], radius=12, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.rounded_rectangle([cx + 14, y1 + 14, cx + 18, y1 + h1 - 14], radius=2, fill=step1[3])
        draw.text((cx + 28, y1 + 16), step1[1], font=get_font(14, 'bold'), fill=(15, 23, 42))
        draw.text((cx + 28, y1 + 44), step1[2], font=get_font(12, 'regular'), fill=(100, 116, 139))
        
        # Vertical Arrow 1
        draw.line([(cx + col_w // 2, y1 + h1), (cx + col_w // 2, y1 + h1 + 18)], fill=(148, 163, 184), width=2)
        draw.polygon([(cx + col_w // 2 - 4, y1 + h1 + 14), (cx + col_w // 2 + 4, y1 + h1 + 14), (cx + col_w // 2, y1 + h1 + 20)], fill=(148, 163, 184))
        
        # Row 2: Decision Diamond Card (Aligned Horizontally)
        step2 = steps[1]
        y2 = y1 + h1 + 20
        h2 = 142
        draw.rounded_rectangle([cx, y2, cx + col_w, y2 + h2], radius=14, fill=(255, 251, 235), outline=(245, 158, 11), width=2)
        draw.rounded_rectangle([cx + 14, y2 + 14, cx + 76, y2 + 38], radius=6, fill=(254, 243, 199))
        draw.text((cx + 20, y2 + 18), "◆ DECIDE", font=get_font(10, 'bold'), fill=(180, 83, 9))
        draw.text((cx + 86, y2 + 17), step2[1], font=get_font(13, 'bold'), fill=(15, 23, 42))
        
        branches = step2[4]
        # Branch 1
        b1_tag, b1_txt = branches[0]
        draw.rounded_rectangle([cx + 14, y2 + 48, cx + col_w - 14, y2 + 86], radius=8, fill=(255, 255, 255), outline=(253, 230, 138), width=1)
        draw.rounded_rectangle([cx + 20, y2 + 54, cx + 58, y2 + 80], radius=4, fill=(254, 226, 226) if '불일치' in b1_tag or '위험' in b1_txt or 'YES' in b1_tag else (219, 234, 254))
        draw.text((cx + 24, y2 + 59), b1_tag, font=get_font(10.5, 'bold'), fill=(220, 38, 38) if '불일치' in b1_tag or '위험' in b1_txt or 'YES' in b1_tag else (29, 78, 216))
        draw.text((cx + 66, y2 + 59), b1_txt, font=get_font(11.5, 'semibold'), fill=(30, 41, 59))
        
        # Branch 2
        b2_tag, b2_txt = branches[1]
        draw.rounded_rectangle([cx + 14, y2 + 94, cx + col_w - 14, y2 + 132], radius=8, fill=(255, 255, 255), outline=(253, 230, 138), width=1)
        draw.rounded_rectangle([cx + 20, y2 + 100, cx + 58, y2 + 126], radius=4, fill=(220, 252, 231))
        draw.text((cx + 24, y2 + 105), b2_tag, font=get_font(10.5, 'bold'), fill=(21, 128, 61))
        draw.text((cx + 66, y2 + 105), b2_txt, font=get_font(11.5, 'semibold'), fill=(30, 41, 59))
        
        # Vertical Arrow 2
        draw.line([(cx + col_w // 2, y2 + h2), (cx + col_w // 2, y2 + h2 + 18)], fill=(148, 163, 184), width=2)
        draw.polygon([(cx + col_w // 2 - 4, y2 + h2 + 14), (cx + col_w // 2 + 4, y2 + h2 + 14), (cx + col_w // 2, y2 + h2 + 20)], fill=(148, 163, 184))
        
        # Row 3: Resolution
        step3 = steps[2]
        y3 = y2 + h2 + 20
        h3 = 88
        draw.rounded_rectangle([cx, y3, cx + col_w, y3 + h3], radius=12, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.rounded_rectangle([cx + 14, y3 + 14, cx + 18, y3 + h3 - 14], radius=2, fill=step3[3])
        draw.text((cx + 28, y3 + 16), step3[1], font=get_font(14, 'bold'), fill=(15, 23, 42))
        draw.text((cx + 28, y3 + 44), step3[2], font=get_font(12, 'regular'), fill=(100, 116, 139))
        
        # Horizontal Arrow across Row 2
        if s_idx < len(stages) - 1:
            ax = cx + col_w + 3
            ay = y2 + h2 // 2
            draw.line([(ax, ay), (ax + col_gap - 6, ay)], fill=(0, 87, 255), width=2)
            draw.polygon([(ax + col_gap - 8, ay - 4), (ax + col_gap - 8, ay + 4), (ax + col_gap - 2, ay)], fill=(0, 87, 255))
            
        cx += col_w + col_gap
        
    # Bottom Edge Defense Spec Bar
    draw.rounded_rectangle([bx + 18, by + bh - 86, bx + bw - 18, by + bh - 16], radius=12, fill=(240, 246, 255), outline=(186, 215, 255), width=1)
    draw.rounded_rectangle([bx + 30, by + bh - 74, bx + 160, by + bh - 46], radius=6, fill=(0, 87, 255))
    draw.text((bx + 40, by + bh - 68), "EDGE DEFENSE", font=get_font(11, 'bold'), fill=(255, 255, 255))
    
    defenses = [
        "1. STT 음성 예외 방어: 권한 거부 / 잡음 시 0초 딜레이로 원터치 호가 프리셋 칩(±5%, ±10%) 즉시 대체",
        "2. 수학적 오차 방어: 도달 불가 목표가(P_target <= P_add 또는 >= P_0) 입력 시 즉시 경고 토스트 & 달성 가능 목표 평단 자동 추천",
        "3. Local-First 영속화: 음영 지역 오프라인 환경에서도 Hive NoSQL 0ms 캐싱을 통해 시나리오 및 포트폴리오 데이터 유실 0% 보장"
    ]
    dy = by + bh - 72
    for df in defenses:
        draw.text((bx + 175, dy), "• " + df, font=get_font(12, 'semibold'), fill=(30, 41, 59))
        dy += 21
        
    base.save(f'{OUT_DIR}/slide_05.png')
    print("SAVED slide_05.png")

# ==============================================================
# SLIDE 06: Wireframe Blueprint (Industrial CAD Style)
# ==============================================================
def make_slide_06():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    draw.line([(120, 100), (1800, 100)], fill=(226, 232, 240), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(226, 232, 240), width=1)
    
    draw.text((120, 130), "05  /  WIREFRAME & STRUCTURAL RATIONALE", font=get_font(13, 'bold'), fill=(0, 87, 255))
    draw.text((120, 165), "와이어프레임 구조 설계 및 기능 1:1 매핑 명세", font=get_font(52, 'black'), fill=(15, 23, 42))
    draw.text((120, 240), "시각적 스킨(Visual Skin) 이전에 사용자의 인지 부하(Cognitive Load)를 최소화한 3대 핵심 화면 골격", font=get_font(18, 'regular'), fill=(100, 116, 139))
    
    screens = [
        ("Screen 01. 홈 대시보드 골격", [
            ("① Global Header", "앱 타이틀, 도움말(i), 환경설정(설정) 라우팅"),
            ("② VIP Status Banner", "24시간 무광고 잔여시간 카운트다운 타이머"),
            ("③ AI Ingestion Panel", "원터치 STT 발화 버튼 및 파형 시각화"),
            ("④ Quick Preset Chips", "±5%, ±10%, -20% 호가 즉각 주입 칩"),
            ("⑤ Asset Summary Carousel", "등록 자산 카드 가로 스크롤 및 평단 요약"),
            ("⑥ Bottom Action Dock", "시뮬레이터 포탈 가로 버튼 & 리포트 진입 CTA")
        ]),
        ("Screen 02. 시뮬레이터 골격", [
            ("① Strategy Tab Switcher", "단일 계산 / 시나리오 A vs B / 목표 역산 탭"),
            ("② Batch Step Input Card", "보유 평단, 수량, 1차~N차 추가 매수 입력부"),
            ("③ Auto Yield Indicator", "실시간 가중평균 평단 및 방어율 칩"),
            ("④ Capital Allocation Meter", "추가 투입 필요 자금 프로그레스 바"),
            ("⑤ Comparison Split View", "A안 vs B안 결과 수량 대조 카드"),
            ("⑥ Floating Action Button", "시나리오 로컬 DB 저장 및 리포트 생성")
        ]),
        ("Screen 03. 목표 역산 엔진 골격", [
            ("① Target Price Goal Setter", "사용자 희망 목표 평단가 입력 전용 필드"),
            ("② Current Asset Context", "현재 평단 ₩75,000 / 보유 100주 고정 컨텍스트"),
            ("③ Reverse Math Output", "Closed-Form 도출 필요 추가 매수 수량 출력"),
            ("④ Cash Constraint Slider", "가용 현금 한도 내 달성 가능 평단 인터랙티브 조절"),
            ("⑤ Feasibility Warning", "현재가 미달 시 불가능 경고 인포 텍스트"),
            ("⑥ Auto Inject to Sim", "도출한 수량을 시뮬레이터로 1초 자동 주입")
        ])
    ]
    
    wx = 120
    ww = 533
    wgap = 40
    for title, specs in screens:
        draw.rounded_rectangle([wx, 290, wx + ww, 945], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw.text((wx + 28, 314), title, font=get_font(18, 'bold'), fill=(15, 23, 42))
        
        # Schematic Blueprint Box
        draw.rounded_rectangle([wx + 28, 350, wx + ww - 28, 570], radius=12, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
        draw.rounded_rectangle([wx + 48, 370, wx + ww - 48, 398], radius=6, fill=(219, 234, 254))
        draw.rounded_rectangle([wx + 48, 412, wx + ww - 48, 448], radius=8, fill=(226, 232, 240))
        draw.rounded_rectangle([wx + 48, 462, wx + 245, 510], radius=10, fill=(203, 213, 225))
        draw.rounded_rectangle([wx + 265, 462, wx + ww - 48, 510], radius=10, fill=(203, 213, 225))
        draw.rounded_rectangle([wx + 48, 524, wx + ww - 48, 552], radius=6, fill=(186, 215, 255))
        draw.text((wx + 185, 477), "Lo-Fi Blueprint Schema", font=get_font(11.5, 'bold'), fill=(100, 116, 139))
        
        sy = 595
        for s_title, s_desc in specs:
            draw.text((wx + 28, sy), s_title, font=get_font(13.5, 'bold'), fill=(0, 87, 255))
            lines = wrap_text_by_words(s_desc, get_font(12.5, 'regular'), ww - 60, draw)
            draw.text((wx + 28, sy + 20), lines[0], font=get_font(12.5, 'regular'), fill=(71, 85, 105))
            sy += 54
            
        wx += ww + wgap
        
    base.save(f'{OUT_DIR}/slide_06.png')
    print("SAVED slide_06.png")

# ==============================================================
# SLIDE 07: Design System & W3C Tokens (Precision Dark Spec)
# ==============================================================
def make_slide_07():
    base = Image.new('RGBA', (W, H), (9, 13, 22, 255))
    draw = ImageDraw.Draw(base)
    
    draw.line([(120, 100), (1800, 100)], fill=(255, 255, 255, 20), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(255, 255, 255, 20), width=1)
    
    draw.text((120, 130), "06  /  DESIGN SYSTEM & W3C TOKENS", font=get_font(13, 'bold'), fill=(0, 210, 255))
    draw.text((120, 165), "디자인 시스템 파운데이션 및 시맨틱 토큰 매핑", font=get_font(52, 'black'), fill=(255, 255, 255))
    draw.text((120, 240), "W3C 표준 JSON 토큰, WCAG 2.1 AAA 고대비 컬러, Tabular Numbers 고정폭 폰트 위계 체계", font=get_font(18, 'regular'), fill=(148, 163, 184))
    
    # Left: Color Architecture
    draw.rounded_rectangle([120, 290, 890, 945], radius=16, fill=(16, 22, 34), outline=(255, 255, 255, 20), width=1)
    draw.text((150, 318), "Color Architecture & Semantic Tokens", font=get_font(19, 'bold'), fill=(255, 255, 255))
    draw.text((150, 346), "tokens.json 기반 실시간 바인딩 (WCAG 2.1 AAA 7:1 대비 준수)", font=get_font(13.5, 'regular'), fill=(148, 163, 184))
    
    colors = [
        ("Electric Blue", "#0057FF", "Brand Primary Token", (0, 87, 255)),
        ("Mint Gain", "#00E676", "Semantic Success (+Yield)", (0, 230, 118)),
        ("Coral Loss", "#FF5252", "Semantic Error (-Loss)", (255, 82, 82)),
        ("Gold VIP", "#FFB300", "24h VIP Ad-Free Token", (255, 179, 0)),
        ("Royal Violet", "#7A22FF", "AI Voice STT Accent", (122, 34, 255)),
        ("Sky Cyan", "#00D2FF", "Goal Seeking Highlight", (0, 210, 255)),
        ("Deep Slate", "#0F141C", "Dark Background Surface", (15, 20, 28)),
        ("Pure Slate", "#F6F8FC", "Light Background Surface", (246, 248, 252))
    ]
    
    cy = 388
    for i in range(0, len(colors), 2):
        for col_idx in range(2):
            cname, chex, cdesc, rgb = colors[i + col_idx]
            box_x = 150 + col_idx * 360
            draw.rounded_rectangle([box_x, cy, box_x + 80, cy + 85], radius=12, fill=rgb, outline=(255, 255, 255, 30), width=1)
            draw.text((box_x + 98, cy + 10), cname, font=get_font(15, 'bold'), fill=(255, 255, 255))
            draw.text((box_x + 98, cy + 34), chex, font=get_font(13.5, 'bold'), fill=(0, 210, 255))
            draw.text((box_x + 98, cy + 58), cdesc, font=get_font(12, 'regular'), fill=(148, 163, 184))
        cy += 112
        
    # Right: Typography & Tokens
    draw.rounded_rectangle([930, 290, 1800, 945], radius=16, fill=(16, 22, 34), outline=(255, 255, 255, 20), width=1)
    draw.text((960, 318), "Typography Scale & Layout Tokens", font=get_font(19, 'bold'), fill=(255, 255, 255))
    draw.text((960, 346), "숫자 흔들림 방지 Tabular Numbers & 44px 터치 타깃 규격", font=get_font(13.5, 'regular'), fill=(148, 163, 184))
    
    typos = [
        ("Display 32 / Bold", "₩ 1,480,000", "핵심 결과 평단가 및 수익 금액 (tnum 고정폭)"),
        ("Headline 24 / Bold", "+42.5주 추가 매수 필요", "Goal Seeking 역산 산출 결과 강조"),
        ("Title 18 / Bold", "호가 급락 시 원터치 분할 매수", "섹션 헤더 및 주요 카드 타이틀"),
        ("Body 15 / Regular", "급변하는 시장 변동성에 대비한 리스크 방어", "일반 본문 설명 및 툴팁 가이드")
    ]
    
    ty = 390
    for tscale, tex, tdesc in typos:
        draw.rounded_rectangle([960, ty, 1770, ty + 98], radius=12, fill=(9, 13, 22), outline=(255, 255, 255, 15), width=1)
        draw.text((985, ty + 18), tscale, font=get_font(13.5, 'bold'), fill=(0, 210, 255))
        draw.text((1180, ty + 16), tex, font=get_font(18, 'bold'), fill=(255, 255, 255))
        draw.text((985, ty + 56), tdesc, font=get_font(13, 'regular'), fill=(148, 163, 184))
        ty += 114
        
    draw.rounded_rectangle([960, 855, 1345, 920], radius=10, fill=(9, 13, 22), outline=(255, 255, 255, 15), width=1)
    draw.text((980, 868), "Corner Radius Spec", font=get_font(11, 'bold'), fill=(0, 210, 255))
    draw.text((980, 888), "Card 16px (Soft) · Pill 44px (Full)", font=get_font(13, 'bold'), fill=(255, 255, 255))
    
    draw.rounded_rectangle([1385, 855, 1770, 920], radius=10, fill=(9, 13, 22), outline=(255, 255, 255, 15), width=1)
    draw.text((1405, 868), "Elevation & Shadow Spec", font=get_font(11, 'bold'), fill=(0, 230, 118))
    draw.text((1405, 888), "Ambient Drop Shadow y=8, blur=20", font=get_font(13, 'bold'), fill=(255, 255, 255))
    
    base.save(f'{OUT_DIR}/slide_07.png')
    print("SAVED slide_07.png")

# ==============================================================
# SLIDE 08: Feature Spotlight 01 - 0.2s STT (Stealth Hardware Reveal)
# ==============================================================
def make_slide_08():
    base = Image.new('RGBA', (W, H), (9, 13, 22, 255))
    
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([650, 180, 1350, 950], fill=(0, 87, 255, 55))
    glow = glow.filter(ImageFilter.GaussianBlur(130))
    base = Image.alpha_composite(base, glow)
    draw = ImageDraw.Draw(base)
    
    draw.line([(120, 100), (1800, 100)], fill=(255, 255, 255, 20), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(255, 255, 255, 20), width=1)
    
    # Left Header: Sits strictly within x=120..710 (no collision with phone at x=767)
    draw.text((120, 130), "07  /  FEATURE SPOTLIGHT 01 · ON-DEVICE MULTIMODAL", font=get_font(13, 'bold'), fill=(0, 210, 255))
    draw.text((120, 168), "0.2s 하이브리드 음성\n인제스천 파이프라인", font=get_font(44, 'black'), fill=(255, 255, 255), spacing=8)
    draw.text((120, 280), "Google STT 온디바이스 엔진과 정규식 토크나이저 결합\n'종목명+단가+수량' 복합 발화를 오차 없이 자동 분류", font=get_font(15, 'regular'), fill=(148, 163, 184), spacing=5)
    
    # Center Phone Mockup (x=767, width=385, height=777)
    phone = Image.open('portfolio/mockup_ko_08_voice.png').convert('RGBA')
    pw = 385
    ph = int(phone.height * (pw / phone.width))
    phone = phone.resize((pw, ph), Image.Resampling.LANCZOS)
    
    sh = Image.new('RGBA', (W, H), (0,0,0,0))
    shd = ImageDraw.Draw(sh)
    shd.ellipse([767, 950, 767 + pw, 1030], fill=(0, 0, 0, 255))
    sh = sh.filter(ImageFilter.GaussianBlur(32))
    base = Image.alpha_composite(base, sh)
    base.paste(phone, (767, 100), phone)
    
    draw = ImageDraw.Draw(base)
    
    # Left Cards: Below subtitle (ly=365..920)
    cards_l = [
        ("음성 파형 감지 & 실시간 파싱", "\"삼성전자 7만 원에 50주\"\n발화 즉시 0.2초 안에 단가/수량 분리"),
        ("키패드 타이핑 딜레이 78% 단축", "소수점 단가 8자리 입력 시간을 줄여\n매수 골든타임 슬리피지 방어"),
        ("Local-First 0ms 영속화", "Hive NoSQL 캐싱으로 네트워크 없이도\n시뮬레이터 코어로 즉시 주입")
    ]
    ly = 365
    for title, desc in cards_l:
        draw.rounded_rectangle([120, ly, 710, ly + 165], radius=16, fill=(16, 22, 34, 230), outline=(255, 255, 255, 20), width=1)
        draw.rounded_rectangle([120, ly + 18, 124, ly + 147], radius=2, fill=(0, 114, 255))
        draw.text((150, ly + 24), title, font=get_font(18, 'bold'), fill=(255, 255, 255))
        draw.text((150, ly + 68), desc, font=get_font(14, 'regular'), fill=(148, 163, 184), spacing=5)
        ly += 190
        
    # Right Column Cards: x=1210..1800, ry=140..920
    cards_r = [
        ("0-딜레이 오프라인 호가 칩", "STT 권한 거부 또는 소음 환경 시\n±5%, ±10% 원터치 프리셋 즉시 주입", (0, 210, 255)),
        ("실시간 음성 토큰 정규화", "한국어 수치 어휘(일, 십, 백, 천, 만)를\n아라비아 정수 및 실수로 무손실 변환", (0, 230, 118)),
        ("급락장 호가 오차 차단 가드", "종목 매핑과 단가·수량 경계 조건을 검증하여\n비정상 수치(음수, 비현실 호가) 원천 차단", (255, 179, 0)),
        ("60fps 실시간 음성 파형 UI", "마이크 인풋 시 실시간 Waveform 렌더링으로\n사용자에게 즉각적인 오디오 입력 피드백 제공", (147, 51, 234))
    ]
    ry = 140
    for title, desc, col in cards_r:
        draw.rounded_rectangle([1210, ry, 1800, ry + 165], radius=16, fill=(16, 22, 34, 230), outline=(255, 255, 255, 20), width=1)
        draw.rounded_rectangle([1210, ry + 18, 1214, ry + 147], radius=2, fill=col)
        draw.text((1240, ry + 24), title, font=get_font(18, 'bold'), fill=(255, 255, 255))
        draw.text((1240, ry + 68), desc, font=get_font(14, 'regular'), fill=(148, 163, 184), spacing=5)
        ry += 195
        
    base.save(f'{OUT_DIR}/slide_08.png')
    print("SAVED slide_08.png")

# ==============================================================
# SLIDE 09: Feature Spotlight 02 - Goal-Seeking Math (Wall Street Quant)
# ==============================================================
def make_slide_09():
    base = Image.new('RGBA', (W, H), (9, 13, 22, 255))
    
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([1100, 150, 1850, 950], fill=(0, 114, 255, 50))
    glow = glow.filter(ImageFilter.GaussianBlur(140))
    base = Image.alpha_composite(base, glow)
    draw = ImageDraw.Draw(base)
    
    draw.line([(120, 100), (1800, 100)], fill=(255, 255, 255, 20), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(255, 255, 255, 20), width=1)
    
    draw.text((120, 130), "08  /  FEATURE SPOTLIGHT 02 · QUANTITATIVE ALGORITHM", font=get_font(13, 'bold'), fill=(0, 210, 255))
    draw.text((120, 165), "Goal Seeking 폐쇄형 목표 평단가 역산 엔진", font=get_font(46, 'black'), fill=(255, 255, 255))
    draw.text((120, 235), "목표 탈출가 도달에 필요한 추가 매수 수량을 Closed-Form 수식으로 0.001초 만에 산출", font=get_font(17, 'regular'), fill=(148, 163, 184))
    
    # Left: Mathematical Formulation & Algorithm Spec
    draw.rounded_rectangle([120, 300, 980, 480], radius=16, fill=(16, 22, 34), outline=(0, 210, 255, 80), width=1)
    draw.rounded_rectangle([150, 324, 260, 350], radius=4, fill=(0, 210, 255, 30))
    draw.text((158, 328), "MATHEMATICAL FORMULA", font=get_font(10.5, 'bold'), fill=(0, 210, 255))
    
    # Closed Form Formula
    draw.text((150, 368), "Q_add  =  Q_0  ×  ( P_0 - P_target )  /  ( P_target - P_add )", font=get_num_font(23, 'bold'), fill=(255, 255, 255))
    draw.text((150, 420), "• Q_0: 현재 보유 수량   • P_0: 현재 평균 단가\n• P_target: 희망 목표 평단   • P_add: 추가 매수 희망가 (현재가)", font=get_font(13, 'regular'), fill=(148, 163, 184), spacing=4)
    
    quant_cards = [
        ("수학적 경계 조건 방어 (Boundary Defense)", "P_add < P_target < P_0 조건 위반 시 즉시 에러 토스트를 호출하고,\n현재 투입 가능한 현실적 목표 평단가를 역으로 실시간 제안합니다.", (0, 114, 255)),
        ("가용 예수금 인터랙티브 제약 슬라이더", "총알(예수금)이 부족한 투자자를 위해 보유 현금 한도 내에서\n도달 가능한 최선의 방어 평단을 슬라이더로 60fps 즉각 피드백합니다.", (16, 185, 129))
    ]
    
    qy = 505
    for title, desc, col in quant_cards:
        draw.rounded_rectangle([120, qy, 980, qy + 115], radius=16, fill=(16, 22, 34), outline=(255, 255, 255, 20), width=1)
        draw.rounded_rectangle([120, qy + 16, 124, qy + 99], radius=2, fill=col)
        draw.text((150, qy + 22), title, font=get_font(17, 'bold'), fill=(255, 255, 255))
        draw.text((150, qy + 58), desc, font=get_font(13.5, 'regular'), fill=(148, 163, 184), spacing=3)
        qy += 135
        
    # Right: Phone Mockup
    phone = Image.open('portfolio/mockup_ko_03_target_filled.png').convert('RGBA')
    pw = 385
    ph = int(phone.height * (pw / phone.width))
    phone = phone.resize((pw, ph), Image.Resampling.LANCZOS)
    
    sh = Image.new('RGBA', (W, H), (0,0,0,0))
    shd = ImageDraw.Draw(sh)
    shd.ellipse([1240, 950, 1240 + pw, 1030], fill=(0, 0, 0, 255))
    sh = sh.filter(ImageFilter.GaussianBlur(32))
    base = Image.alpha_composite(base, sh)
    base.paste(phone, (1240, 100), phone)
    
    # Highlight Floating Card
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle([1060, 680, 1540, 830], radius=16, fill=(9, 13, 22, 250), outline=(0, 210, 255, 160), width=2)
    draw.text((1090, 705), "수학적 목표 도달 수량 산출 완료", font=get_font(13.5, 'bold'), fill=(0, 210, 255))
    draw.text((1090, 735), "+42.5주 추가 매수 필요", font=get_num_font(30, 'black'), fill=(255, 255, 255))
    draw.text((1090, 782), "총 투입 필요 예수금: ₩ 2,125,000", font=get_font(15, 'regular'), fill=(180, 215, 220))
    
    base.save(f'{OUT_DIR}/slide_09.png')
    print("SAVED slide_09.png")

# ==============================================================
# SLIDE 10: High-Fidelity 6 Screens Showcase (Studio Showcase)
# ==============================================================
def make_slide_10():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    draw.line([(120, 100), (1800, 100)], fill=(226, 232, 240), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(226, 232, 240), width=1)
    
    draw.text((120, 130), "09  /  HIGH-FIDELITY SCREENS & PROTOTYPE FLOW", font=get_font(13, 'bold'), fill=(0, 87, 255))
    draw.text((120, 165), "6개 핵심 모바일 인터페이스 쇼케이스 및 상호작용 연결", font=get_font(52, 'black'), fill=(15, 23, 42))
    draw.text((120, 240), "홈 대시보드 · 시뮬레이터 · 목표 역산 · 진단 리포트 · OLED 다크모드 · 환경설정 유기적 흐름", font=get_font(18, 'regular'), fill=(100, 116, 139))
    
    mockup_files = [
        ('portfolio/mockup_ko_01_home.png', '01. 홈 대시보드'),
        ('portfolio/mockup_ko_02_sim.png', '02. 물타기 시뮬레이터'),
        ('portfolio/mockup_ko_03_target_filled.png', '03. 목표 역산 엔진'),
        ('portfolio/mockup_clean_report_filled.png', '04. 분석 리포트'),
        ('portfolio/mockup_dark_home_flawless.png', '05. OLED 야간 다크 홈'),
        ('portfolio/mockup_dark_settings_perfect.png', '06. 글로벌 환경설정')
    ]
    
    px = 120
    pw = 244
    pgap = 43
    phone_y = 295
    
    for img_path, ctitle in mockup_files:
        phone = Image.open(img_path).convert('RGBA')
        ph = int(round(phone.height * (pw / phone.width)))
        phone = phone.resize((pw, ph), Image.Resampling.LANCZOS)
        
        # Soft Drop Shadow directly under phone chin
        sh = Image.new('RGBA', (W, H), (0,0,0,0))
        shd = ImageDraw.Draw(sh)
        shd.ellipse([px - 4, phone_y + ph - 16, px + pw + 4, phone_y + ph + 24], fill=(0, 0, 0, 140))
        sh = sh.filter(ImageFilter.GaussianBlur(16))
        base = Image.alpha_composite(base, sh)
        base.paste(phone, (px, phone_y), phone)
        
        draw = ImageDraw.Draw(base)
        tw = draw.textlength(ctitle, font=get_font(12.5, 'bold'))
        pill_w = int(tw + 32)
        pill_x = px + (pw - pill_w) // 2
        pill_y = phone_y + ph + 24
        draw.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + 36], radius=8, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw.text((pill_x + 16, pill_y + 9), ctitle, font=get_font(12.5, 'bold'), fill=(15, 23, 42))
        px += pw + pgap
        
    base.save(f'{OUT_DIR}/slide_10.png')
    print("SAVED slide_10.png")

# ==============================================================
# SLIDE 11: OLED Deep Dark Theme & Accessibility (Pitch Black)
# ==============================================================
def make_slide_11():
    base = Image.new('RGBA', (W, H), (5, 7, 11, 255))
    
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([800, 200, 1700, 950], fill=(0, 87, 255, 45))
    glow = glow.filter(ImageFilter.GaussianBlur(140))
    base = Image.alpha_composite(base, glow)
    draw = ImageDraw.Draw(base)
    
    draw.line([(120, 100), (1800, 100)], fill=(255, 255, 255, 20), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(255, 255, 255, 20), width=1)
    
    # Phone on left
    phone = Image.open('portfolio/mockup_dark_home_flawless.png').convert('RGBA')
    pw = 385
    ph = int(round(phone.height * (pw / phone.width)))
    phone = phone.resize((pw, ph), Image.Resampling.LANCZOS)
    
    sh = Image.new('RGBA', (W, H), (0,0,0,0))
    shd = ImageDraw.Draw(sh)
    shd.ellipse([180, 950, 180 + pw, 1030], fill=(0, 0, 0, 255))
    sh = sh.filter(ImageFilter.GaussianBlur(32))
    base = Image.alpha_composite(base, sh)
    base.paste(phone, (180, 100), phone)
    
    draw = ImageDraw.Draw(base)
    
    # Right Column Content
    tx = 740
    draw.text((tx, 140), "10  /  OLED DEEP DARK & ACCESSIBILITY", font=get_font(13, 'bold'), fill=(0, 210, 255))
    draw.text((tx, 180), "야간 장세 트레이더를 위한\n초고대비 OLED 다크 테마 시스템", font=get_font(52, 'black'), fill=(255, 255, 255), spacing=18)
    draw.text((tx, 340), "Designed for night trading volatility\n7:1 이상의 WCAG 2.1 AAA 명도 대비를 엄격히 준수하여\n급박한 야간 해외주식·가상자산 장세에서도 오독 없는 수치 가독성 보장", font=get_font(18, 'regular'), fill=(148, 163, 184), spacing=8)
    
    specs = [
        ("시맨틱 컬러 토큰 매핑", "Primary Electric (#0057FF), Mint (#00E676), Coral (#FF5252), Gold (#FFB300)", (0, 87, 255)),
        ("Tabular Numbers 고정폭 폰트", "JetBrains Mono / Segoe UI의 'tnum' 속성을 적용하여 실시간 가격 변동 시 레이아웃 무흔들림", (0, 210, 255)),
        ("24시간 VIP 광고 제어 모델", "보상형 동영상 1회 시청 시 24시간 동안 배너 및 전면 광고 100% 완전 제거", (255, 179, 0))
    ]
    
    sy = 470
    for title, desc, col in specs:
        draw.rounded_rectangle([tx, sy, 1800, sy + 130], radius=16, fill=(16, 22, 34), outline=(255, 255, 255, 20), width=1)
        draw.rounded_rectangle([tx, sy + 16, tx + 4, sy + 114], radius=2, fill=col)
        draw.text((tx + 30, sy + 24), title, font=get_font(18, 'bold'), fill=(255, 255, 255))
        draw.text((tx + 30, sy + 64), desc, font=get_font(14, 'regular'), fill=(148, 163, 184))
        sy += 160
        
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
    
    draw.text((120, 130), "11  /  BUSINESS IMPACT & RETROSPECTIVE", font=get_font(13, 'bold'), fill=(0, 210, 255))
    draw.text((120, 165), "정량적 비즈니스 성과 및 STAR 회고", font=get_font(52, 'black'), fill=(255, 255, 255))
    
    metrics = [
        ("0.2s", "STT 음성 수치 파싱 속도", "키보드 타이핑 대비 입력 소요 시간 78% 단축"),
        ("100%", "Goal Seeking 수학적 정밀도", "부동소수점 오차 제로화 및 정밀 역산 도출"),
        ("60fps", "실시간 슬라이더 반응성", "RepaintBoundary 최적화로 버벅임 없는 즉각 반응")
    ]
    mx = 120
    mw = 533
    mgap = 40
    for val, title, desc in metrics:
        draw.rounded_rectangle([mx, 245, mx + mw, 375], radius=16, fill=(16, 22, 34), outline=(255, 255, 255, 20), width=1)
        draw.text((mx + 28, 260), val, font=get_num_font(46, 'black'), fill=(0, 210, 255))
        draw.text((mx + 28, 314), title, font=get_font(17, 'bold'), fill=(255, 255, 255))
        draw.text((mx + 28, 342), desc, font=get_font(13, 'regular'), fill=(148, 163, 184))
        mx += mw + mgap
        
    star_items = [
        ("Situation (상황)", "급격한 주가 하락 시 모바일 환경에서 분할 매수 단가 및 필요 수량을 계산하려는 투자자들의 긴박한 상황 발생. 기존 계산기는 타이핑 피로도가 높고 목표 평단가 도달에 필요한 수량을 역산해주지 못함.", (255, 107, 107)),
        ("Task (과제)", "1) 음성으로 0.2초 만에 단가/수량을 자동 파싱하는 무입력 경험 구축\n2) 목표 평단 입력 시 필요 추가 매수량을 즉각 도출하는 역산 알고리즘 탑재\n3) 오프라인 환경에서도 100% 안전하게 시나리오를 보관하는 Local-First 아키텍처 구현", (255, 193, 7)),
        ("Action (행동)", "STT 스트림 음성 데이터에서 정규식 기반 수치 추출 파이프라인 개발. Goal Seeking Closed Form 수학 공식을 코어로 구현하고, Flutter Hive NoSQL로 0ms 레이턴시 로컬 캐싱 구조 설계. WCAG 2.1 AAA 다크모드 시스템 완성.", (33, 150, 243)),
        ("Result (결과)", "복합 시뮬레이션 계산 소요 시간을 기존 2분에서 5초 이내로 단축. Google Play Console 프로덕션 심사 규격 100% 충족 및 24시간 보상형 무광고 모델을 통해 사용자 잔존율(Retention) 극대화.", (76, 175, 80))
    ]
    
    sx = 120
    sw = 395
    sgap = 33
    f_body = get_font(13.5, 'regular')
    for phase, content, color in star_items:
        draw.rounded_rectangle([sx, 410, sx + sw, 940], radius=16, fill=(16, 22, 34), outline=(255, 255, 255, 20), width=1)
        draw.rounded_rectangle([sx + 18, 428, sx + sw - 18, 468], radius=8, fill=color)
        draw.text((sx + 30, 438), phase, font=get_font(14.5, 'bold'), fill=(255, 255, 255))
        
        wrapped_lines = wrap_text_by_words(content, f_body, sw - 50, draw)
        text_y = 490
        for line in wrapped_lines:
            draw.text((sx + 24, text_y), line, font=f_body, fill=(203, 213, 225))
            text_y += 26
        sx += sw + sgap
        
    base.save(f'{OUT_DIR}/slide_12.png')
    print("SAVED slide_12.png")

if __name__ == '__main__':
    for i in range(1, 13):
        func_name = f'make_slide_{i:02d}'
        if func_name in globals():
            globals()[func_name]()
    print("ALL 12 SLIDES GENERATED WITH MASCULINE EDITORIAL AESTHETIC!")
