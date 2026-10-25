import math
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

def draw_parallelogram(draw, cx, cy, w, h, fill, outline, skew=12, width=1):
    pts = [
        (cx - w // 2 + skew, cy - h // 2),
        (cx + w // 2 + skew, cy - h // 2),
        (cx + w // 2 - skew, cy + h // 2),
        (cx - w // 2 - skew, cy + h // 2)
    ]
    draw.polygon(pts, fill=fill, outline=outline)

def draw_dashed_line(draw, p1, p2, col=(0, 82, 255), width=2, dash_len=4, gap_len=3):
    width = int(round(width))
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y2 - y1
    dist = (dx**2 + dy**2)**0.5
    if dist == 0:
        return
    step = dash_len + gap_len
    num_steps = int(dist // step)
    for i in range(num_steps):
        s = i * step
        e = s + dash_len
        sx = x1 + dx * (s / dist)
        sy = y1 + dy * (s / dist)
        ex = x1 + dx * (min(e, dist) / dist)
        ey = y1 + dy * (min(e, dist) / dist)
        draw.line([(sx, sy), (ex, ey)], fill=col, width=width)

def draw_dashed_rounded_rect(draw, bbox, radius=8, fill=(240, 246, 255), outline=(0, 82, 255), width=1, dash_len=4, gap_len=3):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill)
    x1, y1, x2, y2 = bbox
    draw_dashed_line(draw, (x1 + radius, y1), (x2 - radius, y1), outline, width, dash_len, gap_len)
    draw_dashed_line(draw, (x2, y1 + radius), (x2, y2 - radius), outline, width, dash_len, gap_len)
    draw_dashed_line(draw, (x2 - radius, y2), (x1 + radius, y2), outline, width, dash_len, gap_len)
    draw_dashed_line(draw, (x1, y2 - radius), (x1, y1 + radius), outline, width, dash_len, gap_len)

def draw_dashed_arrow(draw, p1, p2, col=(0, 82, 255), width=2, dash_len=4, gap_len=3, arrow_size=5):
    draw_dashed_line(draw, p1, p2, col, width, dash_len, gap_len)
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2:
        if y2 > y1:
            draw.polygon([(x2 - arrow_size, y2 - arrow_size * 1.5), (x2 + arrow_size, y2 - arrow_size * 1.5), (x2, y2)], fill=col)
        else:
            draw.polygon([(x2 - arrow_size, y2 + arrow_size * 1.5), (x2 + arrow_size, y2 + arrow_size * 1.5), (x2, y2)], fill=col)
    elif y1 == y2:
        if x2 > x1:
            draw.polygon([(x2 - arrow_size * 1.5, y2 - arrow_size), (x2 - arrow_size * 1.5, y2 + arrow_size), (x2, y2)], fill=col)
        else:
            draw.polygon([(x2 + arrow_size * 1.5, y2 - arrow_size), (x2 + arrow_size * 1.5, y2 + arrow_size), (x2, y2)], fill=col)

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

def draw_behavior_slider(draw, x, y, w, label, left_txt, right_txt, ratio, theme='blue'):
    """
    Renders an editorial behavior spectrum slider track with active segment and circular marker dot.
    Inspired by senior Behance case study persona spectrums.
    """
    theme_colors = {
        'blue': {'active': (0, 82, 255), 'dot': (0, 82, 255)},
        'amber': {'active': (217, 119, 6), 'dot': (217, 119, 6)},
        'green': {'active': (16, 185, 129), 'dot': (16, 185, 129)},
        'cyan': {'active': (6, 182, 212), 'dot': (6, 182, 212)},
    }
    col = theme_colors.get(theme, theme_colors['blue'])
    
    # Label
    draw.text((x, y), label, font=get_font(10.5, 'bold'), fill=(15, 23, 42))
    
    # Left and Right endpoint annotations
    draw.text((x + 75, y + 1), left_txt, font=get_font(9, 'medium'), fill=(100, 116, 139))
    r_bbox = draw.textbbox((0, 0), right_txt, font=get_font(9, 'medium'))
    r_w = r_bbox[2] - r_bbox[0]
    draw.text((x + w - r_w, y + 1), right_txt, font=get_font(9, 'medium'), fill=(100, 116, 139))
    
    # Slider Track
    track_x = x + 125
    track_w = w - 135 - r_w
    track_y = y + 7
    
    draw.rounded_rectangle([track_x, track_y, track_x + track_w, track_y + 4], radius=2, fill=(226, 232, 240))
    active_w = int(round(track_w * max(0.0, min(1.0, ratio))))
    draw.rounded_rectangle([track_x, track_y, track_x + active_w, track_y + 4], radius=2, fill=col['active'])
    
    # Indicator Dot (circle with white ring)
    dot_cx = track_x + active_w
    dot_cy = track_y + 2
    r = 5
    draw.ellipse([dot_cx - r - 1, dot_cy - r - 1, dot_cx + r + 1, dot_cy + r + 1], fill=(255, 255, 255))
    draw.ellipse([dot_cx - r, dot_cy - r, dot_cx + r, dot_cy + r], fill=col['dot'])


def draw_dotted_callout(draw, p1, p2, col=(0, 82, 255), dot_r=4, elbow_x=None):
    """
    Renders an architectural blueprint-style dotted connector line from phone UI anchor to annotation card.
    Inspired by Behance feature callout schematics.
    """
    x1, y1 = p1
    x2, y2 = p2
    
    # 1. Anchor node at start point (circle with white ring)
    draw.ellipse([x1 - dot_r - 2, y1 - dot_r - 2, x1 + dot_r + 2, y1 + dot_r + 2], fill=(255, 255, 255, 220))
    draw.ellipse([x1 - dot_r, y1 - dot_r, x1 + dot_r, y1 + dot_r], fill=col)
    
    # 2. Dotted path
    if elbow_x is None:
        elbow_x = int(x1 + (x2 - x1) * 0.45)
        
    pts = [(x1, y1), (elbow_x, y1), (elbow_x, y2), (x2, y2)]
    
    def draw_dotted_segment(ptA, ptB, dot_spacing=6):
        ax, ay = ptA
        bx, by = ptB
        dist = math.hypot(bx - ax, by - ay)
        if dist == 0:
            return
        steps = int(dist // dot_spacing)
        for s in range(steps + 1):
            t = s / max(1, steps)
            px = ax + (bx - ax) * t
            py = ay + (by - ay) * t
            draw.ellipse([px - 1.5, py - 1.5, px + 1.5, py + 1.5], fill=col)
            
    for i in range(len(pts) - 1):
        draw_dotted_segment(pts[i], pts[i+1])
        
    # 3. Arrow / terminal anchor at end point
    draw.polygon([(x2, y2), (x2 - 6, y2 - 4), (x2 - 6, y2 + 4)], fill=col)


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
    # Pristine soft airy canvas
    base = Image.new('RGBA', (W, H), (250, 252, 255, 255))
    
    # 1. Subtle Ambient Radial Glow in the center-right behind phones
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    g_draw.ellipse([850, 140, 1850, 840], fill=(0, 82, 255, 18))
    g_draw.ellipse([1100, 220, 1750, 750], fill=(6, 182, 212, 14))
    glow = glow.filter(ImageFilter.GaussianBlur(130))
    base = Image.alpha_composite(base, glow)
    
    draw = ImageDraw.Draw(base)
    
    # Hairline Top Boundary
    draw.line([(100, 52), (1820, 52)], fill=(226, 232, 240), width=1)
    
    # Top Kicker & Metadata
    draw_pill_badge(draw, left_x=100, cy=78, text="DCA QUANT LAB · 2026 CASE STUDY", font=get_font(11.5, 'bold'), theme='blue', has_dot=True, pad_x=12, height=28)
    
    meta_txt = "Personal Project · UI/UX Product Design & Fullstack Engineering"
    w_meta = draw.textlength(meta_txt, font=get_font(13.5, 'medium'))
    draw.text((1820 - w_meta, 70), meta_txt, font=get_font(13.5, 'medium'), fill=(100, 116, 139))
    
    # 2. Main Title (Centered-Left, Simple, Clean, Impactful - Reference Image Style)
    draw.text((100, 170), "SMART DCA CALCULATOR", font=get_font(15, 'bold'), fill=(0, 82, 255))
    
    # Big Clean Headline
    title_p1 = "평단을 낮추다, "
    title_p2 = "공포를 이기다."
    w_p1 = draw.textlength(title_p1, font=get_font(56, 'black'))
    draw.text((100, 206), title_p1, font=get_font(56, 'black'), fill=(15, 23, 42))
    draw.text((100 + w_p1, 206), title_p2, font=get_font(56, 'black'), fill=(0, 82, 255))
    
    # Clean Subtitle (1-2 sentences)
    sub1 = "급격한 주가 급락 속에서 막연한 감이나 단순 산술평균 계산이 아닌,"
    sub2 = "0.2초 음성 도크와 닫힌 형식(Closed-Form) 퀀트 역산으로 1초 만에 완성하는 스마트 물타기 계산기"
    draw.text((100, 290), sub1, font=get_font(16.5, 'regular'), fill=(71, 85, 105))
    draw.text((100, 318), sub2, font=get_font(16.5, 'semibold'), fill=(30, 41, 59))
    
    # 4 Status Badges (Clean Pastel Theme)
    badges = [
        ("SOLO 100% DESIGN & DEV", "blue"),
        ("GOOGLE PLAY STORE LIVE", "green"),
        ("0.2s VOICE DOCK", "cyan"),
        ("CLOSED-FORM QUANT", "purple")
    ]
    bx = 100
    for b_text, b_theme in badges:
        _, _, b_end, _ = draw_pill_badge(draw, left_x=bx, cy=385, text=b_text, font=get_font(11, 'bold'), theme=b_theme, has_dot=True, pad_x=12, height=30)
        bx = b_end + 12
        
    # Core Highlights Card (Clean Left Box)
    h_box_y = 445
    h_box_w = 680
    h_box_h = 365
    draw.rounded_rectangle([100, h_box_y, 100 + h_box_w, h_box_y + h_box_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    # Card Header
    draw_pill_badge(draw, left_x=128, cy=h_box_y + 36, text="PRODUCT MISSION", font=get_font(10.5, 'bold'), theme='blue', has_dot=False, pad_x=10, height=24)
    draw.text((270, h_box_y + 26), "감에 의존한 물타기를 멈추고 출구 전략을 세우다", font=get_font(15.5, 'bold'), fill=(15, 23, 42))
    
    draw.line([(128, h_box_y + 60), (100 + h_box_w - 28, h_box_y + 60)], fill=(241, 245, 249), width=1)
    
    key_points = [
        ("01", "0.2초 음성 도크 (Voice-First)", "호가 급변 시 타이핑 오타를 원천 차단하고 자연어 발화 즉시 수치 자동 파싱"),
        ("02", "닫힌 형식 퀀트 역산 (Closed-Form)", "희망 탈출 목표가 입력 시 필요한 매수 수량과 가용 자금을 0ms 즉각 도출"),
        ("03", "65% 예수금 안전 가드 (Safety Guard)", "무리한 물타기로 인한 계좌 묶임을 방지하고 차수별 현금 방어선 유지"),
        ("04", "100% 온디바이스 보안 (Zero-Server)", "금융 자산 데이터를 외부 서버에 전송하지 않고 기기 내부 로컬 저장")
    ]
    
    k_y = h_box_y + 78
    for num, k_title, k_desc in key_points:
        draw.rounded_rectangle([128, k_y, 160, k_y + 26], radius=5, fill=(241, 245, 249))
        draw.text((135, k_y + 5), num, font=get_font(11, 'bold'), fill=(0, 82, 255))
        draw.text((172, k_y + 4), k_title, font=get_font(13.5, 'bold'), fill=(15, 23, 42))
        draw.text((172, k_y + 26), k_desc, font=get_font(11.5, 'regular'), fill=(100, 116, 139))
        k_y += 66
        
    # 3. Flagship iPhone Mockups (Centered-Right, Clean & Elegant)
    phone_home = Image.open('portfolio/iphone_mockups/iphone_01_home.png').convert('RGBA')
    phone_target = Image.open('portfolio/iphone_mockups/iphone_03_target.png').convert('RGBA')
    
    target_h = 620
    target_w = int(round(target_h * (phone_home.width / phone_home.height)))
    
    p_front = phone_home.resize((target_w, target_h), Image.Resampling.LANCZOS)
    p_back = phone_target.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    angle = -12.0
    rot_front = p_front.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    rot_back = p_back.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    
    def make_shadow(img, blur=40, offset=(20, 36), alpha=75):
        mask = img.split()[3]
        sh_img = Image.new('RGBA', (img.width + 120, img.height + 120), (0, 0, 0, 0))
        black = Image.new('RGBA', img.size, (0, 0, 0, alpha))
        sh_img.paste(black, (60 + offset[0], 60 + offset[1]), mask)
        return sh_img.filter(ImageFilter.GaussianBlur(blur)), (60, 60)
        
    sh_back, pad_b = make_shadow(rot_back, blur=38, offset=(18, 32), alpha=60)
    sh_front, pad_f = make_shadow(rot_front, blur=44, offset=(22, 40), alpha=85)
    
    # Beautiful spatial placement
    p_back_x = 1260
    p_back_y = 150
    
    p_front_x = 980
    p_front_y = 210
    
    base.paste(sh_back, (p_back_x - pad_b[0], p_back_y - pad_b[1]), sh_back)
    base.paste(rot_back, (p_back_x, p_back_y), rot_back)
    
    base.paste(sh_front, (p_front_x - pad_f[0], p_front_y - pad_f[1]), sh_front)
    base.paste(rot_front, (p_front_x, p_front_y), rot_front)
    
    # 4. Floating Feature Callout Pills anchored to Mockups (Reference Style)
    draw = ImageDraw.Draw(base)
    draw_pill_badge(draw, cx=1140, cy=185, text="0.2s VOICE DOCK", font=get_font(10.5, 'bold'), theme='cyan', pad_x=12, height=28)
    draw_pill_badge(draw, cx=1640, cy=240, text="GOAL-SEEKING ENGINE", font=get_font(10.5, 'bold'), theme='amber', pad_x=12, height=28)
    draw_pill_badge(draw, cx=1550, cy=780, text="65% CASH SAFETY GUARD", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=28)
    
    # 5. Bottom Simple & Clean Specification Strip (Reference Style, Clean 4 Columns)
    bar_y = 860
    bar_h = 100
    draw.rounded_rectangle([100, bar_y, 1820, bar_y + bar_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    col_w = (1720) // 4
    specs = [
        ("PROJECT ROLE", "100% Solo Contribution", "기획(PM) · UI/UX 디자인 · Flutter 풀스택 개발"),
        ("PERIOD & SPRINT", "2026.02 - 2026.04", "6주 집중 스프린트 상용 프로덕션 배포 완료"),
        ("TECH STACK", "Flutter 3.x · Riverpod", "Dart · Riverpod · Python Quant · GitHub"),
        ("PLATFORM RELEASE", "Google Play Live & Web", "Android 상용 출시 & 실시간 인터랙티브 웹")
    ]
    
    for i, (cat, val_bold, val_desc) in enumerate(specs):
        cx = 100 + i * col_w
        if i > 0:
            draw.line([(cx, bar_y + 18), (cx, bar_y + bar_h - 18)], fill=(226, 232, 240), width=1)
        
        draw.text((cx + 28, bar_y + 18), cat, font=get_font(11, 'bold'), fill=(0, 82, 255))
        draw.text((cx + 28, bar_y + 40), val_bold, font=get_font(15, 'bold'), fill=(15, 23, 42))
        draw.text((cx + 28, bar_y + 66), val_desc, font=get_font(11.5, 'regular'), fill=(100, 116, 139))
        
    base.save(f'{OUT_DIR}/slide_01.png')
    print("SAVED clean simple Slide 01 successfully!")

def make_slide_02():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Hairline Top/Bottom Boundaries
    draw.line([(100, 52), (1820, 52)], fill=(226, 232, 240), width=1)
    draw.line([(100, 990), (1820, 990)], fill=(226, 232, 240), width=1)
    
    # Header - Reference Image 1 Center/Left Conversational Style
    draw.text((100, 75), "DESK RESEARCH & SWOT ANALYSIS", font=get_font(13.5, 'bold'), fill=(0, 82, 255))
    t1_a = "국내 투자자 행태 분석과 "
    t1_b = "비이성적 물타기의 기존 문제점"
    font_title = get_font(36, 'bold')
    w_t1_a = draw.textlength(t1_a, font=font_title)
    draw.text((100, 110), t1_a, font=font_title, fill=(15, 23, 42))
    draw.text((100 + w_t1_a, 110), t1_b, font=font_title, fill=(0, 82, 255))
    draw.text((100, 165), "투자자 428명 정량 데이터 및 14대 증권사 전수 조사를 통해 도출한 3대 핵심 위협과 SWOT 전략", font=get_font(15.5, 'regular'), fill=(71, 85, 105))
    
    # ==============================================================
    # 1. TOP: 3 Horizontal Market Trend Cards (Reference Image 1 Style)
    # ==============================================================
    card_w = 546
    card_h = 220
    gap = 40
    sy = 215
    
    # CARD 1: MARKET TREND (Donut Chart)
    c1_x = 100
    draw.rounded_rectangle([c1_x, sy, c1_x + card_w, sy + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([c1_x, sy + 18, c1_x + 5, sy + card_h - 18], radius=2, fill=(220, 38, 38))
    
    draw_pill_badge(draw, left_x=c1_x + 24, cy=sy + 36, text="MARKET TREND", font=get_font(10, 'bold'), theme='red', has_dot=False, pad_x=8, height=22)
    draw.text((c1_x + 24, sy + 62), "손실 회피와 비이성적 물타기", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    draw.text((c1_x + 24, sy + 90), "개인 투자자 10명 중 8명 이상이 출구 전략 없이\n감에 의존해 추가 매수를 감행하다 손실을 키웁니다.", font=get_font(12, 'regular'), fill=(100, 116, 139), spacing=4)
    
    draw.text((c1_x + 24, sy + 148), "82.6%", font=get_num_font(42, 'black'), fill=(220, 38, 38))
    draw.text((c1_x + 165, sy + 166), "경험률 (자본시장연구원 N=428)", font=get_font(11, 'bold'), fill=(100, 116, 139))
    
    cx_donut = c1_x + card_w - 75
    cy_donut = sy + 110
    draw_donut_chart_on_base(base, cx_donut, cy_donut, r_outer=38, r_inner=26, percentage=82.6, col_fill=(220, 38, 38), col_track=(241, 245, 249))
    draw = ImageDraw.Draw(base)
    d_lbl = "83%"
    d_bbox = draw.textbbox((0, 0), d_lbl, font=get_font(11, 'bold'))
    draw.text((cx_donut - (d_bbox[0] + d_bbox[2]) / 2, cy_donut - (d_bbox[1] + d_bbox[3]) / 2), d_lbl, font=get_font(11, 'bold'), fill=(220, 38, 38))
    
    # CARD 2: BEHAVIOR TREND (Bar Chart Comparison)
    c2_x = c1_x + card_w + gap
    draw.rounded_rectangle([c2_x, sy, c2_x + card_w, sy + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([c2_x, sy + 18, c2_x + 5, sy + card_h - 18], radius=2, fill=(217, 119, 6))
    
    draw_pill_badge(draw, left_x=c2_x + 24, cy=sy + 36, text="BEHAVIOR TREND", font=get_font(10, 'bold'), theme='amber', has_dot=False, pad_x=8, height=22)
    draw.text((c2_x + 24, sy + 62), "급박한 순간의 타이핑 인지부하", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    draw.text((c2_x + 24, sy + 90), "호가가 급변하는 폭락장에서 8자리 단가를 직접 치다\n지지선을 놓치고 추가 손실(-6.4%)에 직면합니다.", font=get_font(12, 'regular'), fill=(100, 116, 139), spacing=4)
    
    draw.text((c2_x + 24, sy + 148), "240s ➔ 4.2s", font=get_num_font(34, 'black'), fill=(217, 119, 6))
    draw.text((c2_x + 24, sy + 190), "소요 시간 -98% 단축 (인지부하 인터뷰 N=428)", font=get_font(11, 'bold'), fill=(16, 185, 129))
    
    # Comparison Bar Graphic
    bar_x = c2_x + card_w - 150
    bar_w = 125
    draw.text((bar_x, sy + 115), "기존 240초", font=get_font(9.5, 'bold'), fill=(148, 163, 184))
    draw.rounded_rectangle([bar_x, sy + 130, bar_x + bar_w, sy + 138], radius=4, fill=(254, 202, 202))
    draw.text((bar_x, sy + 152), "스마트 4.2초", font=get_font(9.5, 'bold'), fill=(16, 185, 129))
    draw.rounded_rectangle([bar_x, sy + 167, bar_x + 12, sy + 175], radius=4, fill=(16, 185, 129))
    
    # CARD 3: INDUSTRY GAP (Matrix Segment)
    c3_x = c2_x + card_w + gap
    draw.rounded_rectangle([c3_x, sy, c3_x + card_w, sy + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([c3_x, sy + 18, c3_x + 5, sy + card_h - 18], radius=2, fill=(0, 82, 255))
    
    draw_pill_badge(draw, left_x=c3_x + 24, cy=sy + 36, text="INDUSTRY GAP", font=get_font(10, 'bold'), theme='blue', has_dot=False, pad_x=8, height=22)
    draw.text((c3_x + 24, sy + 62), "증권사 MTS의 역산 기능 부재", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    draw.text((c3_x + 24, sy + 90), "국내 모든 MTS는 사후 가중평균만 보여줄 뿐,\n'탈출하려면 정확히 몇 주를 사야 하는가'에 답하지 못함.", font=get_font(12, 'regular'), fill=(100, 116, 139), spacing=4)
    
    draw.text((c3_x + 24, sy + 148), "0 / 14개", font=get_num_font(42, 'black'), fill=(0, 82, 255))
    draw.text((c3_x + 24, sy + 190), "국내 14대 증권사 MTS 전수조사 (역산 지원 0%)", font=get_font(11, 'bold'), fill=(100, 116, 139))
    
    # Matrix Grid Graphic
    mx = c3_x + card_w - 150
    my = sy + 120
    bs = 14
    bgap = 5
    for idx in range(14):
        r = idx // 7
        c = idx % 7
        bx_seg = mx + c * (bs + bgap)
        by_seg = my + r * (bs + bgap)
        draw.rounded_rectangle([bx_seg, by_seg, bx_seg + bs, by_seg + bs], radius=3, fill=(254, 242, 242), outline=(252, 165, 165), width=1)
        draw.text((bx_seg + 3, by_seg + 1), "✕", font=get_font(7.5, 'bold'), fill=(239, 68, 68))
        
    # ==============================================================
    # 2. MIDDLE: INSIGHT CONNECTING BANNER WITH DOWN ARROW (Image 1 Style)
    # ==============================================================
    ins_y = 465
    draw.rounded_rectangle([100, ins_y, 1820, ins_y + 54], radius=12, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
    draw_pill_badge(draw, left_x=120, cy=ins_y + 27, text="CORE INSIGHT", font=get_font(11, 'bold'), theme='blue', has_dot=True, pad_x=12, height=30)
    
    ins_text = "단순 수치 계산기가 아닌, '확실한 탈출 목표량 역산'과 '0.2초 음성 도크'를 결합한 전략적 퀀트 솔루션이 필요하다."
    draw.text((280, ins_y + 17), ins_text, font=get_font(14.5, 'bold'), fill=(0, 82, 255))
    
    # Down Arrow Indicator
    draw.polygon([(960, ins_y + 54), (952, ins_y + 64), (968, ins_y + 64)], fill=(0, 82, 255))
    
    # ==============================================================
    # 3. BOTTOM: 2x2 SWOT MATRIX (Left) + 3 STRATEGIC OUTCOMES (Right)
    # ==============================================================
    b_y = 550
    
    # Left: 2x2 SWOT Matrix (Reference Image 1 Style)
    swot_w = 830
    swot_h = 415
    draw.rounded_rectangle([100, b_y, 100 + swot_w, b_y + swot_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    draw.text((125, b_y + 20), "SWOT ANALYSIS : 스마트 물타기 계산기의 전략적 포지셔닝", font=get_font(15, 'bold'), fill=(15, 23, 42))
    draw.line([(125, b_y + 48), (100 + swot_w - 25, b_y + 48)], fill=(241, 245, 249), width=1)
    
    qw = (swot_w - 60) // 2
    qh = 158
    
    # S (Strength)
    s_x = 125
    s_y = b_y + 65
    draw.rounded_rectangle([s_x, s_y, s_x + qw, s_y + qh], radius=10, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
    draw_pill_badge(draw, left_x=s_x + 14, cy=s_y + 24, text="Strength (강점)", font=get_font(10, 'bold'), theme='green', has_dot=False, pad_x=8, height=22)
    s_points = [
        "• 0.2초 음성 도크로 타이핑 제로화",
        "• 닫힌 형식 퀀트 방정식 즉시 역산",
        "• 100% 온디바이스 개인정보 보호"
    ]
    dy = s_y + 48
    for p in s_points:
        draw.text((s_x + 14, dy), p, font=get_font(11.5, 'medium'), fill=(6, 95, 70))
        dy += 24
        
    # W (Weakness)
    w_x = s_x + qw + 10
    w_y = s_y
    draw.rounded_rectangle([w_x, w_y, w_x + qw, w_y + qh], radius=10, fill=(254, 242, 242), outline=(254, 202, 202), width=1)
    draw_pill_badge(draw, left_x=w_x + 14, cy=w_y + 24, text="Weakness (약점)", font=get_font(10, 'bold'), theme='red', has_dot=False, pad_x=8, height=22)
    w_points = [
        "• 초기 개인 개발자 브랜드 인지도",
        "• 증권사 계좌 API 실시간 직접 연동 부재",
        "• 사용자 수동 초기 평단/수량 입력 필요"
    ]
    dy = w_y + 48
    for p in w_points:
        draw.text((w_x + 14, dy), p, font=get_font(11.5, 'medium'), fill=(153, 27, 27))
        dy += 24
        
    # O (Opportunity)
    o_x = s_x
    o_y = s_y + qh + 10
    draw.rounded_rectangle([o_x, o_y, o_x + qw, o_y + qh], radius=10, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
    draw_pill_badge(draw, left_x=o_x + 14, cy=o_y + 24, text="Opportunity (기회)", font=get_font(10, 'bold'), theme='blue', has_dot=False, pad_x=8, height=22)
    o_points = [
        "• 변동성 장세 속 개인 물타기 수요 84.7%",
        "• 복잡한 수식 없는 직관적 모바일 도구 요구",
        "• 1인 가구 및 주린이 투자자의 리스크 관리 니즈"
    ]
    dy = o_y + 48
    for p in o_points:
        draw.text((o_x + 14, dy), p, font=get_font(11.5, 'medium'), fill=(30, 64, 175))
        dy += 24
        
    # T (Threat)
    t_x = w_x
    t_y = o_y
    draw.rounded_rectangle([t_x, t_y, t_x + qw, t_y + qh], radius=10, fill=(254, 243, 199), outline=(253, 230, 138), width=1)
    draw_pill_badge(draw, left_x=t_x + 14, cy=t_y + 24, text="Threat (위협)", font=get_font(10, 'bold'), theme='amber', has_dot=False, pad_x=8, height=22)
    t_points = [
        "• 대형 증권사의 유사 퀀트 기능 복제",
        "• 급격한 하락장 장기화로 투자 심리 위축",
        "• 타사 금융 앱의 무료 광고 공세"
    ]
    dy = t_y + 48
    for p in t_points:
        draw.text((t_x + 14, dy), p, font=get_font(11.5, 'medium'), fill=(146, 64, 14))
        dy += 24
        
    # Right: 3 Strategic Outcome Cards (Reference Image 1 Style)
    strat_x = 100 + swot_w + 30
    strat_w = 860
    strat_h = 415
    draw.rounded_rectangle([strat_x, b_y, strat_x + strat_w, b_y + strat_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    draw.text((strat_x + 25, b_y + 20), "STRATEGIC OUTCOMES : 도출된 3대 제품 혁신 전략", font=get_font(15, 'bold'), fill=(15, 23, 42))
    draw.line([(strat_x + 25, b_y + 48), (strat_x + strat_w - 25, b_y + 48)], fill=(241, 245, 249), width=1)
    
    outcomes = [
        ("01", "비중 왜곡 방지 및 65% 예수금 안전선 사수",
         "AS-IS : 4차까지 무계획 추가 매수로 계좌 예수금 78%가 한 종목에 묶이는 비극",
         "TO-BE : 실시간 예수금 한도 가드 & 차수별 방어선 시각화로 비중 왜곡 원천 차단",
         "blue"),
        ("02", "긴박한 호가 변동 속 타이핑 피로 제로화",
         "AS-IS : 급락 순간 키보드로 가격을 치다 지지선을 놓치고 -6.4% 추가 손실",
         "TO-BE : 0.2초 음성 도크 & ±5% 원터치 프리셋 칩으로 4.2초 만에 파라미터 세팅",
         "cyan"),
        ("03", "손익분기점 탈출을 위한 닫힌 형식 퀀트 역산",
         "AS-IS : 원금 회복을 위해 몇 주를 사야 하는지 계산할 수 없어 맹목적 매수",
         "TO-BE : 폐쇄형(Closed-Form) 퀀트 역산 엔진으로 목표 탈출가 도달 수량 0ms 즉각 산출",
         "green")
    ]
    
    sy_out = b_y + 65
    for num, o_title, o_asis, o_tobe, o_theme in outcomes:
        draw.rounded_rectangle([strat_x + 25, sy_out, strat_x + strat_w - 25, sy_out + 102], radius=12, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        
        # Number Badge
        draw.rounded_rectangle([strat_x + 40, sy_out + 14, strat_x + 68, sy_out + 38], radius=6, fill=(15, 23, 42))
        draw.text((strat_x + 46, sy_out + 17), num, font=get_font(12, 'bold'), fill=(255, 255, 255))
        draw.text((strat_x + 78, sy_out + 16), o_title, font=get_font(14, 'bold'), fill=(15, 23, 42))
        
        # As-is line
        draw.text((strat_x + 40, sy_out + 46), o_asis, font=get_font(11.5, 'regular'), fill=(220, 38, 38))
        # To-be line
        draw.text((strat_x + 40, sy_out + 70), o_tobe, font=get_font(11.5, 'bold'), fill=(0, 82, 255))
        
        sy_out += 114
        
    base.save(f'{OUT_DIR}/slide_02.png')
    print("SAVED diverse Slide 02 (Desk Research + Insight + SWOT Matrix + Outcomes) successfully!")

def make_slide_03():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Hairline Top/Bottom Boundaries
    draw.line([(100, 52), (1820, 52)], fill=(226, 232, 240), width=1)
    draw.line([(100, 990), (1820, 990)], fill=(226, 232, 240), width=1)
    
    # Header - Reference Image 2 Style
    draw.text((100, 75), "TARGET SEGMENTATION & COMPETITIVE BENCHMARK", font=get_font(13.5, 'bold'), fill=(0, 82, 255))
    t1_a = "타깃 세그먼트 매트릭스와 "
    t1_b = "경쟁사 벤치마킹 분석"
    font_title = get_font(36, 'bold')
    w_t1_a = draw.textlength(t1_a, font=font_title)
    draw.text((100, 110), t1_a, font=font_title, fill=(15, 23, 42))
    draw.text((100 + w_t1_a, 110), t1_b, font=font_title, fill=(0, 82, 255))
    draw.text((100, 165), "2x2 타깃 포지셔닝 매트릭스와 4대 플랫폼 벤치마크, 그리고 대표 페르소나 행동 지표", font=get_font(15.5, 'regular'), fill=(71, 85, 105))
    
    # ==============================================================
    # 1. TOP-LEFT: 2x2 Target Segmentation Matrix (Reference Image 2 Style)
    # ==============================================================
    t_x = 100
    t_y = 215
    t_w = 780
    t_h = 390
    draw.rounded_rectangle([t_x, t_y, t_x + t_w, t_y + t_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    draw.text((t_x + 24, t_y + 18), "TARGET SEGMENTATION MATRIX (타깃 세그먼트 분석)", font=get_font(14, 'bold'), fill=(15, 23, 42))
    draw.text((t_x + 24, t_y + 38), "매매 빈도와 퀀트 도구 수용도에 따른 4대 투자자 유형 분류", font=get_font(11.5, 'medium'), fill=(100, 116, 139))
    
    # 2x2 Quadrant Grid
    grid_x = t_x + 110
    grid_y = t_y + 70
    grid_w = 630
    grid_h = 285
    qw = (grid_w - 16) // 2
    qh = (grid_h - 16) // 2
    
    # Axis lines & labels
    draw.line([(grid_x + qw + 8, grid_y), (grid_x + qw + 8, grid_y + grid_h)], fill=(203, 213, 225), width=2)
    draw.line([(grid_x, grid_y + qh + 8), (grid_x + grid_w, grid_y + qh + 8)], fill=(203, 213, 225), width=2)
    
    draw.text((grid_x + qw + 16, grid_y - 18), "▲ 실시간 모멘텀 (초단위)", font=get_font(10, 'bold'), fill=(0, 82, 255))
    draw.text((grid_x + qw + 16, grid_y + grid_h + 4), "▼ 적립식 장기 (월단위)", font=get_font(10, 'bold'), fill=(100, 116, 139))
    draw.text((grid_x - 75, grid_y + qh + 2), "◀ 직관/감", font=get_font(10, 'bold'), fill=(100, 116, 139))
    draw.text((grid_x + grid_w + 8, grid_y + qh + 2), "데이터/역산 ▶", font=get_font(10, 'bold'), fill=(0, 82, 255))
    
    # Quadrant 1: Top-Right (Active Momentum Quant) - CORE TARGET
    q1_x = grid_x + qw + 16
    q1_y = grid_y
    draw.rounded_rectangle([q1_x, q1_y, q1_x + qw - 8, q1_y + qh], radius=8, fill=(239, 246, 255), outline=(147, 197, 253), width=1)
    draw_pill_badge(draw, left_x=q1_x + 10, cy=q1_y + 20, text="CORE TARGET", font=get_font(9, 'bold'), theme='blue', has_dot=True, pad_x=6, height=20)
    draw.text((q1_x + 10, q1_y + 40), "실시간 모멘텀 퀀트", font=get_font(13, 'bold'), fill=(0, 82, 255))
    draw.text((q1_x + 10, q1_y + 64), "• 급변 호가 타이핑 스트레스 극심\n• 0.2초 음성 도크 & 역산 최우선 수용", font=get_font(11, 'regular'), fill=(51, 65, 85), spacing=2)
    
    # Quadrant 2: Bottom-Right (Systematic DCA Planner) - PRIMARY TARGET
    q2_x = q1_x
    q2_y = grid_y + qh + 16
    draw.rounded_rectangle([q2_x, q2_y, q2_x + qw - 8, q2_y + qh], radius=8, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
    draw_pill_badge(draw, left_x=q2_x + 10, cy=q2_y + 20, text="PRIMARY TARGET", font=get_font(9, 'bold'), theme='green', has_dot=True, pad_x=6, height=20)
    draw.text((q2_x + 10, q2_y + 40), "안정 적립식 플래너", font=get_font(13, 'bold'), fill=(5, 150, 105))
    draw.text((q2_x + 10, q2_y + 64), "• 계획적 분할 매수 및 계좌 건전성 중시\n• 65% 예수금 안전 가드 적극 활용", font=get_font(11, 'regular'), fill=(51, 65, 85), spacing=2)
    
    # Quadrant 3: Top-Left (Impulsive Scalper)
    q3_x = grid_x
    q3_y = grid_y
    draw.rounded_rectangle([q3_x, q3_y, q3_x + qw, q3_y + qh], radius=8, fill=(254, 243, 199), outline=(253, 230, 138), width=1)
    draw.text((q3_x + 12, q3_y + 14), "충동적 모멘텀 스캘퍼", font=get_font(12.5, 'bold'), fill=(180, 83, 9))
    draw.text((q3_x + 12, q3_y + 42), "• 차트 감에 의존한 뇌동매매\n• 잦은 호가 이탈 손실 경험\n• 솔루션 : 호가 프리셋 원터치 칩", font=get_font(11, 'regular'), fill=(120, 53, 15), spacing=2)
    
    # Quadrant 4: Bottom-Left (Blind Averager)
    q4_x = grid_x
    q4_y = grid_y + qh + 16
    draw.rounded_rectangle([q4_x, q4_y, q4_x + qw, q4_y + qh], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((q4_x + 12, q4_y + 14), "비이성적 맹목 매수자", font=get_font(12.5, 'bold'), fill=(71, 85, 105))
    draw.text((q4_x + 12, q4_y + 42), "• 하락할 때마다 무계획 추가 매수\n• 예수금 조기 고갈로 계좌 묶임\n• 솔루션 : 위험도 경보 및 손익분기 계산", font=get_font(11, 'regular'), fill=(71, 85, 105), spacing=2)

    # ==============================================================
    # 2. TOP-RIGHT: Competitive Benchmark Table (Reference Image 2 Style)
    # ==============================================================
    c_x = 910
    c_y = 215
    c_w = 810
    c_h = 390
    draw.rounded_rectangle([c_x, c_y, c_x + c_w, c_y + c_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    draw.text((c_x + 24, c_y + 18), "COMPETITIVE BENCHMARK (경쟁사 비교 분석)", font=get_font(14, 'bold'), fill=(15, 23, 42))
    draw.text((c_x + 24, c_y + 38), "국내 주요 솔루션 대비 스마트 DCA 계산기의 5대 핵심 차별점", font=get_font(11.5, 'medium'), fill=(100, 116, 139))
    
    # Table Header
    th_y = c_y + 65
    draw.rounded_rectangle([c_x + 16, th_y, c_x + c_w - 16, th_y + 36], radius=6, fill=(241, 245, 249))
    draw.text((c_x + 28, th_y + 10), "비교 차원 (Dimensions)", font=get_font(11.5, 'bold'), fill=(71, 85, 105))
    draw.text((c_x + 230, th_y + 10), "증권사 MTS", font=get_font(11.5, 'bold'), fill=(71, 85, 105))
    draw.text((c_x + 390, th_y + 10), "일반 계산기 웹/앱", font=get_font(11.5, 'bold'), fill=(71, 85, 105))
    
    # Highlighted smart DCA header
    draw.rounded_rectangle([c_x + 560, th_y - 4, c_x + c_w - 20, th_y + 320], radius=8, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw.rounded_rectangle([c_x + 570, th_y + 2, c_x + c_w - 30, th_y + 30], radius=5, fill=(0, 82, 255))
    draw.text((c_x + 595, th_y + 8), "SMART DCA (본 앱)", font=get_font(11.5, 'bold'), fill=(255, 255, 255))
    
    rows = [
        ("입력 방식", "단일 키패드 타이핑", "광고 팝업 지연 키패드", "0.2s 음성 도크 + 호가 칩"),
        ("연산 엔진", "사후 단순 가중평균", "1회성 수동 단일 수식", "닫힌 형식(Closed-Form) 역산"),
        ("의사결정", "단순 평가액 나열", "결과 저장 미지원", "A vs B 시뮬레이션 매트릭스"),
        ("안전 가드", "단일 종목 경고 없음", "경고 기능 없음", "65% 예수금 고갈 사전 방어"),
        ("프라이버시", "서버 공인인증 필수", "임시 세션 리셋", "100% 온디바이스 로컬 암호화")
    ]
    
    r_y = th_y + 44
    for dim, r_mts, r_app, r_smart in rows:
        draw.line([(c_x + 24, r_y), (c_x + 550, r_y)], fill=(241, 245, 249), width=1)
        draw.text((c_x + 28, r_y + 12), dim, font=get_font(12, 'bold'), fill=(15, 23, 42))
        draw.text((c_x + 230, r_y + 12), r_mts, font=get_font(11.5, 'regular'), fill=(100, 116, 139))
        draw.text((c_x + 390, r_y + 12), r_app, font=get_font(11.5, 'regular'), fill=(100, 116, 139))
        
        draw.ellipse([c_x + 580, r_y + 14, c_x + 588, r_y + 22], fill=(0, 82, 255))
        draw.text((c_x + 596, r_y + 11), r_smart, font=get_font(11.5, 'bold'), fill=(0, 82, 255))
        r_y += 48
        
    # ==============================================================
    # 3. BOTTOM: 2 PERSONA CARDS WITH BEHAVIOR SLIDERS (Image 3 Style)
    # ==============================================================
    p_y = 625
    pw = 800
    ph = 345
    
    # Persona A (김투자)
    draw.rounded_rectangle([100, p_y, 100 + pw, p_y + ph], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=128, cy=p_y + 32, text="ARCHETYPE A", font=get_font(10, 'bold'), theme='blue', has_dot=True, pad_x=10, height=26)
    draw.text((255, p_y + 22), "김투자 (34세, 적립식 직장인 투자자)", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    
    draw.text((128, p_y + 58), '"월급날마다 분할 매수하지만, 내 자금이 언제 바닥날지 늘 불안합니다."', font=get_font(13.5, 'bold'), fill=(0, 82, 255))
    
    desc_a = [
        "• 투자 성향 : 계획적 분할 매수를 원하나 모바일에서 계산 수식 관리가 어려움",
        "• 주요 고통 : 추가 매수로 인해 특정 종목 비중이 커져 포트폴리오 균형 붕괴",
        "• 핵심 목표 : 가용 현금 한도 내 최적의 손익분기 평단 도출 (5초 이내 완료)"
    ]
    dy = p_y + 84
    for d in desc_a:
        draw.text((128, dy), d, font=get_font(12, 'regular'), fill=(71, 85, 105))
        dy += 22
        
    draw.line([(128, p_y + 160), (100 + pw - 28, p_y + 160)], fill=(241, 245, 249), width=1)
    draw.text((128, p_y + 172), "BEHAVIOR SPECTRUM (투자 행동 성향 지표)", font=get_font(10.5, 'bold'), fill=(100, 116, 139))
    
    draw_behavior_slider(draw, 128, p_y + 204, 350, "매매 주기", "안정 적립", "공격 단타", 0.20, theme='blue')
    draw_behavior_slider(draw, 500, p_y + 204, 350, "자금 운용", "계획 분할", "몰빵 집중", 0.25, theme='blue')
    draw_behavior_slider(draw, 128, p_y + 250, 350, "계산 도구", "수동 암산", "퀀트 역산", 0.35, theme='blue')
    draw_behavior_slider(draw, 500, p_y + 250, 350, "모바일 긴급", "여유 조망", "초단위 긴급", 0.60, theme='blue')
    
    # Persona B (박스캘퍼)
    pb_x = 100 + pw + 20
    draw.rounded_rectangle([pb_x, p_y, pb_x + pw, p_y + ph], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=pb_x + 28, cy=p_y + 32, text="ARCHETYPE B", font=get_font(10, 'bold'), theme='amber', has_dot=True, pad_x=10, height=26)
    draw.text((pb_x + 155, p_y + 22), "박스캘퍼 (28세, 실시간 모멘텀 트레이더)", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    
    draw.text((pb_x + 28, p_y + 58), '"초 단위로 쏟아지는 급락장에서 가격을 치고 있을 여유가 없습니다."', font=get_font(13.5, 'bold'), fill=(217, 119, 6))
    
    desc_b = [
        "• 투자 성향 : 변동성 모멘텀 매매, 호가 변동에 따른 초 단위 빠른 체결",
        "• 주요 고통 : 소수점 단가 타이핑 중 호가가 이탈하여 체결 기회를 놓침",
        "• 핵심 목표 : 말 한마디로 끝나는 0.2초 음성 입력과 목표 탈출 수량 즉시 확인"
    ]
    dy = p_y + 84
    for d in desc_b:
        draw.text((pb_x + 28, dy), d, font=get_font(12, 'regular'), fill=(71, 85, 105))
        dy += 22
        
    draw.line([(pb_x + 28, p_y + 160), (pb_x + pw - 28, p_y + 160)], fill=(241, 245, 249), width=1)
    draw.text((pb_x + 28, p_y + 172), "BEHAVIOR SPECTRUM (투자 행동 성향 지표)", font=get_font(10.5, 'bold'), fill=(100, 116, 139))
    
    draw_behavior_slider(draw, pb_x + 28, p_y + 204, 350, "매매 주기", "안정 적립", "공격 단타", 0.95, theme='amber')
    draw_behavior_slider(draw, pb_x + 400, p_y + 204, 350, "자금 운용", "계획 분할", "몰빵 집중", 0.85, theme='amber')
    draw_behavior_slider(draw, pb_x + 28, p_y + 250, 350, "계산 도구", "수동 암산", "퀀트 역산", 0.85, theme='amber')
    draw_behavior_slider(draw, pb_x + 400, p_y + 250, 350, "모바일 긴급", "여유 조망", "초단위 긴급", 1.00, theme='amber')
    
    base.save(f'{OUT_DIR}/slide_03.png')
    print("SAVED diverse Slide 03 (Target 2x2 Matrix + Benchmark + Personas) successfully!")

def make_slide_04():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Hairline Boundaries
    draw.line([(100, 52), (1820, 52)], fill=(226, 232, 240), width=1)
    draw.line([(100, 990), (1820, 990)], fill=(226, 232, 240), width=1)
    
    # Header - Reference Image 4 Style
    draw.text((100, 75), "IA & SERVICE ARCHITECTURE", font=get_font(13.5, 'bold'), fill=(0, 82, 255))
    t1_a = "앞서 도출한 솔루션을 가장 효과적으로 보여주는 "
    t1_b = "정보 구조(IA) 설계"
    font_title = get_font(36, 'bold')
    w_t1_a = draw.textlength(t1_a, font=font_title)
    draw.text((100, 110), t1_a, font=font_title, fill=(15, 23, 42))
    draw.text((100 + w_t1_a, 110), t1_b, font=font_title, fill=(0, 82, 255))
    draw.text((100, 165), "자산 진단부터 0.2초 음성 도크, 닫힌 형식 역산, 리스크 감사까지 이어지는 5대 핵심 도메인 계층 구조", font=get_font(15.5, 'regular'), fill=(71, 85, 105))
    
    # Top-Right Legend: Existing vs New/Changed (Reference Image 4 Style)
    leg_x = 1240
    leg_y = 85
    # Existing pill
    draw.rounded_rectangle([leg_x, leg_y, leg_x + 22, leg_y + 12], radius=3, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
    draw.text((leg_x + 30, leg_y - 2), "기존 증권사 기본 구조", font=get_font(11, 'bold'), fill=(100, 116, 139))
    
    # New pill
    draw.rounded_rectangle([leg_x + 190, leg_y, leg_x + 212, leg_y + 12], radius=3, fill=(239, 246, 255), outline=(0, 82, 255), width=1)
    draw.text((leg_x + 220, leg_y - 2), "스마트 DCA 신규 혁신 기능", font=get_font(11, 'bold'), fill=(0, 82, 255))
    
    # LEVEL 0: ROOT NODE (Service Master Hub)
    root_x1, root_y1, root_x2, root_y2 = 680, 220, 1240, 280
    draw.rounded_rectangle([root_x1, root_y1, root_x2, root_y2], radius=14, fill=(255, 255, 255), outline=(0, 82, 255), width=2)
    draw_pill_badge(draw, root_x1 + 65, root_y1 + 30, "SERVICE HUB", font=get_font(10, 'bold'), theme='blue', has_dot=False, pad_x=8, height=24)
    draw.text((root_x1 + 125, root_y1 + 16), "SMART DCA SERVICE MASTER HUB", font=get_font(14, 'bold'), fill=(15, 23, 42))
    draw.text((root_x1 + 125, root_y1 + 38), "1초 자산 조망에서 0.2초 음성 도크, 닫힌 형식 퀀트 역산까지 무결점 연결", font=get_font(11.5, 'medium'), fill=(71, 85, 105))
    
    # Connectors
    draw.line([(960, root_y2), (960, 310)], fill=(0, 82, 255, 220), width=2)
    draw.ellipse([956, 306, 964, 314], fill=(0, 82, 255))
    
    col_centers = [260, 610, 960, 1310, 1660]
    draw.line([(col_centers[0], 310), (col_centers[-1], 310)], fill=(0, 82, 255, 160), width=2)
    for cx in col_centers:
        draw.ellipse([cx - 4, 310 - 4, cx + 4, 310 + 4], fill=(0, 82, 255))
        draw_arrow(draw, (cx, 310), (cx, 340), col=(0, 82, 255, 200), width=2, arrow_size=5)
        
    cw = 325
    cgap = 25
    cols_x = [100 + i * (cw + cgap) for i in range(5)]
    
    domains_data = [
        ("01. PORTFOLIO DASHBOARD", "포트폴리오 대시보드 (홈)", (0, 82, 255), "blue", [
            ("L2.1 자산 종합 요약", "총 투자금, 평가손익, 자산 총람", "• 1초 계좌 조망 & 환율 변환", True),
            ("L2.2 보유 포지션 카드", "종목별 평단가, 보유 수량 진단", "• 손실 종목 상단 자동 정렬", False),
            ("L2.3 AI 음성 & 호가 도크", "0.2초 음성 및 ±5%, ±10% 호가 칩", "• [NEW] 원터치 호가 주입 도크", True),
            ("L2.4 퀵 내비게이션", "엄지 조작 최적화 4대 메뉴", "• 계산기, 역산기, 리포트 이동", False)
        ]),
        ("02. DCA SIMULATOR", "물타기 계산기 (시뮬레이터)", (2, 132, 199), "cyan", [
            ("L2.1 다회차 분할 매수", "1차~N차 단계별 매수 시뮬레이션", "• 차수별 희망가, 주수 증감", False),
            ("L2.2 실시간 평단 피드백", "추가 매수 시 신규 평단 즉시 반영", "• 계좌 방어율(+%p) 무지연 연동", False),
            ("L2.3 전략 비교 매트릭스", "일괄 매수 vs 분할 매수 시나리오", "• [NEW] 손익분기 소요기간 대조", True),
            ("L2.4 시나리오 보관/인계", "검토 결과 저장 및 역산기로 전달", "• 0ms 파라미터 자동 인계", True)
        ]),
        ("03. GOAL-SEEKING INVERTER", "목표 평단가 역산기 (골시킹)", (217, 119, 6), "amber", [
            ("L2.1 손익분기점 역산", "희망 탈출 평단 도달 수량 산출", "• [NEW] 목표가 기준 필요수량 역산", True),
            ("L2.2 수학적 검증 가드", "비현실적 목표 입력 시 오류 방어", "• 실시간 적정 목표 평단 제안", True),
            ("L2.3 예수금 제약 슬라이더", "보유 현금 한도 내 최적 평단 탐색", "• 60fps 반응형 예수금 조율", True),
            ("L2.4 실행 플랜 확정", "최적 매수 플랜 요약 및 공유", "• 1-Tap 클립보드 주문 복사", False)
        ]),
        ("04. RISK AUDIT LAB", "계좌 리스크 진단실 (감사)", (16, 185, 129), "green", [
            ("L2.1 포트폴리오 비중 분석", "물타기 후 특정 종목 쏠림 가시화", "• [NEW] 자산 비중 도넛 및 HHI 지수", True),
            ("L2.2 3단계 위험도 판정", "계좌 건전성(안전/주의/위험) 가이드", "• 단일 비중 65% 초과 과밀 경보", True),
            ("L2.3 하락 스트레스 점검", "시장 추가 급락 시 계좌 충격도 점검", "• 최대 낙폭(MDD) 사전 방어", True),
            ("L2.4 종합 진단 리포트", "퀀트 진단 요약 카드 이미지 생성", "• 리포트 카드 이미지 저장/공유", False)
        ]),
        ("05. PERSONALIZATION & SETTINGS", "사용자 맞춤 환경 (설정)", (124, 58, 237), "purple", [
            ("L2.1 글로벌 통화 & 단위", "KRW, USD, JPY, EUR 및 소수점", "• 7개국어 및 기준 통화 선택", False),
            ("L2.2 거래 수수료 & 제세금", "증권사 수수료 및 거래세 감안", "• 매수/매도 수수료율 직접 지정", False),
            ("L2.3 24시간 안심 세션", "보상형 1회 시청 시 전면 무광고", "• [NEW] 24h 광고 차단 타이머", True),
            ("L2.4 로컬 프라이버시", "개인 금융 데이터 온디바이스 저장", "• 100% 로컬 암호화 및 백업", True)
        ])
    ]
    
    d_bg_map = {
        'blue':   {'header': (239, 246, 255), 'border': (191, 219, 254), 'text': (29, 78, 216),  'tag': (219, 234, 254)},
        'cyan':   {'header': (236, 254, 255), 'border': (165, 243, 252), 'text': (14, 116, 144), 'tag': (207, 250, 254)},
        'amber':  {'header': (254, 243, 199), 'border': (253, 230, 138), 'text': (180, 83, 9),   'tag': (254, 235, 180)},
        'green':  {'header': (236, 253, 245), 'border': (167, 243, 208), 'text': (5, 150, 105),  'tag': (209, 250, 229)},
        'purple': {'header': (245, 243, 255), 'border': (221, 214, 254), 'text': (124, 58, 237), 'tag': (237, 233, 254)},
    }
    
    for i, (dom_code, dom_name, d_col, d_theme, containers) in enumerate(domains_data):
        cx = cols_x[i]
        d_style = d_bg_map.get(d_theme, d_bg_map['blue'])
        
        # Level 1 Domain Header Card
        draw.rounded_rectangle([cx, 340, cx + cw, 410], radius=12, fill=d_style['header'], outline=d_style['border'], width=1)
        draw.text((cx + 14, 350), dom_code, font=get_font(10.5, 'bold'), fill=d_style['text'])
        draw.text((cx + 14, 374), dom_name, font=get_font(13.5, 'bold'), fill=(15, 23, 42))
        
        # Vertical Tree Spine
        tree_x = cx + 18
        draw.line([(tree_x, 410), (tree_x, 930)], fill=(d_col[0], d_col[1], d_col[2], 120), width=2)
        
        # 4 L2 Containers with L3 Specifications
        cy = 435
        for l2_title, l2_desc, l2_tag, is_new in containers:
            draw.line([(tree_x, cy + 24), (cx + 36, cy + 24)], fill=(d_col[0], d_col[1], d_col[2], 140), width=2)
            draw.ellipse([tree_x - 3, cy + 24 - 3, tree_x + 3, cy + 24 + 3], fill=d_col)
            
            card_x = cx + 36
            card_w = cw - 46
            
            card_bg = (255, 255, 255) if not is_new else (250, 252, 255)
            card_bd = (226, 232, 240) if not is_new else (191, 219, 254)
            draw.rounded_rectangle([card_x, cy, card_x + card_w, cy + 112], radius=10, fill=card_bg, outline=card_bd, width=1 if is_new else 1)
            
            # L2 Title & New Badge
            draw.text((card_x + 14, cy + 12), l2_title, font=get_font(13, 'bold'), fill=(15, 23, 42))
            if is_new:
                draw_pill_badge(draw, cx=card_x + card_w - 26, cy=cy + 20, text="NEW", font=get_font(8.5, 'bold'), theme='blue', has_dot=False, pad_x=6, height=18)
                
            # L2 Desc
            draw.text((card_x + 14, cy + 38), l2_desc, font=get_font(11, 'medium'), fill=(71, 85, 105))
            
            # L3 Micro Action Tag
            draw.rounded_rectangle([card_x + 10, cy + 68, card_x + card_w - 10, cy + 100], radius=6, fill=d_style['tag'], outline=(d_col[0], d_col[1], d_col[2], 100), width=1)
            draw.text((card_x + 18, cy + 76), l2_tag, font=get_font(10.5, 'bold'), fill=d_col)
            
            cy += 126
            
    base.save(f'{OUT_DIR}/slide_04.png')
    print("SAVED diverse Slide 04 (Visual Tree IA Architecture with Legend & Status) successfully!")

def make_slide_05():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Hairline Boundaries
    draw.line([(120, 100), (1800, 100)], fill=(226, 232, 240), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(226, 232, 240), width=1)
    
    # Header - Category & Conversational Typography
    draw.text((120, 75), "Flow Chart", font=get_font(15, 'bold'), fill=(0, 82, 255))
    t1_a = "쉽고 빠르게 "
    t1_b = "최적의 물타기 플랜을 계산할 수 있어요"
    font_title = get_font(36, 'bold')
    w_t1_a = draw.textlength(t1_a, font=font_title)
    draw.text((120, 110), t1_a, font=font_title, fill=(15, 23, 42))
    draw.text((120 + w_t1_a, 110), t1_b, font=font_title, fill=(0, 82, 255))
    
    draw.text((120, 165), "페르소나 김민우, 박서연의 저니맵을 바탕으로 제작된 플로우 차트입니다.", font=get_font(14, 'regular'), fill=(71, 85, 105))
    draw.text((120, 188), "프로젝트 목표에 알맞게 플로우를 구성하였으며, 뎁스를 최소화해 쉽고 빠르게 물타기 계산 및 시나리오를 도출할 수 있도록 유도했습니다.", font=get_font(14, 'regular'), fill=(71, 85, 105))
    
    # TOP-RIGHT: 플로우 차트 기호표 (Flow Chart Legend) - EXACT MATCH to Reference Image 1
    leg_x = 1320
    leg_y = 65
    leg_w = 480
    leg_h = 135
    draw.rounded_rectangle([leg_x, leg_y, leg_x + leg_w, leg_y + leg_h], radius=14, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((leg_x + 20, leg_y + 14), "플로우 차트 기호표", font=get_font(12, 'bold'), fill=(0, 82, 255))
    
    # Row 1 of Legend: 시작/끝, 판단, Yes, 화살표
    # 1. 시작/끝 (Blue filled pill)
    draw.rounded_rectangle([leg_x + 20, leg_y + 45, leg_x + 72, leg_y + 68], radius=11, fill=(0, 82, 255))
    draw.text((leg_x + 82, leg_y + 49), "시작/끝", font=get_font(10.5, 'medium'), fill=(71, 85, 105))
    
    # 2. 판단 (Diamond)
    draw_diamond(draw, cx=leg_x + 195, cy=leg_y + 56, w=32, h=22, fill=(255, 255, 255), outline=(0, 82, 255), width=1)
    draw.text((leg_x + 220, leg_y + 49), "판단", font=get_font(10.5, 'medium'), fill=(71, 85, 105))
    
    # 3. Yes (Blue dashed line with arrow)
    draw_dashed_arrow(draw, (leg_x + 300, leg_y + 56), (leg_x + 345, leg_y + 56), col=(0, 82, 255), width=2)
    draw.text((leg_x + 355, leg_y + 49), "Yes", font=get_font(10.5, 'medium'), fill=(71, 85, 105))
    
    # 4. 화살표 (Gray solid arrow)
    draw_arrow(draw, (leg_x + 400, leg_y + 56), (leg_x + 435, leg_y + 56), col=(100, 116, 139), width=2)
    draw.text((leg_x + 442, leg_y + 49), "화살표", font=get_font(10, 'medium'), fill=(71, 85, 105))
    
    # Row 2 of Legend: 프로세스, 주요 프로세스, 입력/출력, No
    # 5. 프로세스 (Rounded rect)
    draw.rounded_rectangle([leg_x + 20, leg_y + 88, leg_x + 72, leg_y + 112], radius=6, fill=(255, 255, 255), outline=(0, 82, 255), width=1)
    draw.text((leg_x + 82, leg_y + 92), "프로세스", font=get_font(10.5, 'medium'), fill=(71, 85, 105))
    
    # 6. 주요 프로세스 (Dashed rounded rect)
    draw_dashed_rounded_rect(draw, [leg_x + 140, leg_y + 88, leg_x + 195, leg_y + 112], radius=6, fill=(240, 246, 255), outline=(0, 82, 255), width=1)
    draw.text((leg_x + 205, leg_y + 92), "주요 프로세스", font=get_font(10.5, 'medium'), fill=(71, 85, 105))
    
    # 7. 입력/출력 (Parallelogram)
    draw_parallelogram(draw, cx=leg_x + 315, cy=leg_y + 100, w=40, h=24, fill=(255, 255, 255), outline=(0, 82, 255), skew=8)
    draw.text((leg_x + 342, leg_y + 92), "입력/출력", font=get_font(10.5, 'medium'), fill=(71, 85, 105))
    
    # 8. No (Pink dashed line with arrow)
    draw_dashed_arrow(draw, (leg_x + 400, leg_y + 100), (leg_x + 435, leg_y + 100), col=(244, 63, 94), width=2)
    draw.text((leg_x + 442, leg_y + 92), "No", font=get_font(10.5, 'medium'), fill=(71, 85, 105))
    
    # =========================================================
    # FLOW CHART BODY
    # =========================================================
    # Entry Sequence (Top Left-Center)
    root_x = 210
    
    # Start Pill
    draw.rounded_rectangle([root_x - 45, 226, root_x + 45, 254], radius=14, fill=(0, 82, 255))
    draw.text((root_x, 240), "Start", font=get_font(12, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # Arrow to Splash
    draw_arrow(draw, (root_x, 254), (root_x, 278), col=(147, 197, 253), width=2)
    
    # Splash Process
    draw.rounded_rectangle([root_x - 55, 278, root_x + 55, 310], radius=8, fill=(255, 255, 255), outline=(0, 82, 255), width=1)
    draw.text((root_x, 294), "Splash", font=get_font(11, 'bold'), fill=(15, 23, 42), anchor='mm')
    
    # Arrow to Onboarding Decision
    draw_arrow(draw, (root_x, 310), (root_x, 335), col=(147, 197, 253), width=2)
    
    # Decision: 최초 실행? (Diamond)
    draw_diamond(draw, cx=root_x, cy=362, w=120, h=48, fill=(255, 255, 255), outline=(0, 82, 255), width=1)
    draw.text((root_x, 362), "온보딩&튜토리얼", font=get_font(10, 'bold'), fill=(15, 23, 42), anchor='mm')
    
    # If Yes (first time) -> goes left to Onboarding Guide
    onb_x = 90
    draw_dashed_line(draw, (root_x - 60, 362), (onb_x, 362), col=(244, 63, 94), width=1)
    draw.text(((root_x - 60 + onb_x) // 2, 350), "No (미완료)", font=get_font(9, 'bold'), fill=(244, 63, 94), anchor='mm')
    draw_dashed_arrow(draw, (onb_x, 362), (onb_x, 395), col=(244, 63, 94), width=1)
    
    draw.rounded_rectangle([onb_x - 45, 395, onb_x + 45, 432], radius=8, fill=(254, 242, 242), outline=(244, 63, 94), width=1)
    draw.text((onb_x, 407), "인터랙티브", font=get_font(9.5, 'bold'), fill=(153, 27, 27), anchor='mm')
    draw.text((onb_x, 420), "온보딩 가이드", font=get_font(9, 'regular'), fill=(153, 27, 27), anchor='mm')
    
    # If Yes (already onboarded) -> directly down to Bus
    draw_dashed_line(draw, (root_x, 386), (root_x, 440), col=(0, 82, 255), width=1)
    draw.text((root_x + 35, 412), "Yes (완료)", font=get_font(9.5, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    # Connect Onboarding back to Bus
    draw_arrow(draw, (onb_x, 432), (onb_x, 440), col=(147, 197, 253), width=2)
    
    # =========================================================
    # Horizontal Distribution Bus Line at y=440
    # =========================================================
    draw.line([(onb_x, 440), (1670, 440)], fill=(147, 197, 253), width=2)
    
    # 5 Main Feature Columns
    cols = [
        ("홈 대시보드", 210, [
            ("header", "홈 (대시보드)", (239, 246, 255), (0, 82, 255)),
            ("process", "보유 자산 총괄 요약", (255, 255, 255), (0, 82, 255)),
            ("process", "최근 계산 기록 확인", (255, 255, 255), (0, 82, 255)),
            ("process", "원터치 호가 프리셋 탭", (255, 255, 255), (0, 82, 255)),
            ("key_process", "빠른 계산 진입", (240, 246, 255), (0, 82, 255)),
            ("finish", "대시보드 조망 완료", (0, 82, 255), (0, 82, 255))
        ]),
        ("물타기 계산기 (Simulator)", 560, [
            ("header", "물타기 계산기", (239, 246, 255), (0, 82, 255)),
            ("io", "보유 평단 · 수량 입력", (255, 255, 255), (0, 82, 255)),
            ("io", "추가 매수가 · 수량 입력", (255, 255, 255), (0, 82, 255)),
            ("process", "가중평균 실시간 연산", (255, 255, 255), (0, 82, 255)),
            ("decision", "목표 평단가 도달?", (255, 255, 255), (0, 82, 255)),
            ("key_process", "포트폴리오 자산 저장", (240, 246, 255), (0, 82, 255)),
            ("finish", "시뮬레이션 완료", (0, 82, 255), (0, 82, 255))
        ]),
        ("목표가 역산기 (Target DCA)", 930, [
            ("header", "목표가 역산기", (239, 246, 255), (0, 82, 255)),
            ("io", "희망 목표 평단가 입력", (255, 255, 255), (0, 82, 255)),
            ("key_process", "폐쇄형 퀀트 역산 가동", (240, 246, 255), (0, 82, 255)),
            ("io", "필요 예수금 · 수량 산출", (255, 255, 255), (0, 82, 255)),
            ("decision", "예수금 감당 가능?", (255, 255, 255), (0, 82, 255)),
            ("key_process", "1-Tap 플랜 클립보드 복사", (240, 246, 255), (0, 82, 255)),
            ("finish", "목표 역산 완료", (0, 82, 255), (0, 82, 255))
        ]),
        ("AI 음성 도크 (Voice DCA)", 1300, [
            ("header", "AI 음성 도크", (239, 246, 255), (0, 82, 255)),
            ("process", "마이크 버튼 탭", (255, 255, 255), (0, 82, 255)),
            ("io", "자연어 발화 ('15,000원에 100주')", (255, 255, 255), (0, 82, 255)),
            ("process", "온디바이스 STT 파싱", (255, 255, 255), (0, 82, 255)),
            ("key_process", "수치 및 종목 자동 매핑", (240, 246, 255), (0, 82, 255)),
            ("key_process", "시뮬레이터 파라미터 주입", (240, 246, 255), (0, 82, 255)),
            ("finish", "음성 계산 완료", (0, 82, 255), (0, 82, 255))
        ]),
        ("포트폴리오 & 글로벌 설정", 1670, [
            ("header", "포트폴리오 & 설정", (239, 246, 255), (0, 82, 255)),
            ("key_process", "SQLite 로컬 암호화 저장", (240, 246, 255), (0, 82, 255)),
            ("process", "종목별 손익 · 비중 차트", (255, 255, 255), (0, 82, 255)),
            ("process", "10개 글로벌 언어 선택", (255, 255, 255), (0, 82, 255)),
            ("process", "다크 / 라이트 모드 설정", (255, 255, 255), (0, 82, 255)),
            ("process", "개인정보처리방침 열람", (255, 255, 255), (0, 82, 255)),
            ("finish", "설정 적용 완료", (0, 82, 255), (0, 82, 255))
        ])
    ]
    
    box_w = 210
    box_h = 38
    start_y = 475
    
    for c_title, cx, nodes in cols:
        # Arrow down from bus line
        draw_arrow(draw, (cx, 440), (cx, start_y), col=(147, 197, 253), width=2)
        
        curr_y = start_y
        for i, (ntype, label, bg, border) in enumerate(nodes):
            if ntype == "header":
                draw.rounded_rectangle([cx - box_w // 2, curr_y, cx + box_w // 2, curr_y + box_h], radius=8, fill=bg, outline=border, width=2)
                draw.text((cx, curr_y + box_h // 2), label, font=get_font(12, 'bold'), fill=border, anchor='mm')
                next_y = curr_y + box_h + 24
                draw_arrow(draw, (cx, curr_y + box_h), (cx, next_y), col=(147, 197, 253), width=2)
                curr_y = next_y
            elif ntype == "process":
                draw.rounded_rectangle([cx - box_w // 2, curr_y, cx + box_w // 2, curr_y + box_h], radius=6, fill=bg, outline=border, width=1)
                draw.text((cx, curr_y + box_h // 2), label, font=get_font(11, 'medium'), fill=(15, 23, 42), anchor='mm')
                next_y = curr_y + box_h + 24
                draw_arrow(draw, (cx, curr_y + box_h), (cx, next_y), col=(147, 197, 253), width=2)
                curr_y = next_y
            elif ntype == "key_process":
                draw_dashed_rounded_rect(draw, [cx - box_w // 2, curr_y, cx + box_w // 2, curr_y + box_h], radius=6, fill=bg, outline=border, width=1)
                draw.text((cx, curr_y + box_h // 2), label, font=get_font(11, 'bold'), fill=border, anchor='mm')
                next_y = curr_y + box_h + 24
                draw_arrow(draw, (cx, curr_y + box_h), (cx, next_y), col=(147, 197, 253), width=2)
                curr_y = next_y
            elif ntype == "io":
                draw_parallelogram(draw, cx=cx, cy=curr_y + box_h // 2, w=box_w, h=box_h, fill=(255, 255, 255), outline=border, skew=10)
                draw.text((cx, curr_y + box_h // 2), label, font=get_font(10.5, 'medium'), fill=(15, 23, 42), anchor='mm')
                next_y = curr_y + box_h + 24
                draw_arrow(draw, (cx, curr_y + box_h), (cx, next_y), col=(147, 197, 253), width=2)
                curr_y = next_y
            elif ntype == "decision":
                dh = 46
                draw_diamond(draw, cx=cx, cy=curr_y + dh // 2, w=box_w, h=dh, fill=(255, 255, 255), outline=border, width=1)
                draw.text((cx, curr_y + dh // 2), label, font=get_font(10.5, 'bold'), fill=border, anchor='mm')
                next_y = curr_y + dh + 24
                draw_arrow(draw, (cx, curr_y + dh), (cx, next_y), col=(147, 197, 253), width=2)
                curr_y = next_y
            elif ntype == "finish":
                draw.rounded_rectangle([cx - 70, curr_y, cx + 70, curr_y + 32], radius=16, fill=(0, 82, 255))
                draw.text((cx, curr_y + 16), label, font=get_font(11, 'bold'), fill=(255, 255, 255), anchor='mm')
                
    base.save(f'{OUT_DIR}/slide_05.png')
    print("SAVED slide_05.png (Enterprise Flow Chart with Symbol Legend)")


def make_slide_06():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Hairline Boundaries
    draw.line([(120, 100), (1800, 100)], fill=(226, 232, 240), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(226, 232, 240), width=1)
    
    # Header - Reference Image 2 Style
    draw.text((120, 75), "Wireframe & Ui components", font=get_font(15, 'bold'), fill=(0, 82, 255))
    draw.text((120, 110), "박스 형태를 모티브로, 전체적으로 둥근 박스 형태의 디자인을 사용했습니다.", font=get_font(32, 'bold'), fill=(15, 23, 42))
    draw.text((120, 160), "인체공학적 조작 반경과 비정상 입력 사전 가드로 설계된 모바일 와이어프레임 및 UI 컴포넌트 시스템", font=get_font(14, 'regular'), fill=(71, 85, 105))
    
    # UPPER SECTION: 3 WIREFRAME & UI COMPONENT COLUMNS (y=200 to y=550)
    col_y = 200
    col_h = 350
    
    # Column 1: UI Components & Stepper Atoms (Left)
    c1_x = 120
    c1_w = 480
    draw.rounded_rectangle([c1_x, col_y, c1_x + c1_w, col_y + col_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, cx=c1_x + 95, cy=col_y + 25, text="UI COMPONENTS", font=get_font(10, 'bold'), theme='cyan', has_dot=False, dark_mode=False, pad_x=10, height=26)
    draw.text((c1_x + 24, col_y + 55), "인터랙티브 스텝퍼 & 퀀트 뱃지", font=get_font(16, 'bold'), fill=(15, 23, 42))
    
    # Stepper Component Mockup
    sy = col_y + 90
    draw.rounded_rectangle([c1_x + 24, sy, c1_x + c1_w - 24, sy + 60], radius=12, fill=(248, 250, 252), outline=(203, 213, 225), width=1)
    draw.rounded_rectangle([c1_x + 36, sy + 10, c1_x + 76, sy + 50], radius=8, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((c1_x + 56, sy + 30), "-", font=get_font(18, 'bold'), fill=(0, 82, 255), anchor='mm')
    draw.text((c1_x + c1_w // 2, sy + 30), "100 주 (수량 조절)", font=get_font(14, 'bold'), fill=(15, 23, 42), anchor='mm')
    draw.rounded_rectangle([c1_x + c1_w - 76, sy + 10, c1_x + c1_w - 36, sy + 50], radius=8, fill=(0, 82, 255))
    draw.text((c1_x + c1_w - 56, sy + 30), "+", font=get_font(18, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # Preset Chips Row
    py = sy + 75
    draw.text((c1_x + 24, py), "빠른 호가 선택 프리셋 칩", font=get_font(12, 'bold'), fill=(71, 85, 105))
    p_chips = [("+10%", "blue"), ("+20%", "blue"), ("-5%", "red"), ("전액", "green")]
    ch_x = c1_x + 24
    for chip_txt, chip_theme in p_chips:
        draw_pill_badge(draw, cx=ch_x + 40, cy=py + 35, text=chip_txt, font=get_font(11, 'bold'), theme=chip_theme, has_dot=False, dark_mode=False, pad_x=12, height=30)
        ch_x += 105
        
    # Price Tag & Metric Card
    my = py + 75
    draw.rounded_rectangle([c1_x + 24, my, c1_x + c1_w - 24, my + 80], radius=12, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((c1_x + 40, my + 18), "예상 방어 평단가", font=get_font(11, 'bold'), fill=(0, 82, 255))
    draw.text((c1_x + 40, my + 44), "42,350 원", font=get_num_font(20, 'bold'), fill=(15, 23, 42))
    draw_pill_badge(draw, cx=c1_x + c1_w - 85, cy=my + 40, text="-18.4% 절감", font=get_font(11, 'bold'), theme='green', has_dot=True, dark_mode=False, pad_x=10, height=28)
    
    # Column 2: Mobile Wireframe Chassis (Center)
    c2_x = 640
    c2_w = 460
    draw.rounded_rectangle([c2_x, col_y, c2_x + c2_w, col_y + col_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, cx=c2_x + 115, cy=col_y + 25, text="THUMB-ZONE WIREFRAME", font=get_font(10, 'bold'), theme='blue', has_dot=False, dark_mode=False, pad_x=10, height=26)
    
    # Phone Frame Miniature
    pw = 220
    ph = 270
    px = c2_x + (c2_w - pw) // 2
    py_phone = col_y + 55
    draw.rounded_rectangle([px, py_phone, px + pw, py_phone + ph], radius=18, fill=(248, 250, 252), outline=(15, 23, 42), width=2)
    # Notch
    draw.rounded_rectangle([px + pw // 2 - 25, py_phone + 6, px + pw // 2 + 25, py_phone + 14], radius=4, fill=(15, 23, 42))
    # Top Card
    draw.rounded_rectangle([px + 12, py_phone + 24, px + pw - 12, py_phone + 85], radius=8, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((px + 20, py_phone + 32), "계좌 총 평가손익", font=get_font(8.5, 'regular'), fill=(100, 116, 139))
    draw.text((px + 20, py_phone + 48), "-16.7%", font=get_num_font(14, 'bold'), fill=(220, 38, 38))
    # Stepper Input in Phone
    draw.rounded_rectangle([px + 12, py_phone + 95, px + pw - 12, py_phone + 155], radius=8, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((px + 20, py_phone + 104), "추가 매수 수량 조절", font=get_font(8.5, 'bold'), fill=(15, 23, 42))
    # Thumb Zone Action Button
    draw.rounded_rectangle([px + 12, py_phone + 215, px + pw - 12, py_phone + 255], radius=10, fill=(0, 82, 255))
    draw.text((px + pw // 2, py_phone + 235), "⚡ 0.2초 음성 도크", font=get_font(10, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # Column 3: Ergonomic Breakdown Callouts (Right)
    c3_x = 1140
    c3_w = 660
    draw.rounded_rectangle([c3_x, col_y, c3_x + c3_w, col_y + col_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, cx=c3_x + 115, cy=col_y + 25, text="ERGONOMIC SPEC", font=get_font(10, 'bold'), theme='purple', has_dot=False, dark_mode=False, pad_x=10, height=26)
    draw.text((c3_x + 24, col_y + 55), "인체공학적 조작성 및 오류 방지 설계", font=get_font(16, 'bold'), fill=(15, 23, 42))
    
    callouts = [
        ("① Fitts' Law Thumb-Zone 48dp", "한 손 파지 시 엄지손가락이 닿는 하단 120dp 반경 내 주요 액션 버튼 배치"),
        ("② 0.2초 음성 도크 시트 연동", "급변하는 호가 속 키패드 8자리 소수점 타이핑 피로도를 78% 줄이는 원터치 마이크"),
        ("③ 비정상 입력 사전 가드 엔진", "도달 불가한 목표 평단가 입력 시 즉각적인 햅틱 경고 및 최적 분할 매수 대안 제시"),
        ("④ 1-Tap 무손실 파라미터 인계", "역산으로 도출된 수치를 시뮬레이터로 0ms 자동 주입하여 재입력 오류 원천 방지")
    ]
    cy_sub = col_y + 90
    for c_title, c_desc in callouts:
        draw.rounded_rectangle([c3_x + 24, cy_sub, c3_x + c3_w - 24, cy_sub + 52], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((c3_x + 38, cy_sub + 12), c_title, font=get_font(12, 'bold'), fill=(0, 82, 255))
        draw.text((c3_x + 38, cy_sub + 30), c_desc, font=get_font(11, 'regular'), fill=(71, 85, 105))
        cy_sub += 62
        
    # =========================================================
    # LOWER SECTION: DESIGN CONCEPT (Naming & Symbol) - EXACT MATCH to Reference Image 2
    # =========================================================
    sec_y = 575
    draw.text((120, sec_y), "Design Concept", font=get_font(24, 'bold'), fill=(15, 23, 42))
    
    card_y = sec_y + 40
    card_h = 340
    
    # Left Card: Naming
    n_x = 120
    n_w = 780
    draw.rounded_rectangle([n_x, card_y, n_x + n_w, card_y + card_h], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((n_x + 32, card_y + 28), "Naming", font=get_font(16, 'bold'), fill=(0, 82, 255))
    draw.text((n_x + 32, card_y + 56), "스마트 물타기는 복잡하고 불안했던 투자를 \"스마트하게 지킨다\"는 메시지를 담았습니다.", font=get_font(13.5, 'regular'), fill=(71, 85, 105))
    
    # Big Typography Display: Smart DCA [스마트 물타기]
    ty_logo = card_y + 105
    draw.text((n_x + 32, ty_logo), "Smart DCA", font=get_font(46, 'black'), fill=(0, 82, 255))
    draw.text((n_x + 320, ty_logo + 10), "[스마트 물타기]", font=get_font(28, 'bold'), fill=(15, 23, 42))
    
    # Detailed Description
    desc_n = (
        "기존 금융 시장에서 공포와 감정에 휩쓸려 무계획하게 행해지던 '물타기(Dollar Cost Averaging)'를 "
        "수학적 가중평균과 폐쇄형 역산 알고리즘으로 '스마트(Smart)'하게 전환하여, "
        "감정이 아닌 객관적 시나리오로 자산을 지킨다는 핵심 메시지를 담았습니다.\n\n"
        "• Smart : 폐쇄형 퀀트 역산 엔진 & 0.2초 온디바이스 음성 AI 파싱\n"
        "• DCA : 분할 매수를 통한 리스크 헷지 및 평단가 방어 철학"
    )
    d_lines = desc_n.split('\n')
    dy = ty_logo + 70
    for line in d_lines:
        draw.text((n_x + 32, dy), line, font=get_font(12, 'regular'), fill=(71, 85, 105))
        dy += 22
        
    # Right Card: Symbol
    s_x = 940
    s_w = 860
    draw.rounded_rectangle([s_x, card_y, s_x + s_w, card_y + card_h], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((s_x + 32, card_y + 28), "Symbol", font=get_font(16, 'bold'), fill=(0, 82, 255))
    
    # App Icon Squircle Mockup
    icon_path = "assets/app_icon_clean_squircle.png"
    if not os.path.exists(icon_path):
        icon_path = "assets/app_icon.png"
        
    ix = s_x + 40
    iy = card_y + 80
    isize = 140
    if os.path.exists(icon_path):
        try:
            icon_img = Image.open(icon_path).convert('RGBA')
            icon_img = icon_img.resize((isize, isize), Image.Resampling.LANCZOS)
            # Create drop shadow
            shadow = Image.new('RGBA', (isize + 24, isize + 24), (0, 0, 0, 0))
            s_draw = ImageDraw.Draw(shadow)
            s_draw.rounded_rectangle([12, 12, isize + 12, isize + 12], radius=32, fill=(0, 0, 0, 45))
            shadow = shadow.filter(ImageFilter.GaussianBlur(6))
            base.paste(shadow, (ix - 12, iy - 6), shadow)
            base.paste(icon_img, (ix, iy), icon_img)
        except Exception as e:
            draw.rounded_rectangle([ix, iy, ix + isize, iy + isize], radius=32, fill=(0, 82, 255))
    else:
        draw.rounded_rectangle([ix, iy, ix + isize, iy + isize], radius=32, fill=(0, 82, 255))
        
    # Symbol Text
    tx_sym = ix + isize + 36
    draw.text((tx_sym, card_y + 75), "“골든 크로스와 U자형 반등”이라는 서비스 네임에 맞추어", font=get_font(14, 'bold'), fill=(15, 23, 42))
    draw.text((tx_sym, card_y + 98), "평단가를 낮춰 반등을 이끄는 형태로 심볼을 디자인했습니다.", font=get_font(14, 'bold'), fill=(0, 82, 255))
    
    desc_s = (
        "하향 곡선을 그리던 평균 단가가 추가 매수를 통해 점진적으로 낮아지며\n"
        "주가 상승 반등 곡선과 교차(Golden Cross)하는 퀀트 모티프를\n"
        "기하학적 곡면 스퀘어클(Squircle) 심볼로 시각화했습니다.\n\n"
        "• Squircle Frame : iOS 및 Android 표준 스토어 규격 준수\n"
        "• Blue Gradient : 금융 신뢰를 상징하는 시그니처 퀀트 블루 팔레트"
    )
    s_lines = desc_s.split('\n')
    sy_desc = card_y + 145
    for line in s_lines:
        draw.text((tx_sym, sy_desc), line, font=get_font(12, 'regular'), fill=(71, 85, 105))
        sy_desc += 22

    base.save(f'{OUT_DIR}/slide_06.png')
    print("SAVED slide_06.png (Wireframe & UI components with Design Concept)")


# ==============================================================
# SLIDE 07: WhatNow-Style Dark Theme Design System (Reference Images 3 & 4)
# ==============================================================


def make_slide_07():
    # Deep Dark Navy Background
    base = Image.new('RGBA', (W, H), (17, 22, 34, 255))
    draw = ImageDraw.Draw(base)
    
    # Hairline Top/Bottom Boundaries in Dark Accent
    draw.line([(120, 90), (1800, 90)], fill=(38, 50, 72), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(38, 50, 72), width=1)
    
    # Header - Category & Giant Italic Title (Reference Image 3 Style)
    draw.text((120, 68), "07 DESIGN SYSTEM | UI COMPONENT ARCHITECTURE", font=get_font(13, 'bold'), fill=(0, 210, 255))
    draw.text((120, 100), "Design System", font=get_font(46, 'black'), fill=(255, 255, 255))
    draw.text((120, 160), "급박한 시장 환경에서도 직관적인 시각 인지성과 조작 안정성을 제공하는 스마트 물타기 계산기만의 UI 디자인 시스템을 제작했습니다.", font=get_font(15, 'regular'), fill=(148, 163, 184))
    
    # 8 MODULAR DARK CONTAINER CARDS (WhatNow Reference Style)
    card_bg = (24, 32, 48)
    card_border = (42, 54, 78)
    inner_dark = (17, 22, 34)
    
    # -------------------------------------------------------------
    # 1. Bottom app bar (Top Left)
    # -------------------------------------------------------------
    b1_x = 120
    b1_y = 210
    b1_w = 520
    b1_h = 190
    draw.rounded_rectangle([b1_x, b1_y, b1_x + b1_w, b1_y + b1_h], radius=16, fill=card_bg, outline=card_border, width=1)
    draw.text((b1_x + 24, b1_y + 16), "Bottom app bar", font=get_font(12, 'bold'), fill=(148, 163, 184))
    
    # Bottom Bar Mockup 1
    bar_y1 = b1_y + 44
    draw.rounded_rectangle([b1_x + 20, bar_y1, b1_x + b1_w - 20, bar_y1 + 54], radius=10, fill=inner_dark, outline=(38, 50, 72), width=1)
    draw.text((b1_x + 45, bar_y1 + 18), "🏠", font=get_font(16, 'regular'), fill=(255, 255, 255))
    draw.text((b1_x + 95, bar_y1 + 18), "🔔", font=get_font(16, 'regular'), fill=(255, 255, 255))
    draw.text((b1_x + 145, bar_y1 + 18), "⚙️", font=get_font(16, 'regular'), fill=(255, 255, 255))
    # Blue Button on right
    draw.rounded_rectangle([b1_x + b1_w - 150, bar_y1 + 8, b1_x + b1_w - 32, bar_y1 + 46], radius=8, fill=(0, 82, 255))
    draw.text((b1_x + b1_w - 91, bar_y1 + 27), "+ Button", font=get_font(12, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # Status Banner Mockup
    bar_y2 = bar_y1 + 68
    draw.rounded_rectangle([b1_x + 20, bar_y2, b1_x + b1_w - 20, bar_y2 + 50], radius=10, fill=inner_dark, outline=(38, 50, 72), width=1)
    draw.text((b1_x + 36, bar_y2 + 15), "🌟", font=get_font(14, 'regular'), fill=(255, 255, 255))
    draw.text((b1_x + 65, bar_y2 + 12), "실시간 퀀트 엔진 가동 중!", font=get_font(11.5, 'bold'), fill=(255, 255, 255))
    draw.text((b1_x + 65, bar_y2 + 28), "0.2초 초고속 역산 모드", font=get_font(10, 'regular'), fill=(148, 163, 184))
    draw.text((b1_x + b1_w - 40, bar_y2 + 25), "›", font=get_font(16, 'bold'), fill=(148, 163, 184), anchor='mm')
    
    # -------------------------------------------------------------
    # 2. Header (Top Center)
    # -------------------------------------------------------------
    b2_x = 670
    b2_y = 210
    b2_w = 540
    b2_h = 190
    draw.rounded_rectangle([b2_x, b2_y, b2_x + b2_w, b2_y + b2_h], radius=16, fill=card_bg, outline=card_border, width=1)
    draw.text((b2_x + 24, b2_y + 16), "Header", font=get_font(12, 'bold'), fill=(148, 163, 184))
    
    # Header Style A
    h_y1 = b2_y + 44
    draw.rounded_rectangle([b2_x + 20, h_y1, b2_x + b2_w - 20, h_y1 + 40], radius=8, fill=(255, 255, 255))
    draw.text((b2_x + 36, h_y1 + 12), "←  Title", font=get_font(13, 'bold'), fill=(15, 23, 42))
    draw.text((b2_x + b2_w - 90, h_y1 + 12), "🔗   📊   ⋮", font=get_font(11, 'bold'), fill=(15, 23, 42))
    
    # Header Style B
    h_y2 = h_y1 + 48
    draw.rounded_rectangle([b2_x + 20, h_y2, b2_x + b2_w - 20, h_y2 + 40], radius=8, fill=(255, 255, 255))
    draw.text((b2_x + 36, h_y2 + 12), "Title", font=get_font(13, 'bold'), fill=(15, 23, 42))
    draw.text((b2_x + b2_w - 90, h_y2 + 12), "🔗   📊   ⋮", font=get_font(11, 'bold'), fill=(15, 23, 42))
    
    # Header Style C
    h_y3 = h_y2 + 48
    draw.rounded_rectangle([b2_x + 20, h_y3, b2_x + b2_w - 20, h_y3 + 40], radius=8, fill=(255, 255, 255))
    draw.text((b2_x + 36, h_y3 + 12), "←  Title", font=get_font(13, 'bold'), fill=(15, 23, 42))
    draw.rounded_rectangle([b2_x + b2_w - 110, h_y3 + 7, b2_x + b2_w - 32, h_y3 + 33], radius=6, fill=(15, 23, 42))
    draw.text((b2_x + b2_w - 71, h_y3 + 20), "+ Button", font=get_font(10.5, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # -------------------------------------------------------------
    # 3. Toast Bar (Top Right)
    # -------------------------------------------------------------
    b3_x = 1240
    b3_y = 210
    b3_w = 560
    b3_h = 190
    draw.rounded_rectangle([b3_x, b3_y, b3_x + b3_w, b3_y + b3_h], radius=16, fill=card_bg, outline=card_border, width=1)
    draw.text((b3_x + 24, b3_y + 16), "Toast Bar", font=get_font(12, 'bold'), fill=(148, 163, 184))
    
    # Toast 1: with arrow
    t_y1 = b3_y + 44
    draw.rounded_rectangle([b3_x + 20, t_y1, b3_x + b3_w - 20, t_y1 + 40], radius=8, fill=(255, 255, 255))
    draw.text((b3_x + 36, t_y1 + 12), "4개 퀀트 파라미터가 0ms 무손실 인계되었습니다.", font=get_font(11.5, 'medium'), fill=(15, 23, 42))
    draw.text((b3_x + b3_w - 40, t_y1 + 12), "↗", font=get_font(14, 'bold'), fill=(15, 23, 42))
    
    # Toast 2: with View action
    t_y2 = t_y1 + 48
    draw.rounded_rectangle([b3_x + 20, t_y2, b3_x + b3_w - 20, t_y2 + 40], radius=8, fill=(255, 255, 255))
    draw.text((b3_x + 36, t_y2 + 12), "온디바이스 SQLite에 안전하게 암호화 저장되었습니다.", font=get_font(11.5, 'medium'), fill=(15, 23, 42))
    draw.text((b3_x + b3_w - 55, t_y2 + 13), "View", font=get_font(11.5, 'bold'), fill=(0, 82, 255))
    
    # Toast 3: basic notice
    t_y3 = t_y2 + 48
    draw.rounded_rectangle([b3_x + 20, t_y3, b3_x + b3_w - 20, t_y3 + 40], radius=8, fill=(255, 255, 255))
    draw.text((b3_x + 36, t_y3 + 12), "초고속 0.2초 음성 인식 엔진이 활성화되었습니다.", font=get_font(11.5, 'medium'), fill=(15, 23, 42))
    
    # -------------------------------------------------------------
    # 4. Button & Presets (Middle Left)
    # -------------------------------------------------------------
    b4_x = 120
    b4_y = 425
    b4_w = 520
    b4_h = 245
    draw.rounded_rectangle([b4_x, b4_y, b4_x + b4_w, b4_y + b4_h], radius=16, fill=card_bg, outline=card_border, width=1)
    draw.text((b4_x + 24, b4_y + 16), "Button", font=get_font(12, 'bold'), fill=(148, 163, 184))
    
    # Row 1: Circular FAB & Pill
    btn_y1 = b4_y + 44
    draw.ellipse([b4_x + 24, btn_y1, b4_x + 64, btn_y1 + 40], fill=inner_dark, outline=(38, 50, 72), width=1)
    draw.text((b4_x + 44, btn_y1 + 20), "+", font=get_font(16, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    draw.rounded_rectangle([b4_x + 80, btn_y1, b4_x + 160, btn_y1 + 40], radius=20, fill=(255, 255, 255))
    draw.text((b4_x + 120, btn_y1 + 20), "+", font=get_font(16, 'bold'), fill=(15, 23, 42), anchor='mm')
    
    draw.rounded_rectangle([b4_x + 180, btn_y1, b4_x + b4_w - 24, btn_y1 + 40], radius=10, fill=inner_dark, outline=(38, 50, 72), width=1)
    draw.text((b4_x + 330, btn_y1 + 20), "+ Button", font=get_font(12, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # Row 2: Standard Buttons
    btn_y2 = btn_y1 + 52
    draw.rounded_rectangle([b4_x + 24, btn_y2, b4_x + 160, btn_y2 + 40], radius=10, fill=inner_dark, outline=(38, 50, 72), width=1)
    draw.text((b4_x + 92, btn_y2 + 20), "Button", font=get_font(12, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    draw.rounded_rectangle([b4_x + 180, btn_y2, b4_x + b4_w - 24, btn_y2 + 40], radius=10, fill=inner_dark, outline=(38, 50, 72), width=1)
    draw.text((b4_x + 330, btn_y2 + 20), "Button", font=get_font(12, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # Row 3: Preset Chips (Quick Action)
    btn_y3 = btn_y2 + 52
    draw.text((b4_x + 24, btn_y3), "호가 프리셋 칩 (Quick Presets)", font=get_font(11, 'bold'), fill=(148, 163, 184))
    chip_y = btn_y3 + 22
    ch_x = b4_x + 24
    for txt, col in [("+10%", (0, 82, 255)), ("+20%", (0, 82, 255)), ("-5%", (220, 38, 38)), ("전액 매수", (16, 185, 129))]:
        draw.rounded_rectangle([ch_x, chip_y, ch_x + 105, chip_y + 32], radius=8, fill=inner_dark, outline=col, width=1)
        draw.text((ch_x + 52, chip_y + 16), txt, font=get_font(11, 'bold'), fill=col, anchor='mm')
        ch_x += 120
        
    # -------------------------------------------------------------
    # 5. Toggle & Segmented Tabs (Middle Center)
    # -------------------------------------------------------------
    b5_x = 670
    b5_y = 425
    b5_w = 540
    b5_h = 245
    draw.rounded_rectangle([b5_x, b5_y, b5_x + b5_w, b5_y + b5_h], radius=16, fill=card_bg, outline=card_border, width=1)
    draw.text((b5_x + 24, b5_y + 16), "Toggle", font=get_font(12, 'bold'), fill=(148, 163, 184))
    
    # Switches
    tog_y1 = b5_y + 44
    # Switch Off
    draw.rounded_rectangle([b5_x + 120, tog_y1, b5_x + 170, tog_y1 + 28], radius=14, fill=(255, 255, 255))
    draw.ellipse([b5_x + 122, tog_y1 + 2, b5_x + 146, tog_y1 + 26], fill=(15, 23, 42))
    # Switch On
    draw.rounded_rectangle([b5_x + 190, tog_y1, b5_x + 240, tog_y1 + 28], radius=14, fill=(99, 102, 241))
    draw.ellipse([b5_x + 214, tog_y1 + 2, b5_x + 238, tog_y1 + 26], fill=(255, 255, 255))
    
    # Segmented Control 1 (Active Purple / Inactive Gray)
    seg_y1 = tog_y1 + 45
    draw.rounded_rectangle([b5_x + 60, seg_y1, b5_x + b5_w - 60, seg_y1 + 44], radius=22, fill=(255, 255, 255))
    draw.rounded_rectangle([b5_x + 63, seg_y1 + 3, b5_x + 270, seg_y1 + 41], radius=19, fill=(99, 102, 241))
    draw.text((b5_x + 166, seg_y1 + 22), "예정된 시나리오", font=get_font(11.5, 'bold'), fill=(255, 255, 255), anchor='mm')
    draw.text((b5_x + 360, seg_y1 + 22), "지난 계산 기록", font=get_font(11.5, 'medium'), fill=(100, 116, 139), anchor='mm')
    
    # Segmented Control 2 (Currency Pills: KRW vs USD)
    seg_y2 = seg_y1 + 56
    draw.rounded_rectangle([b5_x + 60, seg_y2, b5_x + b5_w - 60, seg_y2 + 44], radius=22, fill=(255, 255, 255))
    draw.rounded_rectangle([b5_x + 270, seg_y2 + 3, b5_x + b5_w - 63, seg_y2 + 41], radius=19, fill=(99, 102, 241))
    draw.text((b5_x + 166, seg_y2 + 22), "원화 (KRW ₩)", font=get_font(11.5, 'medium'), fill=(100, 116, 139), anchor='mm')
    draw.text((b5_x + 360, seg_y2 + 22), "달러 (USD $)", font=get_font(11.5, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # -------------------------------------------------------------
    # 6. Card (Middle Right)
    # -------------------------------------------------------------
    b6_x = 1240
    b6_y = 425
    b6_w = 560
    b6_h = 245
    draw.rounded_rectangle([b6_x, b6_y, b6_x + b6_w, b6_y + b6_h], radius=16, fill=card_bg, outline=card_border, width=1)
    draw.text((b6_x + 24, b6_y + 16), "Card", font=get_font(12, 'bold'), fill=(148, 163, 184))
    
    # Card 1: Metric Gauge
    mc_y = b6_y + 44
    draw.rounded_rectangle([b6_x + 20, mc_y, b6_x + 175, mc_y + 180], radius=12, fill=(255, 255, 255))
    draw.text((b6_x + 32, mc_y + 14), "활성화된 계산", font=get_font(9.5, 'bold'), fill=(15, 23, 42))
    # Circular Gauge graphic
    draw.ellipse([b6_x + 48, mc_y + 38, b6_x + 148, mc_y + 138], fill=(238, 242, 255), outline=(99, 102, 241), width=3)
    draw.text((b6_x + 98, mc_y + 88), "-18.4%", font=get_num_font(14, 'bold'), fill=(99, 102, 241), anchor='mm')
    draw.text((b6_x + 32, mc_y + 150), "방어 평단가", font=get_font(11, 'bold'), fill=(15, 23, 42))
    
    # Card 2: Time Over / Warning Alert
    draw.rounded_rectangle([b6_x + 190, mc_y, b6_x + 345, mc_y + 180], radius=12, fill=(255, 255, 255))
    draw.text((b6_x + 202, mc_y + 14), "경고 알림 카드", font=get_font(9.5, 'bold'), fill=(220, 38, 38))
    draw.ellipse([b6_x + 218, mc_y + 38, b6_x + 318, mc_y + 138], fill=(254, 242, 242), outline=(239, 68, 68), width=3)
    draw.text((b6_x + 268, mc_y + 88), "ALERT", font=get_font(13, 'black'), fill=(220, 38, 38), anchor='mm')
    draw.rounded_rectangle([b6_x + 205, mc_y + 145, b6_x + 330, mc_y + 172], radius=6, fill=(239, 68, 68))
    draw.text((b6_x + 268, mc_y + 158), "+ Button", font=get_font(10, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # Card 3: Voice Prompt & Mini Status
    draw.rounded_rectangle([b6_x + 360, mc_y, b6_x + b6_w - 20, mc_y + 90], radius=12, fill=(255, 255, 255))
    draw.text((b6_x + 375, mc_y + 16), "🎙️ 음성 파형 인식", font=get_font(11, 'bold'), fill=(15, 23, 42))
    draw.text((b6_x + 375, mc_y + 38), "15,000원에 100주 물타줘", font=get_font(10, 'regular'), fill=(71, 85, 105))
    draw_pill_badge(draw, cx=b6_x + 450, cy=mc_y + 68, text="99.2% 신뢰도", font=get_font(9, 'bold'), theme='green', has_dot=True, dark_mode=False, pad_x=8, height=20)
    
    draw.rounded_rectangle([b6_x + 360, mc_y + 102, b6_x + b6_w - 20, mc_y + 180], radius=12, fill=inner_dark, outline=(38, 50, 72), width=1)
    draw.text((b6_x + 375, mc_y + 118), "상태 (State)", font=get_font(11, 'bold'), fill=(255, 255, 255))
    draw_pill_badge(draw, cx=b6_x + 410, cy=mc_y + 150, text="NEW", font=get_font(9, 'bold'), theme='amber', has_dot=False, dark_mode=True, pad_x=8, height=22)
    draw_pill_badge(draw, cx=b6_x + 480, cy=mc_y + 150, text="ACTIVE", font=get_font(9, 'bold'), theme='blue', has_dot=False, dark_mode=True, pad_x=8, height=22)
    
    # -------------------------------------------------------------
    # 7. Confirm Dialog (Bottom Left) - EXACT MATCH to Reference Image 4
    # -------------------------------------------------------------
    b7_x = 120
    b7_y = 695
    b7_w = 520
    b7_h = 265
    draw.rounded_rectangle([b7_x, b7_y, b7_x + b7_w, b7_y + b7_h], radius=16, fill=card_bg, outline=card_border, width=1)
    draw.text((b7_x + 24, b7_y + 16), "Confirm dialog", font=get_font(12, 'bold'), fill=(148, 163, 184))
    
    # Clean White Modal Card
    m_x = b7_x + 50
    m_y = b7_y + 45
    m_w = 420
    m_h = 195
    draw.rounded_rectangle([m_x, m_y, m_x + m_w, m_y + m_h], radius=14, fill=(255, 255, 255))
    draw.text((m_x + 24, m_y + 24), "약속 정보 재설정", font=get_font(16, 'bold'), fill=(15, 23, 42))
    draw.text((m_x + 24, m_y + 54), "기입된 약속 정보를 모두 삭제 합니다.\n약속 정보를 재설정 하시겠습니까?", font=get_font(11.5, 'regular'), fill=(71, 85, 105), spacing=4)
    
    # [취소] [확인] Buttons
    draw.rounded_rectangle([m_x + 24, m_y + 128, m_x + 190, m_y + 172], radius=10, fill=(241, 245, 249))
    draw.text((m_x + 107, m_y + 150), "취소", font=get_font(13, 'bold'), fill=(71, 85, 105), anchor='mm')
    
    draw.rounded_rectangle([m_x + 210, m_y + 128, m_x + m_w - 24, m_y + 172], radius=10, fill=(99, 102, 241))
    draw.text((m_x + 300, m_y + 150), "확인", font=get_font(13, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # -------------------------------------------------------------
    # 8. Map Profile, Timer & Chip (Bottom Right)
    # -------------------------------------------------------------
    b8_x = 670
    b8_y = 695
    b8_w = 1130
    b8_h = 265
    draw.rounded_rectangle([b8_x, b8_y, b8_x + b8_w, b8_y + b8_h], radius=16, fill=card_bg, outline=card_border, width=1)
    
    # 8-A: Map Profile & Avatars
    draw.text((b8_x + 30, b8_y + 16), "Map Profile", font=get_font(12, 'bold'), fill=(148, 163, 184))
    draw.rounded_rectangle([b8_x + 30, b8_y + 45, b8_x + 95, b8_y + 125], radius=10, fill=(99, 102, 241))
    draw.text((b8_x + 62, b8_y + 80), "👤", font=get_font(22, 'regular'), fill=(255, 255, 255), anchor='mm')
    draw.rounded_rectangle([b8_x + 35, b8_y + 135, b8_x + 90, b8_y + 160], radius=12, fill=(255, 255, 255))
    draw.text((b8_x + 62, b8_y + 147), "이름", font=get_font(10, 'bold'), fill=(15, 23, 42), anchor='mm')
    
    draw.rounded_rectangle([b8_x + 115, b8_y + 45, b8_x + 180, b8_y + 125], radius=10, fill=(59, 130, 246))
    draw.text((b8_x + 147, b8_y + 80), "📈", font=get_font(22, 'regular'), fill=(255, 255, 255), anchor='mm')
    draw.rounded_rectangle([b8_x + 115, b8_y + 135, b8_x + 180, b8_y + 160], radius=12, fill=(255, 255, 255))
    draw.text((b8_x + 147, b8_y + 147), "세글자", font=get_font(10, 'bold'), fill=(15, 23, 42), anchor='mm')
    
    # 8-B: Timer & Badges
    draw.text((b8_x + 230, b8_y + 16), "Timer", font=get_font(12, 'bold'), fill=(148, 163, 184))
    # Timer Pill
    draw.rounded_rectangle([b8_x + 230, b8_y + 55, b8_x + 350, b8_y + 105], radius=25, fill=(99, 102, 241))
    draw.text((b8_x + 290, b8_y + 80), "58 : 33", font=get_num_font(18, 'bold'), fill=(255, 255, 255), anchor='mm')
    # Time Over Pill
    draw.rounded_rectangle([b8_x + 370, b8_y + 55, b8_x + 500, b8_y + 92], radius=12, fill=(99, 102, 241))
    draw.text((b8_x + 435, b8_y + 73), "TIME OVER", font=get_font(12, 'bold'), fill=(255, 255, 255), anchor='mm')
    draw.rounded_rectangle([b8_x + 370, b8_y + 105, b8_x + 500, b8_y + 142], radius=12, fill=(239, 68, 68))
    draw.text((b8_x + 435, b8_y + 123), "TIME OVER", font=get_font(12, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # 8-C: Chip (WhatNow Style Text, State, Music Chips)
    draw.text((b8_x + 550, b8_y + 16), "Chip", font=get_font(12, 'bold'), fill=(148, 163, 184))
    chip_items = [
        ("💣 Text", "상태", "🎵 000"),
        ("👑 Text", "상태", "☁️ 000"),
        ("⚡ 0.2s Fast", "R8 최적화", "🔒 100% On-Device")
    ]
    cy_c = b8_y + 52
    for c_a, c_b, c_c in chip_items:
        draw.rounded_rectangle([b8_x + 550, cy_c, b8_x + 690, cy_c + 32], radius=16, fill=(255, 255, 255))
        draw.text((b8_x + 620, cy_c + 16), c_a, font=get_font(11, 'bold'), fill=(15, 23, 42), anchor='mm')
        
        draw.rounded_rectangle([b8_x + 710, cy_c, b8_x + 830, cy_c + 32], radius=16, fill=inner_dark, outline=(38, 50, 72), width=1)
        draw.text((b8_x + 770, cy_c + 16), c_b, font=get_font(11, 'medium'), fill=(148, 163, 184), anchor='mm')
        
        draw.rounded_rectangle([b8_x + 850, cy_c, b8_x + 1020, cy_c + 32], radius=16, fill=(99, 102, 241))
        draw.text((b8_x + 935, cy_c + 16), c_c, font=get_font(11, 'bold'), fill=(255, 255, 255), anchor='mm')
        cy_c += 44
        
    # Bottom Design Token Spec Bar
    draw.text((b8_x + 30, b8_y + 225), "Tokens : Pretendard Typography  ·  4pt/8pt Spatial Grid  ·  Accessible Contrast AAA 7:1+  ·  Component Library", font=get_font(11, 'regular'), fill=(100, 116, 139))
    
    base.save(f'{OUT_DIR}/slide_07.png')
    print("SAVED slide_07.png (WhatNow-Style Dark Theme Design System)")


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
    
    # Callout 1: VOICE DOCK
    draw_pill_badge(draw, rx + 65, 270, "VOICE DOCK", font=get_font(11, 'bold'), theme='blue', dark_mode=False, pad_x=12, height=26)
    draw.text((rx, 305), "자연어 음성 즉각 인식 & 파라미터 분리", font=get_font(18, 'bold'), fill=(15, 23, 42))
    draw.text((rx, 340), '"삼성전자 7만 원에 50주" 말하는 순간 종목, 단가, 수량을 자동으로 분리 인식해요.\n발화가 끝남과 동시에 시뮬레이터 수치가 채워져 실시간 호가 변동에 즉각 대응합니다.', font=get_font(14, 'regular'), fill=(71, 85, 105), spacing=5)
    
    # Callout 2: PRESET CHIPS
    draw_pill_badge(draw, rx + 75, 435, "PRESET CHIPS", font=get_font(11, 'bold'), theme='cyan', dark_mode=False, pad_x=12, height=26)
    draw.text((rx, 470), "소음 환경을 위한 원터치 호가 프리셋 칩", font=get_font(18, 'bold'), fill=(15, 23, 42))
    draw.text((rx, 505), "음성을 쓰기 어려운 대중교통이나 조용한 환경에서도 ±5%, ±10% 호가 칩으로\n손가락 1-Tap 터치만으로 0.1초 만에 즉시 추가 매수 시나리오를 계산해요.", font=get_font(14, 'regular'), fill=(71, 85, 105), spacing=5)
    
    # Callout 3: AI LIVE PARSER CARD
    card_y = 600
    card_h = 240
    draw.rounded_rectangle([rx, card_y, rx + r_w, card_y + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    draw_pill_badge(draw, rx + 80, card_y + 30, "AI LIVE PARSER", font=get_font(10.5, 'bold'), theme='purple', dark_mode=False, pad_x=10, height=24)
    draw.text((rx + 160, card_y + 22), "실시간 온디바이스 음성 파싱 피드백", font=get_font(13.5, 'bold'), fill=(15, 23, 42))
    
    draw.rounded_rectangle([rx + 24, card_y + 60, rx + r_w - 24, card_y + 130], radius=12, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
    draw_pill_badge(draw, left_x=rx + 42, cy=card_y + 86, text="LIVE STT", font=get_font(9.5, 'bold'), theme='blue', has_dot=True, dark_mode=False, pad_x=8, height=22)
    draw.text((rx + 130, card_y + 75), '"삼성전자 70,000원에 50주 추가 매수"', font=get_font(16, 'bold'), fill=(0, 82, 255))
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
        
    # Architectural Dotted Callouts linking Phone UI to Badges (Reference Image 5 Style)
    draw_dotted_callout(draw, p1=(px + pw - 30, py + 620), p2=(rx - 15, 270), col=(0, 82, 255))
    draw_dotted_callout(draw, p1=(px + pw - 30, py + 520), p2=(rx - 15, 435), col=(6, 182, 212))
    draw_dotted_callout(draw, p1=(px + pw - 30, py + 380), p2=(rx - 15, 630), col=(124, 58, 237))
        
    base.save(f'{OUT_DIR}/slide_08.png')
    print("SAVED slide_08.png (Voice Dock UI with Blueprint Dotted Callouts)")


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
    
    # Callout 1: CLOSED-FORM QUANT
    draw_pill_badge(draw, rx + 105, 270, "CLOSED-FORM QUANT", font=get_font(11, 'bold'), theme='blue', dark_mode=False, pad_x=12, height=26)
    draw.text((rx, 305), "수학적 폐쇄형 역산 알고리즘 (Zero-Latency)", font=get_font(18, 'bold'), fill=(15, 23, 42))
    draw.text((rx, 340), "Q_add = Q_0 × (P_0 - P_target) / (P_target - P_add) 수식을 온디바이스에서 즉시 풀어내어\n복잡한 시행착오 반복 연산 없이 닫힌 형식으로 필요 수량과 자금을 즉시 산출해요.", font=get_font(14, 'regular'), fill=(71, 85, 105), spacing=5)
    
    # Callout 2: BOUNDARY GUARD
    draw_pill_badge(draw, rx + 95, 435, "BOUNDARY GUARD", font=get_font(11, 'bold'), theme='amber', dark_mode=False, pad_x=12, height=26)
    draw.text((rx, 470), "비현실적 목표 사전 가드 & 대안 평단 제시", font=get_font(18, 'bold'), fill=(15, 23, 42))
    draw.text((rx, 505), "현재 추가 매수가보다 낮은 비현실적 목표 입력 시 즉시 감지하여 안전 경고를 띄우고,\n현재 가용 예수금 범위 안에서 도달 가능한 최선의 방어 평단을 추천해요.", font=get_font(14, 'regular'), fill=(71, 85, 105), spacing=5)
    
    # Callout 3: QUANT ENGINE CARD
    card_y = 600
    card_h = 240
    draw.rounded_rectangle([rx, card_y, rx + r_w, card_y + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    draw_pill_badge(draw, rx + 80, card_y + 30, "QUANT ENGINE", font=get_font(10.5, 'bold'), theme='green', dark_mode=False, pad_x=10, height=24)
    draw.text((rx + 160, card_y + 22), "실시간 퀀트 역산 검증 리포트", font=get_font(13.5, 'bold'), fill=(15, 23, 42))
    
    draw.rounded_rectangle([rx + 24, card_y + 60, rx + r_w - 24, card_y + 130], radius=12, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw_pill_badge(draw, left_x=rx + 42, cy=card_y + 86, text="SOLVED", font=get_font(9.5, 'bold'), theme='green', has_dot=True, dark_mode=False, pad_x=8, height=22)
    draw.text((rx + 130, card_y + 75), "목표 탈출가 ₩70,000 도달을 위해 42.5주 필요", font=get_font(16, 'bold'), fill=(0, 82, 255))
    draw.text((rx + 42, card_y + 104), "100% 로컬 닫힌 형식 퀀트 알고리즘 연산 완료 (연산 오차 0.00%)", font=get_font(12, 'regular'), fill=(100, 116, 139))
    
    chips = [
        ("기존 평단", "₩ 78,000", (100, 116, 139)),
        ("목표 평단", "₩ 70,000", (0, 82, 255)),
        ("필요 수량", "+42.5 주", (16, 185, 129)),
        ("필요 자금", "₩ 2,762,500", (245, 158, 11))
    ]
    cx = rx + 24
    cy = card_y + 155
    cw = 158
    for label, val, c_col in chips:
        draw.rounded_rectangle([cx, cy, cx + cw, cy + 60], radius=8, fill=(250, 252, 255), outline=(226, 232, 240), width=1)
        draw.text((cx + 14, cy + 10), label, font=get_font(11, 'bold'), fill=(100, 116, 139))
        draw.text((cx + 14, cy + 32), val, font=get_font(13.5, 'bold'), fill=c_col)
        cx += cw + 14
        
    # Architectural Dotted Callouts linking Phone UI to Badges (Reference Image 5 Style)
    draw_dotted_callout(draw, p1=(px + pw - 30, py + 330), p2=(rx - 15, 270), col=(0, 82, 255))
    draw_dotted_callout(draw, p1=(px + pw - 30, py + 410), p2=(rx - 15, 435), col=(217, 119, 6))
    draw_dotted_callout(draw, p1=(px + pw - 30, py + 520), p2=(rx - 15, 630), col=(16, 185, 129))
        
    base.save(f'{OUT_DIR}/slide_09.png')
    print("SAVED slide_09.png (Goal Seeking UI with Blueprint Dotted Callouts)")


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
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Hairline Boundaries
    draw.line([(120, 100), (1800, 100)], fill=(226, 232, 240), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(226, 232, 240), width=1)
    
    # Header - Korail Style Conversational Typography
    draw.text((120, 75), "11 IMPACT | QUANTITATIVE RESULTS", font=get_font(14, 'bold'), fill=(0, 82, 255))
    t1_a = "행동재무학적 접근으로 "
    t1_b = "패닉셀을 방지하고 계좌를 지켜내요."
    font_title = get_font(38, 'bold')
    w_t1_a = draw.textlength(t1_a, font=font_title)
    draw.text((120, 115), t1_a, font=font_title, fill=(15, 23, 42))
    draw.text((120 + w_t1_a, 115), t1_b, font=font_title, fill=(0, 82, 255))
    draw.text((120, 175), "처분 효과 방어율 64.2%와 65% 안전 유동성 보존으로 입증된 정량적 사용자 임팩트", font=get_font(16, 'regular'), fill=(71, 85, 105))
    
    # Verified Badge (Top Right)
    draw_pill_badge(draw, 1660, 95, "EMPIRICAL TEST 100% PASS", font=get_font(10.5, 'bold'), theme='green', has_dot=True, dark_mode=False, pad_x=12, height=32)
    
    # DUAL COMPARISON CARDS: BEFORE vs. AFTER DEFENSE ANALYSIS
    card_y = 230
    card_h = 445
    card_w = 810
    
    # LEFT CARD: Traditional Emotional Trading (Before)
    cx1 = 120
    draw.rounded_rectangle([cx1, card_y, cx1 + card_w, card_y + card_h], radius=18, fill=(255, 255, 255), outline=(254, 202, 202), width=1)
    draw.rounded_rectangle([cx1, card_y + 18, cx1 + 6, card_y + card_h - 18], radius=3, fill=(239, 68, 68))
    
    draw_pill_badge(draw, cx1 + 145, card_y + 36, "BEFORE : EMOTIONAL TRADING", font=get_font(10, 'bold'), theme='red', has_dot=True, dark_mode=False, pad_x=10, height=26)
    draw.text((cx1 + 28, card_y + 66), "감정에 치우친 뇌동매매 (Before)", font=get_font(21, 'bold'), fill=(15, 23, 42))
    draw.text((cx1 + 28, card_y + 98), "계획 없는 추가 매수로 인한 자금 고갈 및 패닉셀 유발", font=get_font(13.5, 'regular'), fill=(100, 116, 139))
    
    b_rows = [
        ("초기 투자 포지션", "100주  ·  매입가 ₩ 78,000 (총 투자 ₩ 7,800,000)", (15, 23, 42)),
        ("현재가 및 평가 손실", "₩ 65,000  ·  손실률 -16.67% (계좌 평가손 ₩ -1,300,000)", (220, 38, 38)),
        ("원금 회복 필요 반등률", "+20.00% 상승 필요 (전고점 탈출 부담 극대화)", (220, 38, 38)),
        ("예수금 소진 및 유동성", "자금 소진율 92.4% (초기 무계획 몰빵으로 추가 방어 불가)", (180, 83, 9)),
        ("투자자 심리 상태", "처분 효과와 공포로 인한 비자발적 패닉셀(손절)", (100, 116, 139))
    ]
    ry = card_y + 138
    for label, val, val_col in b_rows:
        draw.rounded_rectangle([cx1 + 28, ry, cx1 + card_w - 28, ry + 48], radius=8, fill=(254, 242, 242), outline=(254, 202, 202), width=1)
        draw.text((cx1 + 44, ry + 14), label, font=get_font(12, 'bold'), fill=(100, 116, 139))
        draw.text((cx1 + 220, ry + 13), val, font=get_font(13, 'bold'), fill=val_col)
        ry += 56
        
    # RIGHT CARD: Smart Quant DCA Inversion (After)
    cx2 = 980
    draw.rounded_rectangle([cx2, card_y, cx2 + card_w, card_y + card_h], radius=18, fill=(255, 255, 255), outline=(191, 219, 254), width=1)
    draw.rounded_rectangle([cx2, card_y + 18, cx2 + 6, card_y + card_h - 18], radius=3, fill=(0, 82, 255))
    
    draw_pill_badge(draw, cx2 + 155, card_y + 36, "AFTER : SMART DCA SOLUTION", font=get_font(10, 'bold'), theme='blue', has_dot=True, dark_mode=False, pad_x=10, height=26)
    draw.text((cx2 + 28, card_y + 66), "스마트 DCA 역산 솔루션 (After)", font=get_font(21, 'bold'), fill=(15, 23, 42))
    draw.text((cx2 + 28, card_y + 98), "희망 탈출 가격에 맞춘 정량 분할 매수로 계좌와 심리적 안정성 확보", font=get_font(13.5, 'regular'), fill=(100, 116, 139))
    
    a_rows = [
        ("정량 최적 매수 집행", "+38주 분할 매수  ·  소요 자금 ₩ 2,470,000 (무지연 산출)", (0, 82, 255)),
        ("방어 후 신규 평균단가", "₩ 74,420  (손실률 -12.65%로 +4.02%p 계좌 즉각 방어)", (5, 150, 105)),
        ("원금 회복 필요 반등률", "+7.69% 반등 시 본전 탈출 (회복 부담 61.5% 대폭 경감)", (5, 150, 105)),
        ("예수금 보존 및 안전 마진", "현금 보존율 65.0% 유지 (추가 지지선 대응 여력 확보)", (180, 83, 9)),
        ("투자자 심리 상태", "수학적 명확성 신뢰로 공포를 걷어내고 냉철한 대응 완성", (15, 23, 42))
    ]
    ry = card_y + 138
    for label, val, val_col in a_rows:
        draw.rounded_rectangle([cx2 + 28, ry, cx2 + card_w - 28, ry + 48], radius=8, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
        draw.text((cx2 + 44, ry + 14), label, font=get_font(12, 'bold'), fill=(100, 116, 139))
        draw.text((cx2 + 220, ry + 13), val, font=get_font(13, 'bold'), fill=val_col)
        ry += 56
        
    # BOTTOM 4 TELEMETRY CARDS
    t_y = 705
    t_h = 245
    t_w = 385
    t_gap = 40
    tx = 120
    
    telemetry_data = [
        ("4.2 s", "계산 소요 시간 극단적 단축", "복합 시뮬레이션 소요 시간을 240초에서 4.2초로 대폭 단축하여\n타이핑 피로 해소", (0, 82, 255), "blue", "TASK SPEED"),
        ("65.0 %", "안전 현금 유동성 보존", "감정에 치우친 몰빵을 막아주고 안전 현금을 남겨\n2차 위기 대응력 확보", (16, 185, 129), "green", "CASH BUFFER"),
        ("0 건", "입력 실수 및 오작동 차단", "비정상적인 단가나 비현실적 목표 입력을 사전에 걸러내어\n주문 실수 원천 방지", (2, 132, 199), "cyan", "ZERO ERROR"),
        ("4.9 ★", "실사용자 만족도 평점", "Google Play Store 실사용자 리뷰 기반\n하락장에서 마음의 안정을 주는 필수 앱 찬사", (245, 158, 11), "amber", "STORE RATING")
    ]
    
    for val, title, desc, col, theme_key, badge in telemetry_data:
        draw.rounded_rectangle([tx, t_y, tx + t_w, t_y + t_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw_pill_badge(draw, tx + 72, t_y + 32, badge, font=get_font(9.5, 'bold'), theme=theme_key, has_dot=True, dark_mode=False, pad_x=8, height=24)
        draw.text((tx + 24, t_y + 54), val, font=get_num_font(38, 'black'), fill=(15, 23, 42))
        draw.text((tx + 24, t_y + 112), title, font=get_font(15, 'bold'), fill=(15, 23, 42))
        draw.text((tx + 24, t_y + 142), desc, font=get_font(12, 'regular'), fill=(100, 116, 139), spacing=4)
        tx += t_w + t_gap
        
    base.save(f'{OUT_DIR}/slide_11.png')
    print("SAVED slide_11.png (Empirical Account Defense & UX Telemetry - Light Theme)")

# ==============================================================
# SLIDE 12: Business Impact & Senior PM / UX Retrospective (STAR)
# ==============================================================
def make_slide_12():
    base = Image.new("RGBA", (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Hairline Boundaries
    draw.line([(120, 100), (1800, 100)], fill=(226, 232, 240), width=1)
    draw.line([(120, 980), (1800, 980)], fill=(226, 232, 240), width=1)
    
    # Header - Korail Style Conversational Typography
    draw.text((120, 75), "12 ROADMAP | RETROSPECTIVE", font=get_font(14, "bold"), fill=(0, 82, 255))
    t1_a = "지속 가능한 퀀트 플랫폼으로 "
    t1_b = "더 넓은 투자의 길을 열어가요."
    font_title = get_font(38, "bold")
    w_t1_a = draw.textlength(t1_a, font=font_title)
    draw.text((120, 115), t1_a, font=font_title, fill=(15, 23, 42))
    draw.text((120 + w_t1_a, 115), t1_b, font=font_title, fill=(0, 82, 255))
    draw.text((120, 175), "위기 극복 경험에서 얻은 3대 핵심 인사이트와 향후 3단계 프로덕트 진화 로드맵", font=get_font(16, "regular"), fill=(71, 85, 105))
    
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
            "cyan", (2, 132, 199)
        ),
        (
            "LEARNING 02",
            "엄지 조작계와 음성 도크 시너지",
            "단일 인터랙션을 넘어선 하이브리드 UX",
            [
                "이동 중이거나 떨리는 손으로 소수점 가격을 직접 입력하는 고통을 해결하기 위해, 한 손 조작 영역(Thumb Zone) 하단에 음성 도크를 상시 배치했습니다.",
                "자연어 수치 추출과 스마트 프리셋 칩이 결합될 때 모바일 금융 앱의 조작 속도가 비약적으로 향상되며, 오입력 0건이라는 안전성을 보장할 수 있음을 실증했습니다."
            ],
            "green", (5, 150, 105)
        ),
        (
            "LEARNING 03",
            "수학적 불변성이 주는 심리적 안정",
            "막연한 추정이 아닌 정밀한 닫힌 형식 해",
            [
                "투자자가 겪는 불안의 본질은 '내가 과연 얼마를 더 사야 탈출할 수 있는가'에 대한 불확실성에 있었습니다.",
                "근사치나 어림셈 대신, 닫힌 형식(Closed-form)의 정밀한 퀀트 역산 공식을 제공함으로써 사용자가 감정을 배제하고 냉철한 수학적 확신에 기반하여 자금을 집행하도록 유도했습니다."
            ],
            "blue", (0, 82, 255)
        )
    ]
    
    lx = 120
    lw = 520
    lgap = 40
    ly = 230
    lh = 330
    
    for badge, title, subtitle, paras, theme_key, col in learnings:
        draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw_pill_badge(draw, lx + 70, ly + 28, badge, font=get_font(10, "bold"), theme=theme_key, has_dot=True, dark_mode=False, pad_x=10, height=24)
        draw.text((lx + 24, ly + 60), title, font=get_font(19, "bold"), fill=(15, 23, 42))
        draw.text((lx + 24, ly + 92), subtitle, font=get_font(13.5, "semibold"), fill=col)
        draw.line([(lx + 24, ly + 120), (lx + lw - 24, ly + 120)], fill=(241, 245, 249), width=1)
        
        py = ly + 134
        for p in paras:
            lines = textwrap.wrap(p, width=28)
            for line in lines:
                draw.text((lx + 24, py), line, font=get_font(11.5, "regular"), fill=(71, 85, 105))
                py += 20
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
            "blue", (0, 82, 255)
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
            "amber", (217, 119, 6)
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
            "purple", (124, 58, 237)
        )
    ]
    
    rx = 120
    rw = 520
    rgap = 40
    ry = 585
    rh = 285
    
    for phase_badge, r_title, r_sub, bullets, theme_key, r_col in roadmap:
        draw.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw_pill_badge(draw, rx + 75, ry + 28, phase_badge, font=get_font(10, "bold"), theme=theme_key, has_dot=True, dark_mode=False, pad_x=10, height=24)
        draw.text((rx + 24, ry + 60), r_title, font=get_font(18, "bold"), fill=(15, 23, 42))
        draw.text((rx + 24, ry + 90), r_sub, font=get_font(12.5, "semibold"), fill=r_col)
        draw.line([(rx + 24, ry + 116), (rx + rw - 24, ry + 116)], fill=(241, 245, 249), width=1)
        
        by = ry + 130
        for b_text in bullets:
            draw.text((rx + 24, by), f"• {b_text}", font=get_font(11.5, "regular"), fill=(71, 85, 105))
            by += 28
            
        rx += rw + rgap
        
    # SECTION 3: PROJECT CREDITS & PRODUCTION WRAP-UP (하단: 크레딧 및 상태)
    cy = 895
    ch = 65
    draw.rounded_rectangle([120, cy, 1800, cy + ch], radius=14, fill=(15, 23, 42), outline=(51, 65, 85), width=1)
    
    draw.text((144, cy + 22), "PROJECT CREDITS", font=get_font(12, "bold"), fill=(0, 210, 255))
    draw.text((270, cy + 22), "End-to-End Product Design  ·  Quant Mathematical Modeling  ·  Flutter Mobile Architecture", font=get_font(13.5, "medium"), fill=(255, 255, 255))
    
    draw_pill_badge(draw, 1420, cy + 32, "GOOGLE PLAY STORE LIVE", font=get_font(10, "bold"), theme="green", has_dot=True, dark_mode=True, pad_x=12, height=26)
    draw.text((1535, cy + 22), "100% Offline Engine · No Financial Logging", font=get_font(12, "medium"), fill=(148, 163, 184))
    
    base.save(f"{OUT_DIR}/slide_12.png")
    print("SAVED slide_12.png (Redesigned Retrospective & Roadmap - Light Theme)")


if __name__ == '__main__':
    for i in range(1, 13):
        func_name = f'make_slide_{i:02d}'
        if func_name in globals():
            globals()[func_name]()
    print("ALL 12 SLIDES GENERATED WITH MASCULINE EDITORIAL AESTHETIC!")
