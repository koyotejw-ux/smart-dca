# -*- coding: utf-8 -*-
import os
import math
from PIL import Image, ImageDraw, ImageFilter

def create_textless_feature_graphic():
    root = r"d:\097.flutter_project\average_down_calculator"
    store_dir = os.path.join(root, "store")
    os.makedirs(store_dir, exist_ok=True)
    
    W, H = 1024, 500
    
    # 1. Base Gradient Canvas (Deep Quant Midnight Navy)
    base = Image.new('RGBA', (W, H), (6, 11, 24, 255))
    draw_base = ImageDraw.Draw(base)
    
    for y in range(H):
        t = y / float(H)
        # Deep blue-black vertical gradient
        r = int(10 * (1 - t) + 2 * t)
        g = int(22 * (1 - t) + 5 * t)
        b = int(45 * (1 - t) + 16 * t)
        draw_base.line([(0, y), (W, y)], fill=(r, g, b, 255))
        
    # 2. Subtle Financial Terminal Grid (Mathematical / Quant Aesthetic)
    grid = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(grid)
    grid_spacing = 40
    for x in range(0, W, grid_spacing):
        g_draw.line([(x, 0), (x, H)], fill=(30, 60, 110, 18), width=1)
    for y in range(0, H, grid_spacing):
        g_draw.line([(0, y), (W, y)], fill=(30, 60, 110, 18), width=1)
    base = Image.alpha_composite(base, grid)
    
    # 3. Volumetric Atmospheric Glows
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    
    # Large Cyan & Electric Blue central aura
    glow_draw.ellipse([W//2 - 260, H//2 - 220, W//2 + 260, H//2 + 220], fill=(0, 160, 255, 75))
    glow_draw.ellipse([W//2 - 140, H//2 - 120, W//2 + 140, H//2 + 120], fill=(0, 230, 255, 90))
    
    # Ambient side glows
    glow_draw.ellipse([60, 120, 380, 440], fill=(16, 185, 129, 35))     # Emerald recovery accent (left)
    glow_draw.ellipse([W - 420, 60, W - 60, 420], fill=(79, 70, 229, 50))  # Royal indigo accent (right)
    
    glow = glow.filter(ImageFilter.GaussianBlur(65))
    base = Image.alpha_composite(base, glow)
    
    # 4. Dynamic Ascending Financial Neon Wave (Mathematical Breakeven Trend)
    wave = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    w_draw = ImageDraw.Draw(wave)
    
    # Compute smooth cubic curve points from bottom-left to top-right
    points = []
    num_steps = 100
    for i in range(num_steps + 1):
        t = i / float(num_steps)
        # S-curve ease-in-out representing DCA recovery
        px = t * W
        # Base wave: starts at y=360, dips slightly, then surges up to y=110
        py = 360 - 240 * (t ** 1.8) + 25 * math.sin(t * math.pi * 2.5)
        points.append((px, py))
        
    # Draw glow line (thick, soft)
    for i in range(len(points) - 1):
        w_draw.line([points[i], points[i+1]], fill=(0, 170, 255, 60), width=12)
    wave_blur = wave.filter(ImageFilter.GaussianBlur(8))
    base = Image.alpha_composite(base, wave_blur)
    
    # Draw sharp neon core line
    wave_core = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    wc_draw = ImageDraw.Draw(wave_core)
    for i in range(len(points) - 1):
        wc_draw.line([points[i], points[i+1]], fill=(0, 240, 255, 230), width=3)
    base = Image.alpha_composite(base, wave_core)
    
    # Milestone pulsing nodes along the curve
    node_indices = [20, 50, 80, 96]
    for idx in node_indices:
        nx, ny = points[idx]
        node_glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ng_draw = ImageDraw.Draw(node_glow)
        ng_draw.ellipse([nx - 14, ny - 14, nx + 14, ny + 14], fill=(0, 230, 255, 120))
        node_glow = node_glow.filter(ImageFilter.GaussianBlur(5))
        base = Image.alpha_composite(base, node_glow)
        
        node_core = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        nc_draw = ImageDraw.Draw(node_core)
        nc_draw.ellipse([nx - 5, ny - 5, nx + 5, ny + 5], fill=(255, 255, 255, 255))
        base = Image.alpha_composite(base, node_core)
        
    # 5. Floating Glass Cards (Left: Mini Candlestick Card, Right: Circular Gauge Card) - 100% TEXTLESS!
    # Left Card: Abstract Candlestick & Bar Graphic
    card_l_w, card_l_h = 210, 150
    cl_x, cl_y = 100, (H - card_l_h) // 2 + 10
    
    card_l = Image.new('RGBA', (card_l_w, card_l_h), (0, 0, 0, 0))
    cl_draw = ImageDraw.Draw(card_l)
    # Glass background
    cl_draw.rounded_rectangle([0, 0, card_l_w, card_l_h], radius=20, fill=(13, 27, 56, 190), outline=(0, 180, 255, 100), width=1)
    
    # Draw purely visual financial bars & candles (no text)
    bar_data = [
        (30, 85, 45, (239, 68, 68, 200)),    # red drop
        (65, 95, 60, (239, 68, 68, 200)),    # red drop
        (100, 70, 40, (16, 185, 129, 220)),  # green recovery
        (135, 55, 55, (16, 185, 129, 230)),  # green surge
        (170, 35, 75, (0, 220, 255, 255)),   # cyan target breakout
    ]
    for bx, by, bh, bcolor in bar_data:
        # candle wick
        cl_draw.line([(bx + 8, by - 12), (bx + 8, by + bh + 12)], fill=bcolor, width=2)
        # candle body
        cl_draw.rounded_rectangle([bx, by, bx + 16, by + bh], radius=4, fill=bcolor)
        
    # Card shadow
    cl_shadow = Image.new('RGBA', (card_l_w + 40, card_l_h + 40), (0, 0, 0, 0))
    cls_draw = ImageDraw.Draw(cl_shadow)
    cls_draw.rounded_rectangle([20, 20, card_l_w + 20, card_l_h + 20], radius=20, fill=(0, 0, 0, 110))
    cl_shadow = cl_shadow.filter(ImageFilter.GaussianBlur(18))
    
    base.paste(cl_shadow, (cl_x - 20, cl_y - 15), cl_shadow)
    base.paste(card_l, (cl_x, cl_y), card_l)
    
    # Right Card: Abstract Circular Target Dial / Precision Gauge (no text)
    card_r_w, card_r_h = 210, 150
    cr_x, cr_y = W - card_r_w - 100, (H - card_r_h) // 2 + 10
    
    card_r = Image.new('RGBA', (card_r_w, card_r_h), (0, 0, 0, 0))
    cr_draw = ImageDraw.Draw(card_r)
    cr_draw.rounded_rectangle([0, 0, card_r_w, card_r_h], radius=20, fill=(13, 27, 56, 190), outline=(0, 180, 255, 100), width=1)
    
    # Arc / Gauge in center of right card
    cx_g, cy_g = card_r_w // 2, card_r_h // 2
    r_g = 42
    # Background ring
    cr_draw.arc([cx_g - r_g, cy_g - r_g, cx_g + r_g, cy_g + r_g], start=135, end=405, fill=(30, 58, 100, 180), width=8)
    # Active glowing green-cyan arc
    cr_draw.arc([cx_g - r_g, cy_g - r_g, cx_g + r_g, cy_g + r_g], start=135, end=340, fill=(0, 230, 255, 255), width=8)
    # Target bullseye center
    cr_draw.ellipse([cx_g - 14, cy_g - 14, cx_g + 14, cy_g + 14], fill=(16, 185, 129, 240), outline=(255, 255, 255, 255), width=2)
    cr_draw.ellipse([cx_g - 4, cy_g - 4, cx_g + 4, cy_g + 4], fill=(255, 255, 255, 255))
    
    # Card shadow
    cr_shadow = Image.new('RGBA', (card_r_w + 40, card_r_h + 40), (0, 0, 0, 0))
    crs_draw = ImageDraw.Draw(cr_shadow)
    crs_draw.rounded_rectangle([20, 20, card_r_w + 20, card_r_h + 20], radius=20, fill=(0, 0, 0, 110))
    cr_shadow = cr_shadow.filter(ImageFilter.GaussianBlur(18))
    
    base.paste(cr_shadow, (cr_x - 20, cr_y - 15), cr_shadow)
    base.paste(card_r, (cr_x, cr_y), card_r)
    
    # 6. Hero Center: 3D Squircle App Icon (290x290)
    icon_src = os.path.join(root, "assets", "app_icon_clean_squircle.png")
    if not os.path.exists(icon_src):
        icon_src = os.path.join(root, "assets", "app_icon.png")
        
    icon_im = Image.open(icon_src).convert('RGBA')
    icon_size = 290
    hero_x = (W - icon_size) // 2
    hero_y = (H - icon_size) // 2 - 4
    
    # Multi-tier realistic soft drop shadow under hero icon
    hero_shadow = Image.new('RGBA', (icon_size + 60, icon_size + 60), (0, 0, 0, 0))
    hs_draw = ImageDraw.Draw(hero_shadow)
    hs_draw.rounded_rectangle([30, 30, icon_size + 30, icon_size + 30], radius=68, fill=(0, 0, 0, 160))
    hero_shadow = hero_shadow.filter(ImageFilter.GaussianBlur(24))
    base.paste(hero_shadow, (hero_x - 30, hero_y - 14), hero_shadow)
    
    # Center ambient rim glow directly behind icon
    rim_glow = Image.new('RGBA', (icon_size + 40, icon_size + 40), (0, 0, 0, 0))
    rg_draw = ImageDraw.Draw(rim_glow)
    rg_draw.rounded_rectangle([15, 15, icon_size + 25, icon_size + 25], radius=68, fill=(0, 215, 255, 120))
    rim_glow = rim_glow.filter(ImageFilter.GaussianBlur(14))
    base.paste(rim_glow, (hero_x - 20, hero_y - 15), rim_glow)
    
    # Paste resized hero squircle
    hero_sq = icon_im.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
    base.paste(hero_sq, (hero_x, hero_y), hero_sq)
    
    # 7. Ambient Particle Sparkles (Subtle floating diamond stars ✦ without text)
    sparkles = [
        (hero_x - 50, hero_y + 30, 8, (0, 220, 255, 200)),
        (hero_x + icon_size + 45, hero_y + 60, 10, (16, 185, 129, 210)),
        (hero_x - 30, hero_y + icon_size - 30, 6, (255, 255, 255, 180)),
        (hero_x + icon_size + 30, hero_y + icon_size - 50, 7, (0, 200, 255, 190)),
        (cl_x + 30, cl_y - 25, 6, (0, 210, 255, 160)),
        (cr_x + card_r_w - 30, cr_y - 20, 8, (16, 185, 129, 180)),
    ]
    sp_canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sp_draw = ImageDraw.Draw(sp_canvas)
    for sx, sy, sr, scolor in sparkles:
        # diamond sparkle shape
        sp_draw.polygon([(sx, sy - sr), (sx + sr//2, sy), (sx, sy + sr), (sx - sr//2, sy)], fill=scolor)
        sp_draw.polygon([(sx - sr, sy), (sx, sy + sr//2), (sx + sr, sy), (sx, sy - sr//2)], fill=scolor)
        
    sp_glow = sp_canvas.filter(ImageFilter.GaussianBlur(3))
    base = Image.alpha_composite(base, sp_glow)
    base = Image.alpha_composite(base, sp_canvas)
    
    # 8. Save Final 1024 x 500 Feature Graphic
    out_path = os.path.join(store_dir, "feature_graphic.png")
    final_rgb = base.convert('RGB')
    final_rgb.save(out_path, format='PNG', quality=95)
    print(f"SUCCESS: Generated 100% textless feature graphic at {out_path} ({W}x{H})")

if __name__ == '__main__':
    create_textless_feature_graphic()
