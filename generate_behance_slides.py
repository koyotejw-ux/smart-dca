import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
CARD_PAD = 36
RADIUS = 44

os.makedirs('portfolio/behance_slides', exist_ok=True)

def get_font(size, bold=False):
    font_path = "C:/Windows/Fonts/malgunbd.ttf" if bold else "C:/Windows/Fonts/malgun.ttf"
    try:
        return ImageFont.truetype(font_path, size)
    except:
        return ImageFont.load_default()

def get_mono_font(size, bold=False):
    # Try Consolas or Courier New or malgun
    for name in ["consolab.ttf" if bold else "consola.ttf", "courbd.ttf" if bold else "cour.ttf"]:
        p = f"C:/Windows/Fonts/{name}"
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return get_font(size, bold)

def create_card_canvas(bg_color):
    base = Image.new('RGBA', (W, H), (243, 245, 249, 255))
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
# SLIDE 01: Hero Cover
# ==============================================================
def make_slide_01():
    base, mask = create_card_canvas((24, 76, 255, 255))
    
    grad = Image.new('RGBA', (W, H), (0,0,0,0))
    g_draw = ImageDraw.Draw(grad)
    for y in range(H):
        ratio = y / H
        r = int(24 * (1 - ratio) + 12 * ratio)
        g = int(72 * (1 - ratio) + 26 * ratio)
        b = int(255 * (1 - ratio) + 160 * ratio)
        g_draw.line([(0, y), (W, y)], fill=(r, g, b, 255))
    
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([1050, 80, 1850, 950], fill=(0, 210, 255, 110))
    gw.ellipse([300, 500, 1100, 1200], fill=(130, 40, 240, 85))
    glow = glow.filter(ImageFilter.GaussianBlur(100))
    grad = Image.alpha_composite(grad, glow)
    base.paste(grad, (0, 0), mask)
    
    # Dual Mockup (Sim & Home)
    phone_back = Image.open('portfolio/mockup_ko_02_sim.png').convert('RGBA')
    pb_w = 380
    pb_h = int(phone_back.height * (pb_w / phone_back.width))
    phone_back = phone_back.resize((pb_w, pb_h), Image.Resampling.LANCZOS)
    
    phone_front = Image.open('portfolio/mockup_ko_01_home.png').convert('RGBA')
    pf_w = 410
    pf_h = int(phone_front.height * (pf_w / phone_front.width))
    phone_front = phone_front.resize((pf_w, pf_h), Image.Resampling.LANCZOS)
    
    sh = Image.new('RGBA', (W, H), (0,0,0,0))
    shd = ImageDraw.Draw(sh)
    shd.ellipse([1260, 880, 1660, 990], fill=(0, 0, 0, 160))
    shd.ellipse([1000, 890, 1440, 1010], fill=(0, 0, 0, 220))
    sh = sh.filter(ImageFilter.GaussianBlur(35))
    base = Image.alpha_composite(base, sh)
    
    base.paste(phone_back, (1260, 140), phone_back)
    base.paste(phone_front, (1000, 90), phone_front)
    
    # 3D Squircle Icon
    icon = Image.open('assets/app_icon_clean_squircle.png').convert('RGBA')
    icon = icon.resize((240, 240), Image.Resampling.LANCZOS)
    ish = Image.new('RGBA', (W, H), (0,0,0,0))
    ishd = ImageDraw.Draw(ish)
    ishd.ellipse([1480, 720, 1740, 840], fill=(0, 0, 0, 180))
    ish = ish.filter(ImageFilter.GaussianBlur(30))
    base = Image.alpha_composite(base, ish)
    base.paste(icon, (1490, 520), icon)
    
    overlay = Image.new('RGBA', (W, H), (0,0,0,0))
    d_ov = ImageDraw.Draw(overlay)
    
    # Category Pill
    d_ov.rounded_rectangle([140, 175, 520, 225], radius=25, fill=(255, 255, 255, 50))
    d_ov.text((165, 189), "SMART AVERAGE DOWN CALCULATOR", font=get_font(15, bold=True), fill=(255, 255, 255, 255))
    
    # Main Headline
    f_title = get_font(52, bold=True)
    d_ov.text((140, 260), "하락장 속 뇌동매매를 막는\n알고리즘 분할매수 솔루션", font=f_title, fill=(255, 255, 255, 255), spacing=18)
    
    # Subhead
    f_sub = get_font(23, bold=False)
    d_ov.text((140, 435), "Stop Panic Selling. Start Algorithmic Scaling.\n0.2초 음성 인식과 Goal Seeking 수학 역산으로 계좌를 방어합니다.", font=f_sub, fill=(215, 230, 255, 255), spacing=12)
    
    metrics = [
        ("0.2s", "STT 음성 인제스천", "호가 급락 시 1초 음성 단가·수량 분리"),
        ("100%", "Goal Seeking 역산", "희망 평단가 달성 필수 매수 수량 도출"),
        ("24h", "VIP 무광고 라이프사이클", "보상형 광고 1회 시청 시 24시간 광고 차단")
    ]
    cy = 580
    for val, title, desc in metrics:
        d_ov.rounded_rectangle([140, cy, 820, cy + 86], radius=20, fill=(255, 255, 255, 250))
        d_ov.text((170, cy + 18), val, font=get_font(34, bold=True), fill=(0, 82, 255, 255))
        d_ov.text((290, cy + 18), title, font=get_font(18, bold=True), fill=(15, 23, 42, 255))
        d_ov.text((290, cy + 48), desc, font=get_font(14, bold=False), fill=(100, 116, 139, 255))
        cy += 102
        
    d_ov.text((140, 925), "Lead Product Designer & Senior Flutter Engineer  ·  Production Verified", font=get_font(16, bold=True), fill=(200, 225, 255, 255))
    
    base = Image.alpha_composite(base, overlay)
    base.save('portfolio/behance_slides/slide_01.png')
    print("SAVED slide_01.png")

# ==============================================================
# SLIDE 02: Discovery & User Research (Pain Points + IDI Data)
# ==============================================================
def make_slide_02():
    base, mask = create_card_canvas((248, 250, 253, 255))
    draw = ImageDraw.Draw(base)
    
    f_cat = get_font(18, bold=True)
    f_title = get_font(44, bold=True)
    f_sub = get_font(20, bold=False)
    
    draw.text((140, 100), "01. DISCOVERY & USER RESEARCH", font=f_cat, fill=(0, 82, 255))
    draw.text((140, 138), "손실 회피 편향과 감정적 물타기의 한계", font=f_title, fill=(15, 23, 42))
    draw.text((140, 202), "개인 투자자 12명 심층 인터뷰(IDI) 및 커뮤니티 데이터 분석을 통해 도출한 3대 핵심 결핍", font=f_sub, fill=(100, 116, 139))
    
    # Left 3 Stat Boxes
    stats = [
        ("78.4%", "하락장 뇌동매매 경험률", "수학적 계획 없는 감정적 추가 매수 집행"),
        ("4.8분", "기존 계산기 수동 입력 소요", "소수점 단가·수량 타이핑 중 호가 급변"),
        ("0건", "MTS 내 목표 역산 기능 부재", "본전 탈출 필요 수량을 알지 못한 채 과매수")
    ]
    sx = 140
    sy = 270
    sw = 460
    for val, stitle, sdesc in stats:
        draw.rounded_rectangle([sx, sy, sx + sw, sy + 180], radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        # Accent pill
        draw.rounded_rectangle([sx + 30, sy + 25, sx + 130, sy + 58], radius=10, fill=(238, 242, 255))
        draw.text((sx + 45, sy + 32), "STAT DATA", font=get_font(12, bold=True), fill=(0, 82, 255))
        draw.text((sx + 30, sy + 70), val, font=get_font(44, bold=True), fill=(0, 82, 255))
        draw.text((sx + 30, sy + 125), stitle, font=get_font(18, bold=True), fill=(15, 23, 42))
        draw.text((sx + 30, sy + 150), sdesc, font=get_font(14, bold=False), fill=(100, 116, 139))
        sy += 210
        
    # Right 3 IDI Pain Point Cards
    cards = [
        ("PAIN POINT 01", "전략 부재: 비중만 비대해지고 평단은 거의 내려오지 않음",
         "\"단가를 낮추려고 예수금을 계속 넣었는데, 나중에 보니 계좌의 80%가 한 종목에 묶여있고 평단은 2%밖에 안 내려왔어요.\"\n— 3년 차 개인 투자자 IDI 인터뷰 내용 중",
         "Solution: 추가 매수 차수별 한계 효용 및 계좌 잠식 위험도 실시간 가시화", (239, 68, 68)),
        
        ("PAIN POINT 02", "조작 지연: 급변하는 호가창 앞에서 타이핑하다 골든타임 상실",
         "\"급락 빔이 쏟아질 때 평단 계산하려고 키패드로 8자리 단가를 치는 동안 이미 반등해버리거나 더 밑으로 뚫려버립니다.\"\n— 가상자산/단타 트레이더 IDI 인터뷰 내용 중",
         "Solution: 0.2초 STT 음성 자동 파싱 및 ±5% 원터치 프리셋 칩 즉각 주입", (245, 158, 11)),
         
        ("PAIN POINT 03", "출구 전략 부재: 목표 탈출가에 도달하기 위한 필요 매수량 미제공",
         "\"본전이나 -5% 선에서 정리하고 싶은데, 지금 얼마를 더 사야 그 평단이 만들어지는지 알려주는 앱이 전혀 없습니다.\"\n— 5년 차 직장인 스윙 투자자 IDI 인터뷰 내용 중",
         "Solution: Goal Seeking Closed Form 수학 공식을 통한 목표 도달 수량 정밀 역산", (16, 185, 129))
    ]
    
    rx = 640
    ry = 270
    rw = 1140
    for ptag, ptitle, pquote, psol, pcolor in cards:
        draw.rounded_rectangle([rx, ry, rx + rw, ry + 180], radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        
        # Tag
        draw.rounded_rectangle([rx + 35, ry + 22, rx + 160, ry + 52], radius=8, fill=(pcolor[0], pcolor[1], pcolor[2], 30), outline=pcolor, width=1)
        draw.text((rx + 48, ry + 28), ptag, font=get_font(12, bold=True), fill=pcolor)
        
        draw.text((rx + 180, ry + 26), ptitle, font=get_font(18, bold=True), fill=(15, 23, 42))
        
        # Quote
        draw.rounded_rectangle([rx + 35, ry + 64, rx + rw - 35, ry + 124], radius=12, fill=(248, 250, 252))
        draw.text((rx + 50, ry + 75), pquote, font=get_font(14, bold=False), fill=(71, 85, 105), spacing=4)
        
        # Sol
        draw.text((rx + 35, ry + 140), "💡 " + psol, font=get_font(14, bold=True), fill=(0, 82, 255))
        
        ry += 210

    base.save('portfolio/behance_slides/slide_02.png')
    print("SAVED slide_02.png")

# ==============================================================
# SLIDE 03: Competitive Benchmark & Target Personas
# ==============================================================
def make_slide_03():
    base, mask = create_card_canvas((248, 250, 253, 255))
    draw = ImageDraw.Draw(base)
    
    f_cat = get_font(18, bold=True)
    f_title = get_font(44, bold=True)
    f_sub = get_font(20, bold=False)
    
    draw.text((140, 100), "02. BENCHMARK & TARGET PERSONAS", font=f_cat, fill=(0, 82, 255))
    draw.text((140, 138), "경쟁사 벤치마킹 매트릭스 및 핵심 페르소나 정의", font=f_title, fill=(15, 23, 42))
    draw.text((140, 202), "기존 MTS 및 일반 계산기 앱 대비 독보적인 사용자 편의성과 알고리즘 기능 우위", font=f_sub, fill=(100, 116, 139))
    
    # Competitive Table (Left side: 920px wide)
    tx = 140
    ty = 270
    tw = 960
    th = 640
    draw.rounded_rectangle([tx, ty, tx + tw, ty + th], radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    # Table Header
    draw.rounded_rectangle([tx, ty, tx + tw, ty + 70], radius=24, fill=(241, 245, 249))
    draw.rectangle([tx, ty + 40, tx + tw, ty + 70], fill=(241, 245, 249)) # square bottom corners
    
    draw.text((tx + 30, ty + 24), "비교 분석 항목", font=get_font(16, bold=True), fill=(71, 85, 105))
    draw.text((tx + 240, ty + 24), "증권사 MTS 내장", font=get_font(16, bold=True), fill=(71, 85, 105))
    draw.text((tx + 470, ty + 24), "일반 앱스토어 계산기", font=get_font(16, bold=True), fill=(71, 85, 105))
    
    # Highlight Header for Our Product
    draw.rounded_rectangle([tx + 700, ty + 8, tx + tw - 12, ty + 62], radius=16, fill=(0, 82, 255))
    draw.text((tx + 725, ty + 24), "스마트 물타기 계산기", font=get_font(16, bold=True), fill=(255, 255, 255))
    
    rows = [
        ("입력 방식", "키패드 수동 입력 (느림)", "키패드 수동 입력 (광고 다수)", "멀티모달 (AI 음성 + 원터치 칩)"),
        ("연산 속도", "3~5초 (복잡한 메뉴 이동)", "2~3초 (단순 합산)", "0.2초 즉시 파싱 및 계산"),
        ("시나리오 비교", "불가능 (단일 계산)", "불가능 (1회성 소멸)", "A vs B 전략 대조 매트릭스"),
        ("목표가 역산", "미지원", "미지원", "Goal Seeking 역산 알고리즘"),
        ("보안/저장", "원격 로그인 필수 (지연)", "세션 종료 시 초기화", "Local-First NoSQL 100% 영속화"),
        ("광고 모델", "금융 상품 배너 혼재", "전면 강제 팝업 (피로도 극심)", "24시간 VIP 무광고 라이프사이클"),
        ("다크 테마", "일부 지원 (가독성 낮음)", "단순 그레이스케일 반전", "OLED 고대비 WCAG AAA 토큰")
    ]
    
    row_y = ty + 70
    for r_idx, (c0, c1, c2, c3) in enumerate(rows):
        bg_r = (255, 255, 255) if r_idx % 2 == 0 else (248, 250, 252)
        draw.rectangle([tx, row_y, tx + tw, row_y + 81], fill=bg_r)
        
        # Highlight column background
        draw.rectangle([tx + 695, row_y, tx + tw - 8, row_y + 81], fill=(238, 242, 255))
        
        draw.text((tx + 30, row_y + 28), c0, font=get_font(15, bold=True), fill=(15, 23, 42))
        draw.text((tx + 240, row_y + 28), c1, font=get_font(14, bold=False), fill=(100, 116, 139))
        draw.text((tx + 470, row_y + 28), c2, font=get_font(14, bold=False), fill=(100, 116, 139))
        draw.text((tx + 715, row_y + 28), c3, font=get_font(14, bold=True), fill=(0, 82, 255))
        
        draw.line([(tx, row_y + 81), (tx + tw, row_y + 81)], fill=(226, 232, 240), width=1)
        row_y += 81
        
    # Right Side: Dual Personas (Width: 640px)
    px = 1140
    py = 270
    pw = 640
    
    # Persona A
    draw.rounded_rectangle([px, py, px + pw, py + 305], radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([px + 30, py + 25, px + 150, py + 58], radius=10, fill=(238, 242, 255))
    draw.text((px + 45, py + 32), "PERSONA A", font=get_font(12, bold=True), fill=(0, 82, 255))
    draw.text((px + 170, py + 30), "김투자 (34세, 대기업 직장인)", font=get_font(18, bold=True), fill=(15, 23, 42))
    draw.text((px + 30, py + 75), "“월급날마다 분할 매수해서 6개월 안에 본전 탈출하고 싶어요.”", font=get_font(15, bold=True), fill=(0, 82, 255))
    
    pa_desc = "• 성향: 국내 대형 우량주 및 미국 지수 ETF 장기 분할 투자\n• 행동: 업무 중 급락 알림을 볼 때 감정적 추매를 자제하고 체계적 대응 시도\n• 핵심 니즈: 총자산 대비 특정 종목 편중 비율 및 A/B 시나리오별 평단 인하폭 대조"
    wrap_a = wrap_text_by_words(pa_desc, get_font(14, bold=False), pw - 60, draw)
    ay = py + 120
    for line in wrap_a:
        draw.text((px + 30, ay), line, font=get_font(14, bold=False), fill=(71, 85, 105))
        ay += 26
        
    # Persona B
    py_b = py + 335
    draw.rounded_rectangle([px, py_b, px + pw, py_b + 305], radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([px + 30, py_b + 25, px + 150, py_b + 58], radius=10, fill=(254, 243, 199))
    draw.text((px + 45, py_b + 32), "PERSONA B", font=get_font(12, bold=True), fill=(217, 119, 6))
    draw.text((px + 170, py_b + 30), "박스캘퍼 (28세, 크립토/단타 트레이더)", font=get_font(18, bold=True), fill=(15, 23, 42))
    draw.text((px + 30, py_b + 75), "“급락 빔 맞았을 때 3초 안에 평단 뽑아서 지지선에서 나와야 해요.”", font=get_font(15, bold=True), fill=(217, 119, 6))
    
    pb_desc = "• 성향: 고변동성 알트코인 및 테마주 단타/스캘핑 매매\n• 행동: 손가락으로 타이핑할 시간이 없어 음성으로 단가/수량을 즉각 투입\n• 핵심 니즈: 목표 탈출 가격에 도달하기 위한 필요 매수 수량을 0.01초 만에 역산"
    wrap_b = wrap_text_by_words(pb_desc, get_font(14, bold=False), pw - 60, draw)
    by = py_b + 120
    for line in wrap_b:
        draw.text((px + 30, by), line, font=get_font(14, bold=False), fill=(71, 85, 105))
        by += 26

    base.save('portfolio/behance_slides/slide_03.png')
    print("SAVED slide_03.png")

# ==============================================================
# SLIDE 04: Information Architecture (IA) & Customer Journey Map
# ==============================================================
def make_slide_04():
    base, mask = create_card_canvas((15, 23, 42, 255))
    
    grad = Image.new('RGBA', (W, H), (0,0,0,0))
    gd = ImageDraw.Draw(grad)
    for y in range(H):
        ratio = y / H
        r = int(15 * (1 - ratio) + 20 * ratio)
        g = int(23 * (1 - ratio) + 30 * ratio)
        b = int(42 * (1 - ratio) + 55 * ratio)
        gd.line([(0, y), (W, y)], fill=(r, g, b, 255))
    base.paste(grad, (0, 0), mask)
    
    draw = ImageDraw.Draw(base)
    f_cat = get_font(18, bold=True)
    f_title = get_font(44, bold=True)
    f_sub = get_font(20, bold=False)
    
    draw.text((140, 95), "03. INFORMATION ARCHITECTURE & USER JOURNEY", font=f_cat, fill=(0, 210, 255))
    draw.text((140, 133), "4단계 모듈형 정보 구조 설계 (IA) & CJM", font=f_title, fill=(255, 255, 255))
    draw.text((140, 192), "진입 온보딩부터 실시간 연산, 포트폴리오 리포트 영속화까지 끊김 없는 4대 도메인 트리 구조", font=f_sub, fill=(148, 163, 184))
    
    # Top Section: 4-Phase CJM Banner
    cjm_y = 245
    draw.rounded_rectangle([140, cjm_y, W - 140, cjm_y + 85], radius=20, fill=(30, 41, 59, 240), outline=(51, 65, 85), width=1)
    
    cjm_steps = [
        ("Phase 1. 급락 인지", "종목 급락 (-15%) 발생\n손실 공포 & 뇌동매매 충동"),
        ("Phase 2. 탐색 & 인제스천", "앱 실행 및 0.2s 음성 입력\n원터치 프리셋 칩 즉시 주입"),
        ("Phase 3. 알고리즘 시뮬레이션", "A vs B 분할 시나리오 대조\n목표 평단가 도달 수량 역산"),
        ("Phase 4. 확신 & 의사결정", "최적 매수 수량 실 집행\n로컬 DB 저장 및 심리적 안정")
    ]
    step_w = (W - 280) // 4
    for s_idx, (stitle, ssub) in enumerate(cjm_steps):
        sx = 140 + s_idx * step_w
        # Step number badge
        draw.rounded_rectangle([sx + 20, cjm_y + 16, sx + 50, cjm_y + 46], radius=8, fill=(0, 82, 255))
        draw.text((sx + 28, cjm_y + 22), str(s_idx + 1), font=get_font(14, bold=True), fill=(255, 255, 255))
        draw.text((sx + 60, cjm_y + 18), stitle, font=get_font(15, bold=True), fill=(255, 255, 255))
        draw.text((sx + 60, cjm_y + 42), ssub, font=get_font(12, bold=False), fill=(148, 163, 184))
        if s_idx < 3:
            draw.text((sx + step_w - 15, cjm_y + 30), "➔", font=get_font(18, bold=True), fill=(0, 210, 255))

    # Bottom Section: 4-Tier IA Domain Tree Columns
    ia_cols = [
        ("01. DISCOVERY & INIT", "1.0 Entry & Onboarding", [
            ("1.1 Splash Screen Engine", "로고 스케일링 & 세션 토큰 검증"),
            ("1.2 Strategy Onboarding (4 Steps)", "분할 매수 수학적 메커니즘 학습"),
            ("1.3 Locale & Currency Auto-Detect", "디바이스 국가 기반 통화(₩,$,¥,€) 연동"),
            ("1.4 VIP Ad-Free Token Activation", "24시간 무광고 라이프사이클 구독")
        ], (0, 82, 255)),
        
        ("02. CORE DASHBOARD", "2.0 Home & Ingestion", [
            ("2.1 Multimodal Voice Panel", "Google STT 온디바이스 실시간 파싱"),
            ("2.2 Quick Action Preset Chips", "±5%, ±10%, -20% 호가 즉각 주입"),
            ("2.3 Asset Portfolio Carousel", "보유 자산 실시간 평단/수량 요약"),
            ("2.4 Quick Dock Router", "자산 추가 / 시뮬레이터 / 리포트 진입")
        ], (16, 185, 129)),
        
        ("03. ALGORITHM CORE", "3.0 Simulation Engine", [
            ("3.1 Multi-Batch Simulator", "1~N차 가중평균 Closed Form 연산"),
            ("3.2 A/B Scenario Comparator", "전략별 평단 방어 효율 동시 대조"),
            ("3.3 Goal Seeking Calculator", "희망 평단가 도달 필수 매수량 역산"),
            ("3.4 Interactive Capital Slider", "예산 제약 내 실시간 최적 평단 피드백")
        ], (245, 158, 11)),
        
        ("04. PERSISTENCE & UTILITY", "4.0 Analytics & Settings", [
            ("4.1 Local-First SQLite & Hive", "100% 로컬 암호화 오프라인 저장"),
            ("4.2 Diagnostic Report Export", "SNS/메신저 시나리오 진단 카드 공유"),
            ("4.3 WCAG 2.1 AAA Dark System", "야간 장세 트레이더 고대비 토큰"),
            ("4.4 Compliance & Help Guide", "GDPR/개인정보 처리 및 MDD FAQ")
        ], (139, 92, 246))
    ]
    
    col_y = 360
    col_w = (W - 280 - 75) // 4
    col_gap = 25
    
    for c_idx, (cat_tag, cat_title, items, border_color) in enumerate(ia_cols):
        cx = 140 + c_idx * (col_w + col_gap)
        
        # Column Container Card
        draw.rounded_rectangle([cx, col_y, cx + col_w, col_y + 580], radius=20, fill=(30, 41, 59, 200), outline=border_color, width=2)
        
        # Column Header Badge
        draw.rounded_rectangle([cx + 18, col_y + 20, cx + col_w - 18, col_y + 68], radius=12, fill=(15, 23, 42, 220))
        draw.text((cx + 30, col_y + 28), cat_tag, font=get_font(12, bold=True), fill=border_color)
        draw.text((cx + 30, col_y + 46), cat_title, font=get_font(16, bold=True), fill=(255, 255, 255))
        
        # Items
        iy = col_y + 88
        for ititle, idesc in items:
            draw.rounded_rectangle([cx + 18, iy, cx + col_w - 18, iy + 106], radius=12, fill=(15, 23, 42, 240), outline=(51, 65, 85), width=1)
            # small bullet
            draw.ellipse([cx + 30, iy + 22, cx + 38, iy + 30], fill=border_color)
            draw.text((cx + 46, iy + 17), ititle, font=get_font(14, bold=True), fill=(241, 245, 249))
            draw.text((cx + 30, iy + 45), idesc, font=get_font(12, bold=False), fill=(148, 163, 184))
            iy += 120

    base.save('portfolio/behance_slides/slide_04.png')
    print("SAVED slide_04.png")

# ==============================================================
# SLIDE 05: User Flowchart & Edge Case Logic Branch
# ==============================================================
def make_slide_05():
    base, mask = create_card_canvas((248, 250, 253, 255))
    draw = ImageDraw.Draw(base)
    
    f_cat = get_font(18, bold=True)
    f_title = get_font(44, bold=True)
    f_sub = get_font(20, bold=False)
    
    draw.text((140, 100), "04. USER FLOWCHART & LOGIC BRANCH", font=f_cat, fill=(0, 82, 255))
    draw.text((140, 138), "사용자 행동 및 예외 처리 로직 플로우차트", font=f_title, fill=(15, 23, 42))
    draw.text((140, 202), "앱 실행부터 STT 권한 거부, 역산 불가 에지 케이스, VIP 무광고 분기까지의 엄밀한 상태 전이", font=f_sub, fill=(100, 116, 139))
    
    # Large Flow Diagram Card
    fx = 140
    fy = 270
    fw = W - 280
    fh = 660
    draw.rounded_rectangle([fx, fy, fx + fw, fy + fh], radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    # 5 Horizontal Swimlanes / Action Blocks
    # Stage 1: App Launch & Guard (x: 180 ~ 440)
    # Stage 2: Dashboard & Ad Check (x: 480 ~ 740)
    # Stage 3: Input & Voice Pipeline (x: 780 ~ 1040)
    # Stage 4: Engine & Simulation (x: 1080 ~ 1340)
    # Stage 5: Persistence & Report (x: 1380 ~ 1700)
    
    stages = [
        ("STAGE 1", "Launch & Init", [
            ("Launch App", "Splash Screen 로드", False),
            ("Check First Run?", "최초 실행 여부 분기", True),
            ("4-Step Onboarding", "원리 가이드 완료", False)
        ]),
        ("STAGE 2", "VIP & Dashboard", [
            ("VIP Active Check", "24h 무광고 토큰 검사", True),
            ("Pass (Skip Ad)", "광고 생략 및 즉시 진입", False),
            ("Main Dashboard", "자산 요약 & 독 로드", False)
        ]),
        ("STAGE 3", "Input Multimodal", [
            ("Tap Voice Mic", "STT 마이크 스트림 활성", False),
            ("STT Success?", "자연어 파싱 성공 분기", True),
            ("Fallback Preset Chip", "±5%, ±10% 칩 수동 선택", False)
        ]),
        ("STAGE 4", "Algorithm Engine", [
            ("Select Mode", "단일 / A-B / 목표 역산", True),
            ("Goal Seeking Calc", "Closed-Form 역산 수행", False),
            ("Target < Current?", "에지 케이스 역산 오류 방어", True)
        ]),
        ("STAGE 5", "Output & Save", [
            ("Show Result Card", "방어율 및 필요 수량 출력", False),
            ("Save to SQLite", "로컬 DB 스냅샷 저장", False),
            ("Share Report", "진단 이미지 외부 공유", False)
        ])
    ]
    
    col_w = 280
    gap = 25
    start_x = 180
    for s_idx, (stag, sname, nodes) in enumerate(stages):
        cx = start_x + s_idx * (col_w + gap)
        
        # Stage Header
        draw.rounded_rectangle([cx, fy + 30, cx + col_w, fy + 75], radius=12, fill=(241, 245, 249))
        draw.text((cx + 16, fy + 42), stag + " · " + sname, font=get_font(13, bold=True), fill=(0, 82, 255))
        
        ny = fy + 105
        for n_idx, (ntitle, ndesc, is_decision) in enumerate(nodes):
            if is_decision:
                # Diamond / Accent Rounded Decision Box
                draw.rounded_rectangle([cx, ny, cx + col_w, ny + 95], radius=20, fill=(254, 243, 199), outline=(245, 158, 11), width=2)
                draw.text((cx + 20, ny + 20), "◆ " + ntitle, font=get_font(15, bold=True), fill=(180, 83, 9))
                draw.text((cx + 20, ny + 50), ndesc, font=get_font(13, bold=False), fill=(120, 53, 15))
            else:
                # Standard Action Box
                draw.rounded_rectangle([cx, ny, cx + col_w, ny + 95], radius=16, fill=(248, 250, 252), outline=(203, 213, 225), width=1)
                draw.text((cx + 20, ny + 20), "■ " + ntitle, font=get_font(15, bold=True), fill=(15, 23, 42))
                draw.text((cx + 20, ny + 50), ndesc, font=get_font(13, bold=False), fill=(100, 116, 139))
                
            # Connecting Arrow Down
            if n_idx < len(nodes) - 1:
                draw.line([(cx + col_w // 2, ny + 95), (cx + col_w // 2, ny + 130)], fill=(0, 82, 255), width=2)
                draw.polygon([(cx + col_w // 2 - 4, ny + 125), (cx + col_w // 2 + 4, ny + 125), (cx + col_w // 2, ny + 130)], fill=(0, 82, 255))
                
            ny += 130
            
        # Connecting Arrow Right to next stage
        if s_idx < len(stages) - 1:
            draw.line([(cx + col_w + 5, fy + 260), (cx + col_w + gap - 5, fy + 260)], fill=(0, 82, 255), width=2)
            draw.polygon([(cx + col_w + gap - 10, fy + 256), (cx + col_w + gap - 10, fy + 264), (cx + col_w + gap - 4, fy + 260)], fill=(0, 82, 255))
            
    # Bottom Note Banner
    draw.rounded_rectangle([fx + 40, fy + fh - 90, fx + fw - 40, fy + fh - 30], radius=14, fill=(238, 242, 255))
    draw.text((fx + 65, fy + fh - 70), "🛡️ 에지 케이스 방어 로직: 목표 평단가가 현재가보다 낮은 불가능 수치 입력 시 즉시 경고 토스트 팝업 및 가용 현금 내 달성 가능 수치 자동 추천", font=get_font(14, bold=True), fill=(0, 82, 255))

    base.save('portfolio/behance_slides/slide_05.png')
    print("SAVED slide_05.png")

# ==============================================================
# SLIDE 06: Low-Fi to Mid-Fi Wireframes (Structural Rationale)
# ==============================================================
def make_slide_06():
    base, mask = create_card_canvas((248, 250, 253, 255))
    draw = ImageDraw.Draw(base)
    
    f_cat = get_font(18, bold=True)
    f_title = get_font(44, bold=True)
    f_sub = get_font(20, bold=False)
    
    draw.text((140, 100), "05. WIREFRAME & STRUCTURAL RATIONALE", font=f_cat, fill=(0, 82, 255))
    draw.text((140, 138), "와이어프레임 구조 설계 및 기능 1:1 매핑 명세", font=f_title, fill=(15, 23, 42))
    draw.text((140, 202), "시각적 스킨(Visual Skin) 이전에 사용자의 인지 부하(Cognitive Load)를 최소화한 3대 핵심 화면 골격", font=f_sub, fill=(100, 116, 139))
    
    wireframes = [
        ("Screen 01. 홈 대시보드 구조", [
            ("① Global Header", "앱 타이틀, 도움말(?), 환경설정(⚙) 라우팅"),
            ("② VIP Status Banner", "24시간 무광고 잔여시간 카운트다운 타이머"),
            ("③ AI Ingestion Panel", "원터치 STT 발화 버튼 및 파형 시각화"),
            ("④ Quick Preset Chips", "±5%, ±10%, -20% 호가 즉각 주입 칩"),
            ("⑤ Asset Summary Carousel", "등록 자산 카드 가로 스크롤 및 평단 요약"),
            ("⑥ Bottom Action Dock", "시뮬레이터 바로가기 & 리포트 진입 CTA")
        ]),
        ("Screen 02. 시뮬레이터 구조", [
            ("① Strategy Tab Switcher", "단일 계산 / 시나리오 A vs B / 목표 역산 탭"),
            ("② Batch Step Input Card", "보유 평단, 수량, 1차~N차 추가 매수 입력부"),
            ("③ Auto Yield Indicator", "실시간 가중평균 평단 및 방어율 칩"),
            ("④ Capital Allocation Meter", "추가 투입 필요 자금 프로그레스 바"),
            ("⑤ Comparison Split View", "A안 vs B안 결과 수평 대조 카드"),
            ("⑥ Floating Action Button", "시나리오 로컬 DB 저장 및 리포트 생성")
        ]),
        ("Screen 03. 목표 역산 엔진 구조", [
            ("① Target Price Goal Setter", "사용자 희망 목표 평단가 입력 인풋 필드"),
            ("② Current Asset Context", "현재 평단 ₩75,000 / 보유 100주 고정 컨텍스트"),
            ("③ Reverse Math Output", "Closed-Form 도출 필요 추가 매수 수량 출력"),
            ("④ Cash Constraint Slider", "가용 현금 한도 내 달성 가능 평단 인터랙티브 조절"),
            ("⑤ Feasibility Warning", "현재가 미달 시 불가능 경고 안내 텍스트"),
            ("⑥ Auto Inject to Sim", "도출된 수량을 시뮬레이터로 1초 자동 주입")
        ])
    ]
    
    col_w = (W - 280 - 60) // 3
    col_gap = 30
    cx = 140
    cy = 270
    
    for ctitle, specs in wireframes:
        # Container Card (Slate White)
        draw.rounded_rectangle([cx, cy, cx + col_w, cy + 660], radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        
        # Header Badge
        draw.rounded_rectangle([cx, cy, cx + col_w, cy + 70], radius=24, fill=(241, 245, 249))
        draw.rectangle([cx, cy + 40, cx + col_w, cy + 70], fill=(241, 245, 249))
        draw.text((cx + 25, cy + 24), ctitle, font=get_font(18, bold=True), fill=(15, 23, 42))
        
        # Wireframe Blueprint Box
        draw.rounded_rectangle([cx + 25, cy + 90, cx + col_w - 25, cy + 320], radius=16, fill=(248, 250, 252), outline=(203, 213, 225), width=2)
        # Draw wireframe schematic lines inside
        draw.rectangle([cx + 45, cy + 110, cx + col_w - 45, cy + 135], fill=(226, 232, 240)) # header
        draw.rectangle([cx + 45, cy + 145, cx + col_w - 45, cy + 175], fill=(219, 234, 254)) # banner
        draw.rectangle([cx + 45, cy + 185, cx + col_w - 45, cy + 245], fill=(226, 232, 240)) # main card
        draw.rectangle([cx + 45, cy + 255, cx + 180, cy + 300], fill=(203, 213, 225)) # button 1
        draw.rectangle([cx + 200, cy + 255, cx + col_w - 45, cy + 300], fill=(203, 213, 225)) # button 2
        draw.text((cx + col_w // 2, cy + 215), "Lo-Fi Blueprint Schema", font=get_font(13, bold=True), fill=(100, 116, 139), anchor="mm")
        
        # Functional Specs Index
        sy = cy + 340
        for idx_tag, idesc in specs:
            draw.text((cx + 25, sy), idx_tag, font=get_font(14, bold=True), fill=(0, 82, 255))
            draw.text((cx + 25, sy + 22), idesc, font=get_font(13, bold=False), fill=(71, 85, 105))
            sy += 50
            
        cx += col_w + col_gap

    base.save('portfolio/behance_slides/slide_06.png')
    print("SAVED slide_06.png")

# ==============================================================
# SLIDE 07: Design System Foundations & Semantic Tokens
# ==============================================================
def make_slide_07():
    base, mask = create_card_canvas((15, 23, 42, 255))
    
    grad = Image.new('RGBA', (W, H), (0,0,0,0))
    gd = ImageDraw.Draw(grad)
    for y in range(H):
        ratio = y / H
        r = int(15 * (1 - ratio) + 20 * ratio)
        g = int(23 * (1 - ratio) + 28 * ratio)
        b = int(42 * (1 - ratio) + 52 * ratio)
        gd.line([(0, y), (W, y)], fill=(r, g, b, 255))
    base.paste(grad, (0, 0), mask)
    
    draw = ImageDraw.Draw(base)
    f_cat = get_font(18, bold=True)
    f_title = get_font(44, bold=True)
    f_sub = get_font(20, bold=False)
    
    draw.text((140, 95), "06. DESIGN SYSTEM & W3C TOKENS", font=f_cat, fill=(0, 210, 255))
    draw.text((140, 133), "디자인 시스템 파운데이션 및 시맨틱 토큰 매핑", font=f_title, fill=(255, 255, 255))
    draw.text((140, 192), "W3C 표준 JSON 토큰, WCAG 2.1 AAA 고대비 컬러, Tabular Numbers 고정폭 폰트 위계 체계", font=f_sub, fill=(148, 163, 184))
    
    # Left Block: Color Tokens Grid (Width: 800px)
    cx = 140
    cy = 255
    cw = 780
    ch = 680
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=24, fill=(30, 41, 59, 220), outline=(51, 65, 85), width=1)
    draw.text((cx + 30, cy + 25), "Color Palette & Semantic Tokens", font=get_font(20, bold=True), fill=(255, 255, 255))
    draw.text((cx + 30, cy + 55), "tokens.json 기반 실시간 테마 바인딩 (WCAG 2.1 AAA 7:1 대비 준수)", font=get_font(13, bold=False), fill=(148, 163, 184))
    
    color_swatches = [
        ("#0051FF", "Electric Blue", "Brand Primary", (0, 81, 255)),
        ("#00E676", "Mint Gain", "Semantic Success (+Yield)", (0, 230, 118)),
        ("#FF5252", "Coral Loss", "Semantic Error (-Loss)", (255, 82, 82)),
        ("#FFB300", "Gold VIP", "24h VIP Ad-Free Token", (255, 179, 0)),
        ("#7A22FF", "Royal Violet", "AI Voice STT Accent", (122, 34, 255)),
        ("#00D2FF", "Sky Cyan", "Goal Seeking Highlight", (0, 210, 255)),
        ("#0F172A", "Deep Slate", "Dark Background Surface", (15, 23, 42)),
        ("#F8FAFC", "Pure Slate", "Light Background Surface", (248, 250, 252))
    ]
    
    sw_x = cx + 30
    sw_y = cy + 95
    for idx, (hex_code, name, role, rgb) in enumerate(color_swatches):
        row = idx // 2
        col = idx % 2
        sx = sw_x + col * 360
        sy = sw_y + row * 135
        
        # Color Box
        draw.rounded_rectangle([sx, sy, sx + 85, sy + 115], radius=16, fill=rgb, outline=(255, 255, 255, 60), width=1)
        draw.text((sx + 105, sy + 15), name, font=get_font(17, bold=True), fill=(255, 255, 255))
        draw.text((sx + 105, sy + 45), hex_code, font=get_mono_font(15, bold=True), fill=(0, 210, 255))
        draw.text((sx + 105, sy + 75), role, font=get_font(13, bold=False), fill=(148, 163, 184))
        
    # Right Block: Typography & Component Geometry (Width: 800px)
    rx = 960
    ry = 255
    rw = 820
    rh = 680
    draw.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=24, fill=(30, 41, 59, 220), outline=(51, 65, 85), width=1)
    
    draw.text((rx + 30, ry + 25), "Typography Scale & Layout Tokens", font=get_font(20, bold=True), fill=(255, 255, 255))
    draw.text((rx + 30, ry + 55), "숫자 흔들림 방지 Tabular Numbers & 44px 터치 타깃 규격", font=get_font(13, bold=False), fill=(148, 163, 184))
    
    typo_items = [
        ("Display 52 / Bold", "₩ 1,480,000", "핵심 결과 평단가 및 수익 금액 (tnum 고정폭)"),
        ("Headline 34 / Bold", "+42.5주 추가 매수 필요", "Goal Seeking 역산 산출 결과 강조"),
        ("Title 22 / Bold", "호가 급락 시 원터치 분할 매수", "섹션 헤더 및 주요 카드 타이틀"),
        ("Body 15 / Regular", "급변하는 시장 변동성에 대비한 리스크 방어", "일반 본문 설명 및 툴팁 가이드")
    ]
    
    ty_y = ry + 95
    for t_scale, t_sample, t_desc in typo_items:
        draw.rounded_rectangle([rx + 30, ty_y, rx + rw - 30, ty_y + 85], radius=14, fill=(15, 23, 42, 200), outline=(51, 65, 85), width=1)
        draw.text((rx + 48, ty_y + 14), t_scale, font=get_mono_font(12, bold=True), fill=(0, 210, 255))
        draw.text((rx + 220, ty_y + 12), t_sample, font=get_font(17, bold=True), fill=(255, 255, 255))
        draw.text((rx + 48, ty_y + 48), t_desc, font=get_font(13, bold=False), fill=(148, 163, 184))
        ty_y += 100
        
    # Radius & Elevation Grid
    draw.rounded_rectangle([rx + 30, ty_y + 10, rx + rw - 30, ry + rh - 30], radius=16, fill=(15, 23, 42, 240))
    draw.text((rx + 50, ty_y + 30), "📐 Component Elevation & Corner Radius Specs", font=get_font(16, bold=True), fill=(0, 230, 118))
    draw.text((rx + 50, ty_y + 60), "• Card Radius: 24px (Soft Round)  /  Pill Radius: 44px (Full Round)\n• Touch Target: Min 48×48dp (WCAG 2.5.5 충족)\n• Elevation: 0dp (Flat Dark) ~ 12dp Drop Shadow (y:12, blur:24, opacity:0.18)", font=get_font(14, bold=False), fill=(203, 213, 225), spacing=8)

    base.save('portfolio/behance_slides/slide_07.png')
    print("SAVED slide_07.png")

# ==============================================================
# SLIDE 08: Feature Spotlight 01 - Multimodal Voice Ingestion
# ==============================================================
def make_slide_08():
    base, mask = create_card_canvas((100, 75, 230, 255))
    
    grad = Image.new('RGBA', (W, H), (0,0,0,0))
    gd = ImageDraw.Draw(grad)
    for y in range(H):
        ratio = y / H
        r = int(105 * (1 - ratio) + 80 * ratio)
        g = int(80 * (1 - ratio) + 50 * ratio)
        b = int(240 * (1 - ratio) + 220 * ratio)
        gd.line([(0, y), (W, y)], fill=(r, g, b, 255))
        
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([600, 200, 1320, 920], fill=(180, 120, 255, 90))
    glow = glow.filter(ImageFilter.GaussianBlur(80))
    grad = Image.alpha_composite(grad, glow)
    base.paste(grad, (0, 0), mask)
    
    draw = ImageDraw.Draw(base)
    f_cat = get_font(18, bold=True)
    f_title = get_font(44, bold=True)
    f_sub = get_font(20, bold=False)
    
    draw.text((W // 2, 105), "FEATURE 01 · 0.2s SPEECH-TO-TEXT INGESTION", font=f_cat, fill=(210, 190, 255), anchor="mm")
    draw.text((W // 2, 150), "말 한마디로 단가와 수량을 즉각 분리 추출", font=f_title, fill=(255, 255, 255), anchor="mm")
    draw.text((W // 2, 205), "급락 호가창 앞에서 타이핑 지연으로 인한 매수 골든타임 슬리피지를 원천 방어", font=f_sub, fill=(220, 210, 255), anchor="mm")
    
    phone = Image.open('portfolio/mockup_ko_01_home.png').convert('RGBA')
    pw = 410
    ph = int(phone.height * (pw / phone.width))
    phone = phone.resize((pw, ph), Image.Resampling.LANCZOS)
    
    sh = Image.new('RGBA', (W, H), (0,0,0,0))
    shd = ImageDraw.Draw(sh)
    shd.ellipse([(W - pw) // 2 - 20, 940, (W + pw) // 2 + 20, 1030], fill=(0, 0, 0, 220))
    sh = sh.filter(ImageFilter.GaussianBlur(30))
    base = Image.alpha_composite(base, sh)
    base.paste(phone, ((W - pw) // 2, 240), phone)
    
    # 4 Solid Callout Cards
    draw = ImageDraw.Draw(base)
    cards = [
        (160, 340, "음성 파형 감지 & 실시간 파싱", "\"삼성전자 7만 원에 50주\"\n발화 즉시 0.2초 만에 단가/수량 분리"),
        (1280, 340, "원터치 호가 프리셋 칩", "-5%, -10%, -20% 원터치 칩으로\n실시간 호가 급락 시 신속 매핑 지원"),
        (160, 620, "키패드 타이핑 딜레이 78% 단축", "소수점 단가 8자리 입력 시간을 줄여\n매수 골든타임 슬리피지 방어"),
        (1280, 620, "오프라인 Hive 영속화", "지하철 음영 지역에서도 100% 동작,\n터치 한 번으로 시뮬레이터 자동 주입")
    ]
    for cx, cy, ctitle, cdesc in cards:
        draw.rounded_rectangle([cx, cy, cx + 460, cy + 175], radius=24, fill=(255, 255, 255, 255))
        draw.text((cx + 28, cy + 24), ctitle, font=get_font(18, bold=True), fill=(80, 50, 210))
        draw.text((cx + 28, cy + 64), cdesc, font=get_font(15, bold=False), fill=(50, 50, 60), spacing=8)
        
    base.save('portfolio/behance_slides/slide_08.png')
    print("SAVED slide_08.png")

# ==============================================================
# SLIDE 09: Feature Spotlight 02 - Goal-Seeking Math Engine
# ==============================================================
def make_slide_09():
    base, mask = create_card_canvas((16, 42, 48, 255))
    
    grad = Image.new('RGBA', (W, H), (0,0,0,0))
    gd = ImageDraw.Draw(grad)
    for y in range(H):
        ratio = y / H
        r = int(10 * (1 - ratio) + 18 * ratio)
        g = int(38 * (1 - ratio) + 52 * ratio)
        b = int(48 * (1 - ratio) + 60 * ratio)
        gd.line([(0, y), (W, y)], fill=(r, g, b, 255))
        
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([900, 100, 1800, 1000], fill=(0, 230, 180, 50))
    gw.ellipse([200, 400, 900, 1100], fill=(0, 120, 255, 45))
    glow = glow.filter(ImageFilter.GaussianBlur(110))
    grad = Image.alpha_composite(grad, glow)
    base.paste(grad, (0, 0), mask)
    
    draw = ImageDraw.Draw(base)
    f_cat = get_font(18, bold=True)
    f_title = get_font(46, bold=True)
    f_sub = get_font(21, bold=False)
    
    tx = 140
    draw.rounded_rectangle([tx, 140, tx + 400, 186], radius=22, fill=(0, 230, 180, 40))
    draw.text((tx + 20, 152), "FINANCIAL ALGORITHM & MATH LOGIC", font=get_font(14, bold=True), fill=(0, 230, 180))
    
    draw.text((tx, 210), "원하는 목표 평단가까지\n수학적으로 정확한 역산 제공", font=f_title, fill=(255, 255, 255), spacing=18)
    draw.text((tx, 350), "수작업 엑셀 계산기의 한계를 극복하고, Goal-Seeking Closed Form 공식을\n적용하여 '추가 매수 가능 금액' 또는 '필요 매수 수량'을 0.01초 만에 즉시 도출합니다.", font=f_sub, fill=(200, 220, 225), spacing=10)
    
    math_cards = [
        ("01. 단일 변수 Closed-Form 역산 공식", "Target Avg = (P0*Q0 + P1*Q1) / (Q0 + Q1) 식을 재배열하여\n필요 매수량 Q1 = Q0 * (P0 - Target) / (Target - P1)을 즉시 계산"),
        ("02. 예산 제약 기반 실시간 슬라이더", "사용자의 현재 가용 현금 내에서 도달 가능한 '최적 목표 평단'을\nInteractive Slider로 직관적 피드백 제공"),
        ("03. 수수료 및 거래세 오차 보정 (0.015%)", "증권사별 매매 수수료 및 유관기관 제비용을 감안한 실질 단가 시뮬레이션")
    ]
    sy = 495
    for title, desc in math_cards:
        draw.rounded_rectangle([tx, sy, tx + 820, sy + 115], radius=20, fill=(255, 255, 255, 255))
        draw.text((tx + 28, sy + 20), title, font=get_font(18, bold=True), fill=(0, 150, 120))
        draw.text((tx + 28, sy + 52), desc, font=get_font(15, bold=False), fill=(51, 65, 85), spacing=6)
        sy += 135
        
    phone = Image.open('portfolio/mockup_ko_03_target.png').convert('RGBA')
    pw = 460
    ph = int(phone.height * (pw / phone.width))
    phone = phone.resize((pw, ph), Image.Resampling.LANCZOS)
    
    sh = Image.new('RGBA', (W, H), (0,0,0,0))
    shd = ImageDraw.Draw(sh)
    shd.ellipse([1180, 910, 1180 + pw, 1020], fill=(0, 0, 0, 240))
    sh = sh.filter(ImageFilter.GaussianBlur(35))
    base = Image.alpha_composite(base, sh)
    base.paste(phone, (1180, 110), phone)
    
    # Floating Result Callout Card
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle([1020, 670, 1450, 800], radius=24, fill=(10, 28, 36, 245), outline=(0, 230, 180, 220), width=3)
    draw.text((1050, 695), "수학적 목표 도달 수량 산출", font=get_font(15, bold=True), fill=(0, 230, 180))
    draw.text((1050, 725), "+42.5주 추가 매수 필요", font=get_font(26, bold=True), fill=(255, 255, 255))
    draw.text((1050, 762), "총 투입 필요 예수금: ₩ 3,400,000", font=get_font(14, bold=False), fill=(180, 210, 215))
    
    base.save('portfolio/behance_slides/slide_09.png')
    print("SAVED slide_09.png")

# ==============================================================
# SLIDE 10: High-Fidelity UI Screens & Interactive Prototype
# ==============================================================
def make_slide_10():
    base, mask = create_card_canvas((245, 247, 252, 255))
    draw = ImageDraw.Draw(base)
    
    f_cat = get_font(18, bold=True)
    f_title = get_font(44, bold=True)
    f_sub = get_font(21, bold=False)
    
    draw.text((140, 95), "08. HIGH-FIDELITY SCREENS & INTERACTION PROTOTYPE", font=f_cat, fill=(0, 82, 255))
    draw.text((140, 133), "6개 핵심 모바일 인터페이스 쇼케이스 및 상호작용 연결", font=f_title, fill=(15, 23, 42))
    draw.text((140, 195), "홈 대시보드 ➔ 시뮬레이터 ➔ 목표 역산 ➔ 진단 리포트 ➔ OLED 다크모드 ➔ 환경설정 유기적 흐름", font=f_sub, fill=(100, 116, 139))
    
    screens = [
        ("portfolio/mockup_ko_01_home.png", "01. 홈 대시보드", 290),
        ("portfolio/mockup_ko_02_sim.png", "02. 물타기 시뮬레이터", 250),
        ("portfolio/mockup_ko_03_target.png", "03. 목표 역산 엔진", 290),
        ("portfolio/mockup_clean_report_filled.png", "04. 분석 리포트", 250),
        ("portfolio/mockup_dark_home_flawless.png", "05. OLED 야간 다크 홈", 290),
        ("portfolio/mockup_dark_settings_perfect.png", "06. 글로벌 환경설정", 250),
    ]
    
    px = 120
    pw = 255
    gap = 25
    for path, label, top_y in screens:
        phone = Image.open(path).convert('RGBA')
        ph = int(phone.height * (pw / phone.width))
        phone = phone.resize((pw, ph), Image.Resampling.LANCZOS)
        
        sh = Image.new('RGBA', (W, H), (0,0,0,0))
        shd = ImageDraw.Draw(sh)
        shd.ellipse([px + 10, top_y + ph - 30, px + pw - 10, top_y + ph + 25], fill=(0, 0, 0, 120))
        sh = sh.filter(ImageFilter.GaussianBlur(18))
        base = Image.alpha_composite(base, sh)
        
        base.paste(phone, (px, top_y), phone)
        
        draw = ImageDraw.Draw(base)
        draw.rounded_rectangle([px + 15, top_y + ph + 20, px + pw - 15, top_y + ph + 56], radius=12, fill=(255, 255, 255), outline=(226, 232, 240))
        draw.text((px + 30, top_y + ph + 30), label, font=get_font(13, bold=True), fill=(30, 41, 59))
        
        px += pw + gap
        
    base.save('portfolio/behance_slides/slide_10.png')
    print("SAVED slide_10.png")

# ==============================================================
# SLIDE 11: OLED Deep Dark Theme & Accessibility
# ==============================================================
def make_slide_11():
    base, mask = create_card_canvas((18, 22, 34, 255))
    
    grad = Image.new('RGBA', (W, H), (0,0,0,0))
    gd = ImageDraw.Draw(grad)
    for y in range(H):
        ratio = y / H
        r = int(18 * (1 - ratio) + 12 * ratio)
        g = int(22 * (1 - ratio) + 16 * ratio)
        b = int(34 * (1 - ratio) + 26 * ratio)
        gd.line([(0, y), (W, y)], fill=(r, g, b, 255))
        
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([200, 200, 1000, 1000], fill=(0, 82, 255, 60))
    glow = glow.filter(ImageFilter.GaussianBlur(100))
    grad = Image.alpha_composite(grad, glow)
    base.paste(grad, (0, 0), mask)
    
    # Pristine Flawless Dark Phone
    phone = Image.open('portfolio/mockup_dark_home_flawless.png').convert('RGBA')
    pw = 480
    ph = int(phone.height * (pw / phone.width))
    phone = phone.resize((pw, ph), Image.Resampling.LANCZOS)
    
    sh = Image.new('RGBA', (W, H), (0,0,0,0))
    shd = ImageDraw.Draw(sh)
    shd.ellipse([240, 930, 240 + pw, 1040], fill=(0, 0, 0, 255))
    sh = sh.filter(ImageFilter.GaussianBlur(40))
    base = Image.alpha_composite(base, sh)
    base.paste(phone, (240, 110), phone)
    
    draw = ImageDraw.Draw(base)
    f_cat = get_font(18, bold=True)
    f_title = get_font(46, bold=True)
    f_sub = get_font(21, bold=False)
    
    tx = 860
    draw.text((tx, 180), "09. OLED DEEP DARK & ACCESSIBILITY", font=f_cat, fill=(0, 210, 255))
    draw.text((tx, 230), "야간 장세 트레이더를 위한\n고대비 다크 테마 시스템", font=f_title, fill=(255, 255, 255), spacing=18)
    draw.text((tx, 380), "Designed for night trading volatility\n7:1 이상의 WCAG 2.1 AAA 명도 대비를 준수하여\n급박한 야간 해외주식·가상자산 장세에서도 오독 없는 수치 가독성 보장.", font=f_sub, fill=(180, 195, 215), spacing=10)
    
    specs = [
        ("시맨틱 컬러 토큰 매핑", "Primary Electric (#0052FF), Mint (#00E676), Coral (#FF5252), Gold (#FFB300)"),
        ("Tabular Numbers 고정폭 폰트", "JetBrains Mono의 'tnum' 속성을 적용하여 실시간 가격 변동 시 레이아웃 무흔들림"),
        ("24시간 VIP 광고 제어 모델", "보상형 동영상 1회 시청 시 24시간 동안 배너 및 전면 광고 100% 제거")
    ]
    sy = 550
    for title, desc in specs:
        draw.rounded_rectangle([tx, sy, tx + 920, sy + 90], radius=18, fill=(255, 255, 255, 255))
        draw.text((tx + 28, sy + 18), title, font=get_font(18, bold=True), fill=(0, 82, 255))
        draw.text((tx + 28, sy + 50), desc, font=get_font(14, bold=False), fill=(71, 85, 105))
        sy += 112
        
    base.save('portfolio/behance_slides/slide_11.png')
    print("SAVED slide_11.png")

# ==============================================================
# SLIDE 12: Quantitative Impact & STAR Retrospective
# ==============================================================
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
    gw.ellipse([1100, 200, 1800, 900], fill=(0, 82, 255, 80))
    gw.ellipse([200, 400, 800, 1000], fill=(0, 230, 118, 50))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    grad = Image.alpha_composite(grad, glow)
    base.paste(grad, (0, 0), mask)
    
    draw = ImageDraw.Draw(base)
    f_cat = get_font(18, bold=True)
    f_title = get_font(44, bold=True)
    
    draw.text((140, 95), "10. BUSINESS IMPACT & STAR RETROSPECTIVE", font=f_cat, fill=(0, 210, 255))
    draw.text((140, 135), "정량적 비즈니스 성과 및 STAR 회고", font=f_title, fill=(255, 255, 255))
    
    # 3 High-contrast Metric Cards
    metrics = [
        ("0.2 sec", "STT 음성 수치 파싱 속도", "키보드 타이핑 대비 입력 소요 시간 78% 단축"),
        ("100%", "Goal Seeking 수학적 정밀도", "부동소수점 오차 제로화 및 정밀 역산 도출"),
        ("60 fps", "실시간 슬라이더 반응성", "RepaintBoundary 최적화로 버벅임 없는 즉각 반응")
    ]
    mx = 140
    mw = 520
    mgap = 40
    for val, title, desc in metrics:
        draw.rounded_rectangle([mx, 220, mx + mw, 350], radius=20, fill=(255, 255, 255, 255))
        draw.text((mx + 28, 240), val, font=get_font(38, bold=True), fill=(0, 150, 100))
        draw.text((mx + 28, 290), title, font=get_font(18, bold=True), fill=(15, 23, 42))
        draw.text((mx + 28, 318), desc, font=get_font(14, bold=False), fill=(100, 116, 139))
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
    f_body = get_font(15, bold=False)
    for phase, content, color in star_items:
        draw.rounded_rectangle([sx, 395, sx + sw, 925], radius=20, fill=(255, 255, 255, 255))
        # Header Badge
        draw.rounded_rectangle([sx + 20, 415, sx + sw - 20, 460], radius=12, fill=color)
        draw.text((sx + 35, 427), phase, font=get_font(16, bold=True), fill=(255, 255, 255))
        
        # Word Wrapped text
        wrapped_lines = wrap_text_by_words(content, f_body, sw - 56, draw)
        text_y = 485
        for line in wrapped_lines:
            draw.text((sx + 28, text_y), line, font=f_body, fill=(30, 41, 59))
            text_y += 28
        
        sx += sw + sgap
        
    base.save('portfolio/behance_slides/slide_12.png')
    print("SAVED slide_12.png")

if __name__ == '__main__':
    for i in range(1, 13):
        func_name = f"make_slide_{i:02d}"
        if func_name in globals():
            globals()[func_name]()
