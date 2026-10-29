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

FLUTTER_MATERIAL_FONT = r"C:\flutter\bin\cache\artifacts\material_fonts\MaterialIcons-Regular.otf"

def get_material_icon_font(size):
    if os.path.exists(FLUTTER_MATERIAL_FONT):
        try:
            return ImageFont.truetype(FLUTTER_MATERIAL_FONT, int(round(size)))
        except:
            pass
    return get_font(size, 'bold')

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

def draw_dashed_line(draw, p1, p2, col=(0, 82, 255), width=2, dash_len=4, gap_len=3, dash=None, gap=None):
    if dash is not None:
        dash_len = dash
    if gap is not None:
        gap_len = gap
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

def draw_dashed_arrow(draw, p1, p2, col=(0, 82, 255), width=2, dash_len=4, gap_len=3, arrow_size=5, dash=None, gap=None):
    if dash is not None:
        dash_len = dash
    if gap is not None:
        gap_len = gap
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
    
    meta_txt = "Solo Production · Android App Live (v2.0) · UI/UX Design & Fullstack Engineering"
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
    
    # 4 Status Badges (Clean Pastel Theme - Reflecting v2.0 & Android Production)
    badges = [
        ("SOLO PO & FULLSTACK 100%", "blue"),
        ("GOOGLE PLAY (ANDROID) LIVE", "green"),
        ("v2.0 MAJOR UPDATE (2026.10)", "purple"),
        ("0.2s VOICE & CLOSED-FORM", "cyan")
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
    bar_y = 856
    bar_h = 108
    draw.rounded_rectangle([100, bar_y, 1820, bar_y + bar_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    col_w = (1720) // 4
    specs = [
        ("PROJECT ROLE", "PO & Solo Fullstack", "기획(PM) · UI/UX 디자인 · Flutter 풀스택 · v2.0 운영"),
        ("PERIOD & SPRINT", "2026.02 - 2026.10 (v2.0)", "v1.0 런칭(4월) ➔ v2.0 고도화 배포(10월, 운영 중)"),
        ("TECH STACK", "Flutter 3.x · Riverpod", "Dart · 온디바이스 STT · Python 퀀트 · Android Native"),
        ("PLATFORM RELEASE", "Google Play Live (Android)", "Android 단독 상용 정식 출시 (실서비스 운영) & Web 데모")
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
    card_h = 224
    gap = 40
    sy = 234
    
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
    t_y = 234
    t_w = 780
    t_h = 378
    draw.rounded_rectangle([t_x, t_y, t_x + t_w, t_y + t_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    draw.text((t_x + 24, t_y + 18), "TARGET SEGMENTATION MATRIX (타깃 세그먼트 분석)", font=get_font(14, 'bold'), fill=(15, 23, 42))
    draw.text((t_x + 24, t_y + 38), "매매 빈도와 퀀트 도구 수용도에 따른 4대 투자자 유형 분류", font=get_font(11.5, 'medium'), fill=(100, 116, 139))
    
    # 2x2 Quadrant Grid - Centered Horizontally & Vertically within card
    grid_w = 540
    grid_h = 260
    grid_x = t_x + (t_w - grid_w) // 2 # 220
    grid_y = t_y + 76 # 310
    qw = (grid_w - 16) // 2 # 262
    qh = (grid_h - 16) // 2 # 122
    
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
    c_y = 234
    c_w = 810
    c_h = 378
    draw.rounded_rectangle([c_x, c_y, c_x + c_w, c_y + c_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    draw.text((c_x + 24, c_y + 18), "COMPETITIVE BENCHMARK (경쟁사 비교 분석)", font=get_font(14, 'bold'), fill=(15, 23, 42))
    draw.text((c_x + 24, c_y + 38), "국내 주요 솔루션 대비 스마트 DCA 계산기의 5대 핵심 차별점", font=get_font(11.5, 'medium'), fill=(100, 116, 139))
    
    # Table layout dimensions
    tbl_x = c_x + 20
    tbl_w = c_w - 40
    th_y = c_y + 64
    th_h = 36
    th_cy = th_y + th_h // 2
    
    x1 = tbl_x + 16
    x2 = tbl_x + 155
    x3 = tbl_x + 335
    col4_x = tbl_x + 520
    col4_w = tbl_w - 520
    
    # Table Header Row background
    draw.rounded_rectangle([tbl_x, th_y, tbl_x + tbl_w, th_y + th_h], radius=8, fill=(241, 245, 249))
    
    # SMART DCA Column 4 Highlight Card (Runs behind header & all data rows)
    draw.rounded_rectangle([col4_x, th_y - 2, col4_x + col4_w, th_y + th_h + 5 * 46 + 4], radius=10, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    
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
    
    row_h = 46
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
    p_y = 632
    pw = 800
    ph = 338
    
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
    
    # Unified Header - Simplified title
    draw_slide_header(
        draw, 
        slide_num=4, 
        category_en="INFORMATION ARCHITECTURE | SERVICE STRUCTURE", 
        title_black="핵심 기능을 직관적으로 연결한 ", 
        title_blue="5대 정보 구조(IA)", 
        subtitle_kr="포트폴리오 진단부터 퀀트 역산, 리스크 감사까지 한눈에 파악하는 서비스 계층 구조"
    )
    
    # Top-Right Legend: Compact IA Notation (w=540, h=78)
    leg_x = 1280
    leg_y = 65
    leg_w = 540
    leg_h = 78
    draw.rounded_rectangle([leg_x, leg_y, leg_x + leg_w, leg_y + leg_h], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=leg_x + 16, cy=leg_y + 20, text="IA NOTATION", font=get_font(8, 'bold'), theme='blue', has_dot=True, pad_x=6, height=18)
    draw.text((leg_x + 120, leg_y + 20), "화면 및 컴포넌트 표기 범례", font=get_font(11, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    # 4 clean legend items with generous margins
    draw.rounded_rectangle([leg_x + 16, leg_y + 44, leg_x + 66, leg_y + 68], radius=4, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
    draw.text((leg_x + 41, leg_y + 56), "Page", font=get_font(8.5, 'bold'), fill=(71, 85, 105), anchor='mm')
    draw.text((leg_x + 74, leg_y + 56), "기본 화면", font=get_font(9.5, 'medium'), fill=(100, 116, 139), anchor='lm')
    
    draw.rounded_rectangle([leg_x + 146, leg_y + 44, leg_x + 224, leg_y + 68], radius=4, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((leg_x + 185, leg_y + 56), "BottomSheet", font=get_font(8, 'bold'), fill=(0, 82, 255), anchor='mm')
    draw.text((leg_x + 232, leg_y + 56), "액션 시트", font=get_font(9.5, 'medium'), fill=(100, 116, 139), anchor='lm')
    
    draw.rounded_rectangle([leg_x + 300, leg_y + 44, leg_x + 350, leg_y + 68], radius=4, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
    draw.text((leg_x + 325, leg_y + 56), "Modal", font=get_font(8.5, 'bold'), fill=(71, 85, 105), anchor='mm')
    draw.text((leg_x + 358, leg_y + 56), "팝업/모달", font=get_font(9.5, 'medium'), fill=(100, 116, 139), anchor='lm')
    
    draw_pill_badge(draw, left_x=leg_x + 430, cy=leg_y + 56, text="NEW", font=get_font(8, 'bold'), theme='blue', pad_x=5, height=18)
    draw.text((leg_x + 470, leg_y + 56), "혁신 기능", font=get_font(9.5, 'bold'), fill=(0, 82, 255), anchor='lm')
    
    # -----------------------------------------------------------------
    # BODY GROUP: Generous 52px Clearance from Subtitle (y = 234)
    # -----------------------------------------------------------------
    # LEVEL 0: ROOT NODE (Service Master Hub) - Spacious & Clean
    root_x1, root_y1, root_x2, root_y2 = 640, 234, 1280, 286
    draw.rounded_rectangle([root_x1, root_y1, root_x2, root_y2], radius=12, fill=(255, 255, 255), outline=(0, 82, 255), width=2)
    draw_pill_badge(draw, cx=root_x1 + 72, cy=root_y1 + 26, text="MASTER HUB", font=get_font(9, 'bold'), theme='blue', pad_x=8, height=24)
    draw.text((root_x1 + 142, root_y1 + 16), "SMART DCA SERVICE MASTER HUB (L0)", font=get_font(13.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((root_x1 + 142, root_y1 + 37), "모바일 한 손 조작 최적화 및 0ms 온디바이스 퀀트 엔진 통합 제어", font=get_font(10.5, 'medium'), fill=(71, 85, 105), anchor='lm')
    
    # Connectors from Root Node to Level 1
    cw = 328
    cgap = 20
    cols_x = [100 + i * (cw + cgap) for i in range(5)]
    col_centers = [cx + cw // 2 for cx in cols_x] # [264, 612, 960, 1308, 1656]
    
    # Connector lines
    draw.line([(960, root_y2), (960, 308)], fill=(0, 82, 255), width=2)
    draw.ellipse([956, 304, 964, 312], fill=(0, 82, 255))
    draw.line([(col_centers[0], 308), (col_centers[-1], 308)], fill=(0, 82, 255, 180), width=2)
    for cx in col_centers:
        draw.ellipse([cx - 4, 308 - 4, cx + 4, 308 + 4], fill=(0, 82, 255))
        draw_arrow(draw, (cx, 308), (cx, 330), col=(0, 82, 255), width=2, arrow_size=4)
        
    # Domains Data (3 High-Impact Cards per Domain, concise text)
    domains_data = [
        ("1.0 DASHBOARD", "포트폴리오 대시보드", "자산 현황 및 손실 포지션 1초 조망", [
            ("SCR-DASH-01", "Page", "자산 종합 진단 요약", "총 투자금 · 평가손익 · 실시간 환율 조망", False),
            ("SCR-DASH-02", "Page", "보유 포지션 카드 뷰", "종목별 평단가 · 손실 상단 스마트 정렬", False),
            ("SCR-VOICE-01", "BottomSheet", "AI 음성 도크 & 호가칩", "0.2초 음성 인식 및 원터치 호가 주입", True)
        ]),
        ("2.0 DCA SIMULATOR", "물타기 계산기", "차수별 분할 매수 및 평단 시뮬레이션", [
            ("SCR-CALC-01", "Page", "다회차 분할 매수 설계", "1차~N차 단계별 매수가 및 수량 입력", False),
            ("SCR-CALC-02", "Widget", "실시간 평단 피드백", "수량 조절에 따른 신규 평단 60fps 연산", False),
            ("SCR-CALC-03", "Page", "전략 비교 매트릭스", "일괄 매수 vs 분할 매수 2종 시나리오 대조", True)
        ]),
        ("3.0 GOAL-SEEKING", "목표 평단가 역산기", "희망 탈출 평단 도달 필요수량 0ms 산출", [
            ("SCR-INVT-01", "Page", "손익분기 목표가 역산", "단일 대수 폐쇄형 공식 0ms 즉시 산출", True),
            ("SCR-INVT-02", "Modal", "수학적 유효성 가드", "비현실적 목표 차단 및 대안 평단 가이드", True),
            ("SCR-INVT-03", "Widget", "예수금 제약 인터랙션", "가용 현금 한도 내 최적 도달 평단 탐색", True)
        ]),
        ("4.0 RISK AUDIT", "계좌 리스크 진단실", "단일 종목 과밀 및 급락 스트레스 테스트", [
            ("SCR-RISK-01", "Page", "포트폴리오 비중 분석", "추가 매수 후 계좌 쏠림도 및 비중 시각화", True),
            ("SCR-RISK-02", "Widget", "65% 예수금 안전선 가드", "단일 종목 과밀 시 뇌동매매 방어 경보", True),
            ("SCR-RISK-03", "Widget", "하락 스트레스 테스트", "시장 -10%~-30% 급락 시 계좌 충격도 점검", True)
        ]),
        ("5.0 SETTINGS", "맞춤 환경설정", "글로벌 통화 · 세션 · 온디바이스 보안", [
            ("SCR-SETT-01", "Page", "글로벌 통화 & 환율", "KRW, USD, JPY, EUR 및 10개국어 다국어", False),
            ("SCR-SETT-02", "BottomSheet", "24시간 안심 세션", "보상형 광고 1회 시청 시 24h 광고 차단", True),
            ("SCR-SETT-03", "Page", "온디바이스 프라이버시", "외부 통신 0건, 로컬 SQLite 암호화 보관", True)
        ])
    ]
    
    # Render 5 Columns (Level 1 + 3 Level 2 cards) with generous inner padding (18px)
    for i, (dom_code, dom_name, dom_desc, containers) in enumerate(domains_data):
        cx = cols_x[i]
        
        # Level 1 Domain Header Card (y=330 to 402, h=72, generous bottom margin)
        draw.rounded_rectangle([cx, 330, cx + cw, 402], radius=10, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
        draw.text((cx + 18, 344), dom_code, font=get_font(9.5, 'bold'), fill=(0, 82, 255))
        draw.text((cx + 18, 363), dom_name, font=get_font(13, 'bold'), fill=(15, 23, 42))
        draw.text((cx + 18, 382), dom_desc, font=get_font(8.5, 'medium'), fill=(100, 116, 139))
        
        # Vertical Tree Line
        tree_x = cx + 16
        draw.line([(tree_x, 402), (tree_x, 670)], fill=(0, 82, 255, 100), width=2)
        
        # 3 L2 Cards with generous inner padding (card_h = 82, gap = 10)
        card_w = cw - 32
        card_x = cx + 32
        cy = 414
        card_h = 82
        gap = 10
        
        for scr_id, view_type, title, desc, is_new in containers:
            # Tree branch line
            draw.line([(tree_x, cy + 20), (card_x, cy + 20)], fill=(0, 82, 255, 120), width=2)
            draw.ellipse([tree_x - 3, cy + 20 - 3, tree_x + 3, cy + 20 + 3], fill=(0, 82, 255))
            
            card_bg = (255, 255, 255) if not is_new else (250, 252, 255)
            card_bd = (226, 232, 240) if not is_new else (191, 219, 254)
            draw.rounded_rectangle([card_x, cy, card_x + card_w, cy + card_h], radius=8, fill=card_bg, outline=card_bd, width=1)
            
            # Generous Inner Margins: left=18, right=18, top=12, bottom=16
            # Row 1: SCR ID & Type tag + NEW badge
            draw.text((card_x + 18, cy + 14), f"{scr_id}  ·  [{view_type}]", font=get_font(8.5, 'bold'), fill=(100, 116, 139), anchor='lm')
            if is_new:
                draw_pill_badge(draw, cx=card_x + card_w - 24, cy=cy + 14, text="NEW", font=get_font(7.5, 'bold'), theme='blue', has_dot=False, pad_x=5, height=16)
                
            # Row 2: Title with breathing room
            draw.text((card_x + 18, cy + 38), title, font=get_font(11.5, 'bold'), fill=(15, 23, 42), anchor='lm')
            
            # Row 3: Description (Clean, concise, 15px bottom margin)
            draw.text((card_x + 18, cy + 61), desc, font=get_font(9.5, 'medium'), fill=(71, 85, 105), anchor='lm')
            
            cy += card_h + gap
            
    # Clean Bottom Architecture Highlights Strip (y=702 to 828, h=126)
    bar_x = 100
    bar_y = 702
    bar_w = 1720
    bar_h = 126
    draw.rounded_rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], radius=12, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    
    draw_pill_badge(draw, left_x=bar_x + 24, cy=bar_y + 24, text="CORE ARCHITECTURE", font=get_font(8.5, 'bold'), theme='blue', has_dot=True, pad_x=8, height=20)
    draw.text((bar_x + 185, bar_y + 24), "엔터프라이즈 정보 구조 설계 4대 원칙", font=get_font(12, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((bar_x + 480, bar_y + 24), "복잡한 금융 연산을 0-Tap 직관적 UI로 단순화한 모바일 최적화 계층 구조", font=get_font(9.5, 'regular'), fill=(100, 116, 139), anchor='lm')
    
    pillars = [
        ("01. 독립 도메인 라우팅", "5대 핵심 기능을 GNB 레벨에서 완전히 분리하여 탐색 비용을 최소화합니다.", "blue"),
        ("02. Thumb-Zone 최적화", "모든 입력 및 주문 제어 컴포넌트를 한 손 엄지 조작 영역(하단 48dp)에 집중 배치합니다.", "cyan"),
        ("03. 0ms 폐쇄형 역산 연동", "단일 대수 수식 엔진을 통해 반복 시뮬레이션 없이 목표 필요 수량을 즉각 도출합니다.", "blue"),
        ("04. 100% 로컬 보안 무결성", "외부 통신 0건, 개인 금융 자산 데이터를 온디바이스 SQLite로 완벽히 암호화합니다.", "green")
    ]
    pw = (bar_w - 48 - 36) // 4
    py = bar_y + 48
    for pidx, (ptitle, pdesc, pcol) in enumerate(pillars):
        px = bar_x + 24 + pidx * (pw + 12)
        draw.rounded_rectangle([px, py, px + pw, py + 62], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        # Inner padding inside pillar cards: 16px left, 15px top, 15px bottom breathing room
        draw.text((px + 16, py + 16), ptitle, font=get_font(10, 'bold'), fill=(0, 82, 255) if pcol == 'blue' else (15, 23, 42))
        draw.text((px + 16, py + 36), pdesc, font=get_font(8.5, 'medium'), fill=(71, 85, 105))
        
    draw_slide_footer(draw, 4)
    base.save(f'{OUT_DIR}/slide_04.png')
    print("SAVED perfect Slide 04 successfully!")

def make_slide_05():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Unified Header - Simplified title
    draw_slide_header(
        draw, 
        slide_num=5, 
        category_en="USER FLOW | SERVICE INTERACTION FLOWCHART", 
        title_black="사용자 행동과 판단을 이끄는 ", 
        title_blue="5단계 서비스 UX 플로우차트", 
        subtitle_kr="진입 온보딩부터 멀티모달 입력, 퀀트 역산, 리스크 가드, 포트폴리오 저장까지 이어지는 핵심 사용자 여정"
    )
    
    # Top-Right Legend: Compact Diagram Notation (w=540, h=78)
    leg_x = 1280
    leg_y = 65
    leg_w = 540
    leg_h = 78
    draw.rounded_rectangle([leg_x, leg_y, leg_x + leg_w, leg_y + leg_h], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=leg_x + 16, cy=leg_y + 20, text="NOTATION", font=get_font(8, 'bold'), theme='blue', has_dot=True, pad_x=6, height=18)
    draw.text((leg_x + 105, leg_y + 20), "플로우차트 기호 범례", font=get_font(11, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    # 4 compact legend items with comfortable margins
    draw.rounded_rectangle([leg_x + 16, leg_y + 44, leg_x + 70, leg_y + 68], radius=10, fill=(0, 82, 255))
    draw.text((leg_x + 43, leg_y + 56), "Start/End", font=get_font(7, 'bold'), fill=(255, 255, 255), anchor='mm')
    draw.text((leg_x + 76, leg_y + 56), "시작/종료", font=get_font(9.5, 'medium'), fill=(71, 85, 105), anchor='lm')
    
    draw.rounded_rectangle([leg_x + 142, leg_y + 44, leg_x + 192, leg_y + 68], radius=4, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw.text((leg_x + 167, leg_y + 56), "Screen", font=get_font(7.5, 'bold'), fill=(15, 23, 42), anchor='mm')
    draw.text((leg_x + 198, leg_y + 56), "화면/접점", font=get_font(9.5, 'medium'), fill=(71, 85, 105), anchor='lm')
    
    draw.rounded_rectangle([leg_x + 268, leg_y + 44, leg_x + 318, leg_y + 68], radius=4, fill=(240, 246, 255), outline=(0, 82, 255), width=1)
    draw.text((leg_x + 293, leg_y + 56), "Action", font=get_font(7.5, 'bold'), fill=(0, 82, 255), anchor='mm')
    draw.text((leg_x + 325, leg_y + 56), "사용자 행동", font=get_font(9.5, 'medium'), fill=(71, 85, 105), anchor='lm')
    
    draw_diamond(draw, cx=leg_x + 410, cy=leg_y + 56, w=34, h=22, fill=(254, 243, 199), outline=(217, 119, 6), width=1)
    draw.text((leg_x + 410, leg_y + 56), "Decide", font=get_font(6.5, 'bold'), fill=(180, 83, 9), anchor='mm')
    draw.text((leg_x + 434, leg_y + 56), "판단 분기", font=get_font(9.5, 'medium'), fill=(71, 85, 105), anchor='lm')
    
    # -----------------------------------------------------------------
    # BODY GROUP: Generous 52px Clearance from Subtitle (y = 234)
    # -----------------------------------------------------------------
    # 5 STAGE COLUMNS
    cw = 328
    cgap = 20
    cols_x = [100 + i * (cw + cgap) for i in range(5)]
    col_centers = [cx + cw // 2 for cx in cols_x]  # [264, 612, 960, 1308, 1656]
    
    stages_info = [
        ("STAGE 01", "진입 & 온보딩", "Launch & Onboarding"),
        ("STAGE 02", "멀티모달 입력", "Multi-Modal Input"),
        ("STAGE 03", "퀀트 목표 역산", "Goal Inversion"),
        ("STAGE 04", "리스크 안전 가드", "Risk Guardrail"),
        ("STAGE 05", "플랜 확정 & 저장", "Plan Finalize & Save")
    ]
    
    # Stage Headers (y=234 to 284, h=50) - Generous 52px whitespace below subtitle!
    for i, (st_code, st_name, st_en) in enumerate(stages_info):
        cx = cols_x[i]
        # Inner padding: 16px left, 12px top
        draw.rounded_rectangle([cx, 234, cx + cw, 284], radius=8, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
        draw_pill_badge(draw, left_x=cx + 16, cy=249, text=st_code, font=get_font(7.5, 'bold'), theme='blue', pad_x=5, height=16)
        draw.text((cx + 86, 249), st_name, font=get_font(11, 'bold'), fill=(15, 23, 42), anchor='lm')
        draw.text((cx + 16, 269), st_en, font=get_font(8.5, 'medium'), fill=(100, 116, 139), anchor='lm')
        
        # Inter-stage advance arrow with comfortable margin
        if i < 4:
            arrow_start_x = cx + cw
            arrow_end_x = cols_x[i + 1]
            draw_arrow(draw, (arrow_start_x + 2, 259), (arrow_end_x - 2, 259), col=(0, 82, 255), width=2, arrow_size=4)
            
    # Node width: 260px (Margin inside 328px column is 34px left and 34px right)
    nw = 260
    
    # =============================================================
    # DIAGRAM TRACK 1: STAGE 01 (Center: 264)
    # =============================================================
    c0 = col_centers[0]
    
    # 1. Start Capsule (y=300 to 328, h=28)
    draw.rounded_rectangle([c0 - 75, 300, c0 + 75, 328], radius=14, fill=(0, 82, 255))
    draw.text((c0, 314), "Start : 앱 실행", font=get_font(9.5, 'bold'), fill=(255, 255, 255), anchor='mm')
    draw_arrow(draw, (c0, 328), (c0, 344), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 2. Screen: 스플래시 & 홈 화면 (y=344 to 388, h=44)
    # Inner padding: 14px left, 10px top
    draw.rounded_rectangle([c0 - nw // 2, 344, c0 + nw // 2, 388], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw_pill_badge(draw, left_x=c0 - 114, cy=358, text="SCREEN", font=get_font(6.5, 'bold'), theme='slate', pad_x=4, height=14)
    draw.text((c0 - 54, 358), "스플래시 & 로컬 환경 동기화", font=get_font(9, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((c0, 375), "SQLite 로컬 DB 로드 및 환경설정 바인딩", font=get_font(8, 'medium'), fill=(100, 116, 139), anchor='mm')
    draw_arrow(draw, (c0, 388), (c0, 406), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 3. Decision Diamond: 최초 실행 여부? (cy=432, w=176, h=52)
    draw_diamond(draw, cx=c0, cy=432, w=176, h=52, fill=(254, 243, 199), outline=(217, 119, 6), width=2)
    draw.text((c0, 432), "최초 실행 여부?", font=get_font(9.5, 'bold'), fill=(180, 83, 9), anchor='mm')
    
    # Branch Yes (Right -> Onboarding loop)
    draw_dashed_line(draw, (c0 + 88, 432), (cols_x[0] + cw - 16, 432), col=(244, 63, 94), width=1)
    draw.text(((c0 + 88 + cols_x[0] + cw - 16) // 2, 422), "Yes (신규)", font=get_font(7.5, 'bold'), fill=(220, 38, 38), anchor='mm')
    draw_dashed_arrow(draw, (cols_x[0] + cw - 16, 432), (cols_x[0] + cw - 16, 464), col=(244, 63, 94), width=1, arrow_size=3)
    draw.rounded_rectangle([cols_x[0] + cw - 88, 464, cols_x[0] + cw - 6, 496], radius=5, fill=(254, 242, 242), outline=(244, 63, 94), width=1)
    draw.text((cols_x[0] + cw - 47, 475), "온보딩 4단계", font=get_font(7.5, 'bold'), fill=(153, 27, 27), anchor='mm')
    draw.text((cols_x[0] + cw - 47, 486), "핵심 인터랙션", font=get_font(7, 'medium'), fill=(153, 27, 27), anchor='mm')
    draw_dashed_line(draw, (cols_x[0] + cw - 47, 496), (cols_x[0] + cw - 47, 524), col=(244, 63, 94), width=1)
    draw_dashed_arrow(draw, (cols_x[0] + cw - 47, 524), (c0 + nw // 2, 524), col=(244, 63, 94), width=1, arrow_size=3)
    
    # Branch No (Straight down -> Home Dashboard)
    draw_arrow(draw, (c0, 458), (c0, 502), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text((c0 - 30, 480), "No (기존)", font=get_font(8, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    # 4. Screen: 홈 대시보드 화면 로드 (y=502 to 546, h=44)
    draw.rounded_rectangle([c0 - nw // 2, 502, c0 + nw // 2, 546], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw_pill_badge(draw, left_x=c0 - 114, cy=516, text="SCREEN", font=get_font(6.5, 'bold'), theme='slate', pad_x=4, height=14)
    draw.text((c0 - 54, 516), "홈 대시보드 화면 로드", font=get_font(9, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((c0, 533), "총 자산 · 계좌 손익률 · 보유 종목 1초 조망", font=get_font(8, 'medium'), fill=(100, 116, 139), anchor='mm')
    draw_arrow(draw, (c0, 546), (c0, 564), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 5. Action: 손실 종목 카드 원터치 탭 (y=564 to 608, h=44)
    draw.rounded_rectangle([c0 - nw // 2, 564, c0 + nw // 2, 608], radius=6, fill=(240, 246, 255), outline=(0, 82, 255), width=1)
    draw_pill_badge(draw, left_x=c0 - 114, cy=578, text="ACTION", font=get_font(6.5, 'bold'), theme='blue', pad_x=4, height=14)
    draw.text((c0 - 54, 578), "손실 종목 카드 원터치 탭", font=get_font(9, 'bold'), fill=(0, 82, 255), anchor='lm')
    draw.text((c0, 595), "물타기 계산/역산 모드 진입 (P0·Q0 자동 주입)", font=get_font(8, 'medium'), fill=(71, 85, 105), anchor='mm')
    draw_arrow(draw, (c0, 608), (c0, 626), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 6. Feedback: 파라미터 번들 0ms 연동 (y=626 to 672, h=46)
    draw.rounded_rectangle([c0 - nw // 2, 626, c0 + nw // 2, 672], radius=6, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw_pill_badge(draw, left_x=c0 - 114, cy=640, text="FEEDBACK", font=get_font(6.5, 'bold'), theme='green', pad_x=4, height=14)
    draw.text((c0 - 44, 640), "파라미터 번들 0ms 연동 완료", font=get_font(9, 'bold'), fill=(22, 101, 52), anchor='lm')
    draw.text((c0, 656), "현재 평단가 P0 · 수량 Q0 무손실 인계", font=get_font(7.5, 'medium'), fill=(21, 128, 61), anchor='mm')
    
    # Inter-Stage Handover Arrow to Stage 02
    draw_arrow(draw, (cols_x[0] + cw, 647), (cols_x[1], 647), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text(((cols_x[0] + cw + cols_x[1]) // 2, 635), "연동 →", font=get_font(8, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    # =============================================================
    # DIAGRAM TRACK 2: STAGE 02 (Center: 612)
    # =============================================================
    c1 = col_centers[1]
    
    # 1. Screen: 바텀시트 전개 (y=300 to 344, h=44)
    draw.rounded_rectangle([c1 - nw // 2, 300, c1 + nw // 2, 344], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw_pill_badge(draw, left_x=c1 - 114, cy=314, text="SCREEN", font=get_font(6.5, 'bold'), theme='slate', pad_x=4, height=14)
    draw.text((c1 - 54, 314), "0.2초 스마트 입력 시트 전개", font=get_font(9, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((c1, 331), "엄지 조작 영역(Thumb Zone) 최적화 바텀시트", font=get_font(8, 'medium'), fill=(100, 116, 139), anchor='mm')
    draw_arrow(draw, (c1, 344), (c1, 360), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 2. Decision Container: 3대 멀티모달 입력 채널 (y=360 to 464, h=104)
    draw.rounded_rectangle([c1 - nw // 2, 360, c1 + nw // 2, 464], radius=6, fill=(250, 252, 255), outline=(191, 219, 254), width=1)
    draw_pill_badge(draw, left_x=c1 - 114, cy=374, text="DECISION", font=get_font(6.5, 'bold'), theme='amber', pad_x=4, height=14)
    draw.text((c1 - 48, 374), "3대 멀티모달 입력 채널 선택", font=get_font(8.5, 'bold'), fill=(180, 83, 9), anchor='lm')
    
    # Channel rows with generous inner margins
    draw.rounded_rectangle([c1 - 114, 387, c1 + 114, 408], radius=4, fill=(255, 255, 255), outline=(191, 219, 254), width=1)
    draw_pill_badge(draw, left_x=c1 - 110, cy=397, text="음성", font=get_font(6.5, 'bold'), theme='blue', pad_x=3, height=12)
    draw.text((c1 - 72, 397), "AI 음성 STT '15,000원에 100주' 발화", font=get_font(7.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    draw.rounded_rectangle([c1 - 114, 411, c1 + 114, 432], radius=4, fill=(255, 255, 255), outline=(191, 219, 254), width=1)
    draw_pill_badge(draw, left_x=c1 - 110, cy=421, text="호가칩", font=get_font(6.5, 'bold'), theme='cyan', pad_x=3, height=12)
    draw.text((c1 - 68, 421), "원터치 호가 프리셋(±5%, ±10%) 주입", font=get_font(7.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    
    draw.rounded_rectangle([c1 - 114, 435, c1 + 114, 456], radius=4, fill=(255, 255, 255), outline=(191, 219, 254), width=1)
    draw_pill_badge(draw, left_x=c1 - 110, cy=445, text="키패드", font=get_font(6.5, 'bold'), theme='slate', pad_x=3, height=12)
    draw.text((c1 - 68, 445), "정밀 텐키패드 목표 평단가 직접 입력", font=get_font(7.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw_arrow(draw, (c1, 464), (c1, 478), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 3. Action: 파라미터 주입 (y=478 to 522, h=44)
    draw.rounded_rectangle([c1 - nw // 2, 478, c1 + nw // 2, 522], radius=6, fill=(240, 246, 255), outline=(0, 82, 255), width=1)
    draw_pill_badge(draw, left_x=c1 - 114, cy=492, text="ACTION", font=get_font(6.5, 'bold'), theme='blue', pad_x=4, height=14)
    draw.text((c1 - 54, 492), "추가 매수가 & 목표단가 주입", font=get_font(9, 'bold'), fill=(0, 82, 255), anchor='lm')
    draw.text((c1, 509), "1-Tap 또는 발화 종료 즉시 입력 번들 완성", font=get_font(7.5, 'medium'), fill=(71, 85, 105), anchor='mm')
    draw_arrow(draw, (c1, 522), (c1, 540), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 4. Diamond Decision: 입력값 유효성 검증? (cy=566, w=196, h=52)
    draw_diamond(draw, cx=c1, cy=566, w=196, h=52, fill=(254, 243, 199), outline=(217, 119, 6), width=2)
    draw.text((c1, 560), "입력값 유효성 검증?", font=get_font(9, 'bold'), fill=(180, 83, 9), anchor='mm')
    draw.text((c1, 574), "결측치 & 음수 방어", font=get_font(7, 'medium'), fill=(146, 64, 14), anchor='mm')
    
    # Branch No (Left loop)
    draw_dashed_line(draw, (c1 - 98, 566), (cols_x[1] + 16, 566), col=(244, 63, 94), width=1)
    draw_dashed_arrow(draw, (cols_x[1] + 16, 566), (cols_x[1] + 16, 524), col=(244, 63, 94), width=1, arrow_size=3)
    draw.rounded_rectangle([cols_x[1] + 4, 496, cols_x[1] + 80, 524], radius=5, fill=(254, 242, 242), outline=(244, 63, 94), width=1)
    draw.text((cols_x[1] + 42, 510), "햅틱 진동 피드백", font=get_font(7, 'bold'), fill=(153, 27, 27), anchor='mm')
    draw_dashed_line(draw, (cols_x[1] + 42, 496), (cols_x[1] + 42, 482), col=(244, 63, 94), width=1)
    draw_dashed_arrow(draw, (cols_x[1] + 42, 482), (c1 - nw // 2, 482), col=(244, 63, 94), width=1, arrow_size=3)
    
    # Branch Yes (Down)
    draw_arrow(draw, (c1, 592), (c1, 626), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text((c1 + 32, 609), "Yes (정상)", font=get_font(7.5, 'bold'), fill=(5, 150, 105), anchor='mm')
    
    # 5. Feedback: 데이터 정규화 완료 (y=626 to 672, h=46)
    draw.rounded_rectangle([c1 - nw // 2, 626, c1 + nw // 2, 672], radius=6, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw_pill_badge(draw, left_x=c1 - 114, cy=640, text="FEEDBACK", font=get_font(6.5, 'bold'), theme='green', pad_x=4, height=14)
    draw.text((c1 - 44, 640), "실시간 데이터 정규화 완료", font=get_font(9, 'bold'), fill=(22, 101, 52), anchor='lm')
    draw.text((c1, 656), "호가 단위 자동 변환 및 엔진 즉시 전송", font=get_font(7.5, 'medium'), fill=(21, 128, 61), anchor='mm')
    
    # Inter-Stage Handover Arrow to Stage 03
    draw_arrow(draw, (cols_x[1] + cw, 647), (cols_x[2], 647), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text(((cols_x[1] + cw + cols_x[2]) // 2, 635), "연산 →", font=get_font(8, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    # =============================================================
    # DIAGRAM TRACK 3: STAGE 03 (Center: 960)
    # =============================================================
    c2 = col_centers[2]
    
    # 1. Quant Engine Process (y=300 to 344, h=44)
    draw.rounded_rectangle([c2 - nw // 2, 300, c2 + nw // 2, 344], radius=6, fill=(239, 246, 255), outline=(0, 82, 255), width=2)
    draw_pill_badge(draw, left_x=c2 - 114, cy=314, text="QUANT", font=get_font(6.5, 'bold'), theme='blue', pad_x=4, height=14)
    draw.text((c2 - 54, 314), "폐쇄형 퀀트 역산 가동 (0ms)", font=get_font(9, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((c2, 331), "단일 수식 대수 전개로 필요 수량 0ms 즉시 산출", font=get_font(8, 'medium'), fill=(0, 82, 255), anchor='mm')
    draw_arrow(draw, (c2, 344), (c2, 362), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 2. Diamond Decision: 목표가 실현 가능 범위? (cy=390, w=216, h=56)
    draw_diamond(draw, cx=c2, cy=390, w=216, h=56, fill=(254, 243, 199), outline=(217, 119, 6), width=2)
    draw.text((c2, 384), "목표가 실현 가능 범위?", font=get_font(9, 'bold'), fill=(180, 83, 9), anchor='mm')
    draw.text((c2, 397), "추가매수가 < 목표가 < 현재평단", font=get_font(7, 'medium'), fill=(146, 64, 14), anchor='mm')
    
    # Branch No (Left loop)
    draw_dashed_line(draw, (c2 - 108, 390), (cols_x[2] + 16, 390), col=(244, 63, 94), width=1)
    draw_dashed_arrow(draw, (cols_x[2] + 16, 390), (cols_x[2] + 16, 416), col=(244, 63, 94), width=1, arrow_size=3)
    draw.rounded_rectangle([cols_x[2] + 4, 416, cols_x[2] + 80, 452], radius=5, fill=(254, 242, 242), outline=(244, 63, 94), width=1)
    draw.text((cols_x[2] + 42, 428), "비정상 목표 경고", font=get_font(7, 'bold'), fill=(153, 27, 27), anchor='mm')
    draw.text((cols_x[2] + 42, 440), "대안 평단 자동 제안", font=get_font(6.5, 'medium'), fill=(153, 27, 27), anchor='mm')
    draw_dashed_line(draw, (cols_x[2] + 42, 452), (cols_x[2] + 42, 474), col=(244, 63, 94), width=1)
    draw_dashed_arrow(draw, (cols_x[2] + 42, 474), (cols_x[1] + cw - 10, 474), col=(244, 63, 94), width=1, arrow_size=3)
    draw.text(((cols_x[2] + 42 + cols_x[1] + cw) // 2, 464), "재설정", font=get_font(7, 'bold'), fill=(220, 38, 38), anchor='mm')
    
    # Branch Yes (Down)
    draw_arrow(draw, (c2, 418), (c2, 454), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text((c2 + 30, 436), "Yes (통과)", font=get_font(7.5, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    # 3. Screen: 역산 결과 시뮬레이션 (y=454 to 498, h=44)
    draw.rounded_rectangle([c2 - nw // 2, 454, c2 + nw // 2, 498], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw_pill_badge(draw, left_x=c2 - 114, cy=468, text="SCREEN", font=get_font(6.5, 'bold'), theme='slate', pad_x=4, height=14)
    draw.text((c2 - 54, 468), "목표 역산 시뮬레이터 뷰", font=get_font(9, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((c2, 485), "필요 매수 수량 & 소요 자금 오차 0.00% 산출", font=get_font(7.5, 'medium'), fill=(100, 116, 139), anchor='mm')
    draw_arrow(draw, (c2, 498), (c2, 518), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 4. Action: 차수별 분할 조절 (y=518 to 562, h=44)
    draw.rounded_rectangle([c2 - nw // 2, 518, c2 + nw // 2, 562], radius=6, fill=(240, 246, 255), outline=(0, 82, 255), width=1)
    draw_pill_badge(draw, left_x=c2 - 114, cy=532, text="ACTION", font=get_font(6.5, 'bold'), theme='blue', pad_x=4, height=14)
    draw.text((c2 - 54, 532), "차수별 분할 매수 비중 조절", font=get_font(9, 'bold'), fill=(0, 82, 255), anchor='lm')
    draw.text((c2, 549), "1차~N차 분할 가중치 & 목표 평단가 시뮬레이션", font=get_font(7.5, 'medium'), fill=(71, 85, 105), anchor='mm')
    draw_arrow(draw, (c2, 562), (c2, 626), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 5. Feedback: 분할 매수 확정 (y=626 to 672, h=46)
    draw.rounded_rectangle([c2 - nw // 2, 626, c2 + nw // 2, 672], radius=6, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw_pill_badge(draw, left_x=c2 - 114, cy=640, text="FEEDBACK", font=get_font(6.5, 'bold'), theme='green', pad_x=4, height=14)
    draw.text((c2 - 44, 640), "차수별 분할 매수 분배 완료", font=get_font(9, 'bold'), fill=(22, 101, 52), anchor='lm')
    draw.text((c2, 656), "1차~N차 분할 가중치 & 계좌 방어율 매핑", font=get_font(7.5, 'medium'), fill=(21, 128, 61), anchor='mm')
    
    # Inter-Stage Handover Arrow to Stage 04
    draw_arrow(draw, (cols_x[2] + cw, 647), (cols_x[3], 647), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text(((cols_x[2] + cw + cols_x[3]) // 2, 635), "검증 →", font=get_font(8, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    # =============================================================
    # DIAGRAM TRACK 4: STAGE 04 (Center: 1308)
    # =============================================================
    c3 = col_centers[3]
    
    # 1. Screen: 포트폴리오 리스크 시트 (y=300 to 344, h=44)
    draw.rounded_rectangle([c3 - nw // 2, 300, c3 + nw // 2, 344], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw_pill_badge(draw, left_x=c3 - 114, cy=314, text="SCREEN", font=get_font(6.5, 'bold'), theme='slate', pad_x=4, height=14)
    draw.text((c3 - 54, 314), "포트폴리오 리스크 시뮬레이션", font=get_font(9, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((c3, 331), "추가 매수 후 계좌 쏠림도 및 잔여 예수금 산출", font=get_font(7.5, 'medium'), fill=(100, 116, 139), anchor='mm')
    draw_arrow(draw, (c3, 344), (c3, 362), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 2. Diamond Decision: 65% 예수금 안전선 판정 (cy=390, w=216, h=56)
    draw_diamond(draw, cx=c3, cy=390, w=216, h=56, fill=(254, 243, 199), outline=(217, 119, 6), width=2)
    draw.text((c3, 384), "예수금 안전선 판정 (Risk Guard)", font=get_font(9, 'bold'), fill=(180, 83, 9), anchor='mm')
    draw.text((c3, 397), "소요 예수금 > 가용 자산 65% ?", font=get_font(7, 'medium'), fill=(146, 64, 14), anchor='mm')
    
    # Branch Yes (Left warning)
    draw_dashed_line(draw, (c3 - 108, 390), (cols_x[3] + 16, 390), col=(244, 63, 94), width=1)
    draw_dashed_arrow(draw, (cols_x[3] + 16, 390), (cols_x[3] + 16, 416), col=(244, 63, 94), width=1, arrow_size=3)
    draw.rounded_rectangle([cols_x[3] + 4, 416, cols_x[3] + 80, 452], radius=5, fill=(254, 242, 242), outline=(244, 63, 94), width=1)
    draw.text((cols_x[3] + 42, 428), "자금 고갈 주의", font=get_font(7, 'bold'), fill=(153, 27, 27), anchor='mm')
    draw.text((cols_x[3] + 42, 440), "분할 차수 확대 권고", font=get_font(6.5, 'medium'), fill=(153, 27, 27), anchor='mm')
    draw_dashed_line(draw, (cols_x[3] + 42, 452), (cols_x[3] + 42, 474), col=(244, 63, 94), width=1)
    draw_dashed_arrow(draw, (cols_x[3] + 42, 474), (c3 - nw // 2, 474), col=(244, 63, 94), width=1, arrow_size=3)
    
    # Branch No (Down: Safe)
    draw_arrow(draw, (c3, 418), (c3, 454), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text((c3 + 30, 436), "No (안전)", font=get_font(7.5, 'bold'), fill=(5, 150, 105), anchor='mm')
    
    # 3. Action: 하락 스트레스 테스트 검증 (y=454 to 498, h=44)
    draw.rounded_rectangle([c3 - nw // 2, 454, c3 + nw // 2, 498], radius=6, fill=(240, 246, 255), outline=(0, 82, 255), width=1)
    draw_pill_badge(draw, left_x=c3 - 114, cy=468, text="ACTION", font=get_font(6.5, 'bold'), theme='blue', pad_x=4, height=14)
    draw.text((c3 - 54, 468), "하락 스트레스 테스트 검증", font=get_font(9, 'bold'), fill=(0, 82, 255), anchor='lm')
    draw.text((c3, 485), "시장 -10%~-30% 급락 시 계좌 충격도 점검", font=get_font(7.5, 'medium'), fill=(71, 85, 105), anchor='mm')
    draw_arrow(draw, (c3, 498), (c3, 524), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 4. Diamond Decision: 리스크 허용 한도 승인? (cy=550, w=186, h=52)
    draw_diamond(draw, cx=c3, cy=550, w=186, h=52, fill=(254, 243, 199), outline=(217, 119, 6), width=2)
    draw.text((c3, 544), "리스크 허용 한도 승인?", font=get_font(9, 'bold'), fill=(180, 83, 9), anchor='mm')
    draw.text((c3, 558), "객관적 방어선 충족 판정", font=get_font(7, 'medium'), fill=(146, 64, 14), anchor='mm')
    draw_arrow(draw, (c3, 576), (c3, 626), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text((c3 + 30, 601), "승인 완료", font=get_font(7.5, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    # 5. Feedback: 최종 승인 완료 (y=626 to 672, h=46)
    draw.rounded_rectangle([c3 - nw // 2, 626, c3 + nw // 2, 672], radius=6, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw_pill_badge(draw, left_x=c3 - 114, cy=640, text="FEEDBACK", font=get_font(6.5, 'bold'), theme='green', pad_x=4, height=14)
    draw.text((c3 - 44, 640), "안전 가이드 적합 최종 승인", font=get_font(9, 'bold'), fill=(22, 101, 52), anchor='lm')
    draw.text((c3, 656), "리스크 검증 완료 및 최종 분할 매수안 확정", font=get_font(7.5, 'medium'), fill=(21, 128, 61), anchor='mm')
    
    # Inter-Stage Handover Arrow to Stage 05
    draw_arrow(draw, (cols_x[3] + cw, 647), (cols_x[4], 647), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text(((cols_x[3] + cw + cols_x[4]) // 2, 635), "승인 →", font=get_font(8, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    # =============================================================
    # DIAGRAM TRACK 5: STAGE 05 (Center: 1656)
    # =============================================================
    c4 = col_centers[4]
    
    # 1. Action: 1-Tap 포트폴리오 저장 (y=300 to 344, h=44)
    draw.rounded_rectangle([c4 - nw // 2, 300, c4 + nw // 2, 344], radius=6, fill=(239, 246, 255), outline=(0, 82, 255), width=2)
    draw_pill_badge(draw, left_x=c4 - 114, cy=314, text="ACTION", font=get_font(6.5, 'bold'), theme='blue', pad_x=4, height=14)
    draw.text((c4 - 54, 314), "1-Tap 포트폴리오 저장", font=get_font(9, 'bold'), fill=(0, 82, 255), anchor='lm')
    draw.text((c4, 331), "최적 매수 플랜 & 시나리오를 내 자산에 즉시 반영", font=get_font(7.5, 'medium'), fill=(15, 23, 42), anchor='mm')
    draw_arrow(draw, (c4, 344), (c4, 362), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 2. Feedback: 저장 완료 스낵바 (y=362 to 406, h=44)
    draw.rounded_rectangle([c4 - nw // 2, 362, c4 + nw // 2, 406], radius=6, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw_pill_badge(draw, left_x=c4 - 114, cy=376, text="FEEDBACK", font=get_font(6.5, 'bold'), theme='green', pad_x=4, height=14)
    draw.text((c4 - 44, 376), "저장 완료 스낵바 & 자산 연동", font=get_font(9, 'bold'), fill=(22, 101, 52), anchor='lm')
    draw.text((c4, 393), "포트폴리오 자산 등록 및 목표 평단가 트래킹 개시", font=get_font(7.5, 'medium'), fill=(21, 128, 61), anchor='mm')
    draw_arrow(draw, (c4, 406), (c4, 426), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 3. Decision Diamond: 데이터 무결성 검증 (cy=454, w=206, h=56)
    draw_diamond(draw, cx=c4, cy=454, w=206, h=56, fill=(254, 243, 199), outline=(217, 119, 6), width=2)
    draw.text((c4, 448), "데이터 무결성 검증?", font=get_font(9, 'bold'), fill=(180, 83, 9), anchor='mm')
    draw.text((c4, 461), "외부 서버 전송 0건 & 로컬 암호화", font=get_font(7, 'medium'), fill=(146, 64, 14), anchor='mm')
    draw_arrow(draw, (c4, 482), (c4, 514), col=(0, 82, 255), width=2, arrow_size=4)
    draw.text((c4 + 32, 498), "100% 무결", font=get_font(7.5, 'bold'), fill=(5, 150, 105), anchor='mm')
    
    # 4. Storage Node (y=514 to 562, h=48)
    draw_database_node(draw, cx=c4, cy=538, w=nw, h=48, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw_pill_badge(draw, left_x=c4 - 114, cy=530, text="STORAGE", font=get_font(6.5, 'bold'), theme='slate', pad_x=4, height=14)
    draw.text((c4 - 48, 530), "100% 온디바이스 로컬 암호화", font=get_font(9, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((c4, 550), "외부 서버 전송 0건, 개인 금융 데이터 완전 보호", font=get_font(7.5, 'medium'), fill=(100, 116, 139), anchor='mm')
    draw_arrow(draw, (c4, 562), (c4, 586), col=(0, 82, 255), width=2, arrow_size=4)
    
    # 5. Finish Terminal Capsule (y=586 to 622, h=36)
    draw.rounded_rectangle([c4 - 90, 586, c4 + 90, 622], radius=18, fill=(0, 82, 255))
    draw.text((c4, 604), "Finish : 최적 방어 플랜 저장", font=get_font(10, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # -------------------------------------------------------------
    # SIMPLIFIED BOTTOM SUMMARY STRIP (y=706 to 826, h=120)
    # Generous margin from diagram (cy ended at 668, gap = 38px)
    # -------------------------------------------------------------
    bar_x = 100
    # -------------------------------------------------------------
    bar_x = 100
    bar_y = 698
    bar_w = 1720
    bar_h = 142
    draw.rounded_rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], radius=12, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    
    # Left Half: Emotional Curve (w = 860) with generous internal padding
    draw_pill_badge(draw, left_x=bar_x + 24, cy=bar_y + 20, text="USER MINDSET", font=get_font(8, 'bold'), theme='amber', has_dot=True, pad_x=7, height=18)
    draw.text((bar_x + 150, bar_y + 20), "5단계 심리 변화 여정 (불안에서 확신까지)", font=get_font(11.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((bar_x + 24, bar_y + 40), "급락장 패닉 상태의 투자자가 객관적 퀀트 가이드를 통해 평정심을 되찾고 최적 플랜을 확정하는 여정", font=get_font(8.5, 'regular'), fill=(100, 116, 139))
    
    emotions = [
        ("STAGE 01", "불안 & 막막함", "red"),
        ("STAGE 02", "긴박 & 촉박", "amber"),
        ("STAGE 03", "명확한 목표 발견", "blue"),
        ("STAGE 04", "안도 & 통제감 회복", "cyan"),
        ("STAGE 05", "확신 & 플랜 확정", "green")
    ]
    node_w = 145
    node_y = bar_y + 58
    node_h = 68
    for e_idx, (ecode, ename, etheme) in enumerate(emotions):
        nx = bar_x + 24 + e_idx * (node_w + 22)
        draw.rounded_rectangle([nx, node_y, nx + node_w, node_y + node_h], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        # Inner padding inside emotion node: 12px left, 12px top, generous 15px bottom margin
        draw_pill_badge(draw, left_x=nx + 12, cy=node_y + 18, text=ecode, font=get_font(7.5, 'bold'), theme=etheme, pad_x=4, height=16)
        draw.text((nx + 12, node_y + 42), ename, font=get_font(9.5, 'bold'), fill=(15, 23, 42))
        if e_idx < 4:
            arrow_sx = nx + node_w + 2
            arrow_ex = nx + node_w + 20
            draw_arrow(draw, (arrow_sx, node_y + node_h // 2), (arrow_ex, node_y + node_h // 2), col=(148, 163, 184), width=1, arrow_size=3)
            
    # Vertical Divider Line
    draw.line([(bar_x + 890, bar_y + 14), (bar_x + 890, bar_y + bar_h - 14)], fill=(226, 232, 240), width=1)
    
    # Right Half: Enterprise UX KPIs (w = 800) with generous internal padding
    kpi_x = bar_x + 914
    draw_pill_badge(draw, left_x=kpi_x, cy=bar_y + 20, text="UX IMPACT", font=get_font(8, 'bold'), theme='blue', has_dot=True, pad_x=7, height=18)
    draw.text((kpi_x + 120, bar_y + 20), "정량적 서비스 기획 성과 지표", font=get_font(11.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.text((kpi_x, bar_y + 40), "실제 프로덕션 배포 및 태스크 기반 검증 완료 지표", font=get_font(8.5, 'regular'), fill=(100, 116, 139))
    
    kpis = [
        ("총 소요 시간", "< 3.2초", "기존 대비 84% 단축", "blue"),
        ("인터랙션 단계", "7단계 → 2단계", "엄지 영역 통합 설계", "green"),
        ("역산 연산 지연", "0ms 즉시", "폐쇄형 대수 공식 완결", "blue"),
        ("개인 금융 보안", "100% 로컬", "외부 유출 0건 온디바이스", "slate")
    ]
    kw = (bar_w - 938 - 24) // 4
    for kidx, (klabel, kval, ksub, kcol) in enumerate(kpis):
        kx = kpi_x + kidx * (kw + 10)
        draw.rounded_rectangle([kx, node_y, kx + kw, node_y + node_h], radius=8, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
        # Inner padding inside KPI card: 14px left, 13px top, and generous 13px bottom margin
        draw.text((kx + 14, node_y + 13), klabel, font=get_font(8.5, 'bold'), fill=(100, 116, 139))
        draw.text((kx + 14, node_y + 28), kval, font=get_font(12, 'bold'), fill=(0, 82, 255))
        draw.text((kx + 14, node_y + 46), ksub, font=get_font(7.5, 'medium'), fill=(71, 85, 105))
        
    draw_slide_footer(draw, 5)
    base.save(f'{OUT_DIR}/slide_05.png')
    print("SAVED perfect Slide 05 successfully!")



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
        title_blue="4대 모바일 와이어프레임과 인체공학적 설계", 
        subtitle_kr="홈 대시보드·계산기·음성도크·목표역산 4대 핵심 화면의 골격 구조와 한 손 조작을 위한 엄지 조작 반경(Thumb-Zone) 인체공학 설계"
    )
    
    # -----------------------------------------------------------------
    # UPPER SECTION: 4 EXPANDED MODERN 19.5:9 SMARTPHONE WIREFRAME CHASSIS
    # -----------------------------------------------------------------
    sec_y = 234
    ph = 525
    pw = 280
    
    p1_x = 100
    p2_x = 580
    p3_x = 1060
    p4_x = 1540
    
    # Helper to draw chassis base with soft shadow & dynamic island
    def draw_wireframe_chassis(draw_obj, px, title_text, theme_key):
        # Soft drop shadow
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        shd = ImageDraw.Draw(sh)
        shd.rounded_rectangle([px + 8, sec_y + 12, px + pw - 8, sec_y + ph + 16], radius=28, fill=(0, 0, 0, 30))
        sh_blur = sh.filter(ImageFilter.GaussianBlur(14))
        base.paste(sh_blur, (0, 0), sh_blur)
        
        # Outer Chassis
        draw.rounded_rectangle([px, sec_y, px + pw, sec_y + ph], radius=26, fill=(255, 255, 255), outline=(15, 23, 42), width=2)
        # Dynamic Island Pill
        draw.rounded_rectangle([px + pw//2 - 24, sec_y + 8, px + pw//2 + 24, sec_y + 20], radius=6, fill=(15, 23, 42))
        # Screen Title Badge
        draw_pill_badge(draw, cx=px + pw//2, cy=sec_y + 36, text=title_text, font=get_font(9.5, 'bold'), theme=theme_key, has_dot=True, pad_x=8, height=20)
        # Native Home Indicator
        draw.rounded_rectangle([px + pw//2 - 24, sec_y + ph - 8, px + pw//2 + 24, sec_y + ph - 4], radius=2, fill=(15, 23, 42))
        
        # Thumb-Zone 48dp ergonomic bottom arc highlight
        tz_y = sec_y + ph - 92
        draw.rounded_rectangle([px + 6, tz_y, px + pw - 6, sec_y + ph - 14], radius=16, fill=(0, 81, 255, 12), outline=(0, 81, 255, 70), width=1)
        draw.text((px + pw - 14, tz_y + 6), "Thumb-Zone (48dp)", font=get_font(7.5, 'bold'), fill=(0, 81, 255), anchor='ra')

    # Helper to draw PRD-level aesthetic callout pin on core features
    def draw_callout_anchor_pin(draw_obj, cx, cy, pin_num, pin_label, accent_col, is_right=True):
        # Soft outer pulse halo (radius 16)
        draw_obj.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(*accent_col[:3], 45))
        # Crisp white border ring
        draw_obj.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(255, 255, 255), outline=accent_col, width=2)
        # Inner solid colored circle
        draw_obj.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=accent_col)
        # Pin number text
        draw_obj.text((cx, cy), str(pin_num), font=get_font(9.5, 'bold'), fill=(255, 255, 255), anchor='mm')
        
        # Micro callout pill tag
        tag_font = get_font(8.5, 'bold')
        t_bbox = draw_obj.textbbox((0, 0), pin_label, font=tag_font)
        tw = t_bbox[2] - t_bbox[0] + 16
        th = 20
        if is_right:
            tx = cx + 14
            draw_obj.rounded_rectangle([tx, cy - th//2, tx + tw, cy + th//2], radius=5, fill=(15, 23, 42), outline=accent_col, width=1)
            draw_obj.text((tx + tw//2, cy), pin_label, font=tag_font, fill=(255, 255, 255), anchor='mm')
        else:
            tx = cx - 14 - tw
            draw_obj.rounded_rectangle([tx, cy - th//2, tx + tw, cy + th//2], radius=5, fill=(15, 23, 42), outline=accent_col, width=1)
            draw_obj.text((tx + tw//2, cy), pin_label, font=tag_font, fill=(255, 255, 255), anchor='mm')

    # -----------------------------------------------------------------
    # Chassis 1: [SCR-01 · 홈 대시보드] (p1_x = 100)
    # -----------------------------------------------------------------
    draw_wireframe_chassis(draw, p1_x, "① SCR-01 · 홈 대시보드", "blue")
    
    # VIP One-Line Banner Mockup
    v_y = sec_y + 54
    draw.rounded_rectangle([p1_x + 14, v_y, p1_x + pw - 14, v_y + 24], radius=6, fill=(254, 243, 199), outline=(253, 230, 138), width=1)
    draw.text((p1_x + 24, v_y + 6), "⚡ VIP 24h 무광고 세션", font=get_font(8.5, 'bold'), fill=(180, 83, 9))
    draw.text((p1_x + pw - 24, v_y + 6), "남은시간 23:59:42", font=get_num_font(8.5, 'bold'), fill=(217, 119, 6), anchor='ra')
    
    # Smart Portfolio Summary Card (_buildMembershipCard)
    sc_y = v_y + 32
    draw.rounded_rectangle([p1_x + 14, sc_y, p1_x + pw - 14, sc_y + 116], radius=12, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((p1_x + 24, sc_y + 12), "스마트 포트폴리오 메인 요약", font=get_font(10.5, 'bold'), fill=(0, 81, 255))
    draw.text((p1_x + 24, sc_y + 32), "₩ 12,500,000", font=get_num_font(18, 'black'), fill=(15, 23, 42))
    draw.text((p1_x + 24, sc_y + 60), "평가손익 -₩ 2,150,000", font=get_font(10.5, 'bold'), fill=(239, 68, 68))
    draw_pill_badge(draw, cx=p1_x + pw - 48, cy=sc_y + 67, text="-17.2%", font=get_num_font(9, 'bold'), theme='red', has_dot=False, pad_x=8, height=18, solid=True)
    draw.line([(p1_x + 24, sc_y + 84), (p1_x + pw - 24, sc_y + 84)], fill=(191, 219, 254), width=1)
    draw.text((p1_x + 24, sc_y + 94), "• 1차 분할매수 가이드 권장", font=get_font(9.5, 'medium'), fill=(71, 85, 105))
    draw.text((p1_x + pw - 24, sc_y + 94), "통화 : KRW ₩", font=get_font(9.5, 'bold'), fill=(0, 81, 255), anchor='ra')
    
    # 1-Line Hero Button (_buildSimulatorHeroButton)
    hb_y = sc_y + 124
    draw.rounded_rectangle([p1_x + 14, hb_y, p1_x + pw - 14, hb_y + 36], radius=9, fill=(0, 81, 255))
    draw.text((p1_x + pw//2, hb_y + 18), "+ 물타기 계산기 실행 (DCA)", font=get_font(11, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # 2x2 Quick Actions Grid (_buildQuickActions)
    qg_y = hb_y + 44
    qw = (pw - 28 - 10) // 2
    qh = 30
    quick_items = [("목표 평단 역산", 0), ("1-Tap MTS 복사", 1), ("하락 시나리오", 2), ("거래 수수료 계산", 3)]
    for q_txt, q_idx in quick_items:
        qx = p1_x + 14 + (q_idx % 2) * (qw + 10)
        qy = qg_y + (q_idx // 2) * (qh + 8)
        draw.rounded_rectangle([qx, qy, qx + qw, qy + qh], radius=7, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((qx + qw//2, qy + qh//2), q_txt, font=get_font(9.5, 'medium'), fill=(71, 85, 105), anchor='mm')
        
    # Asset List Card Item (_buildAssetCard)
    ac_y = qg_y + 76
    draw.rounded_rectangle([p1_x + 14, ac_y, p1_x + pw - 14, ac_y + 50], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((p1_x + 24, ac_y + 9), "삼성전자 (005930)", font=get_font(10.5, 'bold'), fill=(15, 23, 42))
    draw_pill_badge(draw, cx=p1_x + pw - 45, cy=ac_y + 16, text="-18.3%", font=get_num_font(8.5, 'bold'), theme='red', has_dot=False, pad_x=6, height=16)
    draw.text((p1_x + 24, ac_y + 29), "평단 ₩ 72,500 (100주) · 현재 ₩ 59,200", font=get_font(9, 'medium'), fill=(100, 116, 139))
    
    # Callout Anchor Pin ① floating above Thumb-Zone
    draw_callout_anchor_pin(draw, p1_x + 24, ac_y + 68, "1", "① Fitts' 한 손 조작 존", (0, 81, 255), is_right=True)

    # Bottom Navigation Bar
    bb_y = sec_y + ph - 70
    draw.line([(p1_x + 14, bb_y), (p1_x + pw - 14, bb_y)], fill=(226, 232, 240), width=1)
    draw.text((p1_x + 40, bb_y + 18), "홈", font=get_font(10, 'bold'), fill=(0, 81, 255), anchor='mm')
    draw.text((p1_x + pw - 40, bb_y + 18), "설정", font=get_font(10, 'medium'), fill=(100, 116, 139), anchor='mm')
    # Center Mic FAB inside Thumb Zone
    fab_cx = p1_x + pw//2
    fab_cy = bb_y + 18
    draw.ellipse([fab_cx - 16, fab_cy - 16, fab_cx + 16, fab_cy + 16], fill=(0, 81, 255))
    draw_mic_icon(draw, cx=fab_cx, cy=fab_cy, size=16, color=(255, 255, 255))

    # -----------------------------------------------------------------
    # Chassis 2: [SCR-02 · 스마트 물타기 계산기] (p2_x = 580)
    # -----------------------------------------------------------------
    draw_wireframe_chassis(draw, p2_x, "② SCR-02 · 계산기 엔진", "amber")
    
    # Input 1: Current Price & Holdings (_buildInputSection)
    i1_y = sec_y + 54
    draw.rounded_rectangle([p2_x + 14, i1_y, p2_x + pw - 14, i1_y + 54], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((p2_x + 24, i1_y + 9), "현재 보유 평단가 & 수량", font=get_font(9.5, 'bold'), fill=(100, 116, 139))
    draw.text((p2_x + 24, i1_y + 29), "₩ 65,000", font=get_num_font(15, 'bold'), fill=(15, 23, 42))
    draw.text((p2_x + pw - 24, i1_y + 29), "100 주 (₩6.5M)", font=get_font(10, 'bold'), fill=(71, 85, 105), anchor='ra')
    
    # Input 2: Additional Price & Stepper
    i2_y = i1_y + 64
    draw.rounded_rectangle([p2_x + 14, i2_y, p2_x + pw - 14, i2_y + 68], radius=10, fill=(248, 250, 252), outline=(0, 81, 255), width=2)
    draw.text((p2_x + 24, i2_y + 9), "추가 매수 단가 & 수량 조절", font=get_font(9.5, 'bold'), fill=(0, 81, 255))
    draw.text((p2_x + 24, i2_y + 29), "₩ 55,000", font=get_num_font(15, 'bold'), fill=(15, 23, 42))
    # Glowing cursor
    draw.line([(p2_x + 115, i2_y + 29), (p2_x + 115, i2_y + 47)], fill=(0, 81, 255), width=2)
    
    # Stepper Control [ - 50주 + ]
    st_y = i2_y + 21
    draw.rounded_rectangle([p2_x + pw - 105, st_y, p2_x + pw - 20, st_y + 28], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw.text((p2_x + pw - 94, st_y + 14), "-", font=get_font(13, 'bold'), fill=(0, 81, 255), anchor='mm')
    draw.text((p2_x + pw - 62, st_y + 14), "50 주", font=get_num_font(10.5, 'bold'), fill=(15, 23, 42), anchor='mm')
    draw.text((p2_x + pw - 31, st_y + 14), "+", font=get_font(13, 'bold'), fill=(0, 81, 255), anchor='mm')
    
    # Preset Chips Row
    pr_y = i2_y + 76
    chips = ["-5%", "-10%", "+50주", "+100주", "전액 매수"]
    c_x = p2_x + 14
    for cp in chips:
        c_w = (pw - 28 - 16) // len(chips)
        draw.rounded_rectangle([c_x, pr_y, c_x + c_w, pr_y + 24], radius=6, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
        draw.text((c_x + c_w//2, pr_y + 12), cp, font=get_font(8.5, 'bold'), fill=(0, 81, 255), anchor='mm')
        c_x += c_w + 4
        
    # Callout Anchor Pin ② in clean corridor (y=474, chips end at 452, result card starts at 496)
    res_y = pr_y + 44
    draw_callout_anchor_pin(draw, p2_x + 24, pr_y + 34, "2", "② 비정상 사전 가드 엔진", (217, 119, 6), is_right=True)

    # Result Summary Card (_buildResultSummaryCard)
    draw.rounded_rectangle([p2_x + 14, res_y, p2_x + pw - 14, res_y + 114], radius=12, fill=(254, 243, 199), outline=(217, 119, 6), width=1)
    draw.text((p2_x + 24, res_y + 12), "실시간 가중평균 & 가드 결과", font=get_font(10.5, 'bold'), fill=(180, 83, 9))
    draw.text((p2_x + 24, res_y + 32), "예상 신규 평단 ₩ 61,667", font=get_num_font(16, 'black'), fill=(15, 23, 42))
    draw_pill_badge(draw, cx=p2_x + pw - 48, cy=res_y + 40, text="+5.1%p", font=get_num_font(8.5, 'bold'), theme='amber', has_dot=False, pad_x=6, height=18, solid=True)
    draw.line([(p2_x + 24, res_y + 60), (p2_x + pw - 24, res_y + 60)], fill=(253, 230, 138), width=1)
    draw.text((p2_x + 24, res_y + 72), "필요 소요 예수금 : ₩ 2,750,000", font=get_font(9.5, 'medium'), fill=(71, 85, 105))
    draw.text((p2_x + 24, res_y + 92), "총 보유 수량 : 150 주 (본전 탈출선 회복)", font=get_font(9.5, 'bold'), fill=(15, 23, 42))
    
    # Primary CTA Button inside Thumb Zone
    btn_y = res_y + 124
    draw.rounded_rectangle([p2_x + 14, btn_y, p2_x + pw - 14, btn_y + 40], radius=10, fill=(0, 81, 255))
    draw_copy_icon(draw, cx=p2_x + 40, cy=btn_y + 20, size=13, color=(255, 255, 255))
    draw.text((p2_x + pw//2 + 8, btn_y + 20), "1-Tap MTS 주문 복사", font=get_font(12, 'bold'), fill=(255, 255, 255), anchor='mm')

    # -----------------------------------------------------------------
    # Chassis 3: [SCR-03 · AI 음성 비서 바텀시트] (p3_x = 1060)
    # -----------------------------------------------------------------
    draw_wireframe_chassis(draw, p3_x, "③ SCR-03 · AI 음성 도크", "purple")
    
    # Dimmed background representation
    draw.rounded_rectangle([p3_x + 10, sec_y + 50, p3_x + pw - 10, sec_y + 105], radius=8, fill=(226, 232, 240))
    draw.text((p3_x + pw//2, sec_y + 68), "배경 : 계산기 화면 (Dim 60%)", font=get_font(9.5, 'regular'), fill=(100, 116, 139), anchor='mm')
    draw.text((p3_x + pw//2, sec_y + 86), "화면 전환 없는 온디바이스 모달 오버레이", font=get_font(8.5, 'medium'), fill=(148, 163, 184), anchor='mm')
    
    # Bottom Sheet Container (Sliding up within phone bezel)
    bs_y = sec_y + 105
    draw.rounded_rectangle([p3_x + 4, bs_y, p3_x + pw - 4, sec_y + ph - 8], radius=22, fill=(255, 255, 255), outline=(122, 34, 255), width=2)
    # Drag Handle
    draw.rounded_rectangle([p3_x + pw//2 - 20, bs_y + 8, p3_x + pw//2 + 20, bs_y + 13], radius=2, fill=(203, 213, 225))
    
    # Sheet Header Badge
    draw_pill_badge(draw, cx=p3_x + pw//2, cy=bs_y + 28, text="0.2s VOICE RECOGNITION", font=get_font(9, 'bold'), theme='purple', has_dot=True, pad_x=8, height=20)
    
    # Floating Mic Pulse Glow
    mic_cy = bs_y + 66
    draw.ellipse([p3_x + pw//2 - 26, mic_cy - 26, p3_x + pw//2 + 26, mic_cy + 26], fill=(245, 243, 255), outline=(221, 214, 254), width=1)
    draw.ellipse([p3_x + pw//2 - 19, mic_cy - 19, p3_x + pw//2 + 19, mic_cy + 19], fill=(122, 34, 255))
    draw_mic_icon(draw, cx=p3_x + pw//2, cy=mic_cy, size=17, color=(255, 255, 255))
    
    # Realtime 9-Bar Voice Waveform Animation
    wv_y = mic_cy + 34
    wave_h = [8, 16, 26, 36, 22, 14, 20, 30, 12]
    w_start_x = p3_x + pw//2 - (len(wave_h) * 12) // 2
    for idx, wh in enumerate(wave_h):
        wx = w_start_x + idx * 12
        draw.rounded_rectangle([wx, wv_y - wh//2, wx + 6, wv_y + wh//2], radius=3, fill=(122, 34, 255))
        
    # Callout Anchor Pin ③ in clean corridor (y=478, wave ends at 453, bubble starts at 498)
    draw_callout_anchor_pin(draw, p3_x + 24, wv_y + 34, "3", "③ 0.2s 음성 STT 도크", (122, 34, 255), is_right=True)

    # Speech Bubble Mockup
    sb_y = wv_y + 50
    draw.rounded_rectangle([p3_x + 14, sb_y, p3_x + pw - 14, sb_y + 44], radius=8, fill=(245, 243, 255), outline=(221, 214, 254), width=1)
    draw.text((p3_x + pw//2, sb_y + 14), "“삼성전자 55,000원에 50주”", font=get_font(11, 'bold'), fill=(109, 40, 217), anchor='mm')
    draw.text((p3_x + pw//2, sb_y + 30), "0.2s 음성 STT 파싱 완료 → 3개 파라미터 추출", font=get_font(8.5, 'regular'), fill=(100, 116, 139), anchor='mm')
    
    # Parsed Quant Tags Row
    pt_y = sb_y + 52
    tags = [("종목: 삼성전자", 100), ("단가: ₩55,000", 85), ("수량: 50주", 65)]
    tx_start = p3_x + 14
    for tg, tw in tags:
        draw.rounded_rectangle([tx_start, pt_y, tx_start + tw, pt_y + 24], radius=6, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
        draw.text((tx_start + tw//2, pt_y + 12), tg, font=get_font(8.5, 'bold'), fill=(0, 81, 255), anchor='mm')
        tx_start += tw + 6
        
    # Auto Inject Button inside Thumb Zone
    inj_y = pt_y + 34
    draw.rounded_rectangle([p3_x + 14, inj_y, p3_x + pw - 14, inj_y + 40], radius=10, fill=(122, 34, 255))
    draw.text((p3_x + pw//2, inj_y + 20), "⚡ 계산기에 즉시 주입 (0.2s)", font=get_font(12, 'bold'), fill=(255, 255, 255), anchor='mm')

    # -----------------------------------------------------------------
    # Chassis 4: [SCR-04 · 목표 평단 역산 & 리포트] (p4_x = 1540)
    # -----------------------------------------------------------------
    draw_wireframe_chassis(draw, p4_x, "④ SCR-04 · 목표 역산 엔진", "green")
    
    # Target Goal Price Input
    g1_y = sec_y + 54
    draw.rounded_rectangle([p4_x + 14, g1_y, p4_x + pw - 14, g1_y + 52], radius=10, fill=(240, 246, 255), outline=(0, 81, 255), width=2)
    draw.text((p4_x + 24, g1_y + 9), "탈출 희망 목표 평단가 입력", font=get_font(9.5, 'bold'), fill=(0, 81, 255))
    draw.text((p4_x + 24, g1_y + 29), "₩ 70,000", font=get_num_font(17, 'black'), fill=(0, 81, 255))
    draw_pill_badge(draw, cx=p4_x + pw - 48, cy=g1_y + 32, text="TARGET", font=get_font(8.5, 'bold'), theme='blue', has_dot=False, pad_x=6, height=18)
    
    # Callout Anchor Pin ④ in clean corridor (g1 ends at 340, solution starts at 368)
    sol_y = g1_y + 76
    draw_callout_anchor_pin(draw, p4_x + 24, g1_y + 61, "4", "④ 0ms 닫힌 형식 역산", (5, 150, 105), is_right=True)

    # Closed-Form Solution Box (Green Theme)
    draw.rounded_rectangle([p4_x + 14, sol_y, p4_x + pw - 14, sol_y + 104], radius=12, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
    draw.text((p4_x + 24, sol_y + 12), "닫힌 형식(Closed-Form) 역산 결과", font=get_font(10, 'bold'), fill=(5, 150, 105))
    draw.text((p4_x + 24, sol_y + 32), "필요 매수량 : +42.5 주", font=get_font(14, 'bold'), fill=(5, 150, 105))
    draw.text((p4_x + 24, sol_y + 54), "소요 예수금 : ₩ 2,762,500", font=get_font(14, 'bold'), fill=(217, 119, 6))
    draw.line([(p4_x + 24, sol_y + 78), (p4_x + pw - 24, sol_y + 78)], fill=(167, 243, 208), width=1)
    draw.text((p4_x + 24, sol_y + 88), "✓ 오차율 0.00% · 단일 대수 방정식 도출", font=get_font(8.5, 'bold'), fill=(5, 150, 105))
    
    # Risk Telemetry & Boundary Check Card
    rk_y = sol_y + 112
    draw.rounded_rectangle([p4_x + 14, rk_y, p4_x + pw - 14, rk_y + 80], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((p4_x + 24, rk_y + 10), "계좌 리스크 진단 리포트", font=get_font(10, 'bold'), fill=(15, 23, 42))
    draw.text((p4_x + 24, rk_y + 29), "• 자산 쏠림도 : 42.5% (안전 한도 65% 이하)", font=get_font(9, 'medium'), fill=(71, 85, 105))
    draw.text((p4_x + 24, rk_y + 46), "• 예수금 보존율 : 65.0% (안전 마진 통과)", font=get_font(9, 'medium'), fill=(5, 150, 105))
    draw.text((p4_x + 24, rk_y + 62), "• 뇌동매매 방어 : 비정상 주문 사전 차단 완료", font=get_font(9, 'medium'), fill=(71, 85, 105))
    
    # Confirm Plan Action Button inside Thumb Zone
    cf_y = rk_y + 90
    draw.rounded_rectangle([p4_x + 14, cf_y, p4_x + pw - 14, cf_y + 40], radius=10, fill=(0, 81, 255))
    draw.text((p4_x + pw//2, cf_y + 20), "최종 분할 매수 플랜 확정 ↗", font=get_font(12, 'bold'), fill=(255, 255, 255), anchor='mm')

    # -----------------------------------------------------------------
    # INTERACTION FLOW STEP CONNECTORS (Between the 4 phones)
    # -----------------------------------------------------------------
    flow_connectors = [
        (p1_x + pw, p2_x, "01 → 02 계산기 실행", "1-Tap Handoff", "blue"),
        (p2_x + pw, p3_x, "02 → 03 음성 도크 호출", "0.2s STT 파싱", "purple"),
        (p3_x + pw, p4_x, "03 → 04 목표 역산 연동", "닫힌 공식 도출", "blue")
    ]
    flow_cy = sec_y + 240
    for x_start, x_end, flow_title, flow_sub, f_theme in flow_connectors:
        fcx = (x_start + x_end) // 2
        # Subtle horizontal connection line
        draw.line([(x_start + 12, flow_cy), (x_end - 12, flow_cy)], fill=(203, 213, 225), width=2)
        # Flow Badge Circle
        draw.ellipse([fcx - 16, flow_cy - 16, fcx + 16, flow_cy + 16], fill=(255, 255, 255), outline=(0, 81, 255) if f_theme=='blue' else (122, 34, 255), width=2)
        draw.text((fcx, flow_cy), "→", font=get_font(14, 'bold'), fill=(0, 81, 255) if f_theme=='blue' else (122, 34, 255), anchor='mm')
        # Flow step pill above
        draw_pill_badge(draw, cx=fcx, cy=flow_cy - 28, text=flow_title, font=get_font(8.5, 'bold'), theme=f_theme, pad_x=8, height=20)
        # Flow sub text below
        draw.text((fcx, flow_cy + 26), flow_sub, font=get_font(9, 'medium'), fill=(100, 116, 139), anchor='mm')

    # =========================================================================
    # LOWER SECTION: 4 SLIM ERGONOMIC ARCHITECTURE SYSTEM CARDS (y=785 to 970)
    # =========================================================================
    card_y = 785
    card_h = 185
    c_w = 415
    c_gap = 20
    
    ergo_cards = [
        (
            100,
            "THUMB-ZONE 48dp",
            "① Fitts' Law 한 손 조작성 최적화",
            "한 손 파지 시 엄지가 닿는 하단 120dp 반경 내 주요 액션(계산 실행, MTS 복사, 음성 FAB)을 집중 배치하여 손가락 이동 거리를 65% 단축했습니다.",
            "✓ 엄지 도달 속도 0.18s 입증",
            "blue", (0, 81, 255)
        ),
        (
            100 + (c_w + c_gap),
            "BOUNDARY GUARD",
            "② 비정상 입력 사전 가드 엔진",
            "현재가보다 높은 비현실적 목표가나 음수 입력 시 즉각 햅틱 경고를 발생시키고, 가용 예수금 범위 내 실현 가능한 최적 방어 평단을 추천합니다.",
            "✓ 주문 실수 및 뇌동매매 100% 차단",
            "amber", (217, 119, 6)
        ),
        (
            100 + (c_w + c_gap) * 2,
            "VOICE STT ENGINE",
            "③ 0.2초 온디바이스 음성 도크",
            "급변하는 주식 호가 속 8자리 소수점 키패드 타이핑을 대체하는 온디바이스 음성 인식으로, 0.2초 만에 종목·단가·수량을 동시 추출합니다.",
            "✓ 키패드 타이핑 피로 78% 절감",
            "purple", (122, 34, 255)
        ),
        (
            100 + (c_w + c_gap) * 3,
            "ZERO-LOSS HANDOFF",
            "④ 0ms 무손실 파라미터 인계",
            "역산으로 도출된 수치를 시뮬레이터와 MTS 클립보드로 0ms 자동 주입하여 수기 재입력 오류 및 시장가 매수 실수를 원천 방어합니다.",
            "✓ 파라미터 전달 손실률 0.00%",
            "green", (5, 150, 105)
        )
    ]
    
    for cx_card, badge_txt, title_txt, body_txt, metric_txt, th_key, accent_col in ergo_cards:
        draw.rounded_rectangle([cx_card, card_y, cx_card + c_w, card_y + card_h], radius=14, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        # Left accent stripe
        draw.rounded_rectangle([cx_card, card_y + 12, cx_card + 4, card_y + card_h - 12], radius=2, fill=accent_col)
        
        # Header Badge
        draw_pill_badge(draw, left_x=cx_card + 18, cy=card_y + 22, text=badge_txt, font=get_font(9, 'bold'), theme=th_key, has_dot=True, pad_x=8, height=20)
        # Title
        draw.text((cx_card + 18, card_y + 48), title_txt, font=get_font(13.5, 'bold'), fill=(15, 23, 42))
        draw.line([(cx_card + 18, card_y + 68), (cx_card + c_w - 18, card_y + 68)], fill=(241, 245, 249), width=1)
        
        # Body text wrap
        b_lines = wrap_text_by_words(body_txt, get_font(10.5, 'regular'), c_w - 36, draw)
        by_start = card_y + 78
        for bl in b_lines:
            draw.text((cx_card + 18, by_start), bl, font=get_font(10.5, 'regular'), fill=(71, 85, 105))
            by_start += 17
            
        # Metric Bottom Pill Tag
        draw.rounded_rectangle([cx_card + 16, card_y + card_h - 34, cx_card + c_w - 16, card_y + card_h - 12], radius=6, fill=(240, 246, 255) if th_key=='blue' else ((245, 243, 255) if th_key=='purple' else (248, 250, 252)), outline=(191, 219, 254) if th_key=='blue' else (226, 232, 240), width=1)
        draw.text((cx_card + 24, card_y + card_h - 23), metric_txt, font=get_font(10, 'bold'), fill=accent_col, anchor='lm')

    draw_slide_footer(draw, 6)
    base.save(f'{OUT_DIR}/slide_06.png')
    print("SAVED slide_06.png (Enhanced 4-Screen Mobile Wireframe & Ergonomic Architecture)")


# -----------------------------------------------------------------------------
# 24dp Financial Line Iconography Drawers (Uniform 1.5dp Stroke & 2dp Radius)
# -----------------------------------------------------------------------------
def draw_line_chart_icon(draw, cx, cy, size=24, color=(0, 81, 255)):
    s = size / 2.0
    draw.line([(cx - s*0.8, cy + s*0.8), (cx + s*0.8, cy + s*0.8)], fill=color, width=2)
    pts = [(cx - s*0.7, cy + s*0.4), (cx - s*0.2, cy + s*0.2), (cx + s*0.2, cy - s*0.1), (cx + s*0.7, cy - s*0.6)]
    draw.line(pts, fill=color, width=2)
    for px, py in pts:
        draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 255, 255), outline=color, width=1)
    draw.polygon([(cx + s*0.7, cy - s*0.6), (cx + s*0.4, cy - s*0.6), (cx + s*0.7, cy - s*0.3)], fill=color)

def draw_line_target_icon(draw, cx, cy, size=24, color=(0, 81, 255)):
    s = size / 2.0
    draw.ellipse([cx - s*0.8, cy - s*0.8, cx + s*0.8, cy + s*0.8], outline=color, width=2)
    draw.ellipse([cx - s*0.35, cy - s*0.35, cx + s*0.35, cy + s*0.35], outline=color, width=1)
    draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=color)
    draw.line([(cx - s*0.95, cy), (cx - s*0.6, cy)], fill=color, width=2)
    draw.line([(cx + s*0.6, cy), (cx + s*0.95, cy)], fill=color, width=2)
    draw.line([(cx, cy - s*0.95), (cx, cy - s*0.6)], fill=color, width=2)
    draw.line([(cx, cy + s*0.6), (cx, cy + s*0.95)], fill=color, width=2)

def draw_line_mic_icon(draw, cx, cy, size=24, color=(0, 81, 255)):
    s = size / 2.0
    draw.rounded_rectangle([cx - s*0.35, cy - s*0.8, cx + s*0.35, cy + s*0.1], radius=int(s*0.35), outline=color, width=2)
    draw.arc([cx - s*0.65, cy - s*0.35, cx + s*0.65, cy + s*0.45], start=0, end=180, fill=color, width=2)
    draw.line([(cx, cy + s*0.45), (cx, cy + s*0.8)], fill=color, width=2)
    draw.line([(cx - s*0.4, cy + s*0.8), (cx + s*0.4, cy + s*0.8)], fill=color, width=2)

def draw_line_shield_icon(draw, cx, cy, size=24, color=(0, 81, 255)):
    s = size / 2.0
    pts = [
        (cx - s*0.75, cy - s*0.75),
        (cx + s*0.75, cy - s*0.75),
        (cx + s*0.75, cy + s*0.1),
        (cx, cy + s*0.85),
        (cx - s*0.75, cy + s*0.1)
    ]
    draw.polygon(pts, outline=color, fill=(240, 246, 255))
    draw.line([(cx - s*0.3, cy), (cx - s*0.05, cy + s*0.3), (cx + s*0.4, cy - s*0.3)], fill=color, width=2)

def draw_line_wallet_icon(draw, cx, cy, size=24, color=(0, 81, 255)):
    s = size / 2.0
    draw.rounded_rectangle([cx - s*0.8, cy - s*0.6, cx + s*0.8, cy + s*0.7], radius=3, outline=color, width=2)
    draw.line([(cx - s*0.8, cy - s*0.2), (cx + s*0.8, cy - s*0.2)], fill=color, width=1)
    draw.rounded_rectangle([cx + s*0.2, cy - s*0.05, cx + s*0.85, cy + s*0.4], radius=2, fill=(240, 246, 255), outline=color, width=1)
    draw.ellipse([cx + s*0.45, cy + s*0.12, cx + s*0.6, cy + s*0.25], fill=color)

def draw_line_calc_icon(draw, cx, cy, size=24, color=(0, 81, 255)):
    s = size / 2.0
    draw.rounded_rectangle([cx - s*0.7, cy - s*0.85, cx + s*0.7, cy + s*0.85], radius=3, outline=color, width=2)
    draw.rounded_rectangle([cx - s*0.5, cy - s*0.65, cx + s*0.5, cy - s*0.25], radius=1, fill=(240, 246, 255), outline=color, width=1)
    draw.text((cx - s*0.35, cy - s*0.05), "+", font=get_font(7, 'bold'), fill=color, anchor='mm')
    draw.text((cx + s*0.35, cy - s*0.05), "-", font=get_font(7, 'bold'), fill=color, anchor='mm')
    draw.text((cx - s*0.35, cy + s*0.45), "×", font=get_font(7, 'bold'), fill=color, anchor='mm')
    draw.text((cx + s*0.35, cy + s*0.45), "=", font=get_font(7, 'bold'), fill=color, anchor='mm')

def draw_line_lock_icon(draw, cx, cy, size=24, color=(0, 81, 255)):
    s = size / 2.0
    draw.arc([cx - s*0.45, cy - s*0.85, cx + s*0.45, cy - s*0.05], start=180, end=0, fill=color, width=2)
    draw.rounded_rectangle([cx - s*0.65, cy - s*0.2, cx + s*0.65, cy + s*0.75], radius=3, fill=(240, 246, 255), outline=color, width=2)
    draw.ellipse([cx - 2, cy + s*0.05, cx + 2, cy + s*0.25], fill=color)
    draw.line([(cx, cy + s*0.2), (cx, cy + s*0.45)], fill=color, width=2)

def draw_line_tag_icon(draw, cx, cy, size=24, color=(0, 81, 255)):
    s = size / 2.0
    pts = [
        (cx - s*0.7, cy - s*0.3),
        (cx - s*0.2, cy - s*0.8),
        (cx + s*0.7, cy + s*0.1),
        (cx + s*0.2, cy + s*0.8),
        (cx - s*0.7, cy + s*0.3)
    ]
    draw.polygon(pts, outline=color, fill=(240, 246, 255), width=2)
    draw.ellipse([cx - s*0.35, cy - s*0.35, cx - s*0.15, cy - s*0.15], fill=color)
    draw.text((cx + s*0.1, cy + s*0.15), "%", font=get_font(7, 'bold'), fill=color, anchor='mm')

def make_slide_07():
    base = Image.new('RGBA', (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # Unified Header
    draw_slide_header(
        draw, 
        slide_num=7, 
        category_en="DESIGN SYSTEM | BRAND IDENTITY & COMPONENT ARCHITECTURE", 
        title_black="브랜드 정체성과 정밀함을 규정하는 ", 
        title_blue="비주얼 아이덴티티 & 디자인 시스템", 
        subtitle_kr="스마트 DCA 핵심 디자인 컨셉(침착한 정밀성·폐쇄형 역산·무마찰 기동성), 기하학 키라인 그리드, 24dp 아이코노그라피, 토큰 & 아토믹 킷"
    )
    
    # Coordinates
    # Row 1 (y=234 to 574, h=340) - 3 Columns
    r1_y = 234
    r1_h = 340
    
    col1_x = 100
    col1_w = 540
    
    col2_x = 665
    col2_w = 540
    
    col3_x = 1230
    col3_w = 590
    
    # -------------------------------------------------------------
    # CARD 01 (Upper Left): SMART DCA DESIGN CORE CONCEPTS (UX & GUI)
    # -------------------------------------------------------------
    draw.rounded_rectangle([col1_x, r1_y, col1_x + col1_w, r1_y + r1_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    b1_box = draw_pill_badge(draw, left_x=col1_x + 24, cy=r1_y + 30, text="FOUNDATION 01", font=get_font(9.5, 'bold'), theme='amber', has_dot=True, pad_x=8, height=22)
    draw.text((b1_box[2] + 14, r1_y + 30), "스마트 물타기 계산기 디자인 핵심 컨셉 (UX & GUI)", font=get_font(13.0, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.line([(col1_x + 24, r1_y + 52), (col1_x + col1_w - 24, r1_y + 52)], fill=(241, 245, 249), width=1)
    
    principles = [
        ("01. Calm Precision (침착한 정밀성 · Panic-Free)", 
         "하락장 공포와 정보 과부하를 차단하는 멘탈 케어 유도, 1초 내 주요 지표 식별",
         "불안을 잠재우는 딥 옵시디언 다크(#0D1117) & 이성적 퀀트 블루 AAA 고대비 배색", 
         (0, 81, 255)),
        ("02. Closed-Form Inversion (폐쇄형 역산 · Goal Seeking)", 
         "반복 입력 없이 단 1개의 목표 평단 지정으로 탈출 필요 수량·자금 즉시 도출",
         "핵심 지표 강조 빅 넘버 카드, Tabular 고정폭 타이포, 안전 마진 경고 뱃지", 
         (5, 150, 105)),
        ("03. Frictionless Velocity (무마찰 기동성 · Thumb-Zone)", 
         "변동성 장세에서 키보드 타자 마찰을 0으로 만드는 0.2초 음성 도크 & 1-Tap 칩",
         "화면 하단 엄지 조작 반경 플로팅 도크, R12/R16 일관된 스쿼클 터치 타겟", 
         (122, 34, 255))
    ]
    py_start = r1_y + 64
    for p_title, ux_text, gui_text, p_accent in principles:
        draw.rounded_rectangle([col1_x + 24, py_start, col1_x + col1_w - 24, py_start + 70], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.rounded_rectangle([col1_x + 24, py_start + 6, col1_x + 28, py_start + 64], radius=2, fill=p_accent)
        draw.text((col1_x + 36, py_start + 13), p_title, font=get_font(10.2, 'bold'), fill=p_accent)
        
        # UX Concept Row
        draw.text((col1_x + 36, py_start + 32), "[UX 컨셉]", font=get_font(8.2, 'bold'), fill=(15, 23, 42))
        draw.text((col1_x + 88, py_start + 32), ux_text, font=get_font(8.2, 'regular'), fill=(71, 85, 105))
        
        # GUI Concept Row
        draw.text((col1_x + 36, py_start + 49), "[GUI 컨셉]", font=get_font(8.2, 'bold'), fill=(15, 23, 42))
        draw.text((col1_x + 88, py_start + 49), gui_text, font=get_font(8.2, 'regular'), fill=(71, 85, 105))
        
        py_start += 78
        
    draw.rounded_rectangle([col1_x + 24, r1_y + r1_h - 38, col1_x + col1_w - 24, r1_y + r1_h - 14], radius=6, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((col1_x + col1_w // 2, r1_y + r1_h - 26), "Core Concepts: Calm Precision · Closed-Form Inversion · Frictionless Velocity", font=get_font(8.8, 'bold'), fill=(0, 81, 255), anchor='mm')
    
    # -------------------------------------------------------------
    # CARD 02 (Upper Center): APP ICON GEOMETRIC DRAFTING GRID & SPEC
    # -------------------------------------------------------------
    draw.rounded_rectangle([col2_x, r1_y, col2_x + col2_w, r1_y + r1_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    b2_box = draw_pill_badge(draw, left_x=col2_x + 24, cy=r1_y + 30, text="FOUNDATION 02", font=get_font(9.5, 'bold'), theme='blue', has_dot=True, pad_x=8, height=22)
    draw.text((b2_box[2] + 14, r1_y + 30), "앱 아이콘 기하학 와이어프레임 & 조형 규격", font=get_font(13.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.line([(col2_x + 24, r1_y + 52), (col2_x + col2_w - 24, r1_y + 52)], fill=(241, 245, 249), width=1)
    
    # Technical Drafting Blueprint Canvas Box (CLEAN LIGHT BACKGROUND - NO BLACK)
    ic_box_x = col2_x + 22
    ic_box_y = r1_y + 62
    ic_box_size = 178
    
    # Clean drafting canvas base
    draw.rounded_rectangle([ic_box_x, ic_box_y, ic_box_x + ic_box_size, ic_box_y + ic_box_size], radius=12, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    
    cx = ic_box_x + ic_box_size // 2
    cy = ic_box_y + ic_box_size // 2
    
    # Geometric Grid Parameters matching the exact reference guide
    S = 136
    R = S / 2.0 # 68px
    r_in = R * 0.425 # 28.9px
    r_mid = math.sqrt(2) * r_in # 40.87px
    ext = 11
    
    grid_line_color = (100, 116, 139)
    
    # -------------------------------------------------------------
    # BACKGROUND KEYLINE GRID (Exact form of attached reference guide)
    # -------------------------------------------------------------
    # 1. 45-degree & 135-degree Diagonals (Extended past corners)
    draw.line([(cx - R - ext, cy - R - ext), (cx + R + ext, cy + R + ext)], fill=grid_line_color, width=1)
    draw.line([(cx - R - ext, cy + R + ext), (cx + R + ext, cy - R - ext)], fill=grid_line_color, width=1)
    
    # 2. 5 Horizontal lines (Outer lines extended past corners to form tick crosses)
    draw.line([(cx - R - ext, cy - R), (cx + R + ext, cy - R)], fill=grid_line_color, width=1) # top outer
    draw.line([(cx - R, cy - r_in), (cx + R, cy - r_in)], fill=grid_line_color, width=1) # top inner
    draw.line([(cx - R, cy), (cx + R, cy)], fill=grid_line_color, width=1) # center horizontal
    draw.line([(cx - R, cy + r_in), (cx + R, cy + r_in)], fill=grid_line_color, width=1) # bottom inner
    draw.line([(cx - R - ext, cy + R), (cx + R + ext, cy + R)], fill=grid_line_color, width=1) # bottom outer
    
    # 3. 5 Vertical lines (Outer lines extended past corners to form tick crosses)
    draw.line([(cx - R, cy - R - ext), (cx - R, cy + R + ext)], fill=grid_line_color, width=1) # left outer
    draw.line([(cx - r_in, cy - R), (cx - r_in, cy + R)], fill=grid_line_color, width=1) # left inner
    draw.line([(cx, cy - R), (cx, cy + R)], fill=grid_line_color, width=1) # center vertical
    draw.line([(cx + r_in, cy - R), (cx + r_in, cy + R)], fill=grid_line_color, width=1) # right inner
    draw.line([(cx + R, cy - R - ext), (cx + R, cy + R + ext)], fill=grid_line_color, width=1) # right outer
    
    # 4. 3 Concentric Circles (Inner, Middle, Outer)
    draw.ellipse([cx - r_in, cy - r_in, cx + r_in, cy + r_in], outline=grid_line_color, width=1)
    draw.ellipse([cx - r_mid, cy - r_mid, cx + r_mid, cy + r_mid], outline=grid_line_color, width=1)
    draw.ellipse([cx - R, cy - R, cx + R, cy + R], outline=grid_line_color, width=1)
    
    # 5. Continuous Squircle Outer Border (R22.5%)
    r_corner = int(round(S * 0.225))
    draw.rounded_rectangle([cx - R, cy - R, cx + R, cy + R], radius=r_corner, outline=grid_line_color, width=1)
    
    # -------------------------------------------------------------
    # APP ICON PLACED ON TOP OF GRID (With Elevation Drop Shadow)
    # -------------------------------------------------------------
    try:
        raw_icon = Image.open('assets/app_icon.png')
        bbox = raw_icon.getbbox()
        bcx = (bbox[0] + bbox[2]) // 2
        bcy = (bbox[1] + bbox[3]) // 2
        bsize = max(bbox[2] - bbox[0], bbox[3] - bbox[1])
        cropped = raw_icon.crop((bcx - bsize//2, bcy - bsize//2, bcx + bsize//2, bcy + bsize//2))
        resized = cropped.resize((S, S), Image.Resampling.LANCZOS)
        
        # Soft elevation shadow behind icon
        s_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(s_layer)
        sdraw.rounded_rectangle([cx - S//2 + 2, cy - S//2 + 5, cx + S//2 + 2, cy + S//2 + 7], radius=r_corner + 2, fill=(15, 23, 42, 45))
        s_layer = s_layer.filter(ImageFilter.GaussianBlur(6))
        base = Image.alpha_composite(base, s_layer)
        
        # Translucent app icon (86% opacity) so the exact attached grid shows through!
        cr_rgba = resized.convert('RGBA')
        r, g, b, a = cr_rgba.split()
        a = a.point(lambda p: int(p * 0.86))
        cr_rgba.putalpha(a)
        
        icon_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        icon_layer.paste(cr_rgba, (cx - S//2, cy - S//2))
        base = Image.alpha_composite(base, icon_layer)
        draw = ImageDraw.Draw(base)
        
        # Crisp 1px boundary stroke around the icon
        draw.rounded_rectangle([cx - S//2, cy - S//2, cx + S//2, cy + S//2], radius=r_corner, outline=(0, 81, 255, 120), width=1)
    except Exception as e:
        print("Icon paste error:", e)
        
    # Technical Dimension Labels below box
    draw.text((cx, ic_box_y + ic_box_size + 13), "Golden Ratio Squircle Grid (1024×1024)", font=get_font(8.5, 'bold'), fill=(0, 81, 255), anchor='mm')
    draw.text((cx, ic_box_y + ic_box_size + 27), "Inner Ø288 · Mid Ø408 · Outer Ø680 · R22.5%", font=get_font(7.5, 'medium'), fill=(100, 116, 139), anchor='mm')
    
    # Right side: Specifications Breakdown
    m_x = ic_box_x + ic_box_size + 16
    specs = [
        ("01. 3대 기하학 동심원 & 황금비 분할", 
         "외접원, 내접원, 중심원의 수학적 동심원 체계와 45° 대각선 교차로",
         "시각적 무게중심과 조형적 황금비(Golden Ratio) 정밀 구축"),
        ("02. Dynamic Squircle Curvature (R22.5%)", 
         "연속 곡률(Continuous Curvature) 기반 스쿼클 마스킹으로",
         "모바일 런처 및 스토어 환경에서 왜곡 없는 라운딩 구현"),
        ("03. DCA 상승 아크(Arc) & 분할매수 기둥", 
         "하락을 반등으로 전환하는 상승 아크 곡선과 4개의 DCA 분할매수 바가",
         "기하학 그리드 축선에 100% 정렬된 퀀트 아이덴티티 완성")
    ]
    
    sy = r1_y + 64
    for title, l1, l2 in specs:
        draw.text((m_x, sy), title, font=get_font(10, 'bold'), fill=(0, 81, 255) if "01" in title else (15, 23, 42))
        draw.text((m_x, sy + 18), l1, font=get_font(8.5, 'regular'), fill=(71, 85, 105))
        draw.text((m_x, sy + 32), l2, font=get_font(8.5, 'regular'), fill=(71, 85, 105))
        sy += 54
        
    # Bottom Spec Pill
    draw.rounded_rectangle([col2_x + 24, r1_y + r1_h - 38, col2_x + col2_w - 24, r1_y + r1_h - 14], radius=6, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((col2_x + col2_w // 2, r1_y + r1_h - 26), "Golden Ratio Keyline Drafting Grid & Continuous Squircle Specification", font=get_font(8.8, 'bold'), fill=(71, 85, 105), anchor='mm')


    
    # -------------------------------------------------------------
    # CARD 03 (Upper Right): 24dp ICONOGRAPHY SYSTEM (FLUTTER MATERIAL)
    # -------------------------------------------------------------
    draw.rounded_rectangle([col3_x, r1_y, col3_x + col3_w, r1_y + r1_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    b3_box = draw_pill_badge(draw, left_x=col3_x + 24, cy=r1_y + 30, text="FOUNDATION 03", font=get_font(9.5, 'bold'), theme='cyan', has_dot=True, pad_x=8, height=22)
    draw.text((b3_box[2] + 14, r1_y + 30), "Flutter Material Rounded 24dp 아이코노그라피", font=get_font(13.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.line([(col3_x + 24, r1_y + 52), (col3_x + col3_w - 24, r1_y + 52)], fill=(241, 245, 249), width=1)
    
    # Spec Sub-strip
    draw.text((col3_x + 24, r1_y + 64), "Grid 24×24dp  ·  Optical Center  ·  Production Flutter Icons.*_rounded 토큰 1:1 바인딩", font=get_font(9, 'bold'), fill=(0, 81, 255))
    
    # 8 Official Flutter Production Icons (4 columns x 2 rows)
    icons_data = [
        ("차트/물타기 분석", "Icons.show_chart_rounded", 0xf0174),
        ("퀀트 역산 계산기", "Icons.calculate_rounded", 0xf5fd),
        ("0.2s 음성 도크", "Icons.mic_rounded", 0xf8bd),
        ("리스크 가드레일", "Icons.shield_outlined", 0xf379),
        ("스마트 포트폴리오", "Icons.account_balance_wallet", 0xf520),
        ("VIP 무광고 세션", "Icons.stars_rounded", 0xf01d5),
        ("시나리오 히스토리", "Icons.history_toggle_off", 0xf7f0),
        ("1-Tap 플랜 저장", "Icons.bookmark_added", 0xf5ce),
    ]
    
    ic_start_y = r1_y + 86
    ic_w = (col3_w - 48 - 30) // 4  # 128px
    ic_h = 96
    mat_font_icon = get_material_icon_font(23)
    
    for idx, (iname, itoken, icp) in enumerate(icons_data):
        row = idx // 4
        col = idx % 4
        ix = col3_x + 24 + col * (ic_w + 10)
        iy = ic_start_y + row * (ic_h + 10)
        
        draw.rounded_rectangle([ix, iy, ix + ic_w, iy + ic_h], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        
        icx = ix + ic_w // 2
        icy = iy + 26
        draw.rounded_rectangle([icx - 17, icy - 17, icx + 17, icy + 17], radius=8, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
        draw.text((icx, icy), chr(icp), font=mat_font_icon, fill=(0, 81, 255), anchor='mm')
        
        draw.text((icx, iy + 53), iname, font=get_font(10, 'bold'), fill=(15, 23, 42), anchor='mm')
        draw.text((icx, iy + 68), itoken, font=get_font(7.5, 'bold'), fill=(0, 81, 255), anchor='mm')
        draw.text((icx, iy + 82), f"{hex(icp)} · 24dp", font=get_font(7.5, 'regular'), fill=(100, 116, 139), anchor='mm')
        
    draw.rounded_rectangle([col3_x + 24, r1_y + r1_h - 38, col3_x + col3_w - 24, r1_y + r1_h - 14], radius=6, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((col3_x + col3_w // 2, r1_y + r1_h - 26), "Flutter 런타임 MaterialIcons-Regular.otf 실기기 렌더링 및 코드 토큰 100% 동기화", font=get_font(9.5, 'medium'), fill=(0, 81, 255), anchor='mm')

    # -------------------------------------------------------------
    # LOWER ROW (y=594 to 970, h=376): 2 WIDE COLUMNS
    # -------------------------------------------------------------
    r2_y = 594
    r2_h = 376
    
    colA_x = 100
    colA_w = 840
    
    colB_x = 960
    colB_w = 860
    
    # -------------------------------------------------------------
    # CARD 04 (Lower Left): DESIGN TOKENS (COLOR & TYPOGRAPHY)
    # -------------------------------------------------------------
    draw.rounded_rectangle([colA_x, r2_y, colA_x + colA_w, r2_y + r2_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    b4_box = draw_pill_badge(draw, left_x=colA_x + 28, cy=r2_y + 32, text="FOUNDATION 04", font=get_font(9.5, 'bold'), theme='blue', has_dot=True, pad_x=8, height=22)
    draw.text((b4_box[2] + 14, r2_y + 32), "AppColors 토큰 & Pretendard 타이포그래피", font=get_font(14, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.line([(colA_x + 28, r2_y + 54), (colA_x + colA_w - 28, r2_y + 54)], fill=(241, 245, 249), width=1)
    
    col_w_inner = (colA_w - 56 - 20) // 2  # 382px
    
    # Hero Color Swatch Card: Primary Electric Blue #0051FF
    hb_y = r2_y + 68
    draw.rounded_rectangle([colA_x + 28, hb_y, colA_x + 28 + col_w_inner, hb_y + 64], radius=10, fill=(0, 81, 255))
    draw.text((colA_x + 42, hb_y + 14), "PRIMARY ELECTRIC BLUE", font=get_font(12.5, 'bold'), fill=(255, 255, 255))
    draw.text((colA_x + 42, hb_y + 32), "AppColors.primaryBlue  ·  #0051FF", font=get_num_font(9.5, 'medium'), fill=(191, 219, 254))
    draw.text((colA_x + 42, hb_y + 46), "투자의 확신과 신뢰를 상징하는 시그니처 퀀트 블루", font=get_font(8.5, 'regular'), fill=(224, 242, 254))
    draw_pill_badge(draw, cx=colA_x + 28 + col_w_inner - 50, cy=hb_y + 32, text="8.4:1 AAA", font=get_font(9, 'bold'), theme='green', has_dot=False, pad_x=8, height=22)
    
    # 5 Semantic Swatches
    sub_swatches = [
        ("Accent Cyan", "#00D2FF", (0, 210, 255), "음성 도크 & 파형"),
        ("Accent Mint", "#00E676", (0, 230, 118), "수익률 & 반등"),
        ("Accent Coral", "#FF5252", (255, 82, 82), "손실 경고 & 헤지"),
        ("Surface Dark", "#0D1117", (13, 17, 23), "다크모드 캔버스"),
        ("Premium Gold", "#FFB300", (255, 179, 0), "VIP 무광고 배너"),
    ]
    sw_w = (col_w_inner - 32) // 5
    sw_y = hb_y + 74
    for i, (s_name, s_hex, s_col, s_usage) in enumerate(sub_swatches):
        sx = colA_x + 28 + i * (sw_w + 8)
        draw.rounded_rectangle([sx, sw_y, sx + sw_w, sw_y + 68], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.rounded_rectangle([sx + 6, sw_y + 6, sx + sw_w - 6, sw_y + 24], radius=4, fill=s_col)
        draw.text((sx + 6, sw_y + 28), s_name, font=get_font(8, 'bold'), fill=(15, 23, 42))
        draw.text((sx + 6, sw_y + 40), s_hex, font=get_num_font(8, 'bold'), fill=(71, 85, 105))
        draw.text((sx + 6, sw_y + 52), s_usage, font=get_font(7, 'medium'), fill=(100, 116, 139))
        
    # Gradients Row
    gr_y = sw_y + 78
    draw.text((colA_x + 28, gr_y), "Signature App Gradients:", font=get_font(9.5, 'bold'), fill=(71, 85, 105))
    gradients_data = [
        ("primaryGradient", (0, 81, 255), (0, 210, 255)),
        ("cardTealBlue", (10, 37, 64), (19, 62, 104)),
        ("vipGoldGradient", (255, 179, 0), (255, 109, 0)),
        ("voiceWaveGradient", (0, 210, 255), (122, 34, 255)),
    ]
    gr_w = (col_w_inner - 24) // 4
    for idx, (g_name, g_c1, g_c2) in enumerate(gradients_data):
        gx = colA_x + 28 + idx * (gr_w + 8)
        for step in range(gr_w):
            ratio = step / max(1, gr_w - 1)
            rc = int(g_c1[0] + (g_c2[0] - g_c1[0]) * ratio)
            gc = int(g_c1[1] + (g_c2[1] - g_c1[1]) * ratio)
            bc = int(g_c1[2] + (g_c2[2] - g_c1[2]) * ratio)
            draw.line([(gx + step, gr_y + 16), (gx + step, gr_y + 36)], fill=(rc, gc, bc))
        draw.rounded_rectangle([gx, gr_y + 16, gx + gr_w, gr_y + 36], radius=4, outline=(203, 213, 225), width=1)
        draw.text((gx + gr_w//2, gr_y + 44), g_name, font=get_font(7.5, 'bold'), fill=(71, 85, 105), anchor='mm')
        
    # Right Half of Card 04: Typography & Spatial Tokens
    ty_x = colA_x + 28 + col_w_inner + 20
    ty_w = col_w_inner
    
    t_rows = [
        ("Display 28", "Bold", "₩ 61,667", True),
        ("Headline 20", "Bold", "스마트 포트폴리오 요약", False),
        ("Title 16", "SemiBold", "추가 매수 단가 & 수량", False),
        ("Body 14", "Regular", "현재 평단가 기준 50주 추가", False),
        ("Caption 11", "Medium", "0.2s 음성 STT 파싱 완료", False),
    ]
    ty_start = r2_y + 68
    for i, (t_role, t_weight, t_sample, is_mono) in enumerate(t_rows):
        ry = ty_start + i * 32
        draw.rounded_rectangle([ty_x, ry, ty_x + ty_w, ry + 26], radius=6, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((ty_x + 10, ry + 6), t_role, font=get_font(9.5, 'bold'), fill=(0, 81, 255))
        draw.text((ty_x + 95, ry + 6), t_weight, font=get_font(9, 'medium'), fill=(100, 116, 139))
        draw.text((ty_x + ty_w - 10, ry + 6), t_sample, font=get_num_font(10, 'bold') if is_mono else get_font(9, 'semibold'), fill=(15, 23, 42), anchor='ra')
        
    # OpenType Spec Box
    sp_box_y = ty_start + len(t_rows) * 32 + 8
    draw.rounded_rectangle([ty_x, sp_box_y, ty_x + ty_w, r2_y + r2_h - 20], radius=10, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((ty_x + 14, sp_box_y + 10), "OpenType `tabularFigures()` & 4/8pt Grid", font=get_font(10, 'bold'), fill=(0, 81, 255))
    draw.text((ty_x + 14, sp_box_y + 28), "• Tabular Numbers: 실시간 호가 변동 시 숫자 떨림 방지", font=get_font(8.5, 'regular'), fill=(71, 85, 105))
    draw.text((ty_x + 14, sp_box_y + 44), "• Spatial System : 4pt/8pt 기반 스페이싱 및 r-8/12/16 라운딩", font=get_font(8.5, 'regular'), fill=(71, 85, 105))
    draw.text((ty_x + 14, sp_box_y + 60), "• Elevation : Level 1 (2dp), Level 2 (8dp), Level 3 (16dp FAB)", font=get_font(8.5, 'regular'), fill=(71, 85, 105))
    
    draw.text((colA_x + 28, r2_y + r2_h - 18), "• WCAG 2.1 AAA 7:1+ 초고대비율 엄격 준수 · AppColors 싱글톤 토큰 시스템", font=get_font(9, 'regular'), fill=(100, 116, 139))
    
    # -------------------------------------------------------------
    # CARD 05 (Lower Right): ATOMIC UI COMPONENT KIT
    # -------------------------------------------------------------
    draw.rounded_rectangle([colB_x, r2_y, colB_x + colB_w, r2_y + r2_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    b5_box = draw_pill_badge(draw, left_x=colB_x + 28, cy=r2_y + 32, text="FOUNDATION 05", font=get_font(9.5, 'bold'), theme='cyan', has_dot=True, pad_x=8, height=22)
    draw.text((b5_box[2] + 14, r2_y + 32), "프로덕션 아토믹 UI 컴포넌트 킷", font=get_font(14, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.line([(colB_x + 28, r2_y + 54), (colB_x + colB_w - 28, r2_y + 54)], fill=(241, 245, 249), width=1)
    
    k1_y = r2_y + 68
    k1_w = (colB_w - 56 - 20) // 2
    
    # Stepper Input Box
    draw.rounded_rectangle([colB_x + 28, k1_y, colB_x + 28 + k1_w, k1_y + 80], radius=10, fill=(248, 250, 252), outline=(0, 81, 255), width=2)
    draw.text((colB_x + 40, k1_y + 10), "현재 보유 평단가 & 정밀 스텝퍼", font=get_font(9.5, 'bold'), fill=(0, 81, 255))
    draw.text((colB_x + 40, k1_y + 30), "₩ 65,000", font=get_num_font(14, 'bold'), fill=(15, 23, 42))
    draw_pill_badge(draw, cx=colB_x + 28 + k1_w - 40, cy=k1_y + 26, text="ACTIVE", font=get_font(8, 'bold'), theme='blue', has_dot=False, pad_x=5, height=18)
    
    draw.rounded_rectangle([colB_x + 40, k1_y + 50, colB_x + 28 + k1_w - 12, k1_y + 72], radius=5, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    mat_font_btn = get_material_icon_font(15)
    draw.text((colB_x + 58, k1_y + 61), chr(0xf00f1), font=mat_font_btn, fill=(0, 81, 255), anchor='mm') # Icons.remove_rounded
    draw.text((colB_x + 28 + k1_w // 2, k1_y + 61), "100주 (수량 가감 조절)", font=get_font(9.5, 'bold'), fill=(15, 23, 42), anchor='mm')
    draw.text((colB_x + 28 + k1_w - 28, k1_y + 61), chr(0xf537), font=mat_font_btn, fill=(0, 81, 255), anchor='mm') # Icons.add_rounded
    
    # Portfolio Summary & Currency Toggle Box
    k2_x = colB_x + 28 + k1_w + 20
    draw.rounded_rectangle([k2_x, k1_y, k2_x + k1_w, k1_y + 80], radius=10, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw.text((k2_x + 14, k1_y + 10), "스마트 자산 요약 & 통화 토글", font=get_font(9.5, 'bold'), fill=(0, 81, 255))
    draw.text((k2_x + 14, k1_y + 30), "총 투자 원금 ₩ 12,500,000", font=get_font(13.5, 'bold'), fill=(15, 23, 42))
    draw.text((k2_x + 14, k1_y + 54), "평가손익 -₩2,150,000 (-17.2%)", font=get_font(9.5, 'bold'), fill=(255, 82, 82))
    
    # Currency Toggle
    tog_x = k2_x + k1_w - 110
    draw.rounded_rectangle([tog_x, k1_y + 10, tog_x + 95, k1_y + 32], radius=11, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw.rounded_rectangle([tog_x + 2, k1_y + 12, tog_x + 48, k1_y + 30], radius=9, fill=(0, 81, 255))
    draw.text((tog_x + 25, k1_y + 21), "KRW", font=get_font(8, 'bold'), fill=(255, 255, 255), anchor='mm')
    draw.text((tog_x + 72, k1_y + 21), "USD", font=get_font(8, 'medium'), fill=(100, 116, 139), anchor='mm')
    
    # Micro-Component 3: Preset Chips Row
    ch_y = k1_y + 92
    draw.text((colB_x + 28, ch_y + 6), "호가/수량 원터치 프리셋 칩:", font=get_font(10, 'bold'), fill=(100, 116, 139))
    presets = [
        ("+5%", (0, 81, 255), (239, 246, 255)),
        ("+10%", (0, 81, 255), (239, 246, 255)),
        ("-5%", (255, 82, 82), (254, 242, 242)),
        ("-10%", (255, 82, 82), (254, 242, 242)),
        ("+50주", (0, 81, 255), (239, 246, 255)),
        ("+100주", (0, 81, 255), (239, 246, 255)),
        ("전액 매수", (0, 180, 90), (236, 253, 245)),
    ]
    cur_ch_x = colB_x + 185
    for p_txt, p_col, p_bg in presets:
        draw.rounded_rectangle([cur_ch_x, ch_y, cur_ch_x + 82, ch_y + 26], radius=13, fill=p_bg, outline=p_col, width=1)
        draw.text((cur_ch_x + 41, ch_y + 13), p_txt, font=get_font(9.5, 'bold'), fill=p_col, anchor='mm')
        cur_ch_x += 89
        
    # Micro-Component 4: CTAs Button Row (Production Flutter Material Widgets)
    cta_y = ch_y + 38
    mat_font_cta = get_material_icon_font(15)
    
    # 1. Calculate Button
    draw.rounded_rectangle([colB_x + 28, cta_y, colB_x + 230, cta_y + 40], radius=10, fill=(0, 81, 255))
    draw.text((colB_x + 50, cta_y + 20), chr(0xf5fd), font=mat_font_cta, fill=(255, 255, 255), anchor='mm') # Icons.calculate_rounded
    draw.text((colB_x + 138, cta_y + 20), "물타기 계산 실행", font=get_font(11, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # 2. Target Reverse Goal Button
    draw.rounded_rectangle([colB_x + 242, cta_y, colB_x + 432, cta_y + 40], radius=10, fill=(240, 246, 255), outline=(0, 81, 255), width=1)
    draw.text((colB_x + 264, cta_y + 20), chr(0xf0204), font=mat_font_cta, fill=(0, 81, 255), anchor='mm') # Icons.sync_alt_rounded
    draw.text((colB_x + 347, cta_y + 20), "목표 평단가 역산", font=get_font(11, 'bold'), fill=(0, 81, 255), anchor='mm')
    
    # 3. Plan Save Button
    draw.rounded_rectangle([colB_x + 444, cta_y, colB_x + 614, cta_y + 40], radius=10, fill=(248, 250, 252), outline=(203, 213, 225), width=1)
    draw.text((colB_x + 466, cta_y + 20), chr(0xf5ce), font=mat_font_cta, fill=(51, 65, 85), anchor='mm') # Icons.bookmark_added_rounded
    draw.text((colB_x + 538, cta_y + 20), "1-Tap 플랜 저장", font=get_font(10.5, 'bold'), fill=(51, 65, 85), anchor='mm')
    
    # 4. VIP Session Banner
    draw.rounded_rectangle([colB_x + 626, cta_y, colB_x + colB_w - 28, cta_y + 40], radius=10, fill=(254, 243, 199), outline=(253, 230, 138), width=1)
    draw.text((colB_x + 648, cta_y + 20), chr(0xf01d5), font=get_material_icon_font(18), fill=(217, 119, 6), anchor='mm') # Icons.stars_rounded
    draw.text((colB_x + 664 + (colB_w - 28 - 664)//2, cta_y + 12), "VIP 24h 무광고 세션", font=get_font(8.5, 'bold'), fill=(180, 83, 9), anchor='mm')
    draw.text((colB_x + 664 + (colB_w - 28 - 664)//2, cta_y + 26), "남은 시간 23:59:42", font=get_font(8.5, 'bold'), fill=(217, 119, 6), anchor='mm')
    
    # Micro-Component 5: Status Badges Row
    bdg_y = cta_y + 50
    draw.text((colB_x + 28, bdg_y + 6), "상태 뱃지 시스템:", font=get_font(10, 'bold'), fill=(100, 116, 139))
    badges = [
        ("0.2s 음성 도크", "cyan", True),
        ("목표 평단가 역산", "blue", True),
        ("수익 반등 회복", "green", True),
        ("손실 리스크 헤지", "red", True),
        ("100% 온디바이스", "slate", True),
        ("60fps R8 최적화", "purple", False),
    ]
    cur_bx = colB_x + 145
    for b_txt, b_thm, b_dt in badges:
        _, _, b_end, _ = draw_pill_badge(draw, left_x=cur_bx, cy=bdg_y + 14, text=b_txt, font=get_font(9.5, 'bold'), theme=b_thm, has_dot=b_dt, dark_mode=False, pad_x=8, height=24)
        cur_bx = b_end + 8
        
    draw.text((colB_x + 28, r2_y + r2_h - 18), "• Flutter 실제 위젯 트리 1:1 바인딩 (app_colors.dart · simulator_screen.dart · MaterialIcons)", font=get_font(9, 'regular'), fill=(100, 116, 139))
    
    draw_slide_footer(draw, 7)
    base.save(f'{OUT_DIR}/slide_07.png')
    print("SAVED slide_07.png (Visual Identity, App Icon & 24dp Iconography System)")


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
    py = 234
    
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
    c1_y = 234
    c1_h = 145
    draw.rounded_rectangle([rx, c1_y, rx + rw, c1_y + c1_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=rx + 28, cy=c1_y + 30, text="VOICE DOCK · STT PARSER", font=get_font(10, 'bold'), theme='blue', has_dot=True, dark_mode=False, pad_x=10, height=24)
    draw.text((rx + 240, c1_y + 20), "자연어 음성 즉각 인식 & 파라미터 분리", font=get_font(17, 'bold'), fill=(15, 23, 42))
    draw.line([(rx + 28, c1_y + 50), (rx + rw - 28, c1_y + 50)], fill=(241, 245, 249), width=1)
    
    c1_desc = '"삼성전자 7만 원에 50주"라고 말하는 순간, 온디바이스 AI가 종목, 단가, 수량을 자동으로 분리 인식합니다.\n발화 종료와 동시에 시뮬레이터 수치가 즉시 채워져 실시간 호가 변동에 0.2초 만에 즉각 대응합니다.'
    draw.text((rx + 28, c1_y + 64), c1_desc, font=get_font(12.5, 'regular'), fill=(71, 85, 105), spacing=5)
    draw.text((rx + 28, c1_y + 116), "✓ 8자리 소수점 키패드 타이핑 피로도 78% 절감 · 0.2s 음성 STT 파싱 무손실 주입", font=get_font(11, 'bold'), fill=(0, 81, 255))
    
    # CARD 2: Preset Chips Card
    c2_y = 394
    c2_h = 145
    draw.rounded_rectangle([rx, c2_y, rx + rw, c2_y + c2_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=rx + 28, cy=c2_y + 30, text="PRESET CHIPS · 1-TAP HAPTIC", font=get_font(10, 'bold'), theme='cyan', has_dot=True, dark_mode=False, pad_x=10, height=24)
    draw.text((rx + 270, c2_y + 20), "소음 환경을 위한 원터치 호가 프리셋 칩", font=get_font(17, 'bold'), fill=(15, 23, 42))
    draw.line([(rx + 28, c2_y + 50), (rx + rw - 28, c2_y + 50)], fill=(241, 245, 249), width=1)
    
    c2_desc = '음성을 쓰기 어려운 대중교통이나 조용한 환경에서도 ±5%, ±10% 호가 칩과 +50주, +100주 수량 칩으로\n손가락 1-Tap 터치만으로 0.1초 만에 즉시 추가 매수 시나리오를 안전하게 계산합니다.'
    draw.text((rx + 28, c2_y + 64), c2_desc, font=get_font(12.5, 'regular'), fill=(71, 85, 105), spacing=5)
    draw.text((rx + 28, c2_y + 116), "✓ 1-Tap 햅틱 피드백 연동 · 소음 및 무음 환경에서도 완전한 퀀트 시뮬레이션 지원", font=get_font(11, 'bold'), fill=(8, 145, 178))
    
    # CARD 3: Realtime Telemetry & AI Live Parser Card
    c3_y = 554
    c3_h = 416
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
        draw.rounded_rectangle([cx, ch_y, cx + ch_w, ch_y + 92], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((cx + 14, ch_y + 12), label, font=get_font(10.5, 'bold'), fill=(100, 116, 139))
        draw.text((cx + 14, ch_y + 36), val, font=get_num_font(15, 'bold'), fill=c_col)
        draw.text((cx + 14, ch_y + 64), sub_txt, font=get_font(9.5, 'medium'), fill=(71, 85, 105))
        
    # Technical Architecture Audit Footer inside Card 3
    tf_y = ch_y + 106
    draw.rounded_rectangle([rx + 28, tf_y, rx + rw - 28, c3_y + c3_h - 18], radius=10, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
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
    py = 234
    
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
    step_y = 234
    step_h = 475
    draw.rounded_rectangle([rx, step_y, rx + rw, step_y + step_h], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    draw_pill_badge(draw, left_x=rx + 28, cy=step_y + 30, text="VERIFIED WORKFLOW", font=get_font(10, 'bold'), theme='blue', has_dot=True, dark_mode=False, pad_x=10, height=24)
    draw.text((rx + 220, step_y + 20), "2단계 목표 역산 & 리스크 검증 워크플로우", font=get_font(16, 'bold'), fill=(15, 23, 42))
    draw.line([(rx + 28, step_y + 52), (rx + rw - 28, step_y + 52)], fill=(241, 245, 249), width=1)
    
    # 2 Step Phone Mockups side-by-side (19.5:9 Modern Ratio)
    screen_report = Image.open('portfolio/iphone_mockups/iphone_04_report.png').convert('RGBA')
    
    step_pw = 142
    step_ph = int(round(step_pw * (screen_target.height / screen_target.width)))
    m1 = screen_target.resize((step_pw, step_ph), Image.Resampling.LANCZOS)
    m2 = screen_report.resize((step_pw, step_ph), Image.Resampling.LANCZOS)
    
    # Two Balanced Stage Pods (Left: STEP 01, Right: STEP 02) with even LTR layout
    p_w = 326
    p_h = 400
    p_y = step_y + 60
    p1_x = rx + 24
    p2_x = rx + rw - 24 - p_w
    
    # ---------------------------------------------------------
    # LEFT POD: STEP 01 (목표 평단 역산 지정)
    # ---------------------------------------------------------
    draw.rounded_rectangle([p1_x, p_y, p1_x + p_w, p_y + p_h], radius=14, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw_pill_badge(draw, left_x=p1_x + 14, cy=p_y + 20, text="STEP 01", font=get_font(9, 'bold'), theme='slate', has_dot=False, pad_x=8, height=20)
    draw.text((p1_x + 82, p_y + 20), "목표 평단 역산 지정", font=get_font(13.5, 'bold'), fill=(15, 23, 42), anchor='lm')
    draw.line([(p1_x + 14, p_y + 36), (p1_x + p_w - 14, p_y + 36)], fill=(226, 232, 240), width=1)
    
    # Phone 1 Mockup (Left side of Pod 1)
    phone1_x = p1_x + 14
    phone1_y = p_y + 48
    
    # Step 1 Data Column (Right side of Pod 1)
    d1_x = phone1_x + step_pw + 12
    d1_w = p1_x + p_w - 14 - d1_x
    
    draw_pill_badge(draw, left_x=d1_x, cy=p_y + 58, text="CORE QUANT", font=get_font(8.5, 'bold'), theme='blue', pad_x=8, height=20)
    
    # Step 1: 3 Rich Parameter Tiles (No empty void!)
    t1_y = p_y + 74
    t_h = 70
    draw.rounded_rectangle([d1_x, t1_y, d1_x + d1_w, t1_y + t_h], radius=8, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((d1_x + 10, t1_y + 8), "희망 목표가", font=get_font(9.5, 'bold'), fill=(100, 116, 139))
    draw.text((d1_x + 10, t1_y + 26), "₩ 70,000", font=get_font(14, 'bold'), fill=(0, 81, 255))
    draw.text((d1_x + 10, t1_y + 50), "원금 회복 탈출선", font=get_font(8.5, 'medium'), fill=(148, 163, 184))
    
    t2_y = t1_y + t_h + 10
    draw.rounded_rectangle([d1_x, t2_y, d1_x + d1_w, t2_y + t_h], radius=8, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((d1_x + 10, t2_y + 8), "필요 매수량", font=get_font(9.5, 'bold'), fill=(100, 116, 139))
    draw.text((d1_x + 10, t2_y + 26), "+42.5 주", font=get_font(14, 'bold'), fill=(5, 150, 105))
    draw.text((d1_x + 10, t2_y + 50), "0.00% 닫힌 공식", font=get_font(8.5, 'medium'), fill=(16, 185, 129))
    
    t3_y = t2_y + t_h + 10
    draw.rounded_rectangle([d1_x, t3_y, d1_x + d1_w, t3_y + t_h], radius=8, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((d1_x + 10, t3_y + 8), "소요 예수금", font=get_font(9.5, 'bold'), fill=(100, 116, 139))
    draw.text((d1_x + 10, t3_y + 26), "₩ 2,762,500", font=get_font(12.5, 'bold'), fill=(217, 119, 6))
    draw.text((d1_x + 10, t3_y + 50), "가용 자금 내 분할", font=get_font(8.5, 'medium'), fill=(148, 163, 184))
    
    v1_y = t3_y + t_h + 12
    draw_pill_badge(draw, cx=d1_x + d1_w // 2, cy=v1_y + 14, text="✓ 오차율 0.00% 무결성", font=get_font(8.5, 'bold'), theme='green', has_dot=True, pad_x=8, height=28)
    
    # ---------------------------------------------------------
    # RIGHT POD: STEP 02 (리스크 한도 자동 점검)
    # ---------------------------------------------------------
    draw.rounded_rectangle([p2_x, p_y, p2_x + p_w, p_y + p_h], radius=14, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw_pill_badge(draw, left_x=p2_x + 14, cy=p_y + 20, text="STEP 02", font=get_font(9, 'bold'), theme='blue', has_dot=False, pad_x=8, height=20)
    draw.text((p2_x + 82, p_y + 20), "리스크 한도 자동 점검", font=get_font(13.5, 'bold'), fill=(0, 81, 255), anchor='lm')
    draw.line([(p2_x + 14, p_y + 36), (p2_x + p_w - 14, p_y + 36)], fill=(191, 219, 254), width=1)
    
    # Phone 2 Mockup (Left side of Pod 2)
    phone2_x = p2_x + 14
    phone2_y = p_y + 48
    
    # Step 2 Data Column (Right side of Pod 2)
    d2_x = phone2_x + step_pw + 12
    d2_w = p2_x + p_w - 14 - d2_x
    
    draw_pill_badge(draw, left_x=d2_x, cy=p_y + 58, text="SAFETY GUARD", font=get_font(8.5, 'bold'), theme='green', pad_x=8, height=20)
    
    # Step 2: 3 Rich Parameter Tiles (No empty void!)
    draw.rounded_rectangle([d2_x, t1_y, d2_x + d2_w, t1_y + t_h], radius=8, fill=(255, 255, 255), outline=(191, 219, 254), width=1)
    draw.text((d2_x + 10, t1_y + 8), "자산 쏠림도", font=get_font(9.5, 'bold'), fill=(100, 116, 139))
    draw.text((d2_x + 10, t1_y + 26), "42.5 %", font=get_font(14, 'bold'), fill=(0, 81, 255))
    draw.text((d2_x + 10, t1_y + 50), "위험 기준(65%) 이하", font=get_font(8.5, 'medium'), fill=(16, 185, 129))
    
    draw.rounded_rectangle([d2_x, t2_y, d2_x + d2_w, t2_y + t_h], radius=8, fill=(255, 255, 255), outline=(191, 219, 254), width=1)
    draw.text((d2_x + 10, t2_y + 8), "현금 안전 마진", font=get_font(9.5, 'bold'), fill=(100, 116, 139))
    draw.text((d2_x + 10, t2_y + 26), "65.0 %", font=get_font(14, 'bold'), fill=(5, 150, 105))
    draw.text((d2_x + 10, t2_y + 50), "추가 대응 버퍼 보존", font=get_font(8.5, 'medium'), fill=(16, 185, 129))
    
    draw.rounded_rectangle([d2_x, t3_y, d2_x + d2_w, t3_y + t_h], radius=8, fill=(255, 255, 255), outline=(191, 219, 254), width=1)
    draw.text((d2_x + 10, t3_y + 8), "뇌동매매 방어", font=get_font(9.5, 'bold'), fill=(100, 116, 139))
    draw.text((d2_x + 10, t3_y + 26), "가드 엔진 통과", font=get_font(12.5, 'bold'), fill=(15, 23, 42))
    draw.text((d2_x + 10, t3_y + 50), "비정상 주문 원천 차단", font=get_font(8.5, 'medium'), fill=(148, 163, 184))
    
    draw_pill_badge(draw, cx=d2_x + d2_w // 2, cy=v1_y + 14, text="✓ 안전 가이드 적합 판정", font=get_font(8.5, 'bold'), theme='blue', has_dot=True, pad_x=8, height=28)
    
    # Soft Shadows behind both phones
    for sx, simg in [(phone1_x, m1), (phone2_x, m2)]:
        sh = Image.new('RGBA', (W, H), (0,0,0,0))
        shd = ImageDraw.Draw(sh)
        shd.rounded_rectangle([sx + 6, phone1_y + 6, sx + step_pw - 6, phone1_y + step_ph + 6], radius=20, fill=(0, 0, 0, 35))
        sh = sh.filter(ImageFilter.GaussianBlur(12))
        base = Image.alpha_composite(base, sh)
        base.paste(simg, (sx, phone1_y), simg)
        
    draw = ImageDraw.Draw(base)
    
    # Pipeline Connector between Step 1 Pod and Step 2 Pod
    center_cx = (p1_x + p_w + p2_x) // 2
    center_cy = phone1_y + step_ph // 2
    
    # Ambient Glow behind center button
    sh_c = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sh_cd = ImageDraw.Draw(sh_c)
    sh_cd.ellipse([center_cx - 24, center_cy - 24, center_cx + 24, center_cy + 24], fill=(0, 81, 255, 80))
    sh_c = sh_c.filter(ImageFilter.GaussianBlur(10))
    base = Image.alpha_composite(base, sh_c)
    draw = ImageDraw.Draw(base)
    
    # Dotted connection line across the seam
    draw.line([(p1_x + p_w, center_cy), (p2_x, center_cy)], fill=(0, 81, 255), width=2)
    draw.ellipse([center_cx - 16, center_cy - 16, center_cx + 16, center_cy + 16], fill=(0, 81, 255))
    draw.polygon([(center_cx - 4, center_cy - 6), (center_cx + 6, center_cy), (center_cx - 4, center_cy + 6)], fill=(255, 255, 255))
    
    draw_pill_badge(draw, cx=center_cx, cy=center_cy - 28, text="실시간 연동", font=get_font(8, 'bold'), theme='blue', pad_x=6, height=18)
    draw_pill_badge(draw, cx=center_cx, cy=center_cy + 28, text="0ms 무손실", font=get_font(8, 'bold'), theme='slate', pad_x=6, height=18)
    
    # 3-B. Quant Telemetry & Engine Result Card (QUANT ENGINE CARD)
    rep_y = step_y + step_h + 16
    rep_h = 245
    draw.rounded_rectangle([rx, rep_y, rx + rw, rep_y + rep_h], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    draw_pill_badge(draw, left_x=rx + 28, cy=rep_y + 28, text="QUANT ENGINE", font=get_font(10, 'bold'), theme='green', has_dot=True, dark_mode=False, pad_x=10, height=24)
    draw.text((rx + 185, rep_y + 18), "실시간 퀀트 역산 검증 리포트 (Verified Report)", font=get_font(16, 'bold'), fill=(15, 23, 42))
    draw.line([(rx + 28, rep_y + 48), (rx + rw - 28, rep_y + 48)], fill=(241, 245, 249), width=1)
    
    # Solved Banner Box
    sol_y = rep_y + 58
    draw.rounded_rectangle([rx + 28, sol_y, rx + rw - 28, sol_y + 68], radius=12, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
    draw_pill_badge(draw, left_x=rx + 48, cy=sol_y + 22, text="SOLVED 0.00% ERROR", font=get_font(9.5, 'bold'), theme='green', has_dot=True, dark_mode=False, pad_x=8, height=22)
    draw.text((rx + 235, sol_y + 12), "목표 탈출가 ₩70,000 도달을 위해 42.5주 필요", font=get_font(15.5, 'bold'), fill=(0, 81, 255))
    draw.text((rx + 48, sol_y + 44), "100% 로컬 닫힌 형식 퀀트 알고리즘 연산 완료 (연산 오차 0.00% · 실시간 무손실 인계)", font=get_font(10.5, 'regular'), fill=(71, 85, 105))
    
    # 4 Metric Chips
    rep_chips = [
        ("기존 평단 (P_0)", "₩ 78,000", (100, 116, 139)),
        ("목표 평단 (P_target)", "₩ 70,000", (0, 81, 255)),
        ("필요 수량 (Q_add)", "+42.5 주", (0, 180, 90)),
        ("필요 자금 (Total)", "₩ 2,762,500", (217, 119, 6))
    ]
    rc_y = sol_y + 78
    rc_w = (rw - 56 - 36) // 4
    for idx, (label, val, c_col) in enumerate(rep_chips):
        rc_x = rx + 28 + idx * (rc_w + 12)
        draw.rounded_rectangle([rc_x, rc_y, rc_x + rc_w, rc_y + 64], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((rc_x + 14, rc_y + 12), label, font=get_font(9.5, 'bold'), fill=(100, 116, 139))
        draw.text((rc_x + 14, rc_y + 34), val, font=get_num_font(14, 'bold'), fill=c_col)
        
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
    phone_y = 234
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
    
    # TOP DUAL COMPARISON CARDS: BEFORE vs. AFTER (y=234 to 554, h=320)
    card_y = 234
    card_h = 320
    card_w = 840
    
    # Left Card: Traditional Emotional Trading (Before)
    cx1 = 100
    draw.rounded_rectangle([cx1, card_y, cx1 + card_w, card_y + card_h], radius=16, fill=(255, 255, 255), outline=(254, 202, 202), width=1)
    draw.rounded_rectangle([cx1, card_y + 14, cx1 + 5, card_y + card_h - 14], radius=3, fill=(239, 68, 68))
    
    draw_pill_badge(draw, left_x=cx1 + 24, cy=card_y + 24, text="BEFORE : EMOTIONAL TRADING", font=get_font(9.5, 'bold'), theme='red', has_dot=True, pad_x=10, height=22)
    draw.text((cx1 + 24, card_y + 50), "감정에 치우친 뇌동매매와 자금 고갈", font=get_font(18, 'bold'), fill=(15, 23, 42))
    draw.text((cx1 + 24, card_y + 76), "계획 없는 추가 매수로 예수금이 조기 소진되고 패닉셀 손절 유발", font=get_font(12, 'regular'), fill=(100, 116, 139))
    
    b_rows = [
        ("초기 투자 포지션", "100주 · 매입가 ₩78,000 (총 투자 ₩7,800,000)", (15, 23, 42)),
        ("현재가 및 평가 손실", "₩65,000 · 손실률 -16.67% (계좌 평가손 ₩-1,300,000)", (220, 38, 38)),
        ("원금 회복 필요 반등률", "+20.00% 급반등 필요 (전고점 탈출 심리적 부담 극대화)", (220, 38, 38)),
        ("예수금 소진 및 결과", "자금 소진율 92.4% (초기 몰빵으로 추가 방어 불가, 비자발적 손절)", (180, 83, 9))
    ]
    ry = card_y + 104
    for label, val, val_col in b_rows:
        draw.rounded_rectangle([cx1 + 24, ry, cx1 + card_w - 24, ry + 44], radius=8, fill=(254, 242, 242), outline=(254, 202, 202), width=1)
        draw.text((cx1 + 38, ry + 22), label, font=get_font(11.5, 'bold'), fill=(100, 116, 139), anchor='lm')
        draw.text((cx1 + 210, ry + 22), val, font=get_font(12, 'bold'), fill=val_col, anchor='lm')
        ry += 50
        
    # Right Card: Smart Quant DCA Inversion (After)
    cx2 = 980
    draw.rounded_rectangle([cx2, card_y, cx2 + card_w, card_y + card_h], radius=16, fill=(255, 255, 255), outline=(191, 219, 254), width=1)
    draw.rounded_rectangle([cx2, card_y + 14, cx2 + 5, card_y + card_h - 14], radius=3, fill=(0, 82, 255))
    
    draw_pill_badge(draw, left_x=cx2 + 24, cy=card_y + 24, text="AFTER : SMART DCA INVERSION", font=get_font(9.5, 'bold'), theme='blue', has_dot=True, pad_x=10, height=22)
    draw.text((cx2 + 24, card_y + 50), "스마트 퀀트 역산과 안전 유동성 방어", font=get_font(18, 'bold'), fill=(15, 23, 42))
    draw.text((cx2 + 24, card_y + 76), "희망 탈출 가격에 맞춘 정량 분할 매수로 계좌와 심리적 안정성 동시 확보", font=get_font(12, 'regular'), fill=(100, 116, 139))
    
    a_rows = [
        ("정량 최적 매수 집행", "+38주 분할 매수 · 소요 자금 ₩2,470,000 (무지연 0.00% 역산)", (0, 82, 255)),
        ("방어 후 신규 평균단가", "₩74,420 (손실률 -12.65%로 +4.02%p 계좌 즉각 방어)", (5, 150, 105)),
        ("원금 회복 필요 반등률", "+7.69% 반등 시 본전 탈출 (회복 부담 61.5% 대폭 경감)", (5, 150, 105)),
        ("예수금 보존 및 안전 마진", "현금 보존율 65.0% 유지 (추가 지지선 대응 여력 및 심리적 확신)", (180, 83, 9))
    ]
    ry = card_y + 104
    for label, val, val_col in a_rows:
        draw.rounded_rectangle([cx2 + 24, ry, cx2 + card_w - 24, ry + 44], radius=8, fill=(240, 246, 255), outline=(191, 219, 254), width=1)
        draw.text((cx2 + 38, ry + 22), label, font=get_font(11.5, 'bold'), fill=(100, 116, 139), anchor='lm')
        draw.text((cx2 + 210, ry + 22), val, font=get_font(12, 'bold'), fill=val_col, anchor='lm')
        ry += 50
        
    # MIDDLE 4 TELEMETRY METRICS CARDS (y=572 to 717, h=145)
    m_y = 572
    m_h = 145
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
        draw_pill_badge(draw, left_x=tx + 18, cy=m_y + 20, text=badge, font=get_font(9, 'bold'), theme=theme_key, has_dot=True, pad_x=8, height=20)
        draw.text((tx + 18, m_y + 46), val, font=get_num_font(30, 'black'), fill=(15, 23, 42))
        draw.text((tx + 18, m_y + 86), title, font=get_font(13, 'bold'), fill=(15, 23, 42))
        draw.text((tx + 18, m_y + 110), desc, font=get_font(10.5, 'regular'), fill=(100, 116, 139))
        tx += m_w + m_gap
        
    # BOTTOM 3 STRATEGIC RETROSPECTIVE & ROADMAP CARDS (y=735 to 970, h=235)
    b_y = 735
    b_h = 235
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
        draw.text((bx + 20, b_y + 50), title, font=get_font(14, 'bold'), fill=(15, 23, 42))
        draw.text((bx + 20, b_y + 72), sub, font=get_font(11, 'bold'), fill=col)
        draw.line([(bx + 20, b_y + 92), (bx + b_w - 20, b_y + 92)], fill=(241, 245, 249), width=1)
        
        py = b_y + 100
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
        ph_back = 570
        pw_back = int(round(ph_back * (im_voice.width / im_voice.height)))
        im_voice = im_voice.resize((pw_back, ph_back), Image.Resampling.LANCZOS)
        
        im_target = Image.open(phone_target_path).convert('RGBA')
        ph_front = 610
        pw_front = int(round(ph_front * (im_target.width / im_target.height)))
        im_target = im_target.resize((pw_front, ph_front), Image.Resampling.LANCZOS)
        
        # Gorgeous Neon Glow & Shadows on Dark Background
        sh = Image.new('RGBA', (W, H), (0,0,0,0))
        shd = ImageDraw.Draw(sh)
        shd.ellipse([110, 230, 130 + pw_back + 40, 254 + ph_back + 30], fill=(0, 60, 180, 50))
        shd.rounded_rectangle([130 + 10, 254 + 15, 130 + pw_back - 10, 254 + ph_back + 20], radius=32, fill=(0, 0, 0, 140))
        sh = sh.filter(ImageFilter.GaussianBlur(24))
        base = Image.alpha_composite(base, sh)
        base.paste(im_voice, (130, 254), im_voice)
        
        # Front phone glow
        sh2 = Image.new('RGBA', (W, H), (0,0,0,0))
        shd2 = ImageDraw.Draw(sh2)
        shd2.ellipse([340 - 30, 234 + ph_front - 40, 340 + pw_front + 30, 234 + ph_front + 50], fill=(0, 110, 255, 90))
        shd2.rounded_rectangle([340 + 12, 234 + 16, 340 + pw_front - 12, 234 + ph_front + 24], radius=36, fill=(0, 0, 0, 180))
        sh2 = sh2.filter(ImageFilter.GaussianBlur(28))
        base = Image.alpha_composite(base, sh2)
        base.paste(im_target, (340, 234), im_target)
        
        draw = ImageDraw.Draw(base)
    
    # Left Bottom Spec Strip (x=100, y=856, w=660, h=124) - Dark Glass Card
    draw.rounded_rectangle([100, 856, 760, 980], radius=14, fill=(17, 24, 39, 255), outline=(40, 53, 72), width=1)
    draw_pill_badge(draw, left_x=120, cy=880, text="FLUTTER WEB PRODUCTION ENGINE", font=get_font(9, 'bold'), theme='blue', dark_mode=True, pad_x=8, height=20)
    draw.text((120, 908), "• 60fps Native Web CanvasKit / SkWasm 렌더링 파이프라인 탑재", font=get_font(11, 'medium'), fill=(203, 213, 225))
    draw.text((120, 930), "• 100% 온디바이스 퀀트 대수 역산 엔진 (외부 금융 API 무전송 보안)", font=get_font(11, 'medium'), fill=(203, 213, 225))
    draw.text((120, 952), "• 반응형 모바일 뷰포트 시뮬레이터 & URL 딥링크 상태 복원 완벽 지원", font=get_font(11, 'medium'), fill=(56, 189, 248))
    
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
    # 1. PRIMARY HERO (TOP): MASTER LAUNCHER with Iconic Blue Gradient (y=234 to 348, h=114)
    # ---------------------------------------------------------
    my = 234
    mh = 114
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
    draw.rounded_rectangle([rx + 24, my + 14, rx + 24 + badge_w, my + 35], radius=10, fill=(0, 36, 110, 190), outline=(255, 255, 255, 180), width=1)
    draw.text((rx + 24 + badge_w // 2, my + 24), "MASTER LAUNCHER", font=get_font(9, 'bold'), fill=(255, 255, 255), anchor='mm')
    
    # Hero White Headline
    draw.text((rx + 24, my + 57), "모바일 목업 디바이스에서 전체 플로우 직접 실행하기 ↗", font=get_font(18, 'extrabold'), fill=(255, 255, 255), anchor='lm')
    # Hero Subtitle
    draw.text((rx + 24, my + 87), "0.2초 음성 도크부터 목표 역산 엔진까지, 4대 핵심 여정을 실물 뷰포트에서 한 번에 체험하세요.", font=get_font(12, 'medium'), fill=(225, 242, 255), anchor='lm')
    
    # Large High-Contrast Pure White CTA Button
    btn_w = 210
    btn_h = 48
    btn_rx = rx + rw - btn_w - 24
    btn_ry = my + (mh - btn_h) // 2
    
    # Button soft drop shadow
    sh_btn = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sh_btn_d = ImageDraw.Draw(sh_btn)
    sh_btn_d.rounded_rectangle([btn_rx - 2, btn_ry + 2, btn_rx + btn_w + 2, btn_ry + btn_h + 8], radius=24, fill=(0, 40, 120, 100))
    sh_btn = sh_btn.filter(ImageFilter.GaussianBlur(8))
    base = Image.alpha_composite(base, sh_btn)
    draw = ImageDraw.Draw(base)
    
    # Pure white button with electric blue text
    draw.rounded_rectangle([btn_rx, btn_ry, btn_rx + btn_w, btn_ry + btn_h], radius=24, fill=(255, 255, 255))
    draw.text((btn_rx + btn_w // 2, btn_ry + btn_h // 2), "RUN PROTOTYPE ↗", font=get_font(13.5, 'bold'), fill=(0, 82, 255), anchor='mm')
    
    # ---------------------------------------------------------
    # 2. 4 SUBDUED STEP CARDS (y=358 to 678, h=74, sgap=8)
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
    
    sy = 358
    sh_h = 74
    sgap = 8
    step_boxes = []
    
    for badge, title, desc, url in steps:
        box_rect = [rx, sy, rx + rw, sy + sh_h]
        step_boxes.append((box_rect, url))
        
        # Subdued Dark Glass Box (No bright stripes)
        draw.rounded_rectangle(box_rect, radius=12, fill=(15, 20, 32, 230), outline=(32, 42, 58), width=1)
        
        # Muted Dark Slate Badge (Uniform and quiet)
        draw_pill_badge(draw, left_x=rx + 18, cy=sy + 22, text=badge, font=get_font(9, 'bold'), theme='slate', dark_mode=True, has_dot=False, pad_x=8, height=20)
        draw.text((rx + 90, sy + 22), title, font=get_font(13.5, 'bold'), fill=(226, 232, 240), anchor='lm')
        draw.text((rx + 18, sy + 52), desc, font=get_font(11, 'regular'), fill=(105, 120, 140), anchor='lm')
        
        # Right Click Button - Subtle Ghost Outline Pill (Secondary)
        btn_x = rx + rw - 120
        draw_pill_badge(draw, cx=btn_x + 45, cy=sy + 37, text="바로가기 ↗", font=get_font(10.5, 'bold'), theme='slate', dark_mode=True, has_dot=False, pad_x=12, height=28)
        
        sy += sh_h + sgap
        
    # ---------------------------------------------------------
    # 3. TERTIARY: Subtle, Un-emphasized Guide Hint
    # ---------------------------------------------------------
    draw.text((rx + 4, 696), "TIP · 특정 단계만 개별 테스트하거나, 모바일 실물 기기에서는 아래 QR 코드를 카메라로 스캔하세요.", font=get_font(11.5, 'regular'), fill=(115, 130, 150), anchor='lm')
    
    # ---------------------------------------------------------
    # 4. SUPPORTING: Dark QR Code & Hyperlink Area (y=716 to 970, h=254)
    # ---------------------------------------------------------
    qy = 716
    qh = 254
    draw.rounded_rectangle([rx, qy, rx + rw, qy + qh], radius=14, fill=(14, 19, 30, 255), outline=(32, 42, 58), width=1)
    
    draw_pill_badge(draw, left_x=rx + 24, cy=qy + 28, text="HYPERLINK & MOBILE QR SCAN", font=get_font(9, 'bold'), theme='slate', has_dot=True, dark_mode=True, pad_x=8, height=20)
    draw.text((rx + 24, qy + 64), "• PDF 원클릭 하이퍼링크 : PDF 뷰어에서 각 카드나 버튼 클릭 시 반응형 프로토타입 즉시 실행", font=get_font(11.5, 'medium'), fill=(180, 195, 215))
    draw.text((rx + 24, qy + 94), "• 스마트폰 실물 QR 스캔 : 스마트폰 기본 카메라로 우측 QR 코드 스캔 시 모바일 전용 뷰 작동", font=get_font(11.5, 'medium'), fill=(180, 195, 215))
    draw.text((rx + 24, qy + 124), "• GitHub Pages 상시 배포 : 전 세계 어디서든 무설치로 60fps 플러터 엔진 즉각 체험 가능", font=get_font(11.5, 'medium'), fill=(56, 189, 248))
    draw.text((rx + 24, qy + 160), f"Live Web : {proto_entry_url}", font=get_num_font(11, 'bold'), fill=(130, 145, 170))
    
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
    
    draw.rounded_rectangle([qr_x - 8, qr_y - 6, qr_x + qr_size + 8, qr_y + qr_size + 28], radius=10, fill=(255, 255, 255))
    base.paste(qr_img, (qr_x, qr_y), qr_img)
    draw.text((qr_x + qr_size // 2, qr_y + qr_size + 10), "SCAN FOR MOBILE TEST", font=get_font(8.5, 'bold'), fill=(11, 15, 23), anchor='mm')
    
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
