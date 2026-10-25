import os
from PIL import Image

def export_slides_to_pdf():
    slide_dir = 'portfolio/behance_slides'
    out_pdf = 'portfolio/Smart_DCA_Portfolio.pdf'
    
    # Ordered slides 01 to 12
    slide_files = [f"slide_{i:02d}.png" for i in range(1, 13)]
    images = []
    
    for f in slide_files:
        p = os.path.join(slide_dir, f)
        if os.path.exists(p):
            im = Image.open(p).convert('RGB')
            images.append(im)
        else:
            print(f"Warning: {p} does not exist.")
            
    if images:
        images[0].save(
            out_pdf,
            save_all=True,
            append_images=images[1:],
            resolution=150.0,
            quality=95
        )
        pdf_size_mb = os.path.getsize(out_pdf) / (1024 * 1024)
        print(f"SUCCESS: Generated {out_pdf} ({len(images)} slides, {pdf_size_mb:.2f} MB)")
    else:
        print("ERROR: No slide images found.")

if __name__ == '__main__':
    export_slides_to_pdf()
