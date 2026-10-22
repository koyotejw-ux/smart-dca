import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
CARD_PAD = 36
RADIUS = 44

os.makedirs('portfolio/behance_slides', exist_ok=True)

def get_font(size, bold=False):
    font_path = "C:/Windows/Fonts/malgunbd.ttf" if bold else "C:/Windows/Fonts/malgun.ttf"
    try:
        return ImageFont.truetype(font_path, int(size))
    except:
        return ImageFont.load_default()

def get_num_font(size, bold=True):
    font_path = "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"
    try:
        return ImageFont.truetype(font_path, int(size))
    except:
        return get_font(size, bold)

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
# SLIDE 01: Hero Cover & Value Proposition
# ==============================================================
def make_slide_01():
    base, mask = create_card_canvas((18, 52, 210, 255))
    
    grad = Image.new('RGBA', (W, H), (0,0,0,0))
    g_draw = ImageDraw.Draw(grad)
    for y in range(H):
        ratio = y / H
        r = int(14 * (1 - ratio) + 8 * ratio)
        g = int(48 * (1 - ratio) + 20 * ratio)
        b = int(210 * (1 - ratio) + 140 * ratio)
        g_draw.line([(0, y), (W, y)], fill=(r, g, b, 255))
    
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([1020, 50, 1860, 950], fill=(0, 210, 255, 95))
    gw.ellipse([260, 480, 1100, 1200], fill=(120, 30, 230, 75))
    gw.ellipse([1350, 600, 1850, 1100], fill=(255, 0, 128, 60))
    glow = glow.filter(ImageFilter.GaussianBlur(110))
    grad = Image.alpha_composite(grad, glow)
    base.paste(grad, (0, 0), mask)
    
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
    shd.ellipse([1270, 880, 1680, 995], fill=(0, 0, 0, 170))
    shd.ellipse([1000, 890, 1450, 1015], fill=(0, 0, 0, 230))
    sh = sh.filter(ImageFilter.GaussianBlur(35))
    base = Image.alpha_composite(base, sh)
    
    base.paste(phone_back, (1270, 135), phone_back)
    base.paste(phone_front, (1000, 85), phone_front)
    
    # 3D Squircle Icon
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
    
    # Category Pill
    d_ov.rounded_rectangle([140, 165, 540, 218], radius=26, fill=(255, 255, 255, 45), outline=(255, 255, 255, 80), width=1)
    d_ov.text((168, 182), "SMART DCA AVERAGE DOWN CALCULATOR", font=get_font(14, bold=True), fill=(255, 255, 255, 255))
    
    # Main Headline with High Visual Contrast
    f_title = get_font(52, bold=True)
    d_ov.text((140, 248), "하락장 속 뇌동매매를 막는\n알고리즘 분할매수 솔루션", font=f_title, fill=(255, 255, 255, 255), spacing=16)
    
    # Subhead
    f_sub = get_font(21, bold=False)
    d_ov.text((140, 420), "Stop Panic Selling. Start Algorithmic Scaling.\n0.2초 음성 인식과 Goal Seeking 수학 역산으로 계좌 손실을 정밀 방어합니다.", font=f_sub, fill=(215, 232, 255, 255), spacing=10)
    
    # 3 Glassmorphic Metric Cards with Generous Margins
    metrics = [
        ("0.2s", "STT 음성 인제스천", "호가 급락 시 1초 음성으로 매수 단가·수량 즉시 파싱"),
        ("100%", "Goal Seeking 수학 역산", "희망 목표 평단가 도달 필수 추가 매수량 폐쇄형 산출"),
        ("24h", "VIP 무광고 라이프사이클", "보상형 광고 1회 시청 시 24시간 동안 배너 및 전면 광고 100% 제거")
    ]
    cy = 570
    for val, title, desc in metrics:
        d_ov.rounded_rectangle([140, cy, 840, cy + 92], radius=20, fill=(255, 255, 255, 245), outline=(255, 255, 255, 255), width=2)
        d_ov.rounded_rectangle([140, cy + 20, 146, cy + 72], radius=3, fill=(0, 81, 255))
        d_ov.text((170, cy + 22), val, font=get_num_font(34, bold=True), fill=(0, 81, 255))
        d_ov.text((295, cy + 22), title, font=get_font(18, bold=True), fill=(15, 23, 42))
        d_ov.text((295, cy + 52), desc, font=get_font(13.5, bold=False), fill=(100, 116, 139))
        cy += 108
        
    d_ov.text((140, 925), "Lead Product Designer & Senior Flutter Engineer  ·  Production Store Verified", font=get_font(16, bold=True), fill=(210, 230, 255, 255))
    
    base = Image.alpha_composite(base, overlay)
    base.save('portfolio/behance_slides/slide_01.png')
    print("SAVED slide_01.png")

# ==============================================================
# SLIDE 02: Discovery & User Research (Pain Points + IDI Data)
# ==============================================================
def make_slide_02():
    base, mask = create_card_canvas((248, 250, 254, 255))
    draw = ImageDraw.Draw(base)
    
    f_cat = get_font(18, bold=True)
    f_title = get_font(44, bold=True)
    f_sub = get_font(20, bold=False)
    
    draw.text((140, 95), "01. DISCOVERY & USER RESEARCH", font=f_cat, fill=(0, 81, 255))
    draw.text((140, 133), "손실 회피 편향과 감정적 물타기의 한계", font=f_title, fill=(15, 23, 42))
    draw.text((140, 195), "개인 투자자 12명 심층 인터뷰(IDI) 및 커뮤니티 데이터 분석을 통해 도출한 3대 핵심 결핍", font=f_sub, fill=(100, 116, 139))
    
    # Left 3 Stat Boxes with Generous Padding
    stats = [
        ("78.4%", "하락장 뇌동매매 경험률", "수학적 계획 없는 감정적 추가 매수 집행", 0.784, (239, 68, 68)),
        ("4.8분", "기존 계산기 수동 입력 소요", "소수점 단가·수량 타이핑 중 호가 급변", 0.65, (245, 158, 11)),
        ("0건", "MTS 내 목표 역산 기능 부재", "본전 탈출 필요 수량을 알지 못한 채 과매수", 0.0, (0, 81, 255))
    ]
    sx = 140
    sy = 265
    sw = 460
    for val, stitle, sdesc, prog, pcol in stats:
        draw.rounded_rectangle([sx, sy, sx + sw, sy + 195], radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw.rounded_rectangle([sx + 30, sy + 24, sx + 135, sy + 54], radius=10, fill=(240, 244, 255))
        draw.text((sx + 45, sy + 30), "STAT DATA", font=get_font(12, bold=True), fill=(0, 81, 255))
        
        num_str = "".join([c for c in val if c.isdigit() or c in ['.', '%', '+', '-']])
        unit_str = val.replace(num_str, "")
        draw.text((sx + 30, sy + 66), num_str, font=get_num_font(42, bold=True), fill=pcol)
        nw = draw.textlength(num_str, font=get_num_font(42, bold=True))
        if unit_str:
            draw.text((sx + 30 + nw + 4, sy + 78), unit_str, font=get_font(24, bold=True), fill=pcol)
            
        draw.text((sx + 30, sy + 128), stitle, font=get_font(18, bold=True), fill=(15, 23, 42))
        draw.text((sx + 30, sy + 156), sdesc, font=get_font(13.5, bold=False), fill=(100, 116, 139))
        
        if prog > 0:
            draw.rounded_rectangle([sx + 30, sy + 118, sx + sw - 30, sy + 123], radius=3, fill=(241, 245, 249))
            draw.rounded_rectangle([sx + 30, sy + 118, sx + 30 + int((sw - 60) * prog), sy + 123], radius=3, fill=pcol)
            
        sy += 225
        
    cards = [
        ("PAIN POINT 01", "전략 부재: 비중만 비대해지고 평단은 거의 내려오지 않음",
         "\"단가를 낮추려고 예수금을 계속 넣었는데, 나중에 보니 계좌의 80%가 한 종목에 묶여있고 평단은 2%밖에 안 내려왔어요.\"\n— 3년 차 개인 투자자 IDI 인터뷰 내용 중",
         "추가 매수 차수별 한계 효용 및 계좌 잠식 위험도 실시간 가시화", (239, 68, 68)),
        
        ("PAIN POINT 02", "조작 지연: 급변하는 호가창 앞에서 타이핑하다 골든타임 상실",
         "\"급락 빔이 쏟아질 때 평단 계산하려고 키패드로 8자리 단가를 치는 동안 이미 반등해버리거나 더 밑으로 뚫려버립니다.\"\n— 가상자산/단타 트레이더 IDI 인터뷰 내용 중",
         "0.2초 STT 음성 자동 파싱 및 ±5% 원터치 프리셋 칩 즉각 주입", (245, 158, 11)),
         
        ("PAIN POINT 03", "출구 전략 부재: 목표 탈출가에 도달하기 위한 필요 매수량 미제공",
         "\"본전이나 -5% 선에서 정리하고 싶은데, 지금 얼마를 더 사야 그 평단이 만들어지는지 알려주는 앱이 전혀 없습니다.\"\n— 5년 차 직장인 스윙 투자자 IDI 인터뷰 내용 중",
         "Goal Seeking Closed Form 수학 공식을 통한 목표 도달 수량 정밀 역산", (16, 185, 129))
    ]
    
    rx = 640
    ry = 265
    rw = 1140
    for ptag, ptitle, pquote, psol, pcolor in cards:
        draw.rounded_rectangle([rx, ry, rx + rw, ry + 195], radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw.rounded_rectangle([rx, ry + 22, rx + 6, ry + 173], radius=3, fill=pcolor)
        
        draw.rounded_rectangle([rx + 30, ry + 22, rx + 160, ry + 52], radius=10, fill=(pcolor[0], pcolor[1], pcolor[2], 30))
        draw.text((rx + 42, ry + 28), ptag, font=get_font(12, bold=True), fill=pcolor)
        draw.text((rx + 175, ry + 26), ptitle, font=get_font(18, bold=True), fill=(15, 23, 42))
        
        # Quote Box with 30px Safety Margins
        draw.rounded_rectangle([rx + 30, ry + 64, rx + rw - 30, ry + 134], radius=12, fill=(248, 250, 252))
        lines = wrap_text_by_words(pquote, get_font(13.5, bold=False), rw - 90, draw)
        qy = ry + 74
        for line in lines[:2]:
            draw.text((rx + 45, qy), line, font=get_font(13.5, bold=False), fill=(71, 85, 105))
            qy += 24
            
        # Solution Pill & Text
        draw.rounded_rectangle([rx + 30, ry + 148, rx + 120, ry + 176], radius=6, fill=(238, 242, 255))
        draw.text((rx + 38, ry + 154), "SOLUTION", font=get_font(11, bold=True), fill=(0, 81, 255))
        draw.text((rx + 132, ry + 152), psol, font=get_font(14, bold=True), fill=(15, 23, 42))
        ry += 225
        
    base.save('portfolio/behance_slides/slide_02.png')
    print("SAVED slide_02.png")

# ==============================================================
# SLIDE 03: Benchmark Matrix & Personas (Margin & Overflow Fixed!)
# ==============================================================
def make_slide_03():
    base, mask = create_card_canvas((248, 250, 254, 255))
    draw = ImageDraw.Draw(base)
    
    f_cat = get_font(18, bold=True)
    f_title = get_font(44, bold=True)
    f_sub = get_font(20, bold=False)
    
    draw.text((140, 95), "02. BENCHMARK & TARGET PERSONAS", font=f_cat, fill=(0, 81, 255))
    draw.text((140, 133), "경쟁사 벤치마킹 매트릭스 및 핵심 페르소나 정의", font=f_title, fill=(15, 23, 42))
    draw.text((140, 195), "기존 MTS 및 일반 계산기 앱 대비 독보적인 사용자 편의성과 알고리즘 기능 우위", font=f_sub, fill=(100, 116, 139))
    
    # Expanded Table width (tw = 960) with 310px width dedicated to column 4!
    tx = 140
    ty = 265
    tw = 960
    draw.rounded_rectangle([tx, ty, tx + tw, ty + 655], radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    draw.rounded_rectangle([tx, ty, tx + tw, ty + 65], radius=24, fill=(241, 245, 249))
    draw.text((tx + 28, ty + 22), "비교 분석 항목", font=get_font(15, bold=True), fill=(71, 85, 105))
    draw.text((tx + 200, ty + 22), "증권사 MTS 내장", font=get_font(15, bold=True), fill=(71, 85, 105))
    draw.text((tx + 410, ty + 22), "일반 앱스토어 계산기", font=get_font(15, bold=True), fill=(71, 85, 105))
    
    # 4th Column Hero Box (Width = 325px, leaves 40px right padding inside!)
    col4_left = tx + 625
    col4_right = tx + tw - 12
    draw.rounded_rectangle([col4_left, ty + 10, col4_right, ty + 645], radius=18, fill=(240, 246, 255), outline=(186, 215, 255), width=2)
    draw.rounded_rectangle([col4_left + 15, ty + 16, col4_right - 15, ty + 56], radius=12, fill=(0, 81, 255))
    draw.text((col4_left + 45, ty + 24), "스마트 물타기 계산기", font=get_font(14, bold=True), fill=(255, 255, 255))
    
    matrix = [
        ("입력 방식", "키패드 수동 입력 (느림)", "키패드 수동 입력 (광고 다수)", "멀티모달 (AI 음성 + 원터치 칩)"),
        ("연산 속도", "3~5초 (복잡한 메뉴 이동)", "2~3초 (단순 합산)", "0.2초 즉시 파싱 및 자동 연산"),
        ("시나리오 비교", "불가능 (단일 계산)", "불가능 (1회성 소멸)", "A vs B 전략 대조 매트릭스"),
        ("목표가 역산", "미지원", "미지원", "Goal Seeking 폐쇄형 역산 알고리즘"),
        ("보안/저장", "동작 로그인 필수 (지연)", "세션 종료 시 초기화", "Local-First NoSQL 100% 영속화"),
        ("광고 모델", "금융 상품 배너 혼재", "전면 강제 팝업 (피로도 극심)", "24시간 VIP 무광고 라이프사이클"),
        ("다크 테마", "일부 지원 (가독성 낮음)", "단순 그레이스케일 반전", "OLED 고대비 WCAG AAA 토큰")
    ]
    
    row_y = ty + 75
    for item, c1, c2, c3 in matrix:
        draw.line([(tx + 20, row_y), (col4_left - 15, row_y)], fill=(241, 245, 249), width=1)
        draw.text((tx + 28, row_y + 20), item, font=get_font(14.5, bold=True), fill=(15, 23, 42))
        draw.text((tx + 200, row_y + 20), c1, font=get_font(13, bold=False), fill=(100, 116, 139))
        draw.text((tx + 410, row_y + 20), c2, font=get_font(13, bold=False), fill=(100, 116, 139))
        
        # 4th Column Content with Safe 35px Margins inside Box!
        draw.ellipse([col4_left + 16, row_y + 24, col4_left + 24, row_y + 32], fill=(0, 81, 255))
        draw.text((col4_left + 32, row_y + 19), c3, font=get_font(12.5, bold=True), fill=(0, 81, 255))
        row_y += 80
        
    px = 1140
    py = 265
    pw = 640
    
    # Persona A
    draw.rounded_rectangle([px, py, px + pw, py + 312], radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([px + 30, py + 25, px + 150, py + 58], radius=12, fill=(240, 246, 255))
    draw.text((px + 45, py + 33), "PERSONA A", font=get_font(13, bold=True), fill=(0, 81, 255))
    draw.text((px + 170, py + 30), "김투자 (34세, 대기업 직장인)", font=get_font(20, bold=True), fill=(15, 23, 42))
    
    draw.text((px + 30, py + 78), "\"월급날마다 분할 매수해서 6개월 안에 본전 탈출하고 싶어요.\"", font=get_font(16, bold=True), fill=(0, 81, 255))
    desc_a = [
        "• 성향: 국내 대형 우량주 및 미국 지수 ETF 장기 분할 투자",
        "• 행동: 업무 중 급락 알림을 볼 때 감정적 추매를 지양하고 체계적 대응 시도",
        "• 핵심 니즈: 총예산 대비 특정 종목 편중 비율 및 A/B 시나리오 평단 만족도 대조"
    ]
    dy = py + 125
    for d in desc_a:
        draw.text((px + 30, dy), d, font=get_font(13.5, bold=False), fill=(71, 85, 105))
        dy += 34
        
    # Persona B
    py += 342
    draw.rounded_rectangle([px, py, px + pw, py + 312], radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([px + 30, py + 25, px + 150, py + 58], radius=12, fill=(254, 243, 199))
    draw.text((px + 45, py + 33), "PERSONA B", font=get_font(13, bold=True), fill=(217, 119, 6))
    draw.text((px + 170, py + 30), "박스캘퍼 (28세, 크립토/단타 트레이더)", font=get_font(20, bold=True), fill=(15, 23, 42))
    
    draw.text((px + 30, py + 78), "\"급락 빔 맞았을 때 3초 안에 평단 뽑아서 지지선에서 나와야 해요.\"", font=get_font(16, bold=True), fill=(217, 119, 6))
    desc_b = [
        "• 성향: 고변동성 알트코인 및 테마주 단타/스캘핑 매매",
        "• 행동: 손가락으로 타이핑할 시간이 없어 음성으로 단가/수량을 즉각 주입",
        "• 핵심 니즈: 목표 탈출 가격에 도달하기 위한 필요 매수 수량을 0.01초 만에 역산"
    ]
    dy = py + 125
    for d in desc_b:
        draw.text((px + 30, dy), d, font=get_font(13.5, bold=False), fill=(71, 85, 105))
        dy += 34
        
    base.save('portfolio/behance_slides/slide_03.png')
    print("SAVED slide_03.png")

# ==============================================================
# SLIDE 04: Information Architecture & Customer Journey (CJM)
# ==============================================================
def make_slide_04():
    base, mask = create_card_canvas((15, 23, 42, 255))
    draw = ImageDraw.Draw(base)
    
    f_cat = get_font(18, bold=True)
    f_title = get_font(44, bold=True)
    f_sub = get_font(20, bold=False)
    
    draw.text((140, 95), "03. INFORMATION ARCHITECTURE & USER JOURNEY", font=f_cat, fill=(0, 210, 255))
    draw.text((140, 133), "4단계 모듈형 정보 구조 설계 (IA) & CJM", font=f_title, fill=(255, 255, 255))
    draw.text((140, 195), "진입 온보딩부터 실시간 연산, 포트폴리오 리포트 영속화까지 끊김 없는 4대 도메인 트리 구조", font=f_sub, fill=(148, 163, 184))
    
    stages = [
        ("Phase 1. 급락 인지", "종목 급락 (-10%) 발생\n손실 공포 & 뇌동매매 충동", (0, 81, 255)),
        ("Phase 2. 탐색 & 인제스천", "앱 실행 후 0.2초 음성 입력\n원터치 프리셋 칩 즉시 주입", (0, 210, 255)),
        ("Phase 3. 알고리즘 시뮬레이션", "A vs B 분할 시나리오 대조\n목표 평단가 도달 수량 역산", (139, 92, 246)),
        ("Phase 4. 확신 & 의사결정", "최적 매수 수량 및 일정 확정\n로컬 DB 저장 및 심리적 안정", (16, 185, 129))
    ]
    jx = 140
    jw = 390
    jgap = 26
    for stitle, sdesc, scolor in stages:
        draw.rounded_rectangle([jx, 260, jx + jw, 355], radius=16, fill=(30, 41, 59), outline=(scolor[0], scolor[1], scolor[2], 120), width=2)
        draw.rounded_rectangle([jx + 16, 276, jx + 22, 338], radius=3, fill=scolor)
        draw.text((jx + 32, 276), stitle, font=get_font(16, bold=True), fill=scolor)
        draw.text((jx + 32, 306), sdesc, font=get_font(13.5, bold=False), fill=(203, 213, 225), spacing=4)
        jx += jw + jgap
        
    cols = [
        ("01. DISCOVERY & INIT", "1.0 Entry & Onboarding", [
            ("1.1 Splash Screen Engine", "로고 스케일링 & 비전 초점 집중"),
            ("1.2 Strategy Onboarding (4 Steps)", "분할 매수 수학적 메커니즘 학습"),
            ("1.3 Locale & Currency Auto Detect", "디바이스 국가 기반 통화/L10n 연동"),
            ("1.4 VIP Ad-Free Token Activation", "24시간 무광고 라이프사이클 구축")
        ], (0, 81, 255)),
        
        ("02. CORE DASHBOARD", "2.0 Home & Ingestion", [
            ("2.1 Multimodal Voice Panel", "Google STT 온디바이스 실시간 파싱"),
            ("2.2 Quick Action Preset Chips", "±5%, ±10%, -20% 호가 즉각 주입"),
            ("2.3 Asset Portfolio Carousel", "보유 자산 실시간 평단/수량 요약"),
            ("2.4 Quick Dock Router", "자산 추가 / 시뮬레이터 / 리포트 진입")
        ], (0, 210, 255)),
        
        ("03. ALGORITHM CORE", "3.0 Simulation Engine", [
            ("3.1 Multi-Batch Simulator", "1~N차 가중평균 Closed Form 연산"),
            ("3.2 A/B Scenario Comparator", "전략별 평단 방어 효율 동시 대조"),
            ("3.3 Goal Seeking Calculator", "희망 평단가 도달 필수 매수량 역산"),
            ("3.4 Interactive Capital Slider", "예산 제약 내 실시간 최적 평단 피드백")
        ], (245, 158, 11)),
        
        ("04. PERSISTENCE & UTILITY", "4.0 Analytics & Settings", [
            ("4.1 Local-First SQLite & Hive", "100% 로컬 암호화 오프라인 저장"),
            ("4.2 Diagnostic Report Export", "PNG/텍스트 시나리오 진단 카드 공유"),
            ("4.3 WCAG 2.1 AAA Dark System", "야간 장세 트레이더 고대비 토큰"),
            ("4.4 Compliance & Help Guide", "GDPR/개인정보 처리 및 주식 FAQ")
        ], (139, 92, 246))
    ]
    
    cx = 140
    cw = 390
    cgap = 26
    for tag, ctitle, items, ccolor in cols:
        draw.rounded_rectangle([cx, 385, cx + cw, 940], radius=20, fill=(30, 41, 59), outline=(ccolor[0], ccolor[1], ccolor[2], 120), width=2)
        draw.rounded_rectangle([cx + 20, 405, cx + cw - 20, 455], radius=12, fill=(20, 29, 44), outline=(ccolor[0], ccolor[1], ccolor[2], 80), width=1)
        draw.text((cx + 35, 413), tag, font=get_font(12, bold=True), fill=ccolor)
        draw.text((cx + 35, 431), ctitle, font=get_font(15, bold=True), fill=(255, 255, 255))
        
        iy = 475
        for ititle, idesc in items:
            draw.rounded_rectangle([cx + 20, iy, cx + cw - 20, iy + 92], radius=14, fill=(15, 23, 42), outline=(51, 65, 85), width=1)
            draw.ellipse([cx + 36, iy + 22, cx + 44, iy + 30], fill=ccolor)
            draw.text((cx + 54, iy + 16), ititle, font=get_font(14, bold=True), fill=(255, 255, 255))
            draw.text((cx + 54, iy + 45), idesc, font=get_font(12.5, bold=False), fill=(148, 163, 184))
            iy += 110
            
        cx += cw + cgap
        
    base.save('portfolio/behance_slides/slide_04.png')
    print("SAVED slide_04.png")

# ==============================================================
# SLIDE 05: User Flowchart & Edge Case Logic Branch (Clean Arrows!)
# ==============================================================
def make_slide_05():
    base, mask = create_card_canvas((248, 250, 254, 255))
    draw = ImageDraw.Draw(base)
    
    f_cat = get_font(18, bold=True)
    f_title = get_font(44, bold=True)
    f_sub = get_font(20, bold=False)
    
    draw.text((140, 95), "04. USER FLOWCHART & LOGIC BRANCH", font=f_cat, fill=(0, 81, 255))
    draw.text((140, 133), "사용자 행동 및 예외 처리 로직 플로우차트", font=f_title, fill=(15, 23, 42))
    draw.text((140, 195), "앱 실행부터 STT 권한 거부, 역산 불가 엣지 케이스, VIP 무광고 분기까지의 정밀한 상태 전이", font=f_sub, fill=(100, 116, 139))
    
    bx = 140
    by = 265
    bw = 1640
    bh = 660
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
    
    cols = [
        ("STAGE 1 : Launch & Init", [
            ("Launch App", "Splash Screen 로드", False),
            ("Check First Run?", "최초 실행 여부 분기", True),
            ("4-Step Onboarding", "원리 가이드 완료", False)
        ]),
        ("STAGE 2 : VIP & Dashboard", [
            ("VIP Active Check", "24h 무광고 토큰 검사", True),
            ("Pass (Skip Ad)", "광고 생략 후 즉시 진입", False),
            ("Main Dashboard", "자산 요약 & 퀵 로드", False)
        ]),
        ("STAGE 3 : Input Multimodal", [
            ("Tap Voice Mic", "STT 마이크 스트림 활성", False),
            ("STT Success?", "자연어 파싱 성공 분기", True),
            ("Fallback Preset Chip", "±5%, ±10% 칩 수동 선택", False)
        ]),
        ("STAGE 4 : Algorithm Engine", [
            ("Select Mode", "단일 / A-B / 목표 역산", True),
            ("Goal Seeking Calc", "Closed-Form 역산 수행", False),
            ("Target >= Current?", "엣지 케이스 역산 오류 방어", True)
        ]),
        ("STAGE 5 : Output & Save", [
            ("Show Result Card", "평단가 및 필요 수량 출력", False),
            ("Save to SQLite", "로컬 DB 스냅샷 저장", False),
            ("Share Report", "진단 이미지 외부 공유", False)
        ])
    ]
    
    cx = bx + 40
    col_w = 275
    cgap = 42
    
    for stitle, steps in cols:
        draw.text((cx, by + 35), stitle, font=get_font(13.5, bold=True), fill=(0, 81, 255))
        draw.line([(cx, by + 65), (cx + col_w, by + 65)], fill=(226, 232, 240), width=1)
        
        sy = by + 90
        for step_idx, (title, desc, is_cond) in enumerate(steps):
            if is_cond:
                draw.rounded_rectangle([cx, sy, cx + col_w, sy + 86], radius=16, fill=(255, 247, 237), outline=(249, 115, 22), width=2)
                draw.text((cx + 18, sy + 18), "◆ " + title, font=get_font(14.5, bold=True), fill=(194, 65, 12))
                draw.text((cx + 18, sy + 48), desc, font=get_font(12.5, bold=False), fill=(154, 52, 18))
            else:
                draw.rounded_rectangle([cx, sy, cx + col_w, sy + 86], radius=16, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
                draw.text((cx + 18, sy + 18), "■ " + title, font=get_font(14.5, bold=True), fill=(15, 23, 42))
                draw.text((cx + 18, sy + 48), desc, font=get_font(12.5, bold=False), fill=(100, 116, 139))
            
            # Draw vertical arrow ONLY between step 1->2 and 2->3, NEVER after step 3!
            if step_idx < len(steps) - 1:
                draw.line([(cx + col_w // 2, sy + 86), (cx + col_w // 2, sy + 115)], fill=(148, 163, 184), width=2)
                draw.polygon([(cx + col_w // 2 - 4, sy + 110), (cx + col_w // 2 + 4, sy + 110), (cx + col_w // 2, sy + 116)], fill=(148, 163, 184))
            sy += 142
            
        # Horizontal flow connector to next stage
        draw.line([(cx + col_w, by + 300), (cx + col_w + cgap, by + 300)], fill=(0, 81, 255), width=2)
        draw.polygon([(cx + col_w + cgap - 6, by + 296), (cx + col_w + cgap - 6, by + 304), (cx + col_w + cgap, by + 300)], fill=(0, 81, 255))
        cx += col_w + cgap
        
    # Safe Bottom Info Bar
    draw.rounded_rectangle([bx + 40, by + bh - 72, bx + bw - 40, by + bh - 20], radius=12, fill=(240, 246, 255))
    draw.rounded_rectangle([bx + 55, by + bh - 60, bx + 165, by + bh - 32], radius=6, fill=(0, 81, 255))
    draw.text((bx + 63, by + bh - 55), "EDGE DEFENSE", font=get_font(11, bold=True), fill=(255, 255, 255))
    draw.text((bx + 178, by + bh - 54), "목표 평단가가 현재가보다 낮은 불가능 수치 입력 시 즉시 경고 토스트 팝업 및 가용 예수금 내 달성 가능 수치 자동 추천", font=get_font(13.5, bold=False), fill=(15, 23, 42))
    
    base.save('portfolio/behance_slides/slide_05.png')
    print("SAVED slide_05.png")

# ==============================================================
# SLIDE 06: Wireframe Blueprint & Functional Specs (Overflow Fixed!)
# ==============================================================
def make_slide_06():
    base, mask = create_card_canvas((248, 250, 254, 255))
    draw = ImageDraw.Draw(base)
    
    f_cat = get_font(18, bold=True)
    f_title = get_font(44, bold=True)
    f_sub = get_font(20, bold=False)
    
    draw.text((140, 95), "05. WIREFRAME & STRUCTURAL RATIONALE", font=f_cat, fill=(0, 81, 255))
    draw.text((140, 133), "와이어프레임 구조 설계 및 기능 1:1 매핑 명세", font=f_title, fill=(15, 23, 42))
    draw.text((140, 195), "시각적 스킨(Visual Skin) 이전에 사용자의 인지 부하(Cognitive Load)를 최소화한 3대 핵심 화면 골격", font=f_sub, fill=(100, 116, 139))
    
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
        draw.rounded_rectangle([wx, 260, wx + ww, 940], radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
        draw.text((wx + 30, 288), title, font=get_font(18, bold=True), fill=(15, 23, 42))
        
        # Lo-Fi Blueprint Box
        draw.rounded_rectangle([wx + 30, 325, wx + ww - 30, 560], radius=16, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
        draw.rounded_rectangle([wx + 50, 345, wx + ww - 50, 375], radius=8, fill=(219, 234, 254))
        draw.rounded_rectangle([wx + 50, 390, wx + ww - 50, 430], radius=10, fill=(226, 232, 240))
        draw.rounded_rectangle([wx + 50, 445, wx + 240, 495], radius=12, fill=(203, 213, 225))
        draw.rounded_rectangle([wx + 260, 445, wx + ww - 50, 495], radius=12, fill=(203, 213, 225))
        draw.rounded_rectangle([wx + 50, 510, wx + ww - 50, 540], radius=8, fill=(186, 215, 255))
        draw.text((wx + 185, 462), "Lo-Fi Blueprint Schema", font=get_font(12, bold=True), fill=(100, 116, 139))
        
        # Spec List with Strict Width Control (No overflow!)
        sy = 585
        for s_title, s_desc in specs:
            draw.text((wx + 30, sy), s_title, font=get_font(13.5, bold=True), fill=(0, 81, 255))
            # Wrap description if needed inside ww - 55
            lines = wrap_text_by_words(s_desc, get_font(12.5, bold=False), ww - 65, draw)
            draw.text((wx + 30, sy + 20), lines[0], font=get_font(12.5, bold=False), fill=(71, 85, 105))
            sy += 54
            
        wx += ww + wgap
        
    base.save('portfolio/behance_slides/slide_06.png')
    print("SAVED slide_06.png")

# ==============================================================
# SLIDE 07: Design System Foundations & Semantic Tokens (Overflow Fixed!)
# ==============================================================
def make_slide_07():
    base, mask = create_card_canvas((15, 23, 42, 255))
    draw = ImageDraw.Draw(base)
    
    f_cat = get_font(18, bold=True)
    f_title = get_font(44, bold=True)
    f_sub = get_font(20, bold=False)
    
    draw.text((140, 95), "06. DESIGN SYSTEM & W3C TOKENS", font=f_cat, fill=(0, 210, 255))
    draw.text((140, 133), "디자인 시스템 파운데이션 및 시맨틱 토큰 매핑", font=f_title, fill=(255, 255, 255))
    draw.text((140, 195), "W3C 표준 JSON 토큰, WCAG 2.1 AAA 고대비 컬러, Tabular Numbers 고정폭 폰트 위계 체계", font=f_sub, fill=(148, 163, 184))
    
    # Left: Color Palette
    draw.rounded_rectangle([140, 260, 900, 940], radius=24, fill=(30, 41, 59), outline=(51, 65, 85), width=2)
    draw.text((170, 290), "Color Palette & Semantic Tokens", font=get_font(20, bold=True), fill=(255, 255, 255))
    draw.text((170, 320), "tokens.json 기반 실시간 테마 바인딩 (WCAG 2.1 AAA 7:1 대비 준수)", font=get_font(14, bold=False), fill=(148, 163, 184))
    
    colors = [
        ("Electric Blue", "#0051FF", "Brand Primary", (0, 81, 255)),
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
            draw.text((box_x + 105, cy + 12), cname, font=get_font(16, bold=True), fill=(255, 255, 255))
            draw.text((box_x + 105, cy + 38), chex, font=get_font(14, bold=True), fill=(0, 210, 255))
            draw.text((box_x + 105, cy + 62), cdesc, font=get_font(12, bold=False), fill=(148, 163, 184))
        cy += 115
        
    # Right: Typography Scale & Elevated Spec Box
    draw.rounded_rectangle([940, 260, 1780, 940], radius=24, fill=(30, 41, 59), outline=(51, 65, 85), width=2)
    draw.text((970, 290), "Typography Scale & Layout Tokens", font=get_font(20, bold=True), fill=(255, 255, 255))
    draw.text((970, 320), "숫자 흔들림 방지 Tabular Numbers & 44px 터치 타깃 규격", font=get_font(14, bold=False), fill=(148, 163, 184))
    
    typos = [
        ("Display 32 / Bold", "₩ 1,480,000", "핵심 결과 평단가 및 수익 금액 (tnum 고정폭)"),
        ("HeadLine 24 / Bold", "+42.5주 추가 매수 필요", "Goal Seeking 역산 산출 결과 강조"),
        ("Title 18 / Bold", "호가 급락 시 원터치 분할 매수", "섹션 헤더 및 주요 카드 타이틀"),
        ("Body 15 / Regular", "급변하는 시장 변동성에 대비한 리스크 방어", "일반 본문 설명 및 툴팁 가이드")
    ]
    
    ty = 370
    for tscale, tex, tdesc in typos:
        draw.rounded_rectangle([970, ty, 1750, ty + 100], radius=16, fill=(15, 23, 42), outline=(51, 65, 85))
        draw.text((995, ty + 18), tscale, font=get_font(13.5, bold=True), fill=(0, 210, 255))
        draw.text((1180, ty + 16), tex, font=get_font(19, bold=True), fill=(255, 255, 255))
        draw.text((995, ty + 56), tdesc, font=get_font(13, bold=False), fill=(148, 163, 184))
        ty += 118
        
    # Clean Split Token Cards (NO OVERFLOW!)
    draw.rounded_rectangle([970, 850, 1345, 915], radius=14, fill=(15, 23, 42), outline=(51, 65, 85))
    draw.text((990, 863), "Corner Radius Spec", font=get_font(11, bold=True), fill=(0, 210, 255))
    draw.text((990, 883), "Card Radius 24px (Soft) · Pill 44px (Full)", font=get_font(13, bold=True), fill=(255, 255, 255))
    
    draw.rounded_rectangle([1375, 850, 1750, 915], radius=14, fill=(15, 23, 42), outline=(51, 65, 85))
    draw.text((1395, 863), "Elevation & Shadow Spec", font=get_font(11, bold=True), fill=(0, 230, 118))
    draw.text((1395, 883), "Ambient Drop Shadow y=8, blur=20", font=get_font(13, bold=True), fill=(255, 255, 255))
    
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
    gw.ellipse([700, 150, 1300, 850], fill=(0, 81, 255, 80))
    gw.ellipse([1200, 200, 1800, 800], fill=(139, 92, 246, 60))
    gw.ellipse([100, 100, 700, 700], fill=(0, 210, 255, 50))
    glow = glow.filter(ImageFilter.GaussianBlur(110))
    grad = Image.alpha_composite(grad, glow)
    base.paste(grad, (0, 0), mask)
    
    draw = ImageDraw.Draw(base)
    f_cat = get_font(18, bold=True)
    f_title = get_font(40, bold=True)
    f_sub = get_font(18, bold=False)
    
    # Left Header: Clean 2-line layout that never overlaps center phone
    draw.text((140, 95), "07. FEATURE SPOTLIGHT 01 · MULTIMODAL INGESTION", font=f_cat, fill=(0, 210, 255))
    draw.text((140, 132), "말 한마디로 단가와 수량을\n0.2초 즉각 분리 추출", font=f_title, fill=(255, 255, 255), spacing=10)
    draw.text((140, 242), "급락 호가창 앞에서 타이핑 지연 없이\n매수 골든타임 슬리피지를 원천 방어", font=f_sub, fill=(215, 230, 255), spacing=6)
    
    # Right Header: Engine Spec Banner with 25px Padding
    draw.rounded_rectangle([1220, 110, 1780, 275], radius=20, fill=(24, 32, 50, 240), outline=(0, 210, 255, 120), width=1)
    draw.rounded_rectangle([1245, 130, 1375, 158], radius=8, fill=(0, 81, 255))
    draw.text((1257, 135), "ON-DEVICE STT", font=get_font(12, bold=True), fill=(255, 255, 255))
    draw.text((1390, 133), "0.2s 하이브리드 파싱 파이프라인", font=get_font(17, bold=True), fill=(255, 255, 255))
    draw.text((1245, 175), "Google STT 온디바이스 엔진과 정밀 정규식 토크나이저를\n결합하여 '종목명+단가+수량' 복합 발화를 오차 없이 분류합니다.", font=get_font(14, bold=False), fill=(180, 200, 225), spacing=5)
    
    # Center Phone Mockup
    phone = Image.open('portfolio/mockup_ko_08_voice.png').convert('RGBA')
    pw = 410
    ph = int(phone.height * (pw / phone.width))
    phone = phone.resize((pw, ph), Image.Resampling.LANCZOS)
    
    sh = Image.new('RGBA', (W, H), (0,0,0,0))
    shd = ImageDraw.Draw(sh)
    shd.ellipse([755, 910, 755 + pw, 1020], fill=(0, 0, 0, 240))
    sh = sh.filter(ImageFilter.GaussianBlur(35))
    base = Image.alpha_composite(base, sh)
    base.paste(phone, (755, 110), phone)
    
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
        draw.rounded_rectangle([140, cy + 22, 146, cy + 153], radius=3, fill=(0, 81, 255))
        draw.text((175, cy + 28), title, font=get_font(19, bold=True), fill=(15, 23, 42))
        lines = wrap_text_by_words(desc, get_font(14, bold=False), 440, draw)
        ly = cy + 68
        for l in lines:
            draw.text((175, ly), l, font=get_font(14, bold=False), fill=(71, 85, 105))
            ly += 24
        cy += 215
        
    cy = 340
    for title, desc in cards_r:
        draw.rounded_rectangle([1220, cy, 1780, cy + 175], radius=20, fill=(255, 255, 255, 245), outline=(255, 255, 255, 255), width=2)
        draw.rounded_rectangle([1220, cy + 22, 1226, cy + 153], radius=3, fill=(0, 210, 255))
        draw.text((1255, cy + 28), title, font=get_font(19, bold=True), fill=(15, 23, 42))
        lines = wrap_text_by_words(desc, get_font(14, bold=False), 440, draw)
        ly = cy + 68
        for l in lines:
            draw.text((1255, ly), l, font=get_font(14, bold=False), fill=(71, 85, 105))
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
    gw.ellipse([200, 200, 900, 900], fill=(0, 81, 255, 70))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    grad = Image.alpha_composite(grad, glow)
    base.paste(grad, (0, 0), mask)
    
    draw = ImageDraw.Draw(base)
    f_cat = get_font(18, bold=True)
    f_title = get_font(44, bold=True)
    f_sub = get_font(21, bold=False)
    
    draw.text((140, 95), "FINANCIAL ALGORITHM & MATH LOGIC", font=f_cat, fill=(0, 230, 180))
    draw.text((140, 133), "원하는 목표 평단가까지\n수학적으로 정확한 역산 제공", font=f_title, fill=(255, 255, 255), spacing=12)
    draw.text((140, 255), "수작업 엑셀 계산기의 한계를 극복하고, Goal-Seeking Closed Form 공식을\n적용하여 '추가 매수 가능 금액' 또는 '필요 매수 수량'을 0.01초 안에 즉시 도출합니다.", font=f_sub, fill=(180, 210, 215), spacing=8)
    
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
        draw.text((175, cy + 24), title, font=get_font(19, bold=True), fill=(10, 28, 36))
        lines = wrap_text_by_words(desc, get_font(14, bold=False), 700, draw)
        ly = cy + 62
        for l in lines:
            draw.text((175, ly), l, font=get_font(14, bold=False), fill=(60, 80, 90))
            ly += 24
        cy += 150
        
    phone = Image.open('portfolio/mockup_ko_03_target_filled.png').convert('RGBA')
    pw = 410
    ph = int(phone.height * (pw / phone.width))
    phone = phone.resize((pw, ph), Image.Resampling.LANCZOS)
    
    sh = Image.new('RGBA', (W, H), (0,0,0,0))
    shd = ImageDraw.Draw(sh)
    shd.ellipse([1180, 910, 1180 + pw, 1020], fill=(0, 0, 0, 240))
    sh = sh.filter(ImageFilter.GaussianBlur(35))
    base = Image.alpha_composite(base, sh)
    base.paste(phone, (1180, 110), phone)
    
    # Safe Bottom Stat Badge
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle([1020, 660, 1480, 810], radius=24, fill=(10, 28, 36, 250), outline=(0, 230, 180, 230), width=3)
    draw.text((1050, 685), "수학적 목표 도달 수량 산출", font=get_font(15, bold=True), fill=(0, 230, 180))
    draw.text((1050, 715), "+42.5주 추가 매수 필요", font=get_font(28, bold=True), fill=(255, 255, 255))
    draw.text((1050, 762), "총 투입 필요 예수금: ₩ 2,125,000", font=get_font(15, bold=False), fill=(180, 215, 220))
    
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
    f_sub = get_font(20, bold=False)
    
    draw.text((140, 95), "08. HIGH-FIDELITY SCREENS & INTERACTION PROTOTYPE", font=f_cat, fill=(0, 81, 255))
    draw.text((140, 133), "6개 핵심 모바일 인터페이스 쇼케이스 및 상호작용 연결", font=f_title, fill=(15, 23, 42))
    draw.text((140, 195), "홈 대시보드 ➔ 시뮬레이터 ➔ 목표 역산 ➔ 진단 리포트 ➔ OLED 다크모드 ➔ 환경설정 유기적 흐름", font=f_sub, fill=(100, 116, 139))
    
    mockup_files = [
        ('portfolio/mockup_ko_01_home.png', '01. 홈 대시보드'),
        ('portfolio/mockup_ko_02_sim.png', '02. 물타기 시뮬레이터'),
        ('portfolio/mockup_ko_03_target_filled.png', '03. 목표 역산 엔진'),
        ('portfolio/mockup_clean_report_filled.png', '04. 분석 리포트'),
        ('portfolio/mockup_dark_home_flawless.png', '05. OLED 야간 다크 홈'),
        ('portfolio/mockup_dark_settings_perfect.png', '06. 글로벌 환경설정')
    ]
    
    px = 120
    pw = 255
    pgap = 24
    
    for img_path, ctitle in mockup_files:
        phone = Image.open(img_path).convert('RGBA')
        ph = int(phone.height * (pw / phone.width))
        phone = phone.resize((pw, ph), Image.Resampling.LANCZOS)
        
        sh = Image.new('RGBA', (W, H), (0,0,0,0))
        shd = ImageDraw.Draw(sh)
        shd.ellipse([px, 860, px + pw, 915], fill=(0, 0, 0, 140))
        sh = sh.filter(ImageFilter.GaussianBlur(18))
        base = Image.alpha_composite(base, sh)
        
        base.paste(phone, (px, 240), phone)
        
        # Pill Caption with Dynamic Width and Generous Padding
        draw = ImageDraw.Draw(base)
        tw = draw.textlength(ctitle, font=get_font(13.5, bold=True))
        pill_w = int(tw + 36)
        pill_x = px + (pw - pill_w) // 2
        draw.rounded_rectangle([pill_x, 935, pill_x + pill_w, 972], radius=12, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw.text((pill_x + 18, 945), ctitle, font=get_font(13.5, bold=True), fill=(15, 23, 42))
        
        px += pw + pgap
        
    base.save('portfolio/behance_slides/slide_10.png')
    print("SAVED slide_10.png")

# ==============================================================
# SLIDE 11: OLED Deep Dark Theme & Accessibility
# ==============================================================
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
    gw.ellipse([700, 200, 1600, 950], fill=(0, 81, 255, 55))
    gw.ellipse([1100, 100, 1800, 700], fill=(0, 210, 255, 40))
    glow = glow.filter(ImageFilter.GaussianBlur(130))
    grad = Image.alpha_composite(grad, glow)
    base.paste(grad, (0, 0), mask)
    
    phone = Image.open('portfolio/mockup_dark_home_flawless.png').convert('RGBA')
    pw = 450
    ph = int(phone.height * (pw / phone.width))
    phone = phone.resize((pw, ph), Image.Resampling.LANCZOS)
    
    crop_bottom = 200
    phone = phone.crop((0, 0, phone.width, phone.height - crop_bottom))
    
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
    draw.text((tx, 165), "09. OLED DEEP DARK & ACCESSIBILITY", font=f_cat, fill=(0, 210, 255))
    draw.text((tx, 215), "야간 장세 트레이더를 위한\n고대비 다크 테마 시스템", font=f_title, fill=(255, 255, 255), spacing=18)
    draw.text((tx, 370), "Designed for night trading volatility\n7:1 이상의 WCAG 2.1 AAA 명도 대비를 엄격히 준수하여\n급박한 야간 해외주식·가상자산 장세에서도 오독 없는 수치 가독성 보장.", font=f_sub, fill=(180, 198, 220), spacing=10)
    
    specs = [
        ("시맨틱 컬러 토큰 매핑", "Primary Electric (#0051FF), Mint (#00E676), Coral (#FF5252), Gold (#FFB300)", (0, 81, 255)),
        ("Tabular Numbers 고정폭 폰트", "JetBrains Mono / Segoe UI의 'tnum' 속성을 적용하여 실시간 가격 변동 시 레이아웃 무흔들림", (0, 210, 255)),
        ("24시간 VIP 광고 제어 모델", "보상형 동영상 1회 시청 시 24시간 동안 배너 및 전면 광고 100% 완전 제거", (255, 179, 0))
    ]
    sy = 540
    for title, desc, ac_col in specs:
        draw.rounded_rectangle([tx, sy, tx + 920, sy + 104], radius=20, fill=(24, 32, 48, 240), outline=(ac_col[0], ac_col[1], ac_col[2], 120), width=2)
        draw.rounded_rectangle([tx, sy + 18, tx + 6, sy + 86], radius=3, fill=ac_col)
        draw.text((tx + 32, sy + 24), title, font=get_font(18, bold=True), fill=(255, 255, 255))
        draw.text((tx + 32, sy + 58), desc, font=get_font(14, bold=False), fill=(148, 163, 184))
        sy += 124
        
    base.save('portfolio/behance_slides/slide_11.png')
    print("SAVED slide_11.png")

# ==============================================================
# SLIDE 12: Quantitative Impact & STAR Retrospective (Safe Margins!)
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
    gw.ellipse([1100, 200, 1800, 900], fill=(0, 81, 255, 80))
    gw.ellipse([200, 400, 800, 1000], fill=(0, 230, 118, 50))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    grad = Image.alpha_composite(grad, glow)
    base.paste(grad, (0, 0), mask)
    
    draw = ImageDraw.Draw(base)
    f_cat = get_font(18, bold=True)
    f_title = get_font(44, bold=True)
    
    draw.text((140, 95), "10. BUSINESS IMPACT & STAR RETROSPECTIVE", font=f_cat, fill=(0, 210, 255))
    draw.text((140, 135), "정량적 비즈니스 성과 및 STAR 회고", font=f_title, fill=(255, 255, 255))
    
    metrics = [
        ("0.2 sec", "STT 음성 수치 파싱 속도", "키보드 타이핑 대비 입력 소요 시간 78% 단축"),
        ("100%", "Goal Seeking 수학적 정밀도", "부동소수점 오차 제로화 및 정밀 역산 도출"),
        ("60 fps", "실시간 슬라이더 반응성", "RepaintBoundary 최적화로 버벅임 없는 즉각 반응")
    ]
    mx = 140
    mw = 520
    mgap = 40
    for val, title, desc in metrics:
        draw.rounded_rectangle([mx, 215, mx + mw, 345], radius=20, fill=(255, 255, 255, 255))
        draw.text((mx + 28, 232), val, font=get_num_font(38, bold=True), fill=(0, 150, 100))
        draw.text((mx + 28, 284), title, font=get_font(18, bold=True), fill=(15, 23, 42))
        draw.text((mx + 28, 312), desc, font=get_font(13.5, bold=False), fill=(100, 116, 139))
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
    f_body = get_font(14, bold=False)
    for phase, content, color in star_items:
        draw.rounded_rectangle([sx, 385, sx + sw, 925], radius=20, fill=(255, 255, 255, 255))
        draw.rounded_rectangle([sx + 20, 405, sx + sw - 20, 450], radius=12, fill=color)
        draw.text((sx + 35, 417), phase, font=get_font(15.5, bold=True), fill=(255, 255, 255))
        
        wrapped_lines = wrap_text_by_words(content, f_body, sw - 56, draw)
        text_y = 475
        for line in wrapped_lines:
            draw.text((sx + 28, text_y), line, font=f_body, fill=(30, 41, 59))
            text_y += 26
        
        sx += sw + sgap
        
    base.save('portfolio/behance_slides/slide_12.png')
    print("SAVED slide_12.png")

# ==============================================================
# MAIN ENTRY
# ==============================================================
if __name__ == '__main__':
    for i in range(1, 13):
        func_name = f'make_slide_{i:02d}'
        if func_name in globals():
            globals()[func_name]()
    print("ALL 12 SLIDES GENERATED WITH STRICT MARGIN DEFENSE & HIGH CONTRAST TYPOGRAPHY!")
