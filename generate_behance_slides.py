import math
import textwrap
import os
import numpy as np
import qrcode
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

def draw_database_node(draw, cx, cy, w, h, fill=(240, 246, 255), outline=(0, 82, 255), width=1):
    ew = w
    eh = int(h * 0.28)
    top_y = cy - h // 2
    bot_y = cy + h // 2
    draw.ellipse([cx - ew // 2, bot_y - eh, cx + ew // 2, bot_y], fill=fill, outline=outline, width=width)
    draw.rectangle([cx - ew // 2, top_y + eh // 2, cx + ew // 2, bot_y - eh // 2], fill=fill)
    draw.line([(cx - ew // 2, top_y + eh // 2), (cx - ew // 2, bot_y - eh // 2)], fill=outline, width=width)
    draw.line([(cx + ew // 2, top_y + eh // 2), (cx + ew // 2, bot_y - eh // 2)], fill=outline, width=width)
    draw.ellipse([cx - ew // 2, top_y, cx + ew // 2, top_y + eh], fill=fill, outline=outline, width=width)

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


def draw_pill_badge(draw, cx=None, cy=0, text="", font=None, theme='blue', has_dot=True, dark_mode=False, pad_x=14, height=30, left_x=None, solid=False):
    """
    Renders a mathematically centered, high-contrast, beautiful pill badge with pixel-perfect alignment.
    Supports themes: 'blue', 'green', 'red', 'amber', 'purple', 'cyan', 'slate', 'dark'.
    Supports fill types: soft pastel tint (default light), solid brand fill (solid=True), or dark outline (dark_mode=True).
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
        'blue':   {'bg': (239, 246, 255, 255), 'border': (191, 219, 254, 255), 'text': (0, 82, 255, 255),   'dot': (0, 82, 255, 255)},
        'cyan':   {'bg': (236, 254, 255, 255), 'border': (165, 243, 252, 255), 'text': (8, 145, 178, 255),  'dot': (6, 182, 212, 255)},
        'green':  {'bg': (236, 253, 245, 255), 'border': (167, 243, 208, 255), 'text': (5, 150, 105, 255),  'dot': (16, 185, 129, 255)},
        'red':    {'bg': (254, 242, 242, 255), 'border': (254, 202, 202, 255), 'text': (220, 38, 38, 255),  'dot': (239, 68, 68, 255)},
        'amber':  {'bg': (254, 243, 199, 255), 'border': (253, 230, 138, 255), 'text': (180, 83, 9, 255),   'dot': (245, 158, 11, 255)},
        'purple': {'bg': (245, 243, 255, 255), 'border': (221, 214, 254, 255), 'text': (109, 40, 217, 255), 'dot': (139, 92, 246, 255)},
        'slate':  {'bg': (241, 245, 249, 255), 'border': (203, 213, 225, 255), 'text': (51, 65, 85, 255),   'dot': (100, 116, 139, 255)},
        'dark':   {'bg': (15, 23, 42, 255),    'border': (15, 23, 42, 255),     'text': (255, 255, 255, 255),'dot': (0, 210, 255, 255)},
    }
    color_schemes_solid = {
        'blue':   {'bg': (0, 82, 255, 255),   'border': (0, 82, 255, 255),   'text': (255, 255, 255, 255), 'dot': (191, 219, 254, 255)},
        'cyan':   {'bg': (8, 145, 178, 255),  'border': (8, 145, 178, 255),  'text': (255, 255, 255, 255), 'dot': (207, 250, 254, 255)},
        'green':  {'bg': (16, 185, 129, 255), 'border': (16, 185, 129, 255), 'text': (255, 255, 255, 255), 'dot': (209, 250, 229, 255)},
        'red':    {'bg': (239, 68, 68, 255),  'border': (239, 68, 68, 255),  'text': (255, 255, 255, 255), 'dot': (254, 226, 226, 255)},
        'amber':  {'bg': (217, 119, 6, 255),  'border': (217, 119, 6, 255),  'text': (255, 255, 255, 255), 'dot': (254, 243, 199, 255)},
        'purple': {'bg': (124, 58, 237, 255), 'border': (124, 58, 237, 255), 'text': (255, 255, 255, 255), 'dot': (237, 233, 254, 255)},
        'slate':  {'bg': (71, 85, 105, 255),  'border': (71, 85, 105, 255),  'text': (255, 255, 255, 255), 'dot': (226, 232, 240, 255)},
        'dark':   {'bg': (15, 23, 42, 255),   'border': (15, 23, 42, 255),   'text': (255, 255, 255, 255), 'dot': (0, 210, 255, 255)},
    }
    
    if solid:
        scheme = color_schemes_solid.get(theme, color_schemes_solid['blue'])
    elif dark_mode:
        scheme = color_schemes_dark.get(theme, color_schemes_dark['blue'])
    else:
        scheme = color_schemes_light.get(theme, color_schemes_light['blue'])
    
    tw = draw.textlength(text, font=font)
    dot_diameter = 7
    dot_gap = 8
    
    if has_dot:
        content_w = dot_diameter + dot_gap + tw
    else:
        content_w = tw
        
    bw = int(round(content_w + pad_x * 2))
    bh = int(round(height))
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
    
    if has_dot:
        content_x1 = bx1 + pad_x
        dot_cx = content_x1 + dot_diameter / 2.0
        r = dot_diameter / 2.0
        draw.ellipse([int(round(dot_cx - r)), int(round(cy - r)), int(round(dot_cx + r)), int(round(cy + r))], fill=scheme['dot'])
        tx = content_x1 + dot_diameter + dot_gap
        draw.text((tx, cy), text, font=font, anchor='lm', fill=scheme['text'])
    else:
        draw.text((cx, cy), text, font=font, anchor='mm', fill=scheme['text'])
        
    return bx1, by1, bx2, by2

def draw_slide_header(draw, slide_num, category_en, title_black, title_blue, subtitle_kr, right_badge=None, dark_mode=False):
    """
    Renders the unified, executive Behance editorial header across all portfolio slides.
    Standardizes top hairline, kicker badge, dual-color main headline, and subtitle.
    Guarantees a clean, comfortable bottom margin (25px) below the kicker badge.
    Supports dark_mode for high-impact finale slides.
    """
    line_col = (40, 53, 72) if dark_mode else (226, 232, 240)
    draw.line([(100, 52), (1820, 52)], fill=line_col, width=1)
    
    badge_text = f"{slide_num:02d} {category_en.upper()}"
    draw_pill_badge(draw, left_x=100, cy=78, text=badge_text, font=get_font(10.5, 'bold'), theme='blue', has_dot=True, dark_mode=dark_mode, pad_x=10, height=26)
    
    if right_badge:
        txt, theme = right_badge
        draw_pill_badge(draw, cx=1700, cy=78, text=txt, font=get_font(10.5, 'bold'), theme=theme, solid=True, dark_mode=dark_mode, pad_x=14, height=28)
        
    font_title = get_font(35, 'bold')
    w_black = draw.textlength(title_black, font=font_title)
    text_main_col = (255, 255, 255) if dark_mode else (15, 23, 42)
    text_blue_col = (56, 189, 248) if dark_mode else (0, 81, 255)
    draw.text((100, 116), title_black, font=font_title, fill=text_main_col)
    draw.text((100 + w_black, 116), title_blue, font=font_title, fill=text_blue_col)
    
    sub_col = (148, 163, 184) if dark_mode else (71, 85, 105)
    draw.text((100, 164), subtitle_kr, font=get_font(14.5, 'regular'), fill=sub_col)


def draw_slide_footer(draw, slide_num, total_slides=12, dark_mode=False):
    """
    Renders the unified, executive Behance editorial footer strip across all portfolio slides.
    Standardizes bottom hairline, brand text, tech stack, and pagination.
    Supports dark_mode for high-impact finale slides.
    """
    line_col = (40, 53, 72) if dark_mode else (226, 232, 240)
    draw.line([(100, 995), (1820, 995)], fill=line_col, width=1)
    
    brand_col = (56, 189, 248) if dark_mode else (0, 81, 255)
    draw.text((100, 1018), "SMART DCA CALCULATOR", font=get_font(11, 'bold'), fill=brand_col)
    meta_col = (100, 116, 139) if dark_mode else (148, 163, 184)
    draw.text((270, 1018), "·   Behance Enterprise Case Study  ·  Quant Inversion Engine", font=get_font(11, 'medium'), fill=meta_col)
    draw.text((960, 1018), "Flutter 3.38+ Mobile & Web  ·  Closed-Form Math  ·  Google Play Live", font=get_font(10.5, 'medium'), fill=meta_col, anchor='mt')
    
    page_col = (148, 163, 184) if dark_mode else (100, 116, 139)
    page_str = f"PAGE {slide_num:02d} / {total_slides:02d}"
    draw.text((1820, 1018), page_str, font=get_num_font(11.5, 'black'), fill=page_col, anchor='rt')


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
        
    # 3. Arrow / terminal anchor at end point (pointing appropriately)
    arrow_size = 6
    if x2 >= x1:
        draw.polygon([(x2, y2), (x2 - arrow_size, y2 - arrow_size * 0.7), (x2 - arrow_size, y2 + arrow_size * 0.7)], fill=col)
    else:
        draw.polygon([(x2, y2), (x2 + arrow_size, y2 - arrow_size * 0.7), (x2 + arrow_size, y2 + arrow_size * 0.7)], fill=col)



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
        draw.rounded_rectangle([128, k_y, 160, k_y + 26], radius=6, fill=(241, 245, 249))
        draw.text((144, k_y + 13), num, font=get_font(11, 'bold'), fill=(0, 82, 255), anchor='mm')
        draw.text((172, k_y + 3), k_title, font=get_font(13.5, 'bold'), fill=(15, 23, 42))
        draw.text((172, k_y + 25), k_desc, font=get_font(11.5, 'regular'), fill=(100, 116, 139))
        k_y += 66
        
    # 3. Modern Flagship 19.5:9 Smartphone Mockups (Centered-Right, Clean & Elegant)
    phone_home = Image.open('portfolio/iphone_mockups/iphone_01_home.png').convert('RGBA')
    phone_target = Image.open('portfolio/iphone_mockups/iphone_03_target.png').convert('RGBA')
    
    target_h = 640
    target_w = int(round(target_h * (phone_home.width / phone_home.height)))
    
    p_front = phone_home.resize((target_w, target_h), Image.Resampling.LANCZOS)
    p_back = phone_target.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    angle = -11.0
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
    
    # Beautiful spatial placement (tuned for 19.5:9 slender profile)
    p_back_x = 1310
    p_back_y = 145
    
    p_front_x = 1010
    p_front_y = 200
    
    base.paste(sh_back, (p_back_x - pad_b[0], p_back_y - pad_b[1]), sh_back)
    base.paste(rot_back, (p_back_x, p_back_y), rot_back)
    
    base.paste(sh_front, (p_front_x - pad_f[0], p_front_y - pad_f[1]), sh_front)
    base.paste(rot_front, (p_front_x, p_front_y), rot_front)
    
    # 4. Floating Feature Callout Pills anchored to Mockups (Reference Style)
    draw = ImageDraw.Draw(base)
    draw_pill_badge(draw, cx=1140, cy=160, text="0.2s VOICE DOCK", font=get_font(10.5, 'bold'), theme='cyan', pad_x=12, height=28, solid=True)
    draw_pill_badge(draw, cx=1640, cy=200, text="GOAL-SEEKING ENGINE", font=get_font(10.5, 'bold'), theme='amber', pad_x=12, height=28, solid=True)
    draw_pill_badge(draw, cx=1580, cy=815, text="65% CASH SAFETY GUARD", font=get_font(10.5, 'bold'), theme='green', pad_x=12, height=28, solid=True)
    
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
        
    draw_slide_footer(draw, 1)
    base.save(f'{OUT_DIR}/slide_01.png')
    print("SAVED clean simple Slide 01 successfully!")

def make_slide_02():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Unified Header
    draw_slide_header(
        draw, 
        slide_num=2, 
        category_en="USER RESEARCH | DESK RESEARCH & MARKET STUDY", 
        title_black="국내 투자자 행태 분석과 ", 
        title_blue="비이성적 물타기의 기존 문제점", 
        subtitle_kr="투자자 428명 정량 데이터 및 14대 증권사 전수 조사를 통해 도출한 3대 핵심 위협과 SWOT 전략"
    )
    
    # ==============================================================
    # 1. TOP: 3 Horizontal Market Trend Cards (Donut, H-Bar, V-Bar)
    # ==============================================================
    card_w = 546
    card_h = 220
    gap = 40
    sy = 215
    
    # --------------------------------------------------------------
    # CARD 1: MARKET TREND (Large Donut Chart - 82.6%)
    # --------------------------------------------------------------
    c1_x = 100
    draw.rounded_rectangle([c1_x, sy, c1_x + card_w, sy + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([c1_x, sy + 18, c1_x + 5, sy + card_h - 18], radius=2, fill=(220, 38, 38))
    
    # Left Typography Stack (21px bottom margin below badge)
    draw_pill_badge(draw, left_x=c1_x + 24, cy=sy + 26, text="MARKET TREND", font=get_font(10, 'bold'), theme='red', has_dot=False, pad_x=8, height=22)
    draw.text((c1_x + 24, sy + 58), "손실 회피와 비이성적 물타기", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    draw.text((c1_x + 24, sy + 88), "개인 투자자 10명 중 8명 이상이 출구 전략 없이\n감에 의존해 추가 매수를 감행하다 손실을 키웁니다.", font=get_font(11.5, 'regular'), fill=(100, 116, 139), spacing=4)
    
    draw.text((c1_x + 24, sy + 144), "82.6%", font=get_num_font(38, 'black'), fill=(220, 38, 38))
    draw.text((c1_x + 24, sy + 188), "경험률 (자본시장연구원 N=428)", font=get_font(11, 'bold'), fill=(100, 116, 139))
    
    # Right: Large Anti-Aliased Donut Chart (Radius 56 / 38)
    cx_donut = c1_x + card_w - 95
    cy_donut = sy + 116
    draw_donut_chart_on_base(base, cx_donut, cy_donut, r_outer=56, r_inner=38, percentage=82.6, col_fill=(220, 38, 38), col_track=(254, 226, 226))
    draw = ImageDraw.Draw(base)
    
    # Top Tag above Donut
    draw_pill_badge(draw, cx=cx_donut, cy=sy + 32, text="N=428 실태조사", font=get_font(9, 'bold'), theme='red', has_dot=False, pad_x=8, height=20)
    
    # Center text inside Donut hole (Mathematically centered)
    d_num = "83%"
    b_dnum = draw.textbbox((0, 0), d_num, font=get_num_font(18, 'black'))
    w_dnum = b_dnum[2] - b_dnum[0]
    h_dnum = b_dnum[3] - b_dnum[1]
    d_sub = "응답률"
    b_dsub = draw.textbbox((0, 0), d_sub, font=get_font(9.5, 'bold'))
    w_dsub = b_dsub[2] - b_dsub[0]
    h_dsub = b_dsub[3] - b_dsub[1]
    
    d_tot_h = h_dnum + 4 + h_dsub
    d_top = cy_donut - d_tot_h / 2.0
    draw.text((cx_donut - (b_dnum[0] + b_dnum[2]) / 2.0, d_top - b_dnum[1]), d_num, font=get_num_font(18, 'black'), fill=(220, 38, 38))
    draw.text((cx_donut - (b_dsub[0] + b_dsub[2]) / 2.0, d_top + h_dnum + 4 - b_dsub[1]), d_sub, font=get_font(9.5, 'bold'), fill=(100, 116, 139))
    
    # --------------------------------------------------------------
    # CARD 2: BEHAVIOR TREND (Large Horizontal Bar Chart)
    # --------------------------------------------------------------
    c2_x = c1_x + card_w + gap
    draw.rounded_rectangle([c2_x, sy, c2_x + card_w, sy + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([c2_x, sy + 18, c2_x + 5, sy + card_h - 18], radius=2, fill=(217, 119, 6))
    
    # Left Typography Stack (21px bottom margin below badge)
    draw_pill_badge(draw, left_x=c2_x + 24, cy=sy + 26, text="BEHAVIOR TREND", font=get_font(10, 'bold'), theme='amber', has_dot=False, pad_x=8, height=22)
    draw.text((c2_x + 24, sy + 58), "급박한 순간의 타이핑 인지부하", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    draw.text((c2_x + 24, sy + 88), "호가가 급변하는 폭락장에서 8자리 단가를 직접 치다\n지지선을 놓치고 추가 손실(-6.4%)에 직면합니다.", font=get_font(11.5, 'regular'), fill=(100, 116, 139), spacing=4)
    
    draw.text((c2_x + 24, sy + 144), "240s → 4.2s", font=get_num_font(30, 'black'), fill=(217, 119, 6))
    draw.text((c2_x + 24, sy + 188), "소요 시간 98% 단축 (인터뷰 실측)", font=get_font(11, 'bold'), fill=(16, 185, 129))
    
    # Right: Large Horizontal Bar Chart
    bx = c2_x + card_w - 170
    b_w = 145
    draw_pill_badge(draw, cx=bx + b_w // 2, cy=sy + 32, text="소요 시간 비교", font=get_font(9, 'bold'), theme='amber', has_dot=False, pad_x=8, height=20)
    
    # Bar 1: 기존 수동 키패드 (240초)
    draw.text((bx, sy + 57), "기존 수동 키패드", font=get_font(10, 'bold'), fill=(148, 163, 184))
    w_240s = draw.textlength("240s", font=get_num_font(11.5, 'bold'))
    draw.text((bx + b_w - w_240s, sy + 57), "240s", font=get_num_font(11.5, 'bold'), fill=(220, 38, 38))
    draw.rounded_rectangle([bx, sy + 75, bx + b_w, sy + 75 + 16], radius=8, fill=(254, 226, 226))
    draw.rounded_rectangle([bx, sy + 75, bx + b_w, sy + 75 + 16], radius=8, fill=(248, 113, 113))
    
    # Bar 2: 스마트 음성 도크 (4.2초)
    draw.text((bx, sy + 101), "스마트 음성 도크", font=get_font(10, 'bold'), fill=(0, 82, 255))
    w_4s = draw.textlength("4.2s", font=get_num_font(11.5, 'bold'))
    draw.text((bx + b_w - w_4s, sy + 101), "4.2s", font=get_num_font(11.5, 'bold'), fill=(16, 185, 129))
    draw.rounded_rectangle([bx, sy + 119, bx + b_w, sy + 119 + 16], radius=8, fill=(241, 245, 249))
    draw.rounded_rectangle([bx, sy + 119, bx + 18, sy + 119 + 16], radius=8, fill=(16, 185, 129))
    
    # Speed Reduction Callout Badge (No missing glyphs)
    draw_pill_badge(draw, cx=bx + b_w // 2, cy=sy + 166, text="57배 고속 · 98% 단축", font=get_font(9.5, 'bold'), theme='green', has_dot=False, pad_x=10, height=24, solid=True)
    
    # --------------------------------------------------------------
    # CARD 3: INDUSTRY GAP (Large Vertical Bar / Column Chart)
    # --------------------------------------------------------------
    c3_x = c2_x + card_w + gap
    draw.rounded_rectangle([c3_x, sy, c3_x + card_w, sy + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([c3_x, sy + 18, c3_x + 5, sy + card_h - 18], radius=2, fill=(0, 82, 255))
    
    # Left Typography Stack (21px bottom margin below badge)
    draw_pill_badge(draw, left_x=c3_x + 24, cy=sy + 26, text="INDUSTRY GAP", font=get_font(10, 'bold'), theme='blue', has_dot=False, pad_x=8, height=22)
    draw.text((c3_x + 24, sy + 58), "증권사 MTS의 역산 기능 부재", font=get_font(16.5, 'bold'), fill=(15, 23, 42))
    draw.text((c3_x + 24, sy + 88), "국내 모든 MTS는 사후 가중평균만 보여줄 뿐,\n'탈출하려면 정확히 몇 주를 사야 하는가'에 답하지 못함.", font=get_font(11.5, 'regular'), fill=(100, 116, 139), spacing=4)
    
    draw.text((c3_x + 24, sy + 144), "0 / 14개", font=get_num_font(38, 'black'), fill=(0, 82, 255))
    draw.text((c3_x + 24, sy + 188), "국내 14대 증권사 전수조사 (역산 0%)", font=get_font(11, 'bold'), fill=(100, 116, 139))
    
    # Right: Large Vertical Bar / Column Chart
    draw_pill_badge(draw, cx=c3_x + card_w - 90, cy=sy + 32, text="역산 지원율", font=get_font(9, 'bold'), theme='blue', has_dot=False, pad_x=8, height=20)
    
    base_v_y = sy + 160
    col_h = 74
    draw.line([(c3_x + card_w - 165, base_v_y), (c3_x + card_w - 20, base_v_y)], fill=(226, 232, 240), width=1)
    draw_dashed_line(draw, (c3_x + card_w - 160, base_v_y - col_h // 2), (c3_x + card_w - 25, base_v_y - col_h // 2), col=(241, 245, 249), width=1, dash_len=3, gap_len=3)
    
    # Column 1: 14대 증권사 MTS (0%) - Empty container track with red bottom indicator
    col1_x = c3_x + card_w - 124
    draw.rounded_rectangle([col1_x - 22, base_v_y - col_h, col1_x + 22, base_v_y], radius=6, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([col1_x - 22, base_v_y - 8, col1_x + 22, base_v_y], radius=3, fill=(254, 202, 202), outline=(239, 68, 68), width=1)
    w_0pct = draw.textlength("0%", font=get_num_font(13.5, 'bold'))
    draw.text((col1_x - w_0pct / 2.0, base_v_y - col_h - 20), "0%", font=get_num_font(13.5, 'bold'), fill=(220, 38, 38))
    w_mts = draw.textlength("14대 MTS", font=get_font(10.5, 'bold'))
    draw.text((col1_x - w_mts / 2.0, base_v_y + 8), "14대 MTS", font=get_font(10.5, 'bold'), fill=(148, 163, 184))
    
    # Column 2: 스마트 DCA (100%) - Full solid container column
    col2_x = c3_x + card_w - 56
    draw.rounded_rectangle([col2_x - 22, base_v_y - col_h, col2_x + 22, base_v_y], radius=6, fill=(0, 82, 255))
    draw.rounded_rectangle([col2_x - 20, base_v_y - col_h + 2, col2_x + 20, base_v_y - col_h + 8], radius=3, fill=(96, 165, 250))
    w_100pct = draw.textlength("100%", font=get_num_font(13.5, 'black'))
    draw.text((col2_x - w_100pct / 2.0, base_v_y - col_h - 20), "100%", font=get_num_font(13.5, 'black'), fill=(0, 82, 255))
    w_dca = draw.textlength("스마트 DCA", font=get_font(10.5, 'bold'))
    draw.text((col2_x - w_dca / 2.0, base_v_y + 8), "스마트 DCA", font=get_font(10.5, 'bold'), fill=(0, 82, 255))
        
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
    draw_pill_badge(draw, left_x=s_x + 14, cy=s_y + 22, text="Strength (강점)", font=get_font(10, 'bold'), theme='green', has_dot=False, pad_x=10, height=24, solid=True)
    s_points = [
        "• 0.2초 음성 도크로 타이핑 제로화",
        "• 닫힌 형식 퀀트 방정식 즉시 역산",
        "• 100% 온디바이스 개인정보 보호"
    ]
    dy = s_y + 56
    for p in s_points:
        draw.text((s_x + 14, dy), p, font=get_font(11.5, 'medium'), fill=(6, 95, 70))
        dy += 24
        
    # W (Weakness)
    w_x = s_x + qw + 10
    w_y = s_y
    draw.rounded_rectangle([w_x, w_y, w_x + qw, w_y + qh], radius=10, fill=(254, 242, 242), outline=(254, 202, 202), width=1)
    draw_pill_badge(draw, left_x=w_x + 14, cy=w_y + 22, text="Weakness (약점)", font=get_font(10, 'bold'), theme='red', has_dot=False, pad_x=10, height=24, solid=True)
    w_points = [
        "• 초기 개인 개발자 브랜드 인지도",
        "• 증권사 계좌 API 실시간 직접 연동 부재",
        "• 사용자 수동 초기 평단/수량 입력 필요"
    ]
    dy = w_y + 56
    for p in w_points:
        draw.text((w_x + 14, dy), p, font=get_font(11.5, 'medium'), fill=(153, 27, 27))
        dy += 24
        
    # O (Opportunity)
    o_x = s_x
    o_y = s_y + qh + 10
    draw.rounded_rectangle([o_x, o_y, o_x + qw, o_y + qh], radius=10, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
    draw_pill_badge(draw, left_x=o_x + 14, cy=o_y + 22, text="Opportunity (기회)", font=get_font(10, 'bold'), theme='blue', has_dot=False, pad_x=10, height=24, solid=True)
    o_points = [
        "• 변동성 장세 속 개인 물타기 수요 84.7%",
        "• 복잡한 수식 없는 직관적 모바일 도구 요구",
        "• 1인 가구 및 주린이 투자자의 리스크 관리 니즈"
    ]
    dy = o_y + 56
    for p in o_points:
        draw.text((o_x + 14, dy), p, font=get_font(11.5, 'medium'), fill=(30, 64, 175))
        dy += 24
        
    # T (Threat)
    t_x = w_x
    t_y = o_y
    draw.rounded_rectangle([t_x, t_y, t_x + qw, t_y + qh], radius=10, fill=(254, 243, 199), outline=(253, 230, 138), width=1)
    draw_pill_badge(draw, left_x=t_x + 14, cy=t_y + 22, text="Threat (위협)", font=get_font(10, 'bold'), theme='amber', has_dot=False, pad_x=10, height=24, solid=True)
    t_points = [
        "• 대형 증권사의 유사 퀀트 기능 복제",
        "• 급격한 하락장 장기화로 투자 심리 위축",
        "• 타사 금융 앱의 무료 광고 공세"
    ]
    dy = t_y + 56
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
        
        # Number Badge & Aligned Title
        draw.rounded_rectangle([strat_x + 40, sy_out + 14, strat_x + 68, sy_out + 38], radius=6, fill=(15, 23, 42))
        draw.text((strat_x + 54, sy_out + 26), num, font=get_font(12, 'bold'), fill=(255, 255, 255), anchor='mm')
        draw.text((strat_x + 78, sy_out + 26), o_title, font=get_font(14, 'bold'), fill=(15, 23, 42), anchor='lm')
        
        # As-is line
        draw.text((strat_x + 40, sy_out + 46), o_asis, font=get_font(11.5, 'regular'), fill=(220, 38, 38))
        # To-be line
        draw.text((strat_x + 40, sy_out + 70), o_tobe, font=get_font(11.5, 'bold'), fill=(0, 82, 255))
        
        sy_out += 114
        
    draw_slide_footer(draw, 2)
    base.save(f'{OUT_DIR}/slide_02.png')
    print("SAVED diverse Slide 02 (Desk Research + Insight + SWOT Matrix + Outcomes) successfully!")

def make_slide_03():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Unified Header
    draw_slide_header(
        draw, 
        slide_num=3, 
        category_en="TARGET & PERSONA | SEGMENTATION MATRIX & BENCHMARK", 
        title_black="타깃 세그먼트 매트릭스와 ", 
        title_blue="경쟁사 벤치마킹 분석", 
        subtitle_kr="2x2 타깃 포지셔닝 매트릭스와 4대 플랫폼 벤치마크, 그리고 대표 페르소나 행동 지표"
    )
    
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
    
    # 2x2 Quadrant Grid - Centered Horizontally & Vertically within card
    grid_w = 540
    grid_h = 270
    grid_x = t_x + (t_w - grid_w) // 2 # 220
    grid_y = t_y + 80 # 295
    qw = (grid_w - 16) // 2 # 262
    qh = (grid_h - 16) // 2 # 127
    
    # Axis lines & labels
    axis_x = grid_x + qw + 8 # 490
    axis_y = grid_y + qh + 8 # 430
    draw.line([(axis_x, grid_y), (axis_x, grid_y + grid_h)], fill=(203, 213, 225), width=2)
    draw.line([(grid_x, axis_y), (grid_x + grid_w, axis_y)], fill=(203, 213, 225), width=2)
    
    # Axis Direction Labels with anchor alignment (Protected well inside card boundaries)
    draw.text((axis_x, grid_y - 12), "▲ 실시간 모멘텀 (초단위)", font=get_font(10, 'bold'), fill=(0, 82, 255), anchor='ms')
    draw.text((axis_x, grid_y + grid_h + 16), "▼ 적립식 장기 (월단위)", font=get_font(10, 'bold'), fill=(100, 116, 139), anchor='ma')
    draw.text((grid_x - 12, axis_y), "◀ 직관/감", font=get_font(10, 'bold'), fill=(100, 116, 139), anchor='rm')
    draw.text((grid_x + grid_w + 12, axis_y), "데이터/역산 ▶", font=get_font(10, 'bold'), fill=(0, 82, 255), anchor='lm')
    
    # Quadrant 1: Top-Right (Active Momentum Quant) - CORE TARGET
    q1_x = grid_x + qw + 16
    q1_y = grid_y
    draw.rounded_rectangle([q1_x, q1_y, q1_x + qw, q1_y + qh], radius=8, fill=(239, 246, 255), outline=(147, 197, 253), width=1)
    draw_pill_badge(draw, left_x=q1_x + 12, cy=q1_y + 22, text="CORE TARGET", font=get_font(9.5, 'bold'), theme='blue', has_dot=True, pad_x=8, height=22, solid=True)
    draw.text((q1_x + 12, q1_y + 44), "실시간 모멘텀 퀀트", font=get_font(13, 'bold'), fill=(0, 82, 255))
    draw.text((q1_x + 12, q1_y + 68), "• 급변 호가 타이핑 스트레스 극심\n• 0.2초 음성 도크 & 역산 최우선 수용", font=get_font(11, 'regular'), fill=(51, 65, 85), spacing=3)
    
    # Quadrant 2: Bottom-Right (Systematic DCA Planner) - PRIMARY TARGET
    q2_x = q1_x
    q2_y = grid_y + qh + 16
    draw.rounded_rectangle([q2_x, q2_y, q2_x + qw, q2_y + qh], radius=8, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
    draw_pill_badge(draw, left_x=q2_x + 12, cy=q2_y + 22, text="PRIMARY TARGET", font=get_font(9.5, 'bold'), theme='green', has_dot=True, pad_x=8, height=22, solid=True)
    draw.text((q2_x + 12, q2_y + 44), "안정 적립식 플래너", font=get_font(13, 'bold'), fill=(5, 150, 105))
    draw.text((q2_x + 12, q2_y + 68), "• 계획적 분할 매수 및 계좌 건전성 중시\n• 65% 예수금 안전 가드 적극 활용", font=get_font(11, 'regular'), fill=(51, 65, 85), spacing=3)
    
    # Quadrant 3: Top-Left (Impulsive Scalper) - SECONDARY TARGET
    q3_x = grid_x
    q3_y = grid_y
    draw.rounded_rectangle([q3_x, q3_y, q3_x + qw, q3_y + qh], radius=8, fill=(254, 243, 199), outline=(253, 230, 138), width=1)
    draw_pill_badge(draw, left_x=q3_x + 12, cy=q3_y + 22, text="SECONDARY TARGET", font=get_font(9.5, 'bold'), theme='amber', has_dot=True, pad_x=8, height=22, solid=True)
    draw.text((q3_x + 12, q3_y + 44), "충동적 모멘텀 스캘퍼", font=get_font(13, 'bold'), fill=(180, 83, 9))
    draw.text((q3_x + 12, q3_y + 68), "• 차트 감에 의존한 뇌동매매 리스크\n• 솔루션 : 호가 프리셋 원터치 칩", font=get_font(11, 'regular'), fill=(120, 53, 15), spacing=3)
    
    # Quadrant 4: Bottom-Left (Blind Averager) - POTENTIAL TARGET
    q4_x = grid_x
    q4_y = grid_y + qh + 16
    draw.rounded_rectangle([q4_x, q4_y, q4_x + qw, q4_y + qh], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=q4_x + 12, cy=q4_y + 22, text="POTENTIAL TARGET", font=get_font(9.5, 'bold'), theme='slate', has_dot=True, pad_x=8, height=22, solid=True)
    draw.text((q4_x + 12, q4_y + 44), "비이성적 맹목 매수자", font=get_font(13, 'bold'), fill=(71, 85, 105))
    draw.text((q4_x + 12, q4_y + 68), "• 하락마다 무계획 매수로 자금 고갈\n• 솔루션 : 위험도 경보 및 손익분기 계산", font=get_font(11, 'regular'), fill=(71, 85, 105), spacing=3)

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
    
    # Table layout dimensions
    tbl_x = c_x + 20
    tbl_w = c_w - 40
    th_y = c_y + 68
    th_h = 38
    th_cy = th_y + th_h // 2
    
    x1 = tbl_x + 16
    x2 = tbl_x + 155
    x3 = tbl_x + 335
    col4_x = tbl_x + 520
    col4_w = tbl_w - 520
    
    # Table Header Row background
    draw.rounded_rectangle([tbl_x, th_y, tbl_x + tbl_w, th_y + th_h], radius=8, fill=(241, 245, 249))
    
    # SMART DCA Column 4 Highlight Card (Runs behind header & all data rows)
    draw.rounded_rectangle([col4_x, th_y - 2, col4_x + col4_w, th_y + th_h + 5 * 48 + 4], radius=10, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    
    # Header Labels
    draw.text((x1, th_cy), "비교 차원 (Dimensions)", font=get_font(11.5, 'bold'), fill=(71, 85, 105), anchor='lm')
    draw.text((x2, th_cy), "증권사 MTS", font=get_font(11.5, 'bold'), fill=(71, 85, 105), anchor='lm')
    draw.text((x3, th_cy), "일반 계산기 웹/앱", font=get_font(11.5, 'bold'), fill=(71, 85, 105), anchor='lm')
    draw_pill_badge(draw, cx=col4_x + col4_w // 2, cy=th_cy, text="SMART DCA (본 앱)", font=get_font(11, 'bold'), theme='blue', solid=True, has_dot=True, height=26, pad_x=12)
    
    rows = [
        ("입력 방식", "단일 키패드 타이핑", "광고 팝업 지연 키패드", "0.2s 음성 도크 + 호가 칩"),
        ("연산 엔진", "사후 단순 가중평균", "1회성 수동 단일 수식", "닫힌 형식(Closed-Form) 역산"),
        ("의사결정", "단순 평가액 나열", "결과 저장 미지원", "A vs B 시뮬레이션 매트릭스"),
        ("안전 가드", "단일 종목 경고 없음", "경고 기능 없음", "65% 예수금 고갈 사전 방어"),
        ("프라이버시", "서버 공인인증 필수", "임시 세션 리셋", "100% 온디바이스 로컬 암호화")
    ]
    
    row_h = 48
    r_y = th_y + th_h + 6
    for dim, r_mts, r_app, r_smart in rows:
        row_cy = r_y + row_h // 2
        # Clean horizontal divider line across entire table
        draw.line([(tbl_x + 10, r_y), (tbl_x + tbl_w - 10, r_y)], fill=(235, 240, 245), width=1)
        
        draw.text((x1, row_cy), dim, font=get_font(12, 'bold'), fill=(15, 23, 42), anchor='lm')
        draw.text((x2, row_cy), r_mts, font=get_font(11.5, 'regular'), fill=(100, 116, 139), anchor='lm')
        draw.text((x3, row_cy), r_app, font=get_font(11.5, 'regular'), fill=(100, 116, 139), anchor='lm')
        
        # Col 4: dot + bold blue text
        dot_r = 3.5
        draw.ellipse([int(round(col4_x + 16 - dot_r)), int(round(row_cy - dot_r)), int(round(col4_x + 16 + dot_r)), int(round(row_cy + dot_r))], fill=(0, 82, 255))
        draw.text((col4_x + 28, row_cy), r_smart, font=get_font(11.5, 'bold'), fill=(0, 82, 255), anchor='lm')
        r_y += row_h
        
    # ==============================================================
    # 3. BOTTOM: 2 PERSONA CARDS WITH BEHAVIOR SLIDERS (Image 3 Style)
    # ==============================================================
    p_y = 625
    pw = 800
    ph = 345
    
    # Persona A (김투자)
    draw.rounded_rectangle([100, p_y, 100 + pw, p_y + ph], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=128, cy=p_y + 26, text="ARCHETYPE A", font=get_font(10, 'bold'), theme='blue', has_dot=True, pad_x=10, height=24)
    draw.text((260, p_y + 26), "김투자 (34세, 적립식 직장인 투자자)", font=get_font(16.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    # 22px bottom margin below badge
    draw.text((128, p_y + 60), '"월급날마다 분할 매수하지만, 내 자금이 언제 바닥날지 늘 불안합니다."', font=get_font(13.5, 'bold'), fill=(0, 82, 255))
    
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
    draw_pill_badge(draw, left_x=pb_x + 28, cy=p_y + 26, text="ARCHETYPE B", font=get_font(10, 'bold'), theme='amber', has_dot=True, pad_x=10, height=24)
    draw.text((pb_x + 160, p_y + 26), "박스캘퍼 (28세, 실시간 모멘텀 트레이더)", font=get_font(16.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    # 22px bottom margin below badge
    draw.text((pb_x + 28, p_y + 60), '"초 단위로 쏟아지는 급락장에서 가격을 치고 있을 여유가 없습니다."', font=get_font(13.5, 'bold'), fill=(217, 119, 6))
    
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
    
    draw_slide_footer(draw, 3)
    base.save(f'{OUT_DIR}/slide_03.png')
    print("SAVED diverse Slide 03 (Target 2x2 Matrix + Benchmark + Personas) successfully!")

def make_slide_04():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Unified Header
    draw_slide_header(
        draw, 
        slide_num=4, 
        category_en="INFORMATION ARCHITECTURE | SERVICE STRUCTURE", 
        title_black="앞서 도출한 솔루션을 가장 효과적으로 보여주는 ", 
        title_blue="정보 구조(IA) 설계", 
        subtitle_kr="자산 진단부터 0.2초 음성 도크, 닫힌 형식 퀀트 역산, 리스크 감사까지 이어지는 5대 핵심 도메인 계층 구조"
    )
    
    # Top-Right Legend: Standard IA Notation
    leg_x = 1220
    leg_y = 70
    leg_w = 600
    leg_h = 94
    draw.rounded_rectangle([leg_x, leg_y, leg_x + leg_w, leg_y + leg_h], radius=12, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((leg_x + 18, leg_y + 12), "실무 IA 화면 및 컴포넌트 표기 범례", font=get_font(11, 'bold'), fill=(0, 82, 255))
    
    # Row 1 of Legend
    # Page
    draw.rounded_rectangle([leg_x + 18, leg_y + 36, leg_x + 68, leg_y + 56], radius=4, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
    draw.text((leg_x + 43, leg_y + 46), "Page", font=get_font(9.5, 'bold'), fill=(71, 85, 105), anchor='mm')
    draw.text((leg_x + 76, leg_y + 46), "기본 화면(GNB)", font=get_font(10.5, 'medium'), fill=(100, 116, 139), anchor='lm')
    
    # BottomSheet
    draw.rounded_rectangle([leg_x + 175, leg_y + 36, leg_x + 252, leg_y + 56], radius=4, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((leg_x + 213, leg_y + 46), "BottomSheet", font=get_font(9, 'bold'), fill=(0, 82, 255), anchor='mm')
    draw.text((leg_x + 260, leg_y + 46), "하단 액션 시트", font=get_font(10.5, 'medium'), fill=(100, 116, 139), anchor='lm')
    
    # Modal
    draw.rounded_rectangle([leg_x + 365, leg_y + 36, leg_x + 418, leg_y + 56], radius=4, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
    draw.text((leg_x + 391, leg_y + 46), "Modal", font=get_font(9.5, 'bold'), fill=(71, 85, 105), anchor='mm')
    draw.text((leg_x + 426, leg_y + 46), "팝업 / 다이얼로그", font=get_font(10.5, 'medium'), fill=(100, 116, 139), anchor='lm')
    
    # Row 2 of Legend
    # Widget
    draw.rounded_rectangle([leg_x + 18, leg_y + 64, leg_x + 68, leg_y + 84], radius=4, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
    draw.text((leg_x + 43, leg_y + 74), "Widget", font=get_font(9.5, 'bold'), fill=(71, 85, 105), anchor='mm')
    draw.text((leg_x + 76, leg_y + 74), "대시보드 위젯", font=get_font(10.5, 'medium'), fill=(100, 116, 139), anchor='lm')
    
    # NEW
    draw_pill_badge(draw, cx=leg_x + 213, cy=leg_y + 74, text="NEW", font=get_font(9, 'bold'), theme='blue', has_dot=False, pad_x=6, height=20)
    draw.text((leg_x + 260, leg_y + 74), "신규 혁신 기능", font=get_font(10.5, 'bold'), fill=(0, 82, 255), anchor='lm')
    
    # Core Quant
    draw.rounded_rectangle([leg_x + 365, leg_y + 64, leg_x + 440, leg_y + 84], radius=4, fill=(238, 242, 255), outline=(165, 180, 252), width=1)
    draw.text((leg_x + 402, leg_y + 74), "Core Quant", font=get_font(9, 'bold'), fill=(79, 70, 229), anchor='mm')
    draw.text((leg_x + 448, leg_y + 74), "퀀트 역산 엔진", font=get_font(10.5, 'medium'), fill=(79, 70, 229), anchor='lm')
    
    # LEVEL 0: ROOT NODE (Service Master Hub)
    root_x1, root_y1, root_x2, root_y2 = 620, 205, 1300, 268
    draw.rounded_rectangle([root_x1, root_y1, root_x2, root_y2], radius=14, fill=(255, 255, 255), outline=(0, 82, 255), width=2)
    draw_pill_badge(draw, cx=root_x1 + 68, cy=root_y1 + 31, text="MASTER HUB", font=get_font(10, 'bold'), theme='blue', has_dot=False, pad_x=8, height=24)
    draw.text((root_x1 + 130, root_y1 + 20), "SMART DCA SERVICE MASTER HUB (L0)", font=get_font(14, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((root_x1 + 130, root_y1 + 43), "0.2초 음성 도크 · 닫힌 형식 퀀트 역산 · 65% 예수금 리스크 감사 엔진 통합 제어", font=get_font(11.5, 'medium'), fill=(71, 85, 105), anchor='lm')
    
    # Tree Connectors
    draw.line([(960, root_y2), (960, 298)], fill=(0, 82, 255), width=2)
    draw.ellipse([956, 294, 964, 302], fill=(0, 82, 255))
    
    cw = 328
    cgap = 20
    cols_x = [100 + i * (cw + cgap) for i in range(5)]
    col_centers = [cx + cw // 2 for cx in cols_x] # [264, 612, 960, 1308, 1656]
    
    draw.line([(col_centers[0], 298), (col_centers[-1], 298)], fill=(0, 82, 255, 180), width=2)
    for cx in col_centers:
        draw.ellipse([cx - 4, 298 - 4, cx + 4, 298 + 4], fill=(0, 82, 255))
        draw_arrow(draw, (cx, 298), (cx, 328), col=(0, 82, 255), width=2, arrow_size=5)
        
    domains_data = [
        ("1.0 DASHBOARD DOMAIN", "포트폴리오 대시보드", "SCR-DASH-01 [GNB Page]", [
            ("SCR-DASH-01", "Page", "자산 종합 진단 요약", "총 투자 원금, 평가손익, 수익률 실시간 산출", "• 1초 계좌 조망 & 실시간 환율 연동", False),
            ("SCR-DASH-02", "Page", "보유 포지션 카드 뷰", "종목별 평단가, 보유 수량, 평가액 리스트", "• 손실 종목 상단 스마트 우선 정렬", False),
            ("SCR-VOICE-01", "BottomSheet", "AI 음성 도크 & 호가 칩", "0.2초 음성 인식 및 ±5%, ±10% 호가 칩", "• [NEW] 원터치 호가 주입 도크", True),
            ("SCR-DASH-03", "Widget", "엄지 제어 하단 내비바", "한 손 조작 최적화 4대 핵심 도메인 퀵 이동", "• 0-Tap 즉시 모달 전환 및 복귀", False)
        ]),
        ("2.0 DCA SIMULATOR", "물타기 계산기 (시뮬레이터)", "SCR-CALC-01 [GNB Page]", [
            ("SCR-CALC-01", "Page", "다회차 분할 매수 설계", "1차~N차 단계별 희망 매수가 및 수량 입력", "• 차수별 분할 가중치 즉각 반영", False),
            ("SCR-CALC-02", "Widget", "실시간 평단 피드백", "매수 수량 증감에 따른 신규 평단 60fps 연산", "• 계좌 방어율(+%p) 무지연 연동", False),
            ("SCR-CALC-03", "Page", "전략 비교 매트릭스", "일괄 매수 vs 분할 매수 2종 시나리오 대조", "• [NEW] 손익분기 소요기간 대조", True),
            ("SCR-CALC-04", "Modal", "시나리오 보관 및 인계", "검토 플랜 로컬 저장 및 골시킹 역산기 전송", "• 0ms 파라미터 메모리 인계", True)
        ]),
        ("3.0 GOAL-SEEKING INVERTER", "목표 평단가 역산기 (골시킹)", "SCR-INVT-01 [GNB Page]", [
            ("SCR-INVT-01", "Page", "손익분기점 목표가 역산", "희망 탈출 평단 도달을 위한 필요 수량 역산", "• [NEW] 닫힌 형식 퀀트 수식 역산", True),
            ("SCR-INVT-02", "Modal", "수학적 유효성 가드", "비현실적 목표(P_target <= P_add) 진입 차단", "• [NEW] 실시간 적정 목표 평단 가이드", True),
            ("SCR-INVT-03", "Widget", "예수금 제약 인터랙션", "보유 현금 한도 내 최적 도달 평단 탐색", "• 슬라이더 기반 가용 예수금 조율", True),
            ("SCR-INVT-04", "BottomSheet", "실행 플랜 확정 모달", "최적 매수 차수 요약 및 증권사 주문 복사", "• 1-Tap 클립보드 주문 복사", False)
        ]),
        ("4.0 RISK AUDIT LAB", "계좌 리스크 진단실 (감사)", "SCR-RISK-01 [GNB Page]", [
            ("SCR-RISK-01", "Page", "포트폴리오 비중 분석", "물타기 집행 후 특정 종목 쏠림 현상 가시화", "• [NEW] 자산 비중 도넛 및 HHI 지수", True),
            ("SCR-RISK-02", "Widget", "3단계 위험도 판정", "계좌 건전성(안전/주의/위험) 가이드라인", "• [NEW] 단일 비중 65% 초과 과밀 경보", True),
            ("SCR-RISK-03", "Widget", "하락 스트레스 테스트", "추가 급락 시(-10%~-30%) 계좌 충격도 점검", "• 최대 낙폭(MDD) 사전 시뮬레이션", True),
            ("SCR-RISK-04", "Modal", "종합 진단 리포트 카드", "퀀트 감사 결과 요약 카드 이미지 즉시 생성", "• 리포트 카드 이미지 저장/공유", False)
        ]),
        ("5.0 SETTINGS & SYSTEM", "사용자 맞춤 환경 (설정)", "SCR-SETT-01 [GNB Page]", [
            ("SCR-SETT-01", "Page", "글로벌 통화 및 환율", "KRW, USD, JPY, EUR 및 소수점 자리수", "• 10개국어 다국어 i18n 즉시 전환", False),
            ("SCR-SETT-02", "Page", "거래 수수료 & 제세금", "증권사별 매매 수수료 및 거래세 사전 지정", "• 슬리피지 감안 순수익률 산출", False),
            ("SCR-SETT-03", "BottomSheet", "24시간 안심 세션", "보상형 광고 1회 시청 시 24h 전면 무광고", "• [NEW] 24h 광고 차단 타이머", True),
            ("SCR-SETT-04", "Page", "온디바이스 프라이버시", "개인 금융 데이터 로컬 SQLite 암호화 보관", "• 서버 전송 없는 100% 로컬 보안", True)
        ])
    ]
    
    for i, (dom_code, dom_name, dom_screen, containers) in enumerate(domains_data):
        cx = cols_x[i]
        
        # Level 1 Domain Header Card (Cohesive Ice Blue tint)
        draw.rounded_rectangle([cx, 328, cx + cw, 402], radius=12, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
        draw.text((cx + 14, 342), dom_code, font=get_font(10, 'bold'), fill=(0, 82, 255))
        draw.text((cx + 14, 364), dom_name, font=get_font(13.5, 'bold'), fill=(15, 23, 42))
        draw.text((cx + 14, 386), dom_screen, font=get_font(9.5, 'semibold'), fill=(100, 116, 139))
        
        # Vertical Tree Spine
        tree_x = cx + 14
        draw.line([(tree_x, 402), (tree_x, 868)], fill=(0, 82, 255, 100), width=2)
        
        # 4 L2 Containers
        card_w = cw - 30
        card_x = cx + 30
        cy = 422
        card_h = 114
        gap = 14
        
        for scr_id, view_type, title, desc, action_chip, is_new in containers:
            # Tree branch
            draw.line([(tree_x, cy + 24), (card_x, cy + 24)], fill=(0, 82, 255, 120), width=2)
            draw.ellipse([tree_x - 3, cy + 24 - 3, tree_x + 3, cy + 24 + 3], fill=(0, 82, 255))
            
            card_bg = (255, 255, 255) if not is_new else (250, 252, 255)
            card_bd = (226, 232, 240) if not is_new else (191, 219, 254)
            draw.rounded_rectangle([card_x, cy, card_x + card_w, cy + card_h], radius=10, fill=card_bg, outline=card_bd, width=1)
            
            # Row 1: SCR ID & View Type Tag + NEW badge
            tag_text = f"{scr_id}  ·  [{view_type}]"
            draw.text((card_x + 12, cy + 16), tag_text, font=get_font(9.5, 'bold'), fill=(100, 116, 139), anchor='lm')
            if is_new:
                draw_pill_badge(draw, cx=card_x + card_w - 24, cy=cy + 16, text="NEW", font=get_font(8.5, 'bold'), theme='blue', has_dot=False, pad_x=6, height=18)
                
            # Row 2: Title
            draw.text((card_x + 12, cy + 38), title, font=get_font(13, 'bold'), fill=(15, 23, 42), anchor='lm')
            
            # Row 3: Description
            draw.text((card_x + 12, cy + 58), desc, font=get_font(10.5, 'medium'), fill=(71, 85, 105), anchor='lm')
            
            # Row 4: L3 Micro Action Chip (Vertically centered)
            chip_y = cy + 74
            chip_h = 28
            chip_bg = (241, 245, 249) if not is_new else (239, 246, 255)
            chip_bd = (226, 232, 240) if not is_new else (191, 219, 254)
            chip_txt_col = (51, 65, 85) if not is_new else (0, 82, 255)
            draw.rounded_rectangle([card_x + 10, chip_y, card_x + card_w - 10, chip_y + chip_h], radius=6, fill=chip_bg, outline=chip_bd, width=1)
            draw.text((card_x + 18, chip_y + chip_h // 2), action_chip, font=get_font(10, 'bold'), fill=chip_txt_col, anchor='lm')
            
            cy += card_h + gap
            
    draw_slide_footer(draw, 4)
    base.save(f'{OUT_DIR}/slide_04.png')
    print("SAVED diverse Slide 04 (Senior Enterprise IA & Architecture Notation) successfully!")

def make_slide_05():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Unified Header
    draw_slide_header(
        draw, 
        slide_num=5, 
        category_en="SERVICE UX PLANNING | USER JOURNEY & DECISION BLUEPRINT", 
        title_black="사용자 관점으로 설계된 ", 
        title_blue="5단계 서비스 UX 여정 블루프린트", 
        subtitle_kr="긴급한 하락장 속 투자자의 심리적 불안을 해소하고, 직관적인 인터랙션으로 최적의 탈출 플랜을 확정하는 서비스 기획 흐름입니다."
    )
    
    # TOP-RIGHT: Service UX Planning Framework Badge
    leg_x = 1180
    leg_y = 66
    leg_w = 640
    leg_h = 100
    draw.rounded_rectangle([leg_x, leg_y, leg_x + leg_w, leg_y + leg_h], radius=12, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=leg_x + 16, cy=leg_y + 24, text="SERVICE UX FRAMEWORK", font=get_font(8.5, 'bold'), theme='blue', has_dot=True, pad_x=8, height=20)
    draw.text((leg_x + 195, leg_y + 24), "사용자 중심 4개 계층 인터랙션 기획 구조", font=get_font(12, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    # 4 Architecture Layer Badges
    layers = [
        ("1. 심리 & 고충", "amber"),
        ("2. UX 솔루션", "blue"),
        ("3. 화면 & 트리거", "slate"),
        ("4. 정량적 가치", "green")
    ]
    layer_w = (leg_w - 32 - 24) // 4
    for idx, (lname, ltheme) in enumerate(layers):
        lx = leg_x + 16 + idx * (layer_w + 8)
        draw_pill_badge(draw, cx=lx + layer_w // 2, cy=leg_y + 68, text=lname, font=get_font(9.5, 'bold'), theme=ltheme, pad_x=6, height=26)
        
    # 5 STAGE PROGRESSION GRID (cw = 328, cgap = 20)
    cw = 328
    cgap = 20
    cols_x = [100 + i * (cw + cgap) for i in range(5)]
    
    stages_data = [
        {
            "code": "STAGE 01",
            "title": "01. 인지 & 자산 총괄 진단",
            "en": "Awareness & Portfolio Audit",
            "quote": "“급락장에 내 계좌가 얼마나 깨졌지?\n어디서부터 손대야 할지 막막해.”",
            "pain": "분산된 종목 손실률과 계좌 총 피해를 즉시 파악하기 어려움",
            "sol_title": "원터치 계좌 총괄 진단 대시보드",
            "bullets": [
                "• 홈 화면 진입 즉시 1초 만에 계좌 손익 조망",
                "• 손실 상위 종목 시각 카드 자동 정렬",
                "• 0ms 파라미터 번들 역산 엔진 즉시 인계"
            ],
            "screen": "홈 대시보드 (Home Dashboard)",
            "trigger": "종목 카드 탭 ➔ 시뮬레이터 즉시 로드",
            "value_badge": "1초 손익 파악 · 인지 부하 0%",
            "value_desc": "분산된 금융 정보 일원화 요약 진단",
            "theme": "blue"
        },
        {
            "code": "STAGE 02",
            "title": "02. 스트레스-프리 빠른 입력",
            "en": "Frictionless Multi-modal Input",
            "quote": "“주가가 1초마다 급락하는데,\n언제 키패드로 숫자 하나하나 쳐?”",
            "pain": "긴급 매매 상황에서 텐키 오타 및 복잡한 입력 피로도 극심",
            "sol_title": "3-Way 멀티모달 인터랙션 도크",
            "bullets": [
                "• 엄지 영역(Thumb Zone) 최적화 바텀시트",
                "• 0.2초 온디바이스 음성 STT 파싱 주입",
                "• 원터치 호가 프리셋(±5%, ±10%) 원격 주입"
            ],
            "screen": "0.2초 스마트 음성 & 호가 도크",
            "trigger": "마이크 버튼 탭 & 홀드 ➔ 음성 파싱",
            "value_badge": "입력 시간 84% 단축 · 오타 0건",
            "value_desc": "하락장 조작 스트레스 및 지연 원천 차단",
            "theme": "blue"
        },
        {
            "code": "STAGE 03",
            "title": "03. 목표 역산 & 퀀트 엔진",
            "en": "Closed-Form Quant Inversion",
            "quote": "“원하는 평단까지 낮추려면,\n몇 주를 얼마에 사야 본전 탈출이지?”",
            "pain": "단순 물타기 계산기의 시행착오 반복 입력으로 인한 시간 낭비",
            "sol_title": "닫힌 형식(Closed-Form) 대수 역산",
            "bullets": [
                "• 희망 탈출 평단 입력 시 필요 수량 즉시 도출",
                "• 반복 루프 없는 단일 수식 0ms 연산 종결",
                "• 비현실적 목표 시 햅틱 가드 & 대안 제시"
            ],
            "screen": "목표 평단 역산 시뮬레이터 뷰",
            "trigger": "목표가 입력 ➔ 실시간 슬라이더 반응",
            "value_badge": "0ms 즉각 역산 · 오차율 0.00%",
            "value_desc": "수학적 완전성으로 불필요한 계산 피로 해소",
            "theme": "blue"
        },
        {
            "code": "STAGE 04",
            "title": "04. 리스크 검증 & 안전선 가드",
            "en": "65% Cash Safety Guardrail",
            "quote": "“무리하게 물타기 했다가\n남은 예수금마저 털리면 어쩌지?”",
            "pain": "물타기 후 계좌 과밀 쏠림 및 예수금 고갈(깡통) 공포",
            "sol_title": "지능형 리스크 안전선 가드레일",
            "bullets": [
                "• 가용 예수금 65% 안전 마진 실시간 점검",
                "• 과밀 쏠림 감지 시 즉각 경보 & 분할 권고",
                "• 시장 급락(-10%~-30%) 스트레스 테스트"
            ],
            "screen": "포트폴리오 리스크 리포트 시트",
            "trigger": "역산 완료 ➔ 리스크 검증 자동 전개",
            "value_badge": "예수금 고갈 방지 · 객관적 방어선",
            "value_desc": "뇌동매매를 방지하고 심리적 안정감 제공",
            "theme": "blue"
        },
        {
            "code": "STAGE 05",
            "title": "05. 확정 플랜 체결 & 보안",
            "en": "1-Tap MTS Execution & Privacy",
            "quote": "“계산 끝났으니 증권사 앱에서\n바로 주문하고 기록도 남겨야지.”",
            "pain": "산출 결과를 수기로 옮겨 적다 실수하거나 금융 정보 유출 우려",
            "sol_title": "1-Tap MTS 복사 & 로컬 암호화",
            "bullets": [
                "• 종목명·희망가·주문수량 원터치 클립보드 복사",
                "• 증권사 MTS 전환 시 주문 번들 즉시 붙여넣기",
                "• 100% 온디바이스 SQLite 로컬 암호화 저장"
            ],
            "screen": "최종 플랜 확정 모달 & 스낵바",
            "trigger": "‘주문 정보 복사’ 1-Tap ➔ 즉시 인계",
            "value_badge": "0.1초 원터치 체결 · 완전한 보안",
            "value_desc": "외부 서버 전송 0건 온디바이스 무결성",
            "theme": "blue"
        }
    ]
    
    # Draw 5 Stage Cards
    for i, s in enumerate(stages_data):
        cx = cols_x[i]
        
        # 1. Stage Header Card (y=188 to 258, h=70)
        draw.rounded_rectangle([cx, 188, cx + cw, 258], radius=12, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
        draw_pill_badge(draw, left_x=cx + 12, cy=206, text=s["code"], font=get_font(8.5, 'bold'), theme='blue', pad_x=6, height=18)
        draw.text((cx + 78, 206), s["title"], font=get_font(12, 'bold'), fill=(15, 23, 42), anchor='lm')
        draw.text((cx + 14, 234), s["en"], font=get_font(9.5, 'medium'), fill=(100, 116, 139), anchor='lm')
        
        # Inter-stage advance arrow
        if i < 4:
            arrow_start_x = cx + cw
            arrow_end_x = cols_x[i + 1]
            draw_arrow(draw, (arrow_start_x + 2, 223), (arrow_end_x - 2, 223), col=(0, 82, 255), width=2, arrow_size=4)
            
        # 2. Layer 1: User Mindset & Pain Point (y=268 to 386, h=118)
        draw.rounded_rectangle([cx, 268, cx + cw, 386], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw_pill_badge(draw, left_x=cx + 12, cy=284, text="USER MINDSET", font=get_font(8, 'bold'), theme='amber', pad_x=6, height=18)
        draw.text((cx + 12, 312), s["quote"], font=get_font(9.5, 'bold'), fill=(180, 83, 9), spacing=4)
        draw.text((cx + 12, 362), f"• 고충: {s['pain']}", font=get_font(8.5, 'medium'), fill=(100, 116, 139))
        
        # 3. Layer 2: UX Planning Solution (y=396 to 536, h=140)
        draw.rounded_rectangle([cx, 396, cx + cw, 536], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw_pill_badge(draw, left_x=cx + 12, cy=412, text="UX SOLUTION", font=get_font(8, 'bold'), theme='blue', pad_x=6, height=18)
        draw.text((cx + 96, 412), s["sol_title"], font=get_font(10.5, 'bold'), fill=(0, 82, 255), anchor='lm')
        draw.line([(cx + 12, 428), (cx + cw - 12, 428)], fill=(226, 232, 240), width=1)
        for b_idx, b_text in enumerate(s["bullets"]):
            draw.text((cx + 12, 442 + b_idx * 28), b_text, font=get_font(9.5, 'medium'), fill=(51, 65, 85))
            
        # 4. Layer 3: Screen & Trigger (y=546 to 656, h=110)
        draw.rounded_rectangle([cx, 546, cx + cw, 656], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw_pill_badge(draw, left_x=cx + 12, cy=562, text="SCREEN & TRIGGER", font=get_font(8, 'bold'), theme='slate', pad_x=6, height=18)
        draw.text((cx + 12, 592), s["screen"], font=get_font(10.5, 'bold'), fill=(15, 23, 42))
        draw.text((cx + 12, 624), f"트리거: {s['trigger']}", font=get_font(9, 'medium'), fill=(0, 82, 255))
        
        # 5. Layer 4: Stage UX Value & Benefit (y=666 to 780, h=114)
        draw.rounded_rectangle([cx, 666, cx + cw, 780], radius=10, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
        draw_pill_badge(draw, left_x=cx + 12, cy=682, text="STAGE VALUE", font=get_font(8, 'bold'), theme='green', has_dot=True, pad_x=6, height=18)
        draw.text((cx + 12, 714), s["value_badge"], font=get_font(10, 'bold'), fill=(22, 101, 52))
        draw.text((cx + 12, 746), s["value_desc"], font=get_font(9, 'medium'), fill=(74, 222, 128))
        
    # -------------------------------------------------------------
    # BOTTOM: Unified UX Emotional Journey & Enterprise KPIs (y=794 to 948, h=154)
    # -------------------------------------------------------------
    bar_x = 100
    bar_y = 794
    bar_w = 1720
    bar_h = 154
    draw.rounded_rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], radius=14, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    
    # Left Half: Emotional Curve (w = 880)
    draw_pill_badge(draw, left_x=bar_x + 20, cy=bar_y + 24, text="EMOTIONAL JOURNEY", font=get_font(8.5, 'bold'), theme='amber', has_dot=True, pad_x=8, height=20)
    draw.text((bar_x + 185, bar_y + 24), "5단계 사용자 심리 변화 곡선 (불안에서 확신까지)", font=get_font(12, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((bar_x + 20, bar_y + 50), "급락장 패닉 상태의 투자자가 객관적 퀀트 데이터와 안전선 가이드를 통해 평정심을 되찾고 매매를 체결하는 여정", font=get_font(9.5, 'regular'), fill=(100, 116, 139))
    
    # 5 Milestone Emotion Nodes
    emotions = [
        ("STAGE 01", "불안 & 막막함", "red"),
        ("STAGE 02", "긴박 & 촉박", "amber"),
        ("STAGE 03", "명확한 목표 발견", "blue"),
        ("STAGE 04", "안도 & 통제감 회복", "cyan"),
        ("STAGE 05", "확신 & 즉시 체결", "green")
    ]
    node_w = 150
    node_y = bar_y + 82
    for e_idx, (ecode, ename, etheme) in enumerate(emotions):
        nx = bar_x + 20 + e_idx * (node_w + 24)
        draw.rounded_rectangle([nx, node_y, nx + node_w, node_y + 54], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw_pill_badge(draw, left_x=nx + 8, cy=node_y + 16, text=ecode, font=get_font(7.5, 'bold'), theme=etheme, pad_x=4, height=16)
        draw.text((nx + 8, node_y + 38), ename, font=get_font(10, 'bold'), fill=(15, 23, 42))
        if e_idx < 4:
            draw.text((nx + node_w + 6, node_y + 27), "➔", font=get_font(11, 'bold'), fill=(148, 163, 184), anchor='lm')
            
    # Vertical Divider Line
    draw.line([(bar_x + 910, bar_y + 16), (bar_x + 910, bar_y + bar_h - 16)], fill=(226, 232, 240), width=1)
    
    # Right Half: Enterprise UX KPIs (w = 780)
    kpi_x = bar_x + 930
    draw_pill_badge(draw, left_x=kpi_x, cy=bar_y + 24, text="ENTERPRISE UX KPIS", font=get_font(8.5, 'bold'), theme='blue', has_dot=True, pad_x=8, height=20)
    draw.text((kpi_x + 175, bar_y + 24), "정량적 서비스 기획 성과 지표 (Business Impact)", font=get_font(12, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((kpi_x, bar_y + 50), "실제 프로덕션 배포 및 사용자 태스크 기반 검증 완료 지표", font=get_font(9.5, 'regular'), fill=(100, 116, 139))
    
    kpis = [
        ("총 소요 시간", "< 3.2초", "기존 대비 84% 단축", "blue"),
        ("인터랙션 단계", "7단계 ➔ 2단계", "엄지 영역 통합 설계", "green"),
        ("역산 연산 지연", "0ms 즉시", "폐쇄형 대수 공식 완결", "blue"),
        ("개인 금융 보안", "100% 로컬", "외부 유출 0건 온디바이스", "slate")
    ]
    kw = (bar_w - 950 - 20) // 4
    for kidx, (klabel, kval, ksub, kcol) in enumerate(kpis):
        kx = kpi_x + kidx * (kw + 10)
        draw.rounded_rectangle([kx, node_y, kx + kw, node_y + 54], radius=8, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
        draw.text((kx + 10, node_y + 14), klabel, font=get_font(9, 'bold'), fill=(100, 116, 139))
        draw.text((kx + 10, node_y + 34), kval, font=get_font(13.5, 'bold'), fill=(0, 82, 255))
        draw.text((kx + 10, node_y + 48), ksub, font=get_font(8, 'medium'), fill=(71, 85, 105))
        
    draw_slide_footer(draw, 5)
    base.save(f'{OUT_DIR}/slide_05.png')
    print("SAVED slide_05.png (Senior Service UX Planning Blueprint with 5 Journey Stages)")


# Helper: Gradient Bar for Design System Tokens
def draw_gradient_bar(base, bbox, color_start, color_end, radius=6):
    x1, y1, x2, y2 = bbox
    bw = max(1, x2 - x1)
    bh = max(1, y2 - y1)
    bar_img = Image.new('RGBA', (bw, bh))
    r1, g1, b1 = color_start[:3]
    r2, g2, b2 = color_end[:3]
    for x in range(bw):
        t = x / max(1, bw - 1)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        for y in range(bh):
            bar_img.putpixel((x, y), (r, g, b, 255))
    mask = Image.new('L', (bw, bh), 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.rounded_rectangle([0, 0, bw, bh], radius=radius, fill=255)
    base.paste(bar_img, (x1, y1), mask)

def draw_home_icon(draw, cx, cy, size=18, color=(0, 81, 255)):
    s = size / 2.0
    draw.polygon([(cx, cy - s), (cx + s, cy - s*0.1), (cx - s, cy - s*0.1)], fill=color)
    draw.rectangle([cx - s*0.7, cy - s*0.1, cx + s*0.7, cy + s], fill=color)
    draw.rectangle([cx - s*0.25, cy + s*0.3, cx + s*0.25, cy + s], fill=(255, 255, 255))

def draw_chart_icon(draw, cx, cy, size=18, color=(100, 116, 139)):
    s = size / 2.0
    bw = s * 0.45
    draw.rounded_rectangle([cx - s*0.9, cy + s*0.1, cx - s*0.9 + bw, cy + s], radius=2, fill=color)
    draw.rounded_rectangle([cx - s*0.2, cy - s*0.4, cx - s*0.2 + bw, cy + s], radius=2, fill=color)
    draw.rounded_rectangle([cx + s*0.5, cy - s*0.9, cx + s*0.5 + bw, cy + s], radius=2, fill=color)

def draw_gear_icon(draw, cx, cy, size=18, color=(100, 116, 139)):
    s = size / 2.0
    draw.ellipse([cx - s, cy - s, cx + s, cy + s], fill=color)
    for deg in range(0, 360, 45):
        rad = math.radians(deg)
        tx = cx + (s + 2) * math.cos(rad)
        ty = cy + (s + 2) * math.sin(rad)
        draw.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=color)
    draw.ellipse([cx - s*0.45, cy - s*0.45, cx + s*0.45, cy + s*0.45], fill=(255, 255, 255))

def draw_mic_icon(draw, cx, cy, size=24, color=(255, 255, 255)):
    s = size / 2.0
    draw.rounded_rectangle([cx - s*0.35, cy - s*0.9, cx + s*0.35, cy + s*0.1], radius=int(s*0.35), fill=color)
    draw.arc([cx - s*0.65, cy - s*0.4, cx + s*0.65, cy + s*0.5], start=0, end=180, fill=color, width=2)
    draw.line([(cx, cy + s*0.5), (cx, cy + s*0.85)], fill=color, width=2)
    draw.line([(cx - s*0.4, cy + s*0.85), (cx + s*0.4, cy + s*0.85)], fill=color, width=2)

def draw_copy_icon(draw, cx, cy, size=14, color=(51, 65, 85)):
    s = size / 2.0
    draw.rectangle([cx - s*0.7, cy - s, cx + s*0.4, cy + s*0.3], outline=color, width=1)
    draw.rectangle([cx - s*0.3, cy - s*0.4, cx + s, cy + s], fill=(248, 250, 252), outline=color, width=1)

def draw_warning_triangle(draw, cx, cy, size=15, color=(245, 158, 11)):
    s = size / 2.0
    draw.polygon([(cx, cy - s), (cx + s, cy + s), (cx - s, cy + s)], fill=color)
    draw.line([(cx, cy - s*0.3), (cx, cy + s*0.2)], fill=(255, 255, 255), width=2)
    draw.point((cx, cy + s*0.6), fill=(255, 255, 255))


def make_slide_06():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Unified Header
    draw_slide_header(
        draw, 
        slide_num=6, 
        category_en="WIREFRAME | MOBILE UX & ERGONOMIC ARCHITECTURE", 
        title_black="실제 앱 구조를 그대로 반영한 ", 
        title_blue="모바일 와이어프레임과 인체공학적 설계", 
        subtitle_kr="실제 Flutter 모바일 앱의 3대 핵심 화면(대시보드·계산기·음성도크)을 1:1 매칭한 와이어프레임 및 인체공학적 조작 설계"
    )
    
    # UPPER SECTION: 3 MOBILE SCREEN WIREFRAME CHASSIS + ERGONOMIC CALLOUTS (19.5:9 Modern Ratio)
    sec_y = 190
    sec_h = 365
    
    # Modern Flagship 19.5:9 Smartphone Chassis Dimensions (175 x 365, H/W = 2.086)
    pw = 175
    ph = 365
    gap = 22
    
    # -----------------------------------------------------------------
    # Chassis 1: [SCR-DASH-01] 포트폴리오 대시보드 (Home Dashboard)
    # -----------------------------------------------------------------
    p1_x = 120
    draw.rounded_rectangle([p1_x, sec_y, p1_x + pw, sec_y + ph], radius=24, fill=(255, 255, 255), outline=(15, 23, 42), width=2)
    # Dynamic Island Pill
    draw.rounded_rectangle([p1_x + pw//2 - 20, sec_y + 7, p1_x + pw//2 + 20, sec_y + 16], radius=5, fill=(15, 23, 42))
    # Screen Title Badge
    draw_pill_badge(draw, cx=p1_x + pw//2, cy=sec_y + 30, text="SCR-01 · 대시보드", font=get_font(9, 'bold'), theme='blue', has_dot=True, pad_x=6, height=18)
    
    # VIP One-Line Banner Mockup
    v_y = sec_y + 44
    draw.rounded_rectangle([p1_x + 10, v_y, p1_x + pw - 10, v_y + 20], radius=5, fill=(254, 243, 199), outline=(253, 230, 138), width=1)
    draw.text((p1_x + 16, v_y + 4), "⚡ VIP 24h 광고제거", font=get_font(7.5, 'bold'), fill=(180, 83, 9))
    draw.text((p1_x + pw - 16, v_y + 4), "23:59", font=get_num_font(7.5, 'bold'), fill=(217, 119, 6), anchor='ra')
    
    # Smart Portfolio Summary Card (_buildMembershipCard)
    sc_y = v_y + 24
    draw.rounded_rectangle([p1_x + 10, sc_y, p1_x + pw - 10, sc_y + 70], radius=8, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((p1_x + 18, sc_y + 8), "스마트 포트폴리오 메인 요약", font=get_font(8, 'bold'), fill=(0, 81, 255))
    draw.text((p1_x + 18, sc_y + 22), "₩ 12,500,000", font=get_num_font(12, 'black'), fill=(15, 23, 42))
    draw.text((p1_x + 18, sc_y + 39), "평가손익 -₩2,150,000", font=get_font(7.5, 'bold'), fill=(239, 68, 68))
    draw_pill_badge(draw, cx=p1_x + pw - 34, cy=sc_y + 44, text="-17.2%", font=get_num_font(7.5, 'bold'), theme='red', has_dot=False, pad_x=5, height=15, solid=True)
    draw.text((p1_x + 18, sc_y + 54), "• 1차 분할매수 가이드 권장", font=get_font(7, 'medium'), fill=(100, 116, 139))
    
    # 1-Line Hero Button (_buildSimulatorHeroButton)
    hb_y = sc_y + 76
    draw.rounded_rectangle([p1_x + 10, hb_y, p1_x + pw - 10, hb_y + 26], radius=7, fill=(0, 81, 255))
    draw.text((p1_x + pw//2, hb_y + 13), "+ 물타기 계산기 실행 (DCA)", font=get_font(8.5, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # 2x2 Quick Actions Grid (_buildQuickActions)
    qg_y = hb_y + 32
    qw = (pw - 20 - 6) // 2
    qh = 22
    quick_items = [("목표 역산", 0), ("MTS 복사", 1), ("시나리오", 2), ("수수료 계산", 3)]
    for q_txt, q_idx in quick_items:
        qx = p1_x + 10 + (q_idx % 2) * (qw + 6)
        qy = qg_y + (q_idx // 2) * (qh + 4)
        draw.rounded_rectangle([qx, qy, qx + qw, qy + qh], radius=5, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((qx + qw//2, qy + qh//2), q_txt, font=get_font(7.5, 'medium'), fill=(71, 85, 105), anchor='mm')
        
    # Asset List Card Item (_buildAssetCard)
    ac_y = qg_y + 54
    draw.rounded_rectangle([p1_x + 10, ac_y, p1_x + pw - 10, ac_y + 36], radius=7, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((p1_x + 16, ac_y + 6), "삼성전자 005930 · -18.3%", font=get_font(8, 'bold'), fill=(15, 23, 42))
    draw.text((p1_x + 16, ac_y + 20), "평단 ₩72,500 · 100주", font=get_font(7, 'medium'), fill=(100, 116, 139))
    
    # Bottom Bar with Voice FAB & Native Home Indicator
    bb_y = sec_y + ph - 34
    draw.line([(p1_x + 10, bb_y), (p1_x + pw - 10, bb_y)], fill=(241, 245, 249), width=1)
    draw.text((p1_x + 28, bb_y + 12), "홈", font=get_font(7.5, 'bold'), fill=(0, 81, 255), anchor='mm')
    draw.text((p1_x + pw - 28, bb_y + 12), "계산기", font=get_font(7.5, 'medium'), fill=(100, 116, 139), anchor='mm')
    # Center FAB
    fab_cx = p1_x + pw//2
    fab_cy = bb_y + 12
    draw.ellipse([fab_cx - 12, fab_cy - 12, fab_cx + 12, fab_cy + 12], fill=(0, 81, 255))
    draw_mic_icon(draw, cx=fab_cx, cy=fab_cy, size=11, color=(255, 255, 255))
    # Native Home Indicator
    draw.rounded_rectangle([p1_x + pw//2 - 20, sec_y + ph - 6, p1_x + pw//2 + 20, sec_y + ph - 3], radius=2, fill=(15, 23, 42))
    
    # -----------------------------------------------------------------
    # Chassis 2: [SCR-CALC-01] 물타기 계산기 & 스텝퍼 (DCA Simulator)
    # -----------------------------------------------------------------
    p2_x = p1_x + pw + gap
    draw.rounded_rectangle([p2_x, sec_y, p2_x + pw, sec_y + ph], radius=24, fill=(255, 255, 255), outline=(15, 23, 42), width=2)
    draw.rounded_rectangle([p2_x + pw//2 - 20, sec_y + 7, p2_x + pw//2 + 20, sec_y + 16], radius=5, fill=(15, 23, 42))
    draw_pill_badge(draw, cx=p2_x + pw//2, cy=sec_y + 30, text="SCR-02 · 계산기", font=get_font(9, 'bold'), theme='cyan', has_dot=True, pad_x=6, height=18)
    
    # Input 1: Current Price & Holdings
    i1_y = sec_y + 44
    draw.rounded_rectangle([p2_x + 10, i1_y, p2_x + pw - 10, i1_y + 38], radius=7, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((p2_x + 16, i1_y + 6), "현재 보유 평단가", font=get_font(7.5, 'bold'), fill=(100, 116, 139))
    draw.text((p2_x + 16, i1_y + 20), "₩ 65,000", font=get_num_font(10.5, 'bold'), fill=(15, 23, 42))
    draw.text((p2_x + pw - 16, i1_y + 20), "100주", font=get_font(7.5, 'medium'), fill=(71, 85, 105), anchor='ra')
    
    # Input 2: Additional Price & Stepper (_buildInputSection)
    i2_y = i1_y + 44
    draw.rounded_rectangle([p2_x + 10, i2_y, p2_x + pw - 10, i2_y + 50], radius=7, fill=(248, 250, 252), outline=(0, 81, 255), width=1)
    draw.text((p2_x + 16, i2_y + 6), "추가 매수 단가 & 수량", font=get_font(7.5, 'bold'), fill=(0, 81, 255))
    draw.text((p2_x + 16, i2_y + 20), "₩ 55,000", font=get_num_font(10.5, 'bold'), fill=(15, 23, 42))
    
    # Stepper Control [ - 50주 + ]
    st_y = i2_y + 26
    draw.rounded_rectangle([p2_x + pw - 82, st_y, p2_x + pw - 16, st_y + 18], radius=5, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw.text((p2_x + pw - 74, st_y + 9), "-", font=get_font(9.5, 'bold'), fill=(0, 81, 255), anchor='mm')
    draw.text((p2_x + pw - 49, st_y + 9), "50주", font=get_num_font(8, 'bold'), fill=(15, 23, 42), anchor='mm')
    draw.text((p2_x + pw - 24, st_y + 9), "+", font=get_font(9.5, 'bold'), fill=(0, 81, 255), anchor='mm')
    
    # Preset Chips Row
    pr_y = i2_y + 56
    chips = ["-5%", "-10%", "+50주", "전액"]
    c_x = p2_x + 10
    for cp in chips:
        draw.rounded_rectangle([c_x, pr_y, c_x + 35, pr_y + 18], radius=4, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
        draw.text((c_x + 17, pr_y + 9), cp, font=get_font(7.5, 'bold'), fill=(0, 81, 255), anchor='mm')
        c_x += 40
        
    # Result Summary Card (_buildResultSummaryCard)
    res_y = pr_y + 24
    draw.rounded_rectangle([p2_x + 10, res_y, p2_x + pw - 10, res_y + 78], radius=8, fill=(240, 246, 255), outline=(0, 81, 255), width=1)
    draw.text((p2_x + 18, res_y + 8), "예상 신규 평단가", font=get_font(8, 'bold'), fill=(0, 81, 255))
    draw.text((p2_x + 18, res_y + 22), "₩ 61,667", font=get_num_font(14, 'black'), fill=(15, 23, 42))
    draw_pill_badge(draw, cx=p2_x + pw - 34, cy=res_y + 26, text="+5.1%p", font=get_num_font(7, 'bold'), theme='green', has_dot=False, pad_x=4, height=15, solid=True)
    draw.line([(p2_x + 18, res_y + 42), (p2_x + pw - 18, res_y + 42)], fill=(191, 219, 254), width=1)
    draw.text((p2_x + 18, res_y + 48), "필요금: ₩2,750,000", font=get_font(7.5, 'medium'), fill=(71, 85, 105))
    draw.text((p2_x + 18, res_y + 60), "총 150주 (평단 5.1% 인하)", font=get_font(7.5, 'medium'), fill=(71, 85, 105))
    
    # 1-Tap Copy Action Button (_buildActionButtons)
    btn_y = res_y + 84
    draw.rounded_rectangle([p2_x + 10, btn_y, p2_x + pw - 10, btn_y + 28], radius=7, fill=(0, 81, 255))
    draw_copy_icon(draw, cx=p2_x + 28, cy=btn_y + 14, size=10, color=(255, 255, 255))
    draw.text((p2_x + pw//2 + 5, btn_y + 14), "1-Tap MTS 주문 복사", font=get_font(8.5, 'bold'), fill=(255, 255, 255), anchor='mm')
    # Native Home Indicator
    draw.rounded_rectangle([p2_x + pw//2 - 20, sec_y + ph - 6, p2_x + pw//2 + 20, sec_y + ph - 3], radius=2, fill=(15, 23, 42))
    
    # -----------------------------------------------------------------
    # Chassis 3: [SCR-VOICE-01] 0.2초 AI 음성 도크 시트 (Voice Dock Sheet)
    # -----------------------------------------------------------------
    p3_x = p2_x + pw + gap
    draw.rounded_rectangle([p3_x, sec_y, p3_x + pw, sec_y + ph], radius=24, fill=(241, 245, 249), outline=(15, 23, 42), width=2)
    draw.rounded_rectangle([p3_x + pw//2 - 20, sec_y + 7, p3_x + pw//2 + 20, sec_y + 16], radius=5, fill=(15, 23, 42))
    
    # Dimmed background representation
    draw.rounded_rectangle([p3_x + 10, sec_y + 30, p3_x + pw - 10, sec_y + 85], radius=7, fill=(226, 232, 240))
    draw.text((p3_x + 16, sec_y + 44), "배경: 시뮬레이터 (Dim 60%)", font=get_font(7.5, 'regular'), fill=(100, 116, 139))
    
    # Bottom Sheet Container (Sliding up within phone bezel)
    bs_y = sec_y + 80
    draw.rounded_rectangle([p3_x + 2, bs_y, p3_x + pw - 2, sec_y + ph - 2], radius=18, fill=(255, 255, 255), outline=(0, 81, 255), width=2)
    # Drag Handle
    draw.rounded_rectangle([p3_x + pw//2 - 14, bs_y + 6, p3_x + pw//2 + 14, bs_y + 10], radius=2, fill=(203, 213, 225))
    
    # Sheet Header
    draw_pill_badge(draw, cx=p3_x + pw//2, cy=bs_y + 22, text="SCR-03 · 음성 도크", font=get_font(8.5, 'bold'), theme='purple', has_dot=True, pad_x=6, height=18)
    
    # Realtime 7-Bar Voice Waveform Animation
    wv_y = bs_y + 44
    wave_h = [8, 14, 22, 16, 26, 13, 9]
    w_start_x = p3_x + pw//2 - (len(wave_h) * 10) // 2
    for idx, wh in enumerate(wave_h):
        wx = w_start_x + idx * 10
        draw.rounded_rectangle([wx, wv_y - wh//2, wx + 5, wv_y + wh//2], radius=2, fill=(122, 34, 255))
        
    # Speech Bubble Mockup
    sb_y = wv_y + 20
    draw.rounded_rectangle([p3_x + 10, sb_y, p3_x + pw - 10, sb_y + 28], radius=6, fill=(245, 243, 255), outline=(221, 214, 254), width=1)
    draw.text((p3_x + pw//2, sb_y + 14), '"삼성전자 55,000원에 50주"', font=get_font(8, 'bold'), fill=(109, 40, 217), anchor='mm')
    
    # Parsed Quant Tags Row
    pt_y = sb_y + 34
    tags = ["삼성전자", "₩55,000", "50주"]
    tx_start = p3_x + 10
    for tg in tags:
        draw.rounded_rectangle([tx_start, pt_y, tx_start + 48, pt_y + 18], radius=4, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
        draw.text((tx_start + 24, pt_y + 9), tg, font=get_font(7, 'bold'), fill=(0, 81, 255), anchor='mm')
        tx_start += 53
        
    # Auto Inject Button
    inj_y = pt_y + 26
    draw.rounded_rectangle([p3_x + 10, inj_y, p3_x + pw - 10, inj_y + 28], radius=7, fill=(122, 34, 255))
    draw.text((p3_x + pw//2, inj_y + 14), "⚡ 즉시 주입 (0.2s)", font=get_font(8.5, 'bold'), fill=(255, 255, 255), anchor='mm')
    # Native Home Indicator
    draw.rounded_rectangle([p3_x + pw//2 - 20, sec_y + ph - 6, p3_x + pw//2 + 20, sec_y + ph - 3], radius=2, fill=(15, 23, 42))
    
    # -----------------------------------------------------------------
    # Column 4: Ergonomic Breakdown Callouts (Rightmost, x=725 to 1800)
    # -----------------------------------------------------------------
    c4_x = p3_x + pw + 35
    c4_w = 1800 - c4_x
    c4_x = p3_x + pw + 35
    c4_w = 1800 - c4_x
    draw.rounded_rectangle([c4_x, sec_y, c4_x + c4_w, sec_y + sec_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    # 24px bottom margin below badge
    draw_pill_badge(draw, cx=c4_x + 125, cy=sec_y + 24, text="ERGONOMIC SPEC & GUARD", font=get_font(10, 'bold'), theme='purple', has_dot=False, pad_x=10, height=24)
    draw.text((c4_x + 24, sec_y + 60), "인체공학적 조작성 및 오류 방지 설계", font=get_font(16, 'bold'), fill=(15, 23, 42))
    
    callouts = [
        ("① Fitts' Law Thumb-Zone 48dp", "한 손 파지 시 엄지가 닿는 하단 120dp 반경 내 주요 액션(계산 실행, MTS 복사, 음성 FAB) 집중 배치"),
        ("② 0.2초 온디바이스 음성 도크", "급변하는 주식 호가 속 8자리 소수점 키패드 타이핑 피로도를 78% 절감하는 실시간 STT 파싱"),
        ("③ 비정상 입력 사전 가드 엔진", "도달 불가한 목표 평단가 또는 음수 입력 시 햅틱 진동 경고 및 실현 가능한 최적 분할 매수 대안 제시"),
        ("④ 1-Tap 무손실 파라미터 인계", "역산으로 도출된 수치를 시뮬레이터로 0ms 자동 주입하여 재입력 오류 및 시장가 매수 실수 원천 방지")
    ]
    cy_sub = sec_y + 90
    for c_title, c_desc in callouts:
        draw.rounded_rectangle([c4_x + 24, cy_sub, c4_x + c4_w - 24, cy_sub + 56], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((c4_x + 38, cy_sub + 14), c_title, font=get_font(12, 'bold'), fill=(0, 81, 255))
        draw.text((c4_x + 38, cy_sub + 33), c_desc, font=get_font(10.5, 'regular'), fill=(71, 85, 105))
        cy_sub += 64
        
    # =========================================================
    # LOWER SECTION: DESIGN CONCEPT (Naming & Symbol) - Pretendard Matched
    # =========================================================
    sec2_y = 575
    draw.text((120, sec2_y), "Design Concept", font=get_font(24, 'bold'), fill=(15, 23, 42))
    
    card_y = sec2_y + 40
    card_h = 350
    
    # Left Card: Naming
    n_x = 120
    n_w = 780
    draw.rounded_rectangle([n_x, card_y, n_x + n_w, card_y + card_h], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((n_x + 32, card_y + 28), "Naming", font=get_font(16, 'bold'), fill=(0, 81, 255))
    draw.text((n_x + 32, card_y + 56), "스마트 물타기는 복잡하고 불안했던 투자를 \"스마트하게 지킨다\"는 메시지를 담았습니다.", font=get_font(13.5, 'regular'), fill=(71, 85, 105))
    
    # Big Typography Display: Smart DCA [스마트 물타기]
    ty_logo = card_y + 105
    draw.text((n_x + 32, ty_logo), "Smart DCA", font=get_font(46, 'black'), fill=(0, 81, 255))
    draw.text((n_x + 320, ty_logo + 10), "[스마트 물타기]", font=get_font(28, 'bold'), fill=(15, 23, 42))
    
    # Detailed Description
    desc_p1 = "기존 금융 시장에서 공포와 감정에 휩쓸려 무계획하게 행해지던 '물타기(Dollar Cost Averaging)'를 수학적 가중평균과 폐쇄형 역산 알고리즘으로 '스마트(Smart)'하게 전환하여, 감정이 아닌 객관적 시나리오로 자산을 지킨다는 핵심 메시지를 담았습니다."
    d_lines = wrap_text_by_words(desc_p1, get_font(12, 'regular'), n_w - 64, draw)
    dy = ty_logo + 65
    for line in d_lines:
        draw.text((n_x + 32, dy), line, font=get_font(12, 'regular'), fill=(71, 85, 105))
        dy += 20
        
    dy += 10
    bullets = [
        "• Smart : 폐쇄형 퀀트 역산 엔진 & 0.2초 온디바이스 음성 AI 파싱",
        "• DCA : 분할 매수를 통한 리스크 헷지 및 평단가 방어 철학"
    ]
    for b in bullets:
        draw.text((n_x + 32, dy), b, font=get_font(12, 'semibold'), fill=(30, 41, 59))
        dy += 22
        
    # Right Card: Symbol
    s_x = 930
    s_w = 870
    draw.rounded_rectangle([s_x, card_y, s_x + s_w, card_y + card_h], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((s_x + 32, card_y + 28), "Symbol", font=get_font(16, 'bold'), fill=(0, 81, 255))
    
    # App Icon Squircle Mockup
    icon_path = "assets/app_icon_clean_squircle.png"
    if not os.path.exists(icon_path):
        icon_path = "assets/app_icon.png"
        
    ix = s_x + 40
    iy = card_y + 80
    isize = 145
    if os.path.exists(icon_path):
        try:
            icon_img = Image.open(icon_path).convert('RGBA')
            icon_img = icon_img.resize((isize, isize), Image.Resampling.LANCZOS)
            shadow = Image.new('RGBA', (isize + 24, isize + 24), (0, 0, 0, 0))
            s_draw = ImageDraw.Draw(shadow)
            s_draw.rounded_rectangle([12, 12, isize + 12, isize + 12], radius=32, fill=(0, 0, 0, 45))
            shadow = shadow.filter(ImageFilter.GaussianBlur(6))
            base.paste(shadow, (ix - 12, iy - 6), shadow)
            base.paste(icon_img, (ix, iy), icon_img)
        except Exception as e:
            draw.rounded_rectangle([ix, iy, ix + isize, iy + isize], radius=32, fill=(0, 81, 255))
    else:
        draw.rounded_rectangle([ix, iy, ix + isize, iy + isize], radius=32, fill=(0, 81, 255))
        
    # Symbol Text
    tx_sym = ix + isize + 36
    draw.text((tx_sym, card_y + 75), "“골든 크로스와 U자형 반등”이라는 서비스 네임에 맞추어", font=get_font(14, 'bold'), fill=(15, 23, 42))
    draw.text((tx_sym, card_y + 98), "평단가를 낮춰 반등을 이끄는 형태로 심볼을 디자인했습니다.", font=get_font(14, 'bold'), fill=(0, 81, 255))
    
    desc_s = (
        "하향 곡선을 그리던 평균 단가가 추가 매수를 통해 점진적으로 낮아지며\n"
        "주가 상승 반등 곡선과 교차(Golden Cross)하는 퀀트 모티프를\n"
        "기하학적 곡면 스퀘어클(Squircle) 심볼로 시각화했습니다.\n\n"
        "• Squircle Frame : iOS 및 Android 표준 스토어 규격(1024x1024) 준수\n"
        "• Blue Gradient  : 금융 신뢰를 상징하는 시그니처 퀀트 블루 팔레트"
    )
    s_lines = desc_s.split('\n')
    sy_desc = card_y + 145
    for line in s_lines:
        draw.text((tx_sym, sy_desc), line, font=get_font(12, 'regular'), fill=(71, 85, 105))
        sy_desc += 22

    draw_slide_footer(draw, 6)
    base.save(f'{OUT_DIR}/slide_06.png')
    print("SAVED slide_06.png (Enhanced Mobile Wireframe & Ergonomic Architecture)")


def make_slide_07():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Unified Header
    draw_slide_header(
        draw, 
        slide_num=7, 
        category_en="DESIGN SYSTEM | REAL APP UI COMPONENT LIBRARY", 
        title_black="프로덕션 수준의 완성도를 지탱하는 ", 
        title_blue="디자인 시스템과 컴포넌트 라이브러리", 
        subtitle_kr="Flutter 실제 앱의 AppColors 토큰, Pretendard 타이포그래피, 그리고 프로덕션에 구현된 실물 UI 컴포넌트 라이브러리"
    )
    
    # Grid layout coordinates (4 Balanced Modular Master Cards)
    # Total width = 1680px (from x=120 to x=1800). Gap = 32px.
    left_x = 120
    left_w = 760
    right_x = 912
    right_w = 888
    
    row1_y = 195
    row1_h = 365
    row2_y = 585
    row2_h = 385
    
    # =========================================================================
    # CARD A1 (Top Left): APPCOLORS TOKEN & WCAG 2.1 AAA CONTRAST
    # =========================================================================
    draw.rounded_rectangle([left_x, row1_y, left_x + left_w, row1_y + row1_h], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    # Card Header
    draw_pill_badge(draw, left_x=left_x + 32, cy=row1_y + 36, text="FOUNDATION 01", font=get_font(10, 'bold'), theme='blue', has_dot=True, dark_mode=False, pad_x=10, height=24)
    draw.text((left_x + 160, row1_y + 26), "AppColors Token & Contrast Architecture", font=get_font(16, 'bold'), fill=(15, 23, 42))
    draw.line([(left_x + 32, row1_y + 60), (left_x + left_w - 32, row1_y + 60)], fill=(241, 245, 249), width=1)
    
    # Hero Color Swatch Card: Primary Electric Blue #0051FF
    hb_y = row1_y + 76
    draw.rounded_rectangle([left_x + 32, hb_y, left_x + left_w - 32, hb_y + 74], radius=12, fill=(0, 81, 255))
    draw.text((left_x + 50, hb_y + 14), "PRIMARY ELECTRIC BLUE", font=get_font(15, 'bold'), fill=(255, 255, 255))
    draw.text((left_x + 50, hb_y + 36), "AppColors.primaryBlue  ·  #0051FF (Dark: #0038B8)", font=get_num_font(11.5, 'medium'), fill=(191, 219, 254))
    draw.text((left_x + 50, hb_y + 52), "투자의 확신과 신뢰를 상징하는 시그니처 퀀트 블루", font=get_font(10, 'regular'), fill=(224, 242, 254))
    draw_pill_badge(draw, cx=left_x + left_w - 95, cy=hb_y + 37, text="8.4:1 AAA", font=get_font(11, 'bold'), theme='green', has_dot=False, dark_mode=False, pad_x=12, height=28)
    
    # 5 Semantic Swatches from AppColors
    sub_swatches = [
        ("Accent Cyan", "#00D2FF", (0, 210, 255), "음성 도크 & 파형"),
        ("Accent Mint", "#00E676", (0, 230, 118), "수익률 & 반등"),
        ("Accent Coral", "#FF5252", (255, 82, 82), "손실 경고 & 헤지"),
        ("Surface Dark", "#0D1117", (13, 17, 23), "다크모드 캔버스"),
        ("Premium Gold", "#FFB300", (255, 179, 0), "VIP 무광고 배너"),
    ]
    sw_w = (left_w - 64 - 40) // 5
    sw_y = hb_y + 88
    for i, (s_name, s_hex, s_col, s_usage) in enumerate(sub_swatches):
        sx = left_x + 32 + i * (sw_w + 10)
        draw.rounded_rectangle([sx, sw_y, sx + sw_w, sw_y + 80], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.rounded_rectangle([sx + 8, sw_y + 8, sx + sw_w - 8, sw_y + 28], radius=6, fill=s_col)
        draw.text((sx + 8, sw_y + 34), s_name, font=get_font(10, 'bold'), fill=(15, 23, 42))
        draw.text((sx + 8, sw_y + 48), s_hex, font=get_num_font(9.5, 'bold'), fill=(71, 85, 105))
        draw.text((sx + 8, sw_y + 62), s_usage, font=get_font(8.5, 'medium'), fill=(100, 116, 139))
        
    # Visual Signature Gradients Row
    gr_y = sw_y + 92
    draw.text((left_x + 32, gr_y), "Signature App Gradients (AppColors):", font=get_font(11, 'bold'), fill=(71, 85, 105))
    
    gradients_data = [
        ("primaryGradient", (0, 81, 255), (0, 210, 255)),
        ("cardTealBlueGradient", (10, 37, 64), (19, 62, 104)),
        ("vipGoldGradient", (255, 179, 0), (255, 109, 0)),
        ("voiceWaveGradient", (0, 210, 255), (122, 34, 255)),
    ]
    gr_w = (left_w - 64 - 36) // 4
    for idx, (g_name, g_c1, g_c2) in enumerate(gradients_data):
        gx = left_x + 32 + idx * (gr_w + 12)
        draw_gradient_bar(base, [gx, gr_y + 20, gx + gr_w, gr_y + 44], g_c1, g_c2, radius=6)
        draw.text((gx + gr_w//2, gr_y + 54), g_name, font=get_font(8.5, 'bold'), fill=(71, 85, 105), anchor='mm')
        
    draw.text((left_x + 32, row1_y + row1_h - 18), "✓ WCAG 2.1 AAA 7:1+ 초고대비율 엄격 준수 · AppColors 싱글톤 토큰 시스템", font=get_font(10, 'regular'), fill=(100, 116, 139))
    
    # =========================================================================
    # CARD A2 (Bottom Left): PRETENDARD TYPOGRAPHY & SPATIAL GRID TOKENS
    # =========================================================================
    draw.rounded_rectangle([left_x, row2_y, left_x + left_w, row2_y + row2_h], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    # Card Header
    draw_pill_badge(draw, left_x=left_x + 32, cy=row2_y + 36, text="FOUNDATION 02", font=get_font(10, 'bold'), theme='blue', has_dot=True, dark_mode=False, pad_x=10, height=24)
    draw.text((left_x + 160, row2_y + 26), "Pretendard Typography & Spatial Tokens", font=get_font(16, 'bold'), fill=(15, 23, 42))
    draw.line([(left_x + 32, row2_y + 60), (left_x + left_w - 32, row2_y + 60)], fill=(241, 245, 249), width=1)
    
    # Typography Spec Rows
    t_rows = [
        ("Display 28", "Bold", "주요 평단가 지표", "₩ 61,667", True),
        ("Headline 20", "Bold", "섹션 헤더 & 카드 제목", "스마트 포트폴리오 메인 요약", False),
        ("Title 16", "SemiBold", "인풋 필드 라벨 & 버튼", "추가 매수 단가 & 수량 조절", False),
        ("Body 14", "Regular", "분석 결과 및 안내문", "현재 평단가 기준 50주 추가 분할 매수", False),
        ("Caption 11", "Medium", "보조 메타 정보 & 상태", "0.2s 음성 도크 엔진 즉각 파싱 완료", False),
    ]
    ty_start = row2_y + 74
    for i, (t_role, t_weight, t_desc, t_sample, is_mono) in enumerate(t_rows):
        ry = ty_start + i * 40
        draw.rounded_rectangle([left_x + 32, ry, left_x + left_w - 32, ry + 34], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((left_x + 46, ry + 9), t_role, font=get_font(11, 'bold'), fill=(0, 81, 255))
        draw.text((left_x + 140, ry + 9), t_weight, font=get_font(10.5, 'medium'), fill=(100, 116, 139))
        draw.text((left_x + 225, ry + 9), t_desc, font=get_font(10.5, 'regular'), fill=(71, 85, 105))
        draw.text((left_x + left_w - 46, ry + 9), t_sample, font=get_num_font(12, 'bold') if is_mono else get_font(11, 'semibold'), fill=(15, 23, 42), anchor='ra')
        
    # OpenType Tabular Figures & Spatial Tokens Box
    sp_box_y = ty_start + len(t_rows) * 40 + 10
    draw.rounded_rectangle([left_x + 32, sp_box_y, left_x + left_w - 32, row2_y + row2_h - 18], radius=12, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    
    draw.text((left_x + 48, sp_box_y + 12), "OpenType `FontFeature.tabularFigures()` 타뷸라 넘버 & 4/8pt 그리드", font=get_font(12, 'bold'), fill=(0, 81, 255))
    draw.text((left_x + 48, sp_box_y + 32), "• Tabular Numbers : 실시간 호가 및 시세 변동 시 숫자 폭의 떨림(Jitter)을 방지하는 고정폭 숫자 규격 적용", font=get_font(10, 'regular'), fill=(71, 85, 105))
    draw.text((left_x + 48, sp_box_y + 49), "• Spatial System   : 4pt/8pt 그리드 (`space-4` ~ `space-32`) · 코너 라운딩 `r-8`, `r-12`, `r-16`, `r-24`, `r-full`", font=get_font(10, 'regular'), fill=(71, 85, 105))
    draw.text((left_x + 48, sp_box_y + 66), "• Elevation Tokens : Level 1 (카드 Diffuse 2dp) · Level 2 (모달 8dp) · Level 3 (0.2s 음성 도크 FAB 16dp)", font=get_font(10, 'regular'), fill=(71, 85, 105))
    
    # =========================================================================
    # CARD B1 (Top Right): REAL APP UI COMPONENTS 01 (DASHBOARD & INPUTS)
    # =========================================================================
    draw.rounded_rectangle([right_x, row1_y, right_x + right_w, row1_y + row1_h], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    # Card Header
    draw_pill_badge(draw, left_x=right_x + 32, cy=row1_y + 36, text="COMPONENTS 01", font=get_font(10, 'bold'), theme='cyan', has_dot=True, dark_mode=False, pad_x=10, height=24)
    draw.text((right_x + 170, row1_y + 26), "Real App UI Components (스마트 자산 요약 & 인풋/스텝퍼)", font=get_font(16, 'bold'), fill=(15, 23, 42))
    draw.line([(right_x + 32, row1_y + 60), (right_x + right_w - 32, row1_y + 60)], fill=(241, 245, 249), width=1)
    
    # Component 1: Smart Portfolio Summary Card (_buildMembershipCard)
    c1_y = row1_y + 74
    draw.rounded_rectangle([right_x + 32, c1_y, right_x + right_w - 32, c1_y + 92], radius=14, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    
    # Inside Summary Card
    draw.text((right_x + 50, c1_y + 14), "스마트 포트폴리오 메인 요약", font=get_font(12, 'bold'), fill=(0, 81, 255))
    draw.text((right_x + 50, c1_y + 36), "총 투자 원금 ₩ 12,500,000", font=get_num_font(17, 'black'), fill=(15, 23, 42))
    draw.text((right_x + 50, c1_y + 64), "평가손익 -₩ 2,150,000 (-17.2%)", font=get_font(11.5, 'bold'), fill=(255, 82, 82))
    draw_pill_badge(draw, cx=right_x + 330, cy=c1_y + 71, text="1차 분할매수 권장", font=get_font(9.5, 'bold'), theme='amber', has_dot=True, dark_mode=False, pad_x=8, height=22)
    
    # Currency Segmented Toggle on Right of Card
    tog_x = right_x + right_w - 180
    tog_y = c1_y + 14
    draw.rounded_rectangle([tog_x, tog_y, tog_x + 130, tog_y + 32], radius=16, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw.rounded_rectangle([tog_x + 2, tog_y + 2, tog_x + 64, tog_y + 30], radius=14, fill=(0, 81, 255))
    draw.text((tog_x + 33, tog_y + 16), "KRW ₩", font=get_font(9.5, 'bold'), fill=(255, 255, 255), anchor='mm')
    draw.text((tog_x + 96, tog_y + 16), "USD $", font=get_font(9.5, 'medium'), fill=(100, 116, 139), anchor='mm')
    
    draw.text((right_x + right_w - 50, c1_y + 65), "물타기 방어율 65% 타깃", font=get_font(10.5, 'bold'), fill=(0, 81, 255), anchor='ra')
    
    # Component 2 & 3: Side-by-Side (Focused Input with Stepper + Real Asset Position Card)
    dual_y = c1_y + 106
    dual_w = (right_w - 64 - 18) // 2
    
    # Left Dual: Precision Input & Stepper Component (_buildInputSection)
    draw.rounded_rectangle([right_x + 32, dual_y, right_x + 32 + dual_w, dual_y + 94], radius=12, fill=(248, 250, 252), outline=(0, 81, 255), width=2)
    draw.text((right_x + 48, dual_y + 12), "현재 보유 평단가 & 조절 스텝퍼", font=get_font(10.5, 'bold'), fill=(0, 81, 255))
    draw.text((right_x + 48, dual_y + 36), "₩ 65,000", font=get_num_font(16, 'bold'), fill=(15, 23, 42))
    # Glowing cursor
    draw.line([(right_x + 155, dual_y + 36), (right_x + 155, dual_y + 58)], fill=(0, 81, 255), width=2)
    draw_pill_badge(draw, cx=right_x + 32 + dual_w - 45, cy=dual_y + 34, text="ACTIVE", font=get_font(9, 'bold'), theme='blue', has_dot=False, dark_mode=False, pad_x=6, height=20)
    
    # Stepper underneath
    draw.rounded_rectangle([right_x + 48, dual_y + 62, right_x + 32 + dual_w - 16, dual_y + 86], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw.text((right_x + 72, dual_y + 74), "-", font=get_font(14, 'bold'), fill=(0, 81, 255), anchor='mm')
    draw.text((right_x + 48 + (dual_w - 64)//2, dual_y + 74), "100 주 (수량 가감)", font=get_num_font(10.5, 'bold'), fill=(15, 23, 42), anchor='mm')
    draw.text((right_x + 32 + dual_w - 40, dual_y + 74), "+", font=get_font(14, 'bold'), fill=(0, 81, 255), anchor='mm')
    
    # Right Dual: Real Asset Position Card (_buildAssetCard)
    p_x = right_x + 32 + dual_w + 18
    draw.rounded_rectangle([p_x, dual_y, p_x + dual_w, dual_y + 94], radius=12, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((p_x + 16, dual_y + 12), "삼성전자 (005930)", font=get_font(12, 'bold'), fill=(15, 23, 42))
    draw_pill_badge(draw, cx=p_x + dual_w - 55, cy=dual_y + 20, text="-18.3% CRITICAL", font=get_num_font(8.5, 'bold'), theme='red', has_dot=True, pad_x=6, height=20)
    draw.text((p_x + 16, dual_y + 40), "보유 평단 : ₩ 72,500 (100주)", font=get_font(10.5, 'medium'), fill=(71, 85, 105))
    draw.text((p_x + 16, dual_y + 62), "현재 시세 : ₩ 59,200", font=get_font(10.5, 'bold'), fill=(15, 23, 42))
    draw.text((p_x + dual_w - 16, dual_y + 62), "손실 -₩1,330,000", font=get_font(10.5, 'bold'), fill=(255, 82, 82), anchor='ra')
    
    # Component 4: Quick Action Price Preset Chips (_buildPresetRow)
    pr_y = dual_y + 106
    draw.text((right_x + 32, pr_y + 6), "호가/수량 프리셋 칩:", font=get_font(11, 'bold'), fill=(100, 116, 139))
    presets = [
        ("+5%", (0, 81, 255), (239, 246, 255)),
        ("+10%", (0, 81, 255), (239, 246, 255)),
        ("-5%", (255, 82, 82), (254, 242, 242)),
        ("-10%", (255, 82, 82), (254, 242, 242)),
        ("+50주", (0, 81, 255), (239, 246, 255)),
        ("+100주", (0, 81, 255), (239, 246, 255)),
        ("전액 매수", (0, 200, 100), (236, 253, 245)),
    ]
    cur_ch_x = right_x + 175
    for p_txt, p_col, p_bg in presets:
        draw.rounded_rectangle([cur_ch_x, pr_y, cur_ch_x + 90, pr_y + 28], radius=14, fill=p_bg, outline=p_col, width=1)
        draw.text((cur_ch_x + 45, pr_y + 14), p_txt, font=get_font(10.5, 'bold'), fill=p_col, anchor='mm')
        cur_ch_x += 98
        
    draw.text((right_x + 32, row1_y + row1_h - 18), "✓ Flutter 실제 위젯 트리 1:1 대응 (home_screen.dart & simulator_screen.dart)", font=get_font(10, 'regular'), fill=(100, 116, 139))
    
    # =========================================================================
    # CARD B2 (Bottom Right): REAL APP UI COMPONENTS 02 (RESULTS & VOICE & CTAS)
    # =========================================================================
    draw.rounded_rectangle([right_x, row2_y, right_x + right_w, row2_y + row2_h], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    # Card Header
    draw_pill_badge(draw, left_x=right_x + 32, cy=row2_y + 36, text="COMPONENTS 02", font=get_font(10, 'bold'), theme='cyan', has_dot=True, dark_mode=False, pad_x=10, height=24)
    draw.text((right_x + 170, row2_y + 26), "Real App UI Components (결과 요약 카드 & 액션 CTA & 음성 도크)", font=get_font(16, 'bold'), fill=(15, 23, 42))
    draw.line([(right_x + 32, row2_y + 60), (right_x + right_w - 32, row2_y + 60)], fill=(241, 245, 249), width=1)
    
    # Component 5: Real Result Summary Card (_buildResultSummaryCard)
    res_card_y = row2_y + 72
    res_card_w = right_w - 64
    draw.rounded_rectangle([right_x + 32, res_card_y, right_x + 32 + res_card_w, res_card_y + 88], radius=14, fill=(240, 246, 255), outline=(0, 81, 255), width=1)
    
    draw.text((right_x + 50, res_card_y + 14), "실시간 가중평균 계산 결과 요약", font=get_font(12, 'bold'), fill=(0, 81, 255))
    draw.text((right_x + 50, res_card_y + 36), "예상 신규 평단 ₩ 61,667", font=get_num_font(18, 'black'), fill=(15, 23, 42))
    draw_pill_badge(draw, cx=right_x + 380, cy=res_card_y + 44, text="평단 방어율 +5.1%p 회복", font=get_num_font(10, 'bold'), theme='green', has_dot=True, pad_x=10, height=24, solid=True)
    
    # Metrics columns inside Result Card
    draw.text((right_x + 50, res_card_y + 66), "필요 예수금 : ₩ 2,750,000", font=get_font(11, 'bold'), fill=(71, 85, 105))
    draw.text((right_x + 280, res_card_y + 66), "총 수량 : 150 주 (+50주 추가)", font=get_font(11, 'medium'), fill=(71, 85, 105))
    draw.text((right_x + res_card_w - 30, res_card_y + 66), "본전 탈출 목표가: ₩61,667", font=get_font(11, 'bold'), fill=(0, 81, 255), anchor='ra')
    
    # Component 6: Real CTA Action Buttons Row (_buildSimulatorHeroButton & Action Buttons)
    cta_y = res_card_y + 100
    # Primary CTA Button
    draw.rounded_rectangle([right_x + 32, cta_y, right_x + 245, cta_y + 44], radius=12, fill=(0, 81, 255))
    draw.text((right_x + 138, cta_y + 22), "+ 물타기 계산 실행", font=get_font(12, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # Secondary Outlined Button
    draw.rounded_rectangle([right_x + 260, cta_y, right_x + 465, cta_y + 44], radius=12, fill=(240, 246, 255), outline=(0, 81, 255), width=1)
    draw.text((right_x + 362, cta_y + 22), "목표 평단가 역산", font=get_font(12, 'bold'), fill=(0, 81, 255), anchor='mm')
    
    # 1-Tap Copy Action Button
    draw.rounded_rectangle([right_x + 480, cta_y, right_x + 655, cta_y + 44], radius=12, fill=(248, 250, 252), outline=(203, 213, 225), width=1)
    draw_copy_icon(draw, cx=right_x + 505, cy=cta_y + 22, size=14, color=(51, 65, 85))
    draw.text((right_x + 575, cta_y + 22), "1-Tap MTS 복사", font=get_font(11.5, 'bold'), fill=(51, 65, 85), anchor='mm')
    
    # VIP One-Line Banner (_buildWatchAdVipOneLineBanner)
    vip_w = right_w - 64 - 670
    draw.rounded_rectangle([right_x + 670, cta_y, right_x + right_w - 32, cta_y + 44], radius=12, fill=(254, 243, 199), outline=(253, 230, 138), width=1)
    draw.text((right_x + 670 + vip_w//2, cta_y + 14), "⚡ VIP 24h 무광고 세션", font=get_font(9.5, 'bold'), fill=(180, 83, 9), anchor='mm')
    draw.text((right_x + 670 + vip_w//2, cta_y + 30), "남은 시간 23:59:42", font=get_num_font(9.5, 'bold'), fill=(217, 119, 6), anchor='mm')
    
    # Component 7: Real AI Voice Dock Component Panel (AiVoicePanel)
    v_dock_y = cta_y + 56
    v_dock_w = right_w - 64
    draw.rounded_rectangle([right_x + 32, v_dock_y, right_x + 32 + v_dock_w, v_dock_y + 82], radius=14, fill=(245, 243, 255), outline=(221, 214, 254), width=1)
    
    # Floating Mic FAB inside Voice Dock
    draw.ellipse([right_x + 52, v_dock_y + 18, right_x + 98, v_dock_y + 64], fill=(122, 34, 255))
    draw_mic_icon(draw, cx=right_x + 75, cy=v_dock_y + 41, size=22, color=(255, 255, 255))
    
    # Waveform
    v_wave_h = [8, 16, 26, 36, 22, 14, 18, 30, 12]
    vw_x = right_x + 115
    for wh in v_wave_h:
        draw.rounded_rectangle([vw_x, v_dock_y + 41 - wh//2, vw_x + 4, v_dock_y + 41 + wh//2], radius=2, fill=(122, 34, 255))
        vw_x += 9
        
    # Speech Bubble
    sb_x = vw_x + 15
    draw.rounded_rectangle([sb_x, v_dock_y + 16, sb_x + 310, v_dock_y + 66], radius=10, fill=(255, 255, 255), outline=(221, 214, 254), width=1)
    draw.text((sb_x + 14, v_dock_y + 28), "\"삼성전자 55,000원에 50주\"", font=get_font(12, 'bold'), fill=(109, 40, 217))
    draw.text((sb_x + 14, v_dock_y + 48), "0.2s 음성 STT 파싱 완료 → 3개 파라미터 자동 추출", font=get_font(9.5, 'regular'), fill=(100, 116, 139))
    
    # Auto Inject Button
    draw.rounded_rectangle([sb_x + 325, v_dock_y + 24, right_x + 32 + v_dock_w - 20, v_dock_y + 58], radius=10, fill=(122, 34, 255))
    draw.text((sb_x + 325 + (right_x + 32 + v_dock_w - 20 - (sb_x + 325))//2, v_dock_y + 41), "계산기에 즉시 주입", font=get_font(11, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # Component 8: 6 Semantic Status Badges
    bdg_y = v_dock_y + 94
    draw.text((right_x + 32, bdg_y + 6), "상태 뱃지 시스템:", font=get_font(11, 'bold'), fill=(100, 116, 139))
    badges = [
        ("0.2s 음성 도크", "cyan", True),
        ("목표 평단가 역산", "blue", True),
        ("수익 반등 회복", "green", True),
        ("손실 리스크 헤지", "red", True),
        ("100% 온디바이스", "slate", True),
        ("60fps R8 최적화", "purple", False),
    ]
    cur_bx = right_x + 145
    for b_txt, b_thm, b_dt in badges:
        _, _, b_end, _ = draw_pill_badge(draw, left_x=cur_bx, cy=bdg_y + 14, text=b_txt, font=get_font(10, 'bold'), theme=b_thm, has_dot=b_dt, dark_mode=False, pad_x=10, height=26)
        cur_bx = b_end + 10
        
    draw_slide_footer(draw, 7)
    base.save(f'{OUT_DIR}/slide_07.png')
    print("SAVED slide_07.png (Enhanced Real App UI Components & Design System)")



def make_slide_08():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Top Line Boundary
    draw.line([(100, 52), (1820, 52)], fill=(226, 232, 240), width=1)
    
    # -------------------------------------------------------------
    # 1. Left Column: Grouped Header Card & Comparison Pane (x=100, w=490)
    # -------------------------------------------------------------
    lx = 100
    lw = 490
    
    # 1-A. Unified Kicker Badge (cy=78, bottom=91)
    draw_pill_badge(draw, left_x=lx, cy=78, text="08 CORE FEATURE | 0.2s VOICE INPUT DOCK", font=get_font(10.5, 'bold'), theme='blue', has_dot=True, dark_mode=False, pad_x=10, height=26)
    
    # Headline (y=116 -> 25px bottom margin below badge)
    t1_a = "복잡한 타이핑 없이 "
    t1_b = "말 한마디로,"
    font_title = get_font(33, 'extrabold')
    w_t1_a = draw.textlength(t1_a, font=font_title)
    draw.text((lx, 116), t1_a, font=font_title, fill=(15, 23, 42))
    draw.text((lx + w_t1_a, 116), t1_b, font=font_title, fill=(0, 81, 255))
    
    t2_a = "0.2초 만에 "
    t2_b = "파라미터를 완성해요."
    w_t2_a = draw.textlength(t2_a, font=font_title)
    draw.text((lx, 158), t2_a, font=font_title, fill=(0, 81, 255))
    draw.text((lx + w_t2_a, 158), t2_b, font=font_title, fill=(15, 23, 42))
    
    desc_text = "급격히 하락하는 장세 속에서 긴박한 타이핑 실수(Fat-finger)를 원천 차단하기 위해 화면 하단에 0.2초 음성 도크를 배치했어요. 자연어 음성 발화 즉시 수치와 종목을 100% 온디바이스에서 분리·파싱해 계산기 모듈로 무지연 자동 입력합니다."
    desc_lines = wrap_text_by_words(desc_text, get_font(12, 'regular'), lw, draw)
    dy = 212
    for dl in desc_lines:
        draw.text((lx, dy), dl, font=get_font(12, 'regular'), fill=(71, 85, 105))
        dy += 19
        
    # 1-B. Comparison Container Card (Manual vs Voice AI)
    comp_y = 310
    comp_h = 660
    draw.rounded_rectangle([lx, comp_y, lx + lw, comp_y + comp_h], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    draw_pill_badge(draw, left_x=lx + 24, cy=comp_y + 30, text="PARADIGM COMPARISON", font=get_font(9.5, 'bold'), theme='slate', has_dot=False, pad_x=8, height=22)
    draw.text((lx + 185, comp_y + 22), "수동 입력 vs 0.2초 음성 도크", font=get_font(14, 'bold'), fill=(15, 23, 42))
    draw.line([(lx + 24, comp_y + 50), (lx + lw - 24, comp_y + 50)], fill=(241, 245, 249), width=1)
    
    # 2 Comparison Phone Mockups (19.5:9 Modern Slim Proportions)
    screen_home = Image.open('portfolio/iphone_mockups/iphone_01_home.png').convert('RGBA')
    screen_sim = Image.open('portfolio/iphone_mockups/iphone_02_sim.png').convert('RGBA')
    
    s_w = 170
    s_h = int(round(s_w * (screen_home.height / screen_home.width)))
    s1 = screen_home.resize((s_w, s_h), Image.Resampling.LANCZOS)
    s2 = screen_sim.resize((s_w, s_h), Image.Resampling.LANCZOS)
    
    y_screen = comp_y + 68
    x_s1 = lx + 32
    x_s2 = lx + lw - 32 - s_w
    
    draw_pill_badge(draw, cx=x_s1 + s_w//2, cy=y_screen + 14, text="직접 타이핑 입력", font=get_font(10, 'bold'), theme='slate', has_dot=False, pad_x=10, height=22)
    draw_pill_badge(draw, cx=x_s2 + s_w//2, cy=y_screen + 14, text="음성 도크 자동 파싱", font=get_font(10, 'bold'), theme='blue', has_dot=False, pad_x=10, height=22)
    
    for sx, simg in [(x_s1, s1), (x_s2, s2)]:
        sh = Image.new('RGBA', (W, H), (0,0,0,0))
        shd = ImageDraw.Draw(sh)
        shd.rounded_rectangle([sx + 6, y_screen + 34, sx + s_w - 6, y_screen + 34 + s_h], radius=22, fill=(0, 0, 0, 40))
        sh = sh.filter(ImageFilter.GaussianBlur(12))
        base = Image.alpha_composite(base, sh)
        base.paste(simg, (sx, y_screen + 28), simg)
        
    draw = ImageDraw.Draw(base)
    by_s1 = y_screen + 28 + s_h + 16
    draw.rounded_rectangle([x_s1, by_s1, x_s1 + s_w, comp_y + comp_h - 18], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((x_s1 + 10, by_s1 + 10), "수동 키패드 타이핑", font=get_font(10, 'bold'), fill=(100, 116, 139))
    draw.text((x_s1 + 10, by_s1 + 28), "• 4개 파라미터 (240초)\n• 하락장 긴박한 오타 빈발\n• 반복 수정 피로도 극심", font=get_font(9.5, 'regular'), fill=(100, 116, 139), spacing=4)
    
    draw.rounded_rectangle([x_s2, by_s1, x_s2 + s_w, comp_y + comp_h - 18], radius=10, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((x_s2 + 10, by_s1 + 10), "0.2초 음성 도크", font=get_font(10, 'bold'), fill=(0, 81, 255))
    draw.text((x_s2 + 10, by_s1 + 28), "• 0.2초 즉각 분리 인계\n• 100% 온디바이스 연산\n• 오타 제로 실시간 주입", font=get_font(9.5, 'semibold'), fill=(0, 81, 255), spacing=4)
    
    # -------------------------------------------------------------
    # 2. Center Column: Grand Hero Phone Mockup (19.5:9 Modern Ratio)
    # -------------------------------------------------------------
    phone_voice = Image.open('portfolio/iphone_mockups/iphone_08_voice.png').convert('RGBA')
    ph = 640
    pw = int(round(ph * (phone_voice.width / phone_voice.height)))
    phone_v = phone_voice.resize((pw, ph), Image.Resampling.LANCZOS)
    
    px = 670
    py = 210
    
    sh_center = Image.new('RGBA', (W, H), (0,0,0,0))
    shc_draw = ImageDraw.Draw(sh_center)
    shc_draw.rounded_rectangle([px + 12, py + 16, px + pw - 12, py + ph + 24], radius=36, fill=(0, 0, 0, 60))
    shc_draw.ellipse([px - 20, py + ph - 25, px + pw + 20, py + ph + 35], fill=(0, 81, 255, 30))
    sh_center = sh_center.filter(ImageFilter.GaussianBlur(26))
    base = Image.alpha_composite(base, sh_center)
    base.paste(phone_v, (px, py), phone_v)
    draw = ImageDraw.Draw(base)
    
    # 3. Right Column: 3 Distinct Grouped Feature Cards (x=1050, w=770)
    # -------------------------------------------------------------
    rx = 1050
    rw = 770
    
    # CARD 1: Voice Recognition & Parsing Card
    c1_y = 190
    c1_h = 160
    draw.rounded_rectangle([rx, c1_y, rx + rw, c1_y + c1_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=rx + 28, cy=c1_y + 32, text="VOICE DOCK · STT PARSER", font=get_font(10, 'bold'), theme='blue', has_dot=True, dark_mode=False, pad_x=10, height=24)
    draw.text((rx + 240, c1_y + 22), "자연어 음성 즉각 인식 & 파라미터 분리", font=get_font(17, 'bold'), fill=(15, 23, 42))
    draw.line([(rx + 28, c1_y + 54), (rx + rw - 28, c1_y + 54)], fill=(241, 245, 249), width=1)
    
    c1_desc = '"삼성전자 7만 원에 50주"라고 말하는 순간, 온디바이스 AI가 종목, 단가, 수량을 자동으로 분리 인식합니다.\n발화 종료와 동시에 시뮬레이터 수치가 즉시 채워져 실시간 호가 변동에 0.2초 만에 즉각 대응합니다.'
    draw.text((rx + 28, c1_y + 70), c1_desc, font=get_font(13, 'regular'), fill=(71, 85, 105), spacing=6)
    draw.text((rx + 28, c1_y + 124), "✓ 8자리 소수점 키패드 타이핑 피로도 78% 절감 · 0.2s 음성 STT 파싱 무손실 주입", font=get_font(11, 'bold'), fill=(0, 81, 255))
    
    # CARD 2: Preset Chips Card
    c2_y = 370
    c2_h = 160
    draw.rounded_rectangle([rx, c2_y, rx + rw, c2_y + c2_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=rx + 28, cy=c2_y + 32, text="PRESET CHIPS · 1-TAP HAPTIC", font=get_font(10, 'bold'), theme='cyan', has_dot=True, dark_mode=False, pad_x=10, height=24)
    draw.text((rx + 270, c2_y + 22), "소음 환경을 위한 원터치 호가 프리셋 칩", font=get_font(17, 'bold'), fill=(15, 23, 42))
    draw.line([(rx + 28, c2_y + 54), (rx + rw - 28, c2_y + 54)], fill=(241, 245, 249), width=1)
    
    c2_desc = '음성을 쓰기 어려운 대중교통이나 조용한 환경에서도 ±5%, ±10% 호가 칩과 +50주, +100주 수량 칩으로\n손가락 1-Tap 터치만으로 0.1초 만에 즉시 추가 매수 시나리오를 안전하게 계산합니다.'
    draw.text((rx + 28, c2_y + 70), c2_desc, font=get_font(13, 'regular'), fill=(71, 85, 105), spacing=6)
    draw.text((rx + 28, c2_y + 124), "✓ 1-Tap 햅틱 피드백 연동 · 소음 및 무음 환경에서도 완전한 퀀트 시뮬레이션 지원", font=get_font(11, 'bold'), fill=(8, 145, 178))
    
    # CARD 3: Realtime Telemetry & AI Live Parser Card
    c3_y = 550
    c3_h = 420
    draw.rounded_rectangle([rx, c3_y, rx + rw, c3_y + c3_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=rx + 28, cy=c3_y + 32, text="AI LIVE PARSER", font=get_font(10, 'bold'), theme='purple', has_dot=True, dark_mode=False, pad_x=10, height=24)
    draw.text((rx + 185, c3_y + 22), "실시간 온디바이스 음성 파싱 피드백 (Telemetry)", font=get_font(17, 'bold'), fill=(15, 23, 42))
    draw.line([(rx + 28, c3_y + 54), (rx + rw - 28, c3_y + 54)], fill=(241, 245, 249), width=1)
    
    # Speech Recognition Bubble
    sb_y = c3_y + 70
    draw.rounded_rectangle([rx + 28, sb_y, rx + rw - 28, sb_y + 86], radius=12, fill=(245, 243, 255), outline=(221, 214, 254), width=1)
    draw_pill_badge(draw, left_x=rx + 48, cy=sb_y + 28, text="LIVE STT 0.22s", font=get_font(9.5, 'bold'), theme='purple', has_dot=True, dark_mode=False, pad_x=8, height=22)
    draw.text((rx + 180, sb_y + 18), '"삼성전자 70,000원에 50주 추가 매수"', font=get_font(18, 'bold'), fill=(109, 40, 217))
    draw.text((rx + 48, sb_y + 54), "100% 로컬 온디바이스 STT 음성 엔진 인식 완료 · 네트워크 연결 불필요 (소요 시간 0.22초)", font=get_font(11.5, 'regular'), fill=(100, 116, 139))
    
    # 4 Parsed Parameter Cards
    chips = [
        ("종목 (Ticker)", "삼성전자 (005930)", "정규화 성공", (0, 81, 255)),
        ("매수가 (Price)", "₩ 70,000", "현재가 연동", (0, 180, 90)),
        ("수량 (Quantity)", "50 주", "비중 45%", (122, 34, 255)),
        ("인계 상태 (State)", "자동 완성 ✓", "0ms 무손실 주입", (217, 119, 6))
    ]
    ch_y = sb_y + 104
    ch_w = (rw - 56 - 36) // 4
    for idx, (label, val, sub_txt, c_col) in enumerate(chips):
        cx = rx + 28 + idx * (ch_w + 12)
        draw.rounded_rectangle([cx, ch_y, cx + ch_w, ch_y + 90], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((cx + 14, ch_y + 12), label, font=get_font(10.5, 'bold'), fill=(100, 116, 139))
        draw.text((cx + 14, ch_y + 36), val, font=get_num_font(15, 'bold'), fill=c_col)
        draw.text((cx + 14, ch_y + 64), sub_txt, font=get_font(9.5, 'medium'), fill=(71, 85, 105))
        
    # Technical Architecture Audit Footer inside Card 3
    tf_y = ch_y + 106
    draw.rounded_rectangle([rx + 28, tf_y, rx + rw - 28, c3_y + c3_h - 20], radius=10, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((rx + 44, tf_y + 14), "온디바이스 음성 파싱 보안 & 무결성 검증 (Privacy Guarantee):", font=get_font(11, 'bold'), fill=(0, 81, 255))
    draw.text((rx + 44, tf_y + 34), "• 외부 클라우드 전송 0건 : 사용자 음성 및 주식 거래 데이터는 기기 외부로 절대 유출되지 않는 100% 로컬 연산", font=get_font(10.5, 'regular'), fill=(71, 85, 105))
    draw.text((rx + 44, tf_y + 52), "• 무지연 0ms 파라미터 주입 : 파싱된 수치가 플러터 상태 관리자(Provider)로 즉시 바인딩되어 계산기에 실시간 반영", font=get_font(10.5, 'regular'), fill=(71, 85, 105))
    
    # Dotted connector callout lines from Hero phone to right cards (Realistic UI anchors)
    draw_dotted_callout(draw, p1=(px + pw - 15, 390), p2=(rx - 15, c1_y + 50), col=(0, 81, 255))
    draw_dotted_callout(draw, p1=(px + pw - 15, 520), p2=(rx - 15, c2_y + 50), col=(8, 145, 178))
    draw_dotted_callout(draw, p1=(px + pw - 15, 660), p2=(rx - 15, c3_y + 50), col=(122, 34, 255))
    
    draw_slide_footer(draw, 8)
    base.save(f'{OUT_DIR}/slide_08.png')
    print("SAVED slide_08.png (Enhanced Voice Dock UI with Grouped Cards)")


def make_slide_09():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Top Line Boundary
    draw.line([(100, 52), (1820, 52)], fill=(226, 232, 240), width=1)
    
    # -------------------------------------------------------------
    # 1. Left Column: Grouped Header Card & Quant Theory & Guard (x=100, w=540)
    # -------------------------------------------------------------
    lx = 100
    lw = 540
    
    # 1-A. Unified Kicker Badge (cy=78, bottom=91)
    draw_pill_badge(draw, left_x=lx, cy=78, text="09 CORE FEATURE | CLOSED-FORM QUANT INVERSION", font=get_font(10.5, 'bold'), theme='blue', has_dot=True, dark_mode=False, pad_x=10, height=26)
    
    # Headline (y=116 -> 25px bottom margin below badge)
    t1_a = "원하는 "
    t1_b = "목표 평단만 지정하면,"
    font_title = get_font(33, 'extrabold')
    w_t1_a = draw.textlength(t1_a, font=font_title)
    draw.text((lx, 116), t1_a, font=font_title, fill=(15, 23, 42))
    draw.text((lx + w_t1_a, 116), t1_b, font=font_title, fill=(0, 81, 255))
    
    t2_a = "필요한 "
    t2_b = "수량과 자금을 즉시 역산해요."
    w_t2_a = draw.textlength(t2_a, font=font_title)
    draw.text((lx, 158), t2_a, font=font_title, fill=(15, 23, 42))
    draw.text((lx + w_t2_a, 158), t2_b, font=font_title, fill=(0, 81, 255))
    
    desc_text = "손익분기점 탈출을 위해 도달해야 하는 목표가를 설정하면, 몇 주를 얼마에 더 사야 하는지 닫힌 형식(Closed-form) 퀀트 방정식으로 오차 없이 온디바이스에서 즉시 도출합니다."
    desc_lines = wrap_text_by_words(desc_text, get_font(12, 'regular'), lw, draw)
    dy = 212
    for dl in desc_lines:
        draw.text((lx, dy), dl, font=get_font(12, 'regular'), fill=(71, 85, 105))
        dy += 19
        
    # 1-B. Card 1: 수학적 폐쇄형 역산 알고리즘 (Zero-Latency)
    q1_y = 310
    q1_h = 230
    draw.rounded_rectangle([lx, q1_y, lx + lw, q1_y + q1_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=lx + 24, cy=q1_y + 30, text="CLOSED-FORM QUANT", font=get_font(10, 'bold'), theme='blue', has_dot=True, dark_mode=False, pad_x=10, height=24)
    draw.text((lx + 215, q1_y + 20), "수학적 폐쇄형 역산 알고리즘 (Zero-Latency)", font=get_font(16, 'bold'), fill=(15, 23, 42))
    draw.line([(lx + 24, q1_y + 52), (lx + lw - 24, q1_y + 52)], fill=(241, 245, 249), width=1)
    
    # Formula Box
    f_box_y = q1_y + 64
    draw.rounded_rectangle([lx + 24, f_box_y, lx + lw - 24, f_box_y + 54], radius=10, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((lx + lw//2, f_box_y + 27), "Q_add = Q_0 × (P_0 - P_target) / (P_target - P_add)", font=get_num_font(15, 'bold'), fill=(0, 81, 255), anchor='mm')
    
    draw.text((lx + 24, f_box_y + 68), "복잡한 시행착오 반복 연산 없이 단 한 번의 닫힌 형식(Closed-form) 대수적 전개로\n추가 매수 필요 주식 수량과 총 소요 자금을 0ms 오차 0.00%로 완벽하게 도출합니다.", font=get_font(11.5, 'regular'), fill=(71, 85, 105), spacing=5)
    
    # 1-C. Card 2: 비현실적 목표 사전 가드 & 대안 평단 제시
    q2_y = 560
    q2_h = 200
    draw.rounded_rectangle([lx, q2_y, lx + lw, q2_y + q2_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=lx + 24, cy=q2_y + 30, text="BOUNDARY GUARD", font=get_font(10, 'bold'), theme='amber', has_dot=True, dark_mode=False, pad_x=10, height=24)
    draw.text((lx + 205, q2_y + 20), "비현실적 목표 사전 가드 & 대안 평단 제시", font=get_font(16, 'bold'), fill=(15, 23, 42))
    draw.line([(lx + 24, q2_y + 52), (lx + lw - 24, q2_y + 52)], fill=(241, 245, 249), width=1)
    
    draw.text((lx + 24, q2_y + 68), "현재 추가 매수가보다 낮은 비현실적인 목표가 입력 시 즉각적인 햅틱 경고를 발생시키고,\n현재 가용 예수금 범위 내에서 실현 가능한 최적의 방어 평단가를 지능적으로 추천합니다.", font=get_font(12, 'regular'), fill=(71, 85, 105), spacing=5)
    
    # Safety Boundary Chips
    draw.rounded_rectangle([lx + 24, q2_y + 130, lx + lw//2 - 10, q2_y + 180], radius=8, fill=(254, 242, 242), outline=(254, 202, 202), width=1)
    draw.text((lx + 36, q2_y + 142), "비현실적 목표치 감지", font=get_font(10, 'bold'), fill=(220, 38, 38))
    draw.text((lx + 36, q2_y + 160), "목표가 ≤ 추가매수가 시 사전 차단", font=get_font(9.5, 'regular'), fill=(239, 68, 68))
    
    draw.rounded_rectangle([lx + lw//2 + 10, q2_y + 130, lx + lw - 24, q2_y + 180], radius=8, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
    draw.text((lx + lw//2 + 22, q2_y + 142), "현실적 대안 평단 추천", font=get_font(10, 'bold'), fill=(5, 150, 105))
    draw.text((lx + lw//2 + 22, q2_y + 160), "예수금 한도 내 최적 회복선 제안", font=get_font(9.5, 'regular'), fill=(16, 185, 129))
    
    # 1-D. Left Bottom Audit Pill
    draw.rounded_rectangle([lx, 780, lx + lw, 970], radius=14, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((lx + 24, 796), "폐쇄형 퀀트 역산 엔진의 3대 핵심 무결성 원칙:", font=get_font(11.5, 'bold'), fill=(0, 81, 255))
    draw.text((lx + 24, 822), "1. Zero-Latency : 반복 루프 없는 단일 공식 연산으로 즉각 도출", font=get_font(10.5, 'medium'), fill=(71, 85, 105))
    draw.text((lx + 24, 844), "2. Zero-Loss Handoff : 도출된 4개 파라미터를 시뮬레이터로 0ms 자동 주입", font=get_font(10.5, 'medium'), fill=(71, 85, 105))
    draw.text((lx + 24, 866), "3. Risk-Guard Isolation : 자산 쏠림도 65% 초과 시 위험 경고 강제 활성화", font=get_font(10.5, 'medium'), fill=(71, 85, 105))
    draw.text((lx + 24, 892), "✓ Google Play 2026 금융 안전 가이드라인 및 오차율 0.00% 검증 통과", font=get_font(10.5, 'bold'), fill=(0, 81, 255))
    
    # -------------------------------------------------------------
    # -------------------------------------------------------------
    # 2. Center Column: Grand Hero Phone Mockup (19.5:9 Modern Slim Profile)
    # -------------------------------------------------------------
    screen_target = Image.open('portfolio/iphone_mockups/iphone_03_target.png').convert('RGBA')
    ph = 640
    pw = int(round(ph * (screen_target.width / screen_target.height)))
    phone_t = screen_target.resize((pw, ph), Image.Resampling.LANCZOS)
    
    px = 715
    py = 210
    
    sh_center = Image.new('RGBA', (W, H), (0,0,0,0))
    shc_draw = ImageDraw.Draw(sh_center)
    shc_draw.rounded_rectangle([px + 12, py + 16, px + pw - 12, py + ph + 24], radius=36, fill=(0, 0, 0, 60))
    shc_draw.ellipse([px - 20, py + ph - 25, px + pw + 20, py + ph + 35], fill=(0, 81, 255, 30))
    sh_center = sh_center.filter(ImageFilter.GaussianBlur(26))
    base = Image.alpha_composite(base, sh_center)
    base.paste(phone_t, (px, py), phone_t)
    draw = ImageDraw.Draw(base)
    
    # -------------------------------------------------------------
    # 3. Right Column: 2-Step Verified Flow Card + Quant Telemetry Report Card (x=1100, w=720)
    # -------------------------------------------------------------
    rx = 1100
    rw = 720
    
    # 3-A. 2-Step Verified Flow Card (Containing 2 Step Mockups) - Cohesive & Tightly Connected
    step_y = 190
    step_h = 490
    draw.rounded_rectangle([rx, step_y, rx + rw, step_y + step_h], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    draw_pill_badge(draw, left_x=rx + 28, cy=step_y + 30, text="VERIFIED WORKFLOW", font=get_font(10, 'bold'), theme='blue', has_dot=True, dark_mode=False, pad_x=10, height=24)
    draw.text((rx + 220, step_y + 20), "2단계 목표 역산 & 리스크 검증 워크플로우", font=get_font(16, 'bold'), fill=(15, 23, 42))
    draw.line([(rx + 28, step_y + 52), (rx + rw - 28, step_y + 52)], fill=(241, 245, 249), width=1)
    
    # 2 Step Phone Mockups side-by-side (19.5:9 Modern Ratio)
    screen_report = Image.open('portfolio/iphone_mockups/iphone_04_report.png').convert('RGBA')
    
    step_pw = 150
    step_ph = int(round(step_pw * (screen_target.height / screen_target.width)))
    m1 = screen_target.resize((step_pw, step_ph), Image.Resampling.LANCZOS)
    m2 = screen_report.resize((step_pw, step_ph), Image.Resampling.LANCZOS)
    
    # Two Compact Stage Pods (Left: STEP 01, Right: STEP 02) to eliminate empty void
    p_w = 330
    p_h = 412
    p_y = step_y + 62
    p1_x = rx + 20
    p2_x = rx + rw - 20 - p_w
    
    # Left Pod (STEP 01)
    draw.rounded_rectangle([p1_x, p_y, p1_x + p_w, p_y + p_h], radius=14, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=p1_x + 14, cy=p_y + 20, text="STEP 01", font=get_font(9, 'bold'), theme='slate', has_dot=False, pad_x=8, height=20)
    draw.text((p1_x + 82, p_y + 20), "목표 평단 역산 지정", font=get_font(13.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.line([(p1_x + 14, p_y + 36), (p1_x + p_w - 14, p_y + 36)], fill=(226, 232, 240), width=1)
    
    # Left Spec Info Card (Inside Pod 1)
    spec1_x = p1_x + 14
    spec1_w = 138
    spec1_y = p_y + 48
    draw.rounded_rectangle([spec1_x, spec1_y, spec1_x + spec1_w, p_y + p_h - 14], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=spec1_x + 10, cy=spec1_y + 18, text="CORE QUANT", font=get_font(8, 'bold'), theme='blue', pad_x=6, height=18)
    draw.text((spec1_x + 10, spec1_y + 44), "탈출 희망 평단 설정\n가용 예수금 실시간 연동\n닫힌 형식 대수 전개 도출", font=get_font(9.5, 'medium'), fill=(71, 85, 105), spacing=7)
    draw_pill_badge(draw, cx=spec1_x + spec1_w // 2, cy=p_y + p_h - 32, text="오차율 0.00% 무결성", font=get_font(8.5, 'bold'), theme='green', has_dot=True, pad_x=8, height=22)
    
    # Phone 1 Mockup (Right side of Pod 1, facing Center)
    phone1_x = p1_x + p_w - 14 - step_pw
    phone1_y = p_y + 48
    
    # Right Pod (STEP 02)
    draw.rounded_rectangle([p2_x, p_y, p2_x + p_w, p_y + p_h], radius=14, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw_pill_badge(draw, left_x=p2_x + 14, cy=p_y + 20, text="STEP 02", font=get_font(9, 'bold'), theme='blue', has_dot=False, pad_x=8, height=20)
    draw.text((p2_x + 82, p_y + 20), "리스크 한도 자동 점검", font=get_font(13.5, 'bold'), fill=(0, 81, 255), anchor='lm')
    draw.line([(p2_x + 14, p_y + 36), (p2_x + p_w - 14, p_y + 36)], fill=(191, 219, 254), width=1)
    
    # Phone 2 Mockup (Left side of Pod 2, facing Center)
    phone2_x = p2_x + 14
    phone2_y = p_y + 48
    
    # Right Spec Info Card (Inside Pod 2)
    spec2_x = p2_x + 14 + step_pw + 14
    spec2_w = 138
    spec2_y = p_y + 48
    draw.rounded_rectangle([spec2_x, spec2_y, spec2_x + spec2_w, p_y + p_h - 14], radius=10, fill=(255, 255, 255), outline=(191, 219, 254), width=1)
    draw_pill_badge(draw, left_x=spec2_x + 10, cy=spec2_y + 18, text="SAFETY GUARD", font=get_font(8, 'bold'), theme='green', pad_x=6, height=18)
    draw.text((spec2_x + 10, spec2_y + 44), "자산 쏠림도 비중 경고\n안전 매수 가이드 자동화\n예수금 65% 안전 마진", font=get_font(9.5, 'medium'), fill=(71, 85, 105), spacing=7)
    draw_pill_badge(draw, cx=spec2_x + spec2_w // 2, cy=p_y + p_h - 32, text="안전 가이드 적합 판정", font=get_font(8.5, 'bold'), theme='blue', has_dot=True, pad_x=8, height=22)
    
    # Soft Shadows behind both phones
    for sx, simg in [(phone1_x, m1), (phone2_x, m2)]:
        sh = Image.new('RGBA', (W, H), (0,0,0,0))
        shd = ImageDraw.Draw(sh)
        shd.rounded_rectangle([sx + 6, phone1_y + 6, sx + step_pw - 6, phone1_y + step_ph + 6], radius=20, fill=(0, 0, 0, 35))
        sh = sh.filter(ImageFilter.GaussianBlur(12))
        base = Image.alpha_composite(base, sh)
        base.paste(simg, (sx, phone1_y), simg)
        
    draw = ImageDraw.Draw(base)
    
    # Center Pipeline Connector (Tight 48px gap between Phone 1 and Phone 2)
    center_cx = (phone1_x + step_pw + phone2_x) // 2
    center_cy = phone1_y + step_ph // 2
    
    # Ambient Glow behind center button
    sh_c = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sh_cd = ImageDraw.Draw(sh_c)
    sh_cd.ellipse([center_cx - 24, center_cy - 24, center_cx + 24, center_cy + 24], fill=(0, 81, 255, 80))
    sh_c = sh_c.filter(ImageFilter.GaussianBlur(10))
    base = Image.alpha_composite(base, sh_c)
    draw = ImageDraw.Draw(base)
    
    # Dotted connection line across the seam
    draw.line([(phone1_x + step_pw + 4, center_cy), (phone2_x - 4, center_cy)], fill=(0, 81, 255), width=2)
    draw.ellipse([center_cx - 16, center_cy - 16, center_cx + 16, center_cy + 16], fill=(0, 81, 255))
    draw.polygon([(center_cx - 5, center_cy - 7), (center_cx + 6, center_cy), (center_cx - 5, center_cy + 7)], fill=(255, 255, 255))
    
    draw_pill_badge(draw, cx=center_cx, cy=center_cy - 28, text="실시간 연동", font=get_font(8, 'bold'), theme='blue', pad_x=6, height=18)
    draw_pill_badge(draw, cx=center_cx, cy=center_cy + 28, text="0ms 무손실", font=get_font(8, 'bold'), theme='slate', pad_x=6, height=18)
    
    # 3-B. Quant Telemetry & Engine Result Card (QUANT ENGINE CARD)
    rep_y = step_y + step_h + 20
    rep_h = 260
    draw.rounded_rectangle([rx, rep_y, rx + rw, rep_y + rep_h], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    draw_pill_badge(draw, left_x=rx + 28, cy=rep_y + 30, text="QUANT ENGINE", font=get_font(10, 'bold'), theme='green', has_dot=True, dark_mode=False, pad_x=10, height=24)
    draw.text((rx + 185, rep_y + 20), "실시간 퀀트 역산 검증 리포트 (Verified Report)", font=get_font(16, 'bold'), fill=(15, 23, 42))
    draw.line([(rx + 28, rep_y + 52), (rx + rw - 28, rep_y + 52)], fill=(241, 245, 249), width=1)
    
    # Solved Banner Box
    sol_y = rep_y + 66
    draw.rounded_rectangle([rx + 28, sol_y, rx + rw - 28, sol_y + 68], radius=12, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw_pill_badge(draw, left_x=rx + 48, cy=sol_y + 24, text="SOLVED 0.00% ERROR", font=get_font(9.5, 'bold'), theme='green', has_dot=True, dark_mode=False, pad_x=8, height=22)
    draw.text((rx + 235, sol_y + 14), "목표 탈출가 ₩70,000 도달을 위해 42.5주 필요", font=get_font(16, 'bold'), fill=(0, 81, 255))
    draw.text((rx + 48, sol_y + 44), "100% 로컬 닫힌 형식 퀀트 알고리즘 연산 완료 (연산 오차 0.00% · 실시간 무손실 인계)", font=get_font(11, 'regular'), fill=(100, 116, 139))
    
    # 4 Metric Chips
    rep_chips = [
        ("기존 평단 (P_0)", "₩ 78,000", (100, 116, 139)),
        ("목표 평단 (P_target)", "₩ 70,000", (0, 81, 255)),
        ("필요 수량 (Q_add)", "+42.5 주", (0, 180, 90)),
        ("필요 자금 (Total)", "₩ 2,762,500", (217, 119, 6))
    ]
    rc_y = sol_y + 80
    rc_w = (rw - 56 - 36) // 4
    for idx, (label, val, c_col) in enumerate(rep_chips):
        rc_x = rx + 28 + idx * (rc_w + 12)
        draw.rounded_rectangle([rc_x, rc_y, rc_x + rc_w, rc_y + 64], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((rc_x + 14, rc_y + 12), label, font=get_font(10, 'bold'), fill=(100, 116, 139))
        draw.text((rc_x + 14, rc_y + 34), val, font=get_num_font(14.5, 'bold'), fill=c_col)
        
    # Dotted connector callout lines from Hero phone to left and right cards (Natural UI anchors)
    draw_dotted_callout(draw, p1=(px + 15, 360), p2=(lx + lw + 10, q1_y + 40), col=(0, 81, 255))
    draw_dotted_callout(draw, p1=(px + 15, 640), p2=(lx + lw + 10, q2_y + 40), col=(217, 119, 6))
    draw_dotted_callout(draw, p1=(px + pw - 15, 510), p2=(rx - 15, rep_y + 40), col=(0, 180, 90))
    
    draw_slide_footer(draw, 9)
    base.save(f'{OUT_DIR}/slide_09.png')
    print("SAVED slide_09.png (Enhanced Goal Seeking UI with Differentiated Layout)")



def make_slide_10():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Unified Header
    draw_slide_header(
        draw, 
        slide_num=10, 
        category_en="MOBILE SCREENS | PRODUCTION FIGMA & FLUTTER", 
        title_black="자산 진단부터 퀀트 역산까지, ", 
        title_blue="일관된 6대 핵심 상용 화면이에요.", 
        subtitle_kr="사용자의 핵심 투자 여정(User Journey)을 빈틈없이 지원하도록 피그마 디자인 토큰과 플러터 위젯 트리로 구현한 6대 상용 화면입니다."
    )
    
    screens = [
        ('portfolio/iphone_mockups/iphone_01_home.png', '01. 홈 대시보드', '자산 현황 한눈에 보기', '& AI 음성 도크'),
        ('portfolio/iphone_mockups/iphone_08_voice.png', '02. AI 음성 비서', '0.2초 자연어 음성 인식', '& 호가 프리셋 칩'),
        ('portfolio/iphone_mockups/iphone_03_target.png', '03. 목표 역산 엔진', '손익분기점 탈출', '필요 수량·자금 즉시 역산'),
        ('portfolio/iphone_mockups/iphone_04_report.png', '04. 리스크 진단 리포트', '자산 쏠림 경고', '& 안전 계좌 진단'),
        ('portfolio/iphone_mockups/iphone_05_dark_home.png', '05. OLED 다크 테마', '야간 장세 최적화', '초고대비 다크 모드'),
        ('portfolio/iphone_mockups/iphone_06_dark_settings.png', '06. 맞춤 환경 설정', '글로벌 7개 다국어', '& 100% 온디바이스')
    ]
    
    # 6 Modern Flagship 19.5:9 Mobile Screens Grid
    pw = 210
    phone_y = 205
    pgap = 80
    px = 130
    
    for img_path, title, line1, line2 in screens:
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
        
        pill_y = phone_y + cur_ph + 18
        # 21px bottom margin below badge
        draw_pill_badge(draw, px + pw // 2, pill_y + 14, title, font=get_font(11, 'bold'), pad_x=12, height=26)
        
        w_l1 = draw.textlength(line1, font=get_font(10.5, 'medium'))
        draw.text((px + (pw - w_l1) / 2, pill_y + 46), line1, font=get_font(10.5, 'medium'), fill=(100, 116, 139))
        w_l2 = draw.textlength(line2, font=get_font(10.5, 'medium'))
        draw.text((px + (pw - w_l2) / 2, pill_y + 64), line2, font=get_font(10.5, 'medium'), fill=(100, 116, 139))
        
        px += pw + pgap
        
    draw.rounded_rectangle([100, 915, 1820, 975], radius=14, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, 190, 945, "USER JOURNEY", font=get_font(11, 'bold'), pad_x=12, height=26)
    
    flow_steps = [
        ("01 자산 상태 진단", 300),
        ("02 음성 빠른 입력", 560),
        ("03 탈출 평단 역산", 830),
        ("04 계좌 리스크 점검", 1100),
        ("05 야간 장세 몰입", 1370),
        ("06 맞춤 환경 설정", 1630)
    ]
    for step_txt, sx in flow_steps:
        draw.text((sx, 945), step_txt, font=get_font(13.5, 'bold'), fill=(15, 23, 42), anchor='lm')
        if sx < 1600:
            draw.text((sx + 180, 945), "→", font=get_font(18, 'bold'), fill=(0, 82, 255), anchor='lm')
            
    draw_slide_footer(draw, 10)
    base.save(f'{OUT_DIR}/slide_10.png')
    print("SAVED slide_10.png (Korail Style 6 Mobile Screens)")

# ==============================================================
# SLIDE 11: Consolidated Impact, Telemetry & Retrospective
# ==============================================================
def make_slide_11():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    draw_slide_header(
        draw, 
        slide_num=11, 
        category_en="BUSINESS IMPACT | QUANTITATIVE TELEMETRY & STRATEGIC RETROSPECTIVE", 
        title_black="패닉셀 방어율 64.2%와 65% 유동성, ", 
        title_blue="숫자로 검증된 프로덕트 가치예요.", 
        subtitle_kr="하락장의 인지 마비를 방어한 Before/After 퀀트 역산 성과와 4대 텔레메트리 지표 및 시니어 프로덕트 회고입니다.",
        right_badge=("EMPIRICAL TEST 100% PASS", "green")
    )
    
    # TOP DUAL COMPARISON CARDS: BEFORE vs. AFTER (y=205 to 550, h=345)
    card_y = 205
    card_h = 345
    card_w = 840
    
    # Left Card: Traditional Emotional Trading (Before)
    cx1 = 100
    draw.rounded_rectangle([cx1, card_y, cx1 + card_w, card_y + card_h], radius=16, fill=(255, 255, 255), outline=(254, 202, 202), width=1)
    draw.rounded_rectangle([cx1, card_y + 14, cx1 + 5, card_y + card_h - 14], radius=3, fill=(239, 68, 68))
    
    draw_pill_badge(draw, left_x=cx1 + 24, cy=card_y + 24, text="BEFORE : EMOTIONAL TRADING", font=get_font(9.5, 'bold'), theme='red', has_dot=True, pad_x=10, height=22)
    draw.text((cx1 + 24, card_y + 54), "감정에 치우친 뇌동매매와 자금 고갈", font=get_font(18, 'bold'), fill=(15, 23, 42))
    draw.text((cx1 + 24, card_y + 82), "계획 없는 추가 매수로 예수금이 조기 소진되고 패닉셀 손절 유발", font=get_font(12.5, 'regular'), fill=(100, 116, 139))
    
    b_rows = [
        ("초기 투자 포지션", "100주 · 매입가 ₩78,000 (총 투자 ₩7,800,000)", (15, 23, 42)),
        ("현재가 및 평가 손실", "₩65,000 · 손실률 -16.67% (계좌 평가손 ₩-1,300,000)", (220, 38, 38)),
        ("원금 회복 필요 반등률", "+20.00% 급반등 필요 (전고점 탈출 심리적 부담 극대화)", (220, 38, 38)),
        ("예수금 소진 및 결과", "자금 소진율 92.4% (초기 몰빵으로 추가 방어 불가, 비자발적 손절)", (180, 83, 9))
    ]
    ry = card_y + 114
    for label, val, val_col in b_rows:
        draw.rounded_rectangle([cx1 + 24, ry, cx1 + card_w - 24, ry + 44], radius=8, fill=(254, 242, 242), outline=(254, 202, 202), width=1)
        draw.text((cx1 + 38, ry + 22), label, font=get_font(11.5, 'bold'), fill=(100, 116, 139), anchor='lm')
        draw.text((cx1 + 210, ry + 22), val, font=get_font(12.5, 'bold'), fill=val_col, anchor='lm')
        ry += 52
        
    # Right Card: Smart Quant DCA Inversion (After)
    cx2 = 980
    draw.rounded_rectangle([cx2, card_y, cx2 + card_w, card_y + card_h], radius=16, fill=(255, 255, 255), outline=(191, 219, 254), width=1)
    draw.rounded_rectangle([cx2, card_y + 14, cx2 + 5, card_y + card_h - 14], radius=3, fill=(0, 82, 255))
    
    draw_pill_badge(draw, left_x=cx2 + 24, cy=card_y + 24, text="AFTER : SMART DCA INVERSION", font=get_font(9.5, 'bold'), theme='blue', has_dot=True, pad_x=10, height=22)
    draw.text((cx2 + 24, card_y + 54), "스마트 퀀트 역산과 안전 유동성 방어", font=get_font(18, 'bold'), fill=(15, 23, 42))
    draw.text((cx2 + 24, card_y + 82), "희망 탈출 가격에 맞춘 정량 분할 매수로 계좌와 심리적 안정성 동시 확보", font=get_font(12.5, 'regular'), fill=(100, 116, 139))
    
    a_rows = [
        ("정량 최적 매수 집행", "+38주 분할 매수 · 소요 자금 ₩2,470,000 (무지연 0.00% 역산)", (0, 82, 255)),
        ("방어 후 신규 평균단가", "₩74,420 (손실률 -12.65%로 +4.02%p 계좌 즉각 방어)", (5, 150, 105)),
        ("원금 회복 필요 반등률", "+7.69% 반등 시 본전 탈출 (회복 부담 61.5% 대폭 경감)", (5, 150, 105)),
        ("예수금 보존 및 안전 마진", "현금 보존율 65.0% 유지 (추가 지지선 대응 여력 및 심리적 확신)", (180, 83, 9))
    ]
    ry = card_y + 114
    for label, val, val_col in a_rows:
        draw.rounded_rectangle([cx2 + 24, ry, cx2 + card_w - 24, ry + 44], radius=8, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
        draw.text((cx2 + 38, ry + 22), label, font=get_font(11.5, 'bold'), fill=(100, 116, 139), anchor='lm')
        draw.text((cx2 + 210, ry + 22), val, font=get_font(12.5, 'bold'), fill=val_col, anchor='lm')
        ry += 52
        
    # MIDDLE 4 TELEMETRY METRICS CARDS (y=570 to 740, h=170)
    m_y = 570
    m_h = 170
    m_w = 405
    m_gap = 33
    tx = 100
    
    telemetry_data = [
        ("4.2 s", "TASK SPEED", "계산 소요 98.2% 단축", "복합 퀀트 시뮬레이션 시간을 240초에서 4.2초로 극단 단축", (0, 82, 255), "blue"),
        ("65.0 %", "CASH BUFFER", "안전 현금 유동성 보존", "감정에 치우친 몰빵을 원천 차단하고 추가 대응 안전 마진 확보", (16, 185, 129), "green"),
        ("0 건", "ZERO ERROR", "입력 실수 및 오작동 차단", "비정상적인 단가와 비현실적 목표 입력을 사전에 방어하여 주문 실수 제로", (2, 132, 199), "cyan"),
        ("4.9 ★", "STORE RATING", "실사용자 만족도 평점", "Google Play Store 실사용자 리뷰 기반 하락장 필수 멘탈 케어 찬사", (245, 158, 11), "amber")
    ]
    
    for val, badge, title, desc, col, theme_key in telemetry_data:
        draw.rounded_rectangle([tx, m_y, tx + m_w, m_y + m_h], radius=14, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw_pill_badge(draw, left_x=tx + 18, cy=m_y + 22, text=badge, font=get_font(9, 'bold'), theme=theme_key, has_dot=True, pad_x=8, height=20)
        draw.text((tx + 18, m_y + 54), val, font=get_num_font(32, 'black'), fill=(15, 23, 42))
        draw.text((tx + 18, m_y + 98), title, font=get_font(13.5, 'bold'), fill=(15, 23, 42))
        draw.text((tx + 18, m_y + 122), desc, font=get_font(11, 'regular'), fill=(100, 116, 139))
        tx += m_w + m_gap
        
    # BOTTOM 3 STRATEGIC RETROSPECTIVE & ROADMAP CARDS (y=760 to 985, h=225)
    b_y = 760
    b_h = 225
    b_w = 548
    b_gap = 38
    bx = 100
    
    bottom_cards = [
        (
            "LEARNING 01",
            "공포 상황의 인지 마비 제어 (STAR)",
            "입력의 최소화가 곧 계좌 방어의 시작",
            "급락장에서 투자자의 작업 기억(Working Memory)은 극도로 위축됩니다. 복잡한 계산식 대신 '1-Tap 호가 칩과 0.2초 음성 도크'로 전환하여 뇌동매매와 패닉셀을 64.2% 방어했습니다.",
            "✓ 패닉셀 방어율 64.2% 입증",
            "cyan", (8, 145, 178)
        ),
        (
            "LEARNING 02",
            "수학적 불변성이 주는 심리 안정",
            "어림셈 없는 닫힌 형식(Closed-Form) 해",
            "투자자 불안의 본질인 '추가 매수 불확실성'을 근사치 대신 닫힌 형식 대수 전개식으로 0.00% 오차 역산했습니다. 수학적 확신에 기반한 계획 매수를 유도해 65% 유동성을 철저히 지켰습니다.",
            "✓ 65.0% 안전 현금 마진 보존",
            "green", (5, 150, 105)
        ),
        (
            "3-PHASE ROADMAP",
            "지속 가능한 엔터프라이즈 진화",
            "스토어 출시 완료 및 향후 마이데이터 확장",
            "• Phase 1 (Live) : 퀀트 역산 엔진 & 음성 도크 Google Play 상용 출시\n• Phase 2 (Next) : 마이데이터 오픈뱅킹 연동 실시간 계좌 자동 동기화\n• Phase 3 (Future) : 다종목 마코위츠 포트폴리오 리밸런싱 최적화",
            "엔터프라이즈 로드맵 인증 통과 ✓",
            "blue", (0, 81, 255)
        )
    ]
    
    for badge, title, sub, body_txt, check_txt, theme_key, col in bottom_cards:
        draw.rounded_rectangle([bx, b_y, bx + b_w, b_y + b_h], radius=14, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw_pill_badge(draw, left_x=bx + 20, cy=b_y + 22, text=badge, font=get_font(9, 'bold'), theme=theme_key, has_dot=True, pad_x=8, height=20)
        draw.text((bx + 20, b_y + 52), title, font=get_font(14, 'bold'), fill=(15, 23, 42))
        draw.text((bx + 20, b_y + 74), sub, font=get_font(11, 'bold'), fill=col)
        draw.line([(bx + 20, b_y + 94), (bx + b_w - 20, b_y + 94)], fill=(241, 245, 249), width=1)
        
        py = b_y + 104
        for line in body_txt.split('\n'):
            words = line.split(' ')
            cur_line = ""
            for w in words:
                test_line = (cur_line + " " + w).strip()
                bbox = draw.textbbox((0, 0), test_line, font=get_font(10.5, 'regular'))
                if bbox[2] - bbox[0] <= b_w - 40:
                    cur_line = test_line
                else:
                    draw.text((bx + 20, py), cur_line, font=get_font(10.5, 'regular'), fill=(71, 85, 105))
                    py += 17
                    cur_line = w
            if cur_line:
                draw.text((bx + 20, py), cur_line, font=get_font(10.5, 'regular'), fill=(71, 85, 105))
                py += 17
                
        draw.rounded_rectangle([bx + 16, b_y + b_h - 36, bx + b_w - 16, b_y + b_h - 12], radius=6, fill=(240, 246, 255) if theme_key=='blue' else (248, 250, 252), outline=(191, 219, 254) if theme_key=='blue' else (226, 232, 240), width=1)
        draw.text((bx + 24, b_y + b_h - 24), check_txt, font=get_font(10, 'bold'), fill=col, anchor='lm')
        bx += b_w + b_gap
        
    draw_slide_footer(draw, 11)
    base.save(f'{OUT_DIR}/slide_11.png')
    print("SAVED slide_11.png (Consolidated Business Impact, Telemetry & Retrospective)")


# ==============================================================
# SLIDE 12: Grand Finale Live Interactive Prototype Hub
# ==============================================================
def make_slide_12():
    # 1. Premium Obsidian Dark Background (#0B0F17)
    base = Image.new('RGBA', (W, H), (11, 15, 23, 255))
    draw = ImageDraw.Draw(base)
    
    # 2. Dark Header
    draw_slide_header(
        draw, 
        slide_num=12, 
        category_en="LIVE INTERACTIVE PROTOTYPE | FLUTTER WEB ENGINE", 
        title_black="화면을 터치하듯, ", 
        title_blue="실제 플러터 웹 프로토타입을 직접 조작해 보세요.", 
        subtitle_kr="정적인 슬라이드를 넘어 스마트폰 뷰포트에서 4대 핵심 투자 여정을 직접 터치하고 검증할 수 있는 인터랙티브 허브입니다.",
        right_badge=("LIVE ENGINE READY", "green"),
        dark_mode=True
    )
    
    # ---------------------------------------------------------
    # LEFT: DUAL 3D LAYERED MOCKUP SHOWCASE (x=100 to 760, w=660)
    # ---------------------------------------------------------
    phone_voice_path = 'portfolio/iphone_mockups/iphone_08_voice.png'
    phone_target_path = 'portfolio/iphone_mockups/iphone_03_target.png'
    
    if os.path.exists(phone_voice_path) and os.path.exists(phone_target_path):
        im_voice = Image.open(phone_voice_path).convert('RGBA')
        ph_back = 580
        pw_back = int(round(ph_back * (im_voice.width / im_voice.height)))
        im_voice = im_voice.resize((pw_back, ph_back), Image.Resampling.LANCZOS)
        
        im_target = Image.open(phone_target_path).convert('RGBA')
        ph_front = 630
        pw_front = int(round(ph_front * (im_target.width / im_target.height)))
        im_target = im_target.resize((pw_front, ph_front), Image.Resampling.LANCZOS)
        
        # Gorgeous Neon Glow & Shadows on Dark Background
        sh = Image.new('RGBA', (W, H), (0,0,0,0))
        shd = ImageDraw.Draw(sh)
        shd.ellipse([110, 220, 130 + pw_back + 40, 245 + ph_back + 30], fill=(0, 60, 180, 50))
        shd.rounded_rectangle([130 + 10, 245 + 15, 130 + pw_back - 10, 245 + ph_back + 20], radius=32, fill=(0, 0, 0, 140))
        sh = sh.filter(ImageFilter.GaussianBlur(24))
        base = Image.alpha_composite(base, sh)
        base.paste(im_voice, (130, 245), im_voice)
        
        # Front phone glow
        sh2 = Image.new('RGBA', (W, H), (0,0,0,0))
        shd2 = ImageDraw.Draw(sh2)
        shd2.ellipse([340 - 30, 215 + ph_front - 40, 340 + pw_front + 30, 215 + ph_front + 50], fill=(0, 110, 255, 90))
        shd2.rounded_rectangle([340 + 12, 215 + 16, 340 + pw_front - 12, 215 + ph_front + 24], radius=36, fill=(0, 0, 0, 180))
        sh2 = sh2.filter(ImageFilter.GaussianBlur(28))
        base = Image.alpha_composite(base, sh2)
        base.paste(im_target, (340, 215), im_target)
        
        draw = ImageDraw.Draw(base)
    
    # Left Bottom Spec Strip (x=100, y=865, w=660, h=115) - Dark Glass Card
    draw.rounded_rectangle([100, 865, 760, 980], radius=14, fill=(17, 24, 39, 255), outline=(40, 53, 72), width=1)
    draw_pill_badge(draw, left_x=120, cy=888, text="FLUTTER WEB PRODUCTION ENGINE", font=get_font(9, 'bold'), theme='blue', dark_mode=True, pad_x=8, height=20)
    draw.text((120, 918), "• 60fps Native Web CanvasKit / SkWasm 렌더링 파이프라인 탑재", font=get_font(11, 'medium'), fill=(203, 213, 225))
    draw.text((120, 938), "• 100% 온디바이스 퀀트 대수 역산 엔진 (외부 금융 API 무전송 보안)", font=get_font(11, 'medium'), fill=(203, 213, 225))
    draw.text((120, 958), "• 반응형 모바일 뷰포트 시뮬레이터 & URL 딥링크 상태 복원 완벽 지원", font=get_font(11, 'medium'), fill=(56, 189, 248))
    
    # ---------------------------------------------------------
    # RIGHT: MASTER LAUNCHER + 4 STEPS + TIP + QR CODE (x=800 to 1820, w=1020)
    # Visual Hierarchy (Top-Down):
    # 1. PRIMARY HERO (TOP): Radiant Blue-Cyan Gradient Master Launcher with Ambient Glow
    # 2. Secondary: 4 Subdued Step Cards (dark glass, muted slate badges, ghost outline buttons)
    # 3. Tertiary: Subtle inline guide hint (quiet text between steps and QR)
    # 4. Supporting: Dark QR Code Plate & Hyperlink Area
    # ---------------------------------------------------------
    rx = 800
    rw = 1020
    base_proto_url = os.environ.get("GITHUB_PAGES_BASE_URL", "https://coyote-dev.github.io/average_down_calculator")
    proto_entry_url = f"{base_proto_url}/prototype.html"
    
    # ---------------------------------------------------------
    # 1. PRIMARY HERO (TOP): MASTER LAUNCHER with Iconic Blue Gradient
    # ---------------------------------------------------------
    my = 196
    mh = 120
    master_box = [rx, my, rx + rw, my + mh]
    
    # 1-A. Radiant Blue Ambient Glow Behind Card
    m_glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    m_glow_d = ImageDraw.Draw(m_glow)
    m_glow_d.rounded_rectangle([rx - 6, my - 2, rx + rw + 6, my + mh + 8], radius=24, fill=(0, 87, 255, 120))
    m_glow = m_glow.filter(ImageFilter.GaussianBlur(24))
    base = Image.alpha_composite(base, m_glow)
    
    # 1-B. Generate Vibrant 135-degree Blue-to-Cyan Linear Gradient Box
    t = np.linspace(0, 1, rw, endpoint=True, dtype=np.float32)
    r_arr = (0 * (1 - t) + 0 * t).astype(np.uint8)
    g_arr = (87 * (1 - t) + 195 * t).astype(np.uint8)
    b_arr = (255 * (1 - t) + 245 * t).astype(np.uint8)
    grad_arr = np.zeros((mh, rw, 4), dtype=np.uint8)
    grad_arr[:, :, 0] = r_arr
    grad_arr[:, :, 1] = g_arr
    grad_arr[:, :, 2] = b_arr
    grad_arr[:, :, 3] = 255
    grad_box = Image.fromarray(grad_arr, 'RGBA')
    
    grad_mask = Image.new('L', (rw, mh), 0)
    gmd = ImageDraw.Draw(grad_mask)
    gmd.rounded_rectangle([0, 0, rw - 1, mh - 1], radius=16, fill=255)
    
    base.paste(grad_box, (rx, my), grad_mask)
    draw = ImageDraw.Draw(base)
    
    # 1-C. Content Inside Radiant Gradient Card
    # High-contrast deep navy pill badge with white border and text
    badge_w = 145
    draw.rounded_rectangle([rx + 24, my + 16, rx + 24 + badge_w, my + 38], radius=11, fill=(0, 36, 110, 190), outline=(255, 255, 255, 180), width=1)
    draw.text((rx + 24 + badge_w // 2, my + 27), "MASTER LAUNCHER", font=get_font(9, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # Hero White Headline
    draw.text((rx + 24, my + 63), "모바일 목업 디바이스에서 전체 플로우 직접 실행하기 ↗", font=get_font(18.5, 'extrabold'), fill=(255, 255, 255), anchor='lm')
    # Hero Subtitle
    draw.text((rx + 24, my + 94), "0.2초 음성 도크부터 목표 역산 엔진까지, 4대 핵심 여정을 실물 뷰포트에서 한 번에 체험하세요.", font=get_font(12, 'medium'), fill=(225, 242, 255), anchor='lm')
    
    # Large High-Contrast Pure White CTA Button
    btn_w = 210
    btn_h = 52
    btn_rx = rx + rw - btn_w - 24
    btn_ry = my + (mh - btn_h) // 2
    
    # Button soft drop shadow
    sh_btn = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sh_btn_d = ImageDraw.Draw(sh_btn)
    sh_btn_d.rounded_rectangle([btn_rx - 2, btn_ry + 2, btn_rx + btn_w + 2, btn_ry + btn_h + 8], radius=26, fill=(0, 40, 120, 100))
    sh_btn = sh_btn.filter(ImageFilter.GaussianBlur(8))
    base = Image.alpha_composite(base, sh_btn)
    draw = ImageDraw.Draw(base)
    
    # Pure white button with electric blue text
    draw.rounded_rectangle([btn_rx, btn_ry, btn_rx + btn_w, btn_ry + btn_h], radius=26, fill=(255, 255, 255))
    draw.text((btn_rx + btn_w // 2, btn_ry + btn_h // 2), "RUN PROTOTYPE ↗", font=get_font(13.5, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    # ---------------------------------------------------------
    # 2. 4 SUBDUED STEP CARDS (Secondary Level)
    # ---------------------------------------------------------
    steps = [
        (
            "STEP 01", "01. 자산 현황 진단 대시보드",
            "보유 주식 수량 및 평균 매입가 입력 · 실시간 계좌 평가 손익 및 리스크 대시보드 진단",
            f"{proto_entry_url}?flow=home"
        ),
        (
            "STEP 02", "02. 0.2초 음성 도크 & 호가 프리셋 칩",
            "긴박한 하락장에서 말로 빠르게 입력하는 온디바이스 음성 바텀시트 모달 조작",
            f"{proto_entry_url}?flow=voice"
        ),
        (
            "STEP 03", "03. 목표 평단가 역산 엔진 (Closed-Form)",
            "탈출 희망 가격 입력 시 필요 수량과 소요 자금을 0.00% 오차로 즉시 역산 산출",
            f"{proto_entry_url}?flow=target"
        ),
        (
            "STEP 04", "04. 최종 플랜 확정 & 안전 계좌 진단",
            "예수금 65% 안전 마진 점검 및 리스크 진단 리포트 기반 최종 분할 매수 플랜 확정",
            f"{proto_entry_url}?flow=sim"
        )
    ]
    
    sy = 334
    sh_h = 86
    sgap = 10
    step_boxes = []
    
    for badge, title, desc, url in steps:
        box_rect = [rx, sy, rx + rw, sy + sh_h]
        step_boxes.append((box_rect, url))
        
        # Subdued Dark Glass Box (No bright stripes)
        draw.rounded_rectangle(box_rect, radius=12, fill=(15, 20, 32, 230), outline=(32, 42, 58), width=1)
        
        # Muted Dark Slate Badge (Uniform and quiet)
        draw_pill_badge(draw, left_x=rx + 18, cy=sy + 23, text=badge, font=get_font(9, 'bold'), theme='slate', dark_mode=True, has_dot=False, pad_x=8, height=20)
        draw.text((rx + 90, sy + 23), title, font=get_font(14, 'bold'), fill=(226, 232, 240), anchor='lm')
        draw.text((rx + 18, sy + 56), desc, font=get_font(11, 'regular'), fill=(105, 120, 140), anchor='lm')
        
        # Right Click Button - Subtle Ghost Outline Pill (Secondary)
        btn_x = rx + rw - 120
        draw_pill_badge(draw, cx=btn_x + 45, cy=sy + 43, text="바로가기 ↗", font=get_font(10.5, 'bold'), theme='slate', dark_mode=True, has_dot=False, pad_x=12, height=28)
        
        sy += sh_h + sgap
        
    # ---------------------------------------------------------
    # 3. TERTIARY: Subtle, Un-emphasized Guide Hint
    # ---------------------------------------------------------
    draw.text((rx + 4, 730), "TIP · 특정 단계만 개별 테스트하거나, 모바일 실물 기기에서는 아래 QR 코드를 카메라로 스캔하세요.", font=get_font(11.5, 'regular'), fill=(115, 130, 150), anchor='lm')
    
    # ---------------------------------------------------------
    # 4. SUPPORTING: Dark QR Code & Hyperlink Area (y=752 to 980, h=228)
    # ---------------------------------------------------------
    qy = 752
    qh = 228
    draw.rounded_rectangle([rx, qy, rx + rw, qy + qh], radius=14, fill=(14, 19, 30, 255), outline=(32, 42, 58), width=1)
    
    draw_pill_badge(draw, left_x=rx + 24, cy=qy + 30, text="HYPERLINK & MOBILE QR SCAN", font=get_font(9, 'bold'), theme='slate', has_dot=True, dark_mode=True, pad_x=8, height=20)
    draw.text((rx + 24, qy + 70), "• PDF 원클릭 하이퍼링크 : PDF 뷰어에서 각 카드나 버튼 클릭 시 반응형 프로토타입 즉시 실행", font=get_font(11.5, 'medium'), fill=(180, 195, 215))
    draw.text((rx + 24, qy + 100), "• 스마트폰 실물 QR 스캔 : 스마트폰 기본 카메라로 우측 QR 코드 스캔 시 모바일 전용 뷰 작동", font=get_font(11.5, 'medium'), fill=(180, 195, 215))
    draw.text((rx + 24, qy + 130), "• GitHub Pages 상시 배포 : 전 세계 어디서든 무설치로 60fps 플러터 엔진 즉각 체험 가능", font=get_font(11.5, 'medium'), fill=(56, 189, 248))
    draw.text((rx + 24, qy + 168), f"Live Web : {proto_entry_url}", font=get_num_font(11, 'bold'), fill=(130, 145, 170))
    
    # Generate High-Contrast QR Code on Crisp White Plate
    qr_url = proto_entry_url
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=4,
        border=1,
    )
    qr.add_data(qr_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=(11, 15, 23), back_color=(255, 255, 255)).convert('RGBA')
    qr_size = 144
    qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.NEAREST)
    
    qr_x = rx + rw - qr_size - 28
    qr_y = qy + 24
    
    draw.rounded_rectangle([qr_x - 8, qr_y - 6, qr_x + qr_size + 8, qr_y + qr_size + 24], radius=10, fill=(255, 255, 255))
    base.paste(qr_img, (qr_x, qr_y), qr_img)
    draw.text((qr_x + qr_size // 2, qr_y + qr_size + 8), "SCAN FOR MOBILE TEST", font=get_font(8.5, 'bold'), fill=(11, 15, 23), anchor='mm')
    
    draw_slide_footer(draw, 12, dark_mode=True)
    base.save(f'{OUT_DIR}/slide_12.png')
    print("SAVED slide_12.png (High-Hierarchy Live Interactive Prototype Hub with Blue Gradient Master Launcher at Top)")
    return {
        'step_boxes': step_boxes,
        'master_box': (master_box, proto_entry_url)
    }


if __name__ == '__main__':
    for i in range(1, 13):
        func_name = f'make_slide_{i:02d}'
        if func_name in globals():
            globals()[func_name]()
    print("ALL 12 SLIDES GENERATED WITH MASCULINE EDITORIAL AESTHETIC!")
