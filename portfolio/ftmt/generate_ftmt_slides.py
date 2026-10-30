import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
OUT_DIR = "d:/097.flutter_project/auto_portfolio/ftmt/behance_slides"
ASSETS_DIR = "d:/097.flutter_project/auto_portfolio/ftmt/assets"
MOCKUP_DIR = f"{ASSETS_DIR}/iphone_mockups"
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
    w_name = 'bold' if isinstance(weight, bool) and weight else str(weight).lower()
    font_file = WEIGHT_MAP.get(w_name, 'Pretendard-Regular.ttf')
    font_path = os.path.join(FONT_DIR, font_file)
    try:
        return ImageFont.truetype(font_path, int(round(size)))
    except:
        return ImageFont.load_default()

def draw_pill_badge(draw, left_x=None, cx=None, cy=0, text="", font=None, theme='gold', has_dot=True, pad_x=12, height=26):
    if font is None:
        font = get_font(10.5, 'bold')
        
    color_schemes = {
        'gold':   {'bg': (35, 30, 15, 255),   'border': (229, 192, 123, 220), 'text': (255, 215, 0, 255),  'dot': (255, 215, 0, 255)},
        'purple': {'bg': (30, 18, 48, 255),   'border': (168, 85, 247, 220),  'text': (216, 180, 254, 255),'dot': (168, 85, 247, 255)},
        'cyan':   {'bg': (10, 36, 48, 255),   'border': (0, 229, 255, 220),   'text': (0, 229, 255, 255),  'dot': (0, 229, 255, 255)},
        'green':  {'bg': (12, 42, 30, 255),   'border': (16, 185, 129, 220),  'text': (52, 211, 153, 255), 'dot': (16, 185, 129, 255)},
        'red':    {'bg': (48, 16, 24, 255),   'border': (239, 68, 68, 220),   'text': (255, 140, 140, 255),'dot': (239, 68, 68, 255)},
        'slate':  {'bg': (20, 26, 42, 255),   'border': (100, 116, 139, 200), 'text': (203, 213, 225, 255),'dot': (148, 163, 184, 255)},
    }
    scheme = color_schemes.get(theme, color_schemes['gold'])
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    
    dot_d = 6
    dot_gap = 6
    content_w = (dot_d + dot_gap + tw) if has_dot else tw
    bw = int(round(content_w + pad_x * 2))
    bh = height
    
    if left_x is not None:
        bx1 = int(round(left_x))
        bx2 = bx1 + bw
        cx = (bx1 + bx2) / 2.0
    else:
        bx1 = int(round(cx - bw / 2.0))
        bx2 = bx1 + bw
        
    by1 = int(round(cy - bh / 2.0))
    by2 = by1 + bh
    
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=bh // 2, fill=scheme['bg'], outline=scheme['border'], width=1)
    ty = int(round(cy - (bbox[1] + bbox[3]) / 2.0))
    
    if has_dot:
        content_x1 = cx - content_w / 2.0
        dot_cx = content_x1 + dot_d / 2.0
        r = dot_d / 2.0
        draw.ellipse([int(round(dot_cx - r)), int(round(cy - r)), int(round(dot_cx + r)), int(round(cy + r))], fill=scheme['dot'])
        tx = int(round(content_x1 + dot_d + dot_gap - bbox[0]))
    else:
        tx = int(round(cx - (bbox[0] + bbox[2]) / 2.0))
        
    draw.text((tx, ty), text, font=font, fill=scheme['text'])
    return bx1, by1, bx2, by2

def create_cosmic_base(center_orbit=(1500, 540)):
    base = Image.new('RGBA', (W, H), (7, 10, 18, 255))
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([center_orbit[0] - 400, center_orbit[1] - 400, center_orbit[0] + 350, center_orbit[1] + 350], fill=(138, 43, 226, 35))
    gw.ellipse([center_orbit[0] - 250, center_orbit[1] - 250, center_orbit[0] + 300, center_orbit[1] + 400], fill=(0, 229, 255, 25))
    gw.ellipse([100, 600, 700, 1050], fill=(229, 192, 123, 18))
    glow = glow.filter(ImageFilter.GaussianBlur(130))
    base = Image.alpha_composite(base, glow)
    
    draw = ImageDraw.Draw(base)
    for r in [280, 420, 560]:
        draw.ellipse([center_orbit[0] - r, center_orbit[1] - r, center_orbit[0] + r, center_orbit[1] + r], outline=(229, 192, 123, 16), width=1)
        
    draw.line([(100, 52), (1820, 52)], fill=(229, 192, 123, 40), width=1)
    draw.line([(100, 990), (1820, 990)], fill=(229, 192, 123, 40), width=1)
    return base, draw

def draw_slide_header(draw, slide_num, category_en, title_white, title_gold, subtitle):
    draw_pill_badge(draw, left_x=100, cy=78, text=f"{slide_num:02d} {category_en}", font=get_font(9.5, 'bold'), theme='gold', has_dot=True, height=24, pad_x=10)
    font_title = get_font(32, 'bold')
    draw.text((100, 126), title_white, font=font_title, fill=(244, 246, 252, 255), anchor='ls')
    tw = draw.textlength(title_white, font=font_title)
    draw.text((100 + tw, 126), title_gold, font=font_title, fill=(255, 215, 0, 255), anchor='ls')
    draw.text((100, 158), subtitle, font=get_font(13.5, 'regular'), fill=(163, 176, 204, 255), anchor='ls')

def draw_slide_footer(draw, slide_num, total_slides=12):
    draw.line([(100, 1030), (1820, 1030)], fill=(229, 192, 123, 40), width=1)
    draw.text((100, 1048), "FORTUNEMATCH", font=get_font(10, 'bold'), fill=(255, 215, 0, 255), anchor='ls')
    draw.text((230, 1048), "·   Behance Enterprise Case Study   ·   Cosmic Luxury Brand & UX/UI Architecture", font=get_font(9.5, 'medium'), fill=(163, 176, 204, 255), anchor='ls')
    draw.text((1820, 1048), f"PAGE {slide_num:02d} / {total_slides}", font=get_font(10, 'bold'), fill=(163, 176, 204, 255), anchor='rs')

# =========================================================================
# SLIDE 01: HERO COVER
# =========================================================================
def render_slide_01():
    base, draw = create_cosmic_base(center_orbit=(1480, 520))
    
    icon_path = f"{ASSETS_DIR}/app_icon.png"
    if os.path.exists(icon_path):
        icon = Image.open(icon_path).convert('RGBA').resize((52, 52), Image.Resampling.LANCZOS)
        mask = Image.new('L', (52, 52), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, 52, 52], radius=14, fill=255)
        base.paste(icon, (100, 75), mask)
        draw.rounded_rectangle([100, 75, 152, 127], radius=14, outline=(255, 215, 0, 180), width=1)
        
    draw_pill_badge(draw, left_x=164, cy=101, text="GLOBAL LUXURY FORTUNE & MATCHING PLATFORM", font=get_font(9.5, 'bold'), theme='gold', has_dot=True, height=26, pad_x=12)
    
    font_h1 = get_font(42, 'bold')
    t1 = "우주의 주파수와 사주 오행으로 풀어낸"
    t2 = "나의 고유 우주 좌표 & 인연 매칭"
    draw.text((100, 190), t1, font=font_h1, fill=(244, 246, 252, 255))
    draw.text((100, 246), t2, font=font_h1, fill=(255, 215, 0, 255))
    
    sub = "사주 일주론과 서양 점성술의 결합을 통한 MZ세대 맞춤형 인연 궁합 & 60fps 인터랙티브 플랫폼"
    draw.text((100, 320), sub, font=get_font(16.5, 'regular'), fill=(163, 176, 204, 255))
    
    badges = [
        ("• 0.3s 빠른 우주 좌표 생성", "gold"),
        ("• 5각형 오행 에너지 밸런스", "purple"),
        ("• 92% 정밀 사주 궁합 알고리즘", "cyan"),
        ("• 도파민 타로 & 시크릿 볼트", "green")
    ]
    bx = 100
    for text, theme in badges:
        x1, y1, x2, y2 = draw_pill_badge(draw, left_x=bx, cy=385, text=text, font=get_font(11, 'bold'), theme=theme, has_dot=False, pad_x=14, height=32)
        bx = x2 + 14
        
    box_y = 450
    draw.rounded_rectangle([100, box_y, 980, box_y + 360], radius=20, fill=(14, 20, 36, 220), outline=(229, 192, 123, 70), width=1)
    
    draw.text((130, box_y + 30), "PROJECT OVERVIEW & CORE DESIGN RATIONALE", font=get_font(12, 'bold'), fill=(255, 215, 0, 255))
    draw.line([(130, box_y + 58), (950, box_y + 58)], fill=(229, 192, 123, 40), width=1)
    
    info_items = [
        ("Role & Contribution", "Lead UX/UI Designer & System Architect (100% 개인 기여)"),
        ("Service Scope", "브랜드 아이덴티티, IA 설계, 오행 데이터 시각화, 60fps 프로토타입"),
        ("Target Audience", "자아 탐색 및 관계 지향적 소통을 추구하는 2030 MZ세대"),
        ("Core Technology", "오행 상생상극 알고리즘, 실시간 다각형 렌더링, 물리 엔진 타로"),
        ("Deliverables", "Figma Design System, 12 High-Res Slides, 60fps Live Simulator")
    ]
    iy = box_y + 80
    for label, val in info_items:
        draw.text((130, iy), label, font=get_font(12, 'bold'), fill=(229, 192, 123, 255))
        draw.text((320, iy), val, font=get_font(12.5, 'regular'), fill=(244, 246, 252, 255))
        iy += 52
        
    draw.text((100, 850), "※ 본 포트폴리오는 명리학의 난해한 한자어를 배제하고, 우주적 데이터 시각화로 재해석한 엔터프라이즈 UX/UI 케이스 스터디입니다.", font=get_font(12, 'regular'), fill=(103, 117, 152, 255))
    
    mockup_path = f"{MOCKUP_DIR}/iphone_01_hub.png"
    if os.path.exists(mockup_path):
        m_img = Image.open(mockup_path).convert('RGBA')
        target_h = 840
        target_w = int(round(m_img.width * (target_h / m_img.height)))
        m_resized = m_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        shadow = Image.new('RGBA', (target_w + 80, target_h + 80), (0, 0, 0, 0))
        ImageDraw.Draw(shadow).rounded_rectangle([30, 30, target_w + 50, target_h + 50], radius=50, fill=(0, 0, 0, 160))
        shadow = shadow.filter(ImageFilter.GaussianBlur(30))
        base.paste(shadow, (1260, 110), shadow)
        base.paste(m_resized, (1300, 120), m_resized)
        
    draw_slide_footer(draw, 1)
    base.save(f"{OUT_DIR}/slide_01.png")
    print("Slide 01 saved.")

# =========================================================================
# SLIDE 02: PROBLEM DEFINITION & MARKET STUDY
# =========================================================================
def render_slide_02():
    base, draw = create_cosmic_base(center_orbit=(1600, 700))
    draw_slide_header(
        draw,
        slide_num=2,
        category_en="USER RESEARCH | MARKET & BEHAVIOR STUDY",
        title_white="비과학적 미신과 텍스트 나열의 한계, ",
        title_gold="우주 데이터 시각화의 혁신",
        subtitle="2030 MZ세대 520명 설문 및 기존 운세/사주 앱 16종 전수 조사를 통해 도출한 3대 핵심 위협과 해결 전략"
    )
    
    # 3 Problem Cards
    card_w = 540
    card_h = 320
    sy = 195
    cards_data = [
        ("MARKET PAIN 01", "red", "가독성 붕괴 & 높은 인지부하", 
         "난해한 한자어와 장문의 텍스트가 화면을 가득 채워 핵심 인사이트를 파악하기 어려움.\n조사 대상자의 74.2%가 장문 설명을 읽지 않고 이탈하는 현상 발생.",
         "• 80자 이상의 고문투 설명 문장\n• 일주/만세력 핵심 정보의 파편화\n• 핵심 요약 카드의 부재"),
        ("BEHAVIOR GAP 02", "gold", "미신적 공포 마케팅의 피로감", 
         "‘삼재’, ‘살’ 등 부정적 키워드를 앞세운 결제 유도 방식으로 인해 일상적인 자기 발견과 힐링을 원하는 MZ세대의 심리적 반발 심화.",
         "• 액운을 강조하는 불안 마케팅\n• 긍정적 자아 성찰 기회 차단\n• 친구/지인과 공유하기 꺼려지는 UI"),
        ("INDUSTRY VOID 03", "cyan", "관계 케미스트리의 시각화 부재", 
         "단순히 ‘궁합 75점’ 식의 일차원적 점수만 제시하여, 두 사람의 어떤 기운이 상호 보완되고 어떤 성향이 충돌하는지 구체적 해석 불가.",
         "• 오행 상생상극 설명 전무\n• 상대방 성향별 대화 팁 부재\n• 정량적 비교 다이어그램 결여")
    ]
    
    for i, (badge_txt, badge_theme, title, desc, bullets) in enumerate(cards_data):
        cx = 100 + i * (card_w + 30)
        draw.rounded_rectangle([cx, sy, cx + card_w, sy + card_h], radius=16, fill=(14, 20, 36, 230), outline=(229, 192, 123, 60), width=1)
        draw_pill_badge(draw, left_x=cx + 24, cy=sy + 28, text=badge_txt, font=get_font(10, 'bold'), theme=badge_theme, has_dot=False, pad_x=10, height=24)
        draw.text((cx + 24, sy + 68), title, font=get_font(18, 'bold'), fill=(244, 246, 252, 255))
        
        # Description
        dy = sy + 106
        for line in desc.split('\n'):
            draw.text((cx + 24, dy), line, font=get_font(12, 'regular'), fill=(163, 176, 204, 255))
            dy += 22
            
        # Divider
        draw.line([(cx + 24, sy + 185), (cx + card_w - 24, sy + 185)], fill=(229, 192, 123, 30), width=1)
        
        # Bullets
        by = sy + 205
        for line in bullets.split('\n'):
            draw.text((cx + 24, by), line, font=get_font(11.5, 'medium'), fill=(229, 192, 123, 240))
            by += 28
            
    # Bottom SWOT Matrix & UX Strategy
    swot_y = 550
    swot_h = 410
    draw.rounded_rectangle([100, swot_y, 1820, swot_y + swot_h], radius=20, fill=(11, 16, 28, 240), outline=(229, 192, 123, 50), width=1)
    draw.text((130, swot_y + 26), "SWOT ANALYSIS & STRATEGIC UX POSITIONING", font=get_font(12, 'bold'), fill=(255, 215, 0, 255))
    draw.line([(130, swot_y + 54), (1790, swot_y + 54)], fill=(229, 192, 123, 40), width=1)
    
    q_w = 400
    q_gap = 20
    quadrants = [
        ("Strength (강점)", "green", [
            "• 0.3초 만에 나만의 우주 주파수 & 좌표 생성",
            "• 5각형 오행 에너지 밸런스 실시간 다각형 시각화",
            "• 60fps 물리 엔진 기반 타로 플립의 높은 손맛"
        ]),
        ("Weakness (약점)", "purple", [
            "• 사주 명리학에 익숙하지 않은 초심자 대상 온보딩 필요",
            "• 출생 시간을 모르는 사용자를 위한 시간 보정 로직 구현",
            "• 방대한 오행 지식의 단계적 정보 노출(Progressive Disclosure)"
        ]),
        ("Opportunity (기회)", "cyan", [
            "• 2030 세대의 MBTI를 넘어서는 차세대 자아 탐색 욕구",
            "• 인스타그램/카카오톡을 통한 감각적 궁합 카드 바이럴",
            "• 개인 맞춤형 오행 컬러/소품 라이프스타일 커머스 확장"
        ]),
        ("Threat (위협)", "gold", [
            "• 대형 포털 및 무료 운세 앱의 텍스트 콘텐츠 공세",
            "• 사주/타로 서비스에 대한 비과학적 미신 편견 극복 과제",
            "• 감각적 다크 럭셔리 브랜딩과 시크릿 볼트로 독보적 가치 입증"
        ])
    ]
    
    for i, (q_title, q_theme, points) in enumerate(quadrants):
        qx = 130 + i * (q_w + q_gap)
        qy = swot_y + 75
        draw.rounded_rectangle([qx, qy, qx + q_w, qy + 300], radius=14, fill=(15, 22, 38, 220), outline=(229, 192, 123, 40), width=1)
        draw_pill_badge(draw, left_x=qx + 16, cy=qy + 26, text=q_title, font=get_font(10.5, 'bold'), theme=q_theme, has_dot=False, pad_x=10, height=24)
        
        py = qy + 65
        for p in points:
            draw.text((qx + 16, py), p, font=get_font(11.5, 'regular'), fill=(203, 213, 225, 255))
            py += 42
            
    draw_slide_footer(draw, 2)
    base.save(f"{OUT_DIR}/slide_02.png")
    print("Slide 02 saved.")

# =========================================================================
# SLIDE 03: PERSONA & CUSTOMER JOURNEY MAP
# =========================================================================
def render_slide_03():
    base, draw = create_cosmic_base(center_orbit=(1500, 300))
    draw_slide_header(
        draw,
        slide_num=3,
        category_en="USER PERSONA & CUSTOMER JOURNEY MAP",
        title_white="MZ세대의 자아 탐험과 관계 지향성을 담은 ",
        title_gold="타겟 페르소나 설계",
        subtitle="가치 소비와 정서적 안정을 추구하는 27세 직장인 페르소나의 일상 여정 및 단계별 UX 기회 영역"
    )
    
    # Left Persona Card
    pw = 520
    ph = 780
    px = 100
    py = 190
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=20, fill=(14, 20, 36, 230), outline=(229, 192, 123, 70), width=1)
    draw_pill_badge(draw, left_x=px + 24, cy=py + 30, text="PRIMARY PERSONA ARCHETYPE", font=get_font(10, 'bold'), theme='gold', has_dot=True, pad_x=10, height=24)
    
    draw.text((px + 24, py + 72), "김서윤 (27세, IT 프로덕트 디자이너)", font=get_font(20, 'bold'), fill=(244, 246, 252, 255))
    draw.text((px + 24, py + 104), '"나를 더 깊이 이해하고, 소중한 사람들과의 조화로운 관계를 찾고 싶어요."', font=get_font(12.5, 'bold'), fill=(255, 215, 0, 255))
    draw.line([(px + 24, py + 135), (px + pw - 24, py + 135)], fill=(229, 192, 123, 40), width=1)
    
    traits = [
        ("MBTI / 기질", "INFP (열정적인 중재자), 자아 탐색 및 퍼스널 브랜딩 관심"),
        ("디지털 숙련도", "상급 (모바일 앱 사용성 및 마이크로 인터랙션 민감)"),
        ("라이프스타일", "주 3회 필라테스, 힐링 명상, 친구들과 감성 카페 탐방"),
        ("주요 고민거리", "새로운 인연과의 관계 지속성, 이직 타이밍 및 커리어 방향")
    ]
    ty = py + 155
    for k, v in traits:
        draw.text((px + 24, ty), k, font=get_font(11.5, 'bold'), fill=(229, 192, 123, 255))
        draw.text((px + 140, ty), v, font=get_font(12, 'regular'), fill=(203, 213, 225, 255))
        ty += 38
        
    draw.line([(px + 24, ty + 10), (px + pw - 24, ty + 10)], fill=(229, 192, 123, 40), width=1)
    
    # Pain Points & Needs
    draw.text((px + 24, ty + 30), "Core Pain Points (기존 한계)", font=get_font(13, 'bold'), fill=(255, 140, 140, 255))
    pains = [
        "• 전통 사주 앱의 낡은 UI와 무서운 미신적 어조에 거부감",
        "• 텍스트가 너무 길어 내 사주의 진짜 장단점을 요약하기 어려움",
        "• 썸이나 친구와의 궁합 결과를 세련되게 공유할 방법 부재"
    ]
    pty = ty + 60
    for p in pains:
        draw.text((px + 24, pty), p, font=get_font(11.5, 'regular'), fill=(244, 246, 252, 255))
        pty += 30
        
    draw.text((px + 24, pty + 15), "Design Needs (UX 기대 가치)", font=get_font(13, 'bold'), fill=(52, 211, 153, 255))
    needs = [
        "• 0.3초 만에 직관적으로 시각화되는 우주적 감성의 대시보드",
        "• 오행 밸런스 차트를 통해 나의 결핍/과잉 에너지를 직관적 인지",
        "• 상대방과의 케미스트리를 도파민 넘치게 즐길 수 있는 궁합 카드"
    ]
    nty = pty + 45
    for n in needs:
        draw.text((px + 24, nty), n, font=get_font(11.5, 'regular'), fill=(244, 246, 252, 255))
        nty += 30
        
    # Right Customer Journey Map (4 Stages)
    jw = 1150
    jx = 670
    draw.rounded_rectangle([jx, py, jx + jw, py + ph], radius=20, fill=(11, 16, 28, 230), outline=(229, 192, 123, 60), width=1)
    draw_pill_badge(draw, left_x=jx + 24, cy=py + 30, text="4-STAGE END-TO-END EXPERIENCE JOURNEY MAP", font=get_font(10, 'bold'), theme='cyan', has_dot=True, pad_x=10, height=24)
    draw.line([(jx + 24, py + 58), (jx + jw - 24, py + 58)], fill=(229, 192, 123, 40), width=1)
    
    stages = [
        ("STAGE 01", "Discovery & Onboarding", "purple", 
         "생년월일시 및 출생지 입력", 
         "• 3단계 최소 입력 폼으로 인지 부하 80% 절감\n• 입력 즉시 나만의 우주 주파수 & 좌표 생성 연출\n• '나만의 별자리와 사주 일주'를 발견하는 설렘",
         "감정 지수: 호기심과 기대감 (88%)", "기회: 태양시 보정 자동화로 신뢰도 구축"),
        ("STAGE 02", "Self-Analysis & Radar", "gold", 
         "5각형 오행 에너지 밸런스 탐색", 
         "• 목화토금수 에너지 분포도를 5각형 레이더로 시각화\n• '불(火)이 부족해 행동력이 저하될 때' 맞춤 조언 제공\n• 텍스트 대신 직관적인 그래픽으로 내 기질 확인",
         "감정 지수: 놀라움과 깊은 공감 (94%)", "기회: 부족한 기운을 채우는 행운의 컬러 추천"),
        ("STAGE 03", "Chemistry & Match", "cyan", 
         "인연과의 정밀 사주 궁합 리포트", 
         "• 1-Tap으로 상대방 프로필 추가 및 궁합 분석 요청\n• 92% 천생연분 케미스트리 및 상생상극 피드백\n• 서로의 에너지가 결합되는 중첩 차트 인터랙션",
         "감정 지수: 짜릿한 도파민과 즐거움 (98%)", "기회: 인스타그램 스토리 공유 최적화 카드"),
        ("STAGE 04", "Ritual & Secret Vault", "green", 
         "도파민 타로 리딩 & 기록 보관", 
         "• 물리 엔진 기반의 햅틱 타로 카드 뒤집기 경험\n• 오늘을 위한 우주적 솔루션 및 명확한 행동 가이드\n• 영구 저장되는 '시크릿 볼트'에 궁합 히스토리 축적",
         "감정 지수: 힐링과 만족스러운 평온 (92%)", "기회: 소장 욕구를 자극하는 타로 굿즈 연계")
    ]
    
    sy = py + 75
    for num, title, theme, sub, desc, emo, opp in stages:
        draw.rounded_rectangle([jx + 24, sy, jx + jw - 24, sy + 155], radius=14, fill=(15, 22, 38, 220), outline=(229, 192, 123, 40), width=1)
        draw_pill_badge(draw, left_x=jx + 40, cy=sy + 24, text=num, font=get_font(9.5, 'bold'), theme=theme, has_dot=False, pad_x=8, height=22)
        draw.text((jx + 120, sy + 24), title, font=get_font(15, 'bold'), fill=(244, 246, 252, 255), anchor='lm')
        draw.text((jx + 450, sy + 24), f"[{sub}]", font=get_font(12, 'bold'), fill=(229, 192, 123, 240), anchor='lm')
        
        # Details
        draw.text((jx + 40, sy + 50), desc, font=get_font(11.5, 'regular'), fill=(203, 213, 225, 255))
        
        # Emotion & Opportunity
        draw.rounded_rectangle([jx + 780, sy + 18, jx + jw - 40, sy + 138], radius=10, fill=(9, 13, 24, 200), outline=(229, 192, 123, 30), width=1)
        draw.text((jx + 800, sy + 45), emo, font=get_font(11, 'bold'), fill=(255, 215, 0, 255))
        draw.text((jx + 800, sy + 85), opp, font=get_font(11, 'medium'), fill=(52, 211, 153, 255))
        sy += 172
        
    draw_slide_footer(draw, 3)
    base.save(f"{OUT_DIR}/slide_03.png")
    print("Slide 03 saved.")

# =========================================================================
# SLIDE 04: INFORMATION ARCHITECTURE (IA)
# =========================================================================
def render_slide_04():
    base, draw = create_cosmic_base(center_orbit=(1400, 500))
    draw_slide_header(
        draw,
        slide_num=4,
        category_en="SYSTEM ARCHITECTURE | INFORMATION ARCHITECTURE",
        title_white="복잡한 명리학 데이터를 4단계로 구조화한 ",
        title_gold="인포메이션 아키텍처",
        subtitle="0.3초 이내에 원하는 정보에 도달할 수 있는 직관적인 4대 코어 뎁스 및 서비스 계층 구조"
    )
    
    col_w = 405
    col_gap = 30
    col_h = 760
    cy = 195
    
    ia_data = [
        ("1.0 COSMIC FORTUNE HUB", "gold", "우주 사주 허브", [
            ("1.1 나의 우주 좌표", "생년월일 기반 천간지지 일주 심볼 및 고유 주파수"),
            ("1.2 10년 대운 타임라인", "인생의 황금기 및 전환점을 시각화한 수평 그래프"),
            ("1.3 오늘의 오행 종합 지수", "매일 아침 갱신되는 오행 기운 밸런스 및 행동 요령"),
            ("1.4 오늘의 도파민 시크릿", "시간대별 최고 길시(吉時) 및 주의 인물 가이드"),
            ("1.5 출석 하트 보상", "연속 출석 시 무료 하트 충전 및 행운 부적 획득")
        ]),
        ("2.0 FIVE ELEMENTS RADAR", "purple", "오행 밸런스 분석", [
            ("2.1 5각형 에너지 레이더", "목·화·토·금·수 실시간 다각형 차트 시각화"),
            ("2.2 결핍/과잉 기운 진단", "나에게 부족한 기운과 넘치는 기운의 정량적 비교"),
            ("2.3 상생·상극 순환도", "오행 간의 순환 상호작용을 보여주는 인터랙티브 다이어그램"),
            ("2.4 맞춤 라이프스타일 처방", "부족한 오행을 채우는 행운의 컬러, 소품, 음식 가이드"),
            ("2.5 천간지지 만세력 원문", "심화 학습자를 위한 8글자 만세력 상세 보기 토글")
        ]),
        ("3.0 ZODIAC & SAJU MATCH", "cyan", "궁합 매칭 엔진", [
            ("3.1 인연 프로필 관리", "친구, 연인, 직장 동료 등 다중 인연 등록 및 전환"),
            ("3.2 92% 정밀 케미스트리", "일주 궁합 + 띠 궁합 + 오행 상생도를 결합한 종합 지수"),
            ("3.3 오행 중첩 레이더", "두 사람의 레이더 차트를 겹쳐 서로의 보완점 시각화"),
            ("3.4 실전 소통 & 데이트 팁", "갈등을 예방하고 친밀도를 높이는 대화 가이드라인"),
            ("3.5 인스타그램 공유 카드", "세련된 그라디언트 템플릿으로 원클릭 스토리 공유")
        ]),
        ("4.0 MYSTIC TAROT & VAULT", "green", "타로 & 시크릿 볼트", [
            ("4.1 3D 인터랙티브 타로", "물리 엔진 기반의 사실적인 카드 셔플 및 햅틱 플립"),
            ("4.2 메이저 아르카나 22종", "고해상도 타로 일러스트와 도파민 넘치는 해석 리포트"),
            ("4.3 시크릿 볼트 (보관함)", "과거의 모든 운세와 궁합 기록을 안전하게 암호화 보관"),
            ("4.4 럭셔리 젬스톤 스토어", "프리미엄 해석권 및 운세 보석 구매 인앱 경제 시스템"),
            ("4.5 글로벌 다국어 설정", "한국어/영어/일본어 등 다국어 및 로컬라이제이션")
        ])
    ]
    
    for i, (code, theme, title_kr, items) in enumerate(ia_data):
        cx = 100 + i * (col_w + col_gap)
        draw.rounded_rectangle([cx, cy, cx + col_w, cy + col_h], radius=18, fill=(14, 20, 36, 230), outline=(229, 192, 123, 60), width=1)
        draw_pill_badge(draw, left_x=cx + 20, cy=cy + 30, text=code, font=get_font(10, 'bold'), theme=theme, has_dot=True, pad_x=10, height=24)
        draw.text((cx + 20, cy + 72), title_kr, font=get_font(19, 'bold'), fill=(244, 246, 252, 255))
        draw.line([(cx + 20, cy + 98), (cx + col_w - 20, cy + 98)], fill=(229, 192, 123, 40), width=1)
        
        iy = cy + 115
        for item_title, item_sub in items:
            draw.rounded_rectangle([cx + 16, iy, cx + col_w - 16, iy + 105], radius=12, fill=(10, 14, 26, 220), outline=(229, 192, 123, 30), width=1)
            draw.text((cx + 28, iy + 16), item_title, font=get_font(13, 'bold'), fill=(255, 215, 0, 255))
            
            # Subtitle wrap
            words = item_sub
            if len(words) > 24:
                line1 = words[:24]
                line2 = words[24:]
                draw.text((cx + 28, iy + 45), line1, font=get_font(11, 'regular'), fill=(163, 176, 204, 255))
                draw.text((cx + 28, iy + 68), line2, font=get_font(11, 'regular'), fill=(163, 176, 204, 255))
            else:
                draw.text((cx + 28, iy + 52), words, font=get_font(11.5, 'regular'), fill=(163, 176, 204, 255))
            iy += 122
            
    draw_slide_footer(draw, 4)
    base.save(f"{OUT_DIR}/slide_04.png")
    print("Slide 04 saved.")

# =========================================================================
# SLIDE 05: USER FLOW & EXPERIENCE LOGIC
# =========================================================================
def render_slide_05():
    base, draw = create_cosmic_base(center_orbit=(1300, 600))
    draw_slide_header(
        draw,
        slide_num=5,
        category_en="USER FLOW & EXPERIENCE LOGIC",
        title_white="인지적 마찰을 제로화한 ",
        title_gold="단계별 사용자 인터랙션 흐름도",
        subtitle="탄생 좌표 입력부터 오행 분석, 궁합 매칭, 타로 솔루션으로 이어지는 논리적 상태 전이(State Machine)"
    )
    
    # 5 Horizontal Steps
    step_w = 310
    step_gap = 42
    step_h = 440
    sy = 220
    
    flow_steps = [
        ("STEP 01", "gold", "출생 데이터 입력", [
            "• 양력 / 음력 선택 토글",
            "• 생년월일 및 출생 시각 입력",
            "• 태양시 자동 보정 로직 가동",
            "• 필수 약관 동의 및 확인"
        ], "Action: [우주 좌표 생성 버튼 클릭]"),
        ("STEP 02", "purple", "우주 주파수 연산", [
            "• 만세력 4주 8글자 도출",
            "• 나만의 고유 일주 심볼 매핑",
            "• 신비로운 궤도 애니메이션",
            "• 메인 허브 화면으로 진입"
        ], "Result: [개인화 대시보드 0.3s 렌더링]"),
        ("STEP 03", "cyan", "오행 밸런스 탐색", [
            "• 5각형 레이더 다각형 시각화",
            "• 결핍된 기운(예: 목 10%) 확인",
            "• 부족한 기운 채우기 솔루션",
            "• 일상 라이프스타일 팁 확인"
        ], "Action: [상세 처방 및 궁합 매칭 탭 이동]"),
        ("STEP 04", "green", "인연 궁합 매칭", [
            "• 상대방 출생 정보 모달 입력",
            "• 두 사람의 오행 상생상극 연산",
            "• 92% 천생연분 케미스트리 확인",
            "• 인스타그램 공유 카드 생성"
        ], "Action: [도파민 타로 카드 리딩 요청]"),
        ("STEP 05", "red", "타로 & 시크릿 볼트", [
            "• 3D 타로 덱 물리 셔플",
            "• 1장 뽑기 및 햅틱 카드 플립",
            "• 오늘의 우주적 해답 확인",
            "• 시크릿 볼트에 암호화 영구 저장"
        ], "Goal: [데일리 리텐션 및 볼트 구독 달성]")
    ]
    
    for i, (badge_txt, theme, title, points, cta) in enumerate(flow_steps):
        sx = 100 + i * (step_w + step_gap)
        draw.rounded_rectangle([sx, sy, sx + step_w, sy + step_h], radius=16, fill=(14, 20, 36, 230), outline=(229, 192, 123, 60), width=1)
        draw_pill_badge(draw, left_x=sx + 20, cy=sy + 28, text=badge_txt, font=get_font(10, 'bold'), theme=theme, has_dot=False, pad_x=10, height=24)
        draw.text((sx + 20, sy + 70), title, font=get_font(18, 'bold'), fill=(244, 246, 252, 255))
        draw.line([(sx + 20, sy + 96), (sx + step_w - 20, sy + 96)], fill=(229, 192, 123, 40), width=1)
        
        py = sy + 120
        for p in points:
            draw.text((sx + 20, py), p, font=get_font(12, 'regular'), fill=(203, 213, 225, 255))
            py += 40
            
        # CTA Box
        draw.rounded_rectangle([sx + 14, sy + 360, sx + step_w - 14, sy + 415], radius=10, fill=(9, 13, 24, 220), outline=(229, 192, 123, 40), width=1)
        draw.text((sx + step_w // 2, sy + 387), cta, font=get_font(11, 'bold'), fill=(255, 215, 0, 255), anchor='mm')
        
        # Connection Arrow to next step
        if i < len(flow_steps) - 1:
            arrow_x = sx + step_w + 8
            arrow_y = sy + step_h // 2
            draw.line([(arrow_x, arrow_y), (arrow_x + 24, arrow_y)], fill=(255, 215, 0, 180), width=2)
            draw.polygon([(arrow_x + 24, arrow_y - 6), (arrow_x + 32, arrow_y), (arrow_x + 24, arrow_y + 6)], fill=(255, 215, 0, 180))
            
    # Bottom Experience Logic Highlight Box
    b_box_y = 700
    draw.rounded_rectangle([100, b_box_y, 1820, b_box_y + 260], radius=18, fill=(11, 16, 28, 230), outline=(229, 192, 123, 50), width=1)
    draw.text((130, b_box_y + 30), "KEY UX LOGIC: PROGRESSIVE DISCLOSURE & FRICTIONLESS ONBOARDING", font=get_font(12, 'bold'), fill=(255, 215, 0, 255))
    draw.line([(130, b_box_y + 58), (1790, b_box_y + 58)], fill=(229, 192, 123, 40), width=1)
    
    logic_cols = [
        ("1. 점진적 정보 노출 (Progressive Disclosure)", "초기 온보딩 시 복잡한 명리학 용어를 숨기고 '나만의 우주 좌표'라는 친숙한 메타포로 접근성을 높이고, 사용자가 원할 때만 심화 만세력 데이터를 펼쳐볼 수 있도록 설계."),
        ("2. 모달 기반의 빠른 상대방 전환", "궁합 매칭 시 페이지를 이탈하지 않고 바텀 시트(Modal Bottom Sheet) 형태로 상대방 정보를 즉시 입력/수정할 수 있어 조작 뎁스를 3단계에서 1단계로 축소."),
        ("3. 감성적 보상 루프 (Dopamine Loop)", "타로 카드 리딩 및 출석 보상 시 즉각적인 햅틱 진동과 우주 파티클 이펙트를 트리거하여 단순 정보 조회를 넘어선 오감 만족형 감성 경험 제공.")
    ]
    lx = 130
    for l_title, l_desc in logic_cols:
        draw.text((lx, b_box_y + 85), l_title, font=get_font(13.5, 'bold'), fill=(229, 192, 123, 255))
        # Wrap
        words = l_desc
        line1 = words[:34]
        line2 = words[34:68]
        line3 = words[68:]
        draw.text((lx, b_box_y + 120), line1, font=get_font(11.5, 'regular'), fill=(203, 213, 225, 255))
        draw.text((lx, b_box_y + 148), line2, font=get_font(11.5, 'regular'), fill=(203, 213, 225, 255))
        if line3:
            draw.text((lx, b_box_y + 176), line3, font=get_font(11.5, 'regular'), fill=(203, 213, 225, 255))
        lx += 560
        
    draw_slide_footer(draw, 5)
    base.save(f"{OUT_DIR}/slide_05.png")
    print("Slide 05 saved.")

# =========================================================================
# SLIDE 06: WIREFRAME & UX SOLUTION CALLOUT PINS
# =========================================================================
def render_slide_06():
    base, draw = create_cosmic_base(center_orbit=(500, 600))
    draw_slide_header(
        draw,
        slide_num=6,
        category_en="WIREFRAME & INTERACTION CALLOUTS",
        title_white="인지 부하를 줄이고 몰입감을 극대화한 ",
        title_gold="와이어프레임 설계 원칙",
        subtitle="단순한 기능 배치를 넘어 사용자의 시선 흐름과 조작 편의성을 정밀하게 고려한 UX 콜아웃"
    )
    
    # Left Mockup Display
    m_path = f"{MOCKUP_DIR}/iphone_01_hub.png"
    if os.path.exists(m_path):
        m_img = Image.open(m_path).convert('RGBA')
        target_h = 760
        target_w = int(round(m_img.width * (target_h / m_img.height)))
        m_resized = m_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        base.paste(m_resized, (140, 200), m_resized)
        
    # Draw Callout Lines & Circles on Mockup
    # Pin 1 on top card
    draw.ellipse([320 - 14, 340 - 14, 320 + 14, 340 + 14], fill=(255, 215, 0, 255), outline=(7, 10, 18, 255), width=2)
    draw.text((320, 340), "1", font=get_font(11, 'black'), fill=(7, 10, 18, 255), anchor='mm')
    draw.line([(334, 340), (550, 340)], fill=(255, 215, 0, 180), width=2)
    
    # Pin 2 on middle circle
    draw.ellipse([320 - 14, 480 - 14, 320 + 14, 480 + 14], fill=(0, 229, 255, 255), outline=(7, 10, 18, 255), width=2)
    draw.text((320, 480), "2", font=get_font(11, 'black'), fill=(7, 10, 18, 255), anchor='mm')
    draw.line([(334, 480), (550, 480)], fill=(0, 229, 255, 180), width=2)
    
    # Pin 3 on secret card
    draw.ellipse([320 - 14, 660 - 14, 320 + 14, 660 + 14], fill=(168, 85, 247, 255), outline=(7, 10, 18, 255), width=2)
    draw.text((320, 660), "3", font=get_font(11, 'black'), fill=(7, 10, 18, 255), anchor='mm')
    draw.line([(334, 660), (550, 660)], fill=(168, 85, 247, 180), width=2)
    
    # Pin 4 on bottom reward
    draw.ellipse([320 - 14, 820 - 14, 320 + 14, 820 + 14], fill=(16, 185, 129, 255), outline=(7, 10, 18, 255), width=2)
    draw.text((320, 820), "4", font=get_font(11, 'black'), fill=(7, 10, 18, 255), anchor='mm')
    draw.line([(334, 820), (550, 820)], fill=(16, 185, 129, 180), width=2)
    
    # Right 4 Detailed UX Callout Cards
    rx = 580
    rw = 1240
    ry = 200
    rh = 175
    gap = 20
    
    callouts = [
        ("PIN 01", "gold", "우주 좌표 요약 카드 (Single Source of Truth)", 
         "복잡한 한자와 명리학 전문 용어를 과감히 생략하고, 사용자의 사주 일주를 '고유 우주 좌표'라는 메타포로 변환.\n우측의 [수정] 버튼을 통해 언제든 출생 정보를 원클릭 재설정할 수 있는 유연한 정보 아키텍처 제공.",
         "UX Rationale: 인지적 진입 장벽 70% 감소 및 직관적인 자아 정체성 각인 효과"),
        ("PIN 02", "cyan", "24절기 & 천간지지 우주 궤도 나침반", 
         "전통적인 방위와 계절의 흐름을 현대적인 우주 궤도 심볼로 시각화하여 현재 시간과의 천체 동기화 연출.\n중앙의 '음양(陰陽)' 코어를 터치하면 현재 시점의 에너지 활성도를 즉시 확인할 수 있는 마이크로 인터랙션 구현.",
         "UX Rationale: 시각적 흥미 유발 및 비과학적 미신감을 세련된 천체 과학 감성으로 전환"),
        ("PIN 03", "purple", "오늘의 도파민 시크릿 (Actionable Recommendation)", 
         "단순한 운세 문구가 아니라, '오늘 당신에게 금전운이 터지는 최적 시간: 14:30~16:00'과 같이 즉각 행동 가능한 솔루션 제시.\n주의 인물의 오행(예: 목 기운이 강한 사람)을 사전에 경고하여 일상 대인 관계의 실질적 가이드라인 제공.",
         "UX Rationale: 읽고 끝나는 운세가 아닌, 일상 행동에 직접 영향을 주는 실용적 가치 부여"),
        ("PIN 04", "green", "오늘의 무료 복채 출석 보상 (Retention Loop)", 
         "‘복채’라는 한국적 감성을 긍정적인 출석 리워드로 치환하여 매일 무료 하트를 지급하는 게이미피케이션 루프.\n연속 출석 달성 시 타로 리딩권 및 비밀 볼트 저장 공간을 확장해 주어 자발적인 D1/D7 재방문 유도.",
         "UX Rationale: D1 리텐션 64.2% 달성의 핵심 엔진이자 자연스러운 서비스 충성도 확보")
    ]
    
    for i, (pin_code, theme, c_title, c_desc, rationale) in enumerate(callouts):
        cy_box = ry + i * (rh + gap)
        draw.rounded_rectangle([rx, cy_box, rx + rw, cy_box + rh], radius=16, fill=(14, 20, 36, 230), outline=(229, 192, 123, 60), width=1)
        draw_pill_badge(draw, left_x=rx + 24, cy=cy_box + 26, text=pin_code, font=get_font(10, 'bold'), theme=theme, has_dot=False, pad_x=10, height=24)
        draw.text((rx + 110, cy_box + 26), c_title, font=get_font(17, 'bold'), fill=(244, 246, 252, 255), anchor='lm')
        
        # Desc
        dy = cy_box + 58
        for line in c_desc.split('\n'):
            draw.text((rx + 24, dy), line, font=get_font(12, 'regular'), fill=(203, 213, 225, 255))
            dy += 24
            
        # Rationale
        draw.rounded_rectangle([rx + 20, cy_box + 125, rx + rw - 20, cy_box + 160], radius=8, fill=(9, 13, 24, 220), outline=(229, 192, 123, 30), width=1)
        draw.text((rx + 34, cy_box + 142), f"✦ {rationale}", font=get_font(11, 'bold'), fill=(229, 192, 123, 255), anchor='lm')
        
    draw_slide_footer(draw, 6)
    base.save(f"{OUT_DIR}/slide_06.png")
    print("Slide 06 saved.")

# =========================================================================
# SLIDE 07: VISUAL DESIGN SYSTEM & BRAND TOKENS
# =========================================================================
def render_slide_07():
    base, draw = create_cosmic_base(center_orbit=(1600, 300))
    draw_slide_header(
        draw,
        slide_num=7,
        category_en="DESIGN SYSTEM | VISUAL TOKENS & COMPONENTS",
        title_white="우주의 신비로움과 골드 럭셔리를 융합한 ",
        title_gold="디자인 시스템 & 토큰",
        subtitle="Deep Obsidian, Imperial Gold, Aurora Violet을 아우르는 컬러 팔레트와 체계화된 타이포그래피"
    )
    
    # 1. Color Palette Swatches (Left Column)
    cw = 830
    ch = 770
    cx = 100
    cy = 190
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=20, fill=(14, 20, 36, 230), outline=(229, 192, 123, 60), width=1)
    draw_pill_badge(draw, left_x=cx + 24, cy=cy + 30, text="SEMANTIC COLOR SYSTEM & TOKENS", font=get_font(10, 'bold'), theme='gold', has_dot=True, pad_x=10, height=24)
    draw.line([(cx + 24, cy + 58), (cx + cw - 24, cy + 58)], fill=(229, 192, 123, 40), width=1)
    
    colors = [
        ("Deep Obsidian (Primary BG)", "#070A12", (7, 10, 18), "우주 심연의 깊이를 담아낸 다크 모드 기본 배경색"),
        ("Surface Slate (Surface)", "#0E1424", (14, 20, 36), "정보 계층을 분리하는 1차 카드 및 패널 배경"),
        ("Card Slate (Card Layer)", "#151C33", (21, 28, 51), "인터랙티브 모달 및 강조 섹션 2차 카드 배경"),
        ("Imperial Gold (Hero Accent)", "#FFD700", (255, 215, 0), "오늘의 길시, 1등 궁합 등 최고 가치를 강조하는 골드"),
        ("Champagne Gold (Brand Accent)", "#E5C07B", (229, 192, 123), "우아하고 차분한 하이엔드 럭셔리 라인 및 테두리"),
        ("Aurora Violet (Cosmic Glow)", "#8A2BE2", (138, 43, 226), "신비로운 우주 오행 궤도 및 타로 카드 글로우"),
        ("Cyan Neon (Data Highlight)", "#00E5FF", (0, 229, 255), "실시간 레이더 수치 및 오행 상생 강조 네온 컬러")
    ]
    
    sy = cy + 75
    for name, hex_code, rgb, desc in colors:
        draw.rounded_rectangle([cx + 24, sy, cx + 110, sy + 70], radius=12, fill=rgb, outline=(255, 255, 255, 40), width=1)
        draw.text((cx + 130, sy + 18), name, font=get_font(14, 'bold'), fill=(244, 246, 252, 255))
        draw.text((cx + 130, sy + 44), f"{hex_code}  ·  {desc}", font=get_font(11.5, 'regular'), fill=(163, 176, 204, 255))
        sy += 94
        
    # 2. Typography & Component Architecture (Right Column)
    rw = 830
    rx = 990
    draw.rounded_rectangle([rx, cy, rx + rw, cy + ch], radius=20, fill=(11, 16, 28, 230), outline=(229, 192, 123, 60), width=1)
    draw_pill_badge(draw, left_x=rx + 24, cy=cy + 30, text="TYPOGRAPHY HIERARCHY & COMPONENT ATOMS", font=get_font(10, 'bold'), theme='cyan', has_dot=True, pad_x=10, height=24)
    draw.line([(rx + 24, cy + 58), (rx + rw - 24, cy + 58)], fill=(229, 192, 123, 40), width=1)
    
    # Typography Scale
    draw.text((rx + 24, cy + 80), "Typography Scale (Pretendard Variable)", font=get_font(13.5, 'bold'), fill=(255, 215, 0, 255))
    typos = [
        ("Hero Display (36pt Bold)", "우주의 주파수와 사주 오행", "메인 타이틀 및 핵심 헤드라인"),
        ("Section Title (24pt Bold)", "나의 고유 우주 좌표 & 인연 매칭", "카드 타이틀 및 화면 상단 헤더"),
        ("Subhead (18pt Medium)", "복잡한 명리학 데이터를 4단계로 구조화", "중분류 및 핵심 설명 문구"),
        ("Body Regular (14pt Regular)", "사주 일주론과 서양 점성술의 결합을 통한 MZ세대 맞춤형 분석", "상세 설명 및 본문 단락"),
        ("Caption (11pt Regular)", "※ 본 포트폴리오는 60fps 인터랙티브 프로토타입으로 제공됩니다.", "부연 설명 및 데이터 출처")
    ]
    ty_y = cy + 115
    for scale_name, sample, usage in typos:
        draw.text((rx + 24, ty_y), scale_name, font=get_font(12, 'bold'), fill=(229, 192, 123, 255))
        draw.text((rx + 240, ty_y), sample, font=get_font(12.5, 'regular'), fill=(244, 246, 252, 255))
        draw.text((rx + 650, ty_y), usage, font=get_font(10.5, 'regular'), fill=(103, 117, 152, 255), anchor='ls')
        ty_y += 52
        
    draw.line([(rx + 24, ty_y + 10), (rx + rw - 24, ty_y + 10)], fill=(229, 192, 123, 40), width=1)
    
    # Component Atoms
    draw.text((rx + 24, ty_y + 30), "Core Component Atoms & Corner Radii", font=get_font(13.5, 'bold'), fill=(0, 229, 255, 255))
    atoms = [
        ("Corner Radius Tokens", "Radius 8px (Small Chips), 14px (Badges & Input), 20px (Main Cards), 28px (Hero Surfaces)"),
        ("Elevation & Shadow", "Glow 24px (rgba(138, 43, 226, 0.25)), Ambient Drop Shadow (rgba(0, 0, 0, 0.45))"),
        ("Interactive CTA Buttons", "52dp Standard Touch Target, Golden Gradient Background, 0.98 Scale Press Effect"),
        ("Haptic Feedback Levels", "Light (탭 전환), Medium (타로 카드 뒤집기), Heavy (궁합 매칭 성공 연출)")
    ]
    ay = ty_y + 65
    for a_name, a_desc in atoms:
        draw.text((rx + 24, ay), f"• {a_name}:", font=get_font(12, 'bold'), fill=(244, 246, 252, 255))
        draw.text((rx + 24, ay + 24), a_desc, font=get_font(11.5, 'regular'), fill=(163, 176, 204, 255))
        ay += 62
        
    draw_slide_footer(draw, 7)
    base.save(f"{OUT_DIR}/slide_07.png")
    print("Slide 07 saved.")

# =========================================================================
# SLIDE 08: DEEP DIVE 1 - FIVE ELEMENTS INTERACTIVE RADAR
# =========================================================================
def render_slide_08():
    base, draw = create_cosmic_base(center_orbit=(450, 550))
    draw_slide_header(
        draw,
        slide_num=8,
        category_en="CORE FEATURE DEEP DIVE 01 | FIVE ELEMENTS RADAR",
        title_white="나의 타고난 본질을 한눈에 파악하는 ",
        title_gold="오행 에너지 인터랙티브 레이더",
        subtitle="목(木)·화(火)·토(土)·금(金)·수(水)의 조화도를 실시간 5각형 다각형 차트로 시각화하여 결핍/과잉 기운 완벽 분석"
    )
    
    # Left Mockup
    m_path = f"{MOCKUP_DIR}/iphone_02_radar.png"
    if os.path.exists(m_path):
        m_img = Image.open(m_path).convert('RGBA')
        target_h = 770
        target_w = int(round(m_img.width * (target_h / m_img.height)))
        m_resized = m_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        base.paste(m_resized, (150, 195), m_resized)
        
    # Right Breakdown Cards
    rx = 570
    rw = 1250
    ry = 195
    rh = 230
    gap = 25
    
    features = [
        ("ALGORITHM 01", "gold", "실시간 5각형 오행 에너지 밸런스 연산", 
         "사주 만세력의 천간(10간)과 지지(12지) 8글자가 내포한 오행 속성을 정밀 가중치 공식으로 계산하여 100점 만점 지수로 변환.\n단순 텍스트 설명 대신 5각형 레이더 다각형으로 렌더링하여 나의 타고난 기질과 에너지 쏠림 현상을 0.1초 만에 인지 가능.",
         "• 목(木-성장/추진), 화(火-열정/표현), 토(土-중재/안정), 금(金-결단/원칙), 수(水-지혜/유연성)\n• 각 꼭짓점 터치 시 해당 기운의 강약 분석 모달 즉시 트리거"),
        ("INTERACTION 02", "cyan", "오행 상생·상극 순환 애니메이션", 
         "목생화(木生火), 화생토(火生土) 등 에너지가 순환하며 서로를 돕는 상생(相生) 관계와 과도함을 억제하는 상극(相剋) 관계를 파티클로 표현.\n차트 외곽의 순환 링을 회전시키며 내 사주 내에서 어떤 오행이 충돌하고 화합하는지 직관적으로 학습 가능.",
         "• 60fps 부드러운 캔버스 렌더링으로 프레임 드랍 제로화\n• 어려운 명리학 원리를 감각적인 인터랙티브 그래픽으로 완벽 치환"),
        ("SOLUTION 03", "purple", "결핍 기운 맞춤형 라이프스타일 처방", 
         "예를 들어 '불(火) 기운이 결핍'된 사용자에게는 열정을 돋우는 붉은색 계열 패션, 유산소 운동, 태양빛 산책 등의 행동 솔루션 추천.\n‘사주를 바꿀 수는 없지만, 일상 행동으로 보완한다’는 긍정적 자아 효능감(Self-Efficacy)을 극대화.",
         "• 일상 속에서 가볍게 실천할 수 있는 컬러/음식/방위 추천\n• 친구들에게 공유하고 함께 밸런스를 맞추는 바이럴 트리거 역할")
    ]
    
    for i, (badge_txt, theme, f_title, f_desc, bullets) in enumerate(features):
        cy_box = ry + i * (rh + gap)
        draw.rounded_rectangle([rx, cy_box, rx + rw, cy_box + rh], radius=18, fill=(14, 20, 36, 230), outline=(229, 192, 123, 60), width=1)
        draw_pill_badge(draw, left_x=rx + 24, cy=cy_box + 26, text=badge_txt, font=get_font(10, 'bold'), theme=theme, has_dot=False, pad_x=10, height=24)
        draw.text((rx + 160, cy_box + 26), f_title, font=get_font(17, 'bold'), fill=(244, 246, 252, 255), anchor='lm')
        
        # Desc
        dy = cy_box + 62
        for line in f_desc.split('\n'):
            draw.text((rx + 24, dy), line, font=get_font(12, 'regular'), fill=(203, 213, 225, 255))
            dy += 24
            
        # Bullets box
        draw.rounded_rectangle([rx + 20, cy_box + 145, rx + rw - 20, cy_box + 210], radius=10, fill=(9, 13, 24, 220), outline=(229, 192, 123, 30), width=1)
        by = cy_box + 155
        for line in bullets.split('\n'):
            draw.text((rx + 34, by), line, font=get_font(11, 'medium'), fill=(229, 192, 123, 255))
            by += 26
            
    draw_slide_footer(draw, 8)
    base.save(f"{OUT_DIR}/slide_08.png")
    print("Slide 08 saved.")

# =========================================================================
# SLIDE 09: DEEP DIVE 2 - COSMIC COMPATIBILITY MATCH ENGINE
# =========================================================================
def render_slide_09():
    base, draw = create_cosmic_base(center_orbit=(1500, 550))
    draw_slide_header(
        draw,
        slide_num=9,
        category_en="CORE FEATURE DEEP DIVE 02 | COMPATIBILITY MATCH ENGINE",
        title_white="두 사람의 사주와 별자리를 입체 분석하는 ",
        title_gold="정밀 궁합 매칭 알고리즘",
        subtitle="단순 점수 나열을 넘어 오행의 결합도와 상생 관계를 도출하여 최적의 관계 케미스트리 리포트 제공"
    )
    
    # Left Breakdown Cards
    lx = 100
    lw = 1250
    ly = 195
    lh = 230
    gap = 25
    
    match_features = [
        ("ENGINE 01", "gold", "92% 천생연분 케미스트리 종합 점수 산출", 
         "천간(정신적 교감)과 지지(현실적 라이프스타일), 그리고 12간지 동물 띠와 별자리 속성을 다차원 벡터로 결합.\n단순한 ‘좋다/나쁘다’의 이분법을 벗어나 두 사람이 만났을 때 폭발하는 긍정적 시너지 점수를 투명하게 공개.",
         "• 일주 간합(천간 결합) 및 삼합(지지 결합) 정밀 반영\n• 감정 교류 지수 95점, 가치관 일치도 88점 등 세부 지표 분리"),
        ("VISUAL 02", "purple", "두 사람의 오행 중첩 레이더 비교 UX", 
         "나의 오행 다각형(골드)과 상대방의 오행 다각형(퍼플)을 한 화면에 오버레이하여 빈틈없이 맞물리는 조화도 시각화.\n내가 부족한 '수(水)' 기운을 상대방이 넉넉히 채워주고, 상대방의 결핍을 내가 보완하는 '퍼즐 맞춤형' 연출.",
         "• 시각적 만족감을 극대화한 중첩 반투명 레이어 렌더링\n• '서로가 서로의 귀인(貴人)이 되어주는 이유'를 직관적으로 증명"),
        ("ACTION 03", "cyan", "갈등 예방 맞춤 대화법 & 실전 데이트 가이드", 
         "서로의 오행 충돌 지점(예: 성격이 급한 화 기운 vs 원칙적인 금 기운)에서 발생할 수 있는 오해를 예방하는 소통 화법 제안.\n두 사람의 에너지가 가장 조화로운 데이트 장소(예: 호수 공원, 전시회 등)와 추천 액티비티를 맞춤형 추천.",
         "• '화가 났을 때 이 사람에게 절대 하지 말아야 할 말'\n• 인연 관계를 깊어지게 만드는 최적의 대화 오프너 제공")
    ]
    
    for i, (badge_txt, theme, f_title, f_desc, bullets) in enumerate(match_features):
        cy_box = ly + i * (lh + gap)
        draw.rounded_rectangle([lx, cy_box, lx + lw, cy_box + lh], radius=18, fill=(14, 20, 36, 230), outline=(229, 192, 123, 60), width=1)
        draw_pill_badge(draw, left_x=lx + 24, cy=cy_box + 26, text=badge_txt, font=get_font(10, 'bold'), theme=theme, has_dot=False, pad_x=10, height=24)
        draw.text((lx + 150, cy_box + 26), f_title, font=get_font(17, 'bold'), fill=(244, 246, 252, 255), anchor='lm')
        
        dy = cy_box + 62
        for line in f_desc.split('\n'):
            draw.text((lx + 24, dy), line, font=get_font(12, 'regular'), fill=(203, 213, 225, 255))
            dy += 24
            
        draw.rounded_rectangle([lx + 20, cy_box + 145, lx + lw - 20, cy_box + 210], radius=10, fill=(9, 13, 24, 220), outline=(229, 192, 123, 30), width=1)
        by = cy_box + 155
        for line in bullets.split('\n'):
            draw.text((lx + 34, by), line, font=get_font(11, 'medium'), fill=(229, 192, 123, 255))
            by += 26
            
    # Right Mockup
    m_path = f"{MOCKUP_DIR}/iphone_05_match.png"
    if os.path.exists(m_path):
        m_img = Image.open(m_path).convert('RGBA')
        target_h = 770
        target_w = int(round(m_img.width * (target_h / m_img.height)))
        m_resized = m_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        base.paste(m_resized, (1420, 195), m_resized)
        
    draw_slide_footer(draw, 9)
    base.save(f"{OUT_DIR}/slide_09.png")
    print("Slide 09 saved.")

# =========================================================================
# SLIDE 10: HIGH-FIDELITY MOBILE SCREENS SHOWCASE
# =========================================================================
def render_slide_10():
    base, draw = create_cosmic_base(center_orbit=(960, 500))
    draw_slide_header(
        draw,
        slide_num=10,
        category_en="UI SCREEN GALLERY | HIGH-FIDELITY MOBILE SHOWCASE",
        title_white="다크 모드와 골드 악센트로 완성된 ",
        title_gold="하이엔드 모바일 스크린 라인업",
        subtitle="일관된 디자인 시스템과 디테일한 마이크로 인터랙션으로 완성된 4대 핵심 화면 쇼케이스"
    )
    
    mockup_list = [
        ("iphone_01_hub.png", "01. 우주 사주 허브", "나만의 우주 좌표 & 오늘의 운세"),
        ("iphone_02_radar.png", "02. 오행 레이더 분석", "5각형 실시간 에너지 밸런스"),
        ("iphone_03_tarot.png", "03. 럭셔리 타로 리딩", "물리 엔진 기반 햅틱 카드 플립"),
        ("iphone_04_connections.png", "04. 인연 매칭 & 볼트", "다중 인연 궁합 및 기록 보관")
    ]
    
    mw = 380
    mh = 700
    gap = 40
    start_x = 130
    start_y = 195
    
    for i, (fname, title, sub) in enumerate(mockup_list):
        mx = start_x + i * (mw + gap)
        m_path = f"{MOCKUP_DIR}/{fname}"
        if os.path.exists(m_path):
            m_img = Image.open(m_path).convert('RGBA')
            target_h = 670
            target_w = int(round(m_img.width * (target_h / m_img.height)))
            m_resized = m_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            
            # Subtle drop shadow
            shadow = Image.new('RGBA', (target_w + 40, target_h + 40), (0, 0, 0, 0))
            ImageDraw.Draw(shadow).rounded_rectangle([15, 15, target_w + 25, target_h + 25], radius=40, fill=(0, 0, 0, 140))
            shadow = shadow.filter(ImageFilter.GaussianBlur(20))
            base.paste(shadow, (mx + (mw - target_w) // 2 - 10, start_y - 5), shadow)
            base.paste(m_resized, (mx + (mw - target_w) // 2, start_y), m_resized)
            
        # Label Below
        label_y = start_y + 695
        draw_pill_badge(draw, cx=mx + mw // 2, cy=label_y, text=title, font=get_font(11, 'bold'), theme='gold', has_dot=False, pad_x=12, height=28)
        draw.text((mx + mw // 2, label_y + 32), sub, font=get_font(12, 'regular'), fill=(163, 176, 204, 255), anchor='mm')
        
    draw_slide_footer(draw, 10)
    base.save(f"{OUT_DIR}/slide_10.png")
    print("Slide 10 saved.")

# =========================================================================
# SLIDE 11: BUSINESS IMPACT & STAR RETROSPECTIVE
# =========================================================================
def render_slide_11():
    base, draw = create_cosmic_base(center_orbit=(1400, 700))
    draw_slide_header(
        draw,
        slide_num=11,
        category_en="BUSINESS IMPACT & DESIGN RETROSPECTIVE",
        title_white="정량적 사용자 지표 향상과 ",
        title_gold="시니어 디자이너로서의 회고",
        subtitle="출시 후 사용자 행동 분석 데이터 및 기술적 난제 해결 과정을 담은 STAR 기법 기반 회고록"
    )
    
    # 4 Quantitative Metric Cards
    mw = 405
    mh = 200
    gap = 30
    my = 195
    
    metrics = [
        ("D1 RETENTION RATE", "green", "64.2%", "+28.2%p", "업계 평균 36% 대비 압도적 재방문율 달성"),
        ("AVERAGE SESSION TIME", "gold", "8분 24초", "2.8배 증가", "전통 텍스트 운세 앱 대비 깊은 몰입도 입증"),
        ("COMPATIBILITY SHARING", "cyan", "41.8%", "바이럴 형성", "인스타그램 스토리 및 카톡 공유 급증"),
        ("SECRET VAULT CONV.", "purple", "18.7%", "수익성 검증", "유료 기록 보관함 및 무제한 타로 구독 전환")
    ]
    
    for i, (kicker, theme, val, badge_txt, desc) in enumerate(metrics):
        mx = 100 + i * (mw + gap)
        draw.rounded_rectangle([mx, my, mx + mw, my + mh], radius=18, fill=(14, 20, 36, 230), outline=(229, 192, 123, 60), width=1)
        draw_pill_badge(draw, left_x=mx + 20, cy=my + 28, text=kicker, font=get_font(9.5, 'bold'), theme=theme, has_dot=False, pad_x=10, height=22)
        draw_pill_badge(draw, left_x=mx + mw - 110, cy=my + 28, text=badge_txt, font=get_font(9.5, 'bold'), theme='gold', has_dot=False, pad_x=8, height=22)
        
        draw.text((mx + 20, my + 100), val, font=get_font(42, 'bold'), fill=(255, 215, 0, 255))
        draw.text((mx + 20, my + 155), desc, font=get_font(12, 'regular'), fill=(163, 176, 204, 255))
        
    # STAR Retrospective Box
    star_y = 435
    star_h = 530
    draw.rounded_rectangle([100, star_y, 1820, star_y + star_h], radius=20, fill=(11, 16, 28, 230), outline=(229, 192, 123, 60), width=1)
    draw.text((130, star_y + 32), "STAR METHOD RETROSPECTIVE (200자 이상의 기술적 UX 회고)", font=get_font(13, 'bold'), fill=(255, 215, 0, 255))
    draw.line([(130, star_y + 60), (1790, star_y + 60)], fill=(229, 192, 123, 40), width=1)
    
    star_items = [
        ("Situation (상황 & 문제)", "gold", 
         "기존 동양 명리학 기반의 운세/사주 서비스들은 어려운 한자어가 화면 전체를 뒤덮고, 액운이나 살과 같은 공포 마케팅에 의존하여 2030 MZ세대의 일상적인 이용과 자발적인 공유를 가로막고 있었습니다. 긴 텍스트로 인해 이탈률이 70%에 달했고, 궁합 결과 역시 단순 점수만 제공되어 실질적인 관계 솔루션 역할을 하지 못했습니다."),
        ("Task (과제 & 목표)", "cyan", 
         "명리학의 방대한 4주 8글자 데이터를 0.3초 만에 시각화하는 '우주 좌표 메타포'를 수립하고, 목화토금수 5대 에너지를 5각형 실시간 레이더 차트로 재정의해야 했습니다. 또한 2030 세대가 거부감 없이 즐길 수 있도록 서양 점성술과 도파민 타로 카드를 결합한 하이엔드 럭셔리 다크 UI 디자인 시스템을 구축하는 것이 핵심 과제였습니다."),
        ("Action (실행 & 디자인 솔루션)", "purple", 
         "첫째, 점진적 정보 노출(Progressive Disclosure) 원칙을 적용하여 초심자에게는 핵심 우주 좌표와 오행 요약만 노출하고, 상세 만세력은 토글형으로 분리했습니다. 둘째, 상대방과의 오행 중첩 레이더 차트를 설계하여 결핍된 기운의 상호 보완성을 시각적으로 입증했습니다. 셋째, 60fps 물리 엔진 기반의 햅틱 타로 플립 인터랙션을 구현하고, 디자인 토큰(Color, Typography, Elevation)을 컴포넌트화하여 엔지니어링 개발 효율을 300% 극대화했습니다."),
        ("Result (성과 & 배운 점)", "green", 
         "출시 직후 D1 리텐션 64.2%를 기록하며 업계 평균(36%)을 크게 상회했고, 평균 체류 시간은 8분 24초로 전통 운세 앱 대비 2.8배 증가했습니다. 특히 궁합 카드의 감각적인 비주얼 덕분에 인스타그램 공유율 41.8%를 달성하여 오가닉 바이럴 성장을 이끌어냈습니다. 본 프로젝트를 통해 복잡한 전통 지식도 세련된 데이터 시각화와 디테일한 마이크로 인터랙션을 만나면 현대적인 럭셔리 프로덕트로 재탄생할 수 있음을 입증했습니다.")
    ]
    
    sy = star_y + 80
    for s_title, s_theme, s_text in star_items:
        draw_pill_badge(draw, left_x=130, cy=sy + 12, text=s_title, font=get_font(10.5, 'bold'), theme=s_theme, has_dot=False, pad_x=10, height=24)
        
        # Word wrap text
        words = s_text
        step = 88
        l1 = words[:step]
        l2 = words[step:step*2]
        l3 = words[step*2:]
        draw.text((360, sy), l1, font=get_font(12, 'regular'), fill=(244, 246, 252, 255))
        if l2:
            draw.text((360, sy + 24), l2, font=get_font(12, 'regular'), fill=(244, 246, 252, 255))
        if l3:
            draw.text((360, sy + 48), l3, font=get_font(12, 'regular'), fill=(244, 246, 252, 255))
        sy += 105
        
    draw_slide_footer(draw, 11)
    base.save(f"{OUT_DIR}/slide_11.png")
    print("Slide 11 saved.")

# =========================================================================
# SLIDE 12: LIVE PROTOTYPE INTERACTIVE HUB
# =========================================================================
def render_slide_12():
    base, draw = create_cosmic_base(center_orbit=(1450, 520))
    draw_slide_header(
        draw,
        slide_num=12,
        category_en="INTERACTIVE PROTOTYPE | 60FPS LIVE EXPERIENCE",
        title_white="웹에서 즉시 체험 가능한 ",
        title_gold="60fps 인터랙티브 프로토타입 허브",
        subtitle="실제 디바이스와 100% 동일한 반응속도, 상태 전환, 제스처를 지원하는 라이브 프로토타입 체험"
    )
    
    # Left Presentation & Guide Card
    cw = 960
    ch = 770
    cx = 100
    cy = 195
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=20, fill=(14, 20, 36, 230), outline=(229, 192, 123, 70), width=1)
    draw_pill_badge(draw, left_x=cx + 24, cy=cy + 30, text="HIGH-FIDELITY LIVE INTERACTIVE SIMULATOR", font=get_font(10, 'bold'), theme='gold', has_dot=True, pad_x=10, height=24)
    draw.line([(cx + 24, cy + 58), (cx + cw - 24, cy + 58)], fill=(229, 192, 123, 40), width=1)
    
    draw.text((cx + 24, cy + 85), "웹 브라우저에서 직접 조작 가능한 4대 핵심 인터랙션 플로우", font=get_font(18, 'bold'), fill=(244, 246, 252, 255))
    
    flows = [
        ("FLOW 01", "gold", "우주 사주 허브 & 천체 나침반", 
         "• 생년월일 기반 우주 좌표 카드 및 24절기 천체 궤도 인터랙션\n• 오늘의 황금 시간대 및 오행 에너지 실시간 피드백 확인"),
        ("FLOW 02", "purple", "오행 에너지 인터랙티브 레이더", 
         "• 목화토금수 5각형 다각형 차트 터치 및 꼭짓점 반응\n• 부족한 기운을 채워주는 맞춤 라이프스타일 솔루션 확인"),
        ("FLOW 03", "cyan", "사주 & 별자리 정밀 궁합 매칭", 
         "• 바텀 시트 모달을 통한 1-Tap 상대방 정보 입력 및 전환\n• 92% 천생연분 케미스트리 및 오행 중첩 레이더 비교"),
        ("FLOW 04", "green", "도파민 럭셔리 타로 & 시크릿 볼트", 
         "• 물리 엔진 기반 3D 카드 셔플 및 햅틱 카드 뒤집기 경험\n• 개인화된 타로 해석 확인 및 시크릿 볼트에 암호화 영구 저장")
    ]
    
    fy = cy + 130
    for f_code, f_theme, f_title, f_desc in flows:
        draw.rounded_rectangle([cx + 20, fy, cx + cw - 20, fy + 105], radius=12, fill=(10, 14, 26, 220), outline=(229, 192, 123, 30), width=1)
        draw_pill_badge(draw, left_x=cx + 34, cy=fy + 24, text=f_code, font=get_font(9.5, 'bold'), theme=f_theme, has_dot=False, pad_x=8, height=22)
        draw.text((cx + 120, fy + 24), f_title, font=get_font(14, 'bold'), fill=(244, 246, 252, 255), anchor='lm')
        draw.text((cx + 34, fy + 52), f_desc, font=get_font(11.5, 'regular'), fill=(163, 176, 204, 255))
        fy += 122
        
    # Launch CTA Button
    btn_y = cy + 640
    draw.rounded_rectangle([cx + 20, btn_y, cx + cw - 20, btn_y + 80], radius=14, fill=(35, 30, 15, 255), outline=(255, 215, 0, 220), width=2)
    draw.text((cx + cw // 2, btn_y + 40), "[ 포춘매치 60fps 인터랙티브 프로토타입 체험하기 (Click to Launch) ]", font=get_font(15, 'bold'), fill=(255, 215, 0, 255), anchor='mm')
    
    # Right Mockup Showcase
    m_path = f"{MOCKUP_DIR}/iphone_01_hub.png"
    if os.path.exists(m_path):
        m_img = Image.open(m_path).convert('RGBA')
        target_h = 770
        target_w = int(round(m_img.width * (target_h / m_img.height)))
        m_resized = m_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        shadow = Image.new('RGBA', (target_w + 60, target_h + 60), (0, 0, 0, 0))
        ImageDraw.Draw(shadow).rounded_rectangle([20, 20, target_w + 40, target_h + 40], radius=45, fill=(0, 0, 0, 150))
        shadow = shadow.filter(ImageFilter.GaussianBlur(25))
        base.paste(shadow, (1310, 185), shadow)
        base.paste(m_resized, (1340, 195), m_resized)
        
    draw_slide_footer(draw, 12)
    base.save(f"{OUT_DIR}/slide_12.png")
    print("Slide 12 saved.")

# =========================================================================
# MAIN GENERATOR
# =========================================================================
if __name__ == '__main__':
    print("Generating all 12 FortuneMatch Behance Slides...")
    render_slide_01()
    render_slide_02()
    render_slide_03()
    render_slide_04()
    render_slide_05()
    render_slide_06()
    render_slide_07()
    render_slide_08()
    render_slide_09()
    render_slide_10()
    render_slide_11()
    render_slide_12()
    print("All 12 FortuneMatch slides generated successfully!")
