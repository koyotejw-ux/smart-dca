import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
CARD_PAD = 36
RADIUS = 44

os.makedirs('portfolio/behance_slides', exist_ok=True)

# ==============================================================
# SAMSUNG-GRADE TYPOGRAPHY ENGINE (Pretendard Family)
# ==============================================================
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
    if isinstance(weight, bool):
        w_name = 'bold' if weight else 'regular'
    else:
        w_name = str(weight).lower()
        
    font_file = WEIGHT_MAP.get(w_name, 'Pretendard-Regular.ttf')
    font_path = os.path.join(FONT_DIR, font_file)
    try:
        return ImageFont.truetype(font_path, int(round(size)))
    except:
        return ImageFont.load_default()

def get_num_font(size, weight='black'):
    # Pretendard has native tabular numbers and clean DIN-like glyphs!
    return get_font(size, weight)

def create_card_canvas(bg_color):
    base = Image.new('RGBA', (W, H), (241, 244, 249, 255))
    mask = Image.new('L', (W, H), 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.rounded_rectangle([CARD_PAD, CARD_PAD, W - CARD_PAD, H - CARD_PAD], radius=RADIUS, fill=255)
    
    card = Image.new('RGBA', (W, H), bg_color)
    base.paste(card, (0, 0), mask)
    return base, mask

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
# SLIDE 01: Hero Cover & Value Proposition (Samsung Unpack Style)
# ==============================================================
def make_slide_01():
    base, mask = create_card_canvas((10, 18, 45, 255))
    
    # Deep Samsung Cosmic Blue Gradient
    grad = Image.new('RGBA', (W, H), (0,0,0,0))
    g_draw = ImageDraw.Draw(grad)
    for y in range(H):
        ratio = y / H
        r = int(10 * (1 - ratio) + 6 * ratio)
        g = int(28 * (1 - ratio) + 14 * ratio)
        b = int(75 * (1 - ratio) + 40 * ratio)
        g_draw.line([(0, y), (W, y)], fill=(r, g, b, 255))
    
    # Ambient Electric Glows
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([1000, 30, 1880, 960], fill=(0, 114, 255, 90))
    gw.ellipse([260, 480, 1100, 1200], fill=(100, 30, 240, 65))
    gw.ellipse([1350, 580, 1860, 1120], fill=(0, 210, 255, 60))
    glow = glow.filter(ImageFilter.GaussianBlur(110))
    grad = Image.alpha_composite(grad, glow)
    base.paste(grad, (0, 0), mask)
    
    # Dual Flagship Mockups (100% Uniform Native Aspect Ratio)
    phone_back = Image.open('portfolio/mockup_ko_02_sim.png').convert('RGBA')
    pb_w = 370
    pb_h = int(phone_back.height * (pb_w / phone_back.width))
    phone_back = phone_back.resize((pb_w, pb_h), Image.Resampling.LANCZOS)
    
    phone_front = Image.open('portfolio/mockup_ko_01_home.png').convert('RGBA')
    pf_w = 400
    pf_h = int(phone_front.height * (pf_w / phone_front.width))
    phone_front = phone_front.resize((pf_w, pf_h), Image.Resampling.LANCZOS)
    
    sh = Image.new('RGBA', (W, H), (0,0,0,0))
    shd = ImageDraw.Draw(sh)
    shd.ellipse([1270, 960, 1660, 1050], fill=(0, 0, 0, 190))
    shd.ellipse([990, 990, 1410, 1080], fill=(0, 0, 0, 240))
    sh = sh.filter(ImageFilter.GaussianBlur(35))
    base = Image.alpha_composite(base, sh)
    
    base.paste(phone_back, (1270, 80), phone_back)
    base.paste(phone_front, (990, 45), phone_front)
    
    # 3D Squircle Icon with Ambient Lighting
    icon = Image.open('assets/app_icon_clean_squircle.png').convert('RGBA')
    icon = icon.resize((230, 230), Image.Resampling.LANCZOS)
    ish = Image.new('RGBA', (W, H), (0,0,0,0))
    ishd = ImageDraw.Draw(ish)
    ishd.ellipse([1480, 720, 1730, 830], fill=(0, 0, 0, 180))
    ish = ish.filter(ImageFilter.GaussianBlur(28))
    base = Image.alpha_composite(base, ish)
    base.paste(icon, (1490, 520), icon)
    
    overlay = Image.new('RGBA', (W, H), (0,0,0,0))
    d_ov = ImageDraw.Draw(overlay)
    
    # Micro Tracking Category Label (Samsung Style)
    d_ov.text((140, 175), "SMART DCA CALCULATOR  ·  ENTERPRISE UX CASE STUDY", font=get_font(13.5, 'semibold'), fill=(0, 210, 255))
    
    # Ultra-Bold Modern Headline
    f_title = get_font(54, 'black')
    d_ov.text((140, 235), "하락장 속 뇌동매매를 막는\n알고리즘 분할매수 솔루션", font=f_title, fill=(255, 255, 255), spacing=14)
    
    # Clean Breathing Subtitle
    f_sub = get_font(20, 'regular')
    d_ov.text((140, 410), "Stop Panic Selling. Start Algorithmic Scaling.\n0.2초 음성 인식과 Goal Seeking 수학 역산으로 계좌 손실을 정밀 방어합니다.", font=f_sub, fill=(203, 213, 225), spacing=10)
    
    # 3 Minimalist Glass Cards with High Contrast Numbers
    metrics = [
        ("0.2s", "STT 음성 인제스천", "호가 급락 시 1초 음성으로 매수 단가·수량 즉시 파싱"),
        ("100%", "Goal Seeking 수학 역산", "희망 목표 평단가 도달 필수 추가 매수량 폐쇄형 산출"),
        ("24h", "VIP 무광고 라이프사이클", "보상형 광고 1회 시청 시 24시간 동안 배너 및 전면 광고 100% 제거")
    ]
    cy = 555
    for val, title, desc in metrics:
        d_ov.rounded_rectangle([140, cy, 840, cy + 96], radius=20, fill=(255, 255, 255, 245), outline=(255, 255, 255, 255), width=1)
        d_ov.rounded_rectangle([140, cy + 20, 146, cy + 76], radius=3, fill=(0, 87, 255))
        d_ov.text((172, cy + 22), val, font=get_num_font(38, 'black'), fill=(0, 87, 255))
        d_ov.text((305, cy + 24), title, font=get_font(17.5, 'bold'), fill=(15, 23, 42))
        d_ov.text((305, cy + 54), desc, font=get_font(13.5, 'regular'), fill=(100, 116, 139))
        cy += 112
        
    d_ov.text((140, 930), "Lead Product Designer & Senior Flutter Engineer  ·  Production Store Verified", font=get_font(15, 'semibold'), fill=(148, 163, 184))
    
    base = Image.alpha_composite(base, overlay)
    base.save('portfolio/behance_slides/slide_01.png')
    print("SAVED slide_01.png")

# ==============================================================
# SLIDE 02: Discovery & User Research (Pain Points + IDI Data)
# ==============================================================
def make_slide_02():
    base, mask = create_card_canvas((248, 250, 254, 255))
    draw = ImageDraw.Draw(base)
    
    draw.text((140, 95), "01  /  DISCOVERY & USER RESEARCH", font=get_font(14, 'semibold'), fill=(0, 87, 255))
    draw.text((140, 130), "손실 회피 편향과 감정적 물타기의 한계", font=get_font(46, 'black'), fill=(15, 23, 42))
    draw.text((140, 196), "개인 투자자 12명 심층 인터뷰(IDI) 및 커뮤니티 데이터 분석을 통해 도출한 3대 핵심 결핍", font=get_font(19, 'regular'), fill=(100, 116, 139))
    
    # Left 3 Stat Boxes with Bold Display Numbers
    stats = [
        ("78.4%", "하락장 뇌동매매 경험률", "수학적 계획 없는 감정적 추가 매수 집행", 0.784, (239, 68, 68)),
        ("4.8분", "기존 계산기 수동 입력 소요", "소수점 단가·수량 타이핑 중 호가 급변", 0.65, (245, 158, 11)),
        ("0건", "MTS 내 목표 역산 기능 부재", "본전 탈출 필요 수량을 알지 못한 채 과매수", 0.0, (0, 87, 255))
    ]
    sx = 140
    sy = 265
    sw = 460
    for val, stitle, sdesc, prog, pcol in stats:
        draw.rounded_rectangle([sx, sy, sx + sw, sy + 195], radius=20, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        
        num_str = "".join([c for c in val if c.isdigit() or c in ['.', '%', '+', '-']])
        unit_str = val.replace(num_str, "")
        draw.text((sx + 32, sy + 28), num_str, font=get_num_font(48, 'black'), fill=pcol)
        nw = draw.textlength(num_str, font=get_num_font(48, 'black'))
        if unit_str:
            draw.text((sx + 32 + nw + 4, sy + 44), unit_str, font=get_font(24, 'bold'), fill=pcol)
            
        draw.text((sx + 32, sy + 115), stitle, font=get_font(17.5, 'bold'), fill=(15, 23, 42))
        draw.text((sx + 32, sy + 145), sdesc, font=get_font(13.5, 'regular'), fill=(100, 116, 139))
        
        if prog > 0:
            draw.rounded_rectangle([sx + 32, sy + 95, sx + sw - 32, sy + 100], radius=3, fill=(241, 245, 249))
            draw.rounded_rectangle([sx + 32, sy + 95, sx + 32 + int((sw - 64) * prog), sy + 100], radius=3, fill=pcol)
            
        sy += 225
        
    cards = [
        ("01", "전략 부재", "비중만 비대해지고 평단은 거의 내려오지 않음",
         "\"단가를 낮추려고 예수금을 계속 넣었는데, 나중에 보니 계좌의 80%가 한 종목에 묶여있고 평단은 2%밖에 안 내려왔어요.\"\n— 3년 차 개인 투자자 IDI 인터뷰",
         "추가 매수 차수별 한계 효용 및 계좌 잠식 위험도 실시간 가시화", (239, 68, 68)),
        
        ("02", "조작 지연", "급변하는 호가창 앞에서 타이핑하다 골든타임 상실",
         "\"급락 빔이 쏟아질 때 평단 계산하려고 키패드로 8자리 단가를 치는 동안 이미 반등해버리거나 더 밑으로 뚫려버립니다.\"\n— 가상자산/단타 트레이더 IDI 인터뷰",
         "0.2초 STT 음성 자동 파싱 및 ±5% 원터치 프리셋 칩 즉각 주입", (245, 158, 11)),
         
        ("03", "출구 전략 부재", "목표 탈출가에 도달하기 위한 필요 매수량 미제공",
         "\"본전이나 -5% 선에서 정리하고 싶은데, 지금 얼마를 더 사야 그 평단이 만들어지는지 알려주는 앱이 전혀 없습니다.\"\n— 5년 차 직장인 스윙 투자자 IDI 인터뷰",
         "Goal Seeking Closed Form 수학 공식을 통한 목표 도달 수량 정밀 역산", (0, 87, 255))
    ]
    
    rx = 640
    ry = 265
    rw = 1140
    for num, ptag, ptitle, pquote, psol, pcolor in cards:
        draw.rounded_rectangle([rx, ry, rx + rw, ry + 195], radius=20, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw.rounded_rectangle([rx, ry + 20, rx + 5, ry + 175], radius=3, fill=pcolor)
        
        draw.text((rx + 32, ry + 22), num, font=get_num_font(20, 'black'), fill=pcolor)
        draw.text((rx + 72, ry + 24), ptag + " : " + ptitle, font=get_font(18, 'bold'), fill=(15, 23, 42))
        
        # Quote Box with Generous Margins
        draw.rounded_rectangle([rx + 32, ry + 62, rx + rw - 32, ry + 130], radius=10, fill=(248, 250, 252))
        lines = wrap_text_by_words(pquote, get_font(13.5, 'regular'), rw - 95, draw)
        qy = ry + 72
        for line in lines[:2]:
            draw.text((rx + 48, qy), line, font=get_font(13.5, 'regular'), fill=(71, 85, 105))
            qy += 22
            
        # Solution Line with High Contrast
        draw.text((rx + 32, ry + 148), "SOLUTION", font=get_font(12, 'black'), fill=(0, 87, 255))
        draw.text((rx + 115, ry + 147), psol, font=get_font(14, 'semibold'), fill=(30, 41, 59))
        ry += 225
        
    base.save('portfolio/behance_slides/slide_02.png')
    print("SAVED slide_02.png")

# ==============================================================
# SLIDE 03: Benchmark Matrix & Personas (Samsung Clean Grid)
# ==============================================================
def make_slide_03():
    base, mask = create_card_canvas((248, 250, 254, 255))
    draw = ImageDraw.Draw(base)
    
    draw.text((140, 95), "02  /  BENCHMARK & TARGET PERSONAS", font=get_font(14, 'semibold'), fill=(0, 87, 255))
    draw.text((140, 130), "경쟁사 벤치마킹 매트릭스 및 핵심 페르소나 정의", font=get_font(46, 'black'), fill=(15, 23, 42))
    draw.text((140, 196), "기존 MTS 및 일반 계산기 앱 대비 독보적인 사용자 편의성과 알고리즘 기능 우위", font=get_font(19, 'regular'), fill=(100, 116, 139))
    
    tx = 140
    ty = 265
    tw = 960
    draw.rounded_rectangle([tx, ty, tx + tw, ty + 655], radius=20, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    draw.rounded_rectangle([tx, ty, tx + tw, ty + 62], radius=20, fill=(241, 245, 249))
    draw.text((tx + 28, ty + 20), "비교 분석 항목", font=get_font(15, 'bold'), fill=(71, 85, 105))
    draw.text((tx + 195, ty + 20), "증권사 MTS 내장", font=get_font(15, 'bold'), fill=(71, 85, 105))
    draw.text((tx + 405, ty + 20), "일반 앱스토어 계산기", font=get_font(15, 'bold'), fill=(71, 85, 105))
    
    col4_left = tx + 620
    col4_right = tx + tw - 12
    draw.rounded_rectangle([col4_left, ty + 8, col4_right, ty + 647], radius=16, fill=(240, 246, 255), outline=(186, 215, 255), width=2)
    draw.rounded_rectangle([col4_left + 15, ty + 14, col4_right - 15, ty + 54], radius=10, fill=(0, 87, 255))
    draw.text((col4_left + 45, ty + 22), "스마트 물타기 계산기", font=get_font(14, 'bold'), fill=(255, 255, 255))
    
    matrix = [
        ("입력 방식", "키패드 수동 입력 (느림)", "키패드 수동 입력 (광고 다수)", "멀티모달 (AI 음성 + 원터치 칩)"),
        ("연산 속도", "3~5초 (복잡한 메뉴 이동)", "2~3초 (단순 합산)", "0.2초 즉시 파싱 및 자동 연산"),
        ("시나리오 비교", "불가능 (단일 계산)", "불가능 (1회성 소멸)", "A vs B 전략 대조 매트릭스"),
        ("목표가 역산", "미지원", "미지원", "Goal Seeking 폐쇄형 역산 알고리즘"),
        ("보안/저장", "동작 로그인 필수 (지연)", "세션 종료 시 초기화", "Local-First NoSQL 100% 영속화"),
        ("광고 모델", "금융 상품 배너 혼재", "전면 강제 팝업 (피로도 극심)", "24시간 VIP 무광고 라이프사이클"),
        ("다크 테마", "일부 지원 (가독성 낮음)", "단순 그레이스케일 반전", "OLED 고대비 WCAG AAA 토큰")
    ]
    
    row_y = ty + 72
    for item, c1, c2, c3 in matrix:
        draw.line([(tx + 20, row_y), (col4_left - 15, row_y)], fill=(241, 245, 249), width=1)
        draw.text((tx + 28, row_y + 20), item, font=get_font(14.5, 'bold'), fill=(15, 23, 42))
        draw.text((tx + 195, row_y + 20), c1, font=get_font(13.5, 'regular'), fill=(100, 116, 139))
        draw.text((tx + 405, row_y + 20), c2, font=get_font(13.5, 'regular'), fill=(100, 116, 139))
        
        draw.ellipse([col4_left + 16, row_y + 24, col4_left + 24, row_y + 32], fill=(0, 87, 255))
        draw.text((col4_left + 32, row_y + 19), c3, font=get_font(13, 'bold'), fill=(0, 87, 255))
        row_y += 81
        
    px = 1140
    py = 265
    pw = 640
    
    # Persona A
    draw.rounded_rectangle([px, py, px + pw, py + 312], radius=20, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([px + 30, py + 24, px + 145, py + 54], radius=8, fill=(240, 246, 255))
    draw.text((px + 45, py + 30), "PERSONA A", font=get_font(12, 'bold'), fill=(0, 87, 255))
    draw.text((px + 165, py + 26), "김투자 (34세, 대기업 직장인)", font=get_font(20, 'bold'), fill=(15, 23, 42))
    
    draw.text((px + 30, py + 78), "\"월급날마다 분할 매수해서 6개월 안에 본전 탈출하고 싶어요.\"", font=get_font(16, 'semibold'), fill=(0, 87, 255))
    desc_a = [
        "• 성향: 국내 대형 우량주 및 미국 지수 ETF 장기 분할 투자",
        "• 행동: 업무 중 급락 알림을 볼 때 감정적 추매를 지양하고 체계적 대응 시도",
        "• 핵심 니즈: 총예산 대비 특정 종목 편중 비율 및 A/B 시나리오 평단 만족도 대조"
    ]
    dy = py + 125
    for d in desc_a:
        draw.text((px + 30, dy), d, font=get_font(14, 'regular'), fill=(71, 85, 105))
        dy += 34
        
    # Persona B
    py += 342
    draw.rounded_rectangle([px, py, px + pw, py + 312], radius=20, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([px + 30, py + 24, px + 145, py + 54], radius=8, fill=(254, 243, 199))
    draw.text((px + 45, py + 30), "PERSONA B", font=get_font(12, 'bold'), fill=(217, 119, 6))
    draw.text((px + 165, py + 26), "박스캘퍼 (28세, 크립토/단타 트레이더)", font=get_font(20, 'bold'), fill=(15, 23, 42))
    
    draw.text((px + 30, py + 78), "\"급락 빔 맞았을 때 3초 안에 평단 뽑아서 지지선에서 나와야 해요.\"", font=get_font(16, 'semibold'), fill=(217, 119, 6))
    desc_b = [
        "• 성향: 고변동성 알트코인 및 테마주 단타/스캘핑 매매",
        "• 행동: 손가락으로 타이핑할 시간이 없어 음성으로 단가/수량을 즉각 주입",
        "• 핵심 니즈: 목표 탈출 가격에 도달하기 위한 필요 매수 수량을 0.01초 만에 역산"
    ]
    dy = py + 125
    for d in desc_b:
        draw.text((px + 30, dy), d, font=get_font(14, 'regular'), fill=(71, 85, 105))
        dy += 34
        
    base.save('portfolio/behance_slides/slide_03.png')
    print("SAVED slide_03.png")

# ==============================================================
# SLIDE 04: Information Architecture & Customer Journey (CJM)
# ==============================================================
def make_slide_04():
    base, mask = create_card_canvas((15, 23, 42, 255))
    draw = ImageDraw.Draw(base)
    
    # Header
    draw.text((140, 95), "03  /  INFORMATION ARCHITECTURE & CUSTOMER JOURNEY (CJM)", font=get_font(14, 'semibold'), fill=(0, 210, 255))
    draw.text((140, 130), "5대 핵심 도메인 정보 구조(IA) & 고객 여정 지도", font=get_font(46, 'black'), fill=(255, 255, 255))
    draw.text((140, 196), "급락 인지부터 0.2초 음성 인제스천, 알고리즘 시뮬레이션, 포트폴리오 안전 진단 및 로컬 영속화까지의 완결형 아키텍처", font=get_font(18, 'regular'), fill=(148, 163, 184))
    
    # Top: 5-Stage Customer Journey Map (CJM)
    cjm_stages = [
        ("Phase 1. 급락 인지", "Crisis Awareness", "보유 종목 급락 (-10%)\n손실 공포 & 뇌동매매 충동", "냉정 회복 & 원클릭 실행", (0, 114, 255)),
        ("Phase 2. 초신속 인제스천", "Zero-Friction Ingest", "호가 급변 중 타이핑 지연\n매수 골든타임 상실 위기", "0.2s 음성 STT & 호가 칩", (0, 210, 255)),
        ("Phase 3. 알고리즘 시뮬", "Algorithmic Sim", "추가 매수 시 평단 방어율 &\n필요 자금 불확실성", "가중평균 + A/B + 역산", (139, 92, 246)),
        ("Phase 4. 포트폴리오 진단", "Portfolio Diagnostics", "특정 종목 과매수로 인한\n계좌 잠식 & 비중 왜곡", "3단계 시급도 & 도넛 차트", (245, 158, 11)),
        ("Phase 5. 확신 영속화", "Persistence & Execute", "과거 시뮬레이션 소실 &\n실매매 집행 불안감", "Local DB 암호화 & 진단 공유", (16, 185, 129))
    ]
    
    jx = 140
    jw = 310
    jgap = 22
    for p_title, p_sub, p_desc, p_sol, p_col in cjm_stages:
        draw.rounded_rectangle([jx, 252, jx + jw, 360], radius=16, fill=(24, 32, 48), outline=(p_col[0], p_col[1], p_col[2], 120), width=2)
        draw.rounded_rectangle([jx + 14, 266, jx + 19, 346], radius=2, fill=p_col)
        draw.text((jx + 28, 264), p_title, font=get_font(15, 'bold'), fill=p_col)
        draw.text((jx + 28, 285), p_sub, font=get_font(11.5, 'semibold'), fill=(148, 163, 184))
        draw.text((jx + 28, 305), p_desc, font=get_font(12, 'regular'), fill=(203, 213, 225), spacing=2)
        
        # Pill solution
        draw.rounded_rectangle([jx + 28, 335, jx + jw - 14, 353], radius=6, fill=(p_col[0], p_col[1], p_col[2], 40))
        draw.text((jx + 34, 338), "SOL: " + p_sol, font=get_font(11, 'bold'), fill=p_col)
        jx += jw + jgap
        
    # Bottom: 5-Domain Hierarchical IA Tree
    domains = [
        ("01. ENTRY & INIT", "온보딩 및 초기화", [
            ("1.1 Splash Engine", "로고 모션 & 24h VIP 토큰 즉시 검증"),
            ("1.2 4-Step Guide", "분할 매수 메커니즘 & 역산 원리 학습"),
            ("1.3 Local DB Engine", "SQLite & Hive NoSQL 로컬 암호화"),
            ("1.4 Auto L10n Engine", "디바이스 언어(7국) 및 통화(4종) 연동")
        ], (0, 114, 255)),
        
        ("02. SMART DASHBOARD", "홈 대시보드", [
            ("2.1 Portfolio Hero", "총 평가액, 평균 수익률, 위험도 시각화"),
            ("2.2 24h VIP Banner", "보상형 광고 시청 잔여시간 카운트다운"),
            ("2.3 Multimodal Dock", "Google STT 온디바이스 마이크 & 호가 칩"),
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
            ("4.2 3-Tier Urgency", "안전 / 주의 / 위험 3단계 시급도"),
            ("4.3 Scenario Manager", "저장된 시뮬레이션 기록 로드/편집/CSV"),
            ("4.4 Diagnostic Export", "PNG 리포트 카드 원클릭 클립보드 공유")
        ], (245, 158, 11)),
        
        ("05. GLOBAL GOVERNANCE", "글로벌 설정 & 규정", [
            ("5.1 7-Language L10n", "한국어, 영어, 일본어, 중국어, 스페인어 등"),
            ("5.2 4-Currency System", "KRW(₩), USD($), JPY(¥), EUR(€) 환산"),
            ("5.3 OLED Dark System", "야간 트레이더 고대비 WCAG AAA 토큰"),
            ("5.4 Compliance & FAQ", "GDPR 준수 로컬 암호화 & 금융 가이드")
        ], (16, 185, 129))
    ]
    
    cx = 140
    cw = 310
    cgap = 22
    for d_code, d_name, items, d_col in domains:
        draw.rounded_rectangle([cx, 380, cx + cw, 940], radius=18, fill=(24, 32, 48), outline=(d_col[0], d_col[1], d_col[2], 120), width=2)
        
        # Domain Header Card
        draw.rounded_rectangle([cx + 14, 396, cx + cw - 14, 452], radius=12, fill=(15, 23, 42), outline=(d_col[0], d_col[1], d_col[2], 80), width=1)
        draw.text((cx + 26, 404), d_code, font=get_font(11.5, 'bold'), fill=d_col)
        draw.text((cx + 26, 424), d_name, font=get_font(15, 'bold'), fill=(255, 255, 255))
        
        iy = 468
        for ititle, idesc in items:
            draw.rounded_rectangle([cx + 14, iy, cx + cw - 14, iy + 104], radius=12, fill=(15, 23, 42), outline=(51, 65, 85), width=1)
            draw.ellipse([cx + 28, iy + 20, cx + 36, iy + 28], fill=d_col)
            draw.text((cx + 44, iy + 14), ititle, font=get_font(13.5, 'bold'), fill=(255, 255, 255))
            draw.text((cx + 26, iy + 44), idesc, font=get_font(12, 'regular'), fill=(148, 163, 184))
            iy += 114
            
        cx += cw + cgap
        
    base.save('portfolio/behance_slides/slide_04.png')
    print("SAVED slide_04.png")



# ==============================================================
# SLIDE 05: User Flowchart & Edge Case Logic Branch
# ==============================================================
def make_slide_05():
    base, mask = create_card_canvas((248, 250, 254, 255))
    draw = ImageDraw.Draw(base)
    
    # Header
    draw.text((140, 95), "04  /  USER FLOWCHART & LOGIC BRANCH", font=get_font(14, 'semibold'), fill=(0, 87, 255))
    draw.text((140, 130), "사용자 의사결정 경로 및 예외 방어 로직 플로우차트", font=get_font(46, 'black'), fill=(15, 23, 42))
    draw.text((140, 196), "앱 진입부터 STT 권한 거부, 역산 불가 엣지 케이스, VIP 광고 바이패스까지 실서비스 상태 전이 100% 매핑", font=get_font(18, 'regular'), fill=(100, 116, 139))
    
    # Main Canvas Card
    bx = 140
    by = 252
    bw = 1640
    bh = 698
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    stages = [
        ("STAGE 1 : 진입 & 분기", "Entry & Init", [
            ("Process", "앱 실행 (Splash Launch)", "앱 로고 모션 & 로컬 캐시 초기화", (0, 87, 255), False),
            ("Decision", "최초 실행 여부?", "First Run Check 분기", (217, 119, 6), True, [
                ("YES", "4단계 온보딩 가이드"),
                ("NO", "24h VIP 토큰 검사")
            ]),
            ("Process", "VIP 광고 바이패스", "무광고 시 전면/오픈 광고 100% 스킵", (16, 185, 129), False),
        ]),
        
        ("STAGE 2 : 멀티모달 인제스천", "Multimodal Ingest", [
            ("Process", "스마트 대시보드 진입", "포트폴리오 카드 & 2x2 액션 도크", (0, 87, 255), False),
            ("Decision", "입력 방식 선택?", "음성 STT vs 수동 키패드", (217, 119, 6), True, [
                ("STT", "마이크 탭 (Waveform 활성)"),
                ("Manual", "키패드 / 최근 자산 로드")
            ]),
            ("Process", "자연어 파싱 완료", "0.2s 단가·수량 분리 (실패 시 호가 칩)", (16, 185, 129), False),
        ]),
        
        ("STAGE 3 : 알고리즘 코어", "Simulation Core", [
            ("Process", "시뮬레이터 코어 화면", "단일 DCA / A-B 비교 / 목표 역산", (122, 34, 255), False),
            ("Decision", "목표가 유효성 검증?", "P_add < Target < P_0 여부 판정", (217, 119, 6), True, [
                ("불일치", "경고 토스트 & 달성가능 평단 추천"),
                ("정상", "Closed-Form Q_add 산출")
            ]),
            ("Process", "실시간 수식 연산", "가중평균 & 하락률 방어폭 계산", (16, 185, 129), False),
        ]),
        
        ("STAGE 4 : 포트폴리오 진단", "Portfolio Diagnostics", [
            ("Process", "실시간 결과 요약 카드", "신규 평단, 평단 인하폭, 필요 총자금", (0, 87, 255), False),
            ("Decision", "특정 종목 비중 > 50%?", "포트폴리오 편중 위험 진단", (217, 119, 6), True, [
                ("YES", "위험 배지 표시 & 분산 권고"),
                ("NO", "안전 포트폴리오 판정")
            ]),
            ("Process", "진단 리포트 생성", "도넛 차트 & 시나리오 분석 매트릭스", (16, 185, 129), False),
        ]),
        
        ("STAGE 5 : 영속화 & 완결", "Persistence & Decision", [
            ("Process", "진단 리포트 데이터 수신", "포트폴리오 및 시뮬레이션 완료 수치", (0, 87, 255), False),
            ("Decision", "시나리오 로컬 저장?", "Local-First NoSQL 영속화", (217, 119, 6), True, [
                ("저장", "SQLite / Hive 암호화 저장"),
                ("공유", "1-Click 진단 이미지 공유")
            ]),
            ("Complete", "의사결정 완결 & 24h VIP", "뇌동매매 방어 완료 & VIP 타이머 가동", (16, 185, 129), False),
        ])
    ]
    
    col_w = 295
    col_gap = 36
    cx = bx + 22
    
    # Coordinates:
    # Row 1 (Process): y = by + 74, height = 92
    # Arrow 1: y = by + 166 to by + 186
    # Row 2 (Decision Diamond): y = by + 188, height = 138
    # Arrow 2: y = by + 326 to by + 346
    # Row 3 (Resolution): y = by + 348, height = 92
    
    for s_idx, (s_title, s_sub, steps) in enumerate(stages):
        # Stage Header (Clean 2-line title)
        draw.rounded_rectangle([cx, by + 14, cx + col_w, by + 60], radius=10, fill=(241, 245, 249), outline=(226, 232, 240), width=1)
        draw.text((cx + 14, by + 20), s_sub.upper(), font=get_font(11, 'bold'), fill=(0, 87, 255))
        draw.text((cx + 14, by + 37), s_title.split(' : ')[-1], font=get_font(13.5, 'bold'), fill=(15, 23, 42))
        
        # Row 1: Process
        step1 = steps[0]
        y1 = by + 74
        h1 = 92
        draw.rounded_rectangle([cx, y1, cx + col_w, y1 + h1], radius=14, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.rounded_rectangle([cx + 14, y1 + 14, cx + 20, y1 + h1 - 14], radius=3, fill=step1[3])
        draw.text((cx + 30, y1 + 16), step1[1], font=get_font(14, 'bold'), fill=(15, 23, 42))
        draw.text((cx + 30, y1 + 44), step1[2], font=get_font(12, 'regular'), fill=(100, 116, 139))
        
        # Vertical Arrow 1
        draw.line([(cx + col_w // 2, y1 + h1), (cx + col_w // 2, y1 + h1 + 20)], fill=(148, 163, 184), width=2)
        draw.polygon([(cx + col_w // 2 - 4, y1 + h1 + 16), (cx + col_w // 2 + 4, y1 + h1 + 16), (cx + col_w // 2, y1 + h1 + 22)], fill=(148, 163, 184))
        
        # Row 2: Decision Diamond Card
        step2 = steps[1]
        y2 = y1 + h1 + 22
        h2 = 142
        draw.rounded_rectangle([cx, y2, cx + col_w, y2 + h2], radius=16, fill=(255, 251, 235), outline=(245, 158, 11), width=2)
        draw.rounded_rectangle([cx + 14, y2 + 14, cx + 80, y2 + 38], radius=6, fill=(254, 243, 199))
        draw.text((cx + 22, y2 + 18), "◆ DECIDE", font=get_font(10.5, 'bold'), fill=(180, 83, 9))
        draw.text((cx + 90, y2 + 17), step2[1], font=get_font(13, 'bold'), fill=(15, 23, 42))
        
        branches = step2[5]
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
        draw.line([(cx + col_w // 2, y2 + h2), (cx + col_w // 2, y2 + h2 + 20)], fill=(148, 163, 184), width=2)
        draw.polygon([(cx + col_w // 2 - 4, y2 + h2 + 16), (cx + col_w // 2 + 4, y2 + h2 + 16), (cx + col_w // 2, y2 + h2 + 22)], fill=(148, 163, 184))
        
        # Row 3: Resolution
        step3 = steps[2]
        y3 = y2 + h2 + 22
        h3 = 92
        draw.rounded_rectangle([cx, y3, cx + col_w, y3 + h3], radius=14, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.rounded_rectangle([cx + 14, y3 + 14, cx + 20, y3 + h3 - 14], radius=3, fill=step3[3])
        draw.text((cx + 30, y3 + 16), step3[1], font=get_font(14, 'bold'), fill=(15, 23, 42))
        draw.text((cx + 30, y3 + 44), step3[2], font=get_font(12, 'regular'), fill=(100, 116, 139))
        
        # Horizontal Connecting Arrow across Row 2 (Decisions)
        if s_idx < len(stages) - 1:
            ax = cx + col_w + 4
            ay = y2 + h2 // 2
            draw.line([(ax, ay), (ax + col_gap - 8, ay)], fill=(0, 87, 255), width=2)
            draw.polygon([(ax + col_gap - 10, ay - 4), (ax + col_gap - 10, ay + 4), (ax + col_gap - 4, ay)], fill=(0, 87, 255))
            
        cx += col_w + col_gap
        
    # Bottom Edge Defense Spec Bar
    draw.rounded_rectangle([bx + 20, by + bh - 94, bx + bw - 20, by + bh - 18], radius=14, fill=(240, 246, 255), outline=(186, 215, 255), width=1)
    draw.rounded_rectangle([bx + 34, by + bh - 82, bx + 165, by + bh - 54], radius=6, fill=(0, 87, 255))
    draw.text((bx + 44, by + bh - 76), "EDGE DEFENSE", font=get_font(11, 'bold'), fill=(255, 255, 255))
    
    defenses = [
        "1. STT 음성 예외 방어: 권한 거부 / 잡음 시 0초 딜레이로 원터치 호가 프리셋 칩(±5%, ±10%) 즉시 대체",
        "2. 수학적 오차 방어: 도달 불가 목표가(P_target <= P_add 또는 >= P_0) 입력 시 즉시 경고 토스트 & 달성 가능 목표 평단 자동 추천",
        "3. Local-First 영속화: 음영 지역 오프라인 환경에서도 Hive NoSQL 0ms 캐싱을 통해 시나리오 및 포트폴리오 데이터 유실 0% 보장"
    ]
    dy = by + bh - 78
    for df in defenses:
        draw.text((bx + 180, dy), "• " + df, font=get_font(12, 'semibold'), fill=(30, 41, 59))
        dy += 22
        
    base.save('portfolio/behance_slides/slide_05.png')
    print("SAVED slide_05.png")



def make_slide_06():
    base, mask = create_card_canvas((248, 250, 254, 255))
    draw = ImageDraw.Draw(base)
    
    draw.text((140, 95), "05  /  WIREFRAME & STRUCTURAL RATIONALE", font=get_font(14, 'semibold'), fill=(0, 87, 255))
    draw.text((140, 130), "와이어프레임 구조 설계 및 기능 1:1 매핑 명세", font=get_font(46, 'black'), fill=(15, 23, 42))
    draw.text((140, 196), "시각적 스킨(Visual Skin) 이전에 사용자의 인지 부하(Cognitive Load)를 최소화한 3대 핵심 화면 골격", font=get_font(19, 'regular'), fill=(100, 116, 139))
    
    screens = [
        ("Screen 01. 홈 대시보드 구조", [
            ("① Global Header", "앱 타이틀, 도움말(i), 환경설정(설정) 라우팅"),
            ("② VIP Status Banner", "24시간 무광고 잔여시간 카운트다운 타이머"),
            ("③ AI Ingestion Panel", "원터치 STT 발화 버튼 및 파형 시각화"),
            ("④ Quick Preset Chips", "±5%, ±10%, -20% 호가 즉각 주입 칩"),
            ("⑤ Asset Summary Carousel", "등록 자산 카드 가로 스크롤 및 평단 요약"),
            ("⑥ Bottom Action Dock", "시뮬레이터 포탈 가로 버튼 & 리포트 진입 CTA")
        ]),
        ("Screen 02. 시뮬레이터 구조", [
            ("① Strategy Tab Switcher", "단일 계산 / 시나리오 A vs B / 목표 역산 탭"),
            ("② Batch Step Input Card", "보유 평단, 수량, 1차~N차 추가 매수 입력부"),
            ("③ Auto Yield Indicator", "실시간 가중평균 평단 및 방어율 칩"),
            ("④ Capital Allocation Meter", "추가 투입 필요 자금 프로그레스 바"),
            ("⑤ Comparison Split View", "A안 vs B안 결과 수량 대조 카드"),
            ("⑥ Floating Action Button", "시나리오 로컬 DB 저장 및 리포트 생성")
        ]),
        ("Screen 03. 목표 역산 엔진 구조", [
            ("① Target Price Goal Setter", "사용자 희망 목표 평단가 입력 전용 필드"),
            ("② Current Asset Context", "현재 평단 ₩75,000 / 보유 100주 고정 컨텍스트"),
            ("③ Reverse Math Output", "Closed-Form 도출 필요 추가 매수 수량 출력"),
            ("④ Cash Constraint Slider", "가용 현금 한도 내 달성 가능 평단 인터랙티브 조절"),
            ("⑤ Feasibility Warning", "현재가 미달 시 불가능 경고 인포 텍스트"),
            ("⑥ Auto Inject to Sim", "도출한 수량을 시뮬레이터로 1초 자동 주입")
        ])
    ]
    
    wx = 140
    ww = 520
    wgap = 40
    for title, specs in screens:
        draw.rounded_rectangle([wx, 260, wx + ww, 940], radius=20, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw.text((wx + 30, 288), title, font=get_font(18, 'bold'), fill=(15, 23, 42))
        
        draw.rounded_rectangle([wx + 30, 325, wx + ww - 30, 560], radius=14, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
        draw.rounded_rectangle([wx + 50, 345, wx + ww - 50, 375], radius=8, fill=(219, 234, 254))
        draw.rounded_rectangle([wx + 50, 390, wx + ww - 50, 430], radius=10, fill=(226, 232, 240))
        draw.rounded_rectangle([wx + 50, 445, wx + 240, 495], radius=12, fill=(203, 213, 225))
        draw.rounded_rectangle([wx + 260, 445, wx + ww - 50, 495], radius=12, fill=(203, 213, 225))
        draw.rounded_rectangle([wx + 50, 510, wx + ww - 50, 540], radius=8, fill=(186, 215, 255))
        draw.text((wx + 185, 462), "Lo-Fi Blueprint Schema", font=get_font(12, 'bold'), fill=(100, 116, 139))
        
        sy = 585
        for s_title, s_desc in specs:
            draw.text((wx + 30, sy), s_title, font=get_font(13.5, 'bold'), fill=(0, 87, 255))
            lines = wrap_text_by_words(s_desc, get_font(12.5, 'regular'), ww - 65, draw)
            draw.text((wx + 30, sy + 20), lines[0], font=get_font(12.5, 'regular'), fill=(71, 85, 105))
            sy += 54
            
        wx += ww + wgap
        
    base.save('portfolio/behance_slides/slide_06.png')
    print("SAVED slide_06.png")

# ==============================================================
# SLIDE 07: Design System Foundations & Semantic Tokens
# ==============================================================
def make_slide_07():
    base, mask = create_card_canvas((15, 23, 42, 255))
    draw = ImageDraw.Draw(base)
    
    draw.text((140, 95), "06  /  DESIGN SYSTEM & W3C TOKENS", font=get_font(14, 'semibold'), fill=(0, 210, 255))
    draw.text((140, 130), "디자인 시스템 파운데이션 및 시맨틱 토큰 매핑", font=get_font(46, 'black'), fill=(255, 255, 255))
    draw.text((140, 196), "W3C 표준 JSON 토큰, WCAG 2.1 AAA 고대비 컬러, Tabular Numbers 고정폭 폰트 위계 체계", font=get_font(19, 'regular'), fill=(148, 163, 184))
    
    # Left: Color Palette
    draw.rounded_rectangle([140, 260, 900, 940], radius=20, fill=(24, 32, 48), outline=(51, 65, 85), width=2)
    draw.text((170, 290), "Color Palette & Semantic Tokens", font=get_font(20, 'bold'), fill=(255, 255, 255))
    draw.text((170, 320), "tokens.json 기반 실시간 테마 바인딩 (WCAG 2.1 AAA 7:1 대비 준수)", font=get_font(14, 'regular'), fill=(148, 163, 184))
    
    colors = [
        ("Electric Blue", "#0057FF", "Brand Primary", (0, 87, 255)),
        ("Mint Gain", "#00E676", "Semantic Success (+Yield)", (0, 230, 118)),
        ("Coral Loss", "#FF5252", "Semantic Error (-Loss)", (255, 82, 82)),
        ("Gold VIP", "#FFB300", "24h VIP Ad-Free Token", (255, 179, 0)),
        ("Royal Violet", "#7A22FF", "AI Voice STT Accent", (122, 34, 255)),
        ("Sky Cyan", "#00D2FF", "Goal Seeking Highlight", (0, 210, 255)),
        ("Deep Slate", "#0F141C", "Dark Background Surface", (15, 20, 28)),
        ("Pure Slate", "#F6F8FC", "Light Background Surface", (246, 248, 252))
    ]
    
    cy = 365
    for i in range(0, len(colors), 2):
        for col_idx in range(2):
            cname, chex, cdesc, rgb = colors[i + col_idx]
            box_x = 170 + col_idx * 360
            draw.rounded_rectangle([box_x, cy, box_x + 85, cy + 90], radius=16, fill=rgb, outline=(255, 255, 255, 40), width=1)
            draw.text((box_x + 105, cy + 12), cname, font=get_font(16, 'bold'), fill=(255, 255, 255))
            draw.text((box_x + 105, cy + 38), chex, font=get_font(14, 'bold'), fill=(0, 210, 255))
            draw.text((box_x + 105, cy + 62), cdesc, font=get_font(12.5, 'regular'), fill=(148, 163, 184))
        cy += 115
        
    # Right: Typography Scale
    draw.rounded_rectangle([940, 260, 1780, 940], radius=20, fill=(24, 32, 48), outline=(51, 65, 85), width=2)
    draw.text((970, 290), "Typography Scale & Layout Tokens", font=get_font(20, 'bold'), fill=(255, 255, 255))
    draw.text((970, 320), "숫자 흔들림 방지 Tabular Numbers & 44px 터치 타깃 규격", font=get_font(14, 'regular'), fill=(148, 163, 184))
    
    typos = [
        ("Display 32 / Bold", "₩ 1,480,000", "핵심 결과 평단가 및 수익 금액 (tnum 고정폭)"),
        ("HeadLine 24 / Bold", "+42.5주 추가 매수 필요", "Goal Seeking 역산 산출 결과 강조"),
        ("Title 18 / Bold", "호가 급락 시 원터치 분할 매수", "섹션 헤더 및 주요 카드 타이틀"),
        ("Body 15 / Regular", "급변하는 시장 변동성에 대비한 리스크 방어", "일반 본문 설명 및 툴팁 가이드")
    ]
    
    ty = 370
    for tscale, tex, tdesc in typos:
        draw.rounded_rectangle([970, ty, 1750, ty + 100], radius=16, fill=(15, 23, 42), outline=(51, 65, 85))
        draw.text((995, ty + 18), tscale, font=get_font(13.5, 'bold'), fill=(0, 210, 255))
        draw.text((1180, ty + 16), tex, font=get_font(19, 'bold'), fill=(255, 255, 255))
        draw.text((995, ty + 56), tdesc, font=get_font(13, 'regular'), fill=(148, 163, 184))
        ty += 118
        
    draw.rounded_rectangle([970, 850, 1345, 915], radius=12, fill=(15, 23, 42), outline=(51, 65, 85))
    draw.text((990, 863), "Corner Radius Spec", font=get_font(11, 'bold'), fill=(0, 210, 255))
    draw.text((990, 883), "Card Radius 24px (Soft) · Pill 44px (Full)", font=get_font(13, 'bold'), fill=(255, 255, 255))
    
    draw.rounded_rectangle([1375, 850, 1750, 915], radius=12, fill=(15, 23, 42), outline=(51, 65, 85))
    draw.text((1395, 863), "Elevation & Shadow Spec", font=get_font(11, 'bold'), fill=(0, 230, 118))
    draw.text((1395, 883), "Ambient Drop Shadow y=8, blur=20", font=get_font(13, 'bold'), fill=(255, 255, 255))
    
    base.save('portfolio/behance_slides/slide_07.png')
    print("SAVED slide_07.png")

# ==============================================================
# SLIDE 08: Feature Spotlight 01 - Multimodal Voice Ingestion
# ==============================================================
def make_slide_08():
    base, mask = create_card_canvas((15, 23, 42, 255))
    
    grad = Image.new('RGBA', (W, H), (0,0,0,0))
    gd = ImageDraw.Draw(grad)
    for y in range(H):
        ratio = y / H
        r = int(10 * (1 - ratio) + 5 * ratio)
        g = int(18 * (1 - ratio) + 8 * ratio)
        b = int(45 * (1 - ratio) + 20 * ratio)
        gd.line([(0, y), (W, y)], fill=(r, g, b, 255))
        
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([700, 150, 1300, 850], fill=(0, 87, 255, 80))
    gw.ellipse([1200, 200, 1800, 800], fill=(139, 92, 246, 60))
    gw.ellipse([100, 100, 700, 700], fill=(0, 210, 255, 50))
    glow = glow.filter(ImageFilter.GaussianBlur(110))
    grad = Image.alpha_composite(grad, glow)
    base.paste(grad, (0, 0), mask)
    
    draw = ImageDraw.Draw(base)
    
    draw.text((140, 95), "07  /  FEATURE SPOTLIGHT 01 · MULTIMODAL INGESTION", font=get_font(14, 'semibold'), fill=(0, 210, 255))
    draw.text((140, 130), "말 한마디로 단가와 수량을\n0.2초 즉각 분리 추출", font=get_font(44, 'black'), fill=(255, 255, 255), spacing=10)
    draw.text((140, 245), "급락 호가창 앞에서 타이핑 지연 없이\n매수 골든타임 슬리피지를 원천 방어", font=get_font(18, 'regular'), fill=(215, 230, 255), spacing=6)
    
    # Right Header Spec Banner
    draw.rounded_rectangle([1220, 110, 1780, 275], radius=20, fill=(24, 32, 50, 240), outline=(0, 210, 255, 120), width=1)
    draw.rounded_rectangle([1245, 130, 1375, 158], radius=6, fill=(0, 87, 255))
    draw.text((1257, 135), "ON-DEVICE STT", font=get_font(11.5, 'bold'), fill=(255, 255, 255))
    draw.text((1390, 133), "0.2s 하이브리드 파싱 파이프라인", font=get_font(17, 'bold'), fill=(255, 255, 255))
    draw.text((1245, 175), "Google STT 온디바이스 엔진과 정밀 정규식 토크나이저를\n결합하여 '종목명+단가+수량' 복합 발화를 오차 없이 분류합니다.", font=get_font(14, 'regular'), fill=(180, 200, 225), spacing=5)
    
    # Center Phone Mockup
    phone = Image.open('portfolio/mockup_ko_08_voice.png').convert('RGBA')
    pw = 375
    ph = int(phone.height * (pw / phone.width))
    phone = phone.resize((pw, ph), Image.Resampling.LANCZOS)
    
    sh = Image.new('RGBA', (W, H), (0,0,0,0))
    shd = ImageDraw.Draw(sh)
    shd.ellipse([772, 985, 772 + pw, 1060], fill=(0, 0, 0, 240))
    sh = sh.filter(ImageFilter.GaussianBlur(35))
    base = Image.alpha_composite(base, sh)
    base.paste(phone, (772, 70), phone)
    
    cards_l = [
        ("음성 파형 감지 & 실시간 파싱", "\"삼성전자 7만 원에 50주\"\n발화 즉시 0.2초 안에 단가/수량 분리"),
        ("키패드 타이핑 딜레이 78% 단축", "소수점 단가 8자리 입력 시간을 줄여\n매수 골든타임 슬리피지 방어")
    ]
    cards_r = [
        ("원터치 호가 프리셋 칩", "-5%, -10%, -20% 원터치 칩으로\n실시간 호가 급락 시 신속 매칭 지원"),
        ("오프라인 Hive 영속화", "지하철 음영 지역에서도 100% 동작,\n터치 한 번으로 시뮬레이터 자동 주입")
    ]
    
    draw = ImageDraw.Draw(base)
    cy = 340
    for title, desc in cards_l:
        draw.rounded_rectangle([140, cy, 700, cy + 175], radius=20, fill=(255, 255, 255, 245), outline=(255, 255, 255, 255), width=2)
        draw.rounded_rectangle([140, cy + 22, 146, cy + 153], radius=3, fill=(0, 87, 255))
        draw.text((175, cy + 28), title, font=get_font(19, 'bold'), fill=(15, 23, 42))
        lines = wrap_text_by_words(desc, get_font(14, 'regular'), 440, draw)
        ly = cy + 68
        for l in lines:
            draw.text((175, ly), l, font=get_font(14, 'regular'), fill=(71, 85, 105))
            ly += 24
        cy += 215
        
    cy = 340
    for title, desc in cards_r:
        draw.rounded_rectangle([1220, cy, 1780, cy + 175], radius=20, fill=(255, 255, 255, 245), outline=(255, 255, 255, 255), width=2)
        draw.rounded_rectangle([1220, cy + 22, 1226, cy + 153], radius=3, fill=(0, 210, 255))
        draw.text((1255, cy + 28), title, font=get_font(19, 'bold'), fill=(15, 23, 42))
        lines = wrap_text_by_words(desc, get_font(14, 'regular'), 440, draw)
        ly = cy + 68
        for l in lines:
            draw.text((1255, ly), l, font=get_font(14, 'regular'), fill=(71, 85, 105))
            ly += 24
        cy += 215
        
    base.save('portfolio/behance_slides/slide_08.png')
    print("SAVED slide_08.png")

# ==============================================================
# SLIDE 09: Feature Spotlight 02 - Goal-Seeking Math Logic
# ==============================================================
def make_slide_09():
    base, mask = create_card_canvas((10, 28, 36, 255))
    
    grad = Image.new('RGBA', (W, H), (0,0,0,0))
    gd = ImageDraw.Draw(grad)
    for y in range(H):
        ratio = y / H
        r = int(10 * (1 - ratio) + 6 * ratio)
        g = int(32 * (1 - ratio) + 16 * ratio)
        b = int(40 * (1 - ratio) + 24 * ratio)
        gd.line([(0, y), (W, y)], fill=(r, g, b, 255))
        
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([1100, 100, 1850, 950], fill=(0, 230, 180, 75))
    gw.ellipse([200, 200, 900, 900], fill=(0, 87, 255, 70))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    grad = Image.alpha_composite(grad, glow)
    base.paste(grad, (0, 0), mask)
    
    draw = ImageDraw.Draw(base)
    
    draw.text((140, 95), "08  /  FINANCIAL ALGORITHM & MATH LOGIC", font=get_font(14, 'semibold'), fill=(0, 230, 180))
    draw.text((140, 130), "원하는 목표 평단가까지\n수학적으로 정확한 역산 제공", font=get_font(46, 'black'), fill=(255, 255, 255), spacing=12)
    draw.text((140, 255), "수작업 엑셀 계산기의 한계를 극복하고, Goal-Seeking Closed Form 공식을\n적용하여 '추가 매수 가능 금액' 또는 '필요 매수 수량'을 0.01초 안에 즉시 도출합니다.", font=get_font(19, 'regular'), fill=(180, 210, 215), spacing=8)
    
    specs = [
        ("01. 단일 변수 Closed-Form 역산 공식",
         "Target Avg = (P0*Q0 + P1*Q1) / (Q0 + Q1) 식을 재배열하여\n필요 매수량 Q1 = Q0 * (P0 - Target) / (Target - P1)을 즉시 계산"),
        ("02. 예산 제약 기반 실시간 슬라이더",
         "사용자의 현재 가용 현금 내에서 도달 가능한 '최적 목표 평단'을\nInteractive Slider로 직관적 피드백 제공"),
        ("03. 수수료 및 거래세 오차 보정 (0.015%)",
         "증권사별 매매 수수료 및 유관기관 제비용을 감안한 실질 단가 시뮬레이션")
    ]
    
    cy = 385
    for title, desc in specs:
        draw.rounded_rectangle([140, cy, 940, cy + 130], radius=20, fill=(255, 255, 255, 245), outline=(255, 255, 255, 255), width=2)
        draw.rounded_rectangle([140, cy + 20, 146, cy + 110], radius=3, fill=(0, 230, 180))
        draw.text((175, cy + 24), title, font=get_font(19, 'bold'), fill=(10, 28, 36))
        lines = wrap_text_by_words(desc, get_font(14, 'regular'), 700, draw)
        ly = cy + 62
        for l in lines:
            draw.text((175, ly), l, font=get_font(14, 'regular'), fill=(60, 80, 90))
            ly += 24
        cy += 150
        
    phone = Image.open('portfolio/mockup_ko_03_target_filled.png').convert('RGBA')
    pw = 375
    ph = int(phone.height * (pw / phone.width))
    phone = phone.resize((pw, ph), Image.Resampling.LANCZOS)
    
    sh = Image.new('RGBA', (W, H), (0,0,0,0))
    shd = ImageDraw.Draw(sh)
    shd.ellipse([1195, 985, 1195 + pw, 1060], fill=(0, 0, 0, 240))
    sh = sh.filter(ImageFilter.GaussianBlur(35))
    base = Image.alpha_composite(base, sh)
    base.paste(phone, (1195, 70), phone)
    
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle([1020, 660, 1480, 810], radius=20, fill=(10, 28, 36, 250), outline=(0, 230, 180, 230), width=2)
    draw.text((1050, 685), "수학적 목표 도달 수량 산출", font=get_font(14, 'bold'), fill=(0, 230, 180))
    draw.text((1050, 715), "+42.5주 추가 매수 필요", font=get_font(30, 'black'), fill=(255, 255, 255))
    draw.text((1050, 762), "총 투입 필요 예수금: ₩ 2,125,000", font=get_font(15, 'regular'), fill=(180, 215, 220))
    
    base.save('portfolio/behance_slides/slide_09.png')
    print("SAVED slide_09.png")

# ==============================================================
# SLIDE 10: High-Fidelity UI Screens & Interactive Prototype
# ==============================================================
def make_slide_10():
    base, mask = create_card_canvas((245, 247, 252, 255))
    draw = ImageDraw.Draw(base)
    
    draw.text((140, 95), "09  /  HIGH-FIDELITY SCREENS & PROTOTYPE FLOW", font=get_font(14, 'semibold'), fill=(0, 87, 255))
    draw.text((140, 130), "6개 핵심 모바일 인터페이스 쇼케이스 및 상호작용 연결", font=get_font(46, 'black'), fill=(15, 23, 42))
    draw.text((140, 196), "홈 대시보드  ·  시뮬레이터  ·  목표 역산  ·  진단 리포트  ·  OLED 다크모드  ·  환경설정 유기적 흐름", font=get_font(18, 'regular'), fill=(100, 116, 139))
    
    mockup_files = [
        ('portfolio/mockup_ko_01_home.png', '01. 홈 대시보드'),
        ('portfolio/mockup_ko_02_sim.png', '02. 물타기 시뮬레이터'),
        ('portfolio/mockup_ko_03_target_filled.png', '03. 목표 역산 엔진'),
        ('portfolio/mockup_clean_report_filled.png', '04. 분석 리포트'),
        ('portfolio/mockup_dark_home_flawless.png', '05. OLED 야간 다크 홈'),
        ('portfolio/mockup_dark_settings_perfect.png', '06. 글로벌 환경설정')
    ]
    
    px = 140
    pw = 236
    pgap = 45
    phone_y = 250
    
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
        pill_y = phone_y + ph + 28
        draw.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + 36], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw.text((pill_x + 16, pill_y + 9), ctitle, font=get_font(12.5, 'bold'), fill=(15, 23, 42))
        
        px += pw + pgap
        
    base.save('portfolio/behance_slides/slide_10.png')
    print("SAVED slide_10.png")

def make_slide_11():
    base, mask = create_card_canvas((8, 12, 18, 255))
    
    grad = Image.new('RGBA', (W, H), (0,0,0,0))
    gd = ImageDraw.Draw(grad)
    for y in range(H):
        ratio = y / H
        r = int(12 * (1 - ratio) + 4 * ratio)
        g = int(16 * (1 - ratio) + 8 * ratio)
        b = int(24 * (1 - ratio) + 16 * ratio)
        gd.line([(0, y), (W, y)], fill=(r, g, b, 255))
        
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([700, 200, 1600, 950], fill=(0, 87, 255, 55))
    gw.ellipse([1100, 100, 1800, 700], fill=(0, 210, 255, 40))
    glow = glow.filter(ImageFilter.GaussianBlur(130))
    grad = Image.alpha_composite(grad, glow)
    base.paste(grad, (0, 0), mask)
    
    phone = Image.open('portfolio/mockup_dark_home_flawless.png').convert('RGBA')
    pw = 375
    ph = int(round(phone.height * (pw / phone.width)))
    phone = phone.resize((pw, ph), Image.Resampling.LANCZOS)
    
    # Complete Phone Mockup (Zero bottom crop)
    sh = Image.new('RGBA', (W, H), (0,0,0,0))
    shd = ImageDraw.Draw(sh)
    shd.ellipse([220, 985, 220 + pw, 1060], fill=(0, 0, 0, 255))
    sh = sh.filter(ImageFilter.GaussianBlur(38))
    base = Image.alpha_composite(base, sh)
    base.paste(phone, (220, 70), phone)
    
    draw = ImageDraw.Draw(base)
    
    tx = 840
    draw.text((tx, 165), "10  /  OLED DEEP DARK & ACCESSIBILITY", font=get_font(14, 'semibold'), fill=(0, 210, 255))
    draw.text((tx, 210), "야간 장세 트레이더를 위한\n고대비 다크 테마 시스템", font=get_font(48, 'black'), fill=(255, 255, 255), spacing=16)
    draw.text((tx, 365), "Designed for night trading volatility\n7:1 이상의 WCAG 2.1 AAA 명도 대비를 엄격히 준수하여\n급박한 야간 해외주식·가상자산 장세에서도 오독 없는 수치 가독성 보장.", font=get_font(20, 'regular'), fill=(180, 198, 220), spacing=10)
    
    specs = [
        ("시맨틱 컬러 토큰 매핑", "Primary Electric (#0057FF), Mint (#00E676), Coral (#FF5252), Gold (#FFB300)", (0, 87, 255)),
        ("Tabular Numbers 고정폭 폰트", "JetBrains Mono / Segoe UI의 'tnum' 속성을 적용하여 실시간 가격 변동 시 레이아웃 무흔들림", (0, 210, 255)),
        ("24시간 VIP 광고 제어 모델", "보상형 동영상 1회 시청 시 24시간 동안 배너 및 전면 광고 100% 완전 제거", (255, 179, 0))
    ]
    sy = 540
    for title, desc, ac_col in specs:
        draw.rounded_rectangle([tx, sy, tx + 940, sy + 104], radius=18, fill=(24, 32, 48, 240), outline=(ac_col[0], ac_col[1], ac_col[2], 120), width=2)
        draw.rounded_rectangle([tx, sy + 18, tx + 6, sy + 86], radius=3, fill=ac_col)
        draw.text((tx + 32, sy + 24), title, font=get_font(18, 'bold'), fill=(255, 255, 255))
        draw.text((tx + 32, sy + 58), desc, font=get_font(14, 'regular'), fill=(148, 163, 184))
        sy += 124
        
    base.save('portfolio/behance_slides/slide_11.png')
    print("SAVED slide_11.png")

def make_slide_12():
    base, mask = create_card_canvas((15, 23, 42, 255))
    
    grad = Image.new('RGBA', (W, H), (0,0,0,0))
    gd = ImageDraw.Draw(grad)
    for y in range(H):
        ratio = y / H
        r = int(15 * (1 - ratio) + 24 * ratio)
        g = int(23 * (1 - ratio) + 36 * ratio)
        b = int(42 * (1 - ratio) + 68 * ratio)
        gd.line([(0, y), (W, y)], fill=(r, g, b, 255))
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([1100, 200, 1800, 900], fill=(0, 87, 255, 80))
    gw.ellipse([200, 400, 800, 1000], fill=(0, 230, 118, 50))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    grad = Image.alpha_composite(grad, glow)
    base.paste(grad, (0, 0), mask)
    
    draw = ImageDraw.Draw(base)
    
    draw.text((140, 95), "11  /  BUSINESS IMPACT & RETROSPECTIVE", font=get_font(14, 'semibold'), fill=(0, 210, 255))
    draw.text((140, 130), "정량적 비즈니스 성과 및 STAR 회고", font=get_font(46, 'black'), fill=(255, 255, 255))
    
    metrics = [
        ("0.2s", "STT 음성 수치 파싱 속도", "키보드 타이핑 대비 입력 소요 시간 78% 단축"),
        ("100%", "Goal Seeking 수학적 정밀도", "부동소수점 오차 제로화 및 정밀 역산 도출"),
        ("60fps", "실시간 슬라이더 반응성", "RepaintBoundary 최적화로 버벅임 없는 즉각 반응")
    ]
    mx = 140
    mw = 520
    mgap = 40
    for val, title, desc in metrics:
        draw.rounded_rectangle([mx, 215, mx + mw, 345], radius=20, fill=(255, 255, 255, 255))
        draw.text((mx + 28, 232), val, font=get_num_font(44, 'black'), fill=(0, 160, 100))
        draw.text((mx + 28, 286), title, font=get_font(18, 'bold'), fill=(15, 23, 42))
        draw.text((mx + 28, 314), desc, font=get_font(13.5, 'regular'), fill=(100, 116, 139))
        mx += mw + mgap
        
    star_items = [
        ("Situation (상황)", "급격한 주가 하락 시 모바일 환경에서 분할 매수 단가 및 필요 수량을 계산하려는 투자자들의 긴박한 상황 발생. 기존 계산기는 타이핑 피로도가 높고 목표 평단가 도달에 필요한 수량을 역산해주지 못함.", (255, 107, 107)),
        ("Task (과제)", "1) 음성으로 0.2초 만에 단가/수량을 자동 파싱하는 무입력 경험 구축\n2) 목표 평단 입력 시 필요 추가 매수량을 즉각 도출하는 역산 알고리즘 탑재\n3) 오프라인 환경에서도 100% 안전하게 시나리오를 보관하는 Local-First 아키텍처 구현", (255, 193, 7)),
        ("Action (행동)", "STT 스트림 음성 데이터에서 정규식 기반 수치 추출 파이프라인 개발. Goal Seeking Closed Form 수학 공식을 코어로 구현하고, Flutter Hive NoSQL로 0ms 레이턴시 로컬 캐싱 구조 설계. WCAG 2.1 AAA 다크모드 시스템 완성.", (33, 150, 243)),
        ("Result (결과)", "복합 시뮬레이션 계산 소요 시간을 기존 2분에서 5초 이내로 단축. Google Play Console 프로덕션 심사 규격 100% 충족 및 24시간 보상형 무광고 모델을 통해 사용자 잔존율(Retention) 극대화.", (76, 175, 80))
    ]
    
    sx = 140
    sw = 385
    sgap = 33
    f_body = get_font(14, 'regular')
    for phase, content, color in star_items:
        draw.rounded_rectangle([sx, 385, sx + sw, 925], radius=20, fill=(255, 255, 255, 255))
        draw.rounded_rectangle([sx + 20, 405, sx + sw - 20, 450], radius=10, fill=color)
        draw.text((sx + 35, 417), phase, font=get_font(15.5, 'bold'), fill=(255, 255, 255))
        
        wrapped_lines = wrap_text_by_words(content, f_body, sw - 56, draw)
        text_y = 475
        for line in wrapped_lines:
            draw.text((sx + 28, text_y), line, font=f_body, fill=(30, 41, 59))
            text_y += 26
        
        sx += sw + sgap
        
    base.save('portfolio/behance_slides/slide_12.png')
    print("SAVED slide_12.png")

# ==============================================================
# MAIN PIPELINE
# ==============================================================
if __name__ == '__main__':
    for i in range(1, 13):
        func_name = f'make_slide_{i:02d}'
        if func_name in globals():
            globals()[func_name]()
    print("ALL 12 SLIDES GENERATED WITH SAMSUNG-GRADE PRETENDARD TYPOGRAPHY!")
