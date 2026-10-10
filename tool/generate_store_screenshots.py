import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_rounded_mask(size, radius):
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), size], radius=radius, fill=255)
    return mask

def draw_vertical_gradient(draw, width, height, top_color, bottom_color):
    # Generates a smooth vertical linear gradient
    for y in range(height):
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * (y / height))
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * (y / height))
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

def draw_soft_glow(image, center_x, center_y, radius, color):
    # Radial glow overlay
    glow = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)
    steps = 15
    for i in range(steps, 0, -1):
        cur_radius = int(radius * (i / steps))
        alpha = int(color[3] * ((steps - i + 1) / steps) * 0.4)
        draw.ellipse([
            center_x - cur_radius, center_y - cur_radius,
            center_x + cur_radius, center_y + cur_radius
        ], fill=(color[0], color[1], color[2], alpha))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=radius // 4))
    image.paste(glow, (0, 0), glow)

def render_store_screenshot(config, out_path):
    W, H = config['size']
    scale = W / 1080.0
    
    # Base Canvas with subtle gradient
    base = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(base)
    draw_vertical_gradient(draw, W, H, config['grad_top'], config['grad_bottom'])
    
    # Atmospheric glows
    draw_soft_glow(base, int(W * 0.2), int(H * 0.15), int(280 * scale), config['accent_glow'])
    draw_soft_glow(base, int(W * 0.8), int(H * 0.75), int(320 * scale), (30, 60, 120, 60))
    
    # Convert base to RGBA
    canvas = base.convert('RGBA')
    draw = ImageDraw.Draw(canvas)
    
    # Fonts
    font_bold_path = "C:\\Windows\\Fonts\\malgunbd.ttf"
    font_reg_path = "C:\\Windows\\Fonts\\malgun.ttf"
    if not os.path.exists(font_bold_path):
        font_bold_path = "C:\\Windows\\Fonts\\arialbd.ttf"
        font_reg_path = "C:\\Windows\\Fonts\\arial.ttf"
        
    title_size = int(60 * scale)
    subtitle_size = int(32 * scale)
    badge_size = int(24 * scale)
    
    title_font = ImageFont.truetype(font_bold_path, title_size)
    sub_font = ImageFont.truetype(font_reg_path, subtitle_size)
    badge_font = ImageFont.truetype(font_bold_path, badge_size)
    
    # 1. Category / Feature Badge (Top)
    badge_text = config['badge']
    b_bbox = badge_font.getbbox(badge_text)
    bw = b_bbox[2] - b_bbox[0]
    bh = b_bbox[3] - b_bbox[1]
    
    badge_pad_x = int(24 * scale)
    badge_pad_y = int(10 * scale)
    badge_w = bw + badge_pad_x * 2
    badge_h = bh + badge_pad_y * 2
    badge_x = (W - badge_w) // 2
    badge_y = int(70 * scale)
    
    # Badge background pill
    draw.rounded_rectangle(
        [(badge_x, badge_y), (badge_x + badge_w, badge_y + badge_h)],
        radius=int(badge_h // 2),
        fill=config['badge_bg'],
        outline=config['badge_border'],
        width=int(2 * scale)
    )
    # Badge text
    draw.text((badge_x + badge_pad_x, badge_y + badge_pad_y - int(2*scale)), badge_text, font=badge_font, fill=config['badge_text_color'])
    
    # 2. Main Title (Two lines or single line)
    title_y = badge_y + badge_h + int(32 * scale)
    for line in config['title']:
        t_bbox = title_font.getbbox(line)
        tw = t_bbox[2] - t_bbox[0]
        tx = (W - tw) // 2
        draw.text((tx, title_y), line, font=title_font, fill=(255, 255, 255, 255))
        title_y += int(title_size * 1.28)
        
    # 3. Subtitle / Global Tag
    sub_y = title_y + int(8 * scale)
    s_bbox = sub_font.getbbox(config['subtitle'])
    sw = s_bbox[2] - s_bbox[0]
    sx = (W - sw) // 2
    draw.text((sx, sub_y), config['subtitle'], font=sub_font, fill=(185, 205, 235, 230))
    
    # 4. Device Mockup Frame & Screen Placement
    screen_img = Image.open(config['screen']).convert('RGBA')
    
    # Target frame sizing
    frame_w = int(W * config['frame_w_ratio'])
    aspect = screen_img.height / screen_img.width
    frame_h = int(frame_w * aspect)
    
    # Sizing down to fit canvas bottom nicely
    device_top = sub_y + int(50 * scale)
    max_h = H - device_top + int(120 * scale) # bleed slightly at the bottom for modern look
    if frame_h > max_h:
        frame_h = max_h
        frame_w = int(frame_h / aspect)
        
    device_x = (W - frame_w) // 2
    device_y = device_top
    
    # Resize screen
    screen_resized = screen_img.resize((frame_w, frame_h), Image.Resampling.LANCZOS)
    
    # Rounded corners for screen
    corner_radius = int(36 * scale)
    mask = create_rounded_mask((frame_w, frame_h), corner_radius)
    
    # Outer device bezel/shadow layer
    shadow_pad = int(45 * scale)
    shadow_img = Image.new('RGBA', (frame_w + shadow_pad * 2, frame_h + shadow_pad * 2), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_img)
    s_draw.rounded_rectangle(
        [(shadow_pad, shadow_pad), (shadow_pad + frame_w, shadow_pad + frame_h)],
        radius=corner_radius,
        fill=(0, 0, 0, 180)
    )
    shadow_blurred = shadow_img.filter(ImageFilter.GaussianBlur(radius=int(28 * scale)))
    canvas.paste(shadow_blurred, (device_x - shadow_pad, device_y - shadow_pad + int(15 * scale)), shadow_blurred)
    
    # Bezel border line
    bezel_pad = int(8 * scale)
    bezel = Image.new('RGBA', (frame_w + bezel_pad * 2, frame_h + bezel_pad * 2), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(bezel)
    b_draw.rounded_rectangle(
        [(0, 0), (frame_w + bezel_pad * 2, frame_h + bezel_pad * 2)],
        radius=corner_radius + bezel_pad,
        fill=(18, 24, 38, 255),
        outline=(55, 75, 115, 220),
        width=int(3 * scale)
    )
    canvas.paste(bezel, (device_x - bezel_pad, device_y - bezel_pad), bezel)
    
    # Paste actual screen inside
    canvas.paste(screen_resized, (device_x, device_y), mask)
    
    # Save final PNG
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    canvas.convert('RGB').save(out_path, format='PNG', quality=95)
    print(f"Generated: {out_path} ({W}x{H})")

def main():
    root = r"d:\097.flutter_project\average_down_calculator"
    brain = r"C:\Users\coyot\.gemini\antigravity-ide\brain\11b28641-b715-459c-b556-fc7ec3944b3f"
    brain_temp = os.path.join(brain, ".tempmediaStorage")
    
    screens = {
        'home': os.path.join(brain, "raw_screen_app.png"),
        'sim': os.path.join(brain, "sim_filled_real.png"),
        'target': os.path.join(brain_temp, "sim_target_tapped.png"),
        'portfolio': os.path.join(brain_temp, "portfolio_screen.png"),
        'lang': os.path.join(brain, "lang_dropdown.png"),
    }
    
    targets = [
        ('phone', (1080, 1920), 0.82),
        ('tablet_7inch', (1200, 1920), 0.74),
        ('tablet_10inch', (1600, 2560), 0.70)
    ]
    
    pages = [
        {
            'id': '01_smart_portfolio',
            'screen': screens['home'],
            'badge': 'ALL-IN-ONE PORTFOLIO',
            'title': ['실시간 자산 & 물타기', '통합 포트폴리오 관리'],
            'subtitle': '주식·코인 전 종목 실시간 수익률 & 평단가 한눈에',
            'grad_top': (10, 18, 38),
            'grad_bottom': (5, 9, 20),
            'accent_glow': (20, 100, 255, 90),
            'badge_bg': (18, 48, 100, 220),
            'badge_border': (45, 120, 255, 255),
            'badge_text_color': (140, 200, 255, 255)
        },
        {
            'id': '02_dca_simulator',
            'screen': screens['sim'],
            'badge': 'SMART DCA SIMULATOR',
            'title': ['3단계 정밀 물타기', '평단가 즉시 시뮬레이션'],
            'subtitle': '추가 매수 시 변화하는 최종 평단가와 투자금 완벽 계산',
            'grad_top': (14, 25, 45),
            'grad_bottom': (6, 12, 24),
            'accent_glow': (0, 200, 160, 80),
            'badge_bg': (15, 60, 60, 220),
            'badge_border': (0, 210, 170, 255),
            'badge_text_color': (120, 255, 220, 255)
        },
        {
            'id': '03_target_calculator',
            'screen': screens['target'],
            'badge': 'TARGET PRICE PLANNER',
            'title': ['목표 평단가 도달', '역산 플래너 솔루션'],
            'subtitle': '탈출 희망 평단가 입력 시 필요한 매수 수량과 금액 자동 산출',
            'grad_top': (25, 16, 42),
            'grad_bottom': (12, 8, 22),
            'accent_glow': (180, 80, 255, 80),
            'badge_bg': (60, 25, 90, 220),
            'badge_border': (190, 90, 255, 255),
            'badge_text_color': (230, 180, 255, 255)
        },
        {
            'id': '04_detailed_report',
            'screen': screens['portfolio'],
            'badge': 'AI ANALYSIS & REPORT',
            'title': ['상세 자산 배분 리포트', '& 인공지능 매매 플랜'],
            'subtitle': '비중 분석부터 기대 탈출 시나리오까지 완벽한 투자 가이드',
            'grad_top': (15, 28, 52),
            'grad_bottom': (7, 14, 26),
            'accent_glow': (255, 160, 30, 80),
            'badge_bg': (70, 45, 15, 220),
            'badge_border': (255, 175, 40, 255),
            'badge_text_color': (255, 215, 140, 255)
        },
        {
            'id': '05_global_multi_language',
            'screen': screens['lang'],
            'badge': 'GLOBAL 7 LANGUAGES & OFFLINE',
            'title': ['글로벌 7개국 통화·언어 지원', '& 100% 오프라인 안심 보안'],
            'subtitle': 'KRW · USD · JPY · EUR | 서버 전송 없는 완벽한 개인정보 보호',
            'grad_top': (12, 22, 40),
            'grad_bottom': (6, 10, 20),
            'accent_glow': (50, 150, 255, 85),
            'badge_bg': (20, 50, 95, 220),
            'badge_border': (70, 160, 255, 255),
            'badge_text_color': (160, 220, 255, 255)
        }
    ]
    
    for device_name, size, ratio in targets:
        for idx, page in enumerate(pages, 1):
            cfg = dict(page)
            cfg['size'] = size
            cfg['frame_w_ratio'] = ratio
            out_dir = os.path.join(root, "store", "screenshots", device_name)
            out_file = os.path.join(out_dir, f"{page['id']}.png")
            render_store_screenshot(cfg, out_file)

if __name__ == '__main__':
    main()
