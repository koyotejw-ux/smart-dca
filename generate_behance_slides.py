import os
import numpy as np
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


def draw_pill_badge(draw, cx=None, cy=0, text="", font=None, theme='blue', has_dot=True, dark_mode=True, pad_x=14, height=30, left_x=None):
    """
    Renders a mathematically centered, high-contrast, beautiful pill badge with pixel-perfect alignment.
    Supports themes: 'blue', 'green', 'red', 'amber', 'purple', 'cyan', 'slate', 'dark'.
    Can be positioned by center (cx, cy) or aligned by left edge (left_x, cy).
    """
    if font is None:
        font = get_font(10.5, 'bold')
        
    color_schemes_dark = {
        'blue':   {'bg': (16, 42, 86, 255),  'border': (0, 140, 255, 255),  'text': (0, 215, 255, 255),  'dot': (0, 215, 255, 255)},
        'cyan':   {'bg': (8, 48, 64, 255),   'border': (0, 210, 255, 255),  'text': (0, 230, 255, 255),  'dot': (0, 230, 255, 255)},
        'green':  {'bg': (12, 48, 36, 255),  'border': (16, 185, 129, 255), 'text': (52, 211, 153, 255), 'dot': (16, 185, 129, 255)},
        'red':    {'bg': (58, 20, 24, 255),  'border': (239, 68, 68, 255),  'text': (255, 140, 140, 255),'dot': (239, 68, 68, 255)},
        'amber':  {'bg': (54, 38, 12, 255),  'border': (245, 158, 11, 255), 'text': (251, 191, 36, 255), 'dot': (245, 158, 11, 255)},
        'purple': {'bg': (42, 22, 70, 255),  'border': (168, 85, 247, 255), 'text': (216, 180, 254, 255),'dot': (168, 85, 247, 255)},
        'slate':  {'bg': (30, 41, 59, 255),  'border': (100, 116, 139, 255),'text': (226, 232, 240, 255),'dot': (148, 163, 184, 255)},
        'dark':   {'bg': (15, 23, 42, 255),  'border': (51, 65, 85, 255),   'text': (255, 255, 255, 255),'dot': (0, 215, 255, 255)},
    }
    color_schemes_light = {
        'blue':   {'bg': (239, 246, 255, 255), 'border': (147, 197, 253, 255), 'text': (29, 78, 216, 255),  'dot': (37, 99, 235, 255)},
        'cyan':   {'bg': (236, 254, 255, 255), 'border': (103, 232, 249, 255), 'text': (14, 116, 144, 255), 'dot': (6, 182, 212, 255)},
        'green':  {'bg': (236, 253, 245, 255), 'border': (110, 231, 183, 255), 'text': (6, 95, 70, 255),    'dot': (16, 185, 129, 255)},
        'red':    {'bg': (254, 242, 242, 255), 'border': (252, 165, 165, 255), 'text': (153, 27, 27, 255),  'dot': (220, 38, 38, 255)},
        'amber':  {'bg': (254, 243, 199, 255), 'border': (252, 211, 77, 255),  'text': (146, 64, 14, 255),  'dot': (217, 119, 6, 255)},
        'purple': {'bg': (245, 243, 255, 255), 'border': (216, 180, 254, 255), 'text': (109, 40, 217, 255), 'dot': (147, 51, 234, 255)},
        'slate':  {'bg': (241, 245, 249, 255), 'border': (203, 213, 225, 255), 'text': (51, 65, 85, 255),   'dot': (100, 116, 139, 255)},
        'dark':   {'bg': (15, 23, 42, 255),    'border': (15, 23, 42, 255),     'text': (255, 255, 255, 255),'dot': (0, 210, 255, 255)},
    }
    
    scheme = color_schemes_dark.get(theme, color_schemes_dark['blue']) if dark_mode else color_schemes_light.get(theme, color_schemes_light['blue'])
    
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    dot_diameter = 7
    dot_gap = 8
    
    if has_dot:
        content_w = dot_diameter + dot_gap + tw
    else:
        content_w = tw
        
    bw = int(content_w + pad_x * 2)
    bh = int(height)
    radius = bh // 2
    
    if left_x is not None:
        bx1 = int(round(left_x))
        bx2 = bx1 + bw
        cx = (bx1 + bx2) / 2.0
    else:
        bx1 = int(round(cx - bw / 2.0))
        bx2 = bx1 + bw
        
    by1 = int(round(cy - bh / 2.0))
    by2 = by1 + bh
    
    # Draw pill container
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=radius, fill=scheme['bg'], outline=scheme['border'], width=1)
    
    # Calculate exact vertical text position using bbox center
    ty = int(round(cy - (bbox[1] + bbox[3]) / 2.0))
    
    if has_dot:
        content_x1 = cx - content_w / 2.0
        dot_cx = content_x1 + dot_diameter / 2.0
        dot_cy = cy
        r = dot_diameter / 2.0
        draw.ellipse([int(round(dot_cx - r)), int(round(dot_cy - r)), int(round(dot_cx + r)), int(round(dot_cy + r))], fill=scheme['dot'])
        
        tx = int(round(content_x1 + dot_diameter + dot_gap - bbox[0]))
    else:
        tx = int(round(cx - (bbox[0] + bbox[2]) / 2.0))
        
    draw.text((tx, ty), text, font=font, fill=scheme['text'])
    return bx1, by1, bx2, by2

def draw_branch_badge(draw, cx, cy, text, is_yes=True):
    """Draws a clean, high-contrast, solid badge for YES / NO branches positioned with clear margins."""
    return draw_pill_badge(draw, cx, cy, text, theme='green' if is_yes else 'red', has_dot=False, dark_mode=False, pad_x=10, height=22)

def find_perspective_coeffs(source_coords, target_coords):
    """Computes homography coefficients for PIL inverse perspective transform."""
    matrix = []
    for (x_t, y_t), (x_s, y_s) in zip(target_coords, source_coords):
        matrix.append([x_t, y_t, 1, 0, 0, 0, -x_s * x_t, -x_s * y_t])
        matrix.append([0, 0, 0, x_t, y_t, 1, -y_s * x_t, -y_s * y_t])
    A = np.matrix(matrix, dtype=float)
    B = np.array(source_coords).reshape(8)
    res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
    return np.array(res).reshape(8)

def render_3d_phone(device_img, target_corners, depth=20, extrude_dir=(-14, 12), canvas_size=(W, H)):
    """
    Renders a 3D perspective flagship smartphone with realistic metallic chassis depth extrusion.
    """
    cw, ch = canvas_size
    dw, dh = device_img.size
    src_corners = [(0, 0), (dw, 0), (dw, dh), (0, dh)]
    
    t_tl, t_tr, t_br, t_bl = target_corners
    dx, dy = extrude_dir
    
    # 1. Extrude 3D Chassis Depth Layers (Back-to-Front)
    chassis_canvas = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
    dev_mask = device_img.split()[3]
    
    for step in range(depth, 0, -1):
        ratio = step / depth
        # Dark metallic titanium transition
        v = int(16 + (1 - ratio) * 50)
        step_corners = [
            (t_tl[0] + int(dx * ratio), t_tl[1] + int(dy * ratio)),
            (t_tr[0] + int(dx * ratio), t_tr[1] + int(dy * ratio)),
            (t_br[0] + int(dx * ratio), t_br[1] + int(dy * ratio)),
            (t_bl[0] + int(dx * ratio), t_bl[1] + int(dy * ratio))
        ]
        step_coeffs = find_perspective_coeffs(src_corners, step_corners)
        step_mask = dev_mask.transform((cw, ch), Image.Transform.PERSPECTIVE, step_coeffs, Image.Resampling.BICUBIC)
        
        col_img = Image.new('RGBA', (cw, ch), (v, v + 6, v + 16, 255))
        chassis_canvas.paste(col_img, (0, 0), step_mask)
        
    # 2. Front Face Perspective Transform (Pure Authentic Screenshot + Bezel)
    front_coeffs = find_perspective_coeffs(src_corners, target_corners)
    phone_front = device_img.transform((cw, ch), Image.Transform.PERSPECTIVE, front_coeffs, Image.Resampling.BICUBIC)
    
    # 3. Subtle Glass Specular Reflection Highlight (Very soft 15-alpha sheen)
    specular = Image.new('RGBA', (dw, dh), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(specular)
    s_draw.polygon([(0, 0), (dw // 2, 0), (0, dh // 2)], fill=(255, 255, 255, 14))
    specular_transformed = specular.transform((cw, ch), Image.Transform.PERSPECTIVE, front_coeffs, Image.Resampling.BICUBIC)
    
    # Composite Phone front onto chassis
    composite = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
    composite.paste(chassis_canvas, (0, 0), chassis_canvas)
    composite.paste(phone_front, (0, 0), phone_front)
    composite = Image.alpha_composite(composite, specular_transformed)
    
    return composite

# SLIDE 01: Hero Cover & Value Proposition (Stealth Masculine Keynote)
# ==============================================================
def make_slide_01():
    base = Image.new('RGBA', (W, H), (9, 13, 22, 255))
    
    # Ambient Lighting (Samsung Galaxy Blue Atmosphere)
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([950, 100, 1850, 950], fill=(0, 87, 255, 45))
    gw.ellipse([1150, 250, 1750, 880], fill=(0, 210, 255, 28))
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
    
    # Live Store Badge (100% Mathematically Centered Pill Badge)
    draw_pill_badge(draw, 1695, 138, "PLAY STORE LIVE", theme='green', has_dot=True, dark_mode=True, height=32)
    
    # Headline - Minimalist & Punchy
    draw.text((120, 190), "Smart DCA Calculator", font=get_font(56, 'black'), fill=(255, 255, 255))
    
    # Subtitle - Clean, High-End Core Value
    draw.text((120, 275), "급락장의 패닉을 이성적 확신으로 바꾸는 스마트 분할매수 솔루션", font=get_font(20, 'bold'), fill=(0, 210, 255))
    draw.text((120, 316), "0.2초 음성 입력과 목표 평단가 역산으로 투자자의 마음과 계좌를 함께 지킵니다.", font=get_font(15.5, 'regular'), fill=(148, 163, 184))
    
    # 3 High-Impact Metric Cards (Left: x=120..880, y=420..820)
    metrics = [
        ("0.2s", "VOICE INPUT", "호가 급락 시 오타 없는 0.2초 음성 인식 및 원터치 호가 프리셋", "cyan"),
        ("100%", "GOAL-SEEKING", "희망 탈출 가격에 도달하기 위한 최적 매수 수량 및 소요 자금 산출", "blue"),
        ("24h", "CLEAN SESSION", "긴박한 금융 판단을 방해받지 않는 24시간 무광고 안심 환경", "green")
    ]
    my = 430
    for val, tag, desc, theme in metrics:
        draw.rounded_rectangle([120, my, 880, my + 110], radius=14, fill=(16, 22, 34, 230), outline=(255, 255, 255, 20), width=1)
        draw.rounded_rectangle([120, my + 16, 124, my + 94], radius=2, fill=(0, 114, 255))
        
        draw.text((148, my + 20), val, font=get_num_font(40, 'black'), fill=(255, 255, 255))
        
        # Pill Badge aligned on a clean vertical axis (x=310) with perfect centering and high contrast
        draw_pill_badge(draw, cy=my + 38, text=tag, font=get_font(10, 'bold'), theme=theme, has_dot=False, dark_mode=True, pad_x=10, height=24, left_x=310)
        
        draw.text((148, my + 72), desc, font=get_font(13.5, 'regular'), fill=(148, 163, 184))
        my += 132
        
    # ==============================================================
    # RIGHT SIDE: Dual 3D Flagship Phones in Studio Perspective
    # ==============================================================
    dev_sim = Image.open('portfolio/iphone_mockups/iphone_02_sim.png').convert('RGBA')
    dev_home = Image.open('portfolio/iphone_mockups/iphone_01_home.png').convert('RGBA')
    
    # 3D Soft Floor Contact Shadows
    sh = Image.new('RGBA', (W, H), (0,0,0,0))
    shd = ImageDraw.Draw(sh)
    # Shadow under back phone
    shd.ellipse([1260, 845, 1680, 925], fill=(0, 0, 0, 220))
    # Shadow under front phone
    shd.ellipse([930, 895, 1380, 975], fill=(0, 0, 0, 255))
    sh = sh.filter(ImageFilter.GaussianBlur(32))
    base = Image.alpha_composite(base, sh)
    
    # 1. Back 3D Phone: DCA Simulator (Slightly higher, angled in 3D)
    # [Top-Left, Top-Right, Bottom-Right, Bottom-Left]
    back_corners = [
        (1340, 130),
        (1670, 175),
        (1570, 880),
        (1240, 825)
    ]
    phone_3d_back = render_3d_phone(dev_sim, back_corners, depth=18, extrude_dir=(-14, 10))
    base = Image.alpha_composite(base, phone_3d_back)
    
    # 2. Front 3D Phone: Smart Portfolio Dashboard (Foreground hero focal point)
    front_corners = [
        (1010, 165),
        (1370, 215),
        (1255, 955),
        (895, 890)
    ]
    phone_3d_front = render_3d_phone(dev_home, front_corners, depth=22, extrude_dir=(-16, 12))
    base = Image.alpha_composite(base, phone_3d_front)
    
    # Floating App Icon Squircle
    icon = Image.open('assets/app_icon_clean_squircle.png').convert('RGBA')
    icon_w = 155
    icon = icon.resize((icon_w, icon_w), Image.Resampling.LANCZOS)
    
    icon_sh = Image.new('RGBA', (W, H), (0,0,0,0))
    isd = ImageDraw.Draw(icon_sh)
    isd.ellipse([1360, 715, 1360 + icon_w, 715 + 36], fill=(0, 0, 0, 230))
    icon_sh = icon_sh.filter(ImageFilter.GaussianBlur(22))
    base = Image.alpha_composite(base, icon_sh)
    base.paste(icon, (1360, 580), icon)
    
    base.save(f'{OUT_DIR}/slide_01.png')
    print("SAVED slide_01.png (Pristine 3D Flagship Presentation)")

# SLIDE 02: Discovery & User Research (Stark High-Contrast Editorial)
# ==============================================================
def make_slide_02():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Hairline Grid Accents
    draw.line([(120, 100), (1800, 100)], fill=(226, 232, 240), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(226, 232, 240), width=1)
    
    # Header - Minimalist & Punchy
    draw.text((120, 130), "01  /  USER RESEARCH", font=get_font(13, 'bold'), fill=(0, 87, 255))
    draw.text((120, 165), "User Research", font=get_font(52, 'black'), fill=(15, 23, 42))
    draw.text((120, 240), "투자자 428명 설문과 심층 인터뷰에서 발견한 3대 핵심 문제", font=get_font(18, 'regular'), fill=(100, 116, 139))
    
    # Left Column: 3 Massive Stat Cards (Architectural & Masculine)
    stats = [
        ("82.6%", "손실 회피와 비이성적 물타기", "출구 전략이 없어 손실을 메우려다 더 큰 위험에 노출되는 악순환", (220, 38, 38)),
        ("240s→4.2s", "급박한 순간의 타이핑 스트레스", "8자리 소수점 단가를 치는 동안 호가가 이탈하는 극심한 피로감", (217, 119, 6)),
        ("0 / 14개", "기존 증권사 앱의 역산 부재", "단순히 평단을 더해줄 뿐 '얼마나 더 사야 하는가'에 답하지 못함", (0, 87, 255))
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
        ("01", "비중 왜곡 : 무계획 추가 매수로 계좌가 묶이는 악순환",
         "\"단가를 낮추려 4차까지 추가 매수했지만, 예수금 78%가 한 종목에 물렸고 평단은 겨우 1.8% 내려갔습니다.\"\n— 3년 차 스윙 투자자 인터뷰",
         "단일 종목 편중 경고와 차수별 방어 효과를 실시간으로 보여주어 무리한 물타기 방지", (220, 38, 38)),
         
        ("02", "조작 피로 : 초 단위 폭락 장세에서의 입력 지연과 스트레스",
         "\"호가가 무너지는 순간 키보드로 가격을 입력하다 지지선을 놓쳐 -6.4% 추가 손실을 봤습니다.\"\n— 모멘텀 단타 / 크립토 트레이더 인터뷰",
         "0.2초 음성 입력과 원터치 호가 프리셋 칩으로 긴박한 순간의 타이핑 스트레스 제거", (217, 119, 6)),
         
        ("03", "목표 부재 : 손익분기점 탈출에 필요한 정확한 수량의 부재",
         "\"희망 매도가로 탈출하기 위해 정확히 몇 주를 얼마에 사야 하는지 계산할 수 없어 맹목적으로 샀습니다.\"\n— 5년 차 퀀트 투자자 인터뷰",
         "목표 탈출가 입력 즉시 필요한 정확한 수량과 자금을 한눈에 보여주는 역산 솔루션", (0, 87, 255))
    ]
    
    ry = 300
    for num, ptitle, pquote, psol, pcol in cards:
        draw.rounded_rectangle([660, ry, 1800, ry + 195], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        
        # Number badge (Perfect Mathematical Centering)
        draw.rounded_rectangle([695, ry + 24, 735, ry + 56], radius=6, fill=(15, 23, 42))
        n_bbox = draw.textbbox((0, 0), num, font=get_num_font(15, 'bold'))
        draw.text((715 - (n_bbox[0] + n_bbox[2]) / 2, ry + 40 - (n_bbox[1] + n_bbox[3]) / 2), num, font=get_num_font(15, 'bold'), fill=(255, 255, 255))
        draw.text((750, ry + 28), ptitle, font=get_font(17.5, 'bold'), fill=(15, 23, 42))
        
        # Quote Card
        draw.rounded_rectangle([695, ry + 68, 1765, ry + 128], radius=8, fill=(248, 250, 252))
        lines = wrap_text_by_words(pquote, get_font(13.5, 'regular'), 1030, draw)
        qy = ry + 76
        for line in lines[:2]:
            draw.text((715, qy), line, font=get_font(13.5, 'regular'), fill=(71, 85, 105))
            qy += 22
            
        # Solution Tag (High-Contrast Pill Badge)
        _, _, bx2, _ = draw_pill_badge(draw, 735, ry + 158, "SOLUTION", font=get_font(10.5, 'bold'), theme='blue', has_dot=False, dark_mode=False, pad_x=10, height=24)
        psol_bbox = draw.textbbox((0, 0), psol, font=get_font(13.5, 'semibold'))
        psol_ty = int(round(ry + 158 - (psol_bbox[1] + psol_bbox[3]) / 2.0))
        draw.text((bx2 + 14, psol_ty), psol, font=get_font(13.5, 'semibold'), fill=(30, 41, 59))
        
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
    
    draw.text((120, 130), "02  /  PERSONA & VALUE", font=get_font(13, 'bold'), fill=(0, 87, 255))
    draw.text((120, 165), "Persona & Value", font=get_font(52, 'black'), fill=(15, 23, 42))
    draw.text((120, 240), "기존 앱과의 차별점 비교 및 대표 타깃 페르소나 분석", font=get_font(18, 'regular'), fill=(100, 116, 139))
    
    # Left: High-Precision Comparison Matrix
    tx = 120
    ty = 300
    tw = 960
    draw.rounded_rectangle([tx, ty, tx + tw, ty + 645], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    # Table Header
    draw.rounded_rectangle([tx, ty, tx + tw, ty + 56], radius=16, fill=(241, 245, 249))
    draw.text((tx + 28, ty + 18), "비교 영역 (Dimensions)", font=get_font(14, 'bold'), fill=(71, 85, 105))
    draw.text((tx + 200, ty + 18), "증권사 MTS 내장 (Legacy)", font=get_font(13.5, 'bold'), fill=(71, 85, 105))
    draw.text((tx + 410, ty + 18), "일반 유틸 계산기 (Ad-Heavy)", font=get_font(13.5, 'bold'), fill=(71, 85, 105))
    
    col4_l = tx + 620
    col4_r = tx + tw - 10
    draw.rounded_rectangle([col4_l, ty + 6, col4_r, ty + 639], radius=12, fill=(240, 246, 255), outline=(186, 215, 255), width=2)
    draw.rounded_rectangle([col4_l + 12, ty + 12, col4_r - 12, ty + 50], radius=8, fill=(0, 87, 255))
    draw.text((col4_l + 38, ty + 20), "SMART DCA CALCULATOR", font=get_font(12, 'bold'), fill=(255, 255, 255))
    
    matrix = [
        ("입력 인터랙션 (Modality)", "단일 키패드 (Keypad Only)", "광고 지연 키패드 (Heavy Ad)", "멀티모달 (AI 음성 + 호가 칩)"),
        ("핵심 연산 모델 (Engine)", "단순 가중평균 (사후 합산)", "1회성 단일 수식 (휘발성)", "목표가 기반 폐쇄형 역산 엔진"),
        ("의사결정 지원 (Decision)", "단일 수치 나열", "미지원", "A vs B 전략 실시간 대조 매트릭스"),
        ("자산 안전 가드 (Safety)", "계좌 평가액 단순 나열", "미지원", "단일 종목 편중 및 예수금 고갈 경보"),
        ("개인 데이터 보안 (Privacy)", "중앙 서버 종속 (공인인증)", "임시 세션 (앱 종료 시 리셋)", "100% 온디바이스 로컬 저장"),
        ("사용자 경험 보호 (Session)", "타사 금융 상품 배너 혼재", "무차별 전면 팝업 (피로도 극심)", "24시간 안심 무광고 리워드 세션"),
        ("시각 편의성 (A11y)", "다크모드 미흡 / 저대비", "단순 그레이스케일 반전", "야간 최적화 OLED AAA 고대비")
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
    _, _, bx2_a, _ = draw_pill_badge(draw, cy=py + 36, text="ARCHETYPE A", font=get_font(10, 'bold'), theme='blue', has_dot=True, dark_mode=False, pad_x=10, height=26, left_x=px + 28)
    name_a = "김투자 (34세, 적립식 직장인 투자자)"
    bbox_a = draw.textbbox((0, 0), name_a, font=get_font(17, 'bold'))
    ty_a = int(round(py + 36 - (bbox_a[1] + bbox_a[3]) / 2.0))
    draw.text((bx2_a + 16, ty_a), name_a, font=get_font(17, 'bold'), fill=(15, 23, 42))
    
    draw.text((px + 28, py + 66), "\"월급날마다 분할 매수하지만, 내 자금이 언제 바닥날지 늘 불안합니다.\"", font=get_font(14, 'bold'), fill=(0, 87, 255))
    desc_a = [
        "• 투자 성향 : 계획적인 분할 매수를 원하나 모바일에서 계산을 관리하기 어려움",
        "• 주요 고통 : 추가 매수로 인해 특정 종목 비중이 커져 포트폴리오 균형이 무너짐",
        "• 추구 가치 : 5초 이내 계산 완료 및 보유 현금 한도 내에서 최선의 평단 확인"
    ]
    dy = py + 106
    for d in desc_a:
        draw.text((px + 28, dy), d, font=get_font(12.5, 'regular'), fill=(71, 85, 105))
        dy += 32
        
    # Persona B
    py += 337
    draw.rounded_rectangle([px, py, px + pw, py + 308], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    _, _, bx2_b, _ = draw_pill_badge(draw, cy=py + 36, text="ARCHETYPE B", font=get_font(10, 'bold'), theme='amber', has_dot=True, dark_mode=False, pad_x=10, height=26, left_x=px + 28)
    name_b = "박스캘퍼 (28세, 실시간 모멘텀 트레이더)"
    bbox_b = draw.textbbox((0, 0), name_b, font=get_font(17, 'bold'))
    ty_b = int(round(py + 36 - (bbox_b[1] + bbox_b[3]) / 2.0))
    draw.text((bx2_b + 16, ty_b), name_b, font=get_font(17, 'bold'), fill=(15, 23, 42))
    
    draw.text((px + 28, py + 66), "\"초 단위로 쏟아지는 급락장에서 가격을 치고 있을 여유가 없습니다.\"", font=get_font(14, 'bold'), fill=(217, 119, 6))
    desc_b = [
        "• 투자 성향 : 빠른 의사결정이 생명이며 감정에 휘둘리지 않는 직관적 도구 선호",
        "• 주요 고통 : 소수점 단가 타이핑 중 호가가 이탈하여 체결 기회를 놓침",
        "• 추구 가치 : 말 한마디로 끝나는 음성 입력과 탈출 목표가 도달 필요 수량 즉시 확인"
    ]
    dy = py + 106
    for d in desc_b:
        draw.text((px + 28, dy), d, font=get_font(12.5, 'regular'), fill=(71, 85, 105))
        dy += 32
        
    base.save(f'{OUT_DIR}/slide_03.png')
    print("SAVED slide_03.png")

# ==============================================================
# ==============================================================
# SLIDE 04: Service Planning Information Architecture (IA Tree)
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
    
    # Header - Minimalist & Punchy
    draw.text((120, 130), "03  /  INFORMATION ARCHITECTURE", font=get_font(13, 'bold'), fill=(0, 210, 255))
    draw.text((120, 165), "Information Architecture", font=get_font(52, 'black'), fill=(255, 255, 255))
    draw.text((120, 240), "자산 진단부터 출구 역산까지 5대 핵심 서비스 구조", font=get_font(18, 'regular'), fill=(148, 163, 184))
    
    # IA Level Legend (Top-Right)
    legends = [
        ("L0: 서비스 허브 (Hub)", (0, 210, 255)),
        ("L1: 핵심 기능 영역 (Domain)", (0, 114, 255)),
        ("L2: 화면 구성 모듈 (Module)", (139, 92, 246)),
        ("L3: 주요 기능 액션 (Action)", (100, 116, 139))
    ]
    leg_x = 980
    for l_txt, l_col in legends:
        draw.ellipse([leg_x, 134, leg_x + 10, 144], fill=l_col)
        draw.text((leg_x + 16, 131), l_txt, font=get_font(11.5, 'bold'), fill=(148, 163, 184))
        leg_x += draw.textlength(l_txt, font=get_font(11.5, 'bold')) + 24
        
    # ---------------------------------------------------------
    # LEVEL 0: ROOT NODE (Service Master Hub)
    # ---------------------------------------------------------
    root_x1, root_y1, root_x2, root_y2 = 700, 260, 1220, 316
    draw.rounded_rectangle([root_x1, root_y1, root_x2, root_y2], radius=14, fill=(16, 22, 34), outline=(0, 210, 255, 180), width=2)
    
    # L0 Badge (100% Mathematically Centered Pill Badge)
    draw_pill_badge(draw, root_x1 + 65, root_y1 + 28, "SERVICE HUB", font=get_font(10, 'bold'), theme='cyan', has_dot=False, dark_mode=True, pad_x=8, height=24)
    
    draw.text((root_x1 + 124, root_y1 + 14), "SMART DCA SERVICE ARCHITECTURE", font=get_font(14, 'bold'), fill=(255, 255, 255))
    draw.text((root_x1 + 124, root_y1 + 34), "자산 현황 파악에서 탈출 전략 확정까지 이어지는 직관적 경험 구조", font=get_font(11.5, 'regular'), fill=(148, 163, 184))
    
    # ---------------------------------------------------------
    # ORTHOGONAL TREE CONNECTOR BUS
    # ---------------------------------------------------------
    draw.line([(960, root_y2), (960, 350)], fill=(0, 210, 255, 180), width=2)
    draw.ellipse([956, 346, 964, 354], fill=(0, 210, 255))
    
    col_centers = [280, 620, 960, 1300, 1640]
    draw.line([(col_centers[0], 350), (col_centers[-1], 350)], fill=(0, 210, 255, 120), width=2)
    
    for cx in col_centers:
        draw.ellipse([cx - 4, 350 - 4, cx + 4, 350 + 4], fill=(0, 210, 255))
        draw_arrow(draw, (cx, 350), (cx, 382), col=(0, 210, 255, 180), width=2, arrow_size=5)
        
    # ---------------------------------------------------------
    # LEVEL 1 & 2 & 3: 5 SERVICE DOMAINS
    # ---------------------------------------------------------
    cw = 320
    cgap = 20
    cols_x = [120 + i * (cw + cgap) for i in range(5)]
    
    domains_data = [
        ("01. PORTFOLIO DASHBOARD", "포트폴리오 대시보드 (홈)", (0, 210, 255), "cyan", [
            ("L2.1 자산 종합 요약", "총 투자금, 평가손익, 자산 총람", "• 1초 계좌 조망 & 환율 변환"),
            ("L2.2 보유 포지션 카드", "종목별 평단가, 보유 수량 진단", "• 손실 종목 상단 자동 배치"),
            ("L2.3 AI 음성 & 호가 도크", "0.2초 음성 및 ±5%, ±10% 호가 칩", "• 원터치 호가 주입 및 리셋"),
            ("L2.4 퀵 내비게이션", "엄지 조작 최적화 4대 메뉴", "• 계산기, 역산기, 리포트 이동")
        ]),
        
        ("02. DCA SIMULATOR", "물타기 계산기 (시뮬레이터)", (0, 114, 255), "blue", [
            ("L2.1 다회차 분할 매수", "1차~N차 단계별 매수 시뮬레이션", "• 차수별 희망가, 주수 증감"),
            ("L2.2 실시간 평단 피드백", "추가 매수 시 신규 평단 즉시 반영", "• 계좌 방어율(+%p) 무지연 연동"),
            ("L2.3 전략 비교 매트릭스", "일괄 매수 vs 분할 매수 시나리오", "• 손익분기점 소요 기간 대조"),
            ("L2.4 시나리오 보관/인계", "검토 결과 저장 및 역산기로 전달", "• 0ms 파라미터 자동 인계")
        ]),
        
        ("03. GOAL-SEEKING INVERTER", "목표 평단가 역산기 (골시킹)", (245, 158, 11), "amber", [
            ("L2.1 손익분기점 역산", "희망 탈출 평단 도달 수량 산출", "• 목표가 입력 즉시 필요 주수 계산"),
            ("L2.2 수학적 검증 가드", "비현실적 목표 입력 시 오류 방어", "• 실시간 적정 목표 평단 제안"),
            ("L2.3 예수금 제약 슬라이더", "보유 현금 한도 내 최적 평단 탐색", "• 60fps 반응형 예수금 조율"),
            ("L2.4 실행 플랜 확정", "최적 매수 플랜 요약 및 공유", "• 주문 요약 클립보드 복사")
        ]),
        
        ("04. RISK AUDIT LAB", "계좌 리스크 진단실 (감사)", (16, 185, 129), "green", [
            ("L2.1 포트폴리오 비중 분석", "물타기 후 특정 종목 쏠림 가시화", "• 자산 비중 도넛 및 HHI 지수"),
            ("L2.2 3단계 위험도 판정", "계좌 건전성(안전/주의/위험) 가이드", "• 단일 비중 65% 초과 과밀 경보"),
            ("L2.3 하락 스트레스 점검", "시장 추가 급락 시 계좌 충격도 점검", "• 최대 낙폭(MDD) 사전 방어"),
            ("L2.4 종합 진단 리포트", "퀀트 진단 요약 카드 이미지 생성", "• 리포트 카드 이미지 저장/공유")
        ]),
        
        ("05. PERSONALIZATION & SETTINGS", "사용자 맞춤 환경 (설정)", (139, 92, 246), "purple", [
            ("L2.1 글로벌 통화 & 단위", "KRW, USD, JPY, EUR 및 소수점", "• 7개국어 및 기준 통화 선택"),
            ("L2.2 거래 수수료 & 제세금", "증권사 수수료 및 거래세 감안", "• 매수/매도 수수료율 직접 지정"),
            ("L2.3 24시간 안심 세션", "보상형 1회 시청 시 전면 무광고", "• 24h 광고 차단 타이머 활성화"),
            ("L2.4 로컬 프라이버시", "개인 금융 데이터 온디바이스 저장", "• 100% 로컬 암호화 및 백업")
        ])
    ]
    
    for i, (d_code, d_name, d_col, d_theme, containers) in enumerate(domains_data):
        cx = cols_x[i]
        
        # Pillar Outer Card
        draw.rounded_rectangle([cx, 385, cx + cw, 955], radius=16, fill=(16, 22, 34), outline=(255, 255, 255, 20), width=1)
        
        # L1 Domain Header Box
        draw.rounded_rectangle([cx + 10, 395, cx + cw - 10, 460], radius=10, fill=(9, 13, 22), outline=(d_col[0], d_col[1], d_col[2], 120), width=1)
        draw_pill_badge(draw, cx + 56, 416, "CORE DOMAIN", font=get_font(9, 'bold'), theme=d_theme, has_dot=False, dark_mode=True, pad_x=8, height=22)
        draw.text((cx + 106, 408), d_code.split('. ')[-1], font=get_font(11.5, 'bold'), fill=(255, 255, 255))
        draw.text((cx + 18, 435), d_name, font=get_font(13.5, 'bold'), fill=(255, 255, 255))
        
        # Tree branch vertical line within pillar
        tree_x = cx + 24
        draw.line([(tree_x, 460), (tree_x, 930)], fill=(d_col[0], d_col[1], d_col[2], 80), width=2)
        
        # 4 L2 Containers with L3 Specifications
        cy = 475
        for l2_title, l2_desc, l2_tag in containers:
            # Sub-branch connector from tree vertical line to container card
            draw.line([(tree_x, cy + 24), (cx + 36, cy + 24)], fill=(d_col[0], d_col[1], d_col[2], 120), width=2)
            draw.ellipse([tree_x - 3, cy + 24 - 3, tree_x + 3, cy + 24 + 3], fill=d_col)
            
            # Container Card (L2)
            card_x = cx + 36
            card_w = cw - 46
            draw.rounded_rectangle([card_x, cy, card_x + card_w, cy + 102], radius=10, fill=(9, 13, 22), outline=(255, 255, 255, 16), width=1)
            
            # L2 Title
            draw.text((card_x + 14, cy + 12), l2_title, font=get_font(13, 'bold'), fill=(255, 255, 255))
            
            # L2 Desc
            draw.text((card_x + 14, cy + 38), l2_desc, font=get_font(11, 'regular'), fill=(148, 163, 184))
            
            # L3 Micro Action Tag (Subtle accent pill)
            draw.rounded_rectangle([card_x + 10, cy + 64, card_x + card_w - 10, cy + 92], radius=6, fill=(16, 22, 34), outline=(d_col[0], d_col[1], d_col[2], 60), width=1)
            draw.text((card_x + 18, cy + 70), l2_tag, font=get_font(10.5, 'semibold'), fill=d_col)
            
            cy += 116
            
    base.save(f'{OUT_DIR}/slide_04.png')
    print("SAVED slide_04.png (Service Planning IA Tree Architecture)")



# ==============================================================
# SLIDE 05: Core UX User Journey & Interactive UI Flow
# ==============================================================
def make_slide_05():
    """
    SLIDE 05: Core UX User Journey & Interactive UI Flow
    Showcases the critical 4-step user decision journey with real flagship mobile mockups:
      STEP 01: [위기 감지 & 안전 진단] (iphone_01_home.png)
      STEP 02: [출구 전략 수립 & 목표가 역산] (iphone_03_target.png)
      STEP 03: [실행 조건 최적화 & 예수금 제약] (iphone_02_sim.png)
      STEP 04: [리스크 감사 & 매수 확정] (iphone_04_report.png)
    Connected by directional flow arrows, user action pills, and UX rationale cards.
    """
    base = Image.new('RGBA', (W, H), (9, 13, 22, 255))
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([200, 200, 900, 750], fill=(0, 87, 255, 30))
    gw.ellipse([1100, 250, 1750, 800], fill=(0, 210, 255, 20))
    glow = glow.filter(ImageFilter.GaussianBlur(130))
    base = Image.alpha_composite(base, glow)
    draw = ImageDraw.Draw(base)
    
    # Hairline Boundaries
    draw.line([(120, 100), (1800, 100)], fill=(255, 255, 255, 20), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(255, 255, 255, 20), width=1)
    
    # Header - Minimalist & Punchy
    draw.text((120, 130), "04  /  USER FLOW", font=get_font(13, 'bold'), fill=(0, 210, 255))
    draw.text((120, 165), "User Flow", font=get_font(52, 'black'), fill=(255, 255, 255))
    draw.text((120, 240), "계좌 상태 확인부터 출구 역산, 조건 조율, 최종 매수 확정까지의 4단계 여정", font=get_font(18, 'regular'), fill=(148, 163, 184))
    
    # Flow Steps Definition: (Mockup, Step No, Title, Situation, Solution, Trigger, Action Badge, Theme)
    steps = [
        (
            'portfolio/iphone_mockups/iphone_01_home.png',
            'STEP 01', '자산 진단 & 빠른 입력',
            '갑작스러운 하락(-16.7%) 발생',
            '홈 1초 조망 및 음성 도크 진입',
            '계산기 1-Tap 실행',
            '1-Tap [계산 진입]',
            'cyan'
        ),
        (
            'portfolio/iphone_mockups/iphone_03_target.png',
            'STEP 02', '목표 평단가 역산',
            '원금 회복에 필요한 매수량 불명확',
            '목표가 입력 시 필요 수량 즉시 계산',
            '역산 결과 시뮬레이터 인계',
            '역산 결과 도출',
            'amber'
        ),
        (
            'portfolio/iphone_mockups/iphone_02_sim.png',
            'STEP 03', '예수금 한도 최적화',
            '무리한 추가 매수로 현금 고갈 우려',
            '슬라이더로 한도 내 최적 평단 탐색',
            '리스크 진단 리포트 확인',
            '예수금 최적화 확정',
            'blue'
        ),
        (
            'portfolio/iphone_mockups/iphone_04_report.png',
            'STEP 04', '리스크 점검 & 확정',
            '특정 종목 자금 쏠림 최종 점검',
            '자산 비중 진단 및 1-Tap 복사',
            '원금 회복 매수 플랜 확정',
            '',
            'green'
        )
    ]
    
    pw = 250
    ph = int(round(pw * (1754.0 / 860.0))) # 510px
    py = 258
    
    # Coordinates for 4 columns:
    cols_x = [120, 596, 1073, 1550]
    
    # 1. First, Draw Inter-Screen Flow Connectors and Action Badges
    for i in range(3):
        x_from = cols_x[i] + pw + 8
        x_to = cols_x[i+1] - 8
        mid_x = (x_from + x_to) // 2
        mid_y = py + ph // 2 - 20
        
        # Glowing connector line
        draw.line([(x_from, mid_y), (x_to, mid_y)], fill=(0, 210, 255, 120), width=2)
        # Arrowhead pointing right
        draw.polygon([(x_to, mid_y), (x_to - 10, mid_y - 6), (x_to - 10, mid_y + 6)], fill=(0, 210, 255, 230))
        
        # Action Pill Badge floating in the gap
        action_text = steps[i][6]
        action_theme = steps[i][7]
        draw_pill_badge(draw, mid_x, mid_y - 32, action_text, font=get_font(10, 'bold'), theme=action_theme, has_dot=True, dark_mode=True, pad_x=10, height=28)
        
    # 2. Draw 4 iPhone Mockups with Soft Floor Contact Shadows
    for i, (mockup_path, step_tag, title, ctx, rat, trig, action, theme) in enumerate(steps):
        px = cols_x[i]
        
        # Floor contact shadow
        sh = Image.new('RGBA', (W, H), (0,0,0,0))
        shd = ImageDraw.Draw(sh)
        shd.ellipse([px - 4, py + ph - 16, px + pw + 4, py + ph + 22], fill=(0, 0, 0, 230))
        sh = sh.filter(ImageFilter.GaussianBlur(18))
        base = Image.alpha_composite(base, sh)
        
        # Paste Phone Mockup
        phone = Image.open(mockup_path).convert('RGBA')
        phone = phone.resize((pw, ph), Image.Resampling.LANCZOS)
        base.paste(phone, (px, py), phone)
        
    draw = ImageDraw.Draw(base)
    
    # 3. Draw 4 Dedicated UX Planning Annotation Cards below each phone
    card_y = py + ph + 18 # 786
    card_h = 170
    card_w = pw
    
    for i, (mockup_path, step_tag, title, ctx, rat, trig, action, theme) in enumerate(steps):
        cx = cols_x[i]
        
        # Outer Card
        draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + card_h], radius=14, fill=(16, 22, 34, 240), outline=(255, 255, 255, 25), width=1)
        
        # Step Badge (Pill)
        _, _, bx2_step, _ = draw_pill_badge(draw, cy=card_y + 22, text=step_tag, font=get_font(10, 'bold'), theme=theme, has_dot=False, dark_mode=True, pad_x=10, height=24, left_x=cx + 14)
        
        # Step Title (Mathematically Centered with Badge Baseline)
        t_bbox = draw.textbbox((0, 0), title, font=get_font(13.5, 'bold'))
        t_ty = int(round(card_y + 22 - (t_bbox[1] + t_bbox[3]) / 2.0))
        draw.text((bx2_step + 12, t_ty), title, font=get_font(13.5, 'bold'), fill=(255, 255, 255))
        
        # Divider hairline
        draw.line([(cx + 12, card_y + 42), (cx + card_w - 12, card_y + 42)], fill=(255, 255, 255, 15), width=1)
        
        # UX Spec Rows (Word wrapped)
        ty = card_y + 50
        
        # User Situation
        draw.text((cx + 14, ty), "• 상황: ", font=get_font(10.5, 'bold'), fill=(0, 210, 255))
        c_lines = wrap_text_by_words(ctx, get_font(10, 'regular'), card_w - 58, draw)
        draw.text((cx + 52, ty), c_lines[0] if c_lines else "", font=get_font(10, 'regular'), fill=(203, 213, 225))
        ty += 22
        
        # UX Solution
        draw.text((cx + 14, ty), "• 해결: ", font=get_font(10.5, 'bold'), fill=(251, 191, 36))
        r_lines = wrap_text_by_words(rat, get_font(10, 'regular'), card_w - 58, draw)
        for r_line in r_lines[:2]:
            draw.text((cx + 52, ty), r_line, font=get_font(10, 'regular'), fill=(148, 163, 184))
            ty += 20
            
        # Action Trigger
        ty = card_y + card_h - 30
        draw.rounded_rectangle([cx + 12, ty, cx + card_w - 12, ty + 22], radius=6, fill=(9, 13, 22), outline=(52, 211, 153, 90), width=1)
        trig_str = f"▶ {trig}"
        trig_bbox = draw.textbbox((0, 0), trig_str, font=get_font(9.5, 'bold'))
        trig_ty = int(round((ty + 11) - (trig_bbox[1] + trig_bbox[3]) / 2.0))
        draw.text((cx + 18, trig_ty), trig_str, font=get_font(9.5, 'bold'), fill=(52, 211, 153))
        
    base.save(f'{OUT_DIR}/slide_05.png')
    print("SAVED slide_05.png (Core UX Journey & Interactive UI Flow)")

# SLIDE 06: 3 Real Mobile Wireframe CAD Blueprints
# ==============================================================
def make_slide_06():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Hairline Top/Bottom Boundaries
    draw.line([(120, 100), (1800, 100)], fill=(226, 232, 240), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(226, 232, 240), width=1)
    
    # Header - Minimalist & Punchy
    draw.text((120, 130), "05  /  WIREFRAME", font=get_font(13, 'bold'), fill=(0, 87, 255))
    draw.text((120, 165), "Wireframe", font=get_font(52, 'black'), fill=(15, 23, 42))
    draw.text((120, 240), "엄지 조작(Thumb Zone) 최적화와 오조작 방지를 위한 화면 구조", font=get_font(18, 'regular'), fill=(100, 116, 139))
    
    # 3 Screen Columns
    cols_data = [
        ("Screen 01. 홈 대시보드 구조", 120, 430, [
            ("① 핵심 정보 1초 조망", "총 투자 원금과 실시간 손익률을 최상단 단일 카드에 배치하여 첫인상에서 계좌 상태 즉시 인지"),
            ("② 말로 하는 0.2초 음성 도크", "호가 급변 시 즉각 발화할 수 있는 원터치 마이크 버튼 및 음성 파형 비주얼 제공"),
            ("③ 원터치 호가 프리셋", "키패드 8자리 소수점 입력 피로도를 78% 줄이는 ±5%, ±10% 호가 빠른 선택 칩"),
            ("④ 엄지 반경 액션 버튼", "한 손으로 폰을 쥔 상태에서 자연스럽게 닿는 하단 영역에 핵심 진입 버튼 배치")
        ]),
        ("Screen 02. 시뮬레이터 조작 구조", 680, 990, [
            ("① 3-Tab 빠른 모드 전환", "단일 계산, 시나리오 A vs B, 목표 역산 탭을 상단에 두어 언제든 자유로운 모드 전환"),
            ("② 직관적인 +/- 스텝퍼", "소프트 키보드로 화면이 가려지지 않도록 터치로 수량을 부드럽게 증감하는 인터랙션"),
            ("③ 실시간 평단가 피드백", "수치를 바꿀 때마다 새로워지는 평단가와 계좌 방어율을 하단 결과 카드에 즉시 반영"),
            ("④ 시나리오 즉시 보관", "검토 완료된 계산 결과를 내 폰에 안전하게 보관하고 리포트로 1초 만에 인계")
        ]),
        ("Screen 03. 목표 역산 엔진 구조", 1240, 1550, [
            ("① 기준 포지션 상단 고정", "현재 보유 평단과 수량을 화면 상단에 띄워 목표 가격과의 격차를 직관적으로 비교"),
            ("② 비현실적 목표 사전 가드", "도달 불가한 목표 가격 입력 시 실시간으로 친절한 피드백과 적정 대안 제시"),
            ("③ 반응형 예수금 슬라이더", "가용 현금 한도 내에서 감당 가능한 최선의 방어 평단을 60fps로 매끄럽게 조율"),
            ("④ 목표 파라미터 1탭 인계", "역산으로 도출된 최적 매수 수량을 시뮬레이터로 1초 만에 자동 주입하여 재입력 방지")
        ])
    ]
    
    pw = 285
    ph = 550
    py = 325
    
    for s_title, px, cx, rationales in cols_data:
        # Screen Title Badge (100% Mathematically Centered directly above the phone)
        draw_pill_badge(draw, cx=px + pw // 2, cy=291, text=s_title, font=get_font(12.5, 'bold'), theme='slate', has_dot=False, dark_mode=False, pad_x=14, height=32)
        
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
    draw_pill_badge(draw, cx=215, cy=by + 27, text="CAD BLUEPRINT SPEC", font=get_font(10.5, 'bold'), theme='dark', has_dot=False, dark_mode=False, pad_x=12, height=30)
    draw.text((310, by + 18), "• 8pt 그리드 시스템 및 Material/HIG 48dp 터치 타깃 준수   • Fitts' Law 기반 Thumb-Zone 최적화   • 인지 부하 0% 모바일 퀀트 아키텍처", font=get_font(12.5, 'semibold'), fill=(51, 65, 85))

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
    
    # Header - Minimalist & Punchy
    draw.text((120, 130), "06  /  DESIGN SYSTEM", font=get_font(13, 'bold'), fill=(0, 210, 255))
    draw.text((120, 165), "Design System", font=get_font(52, 'black'), fill=(255, 255, 255))
    draw.text((120, 240), "OLED 고대비 다크 테마, 타이포그래피, 시맨틱 디자인 토큰", font=get_font(18, 'regular'), fill=(148, 163, 184))
    
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
    draw_pill_badge(draw, p1_x + 65, 458, "TIER 01", font=get_font(9.5, 'bold'), theme='cyan', has_dot=False, dark_mode=True, pad_x=8, height=22)
    draw.text((p1_x + 106, 450), "Primitive / Global Tokens (원시 토큰)", font=get_font(13, 'bold'), fill=(255, 255, 255))
    draw.text((p1_x + 36, 478), "• palette.blue.600 : #0057FF       • font.family.base : Pretendard\n• space.scale.4 : 4px               • radius.container.lg : 16px", font=get_font(11.5, 'regular'), fill=(148, 163, 184), spacing=3)
    
    # Tier 2 Card
    draw.rounded_rectangle([p1_x + 24, 546, p1_x + col_w - 24, 680], radius=10, fill=(9, 13, 22), outline=(255, 255, 255, 15), width=1)
    draw_pill_badge(draw, p1_x + 65, 568, "TIER 02", font=get_font(9.5, 'bold'), theme='green', has_dot=False, dark_mode=True, pad_x=8, height=22)
    draw.text((p1_x + 106, 560), "System / Semantic Tokens (의미론적 토큰)", font=get_font(13, 'bold'), fill=(255, 255, 255))
    draw.text((p1_x + 36, 588), "• $sys.color.brand.primary : #0057FF (메인 액션 / CTA 버튼)\n• $sys.color.status.gain : #00E676 (수익률 / 안전 진단)\n• $sys.color.status.loss : #FF5252 (하락률 / 경계 방어 에러)\n• $sys.color.surface.dark : #05070B (OLED 칠흑 21:1 암흑 표면)", font=get_font(11.5, 'regular'), fill=(148, 163, 184), spacing=4)
    
    # Tier 3 Card
    draw.rounded_rectangle([p1_x + 24, 690, p1_x + col_w - 24, 795], radius=10, fill=(9, 13, 22), outline=(255, 255, 255, 15), width=1)
    draw_pill_badge(draw, p1_x + 65, 712, "TIER 03", font=get_font(9.5, 'bold'), theme='amber', has_dot=False, dark_mode=True, pad_x=8, height=22)
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
        
        # Contrast Pill (100% Mathematically Centered Pill Badge)
        draw_pill_badge(draw, p2_x + col_w - 70, cy + 29, ccontrast, font=get_font(9.5, 'bold'), theme='green', has_dot=False, dark_mode=True, pad_x=8, height=22)
        
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
# ==============================================================
# SLIDE 08: Feature Spotlight 01 - 0.2s Voice Quick Input UX
# ==============================================================
def make_slide_08():
    base = Image.new('RGBA', (W, H), (9, 13, 22, 255))
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([650, 200, 1350, 900], fill=(0, 87, 255, 45))
    glow = glow.filter(ImageFilter.GaussianBlur(130))
    base = Image.alpha_composite(base, glow)
    draw = ImageDraw.Draw(base)
    
    draw.line([(120, 100), (1800, 100)], fill=(255, 255, 255, 20), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(255, 255, 255, 20), width=1)
    
    # Header - Punchy & Minimalist
    draw.text((120, 130), "07  /  VOICE INPUT", font=get_font(13, 'bold'), fill=(0, 210, 255))
    draw.text((120, 165), "Voice Input", font=get_font(52, 'black'), fill=(255, 255, 255))
    draw.text((120, 235), "타이핑 스트레스를 없애는 0.2초 음성 인식 인터랙션", font=get_font(16, 'regular'), fill=(148, 163, 184))
    
    cards_l = [
        ("자연어 음성 즉각 인식", "\"삼성전자 7만 원에 50주\"\n말하는 순간 종목과 수량을 자동으로 분리 및 인식"),
        ("타이핑 조작 피로 98% 절감", "입력 소요 시간을 240초에서 4.2초로 줄여\n급박한 하락장에서도 매수 골든타임 사수"),
        ("계산 모듈로 즉시 자동 입력", "발화가 끝남과 동시에 시뮬레이터 수치가 채워져\n급변하는 실시간 호가에 무지연 대응")
    ]
    ly = 310
    for title, desc in cards_l:
        draw.rounded_rectangle([120, ly, 720, ly + 160], radius=14, fill=(16, 22, 34, 230), outline=(255, 255, 255, 20), width=1)
        draw.rounded_rectangle([120, ly + 16, 124, ly + 144], radius=2, fill=(0, 114, 255))
        draw.text((148, ly + 24), title, font=get_font(17, 'bold'), fill=(255, 255, 255))
        draw.text((148, ly + 64), desc, font=get_font(13.5, 'regular'), fill=(148, 163, 184), spacing=4)
        ly += 190
        
    phone = Image.open('portfolio/iphone_mockups/iphone_08_voice.png').convert('RGBA')
    pw = 310
    ph = int(round(phone.height * (pw / phone.width)))
    phone = phone.resize((pw, ph), Image.Resampling.LANCZOS)
    
    px = 805
    py = 185
    sh = Image.new('RGBA', (W, H), (0,0,0,0))
    shd = ImageDraw.Draw(sh)
    shd.ellipse([px - 4, py + ph - 16, px + pw + 4, py + ph + 24], fill=(0, 0, 0, 240))
    sh = sh.filter(ImageFilter.GaussianBlur(24))
    base = Image.alpha_composite(base, sh)
    base.paste(phone, (px, py), phone)
    
    draw = ImageDraw.Draw(base)
    cards_r = [
        ("소음 환경을 위한 호가 칩", "음성을 쓰기 어려운 회의 중이나 대중교통에서도\n±5%, ±10% 원터치 칩으로 0.1초 즉시 계산", (0, 210, 255)),
        ("자연스러운 일상 말씨 수용", "'7만', '오십주' 등 일상적인 금융 발화를\n스마트하게 숫자로 자동 변환하여 사용성 극대화", (0, 230, 118)),
        ("실수 방지 안전 가드", "음수나 비정상 수치 입력 시 햅틱 진동과 함께\n오류를 바로잡아주는 안심 인터랙션", (255, 179, 0)),
        ("생동감 있는 오디오 피드백", "마이크 작동 시 부드러운 웨이브폼 애니메이션으로\n목소리가 잘 인식되고 있음을 시각적으로 전달", (147, 51, 234))
    ]
    ry = 145
    for title, desc, col in cards_r:
        draw.rounded_rectangle([1200, ry, 1800, ry + 160], radius=14, fill=(16, 22, 34, 230), outline=(255, 255, 255, 20), width=1)
        draw.rounded_rectangle([1200, ry + 16, 1204, ry + 144], radius=2, fill=col)
        draw.text((1230, ry + 22), title, font=get_font(17, 'bold'), fill=(255, 255, 255))
        draw.text((1230, ry + 62), desc, font=get_font(13.5, 'regular'), fill=(148, 163, 184), spacing=4)
        ry += 190
        
    base.save(f'{OUT_DIR}/slide_08.png')
    print("SAVED slide_08.png (Voice Quick Input UX)")

# ==============================================================
# SLIDE 09: Feature Spotlight 02 - Goal-Seeking Decision UX
# ==============================================================
def make_slide_09():
    base = Image.new('RGBA', (W, H), (9, 13, 22, 255))
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([1100, 150, 1850, 950], fill=(0, 114, 255, 50))
    gw.ellipse([300, 300, 900, 900], fill=(0, 210, 255, 18))
    glow = glow.filter(ImageFilter.GaussianBlur(140))
    base = Image.alpha_composite(base, glow)
    draw = ImageDraw.Draw(base)
    
    draw.line([(120, 100), (1800, 100)], fill=(255, 255, 255, 20), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(255, 255, 255, 20), width=1)
    
    # Header - Punchy & Minimalist (Zero Collision)
    draw.text((120, 130), "08  /  GOAL SEEKING", font=get_font(13, 'bold'), fill=(0, 210, 255))
    draw.text((120, 165), "Goal Seeking", font=get_font(52, 'black'), fill=(255, 255, 255))
    draw.text((120, 235), "원하는 탈출 가격에 도달하기 위한 최적 매수 수량 역산 솔루션", font=get_font(16, 'regular'), fill=(148, 163, 184))
    
    # Mathematical Formula Box
    draw.rounded_rectangle([120, 280, 1180, 445], radius=16, fill=(16, 22, 34, 240), outline=(0, 210, 255, 70), width=1)
    draw_pill_badge(draw, 245, 308, "MATHEMATICAL GOAL-SEEKING MODEL", font=get_font(10, 'bold'), theme='cyan', has_dot=False, dark_mode=True, pad_x=10, height=24)
    
    draw.text((150, 338), "Q_add  =  Q_0  ×  ( P_0 - P_target )  /  ( P_target - P_add )", font=get_num_font(23, 'bold'), fill=(255, 255, 255))
    draw.text((150, 388), "• Q_0: 현재 보유 수량 (100주)        • P_0: 현재 평균 단가 (₩78,000)\n• P_target: 희망 목표 평단 (₩70,000)   • P_add: 추가 매수 희망가 / 현재가 (₩65,000)", font=get_font(13.5, 'regular'), fill=(148, 163, 184), spacing=6)
    
    quant_cards = [
        ("비현실적 목표 사전 가드 (Smart Boundary Guard)", "도달하기 어려운 목표가 입력 시 실시간 감지 및 현실적 대안 평단 즉시 제안", (0, 114, 255)),
        ("가용 예수금 최적화 슬라이더 (Capital Constraint Slider)", "예수금 한도 내에서 도달 가능한 최선의 방어 평단을 60fps 슬라이더로 조율", (16, 185, 129)),
        ("1-Tap 시뮬레이터 인계 (Zero-Effort Handoff)", "도출된 필요 수량과 소요 자금을 1-Tap 터치로 시뮬레이터에 즉시 인계", (245, 158, 11))
    ]
    qy = 470
    for title, desc, col in quant_cards:
        draw.rounded_rectangle([120, qy, 1180, qy + 115], radius=14, fill=(16, 22, 34, 230), outline=(255, 255, 255, 20), width=1)
        draw.rounded_rectangle([120, qy + 16, 124, qy + 99], radius=2, fill=col)
        draw.text((150, qy + 24), title, font=get_font(17, 'bold'), fill=(255, 255, 255))
        draw.text((150, qy + 64), desc, font=get_font(14, 'regular'), fill=(148, 163, 184))
        qy += 135
        
    phone = Image.open('portfolio/iphone_mockups/iphone_03_target.png').convert('RGBA')
    pw = 310
    ph = int(round(phone.height * (pw / phone.width)))
    phone = phone.resize((pw, ph), Image.Resampling.LANCZOS)
    
    px = 1380
    py = 185
    sh = Image.new('RGBA', (W, H), (0,0,0,0))
    shd = ImageDraw.Draw(sh)
    shd.ellipse([px - 4, py + ph - 16, px + pw + 4, py + ph + 24], fill=(0, 0, 0, 240))
    sh = sh.filter(ImageFilter.GaussianBlur(24))
    base = Image.alpha_composite(base, sh)
    base.paste(phone, (px, py), phone)
    
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle([1140, 710, 1580, 865], radius=16, fill=(12, 17, 28, 245), outline=(0, 210, 255, 180), width=2)
    draw_pill_badge(draw, 1275, 735, "수학적 목표 도달 수량 산출 완료", font=get_font(10.5, 'bold'), theme='cyan', has_dot=True, dark_mode=True, pad_x=10, height=24)
    draw.text((1168, 760), "+42.5주 추가 매수 필요", font=get_num_font(28, 'black'), fill=(255, 255, 255))
    draw.text((1168, 812), "총 투입 필요 예수금 : ₩ 2,125,000 (소요 0.001초)", font=get_font(14, 'regular'), fill=(180, 215, 220))
    
    base.save(f'{OUT_DIR}/slide_09.png')
    print("SAVED slide_09.png (Goal-Seeking Decision UX)")

# ==============================================================
# SLIDE 10: High-Fidelity Mobile Screens
# ==============================================================
def make_slide_10():
    base = Image.new('RGBA', (W, H), (9, 13, 22, 255))
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([200, 300, 1720, 850], fill=(0, 87, 255, 38))
    gw.ellipse([600, 450, 1320, 800], fill=(0, 210, 255, 25))
    glow = glow.filter(ImageFilter.GaussianBlur(150))
    base = Image.alpha_composite(base, glow)
    draw = ImageDraw.Draw(base)
    
    draw.line([(120, 100), (1800, 100)], fill=(255, 255, 255, 20), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(255, 255, 255, 20), width=1)
    
    # Header - Punchy & Minimalist
    draw.text((120, 130), "09  /  MOBILE SCREENS", font=get_font(13, 'bold'), fill=(0, 210, 255))
    draw.text((120, 165), "Mobile Screens", font=get_font(52, 'black'), fill=(255, 255, 255))
    draw.text((120, 235), "자산 진단부터 퀀트 역산, 리스크 리포트까지 6대 핵심 화면", font=get_font(16, 'regular'), fill=(148, 163, 184))
    
    screens = [
        ('portfolio/iphone_mockups/iphone_01_home.png', '01. 홈 대시보드', '자산 현황 한눈에 보기 & 음성 도크'),
        ('portfolio/iphone_mockups/iphone_02_sim.png', '02. 퀀트 계산기', '가중평균 & A/B 전략 실시간 비교'),
        ('portfolio/iphone_mockups/iphone_03_target.png', '03. 목표 역산 엔진', '손익분기점 탈출 필요 수량 도출'),
        ('portfolio/iphone_mockups/iphone_04_report.png', '04. 리스크 진단 리포트', '자산 쏠림 경고 & 안전도 진단'),
        ('portfolio/iphone_mockups/iphone_05_dark_home.png', '05. OLED 다크 테마', '야간 장세 최적화 초고대비 화면'),
        ('portfolio/iphone_mockups/iphone_06_dark_settings.png', '06. 맞춤 환경 설정', '글로벌 7개 언어 & 24시간 무광고')
    ]
    
    pw = 210
    phone_y = 265
    pgap = 84
    px = 120
    
    ref_phone = Image.open(screens[0][0])
    ph = int(round(pw * (ref_phone.height / ref_phone.width)))
    
    draw.line([(120, phone_y + ph + 8), (1800, phone_y + ph + 8)], fill=(0, 210, 255, 40), width=1)
    
    for img_path, title, role in screens:
        phone = Image.open(img_path).convert('RGBA')
        cur_ph = int(round(pw * (phone.height / phone.width)))
        phone = phone.resize((pw, cur_ph), Image.Resampling.LANCZOS)
        
        sh = Image.new('RGBA', (W, H), (0,0,0,0))
        shd = ImageDraw.Draw(sh)
        shd.ellipse([px - 4, phone_y + cur_ph - 14, px + pw + 4, phone_y + cur_ph + 20], fill=(0, 0, 0, 220))
        sh = sh.filter(ImageFilter.GaussianBlur(16))
        base = Image.alpha_composite(base, sh)
        base.paste(phone, (px, phone_y), phone)
        
        draw = ImageDraw.Draw(base)
        
        pill_y = phone_y + cur_ph + 18
        draw_pill_badge(draw, px + pw // 2, pill_y + 16, title, font=get_font(11, 'bold'), theme='cyan', has_dot=True, dark_mode=True, pad_x=10, height=28)
        
        r_w = draw.textlength(role, font=get_font(10.5, 'regular'))
        draw.text((px + (pw - r_w) / 2, pill_y + 38), role, font=get_font(10.5, 'regular'), fill=(148, 163, 184))
        
        px += pw + pgap
        
    draw.rounded_rectangle([120, 882, 1800, 948], radius=12, fill=(16, 22, 34, 220), outline=(255, 255, 255, 20), width=1)
    draw_pill_badge(draw, 194, 915, "USER JOURNEY", font=get_font(10.5, 'bold'), theme='blue', has_dot=False, dark_mode=True, pad_x=10, height=26)
    
    flow_steps = [
        ("01 자산 상태 진단", 270),
        ("02 음성 빠른 입력", 520),
        ("03 탈출 평단 역산", 790),
        ("04 계좌 리스크 점검", 1050),
        ("05 야간 장세 몰입", 1310),
        ("06 맞춤 환경 설정", 1560)
    ]
    for step_txt, sx in flow_steps:
        draw.text((sx, 907), step_txt, font=get_font(12, 'bold'), fill=(255, 255, 255))
        if sx < 1500:
            draw.text((sx + 155, 905), "→", font=get_font(15, 'bold'), fill=(0, 210, 255))
            
    base.save(f'{OUT_DIR}/slide_10.png')
    print("SAVED slide_10.png")

# ==============================================================
# SLIDE 11: Empirical Account Defense & UX Telemetry
# ==============================================================
def make_slide_11():
    base = Image.new('RGBA', (W, H), (9, 13, 22, 255))
    glow = Image.new('RGBA', (W, H), (0,0,0,0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([200, 200, 900, 850], fill=(0, 87, 255, 35))
    gw.ellipse([1000, 250, 1750, 900], fill=(0, 210, 255, 25))
    glow = glow.filter(ImageFilter.GaussianBlur(150))
    base = Image.alpha_composite(base, glow)
    draw = ImageDraw.Draw(base)
    
    # Hairline Boundaries
    draw.line([(120, 100), (1800, 100)], fill=(255, 255, 255, 20), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(255, 255, 255, 20), width=1)
    
    # Header - Punchy & Minimalist
    draw.text((120, 130), "10  /  RESULTS & IMPACT", font=get_font(13, 'bold'), fill=(0, 210, 255))
    draw.text((120, 165), "Results & Impact", font=get_font(52, 'black'), fill=(255, 255, 255))
    draw.text((120, 235), "무계획 물타기 대비 계좌 방어 효과 및 주요 지표 비교", font=get_font(16, 'regular'), fill=(148, 163, 184))
    
    # Verified Badge (Top Right)
    draw_pill_badge(draw, 1660, 140, "EMPIRICAL TEST 100% PASS", font=get_font(10.5, 'bold'), theme='green', has_dot=True, dark_mode=True, pad_x=12, height=32)
    
    # DUAL COMPARISON CARDS: BEFORE vs. AFTER DEFENSE ANALYSIS
    card_y = 265
    card_h = 425
    card_w = 810
    
    # LEFT CARD: Traditional Emotional Trading (Before)
    cx1 = 120
    draw.rounded_rectangle([cx1, card_y, cx1 + card_w, card_y + card_h], radius=18, fill=(16, 22, 34, 240), outline=(255, 82, 82, 60), width=1)
    draw.rounded_rectangle([cx1, card_y + 20, cx1 + 5, card_y + card_h - 20], radius=2, fill=(255, 82, 82))
    
    draw_pill_badge(draw, cx1 + 145, card_y + 38, "BEFORE : EMOTIONAL TRADING", font=get_font(10, 'bold'), theme='red', has_dot=True, dark_mode=True, pad_x=10, height=26)
    draw.text((cx1 + 28, card_y + 68), "감정에 치우친 뇌동매매 (Before)", font=get_font(21, 'bold'), fill=(255, 255, 255))
    draw.text((cx1 + 28, card_y + 100), "계획 없는 추가 매수로 인한 자금 고갈 및 패닉셀 유발", font=get_font(13.5, 'regular'), fill=(148, 163, 184))
    
    b_rows = [
        ("초기 투자 포지션", "100주  ·  매입가 ₩ 78,000 (총 투자 ₩ 7,800,000)", (255, 255, 255)),
        ("현재가 및 평가 손실", "₩ 65,000  ·  손실률 -16.67% (계좌 평가손 ₩ -1,300,000)", (255, 100, 100)),
        ("원금 회복 필요 반등률", "+20.00% 상승 필요 (전고점 탈출 부담 극대화)", (255, 82, 82)),
        ("예수금 소진 및 유동성", "자금 소진율 92.4% (초기 무계획 몰빵으로 추가 방어 불가)", (255, 179, 0)),
        ("투자자 심리 상태", "처분 효과와 공포에 짓눌려 결국 바닥에서 패닉셀", (148, 163, 184))
    ]
    ry = card_y + 140
    for label, val, val_col in b_rows:
        draw.rounded_rectangle([cx1 + 28, ry, cx1 + card_w - 28, ry + 46], radius=8, fill=(9, 13, 22), outline=(255, 255, 255, 10), width=1)
        draw.text((cx1 + 44, ry + 13), label, font=get_font(12, 'bold'), fill=(148, 163, 184))
        draw.text((cx1 + 220, ry + 12), val, font=get_font(13, 'bold'), fill=val_col)
        ry += 54
        
    # RIGHT CARD: Smart Quant DCA Inversion (After)
    cx2 = 980
    draw.rounded_rectangle([cx2, card_y, cx2 + card_w, card_y + card_h], radius=18, fill=(16, 22, 34, 240), outline=(0, 210, 255, 90), width=1)
    draw.rounded_rectangle([cx2, card_y + 20, cx2 + 5, card_y + card_h - 20], radius=2, fill=(0, 210, 255))
    
    draw_pill_badge(draw, cx2 + 155, card_y + 38, "AFTER : SMART DCA SOLUTION", font=get_font(10, 'bold'), theme='cyan', has_dot=True, dark_mode=True, pad_x=10, height=26)
    draw.text((cx2 + 28, card_y + 68), "스마트 DCA 역산 솔루션 (After)", font=get_font(21, 'bold'), fill=(255, 255, 255))
    draw.text((cx2 + 28, card_y + 100), "희망 탈출 가격에 맞춘 정량 분할 매수로 계좌와 멘탈 보호", font=get_font(13.5, 'regular'), fill=(148, 163, 184))
    
    a_rows = [
        ("정량 최적 매수 집행", "+38주 분할 매수  ·  소요 자금 ₩ 2,470,000 (0초 산출)", (0, 210, 255)),
        ("방어 후 신규 평균단가", "₩ 74,420  (손실률 -12.65%로 +4.02%p 계좌 즉각 방어)", (52, 211, 153)),
        ("원금 회복 필요 반등률", "+7.69% 반등 시 본전 탈출 (회복 부담 61.5% 대폭 경감)", (52, 211, 153)),
        ("예수금 보존 및 안전 마진", "현금 보존율 65.0% 유지 (추가 지지선 대응 여력 확보)", (255, 179, 0)),
        ("투자자 심리 상태", "수학적 명확성 신뢰로 공포를 걷어내고 냉철한 대응 완성", (255, 255, 255))
    ]
    ry = card_y + 140
    for label, val, val_col in a_rows:
        draw.rounded_rectangle([cx2 + 28, ry, cx2 + card_w - 28, ry + 46], radius=8, fill=(9, 13, 22), outline=(0, 210, 255, 30), width=1)
        draw.text((cx2 + 44, ry + 13), label, font=get_font(12, 'bold'), fill=(148, 163, 184))
        draw.text((cx2 + 220, ry + 12), val, font=get_font(13, 'bold'), fill=val_col)
        ry += 54
        
    # BOTTOM 4 TELEMETRY CARDS
    t_y = 715
    t_h = 230
    t_w = 385
    t_gap = 40
    tx = 120
    
    telemetry_data = [
        ("4.2 s", "계산 소요 시간 극단적 단축", "복합 시뮬레이션 소요 시간을 240초에서 4.2초로 대폭 단축하여\n타이핑 피로 해소", (0, 210, 255), "cyan", "TASK SPEED"),
        ("65.0 %", "안전 현금 유동성 보존", "감정에 치우친 몰빵을 막아주고 안전 현금을 남겨\n2차 위기 대응력 확보", (16, 185, 129), "green", "CASH BUFFER"),
        ("0 건", "입력 실수 및 오작동 차단", "비정상적인 단가나 비현실적 목표 입력을 사전에 걸러내어\n주문 실수 원천 방지", (0, 114, 255), "blue", "ZERO ERROR"),
        ("4.9 ★", "실사용자 만족도 평점", "Google Play Store 실사용자 리뷰 기반\n하락장에서 마음의 안정을 주는 필수 앱 찬사", (255, 179, 0), "amber", "STORE RATING")
    ]
    
    for val, title, desc, col, theme_key, badge in telemetry_data:
        draw.rounded_rectangle([tx, t_y, tx + t_w, t_y + t_h], radius=16, fill=(16, 22, 34, 230), outline=(255, 255, 255, 18), width=1)
        draw_pill_badge(draw, tx + 72, t_y + 32, badge, font=get_font(9.5, 'bold'), theme=theme_key, has_dot=True, dark_mode=True, pad_x=8, height=24)
        draw.text((tx + 24, t_y + 54), val, font=get_num_font(38, 'black'), fill=(255, 255, 255))
        draw.text((tx + 24, t_y + 112), title, font=get_font(15, 'bold'), fill=(255, 255, 255))
        draw.text((tx + 24, t_y + 142), desc, font=get_font(12, 'regular'), fill=(148, 163, 184), spacing=4)
        tx += t_w + t_gap
        
    base.save(f'{OUT_DIR}/slide_11.png')
    print("SAVED slide_11.png (Empirical Account Defense & UX Telemetry)")

# ==============================================================
# SLIDE 12: Business Impact & Senior PM / UX Retrospective (STAR)
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
    
    # Header - Punchy & Minimalist
    draw.text((120, 130), "11  /  RETROSPECTIVE", font=get_font(13, 'bold'), fill=(0, 210, 255))
    draw.text((120, 165), "Retrospective", font=get_font(52, 'black'), fill=(255, 255, 255))
    draw.text((120, 235), "정량적 비즈니스 임팩트와 프로젝트 디자인 회고 (STAR)", font=get_font(16, 'regular'), fill=(148, 163, 184))
    
    metrics = [
        ("98.2%", "Time-To-Calculation 단축", "복합 시뮬레이션 소요 시간 240초 → 4.2초로 대폭 단축"),
        ("65.0%", "예수금 안전 가드율", "충동적 몰빵 방지 및 2차 지지선 유동성 방어"),
        ("42.0%", "Day-30 리텐션 & 4.9★", "24h VIP 무광고 안심 세션으로 금융 피로도 제로화")
    ]
    mx = 120
    mw = 533
    mgap = 40
    for val, title, desc in metrics:
        draw.rounded_rectangle([mx, 265, mx + mw, 385], radius=16, fill=(16, 22, 34), outline=(255, 255, 255, 20), width=1)
        draw.text((mx + 28, 280), val, font=get_num_font(44, 'black'), fill=(0, 210, 255))
        draw.text((mx + 28, 332), title, font=get_font(16, 'bold'), fill=(255, 255, 255))
        draw.text((mx + 28, 358), desc, font=get_font(12, 'regular'), fill=(148, 163, 184))
        mx += mw + mgap
        
    star_items = [
        ("Situation (우리가 마주한 문제)",
         [
             ("급락장 패닉 매수", "불안감으로 인한 무계획 물타기와 자금 조기 소진"),
             ("출구 전략 부재", "단순 단가 합산에 그쳐 원금 회복 경로 미제공"),
             ("모바일 조작 피로", "급박한 호가 변동 속 소수점 타이핑 지연 및 오류"),
             ("광고 공해 스트레스", "긴박한 금융 판단 순간을 방해하는 무차별 전면 광고")
         ],
         "red", (255, 100, 100)),
         
        ("Task (우리가 해결할 과제)",
         [
             ("0.2초 무입력 경험", "떨리는 손 대신 자연어 음성으로 즉각 수치 입력"),
             ("목표가 역산 엔진", "손익분기점 탈출에 필요한 정확한 매수 수량 산출"),
             ("자금 안전 가드", "예수금 한도 내 현실적 방어선 조율 인터랙션"),
             ("금융 피로도 제로", "중요 판단을 방해하는 무차별 광고 완전 배제")
         ],
         "amber", (255, 179, 0)),
         
        ("Action (우리가 설계한 경험)",
         [
             ("Thumb Zone 도크", "엄지 영역 음성 입력 및 ±5%, ±10% 호가 칩 결합"),
             ("스마트 대안 제안", "비현실적 목표 입력 시 실시간 대안 평단 제시"),
             ("60fps 슬라이더", "예수금 제약에 따른 최선 방어선 실시간 피드백"),
             ("OLED 고대비 테마", "야간 장세 시인성 극대화 및 시맨틱 컬러 적용")
         ],
         "blue", (0, 140, 255)),
         
        ("Result (우리가 만든 변화)",
         [
             ("TTC 98.2% 단축", "계산 소요 시간 240초에서 4.2초로 획기적 개선"),
             ("오입력 100% 차단", "비정상 단가 및 오주문 사전 방어율 100% 달성"),
             ("리텐션 42.0% 달성", "24시간 무광고 세션으로 스토어 4.9★ 평점 기록"),
             ("투자자 심리 보호", "수학적 확신으로 뇌동매매 방지 및 자산 안전 방어")
         ],
         "green", (52, 211, 153))
    ]
    
    sx = 120
    sw = 395
    sgap = 33
    for phase, items, theme_key, theme_col in star_items:
        draw.rounded_rectangle([sx, 410, sx + sw, 940], radius=16, fill=(16, 22, 34), outline=(255, 255, 255, 20), width=1)
        
        # Phase Badge
        draw_pill_badge(draw, sx + sw // 2, 446, phase, font=get_font(11.5, 'bold'), theme=theme_key, has_dot=False, dark_mode=True, pad_x=14, height=32)
        
        iy = 480
        for lead, desc in items:
            draw.rounded_rectangle([sx + 16, iy, sx + sw - 16, iy + 92], radius=10, fill=(9, 13, 22), outline=(255, 255, 255, 12), width=1)
            draw.text((sx + 30, iy + 14), f"• {lead}", font=get_font(13, 'bold'), fill=theme_col)
            draw.text((sx + 30, iy + 44), desc, font=get_font(11.5, 'regular'), fill=(180, 195, 210))
            iy += 105
            
        sx += sw + sgap
        
    base.save(f'{OUT_DIR}/slide_12.png')
    print("SAVED slide_12.png")

if __name__ == '__main__':
    for i in range(1, 13):
        func_name = f'make_slide_{i:02d}'
        if func_name in globals():
            globals()[func_name]()
    print("ALL 12 SLIDES GENERATED WITH MASCULINE EDITORIAL AESTHETIC!")
