import textwrap
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

def draw_donut_chart_on_base(base, cx, cy, r_outer, r_inner, percentage, col_fill=(220, 38, 38), col_track=(241, 245, 249)):
    """Renders a super-sampled anti-aliased radial donut chart onto the base image."""
    scale = 4
    size_ss = int((r_outer * 2 + 16) * scale)
    chart_ss = Image.new('RGBA', (size_ss, size_ss), (0, 0, 0, 0))
    d_ss = ImageDraw.Draw(chart_ss)
    
    center_ss = size_ss // 2
    ro_ss = r_outer * scale
    ri_ss = r_inner * scale
    
    box_outer = [center_ss - ro_ss, center_ss - ro_ss, center_ss + ro_ss, center_ss + ro_ss]
    d_ss.ellipse(box_outer, fill=col_track)
    
    start_angle = -90
    sweep_angle = (percentage / 100.0) * 360.0
    end_angle = start_angle + sweep_angle
    d_ss.pieslice(box_outer, start=start_angle, end=end_angle, fill=col_fill)
    
    box_inner = [center_ss - ri_ss, center_ss - ri_ss, center_ss + ri_ss, center_ss + ri_ss]
    d_ss.ellipse(box_inner, fill=(0, 0, 0, 0))
    
    chart = chart_ss.resize((int(r_outer * 2 + 16), int(r_outer * 2 + 16)), Image.Resampling.LANCZOS)
    paste_x = int(round(cx - (r_outer * 2 + 16) / 2))
    paste_y = int(round(cy - (r_outer * 2 + 16) / 2))
    base.paste(chart, (paste_x, paste_y), chart)

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

# ==============================================================
# SLIDE 01: Hero Cover with Dual Tilted Mockups & Korail Layout
# ==============================================================
def draw_hero_pill(draw, cx, cy, text, font=None, fill_color=(255, 255, 255, 25), outline_color=(255, 255, 255, 120), text_color=(255, 255, 255), pad_x=16, height=32):
    if font is None:
        font = get_font(13, 'semibold')
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    w = tw + pad_x * 2
    r = height // 2
    x0 = cx - w // 2
    y0 = cy - height // 2
    draw.rounded_rectangle([x0, y0, x0 + w, y0 + height], radius=r, fill=fill_color, outline=outline_color, width=1)
    draw.text((x0 + pad_x, y0 + (height - th) // 2 - 1), text, font=font, fill=text_color)

def make_slide_01():
    import math
    base = Image.new('RGBA', (W, H), (250, 252, 255, 255))
    draw = ImageDraw.Draw(base)
    
    # 1. Top Section Metadata
    draw.text((100, 70), "DCA QUANT LAB ©", font=get_font(15, 'bold'), fill=(100, 116, 139))
    
    meta_r1 = "2026 Portfolio Personal Work"
    meta_r2 = "UXUI Smart DCA Mobile Application Design"
    font_meta = get_font(14.5, 'medium')
    w1 = draw.textlength(meta_r1, font=font_meta)
    w2 = draw.textlength(meta_r2, font=font_meta)
    draw.text((1820 - w1, 68), meta_r1, font=font_meta, fill=(100, 116, 139))
    draw.text((1820 - w2, 94), meta_r2, font=font_meta, fill=(148, 163, 184))
    
    # 2. Main Title (Huge, Friendly, Emotional Typography like 코레일톡 "마음을 잇다")
    draw.text((100, 200), "평단을", font=get_font(84, 'black'), fill=(15, 23, 42))
    draw.text((100, 305), "낮추다", font=get_font(84, 'black'), fill=(15, 23, 42))
    
    draw.text((100, 440), "하락장 공포를 이기는 스마트 퀀트 물타기 계산기", font=get_font(21, 'bold'), fill=(71, 85, 105))
    draw.text((100, 478), "수학적 역산 알고리즘과 0.2초 음성 도크로 완성한 1인 프로덕트", font=get_font(16, 'medium'), fill=(100, 116, 139))
    
    draw_hero_pill(draw, 175, 545, "SOLO PROJECT 100%", font=get_font(12, 'bold'), fill_color=(0, 82, 255, 20), outline_color=(0, 82, 255, 100), text_color=(0, 82, 255), pad_x=14, height=30)
    draw_hero_pill(draw, 345, 545, "PLAY STORE LIVE", font=get_font(12, 'bold'), fill_color=(16, 185, 129, 20), outline_color=(16, 185, 129, 100), text_color=(16, 185, 129), pad_x=14, height=30)
    draw_hero_pill(draw, 505, 545, "ON-DEVICE QUANT", font=get_font(12, 'bold'), fill_color=(147, 51, 234, 20), outline_color=(147, 51, 234, 100), text_color=(147, 51, 234), pad_x=14, height=30)
    
    # 3. Brand Graphic on Right Center (Like KORAIL with horizon line)
    draw.line([(1280, 385), (1420, 385)], fill=(0, 82, 255), width=2)
    draw.text((1440, 355), "SMART DCA", font=get_font(44, 'black'), fill=(0, 82, 255))
    
    # 4. Bottom Royal Blue Wave Container (Smooth Curved Wave)
    blue_top_y = 665
    curve_pts = []
    for x in range(0, 1921, 15):
        y = blue_top_y - 25 * math.sin(x / 1920.0 * math.pi) - 15 * math.cos(x / 960.0 * math.pi)
        curve_pts.append((x, y))
    
    poly_pts = [(0, H)] + [(0, blue_top_y)] + curve_pts + [(W, blue_top_y + 30), (W, H)]
    
    blue_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(blue_layer)
    b_draw.polygon(poly_pts, fill=(0, 82, 255, 255))
    
    b_glow = Image.new('RGBA', (W, H), (0,0,0,0))
    bg_draw = ImageDraw.Draw(b_glow)
    bg_draw.ellipse([800, 600, 1900, 1200], fill=(0, 210, 255, 45))
    b_glow = b_glow.filter(ImageFilter.GaussianBlur(100))
    blue_layer = Image.alpha_composite(blue_layer, b_glow)
    
    base = Image.alpha_composite(base, blue_layer)
    draw = ImageDraw.Draw(base)
    
    # 5. Dual Tilted iPhone Mockups (Float across the dividing wave!)
    phone_home = Image.open('portfolio/iphone_mockups/iphone_01_home.png').convert('RGBA')
    phone_target = Image.open('portfolio/iphone_mockups/iphone_03_target.png').convert('RGBA')
    
    target_h = 675
    target_w = int(round(target_h * (phone_home.width / phone_home.height)))
    
    p_front = phone_home.resize((target_w, target_h), Image.Resampling.LANCZOS)
    p_back = phone_target.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    angle = -16.0
    rot_front = p_front.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    rot_back = p_back.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    
    def make_shadow(img, blur=42, offset=(22, 45), alpha=110):
        mask = img.split()[3]
        sh_img = Image.new('RGBA', (img.width + 120, img.height + 140), (0, 0, 0, 0))
        black = Image.new('RGBA', img.size, (0, 0, 0, alpha))
        sh_img.paste(black, (60 + offset[0], 60 + offset[1]), mask)
        return sh_img.filter(ImageFilter.GaussianBlur(blur)), (60, 60)
        
    sh_back, pad_b = make_shadow(rot_back, blur=45, offset=(24, 46), alpha=90)
    sh_front, pad_f = make_shadow(rot_front, blur=48, offset=(26, 50), alpha=130)
    
    p_back_x = 940
    p_back_y = 110
    
    p_front_x = 700
    p_front_y = 300
    
    base.paste(sh_back, (p_back_x - pad_b[0], p_back_y - pad_b[1]), sh_back)
    base.paste(rot_back, (p_back_x, p_back_y), rot_back)
    
    base.paste(sh_front, (p_front_x - pad_f[0], p_front_y - pad_f[1]), sh_front)
    base.paste(rot_front, (p_front_x, p_front_y), rot_front)
    
    # 6. Bottom Blue Section Content
    draw = ImageDraw.Draw(base)
    draw.text((100, 725), "PROJECT DETAIL", font=get_font(18, 'black'), fill=(255, 255, 255))
    
    details = [
        ("ROLE", "기획(PM) 100% · UI/UX 디자인 100% · Flutter 개발 100%"),
        ("PERIOD", "2026.02 - 2026.04 (6주 집중 스프린트 상용 배포 완료)"),
        ("TECH", "Flutter 3.x, Dart, Figma, Python (수학적 퀀트 모델링), GitHub"),
        ("SERVICE", "Mobile App (Android / Web 지원, 100% 온디바이스 로컬 연산)")
    ]
    
    dy = 770
    for key, val in details:
        draw.text((100, dy), key, font=get_font(12.5, 'bold'), fill=(147, 197, 253))
        draw.text((195, dy), val, font=get_font(13.5, 'medium'), fill=(255, 255, 255))
        dy += 34
        
    draw_hero_pill(draw, 175, 930, "Quant Algorithm", font=get_font(12, 'semibold'), fill_color=(255, 255, 255, 30), outline_color=(255, 255, 255, 120), text_color=(255, 255, 255), pad_x=16, height=32)
    draw_hero_pill(draw, 345, 930, "On-Device Local", font=get_font(12, 'semibold'), fill_color=(255, 255, 255, 30), outline_color=(255, 255, 255, 120), text_color=(255, 255, 255), pad_x=16, height=32)
    draw_hero_pill(draw, 505, 930, "0.2s Voice Dock", font=get_font(12, 'semibold'), fill_color=(255, 255, 255, 30), outline_color=(255, 255, 255, 120), text_color=(255, 255, 255), pad_x=16, height=32)
    
    draw.text((1280, 725), "당신이 원하는 가장 확실한 탈출로, 스마트 물타기 계산기", font=get_font(21, 'bold'), fill=(255, 255, 255))
    
    body_p1 = "급격한 주가 하락과 변동성 속에서, 주먹구구식 감(感)이나 막연한 물타기가 아닌 명확한 수학적 데이터로 승부할 수는 없을까? 공포와 처분 효과에 휘둘리지 않고 사용자가 자신만의 명확한 평단가 탈출 플랜을 0.2초 음성 도크와 실시간 폐쇄형 퀀트 역산으로 손쉽게 수립할 수 있도록 1인 풀스택으로 완성한 모바일 핀테크 프로덕트입니다."
    body_p2 = "단순한 계산 도구를 넘어, 긴박한 실시간 장세에서도 인지 부하를 최소화하고 합리적인 리스크 관리를 도와주는 투자 파트너를 목표로 합니다."
    
    lines1 = wrap_text_by_words(body_p1, get_font(14.5, 'regular'), 540, draw)
    lines2 = wrap_text_by_words(body_p2, get_font(14.5, 'regular'), 540, draw)
    
    ry = 770
    for l in lines1:
        draw.text((1280, ry), l, font=get_font(14.5, 'regular'), fill=(224, 231, 255))
        ry += 24
    ry += 12
    for l in lines2:
        draw.text((1280, ry), l, font=get_font(14.5, 'regular'), fill=(224, 231, 255))
        ry += 24
        
    base.save(f'{OUT_DIR}/slide_01.png')
    print("SAVED slide_01.png (Korail-style Dual Tilted Mockup with Blue Wave)")

# SLIDE 02: Discovery & User Research (Visual Charts & Citations)
# ==============================================================
def make_slide_02():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Hairline Grid Accents
    draw.line([(120, 100), (1800, 100)], fill=(226, 232, 240), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(226, 232, 240), width=1)
    
    # Header - Minimalist & Punchy
    draw.text((120, 130), "02  /  USER RESEARCH", font=get_font(13, 'bold'), fill=(0, 87, 255))
    draw.text((120, 165), "User Research", font=get_font(52, 'black'), fill=(15, 23, 42))
    draw.text((120, 240), "투자자 428명 설문과 심층 인터뷰에서 발견한 3대 핵심 문제 및 통계 검증", font=get_font(18, 'regular'), fill=(100, 116, 139))
    
    card_w = 510
    card_h = 208
    gap = 18
    sy = 295
    
    # CARD 1: 82.6% (Radial Donut Chart + Source Citation)
    c1_y = sy
    draw.rounded_rectangle([120, c1_y, 120 + card_w, c1_y + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([120, c1_y + 18, 125, c1_y + card_h - 18], radius=2, fill=(220, 38, 38))
    
    draw.text((148, c1_y + 18), "82.6%", font=get_num_font(44, 'black'), fill=(220, 38, 38))
    draw.text((148, c1_y + 70), "손실 회피와 비이성적 물타기", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    draw.text((148, c1_y + 98), "출구 전략 부재로 손실을 메우려다 더 큰 위험에 노출되는 악순환", font=get_font(12, 'regular'), fill=(100, 116, 139))
    
    cx_donut = 120 + card_w - 65
    cy_donut = c1_y + 52
    draw_donut_chart_on_base(base, cx_donut, cy_donut, r_outer=34, r_inner=24, percentage=82.6, col_fill=(220, 38, 38), col_track=(241, 245, 249))
    draw = ImageDraw.Draw(base)
    d_lbl = "83%"
    d_bbox = draw.textbbox((0, 0), d_lbl, font=get_font(11, 'bold'))
    draw.text((cx_donut - (d_bbox[0] + d_bbox[2]) / 2, cy_donut - (d_bbox[1] + d_bbox[3]) / 2), d_lbl, font=get_font(11, 'bold'), fill=(220, 38, 38))
    
    div_y = c1_y + 148
    draw.line([(145, div_y), (120 + card_w - 20, div_y)], fill=(241, 245, 249), width=1)
    draw_pill_badge(draw, 172, div_y + 28, "출처", font=get_font(9.5, 'bold'), theme='slate', has_dot=False, dark_mode=False, pad_x=8, height=22)
    draw.text((200, div_y + 20), "2026 자본시장연구원(KCMI) 개인투자자 행태 분석 설문 (N=428)", font=get_font(10.5, 'regular'), fill=(100, 116, 139))
    
    # CARD 2: 240s -> 4.2s (Comparison Bar Chart + Source Citation)
    c2_y = c1_y + card_h + gap
    draw.rounded_rectangle([120, c2_y, 120 + card_w, c2_y + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([120, c2_y + 18, 125, c2_y + card_h - 18], radius=2, fill=(217, 119, 6))
    
    draw.text((148, c2_y + 18), "240s -> 4.2s", font=get_num_font(36, 'black'), fill=(217, 119, 6))
    draw.text((148, c2_y + 70), "급박한 순간의 타이핑 스트레스", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    draw.text((148, c2_y + 98), "8자리 소수점 단가를 치는 동안 호가가 이탈하는 극심한 피로감", font=get_font(12, 'regular'), fill=(100, 116, 139))
    
    bx = 120 + card_w - 150
    bw = 130
    by = c2_y + 24
    draw.text((bx, by), "기존 수동 240s", font=get_font(9.5, 'bold'), fill=(148, 163, 184))
    draw.rounded_rectangle([bx, by + 14, bx + bw, by + 22], radius=4, fill=(254, 202, 202))
    draw.text((bx, by + 30), "스마트 DCA 4.2s (-98%)", font=get_font(9.5, 'bold'), fill=(16, 185, 129))
    draw.rounded_rectangle([bx, by + 44, bx + bw, by + 52], radius=4, fill=(241, 245, 249))
    draw.rounded_rectangle([bx, by + 44, bx + 14, by + 52], radius=4, fill=(16, 185, 129))
    
    div_y2 = c2_y + 148
    draw.line([(145, div_y2), (120 + card_w - 20, div_y2)], fill=(241, 245, 249), width=1)
    draw_pill_badge(draw, 172, div_y2 + 28, "출처", font=get_font(9.5, 'bold'), theme='slate', has_dot=False, dark_mode=False, pad_x=8, height=22)
    draw.text((200, div_y2 + 20), "모바일 인지부하(Cognitive Load) 및 호가 변동 타이핑 인터뷰 (N=428)", font=get_font(10.5, 'regular'), fill=(100, 116, 139))
    
    # CARD 3: 0 / 14개 (14-Segment Matrix Block Chart + Source Citation)
    c3_y = c2_y + card_h + gap
    draw.rounded_rectangle([120, c3_y, 120 + card_w, c3_y + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([120, c3_y + 18, 125, c3_y + card_h - 18], radius=2, fill=(0, 87, 255))
    
    draw.text((148, c3_y + 18), "0 / 14개", font=get_num_font(44, 'black'), fill=(0, 87, 255))
    draw.text((148, c3_y + 70), "기존 증권사 앱의 역산 부재", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    draw.text((148, c3_y + 98), "단순히 평단을 더해줄 뿐 '얼마나 더 사야 하는가'에 답하지 못함", font=get_font(12, 'regular'), fill=(100, 116, 139))
    
    mx = 120 + card_w - 150
    my = c3_y + 24
    bs = 14
    bgap = 5
    for idx in range(14):
        r = idx // 7
        c = idx % 7
        bx_seg = mx + c * (bs + bgap)
        by_seg = my + r * (bs + bgap)
        draw.rounded_rectangle([bx_seg, by_seg, bx_seg + bs, by_seg + bs], radius=3, fill=(254, 242, 242), outline=(252, 165, 165), width=1)
        draw.text((bx_seg + 3, by_seg + 1), "✕", font=get_font(7.5, 'bold'), fill=(239, 68, 68))
    draw.text((mx, my + 2 * (bs + bgap) + 5), "14개사 전무 (0% 역산 지원)", font=get_font(8.5, 'bold'), fill=(239, 68, 68))
    
    div_y3 = c3_y + 148
    draw.line([(145, div_y3), (120 + card_w - 20, div_y3)], fill=(241, 245, 249), width=1)
    draw_pill_badge(draw, 172, div_y3 + 28, "출처", font=get_font(9.5, 'bold'), theme='slate', has_dot=False, dark_mode=False, pad_x=8, height=22)
    draw.text((200, div_y3 + 20), "국내 14대 증권사 모바일 트레이딩 시스템(MTS) 기능 전수 조사 (2026.03)", font=get_font(10.5, 'regular'), fill=(100, 116, 139))
    
    # RIGHT SIDE: 3 Concrete IDI Reality Cards
    cards = [
        ("01", "비중 왜곡 : 무계획 추가 매수로 계좌가 묶이는 악순환",
         "\"단가를 낮추려 4차까지 추가 매수했지만, 예수금 78%가 한 종목에 물렸고 평단은 겨우 1.8% 내려갔습니다.\"",
         "— 3년 차 스윙 투자자 심층 인터뷰",
         "단일 종목 편중 경고와 차수별 방어 효과를 실시간으로 보여주어 무리한 물타기 방지"),
         
        ("02", "조작 피로 : 초 단위 폭락 장세에서의 입력 지연과 스트레스",
         "\"호가가 무너지는 순간 키보드로 가격을 입력하다 지지선을 놓쳐 -6.4% 추가 손실을 봤습니다.\"",
         "— 모멘텀 단타 / 크립토 트레이더 인터뷰",
         "0.2초 음성 입력과 원터치 호가 프리셋 칩으로 긴박한 순간의 타이핑 스트레스 제거"),
         
        ("03", "목표 부재 : 손익분기점 탈출에 필요한 정확한 수량의 부재",
         "\"희망 매도가로 탈출하기 위해 정확히 몇 주를 얼마에 사야 하는지 계산할 수 없어 맹목적으로 샀습니다.\"",
         "— 5년 차 퀀트 투자자 심층 인터뷰",
         "목표 탈출가 입력 즉시 필요한 정확한 수량과 자금을 한눈에 보여주는 역산 솔루션")
    ]
    
    ry = sy
    for num, ptitle, pquote, pwho, psol in cards:
        draw.rounded_rectangle([660, ry, 1800, ry + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        
        # Number badge
        draw.rounded_rectangle([695, ry + 22, 735, ry + 54], radius=6, fill=(15, 23, 42))
        n_bbox = draw.textbbox((0, 0), num, font=get_num_font(15, 'bold'))
        draw.text((715 - (n_bbox[0] + n_bbox[2]) / 2, ry + 38 - (n_bbox[1] + n_bbox[3]) / 2), num, font=get_num_font(15, 'bold'), fill=(255, 255, 255))
        draw.text((750, ry + 26), ptitle, font=get_font(17.5, 'bold'), fill=(15, 23, 42))
        
        # Quote Card
        draw.rounded_rectangle([695, ry + 66, 1765, ry + 138], radius=8, fill=(248, 250, 252))
        draw.text((715, ry + 76), pquote, font=get_font(13.5, 'semibold'), fill=(30, 41, 59))
        draw.text((715, ry + 104), pwho, font=get_font(12, 'regular'), fill=(100, 116, 139))
            
        # Solution Tag
        _, _, bx2, _ = draw_pill_badge(draw, 735, ry + 172, "SOLUTION", font=get_font(10.5, 'bold'), theme='blue', has_dot=False, dark_mode=False, pad_x=10, height=24)
        psol_bbox = draw.textbbox((0, 0), psol, font=get_font(13.5, 'semibold'))
        psol_ty = int(round(ry + 172 - (psol_bbox[1] + psol_bbox[3]) / 2.0))
        draw.text((bx2 + 14, psol_ty), psol, font=get_font(13.5, 'semibold'), fill=(30, 41, 59))
        
        ry += card_h + gap
        
    base.save(f'{OUT_DIR}/slide_02.png')
    print("SAVED slide_02.png (Visual Charts & Citations)")

# ==============================================================
# SLIDE 03: Benchmark Matrix & Personas (Quantitative Architecture)
# ==============================================================
def make_slide_03():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    draw.line([(120, 100), (1800, 100)], fill=(226, 232, 240), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(226, 232, 240), width=1)
    
    draw.text((120, 130), "03  /  PERSONA & JOURNEY", font=get_font(13, 'bold'), fill=(0, 87, 255))
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
    draw.text((tx + 410, ty + 18), "일반 계산기 앱 (Ad-Supported)", font=get_font(13.5, 'bold'), fill=(71, 85, 105))
    
    col4_l = tx + 620
    col4_r = tx + tw - 10
    draw.rounded_rectangle([col4_l, ty + 6, col4_r, ty + 639], radius=12, fill=(240, 246, 255), outline=(186, 215, 255), width=2)
    draw.rounded_rectangle([col4_l + 12, ty + 12, col4_r - 12, ty + 50], radius=8, fill=(0, 87, 255))
    draw.text((col4_l + 38, ty + 20), "SMART DCA CALCULATOR", font=get_font(12, 'bold'), fill=(255, 255, 255))
    
    matrix = [
        ("입력 인터랙션 (Modality)", "단일 키패드 (Keypad Only)", "광고 노출 키패드 (Ad-Delay)", "멀티모달 (AI 음성 + 호가 칩)"),
        ("핵심 연산 모델 (Engine)", "단순 가중평균 (사후 합산)", "1회성 단일 수식 (휘발성)", "목표가 기반 폐쇄형 역산 엔진"),
        ("의사결정 지원 (Decision)", "단일 수치 나열", "미지원", "A vs B 전략 실시간 대조 매트릭스"),
        ("자산 안전 가드 (Safety)", "계좌 평가액 단순 나열", "미지원", "단일 종목 편중 및 예수금 고갈 경보"),
        ("개인 데이터 보안 (Privacy)", "중앙 서버 종속 (공인인증)", "임시 세션 (앱 종료 시 리셋)", "100% 온디바이스 로컬 저장"),
        ("사용자 경험 보호 (Session)", "타사 금융 상품 배너 혼재", "연산 중 전면 광고 노출 (흐름 중단)", "24시간 안심 무광고 리워드 세션"),
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
    draw.text((120, 130), "04  /  ARCHITECTURE", font=get_font(13, 'bold'), fill=(0, 210, 255))
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
    draw.text((120, 130), "05  /  USER FLOW", font=get_font(13, 'bold'), fill=(0, 210, 255))
    draw.text((120, 165), "User Flow", font=get_font(52, 'black'), fill=(255, 255, 255))
    draw.text((120, 240), "위기 진단부터 0.2초 음성 입력, 목표 역산, 최종 플랜 확정까지의 4단계 여정", font=get_font(18, 'regular'), fill=(148, 163, 184))
    
    # Flow Steps Definition: (Mockup, Step No, Title, Situation, Solution, Trigger, Action Badge, Theme)
    steps = [
        (
            'portfolio/iphone_mockups/iphone_01_home.png',
            'STEP 01', '자산 현황 진단',
            '갑작스러운 주가 급락(-16.7%) 발생',
            '홈 대시보드 1초 조망 및 계좌 진단',
            '0.2초 음성 도크 진입',
            '0.2초 음성 도크 진입',
            'cyan'
        ),
        (
            'portfolio/iphone_mockups/iphone_08_voice.png',
            'STEP 02', '0.2초 음성 입력',
            '급변하는 호가 속 타이핑 오입력 불안',
            '자연어 음성 인식으로 수치 즉시 추출',
            '목표 평단 역산기 인계',
            '목표 역산 인계',
            'blue'
        ),
        (
            'portfolio/iphone_mockups/iphone_03_target.png',
            'STEP 03', '목표 평단가 역산',
            '원금 탈출을 위한 필요 매수량 불명확',
            '희망 목표가 기준 필요 수량 즉시 역산',
            '예수금 슬라이더 조율',
            '최종 방어 플랜 산출',
            'amber'
        ),
        (
            'portfolio/iphone_mockups/iphone_02_sim.png',
            'STEP 04', '최종 플랜 확정',
            '무리한 매수로 인한 현금 고갈 방지 필요',
            '65% 예수금 보존 최적 평단 확정',
            '1-Tap 주문 플랜 복사',
            '',
            'green'
        )
    ]
    
    pw = 236
    ph = int(round(pw * (2090.0 / 856.0))) # 576px
    py = 265
    
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
    draw.text((120, 130), "06  /  WIREFRAME", font=get_font(13, 'bold'), fill=(0, 87, 255))
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
            draw.text((px + 24, py + 364), "• 공식: Q_add = Q_0(P_0-Pt)/(Pt-Pa)\n• 필요 총 예수금 : ₩ 2,125,000\n• 연산 방식 : 닫힌 형식(Closed-form) 무지연 산출", font=get_font(9.5, 'regular'), fill=(71, 85, 105), spacing=2)
            
            # Bottom Action CTA
            draw.rounded_rectangle([px + 14, py + 490, px + pw - 14, py + 528], radius=8, fill=(16, 185, 129))
            draw.text((px + 52, py + 501), "✓ 시뮬레이터로 즉시 자동 주입", font=get_font(11, 'bold'), fill=(255, 255, 255))
            
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
    draw_pill_badge(draw, cx=215, cy=by + 27, text="WIREFRAME SPEC & ERGONOMICS", font=get_font(10.5, 'bold'), theme='dark', has_dot=False, dark_mode=False, pad_x=12, height=30)
    draw.text((340, by + 18), "• 8pt 그리드 시스템 및 Material/HIG 48dp 터치 타깃 준수   • Fitts' Law 기반 Thumb-Zone 최적화   • 인지 부하 최소화 모바일 인터랙션 최적화", font=get_font(12, 'semibold'), fill=(51, 65, 85))

    base.save(f'{OUT_DIR}/slide_06.png')
    print("SAVED slide_06.png (Mobile Wireframe & Ergonomics)")


# ==============================================================
# SLIDE 07: Enterprise Design System (Korail Reference Image 4 Style)
# ==============================================================
def make_slide_07():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # 1. Header (Centered like Reference Image 4)
    kicker = "DESIGN SYSTEM"
    font_k = get_font(14, 'bold')
    kw = draw.textlength(kicker, font=font_k)
    draw.text(((W - kw) / 2, 75), kicker, font=font_k, fill=(0, 82, 255))
    
    t_pre = "신뢰와 확신을 주는 "
    t_blue = "스마트 퀀트 블루"
    t_post = "를 사용했어요."
    font_title = get_font(38, 'bold')
    w_pre = draw.textlength(t_pre, font=font_title)
    w_blue = draw.textlength(t_blue, font=font_title)
    w_post = draw.textlength(t_post, font=font_title)
    total_w = w_pre + w_blue + w_post
    start_x = (W - total_w) / 2
    
    draw.text((start_x, 115), t_pre, font=font_title, fill=(15, 23, 42))
    draw.text((start_x + w_pre, 115), t_blue, font=font_title, fill=(0, 82, 255))
    draw.text((start_x + w_pre + w_blue, 115), t_post, font=font_title, fill=(15, 23, 42))
    
    desc1 = "브랜드 컬러와 지정 서체를 활용하고, W3C DTCG 및 피그마 디자인 토큰 시스템을 적용했습니다."
    desc2 = "하락장 속에서도 투자자가 차분하게 판단할 수 있도록, 맑고 신뢰감 있는 퀀트 블루와 가독성 높은 Pretendard를 채택했습니다."
    font_desc = get_font(15, 'regular')
    w_d1 = draw.textlength(desc1, font=font_desc)
    w_d2 = draw.textlength(desc2, font=font_desc)
    draw.text(((W - w_d1) / 2, 175), desc1, font=font_desc, fill=(71, 85, 105))
    draw.text(((W - w_d2) / 2, 203), desc2, font=font_desc, fill=(71, 85, 105))
    
    # 2. Three Cards Grid (Left: Typography Scale, Middle: Brand Blue, Right: Grayscale)
    card_y = 265
    card_h = 680
    c1_x = 100
    c1_w = 800
    
    c2_x = 940
    c2_w = 540
    
    c3_x = 1520
    c3_w = 300
    
    # Card 1: Typography (Left Card)
    draw.rounded_rectangle([c1_x, card_y, c1_x + c1_w, card_y + card_h], radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((c1_x + 50, card_y + 45), "Pretendard", font=get_font(42, 'bold'), fill=(15, 23, 42))
    draw.text((c1_x + 300, card_y + 54), "프리텐다드", font=get_font(30, 'bold'), fill=(15, 23, 42))
    
    th_y = card_y + 130
    draw.text((c1_x + 50, th_y), "Scale", font=get_font(14, 'medium'), fill=(148, 163, 184))
    draw.text((c1_x + 520, th_y), "Size", font=get_font(14, 'medium'), fill=(148, 163, 184))
    draw.text((c1_x + 650, th_y), "Weight", font=get_font(14, 'medium'), fill=(148, 163, 184))
    draw.line([(c1_x + 50, th_y + 26), (c1_x + c1_w - 50, th_y + 26)], fill=(226, 232, 240), width=1)
    
    scales = [
        ("H1 디스플레이 타이틀", "32", "Black / Bold"),
        ("H2 메인 타이틀", "24", "SemiBold"),
        ("서브 타이틀", "20", "SemiBold"),
        ("섹션 헤더", "18", "SemiBold"),
        ("본문 1 (Primary Body)", "16", "Medium"),
        ("본문 2 (Secondary Body)", "15", "Medium"),
        ("설명 1 (Caption / Meta)", "14", "Regular"),
        ("설명 2 (Badge / Tiny)", "12", "Regular"),
        ("버튼 텍스트 (Action CTA)", "14", "SemiBold")
    ]
    
    tr_y = th_y + 45
    for s_name, s_size, s_weight in scales:
        draw.text((c1_x + 50, tr_y), s_name, font=get_font(16, 'semibold'), fill=(30, 41, 59))
        draw.text((c1_x + 525, tr_y), s_size, font=get_font(16, 'bold'), fill=(15, 23, 42))
        draw.text((c1_x + 650, tr_y), s_weight, font=get_font(16, 'medium'), fill=(71, 85, 105))
        tr_y += 50
        
    # Card 2: Brand Color Card (Middle Card)
    draw.rounded_rectangle([c2_x, card_y, c2_x + c2_w, card_y + 240], radius=20, fill=(0, 82, 255))
    draw.text((c2_x + 36, card_y + 36), "QUANT BLUE", font=get_font(18, 'bold'), fill=(255, 255, 255))
    draw.text((c2_x + 36, card_y + 64), "#0052FF", font=get_font(14, 'medium'), fill=(191, 219, 254))
    draw.text((c2_x + 220, card_y + 180), "투자의 확신과 신뢰를\n담은 스마트 퀀트 블루", font=get_font(16, 'medium'), fill=(255, 255, 255), spacing=6)
    
    tint_y = card_y + 265
    draw.rounded_rectangle([c2_x, tint_y, c2_x + c2_w, card_y + card_h], radius=20, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    tints = [
        ("Dark", "#0038B8", (0, 56, 184), (255, 255, 255)),
        ("Light 1", "#93C5FD", (147, 197, 253), (30, 41, 59)),
        ("Light 2", "#BFDBFE", (191, 219, 254), (30, 41, 59)),
        ("Light 3", "#DBEAFE", (219, 234, 254), (30, 41, 59)),
        ("Light 4", "#EFF6FF", (239, 246, 255), (30, 41, 59))
    ]
    
    ti_y = tint_y + 15
    for t_label, t_hex, t_rgb, t_tx in tints:
        draw.rounded_rectangle([c2_x + 20, ti_y, c2_x + c2_w - 20, ti_y + 68], radius=12, fill=t_rgb, outline=(226, 232, 240) if t_label == "Light 4" else None)
        draw.text((c2_x + 40, ti_y + 24), f"{t_label}  {t_hex}", font=get_font(15, 'bold'), fill=t_tx)
        ti_y += 76
        
    # Card 3: Grayscale & Semantic Status (Right Card)
    draw.rounded_rectangle([c3_x, card_y, c3_x + c3_w, card_y + card_h], radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    grays = [
        ("Black #0F172A", (15, 23, 42), (255, 255, 255)),
        ("Slate #334155", (51, 65, 85), (255, 255, 255)),
        ("Slate #64748B", (100, 116, 139), (255, 255, 255)),
        ("Gray #94A3B8", (148, 163, 184), (255, 255, 255)),
        ("Gray #CBD5E1", (203, 213, 225), (30, 41, 59)),
        ("Light #E2E8F0", (226, 232, 240), (30, 41, 59)),
        ("Light #F8FAFC", (248, 250, 252), (30, 41, 59)),
        ("White #FFFFFF", (255, 255, 255), (30, 41, 59))
    ]
    
    gi_y = card_y + 20
    for g_label, g_rgb, g_tx in grays:
        draw.rounded_rectangle([c3_x + 18, gi_y, c3_x + c3_w - 18, gi_y + 72], radius=10, fill=g_rgb, outline=(226, 232, 240) if "White" in g_label or "Light" in g_label else None)
        draw.text((c3_x + 36, gi_y + 26), g_label, font=get_font(13.5, 'bold'), fill=g_tx)
        gi_y += 79
        
    base.save(f'{OUT_DIR}/slide_07.png')
    print("SAVED slide_07.png (Korail-style Design System Cards)")

# ==============================================================
# SLIDE 08: Feature Spotlight 01 - Voice Input (Korail Image 5 Style)
# ==============================================================
def make_slide_08():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # 1. Header (Category Kicker + Conversational Title with Blue Highlights)
    draw.text((100, 75), "VOICE INPUT DOCK", font=get_font(14, 'bold'), fill=(0, 82, 255))
    
    t1_a = "복잡한 타이핑 없이 "
    t1_b = "말 한마디로,"
    font_title = get_font(38, 'bold')
    w_t1_a = draw.textlength(t1_a, font=font_title)
    draw.text((100, 115), t1_a, font=font_title, fill=(15, 23, 42))
    draw.text((100 + w_t1_a, 115), t1_b, font=font_title, fill=(0, 82, 255))
    
    t2_a = "0.2초 만에 "
    t2_b = "파라미터를 완성해요."
    w_t2_a = draw.textlength(t2_a, font=font_title)
    draw.text((100, 172), t2_a, font=font_title, fill=(15, 23, 42))
    draw.text((100 + w_t2_a, 172), t2_b, font=font_title, fill=(0, 82, 255))
    
    desc1 = "급격히 하락하는 장세 속에서 긴박한 타이핑 실수(Fat-finger)를 원천 차단하기 위해 화면 하단에 0.2초 음성 도크를 배치했어요."
    desc2 = "자연어 음성 발화 즉시 수치와 종목을 100% 로컬에서 분리·파싱해 계산기 모듈로 무지연 자동 입력합니다."
    draw.text((100, 245), desc1, font=get_font(15, 'regular'), fill=(71, 85, 105))
    draw.text((100, 275), desc2, font=get_font(15, 'regular'), fill=(71, 85, 105))
    
    # 2. Left Column: 2 Clean Comparison Previews
    card_l_w = 200
    screen_home = Image.open('portfolio/iphone_mockups/iphone_01_home.png').convert('RGBA')
    s1_w = card_l_w
    s1_h = int(round(s1_w * (screen_home.height / screen_home.width)))
    s1 = screen_home.resize((s1_w, s1_h), Image.Resampling.LANCZOS)
    
    screen_sim = Image.open('portfolio/iphone_mockups/iphone_02_sim.png').convert('RGBA')
    s2_w = card_l_w
    s2_h = int(round(s2_w * (screen_sim.height / screen_sim.width)))
    s2 = screen_sim.resize((s2_w, s2_h), Image.Resampling.LANCZOS)
    
    y_screen = 375
    x_s1 = 100
    x_s2 = 330
    
    draw.text((x_s1 + 55, y_screen - 36), "직접 타이핑 입력", font=get_font(13.5, 'bold'), fill=(100, 116, 139))
    draw.text((x_s2 + 55, y_screen - 36), "음성 도크 자동 파싱", font=get_font(13.5, 'bold'), fill=(0, 82, 255))
    
    for sx, simg in [(x_s1, s1), (x_s2, s2)]:
        sh = Image.new('RGBA', (W, H), (0,0,0,0))
        shd = ImageDraw.Draw(sh)
        shd.rounded_rectangle([sx + 6, y_screen + 10, sx + card_l_w - 6, y_screen + s1_h + 12], radius=24, fill=(0, 0, 0, 45))
        sh = sh.filter(ImageFilter.GaussianBlur(14))
        base = Image.alpha_composite(base, sh)
        base.paste(simg, (sx, y_screen), simg)
        
    draw = ImageDraw.Draw(base)
    draw.text((x_s1 + 25, y_screen + s1_h + 16), "• 4개 파라미터 수동 입력 (240초)\n• 하락장 긴박한 타이핑 오타 빈발", font=get_font(12, 'regular'), fill=(148, 163, 184), spacing=4)
    draw.text((x_s2 + 25, y_screen + s2_h + 16), "• 자연어 발화 즉시 0.2초 분리 인계\n• 100% 온디바이스 로컬 연산", font=get_font(12, 'semibold'), fill=(0, 82, 255), spacing=4)
    
    # 3. Center Column: Grand Hero Phone Mockup
    phone_voice = Image.open('portfolio/iphone_mockups/iphone_08_voice.png').convert('RGBA')
    pw = 350
    ph = int(round(pw * (phone_voice.height / phone_voice.width)))
    phone_v = phone_voice.resize((pw, ph), Image.Resampling.LANCZOS)
    
    px = 640
    py = 220
    
    sh_center = Image.new('RGBA', (W, H), (0,0,0,0))
    shc_draw = ImageDraw.Draw(sh_center)
    shc_draw.rounded_rectangle([px + 12, py + 16, px + pw - 12, py + ph + 24], radius=36, fill=(0, 0, 0, 65))
    shc_draw.ellipse([px - 20, py + ph - 25, px + pw + 20, py + ph + 35], fill=(0, 82, 255, 30))
    sh_center = sh_center.filter(ImageFilter.GaussianBlur(28))
    base = Image.alpha_composite(base, sh_center)
    base.paste(phone_v, (px, py), phone_v)
    draw = ImageDraw.Draw(base)
    
    # 4. Right Column: Callouts & Component Card
    rx = 1100
    r_w = 720
    
    draw_pill_badge(draw, rx + 65, 270, "VOICE DOCK", font=get_font(11, 'bold'), pad_x=12, height=26)
    draw.text((rx, 305), "자연어 음성 즉각 인식 & 파라미터 분리", font=get_font(18, 'bold'), fill=(15, 23, 42))
    draw.text((rx, 340), "\"삼성전자 7만 원에 50주\" 말하는 순간 종목, 단가, 수량을 자동으로 분리 인식해요.\n발화가 끝남과 동시에 시뮬레이터 수치가 채워져 실시간 호가 변동에 즉각 대응합니다.", font=get_font(14, 'regular'), fill=(71, 85, 105), spacing=5)
    
    draw_pill_badge(draw, rx + 75, 435, "PRESET CHIPS", font=get_font(11, 'bold'), pad_x=12, height=26)
    draw.text((rx, 470), "소음 환경을 위한 원터치 호가 프리셋 칩", font=get_font(18, 'bold'), fill=(15, 23, 42))
    draw.text((rx, 505), "음성을 쓰기 어려운 대중교통이나 조용한 환경에서도 ±5%, ±10% 호가 칩으로\n손가락 1-Tap 터치만으로 0.1초 만에 즉시 추가 매수 시나리오를 계산해요.", font=get_font(14, 'regular'), fill=(71, 85, 105), spacing=5)
    
    card_y = 600
    card_h = 240
    draw.rounded_rectangle([rx, card_y, rx + r_w, card_y + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    draw_pill_badge(draw, rx + 80, card_y + 30, "AI LIVE PARSER", font=get_font(10.5, 'bold'), pad_x=10, height=24)
    draw.text((rx + 160, card_y + 22), "실시간 온디바이스 음성 파싱 피드백", font=get_font(13.5, 'bold'), fill=(15, 23, 42))
    
    draw.rounded_rectangle([rx + 24, card_y + 60, rx + r_w - 24, card_y + 130], radius=12, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
    draw.text((rx + 42, card_y + 76), "🎙️ \"삼성전자 70,000원에 50주 추가 매수\"", font=get_font(16, 'bold'), fill=(0, 82, 255))
    draw.text((rx + 42, card_y + 104), "100% 로컬 STT 음성 엔진 인식 완료 (소요 시간 0.22초)", font=get_font(12, 'regular'), fill=(100, 116, 139))
    
    chips = [
        ("종목", "삼성전자", (0, 82, 255)),
        ("매수가", "₩ 70,000", (16, 185, 129)),
        ("수량", "50 주", (147, 51, 234)),
        ("인계 상태", "자동 완성 ✓", (245, 158, 11))
    ]
    cx = rx + 24
    cy = card_y + 155
    cw = 158
    for label, val, c_col in chips:
        draw.rounded_rectangle([cx, cy, cx + cw, cy + 60], radius=8, fill=(250, 252, 255), outline=(226, 232, 240), width=1)
        draw.text((cx + 14, cy + 10), label, font=get_font(11, 'bold'), fill=(100, 116, 139))
        draw.text((cx + 14, cy + 32), val, font=get_font(13.5, 'bold'), fill=c_col)
        cx += cw + 14
        
    base.save(f'{OUT_DIR}/slide_08.png')
    print("SAVED slide_08.png (Korail Image 5 Style Voice Dock UI)")

# ==============================================================
# SLIDE 09: Feature Spotlight 02 - Goal-Seeking (Korail Image 5 Style)
# ==============================================================
def make_slide_09():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # 1. Header (Category Kicker + Conversational Title with Blue Highlights)
    draw.text((100, 75), "GOAL SEEKING ENGINE", font=get_font(14, 'bold'), fill=(0, 82, 255))
    
    t1_a = "원하는 "
    t1_b = "목표 평단만 지정하면,"
    font_title = get_font(38, 'bold')
    w_t1_a = draw.textlength(t1_a, font=font_title)
    draw.text((100, 115), t1_a, font=font_title, fill=(15, 23, 42))
    draw.text((100 + w_t1_a, 115), t1_b, font=font_title, fill=(0, 82, 255))
    
    t2_a = "필요한 "
    t2_b = "수량과 자금을 즉시 역산해요."
    w_t2_a = draw.textlength(t2_a, font=font_title)
    draw.text((100, 172), t2_a, font=font_title, fill=(15, 23, 42))
    draw.text((100 + w_t2_a, 172), t2_b, font=font_title, fill=(0, 82, 255))
    
    desc1 = "손익분기점 탈출을 위해 도달해야 하는 목표가를 설정하면, 몇 주를 얼마에 더 사야 하는지"
    desc2 = "닫힌 형식(Closed-form) 퀀트 방정식으로 오차 없이 온디바이스에서 즉시 도출합니다."
    draw.text((100, 245), desc1, font=get_font(15, 'regular'), fill=(71, 85, 105))
    draw.text((100, 275), desc2, font=get_font(15, 'regular'), fill=(71, 85, 105))
    
    # 2. Left Column: 2 Comparison / Step Screens
    card_l_w = 200
    screen_target = Image.open('portfolio/iphone_mockups/iphone_03_target.png').convert('RGBA')
    s1_w = card_l_w
    s1_h = int(round(s1_w * (screen_target.height / screen_target.width)))
    s1 = screen_target.resize((s1_w, s1_h), Image.Resampling.LANCZOS)
    
    screen_report = Image.open('portfolio/iphone_mockups/iphone_04_report.png').convert('RGBA')
    s2_w = card_l_w
    s2_h = int(round(s2_w * (screen_report.height / screen_report.width)))
    s2 = screen_report.resize((s2_w, s2_h), Image.Resampling.LANCZOS)
    
    y_screen = 375
    x_s1 = 100
    x_s2 = 330
    
    draw.text((x_s1 + 55, y_screen - 36), "목표 평단가 지정", font=get_font(13.5, 'bold'), fill=(100, 116, 139))
    draw.text((x_s2 + 55, y_screen - 36), "리스크 한도 점검", font=get_font(13.5, 'bold'), fill=(0, 82, 255))
    
    for sx, simg in [(x_s1, s1), (x_s2, s2)]:
        sh = Image.new('RGBA', (W, H), (0,0,0,0))
        shd = ImageDraw.Draw(sh)
        shd.rounded_rectangle([sx + 6, y_screen + 10, sx + card_l_w - 6, y_screen + s1_h + 12], radius=24, fill=(0, 0, 0, 45))
        sh = sh.filter(ImageFilter.GaussianBlur(14))
        base = Image.alpha_composite(base, sh)
        base.paste(simg, (sx, y_screen), simg)
        
    draw = ImageDraw.Draw(base)
    draw.text((x_s1 + 25, y_screen + s1_h + 16), "• 탈출 희망 평단 설정\n• 가용 예수금 실시간 연동", font=get_font(12, 'regular'), fill=(148, 163, 184), spacing=4)
    draw.text((x_s2 + 25, y_screen + s2_h + 16), "• 자산 쏠림도 및 비중 경고\n• 안전 매수 가이드 제시", font=get_font(12, 'semibold'), fill=(0, 82, 255), spacing=4)
    
    # 3. Center Column: Grand Hero Phone Mockup
    pw = 350
    ph = int(round(pw * (screen_target.height / screen_target.width)))
    phone_t = screen_target.resize((pw, ph), Image.Resampling.LANCZOS)
    
    px = 640
    py = 220
    
    sh_center = Image.new('RGBA', (W, H), (0,0,0,0))
    shc_draw = ImageDraw.Draw(sh_center)
    shc_draw.rounded_rectangle([px + 12, py + 16, px + pw - 12, py + ph + 24], radius=36, fill=(0, 0, 0, 65))
    shc_draw.ellipse([px - 20, py + ph - 25, px + pw + 20, py + ph + 35], fill=(0, 82, 255, 30))
    sh_center = sh_center.filter(ImageFilter.GaussianBlur(28))
    base = Image.alpha_composite(base, sh_center)
    base.paste(phone_t, (px, py), phone_t)
    draw = ImageDraw.Draw(base)
    
    # 4. Right Column: Callouts & Result Summary Component Card
    rx = 1100
    r_w = 720
    
    draw_pill_badge(draw, rx + 105, 270, "CLOSED-FORM QUANT", font=get_font(11, 'bold'), pad_x=12, height=26)
    draw.text((rx, 305), "수학적 폐쇄형 역산 알고리즘 (Zero-Latency)", font=get_font(18, 'bold'), fill=(15, 23, 42))
    draw.text((rx, 340), "Q_add = Q_0 × (P_0 - P_target) / (P_target - P_add) 수식을 온디바이스에서 즉시 풀어내어\n복잡한 시행착오 반복 연산 없이 닫힌 형식으로 필요 수량과 자금을 즉시 산출해요.", font=get_font(14, 'regular'), fill=(71, 85, 105), spacing=5)
    
    draw_pill_badge(draw, rx + 95, 435, "BOUNDARY GUARD", font=get_font(11, 'bold'), pad_x=12, height=26)
    draw.text((rx, 470), "비현실적 목표 사전 가드 & 대안 평단 제시", font=get_font(18, 'bold'), fill=(15, 23, 42))
    draw.text((rx, 505), "현재 추가 매수가보다 낮은 비현실적 목표 입력 시 즉시 감지하여 안전 경고를 띄우고,\n현재 가용 예수금 범위 안에서 도달 가능한 최선의 방어 평단을 추천해요.", font=get_font(14, 'regular'), fill=(71, 85, 105), spacing=5)
    
    card_y = 600
    card_h = 240
    draw.rounded_rectangle([rx, card_y, rx + r_w, card_y + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    draw_pill_badge(draw, rx + 80, card_y + 30, "QUANT ENGINE", font=get_font(10.5, 'bold'), pad_x=10, height=24)
    draw.text((rx + 160, card_y + 22), "수학적 목표 도달 수량 산출 완료 (오차 0%)", font=get_font(13.5, 'bold'), fill=(15, 23, 42))
    
    draw.rounded_rectangle([rx + 24, card_y + 60, rx + r_w - 24, card_y + 130], radius=12, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
    draw.text((rx + 42, card_y + 76), "📊 \"+42.5주 추가 매수 필요 (소요 예수금: ₩ 2,125,000)\"", font=get_font(16, 'bold'), fill=(0, 82, 255))
    draw.text((rx + 42, card_y + 104), "목표 탈출 평단 ₩ 70,000 도달 확정 · 1-Tap 시뮬레이터 인계 지원", font=get_font(12, 'regular'), fill=(100, 116, 139))
    
    chips = [
        ("현재 평단", "₩ 78,000", (100, 116, 139)),
        ("목표 평단", "₩ 70,000", (0, 82, 255)),
        ("필요 수량", "+42.5 주", (16, 185, 129)),
        ("탈출 여부", "손익분기 도달 ✓", (245, 158, 11))
    ]
    cx = rx + 24
    cy = card_y + 155
    cw = 158
    for label, val, c_col in chips:
        draw.rounded_rectangle([cx, cy, cx + cw, cy + 60], radius=8, fill=(250, 252, 255), outline=(226, 232, 240), width=1)
        draw.text((cx + 14, cy + 10), label, font=get_font(11, 'bold'), fill=(100, 116, 139))
        draw.text((cx + 14, cy + 32), val, font=get_font(13.5, 'bold'), fill=c_col)
        cx += cw + 14
        
    base.save(f'{OUT_DIR}/slide_09.png')
    print("SAVED slide_09.png (Korail Image 5 Style Goal Seeking UI)")

# ==============================================================
# SLIDE 10: High-Fidelity Mobile Screens (Korail Image 5 Style)
# ==============================================================
def make_slide_10():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Header
    draw.text((100, 75), "FIGMA & FLUTTER SYSTEM", font=get_font(14, 'bold'), fill=(0, 82, 255))
    
    t1_a = "자산 진단부터 퀀트 역산까지, "
    t1_b = "일관된 6대 핵심 화면이에요."
    font_title = get_font(38, 'bold')
    w_t1_a = draw.textlength(t1_a, font=font_title)
    draw.text((100, 115), t1_a, font=font_title, fill=(15, 23, 42))
    draw.text((100 + w_t1_a, 115), t1_b, font=font_title, fill=(0, 82, 255))
    
    desc = "사용자의 핵심 투자 여정(User Journey)을 빈틈없이 지원하도록 피그마 디자인 토큰과 플러터 위젯 트리로 구현한 6대 상용 화면입니다."
    draw.text((100, 175), desc, font=get_font(15, 'regular'), fill=(71, 85, 105))
    
    screens = [
        ('portfolio/iphone_mockups/iphone_01_home.png', '01. 홈 대시보드', '자산 현황 한눈에 보기 & 음성 도크'),
        ('portfolio/iphone_mockups/iphone_08_voice.png', '02. AI 음성 비서', '0.2초 음성 & 호가 프리셋 칩'),
        ('portfolio/iphone_mockups/iphone_03_target.png', '03. 목표 역산 엔진', '손익분기점 탈출 필요 수량 도출'),
        ('portfolio/iphone_mockups/iphone_04_report.png', '04. 리스크 진단 리포트', '자산 쏠림 경고 & 안전도 진단'),
        ('portfolio/iphone_mockups/iphone_05_dark_home.png', '05. OLED 다크 테마', '야간 장세 최적화 초고대비 화면'),
        ('portfolio/iphone_mockups/iphone_06_dark_settings.png', '06. 맞춤 환경 설정', '글로벌 7개 언어 & 24시간 무광고')
    ]
    
    pw = 230
    phone_y = 235
    pgap = 68
    px = 100
    
    ref_phone = Image.open(screens[0][0])
    ph = int(round(pw * (ref_phone.height / ref_phone.width)))
    
    for img_path, title, role in screens:
        phone = Image.open(img_path).convert('RGBA')
        cur_ph = int(round(pw * (phone.height / phone.width)))
        phone = phone.resize((pw, cur_ph), Image.Resampling.LANCZOS)
        
        sh = Image.new('RGBA', (W, H), (0,0,0,0))
        shd = ImageDraw.Draw(sh)
        shd.rounded_rectangle([px + 8, phone_y + 12, px + pw - 8, phone_y + cur_ph + 18], radius=28, fill=(0, 0, 0, 55))
        sh = sh.filter(ImageFilter.GaussianBlur(16))
        base = Image.alpha_composite(base, sh)
        base.paste(phone, (px, phone_y), phone)
        
        draw = ImageDraw.Draw(base)
        
        pill_y = phone_y + cur_ph + 20
        draw_pill_badge(draw, px + pw // 2, pill_y + 16, title, font=get_font(11.5, 'bold'), pad_x=12, height=30)
        
        r_w = draw.textlength(role, font=get_font(11, 'medium'))
        draw.text((px + (pw - r_w) / 2, pill_y + 42), role, font=get_font(11, 'medium'), fill=(100, 116, 139))
        
        px += pw + pgap
        
    draw.rounded_rectangle([100, 920, 1820, 990], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, 190, 955, "USER JOURNEY", font=get_font(11, 'bold'), pad_x=12, height=28)
    
    flow_steps = [
        ("01 자산 상태 진단", 300),
        ("02 음성 빠른 입력", 560),
        ("03 탈출 평단 역산", 830),
        ("04 계좌 리스크 점검", 1100),
        ("05 야간 장세 몰입", 1370),
        ("06 맞춤 환경 설정", 1630)
    ]
    for step_txt, sx in flow_steps:
        draw.text((sx, 946), step_txt, font=get_font(13.5, 'bold'), fill=(15, 23, 42))
        if sx < 1600:
            draw.text((sx + 180, 944), "→", font=get_font(18, 'bold'), fill=(0, 82, 255))
            
    base.save(f'{OUT_DIR}/slide_10.png')
    print("SAVED slide_10.png (Korail Style 6 Mobile Screens)")

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
    draw.text((120, 130), "11  /  RESULTS & IMPACT", font=get_font(13, 'bold'), fill=(0, 210, 255))
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
        ("투자자 심리 상태", "처분 효과와 공포로 인한 비자발적 패닉셀(손절)", (148, 163, 184))
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
    draw.text((cx2 + 28, card_y + 100), "희망 탈출 가격에 맞춘 정량 분할 매수로 계좌와 심리적 안정성 확보", font=get_font(13.5, 'regular'), fill=(148, 163, 184))
    
    a_rows = [
        ("정량 최적 매수 집행", "+38주 분할 매수  ·  소요 자금 ₩ 2,470,000 (무지연 산출)", (0, 210, 255)),
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
    base = Image.new("RGBA", (W, H), (9, 13, 22, 255))
    
    glow = Image.new("RGBA", (W, H), (0,0,0,0))
    gw = ImageDraw.Draw(glow)
    gw.ellipse([1100, 200, 1850, 900], fill=(0, 87, 255, 60))
    gw.ellipse([150, 400, 750, 1000], fill=(0, 230, 118, 40))
    glow = glow.filter(ImageFilter.GaussianBlur(130))
    base = Image.alpha_composite(base, glow)
    draw = ImageDraw.Draw(base)
    
    draw.line([(120, 100), (1800, 100)], fill=(255, 255, 255, 20), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(255, 255, 255, 20), width=1)
    
    # Header - Minimalist & Punchy
    draw.text((120, 130), "12  /  RETROSPECTIVE & ROADMAP", font=get_font(13, "bold"), fill=(0, 210, 255))
    draw.text((120, 165), "Retrospective & Roadmap", font=get_font(52, "black"), fill=(255, 255, 255))
    draw.text((120, 235), "위기 극복 경험에서 얻은 핵심 인사이트와 향후 프로덕트 진화 방향", font=get_font(16, "regular"), fill=(148, 163, 184))
    
    # SECTION 1: 3 KEY LEARNINGS (상단: 핵심 배운 점 & UX 인사이트)
    learnings = [
        (
            "LEARNING 01",
            "공포 상황의 인지 마비 제어",
            "입력의 최소화가 곧 계좌 방어의 시작",
            [
                "급락장 한가운데서 투자자의 작업 기억(Working Memory)은 극도로 위축되며, 0.1초의 지연과 복잡한 키패드 타이핑은 패닉셀(뇌동매매)을 촉발합니다.",
                "'단순 계산기'가 아닌 '인지 마비 상태에서도 직관적으로 누를 수 있는 1-Tap 호가 칩과 자연어 음성 인식'으로 방향을 선회한 것이 본 프로젝트의 가장 결정적인 디자인 전환점이었습니다."
            ],
            "cyan", (0, 210, 255)
        ),
        (
            "LEARNING 02",
            "엄지 조작계와 음성 도크 시너지",
            "단일 인터랙션을 넘어선 하이브리드 UX",
            [
                "이동 중이거나 떨리는 손으로 소수점 가격을 직접 입력하는 고통을 해결하기 위해, 한 손 조작 영역(Thumb Zone) 하단에 음성 도크를 상시 배치했습니다.",
                "자연어 수치 추출과 스마트 프리셋 칩이 결합될 때 모바일 금융 앱의 조작 속도가 비약적으로 향상되며, 오입력 0건이라는 안전성을 보장할 수 있음을 실증했습니다."
            ],
            "green", (16, 185, 129)
        ),
        (
            "LEARNING 03",
            "수학적 불변성이 주는 심리적 안정",
            "막연한 추정이 아닌 정밀한 닫힌 형식 해",
            [
                "투자자가 겪는 불안의 본질은 '내가 과연 얼마를 더 사야 탈출할 수 있는가'에 대한 불확실성에 있었습니다.",
                "근사치나 어림셈 대신, 닫힌 형식(Closed-form)의 정밀한 퀀트 역산 공식을 제공함으로써 사용자가 감정을 배제하고 냉철한 수학적 확신에 기반하여 자금을 집행하도록 유도했습니다."
            ],
            "blue", (0, 114, 255)
        )
    ]
    
    lx = 120
    lw = 533
    lgap = 40
    ly = 265
    lh = 330
    
    for badge, title, subtitle, paras, theme_key, col in learnings:
        draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=16, fill=(16, 22, 34, 230), outline=(255, 255, 255, 20), width=1)
        draw_pill_badge(draw, lx + 70, ly + 28, badge, font=get_font(10, "bold"), theme=theme_key, has_dot=True, dark_mode=True, pad_x=10, height=24)
        draw.text((lx + 24, ly + 62), title, font=get_font(20, "bold"), fill=(255, 255, 255))
        draw.text((lx + 24, ly + 96), subtitle, font=get_font(13.5, "semibold"), fill=col)
        draw.line([(lx + 24, ly + 124), (lx + lw - 24, ly + 124)], fill=(255, 255, 255, 20), width=1)
        
        py = ly + 138
        for p in paras:
            lines = textwrap.wrap(p, width=28)
            for line in lines:
                draw.text((lx + 24, py), line, font=get_font(12, "regular"), fill=(160, 175, 195))
                py += 21
            py += 6
            
        lx += lw + lgap

    # SECTION 2: 3-PHASE PRODUCT EVOLUTION ROADMAP (중단: 향후 로드맵)
    roadmap = [
        (
            "PHASE 01 (LIVE)",
            "퀀트 역산 엔진 & 0.2초 음성 도크",
            "현재 Google Play 스토어 상용 출시 완료",
            [
                "국내/해외 주식 퀀트 목표 평단가 역산 엔진 탑재",
                "0.2초 로컬 자연어 음성 파싱 및 호가 프리셋 칩",
                "100% 오프라인 로컬 연산 (금융 데이터 유출 원천 차단)",
                "OLED 고대비 다크 모드 및 시맨틱 디자인 시스템"
            ],
            "cyan", (0, 210, 255)
        ),
        (
            "PHASE 02 (NEXT)",
            "마이데이터 오픈뱅킹 실시간 연동",
            "2026 Q4 예정 · 증권사 계좌 자동 동기화",
            [
                "금융 마이데이터 API 연동을 통한 보유 주식/예수금 자동 동기화",
                "급변하는 실시간 시장가 추적 및 손익분기 탈출선 자동 갱신",
                "급락 알림 및 1차/2차 분할 매수 적정 타이밍 자동 푸시",
                "다중 증권 계좌 통합 평단가 분산 관리 대시보드"
            ],
            "amber", (255, 179, 0)
        ),
        (
            "PHASE 03 (FUTURE)",
            "포트폴리오 리밸런싱 & 분할 주문 엔진",
            "2027 Q1 예정 · 퀀트 자산 배분 알고리즘",
            [
                "다종목 동시 탈출을 위한 마코위츠 기반 리밸런싱 최적화",
                "볼린저밴드/RSI 기술적 지표 연계 변동성 헷지 분할 주문 엔진",
                "투자 성향별 맞춤 머신러닝 리스크 완화 시나리오 추천",
                "글로벌 7개 국어 커뮤니티 전략 공유 플랫폼 확장"
            ],
            "purple", (168, 85, 247)
        )
    ]
    
    rx = 120
    rw = 533
    rgap = 40
    ry = 615
    rh = 260
    
    for phase_badge, r_title, r_sub, bullets, theme_key, r_col in roadmap:
        draw.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=16, fill=(16, 22, 34, 230), outline=(255, 255, 255, 20), width=1)
        draw_pill_badge(draw, rx + 75, ry + 28, phase_badge, font=get_font(10, "bold"), theme=theme_key, has_dot=True, dark_mode=True, pad_x=10, height=24)
        draw.text((rx + 24, ry + 62), r_title, font=get_font(18, "bold"), fill=(255, 255, 255))
        draw.text((rx + 24, ry + 92), r_sub, font=get_font(12.5, "medium"), fill=r_col)
        draw.line([(rx + 24, ry + 118), (rx + rw - 24, ry + 118)], fill=(255, 255, 255, 20), width=1)
        
        by = ry + 130
        for b_text in bullets:
            draw.text((rx + 24, by), f"• {b_text}", font=get_font(12, "regular"), fill=(160, 175, 195))
            by += 28
            
        rx += rw + rgap

    # SECTION 3: PROJECT CREDITS & PRODUCTION WRAP-UP (하단: 크레딧 및 상태)
    cy = 895
    ch = 60
    draw.rounded_rectangle([120, cy, 1800, cy + ch], radius=12, fill=(12, 17, 26, 255), outline=(255, 255, 255, 25), width=1)
    
    draw.text((144, cy + 20), "PROJECT CREDITS", font=get_font(12, "bold"), fill=(0, 210, 255))
    draw.text((270, cy + 20), "End-to-End Product Design  ·  Quant Mathematical Modeling  ·  Flutter Mobile Architecture", font=get_font(13, "medium"), fill=(255, 255, 255))
    
    draw_pill_badge(draw, 1420, cy + 30, "GOOGLE PLAY STORE LIVE", font=get_font(10, "bold"), theme="green", has_dot=True, dark_mode=True, pad_x=12, height=26)
    draw.text((1535, cy + 20), "100% Offline Engine · No Financial Logging", font=get_font(12, "medium"), fill=(148, 163, 184))
    
    base.save(f"{OUT_DIR}/slide_12.png")
    print("SAVED slide_12.png (Redesigned Retrospective & Roadmap - Zero Duplicate Metrics)")


if __name__ == '__main__':
    for i in range(1, 13):
        func_name = f'make_slide_{i:02d}'
        if func_name in globals():
            globals()[func_name]()
    print("ALL 12 SLIDES GENERATED WITH MASCULINE EDITORIAL AESTHETIC!")
