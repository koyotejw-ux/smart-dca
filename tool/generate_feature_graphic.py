# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def generate_store_assets():
    root = r"d:\097.flutter_project\average_down_calculator"
    store_dir = os.path.join(root, "store")
    os.makedirs(store_dir, exist_ok=True)
    
    # -------------------------------------------------------------
    # 1. Update 512 x 512 App Icon
    # -------------------------------------------------------------
    icon_src = os.path.join(root, "assets", "app_icon_clean_squircle.png")
    if not os.path.exists(icon_src):
        icon_src = os.path.join(root, "assets", "app_icon.png")
        
    out_icon = os.path.join(store_dir, "icon_512.png")
    im = Image.open(icon_src).convert('RGBA')
    im_512 = im.resize((512, 512), Image.Resampling.LANCZOS)
    im_512.save(out_icon, format='PNG')
    print(f"SAVED: {out_icon} (512x512)")
    
    # -------------------------------------------------------------
    # 2. Generate 1024 x 500 Google Play Feature Graphic
    # -------------------------------------------------------------
    W, H = 1024, 500
    base = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(base)
    
    # Vertical/Diagonal Gradient (Deep Quant Blue #0B1426 -> #020617)
    for y in range(H):
        t = y / H
        r = int(11 * (1 - t) + 2 * t)
        g = int(20 * (1 - t) + 6 * t)
        b = int(38 * (1 - t) + 23 * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
        
    # Atmospheric Glow
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    g_draw.ellipse([80, 50, 480, 450], fill=(0, 130, 255, 60))
    g_draw.ellipse([600, 100, 1000, 500], fill=(0, 210, 255, 40))
    glow = glow.filter(ImageFilter.GaussianBlur(50))
    base.paste(glow, (0, 0), glow)
    
    canvas = base.convert('RGBA')
    draw = ImageDraw.Draw(canvas)
    
    # Left: 3D Squircle App Icon Mockup (260x260)
    icon_size = 260
    ix = 90
    iy = (H - icon_size) // 2
    
    # Drop shadow
    shadow = Image.new('RGBA', (icon_size + 40, icon_size + 40), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.rounded_rectangle([20, 20, icon_size + 20, icon_size + 20], radius=56, fill=(0, 0, 0, 90))
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    canvas.paste(shadow, (ix - 20, iy - 10), shadow)
    
    # Resize and paste icon
    im_sq = im.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
    canvas.paste(im_sq, (ix, iy), im_sq)
    
    # Fonts
    font_bold = "C:\\Windows\\Fonts\\malgunbd.ttf"
    font_reg = "C:\\Windows\\Fonts\\malgun.ttf"
    if not os.path.exists(font_bold):
        font_bold = "C:\\Windows\\Fonts\\arialbd.ttf"
        font_reg = "C:\\Windows\\Fonts\\arial.ttf"
        
    f_badge = ImageFont.truetype(font_bold, 16)
    f_title = ImageFont.truetype(font_bold, 44)
    f_eng = ImageFont.truetype(font_bold, 22)
    f_sub = ImageFont.truetype(font_reg, 18)
    f_tag = ImageFont.truetype(font_bold, 14)
    
    # Right Text Hierarchy
    tx = ix + icon_size + 60
    
    # 1. Kicker Badge
    b_y = 78
    draw.rounded_rectangle([tx, b_y, tx + 240, b_y + 32], radius=16, fill=(15, 45, 95, 240), outline=(0, 140, 255, 255), width=1)
    draw.ellipse([tx + 14, b_y + 11, tx + 24, b_y + 21], fill=(0, 210, 255))
    draw.text((tx + 32, b_y + 6), "GOOGLE PLAY OFFICIAL", font=f_badge, fill=(0, 210, 255))
    
    # 2. Main Title (스마트 물타기 계산기)
    draw.text((tx, b_y + 44), "스마트 물타기 계산기", font=f_title, fill=(255, 255, 255))
    draw.text((tx, b_y + 104), "Smart DCA Calculator · Quant Inversion", font=f_eng, fill=(0, 140, 255))
    
    # 3. Subtitle / Value Proposition
    draw.text((tx, b_y + 146), "폐쇄형 퀀트 역산 엔진 · 0.2초 음성 도크 · 100% 로컬 보안", font=f_sub, fill=(148, 163, 184))
    
    # 4. Feature Badges Row
    pills = [
        ("⚡ 0.2s 음성 도크", (16, 42, 86), (0, 140, 255), (0, 215, 255)),
        ("🎯 목표 평단가 역산", (12, 48, 36), (16, 185, 129), (52, 211, 153)),
        ("🔒 100% 온디바이스", (42, 22, 70), (168, 85, 247), (216, 180, 254)),
        ("🚀 R8 최적화 60fps", (54, 38, 12), (245, 158, 11), (251, 191, 36))
    ]
    px_cur = tx
    py_pill = b_y + 195
    for text, bg_col, border_col, txt_col in pills:
        bbox = f_tag.getbbox(text)
        pw = bbox[2] - bbox[0] + 28
        draw.rounded_rectangle([px_cur, py_pill, px_cur + pw, py_pill + 36], radius=18, fill=bg_col, outline=border_col, width=1)
        draw.text((px_cur + 14, py_pill + 8), text, font=f_tag, fill=txt_col)
        px_cur += pw + 12
        
    out_feat = os.path.join(store_dir, "feature_graphic.png")
    canvas.convert('RGB').save(out_feat, format='PNG', quality=95)
    print(f"SAVED: {out_feat} (1024x500)")

if __name__ == '__main__':
    generate_store_assets()
