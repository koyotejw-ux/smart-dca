import os
from PIL import Image, ImageDraw, ImageFilter

MOCKUP_DIR = "d:/097.flutter_project/auto_portfolio/ftmt/assets/iphone_mockups"
RAW_DIR = "d:/097.flutter_project/auto_portfolio/ftmt/assets/raw"
os.makedirs(MOCKUP_DIR, exist_ok=True)

def make_luxury_iphone_mockup(screen_path, target_screen_w=720):
    screen = Image.open(screen_path).convert('RGBA')
    
    # 1. Clean bottom Android navigation bar if present
    sample_y = screen.height - 145
    bg_sample = screen.getpixel((screen.width // 2, sample_y))
    if len(bg_sample) == 4 and bg_sample[3] == 0:
        bg_col = (7, 10, 18, 255)
    else:
        bg_col = (bg_sample[0], bg_sample[1], bg_sample[2], 255)
        
    s_draw = ImageDraw.Draw(screen)
    s_draw.rectangle([0, screen.height - 130, screen.width, screen.height], fill=bg_col)
    
    # Draw native iOS Home Indicator Bar
    bar_w_raw = 280
    bar_h_raw = 10
    bar_y_raw = screen.height - 44
    bar_col_raw = (229, 192, 123, 220) # Champagne gold bar
    s_draw.rounded_rectangle(
        [(screen.width - bar_w_raw) // 2, bar_y_raw, (screen.width + bar_w_raw) // 2, bar_y_raw + bar_h_raw],
        radius=5, fill=bar_col_raw
    )
    
    sw = target_screen_w
    sh = int(round(sw * (screen.height / screen.width)))
    screen_resized = screen.resize((sw, sh), Image.Resampling.LANCZOS)
    
    bezel = 20 # Ultra-slim uniform luxury bezel
    dev_w = sw + bezel * 2
    dev_h = sh + bezel * 2
    
    pad_side = 8
    canvas_w = dev_w + pad_side * 2
    canvas_h = dev_h
    
    device = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(device)
    
    ox = pad_side
    oy = 0
    
    # Hardware Buttons
    draw.rounded_rectangle([ox - 4, 240, ox, 290], radius=2, fill=(40, 45, 60, 255))
    draw.rounded_rectangle([ox - 4, 330, ox, 420], radius=2, fill=(40, 45, 60, 255))
    draw.rounded_rectangle([ox - 4, 450, ox, 540], radius=2, fill=(40, 45, 60, 255))
    draw.rounded_rectangle([ox + dev_w, 360, ox + dev_w + 4, 490], radius=2, fill=(40, 45, 60, 255))
    
    # Body
    draw.rounded_rectangle([ox, oy, ox + dev_w, oy + dev_h], radius=60, fill=(18, 22, 34, 255), outline=(229, 192, 123, 160), width=2)
    draw.rounded_rectangle([ox + 2, oy + 2, ox + dev_w - 2, oy + dev_h - 2], radius=58, outline=(255, 215, 0, 60), width=1)
    draw.rounded_rectangle([ox + bezel - 2, oy + bezel - 2, ox + dev_w - bezel + 2, oy + dev_h - bezel + 2], radius=44, fill=(5, 7, 12, 255))
    
    # Mask
    mask = Image.new('L', (sw, sh), 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.rounded_rectangle([0, 0, sw, sh], radius=42, fill=255)
    device.paste(screen_resized, (ox + bezel, oy + bezel), mask)
    
    # Dynamic Island
    di_w = int(round(sw * 0.28))
    di_h = 32
    di_x = ox + bezel + (sw - di_w) // 2
    di_y = oy + bezel + 12
    draw.rounded_rectangle([di_x, di_y, di_x + di_w, di_y + di_h], radius=16, fill=(0, 0, 0, 255))
    lens_x = di_x + di_w - 22
    lens_y = di_y + di_h // 2
    draw.ellipse([lens_x - 5, lens_y - 5, lens_x + 5, lens_y + 5], fill=(12, 18, 30, 255), outline=(30, 40, 65, 255), width=1)
    draw.ellipse([lens_x - 2, lens_y - 2, lens_x + 1, lens_y + 1], fill=(0, 229, 255, 180))
    
    return device

print("Building distinct luxury iPhone mockups...")
raw_files = {
    'iphone_01_hub.png': f"{RAW_DIR}/screen1.png",
    'iphone_02_radar.png': f"{RAW_DIR}/screen_match.png",
    'iphone_03_tarot.png': f"{RAW_DIR}/screen_shop.png",
    'iphone_04_connections.png': f"{RAW_DIR}/screen_vault.png",
    'iphone_05_match.png': f"{RAW_DIR}/screen_match.png",
    'iphone_06_shop.png': f"{RAW_DIR}/screen_shop.png",
    'iphone_07_vault.png': f"{RAW_DIR}/screen_vault.png",
}

for name, path in raw_files.items():
    if os.path.exists(path):
        dev = make_luxury_iphone_mockup(path)
        out_path = f"{MOCKUP_DIR}/{name}"
        dev.save(out_path)
        print(f"Generated {out_path} ({dev.size})")

print("All distinct mockups generated successfully!")
