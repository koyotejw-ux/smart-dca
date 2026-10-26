import os
import fitz  # PyMuPDF

def export_slides_to_pdf(base_url=None):
    if base_url is None:
        base_url = os.environ.get("GITHUB_PAGES_BASE_URL", "https://coyote-dev.github.io/average_down_calculator")
    slide_dir = 'portfolio/behance_slides'
    out_pdf = 'portfolio/Smart_DCA_Portfolio.pdf'
    
    # Ordered slides 01 to 12
    slide_files = [f"slide_{i:02d}.png" for i in range(1, 13)]
    
    doc = fitz.open()
    
    for idx, f in enumerate(slide_files):
        p = os.path.join(slide_dir, f)
        if not os.path.exists(p):
            print(f"Warning: {p} does not exist.")
            continue
            
        # Create page with exact slide dimensions (1920 x 1080) for 1:1 pixel-to-point coordinate mapping
        page = doc.new_page(width=1920, height=1080)
        page.insert_image(fitz.Rect(0, 0, 1920, 1080), filename=p)
        
        slide_num = idx + 1
        
        # -------------------------------------------------------------
        # Slide 10 Links: Interactive 6 Mobile Screens & User Journey
        # -------------------------------------------------------------
        if slide_num == 10:
            # 6 Phones Grid Click Targets
            px = 130
            pw = 210
            pgap = 80
            phone_targets = [
                ("home", "01. 홈 대시보드"),
                ("voice", "02. AI 음성 비서"),
                ("target", "03. 목표 역산 엔진"),
                ("sim", "04. 리스크 진단 리포트"),
                ("home", "05. OLED 다크 테마"),
                ("home", "06. 맞춤 환경 설정")
            ]
            for flow_key, label in phone_targets:
                rect = fitz.Rect(px, 205, px + pw, 780)
                url = f"{base_url}/prototype.html?flow={flow_key}"
                page.insert_link({
                    'kind': fitz.LINK_URI,
                    'from': rect,
                    'uri': url
                })
                px += pw + pgap
                
            # User Journey Bottom Step Chips
            journey_chips = [
                (300, 500, "home"),
                (560, 770, "voice"),
                (830, 1040, "target"),
                (1100, 1310, "sim"),
                (1370, 1570, "home"),
                (1630, 1800, "home"),
            ]
            for sx, ex, flow_key in journey_chips:
                rect = fitz.Rect(sx, 920, ex, 970)
                url = f"{base_url}/prototype.html?flow={flow_key}"
                page.insert_link({
                    'kind': fitz.LINK_URI,
                    'from': rect,
                    'uri': url
                })
                
        # -------------------------------------------------------------
        # Slide 12 Links: Grand Finale Interactive Prototype Showcase Hub
        # -------------------------------------------------------------
        elif slide_num == 12:
            # Left Dual Phone Hero Mockup Touch Target
            page.insert_link({
                'kind': fitz.LINK_URI,
                'from': fitz.Rect(100, 205, 760, 850),
                'uri': f"{base_url}/prototype.html"
            })
            
            # Left Bottom Flutter Web Spec Strip
            page.insert_link({
                'kind': fitz.LINK_URI,
                'from': fitz.Rect(100, 865, 760, 980),
                'uri': f"{base_url}/prototype.html"
            })
            
            # 4 Step Flow Interactive Cards (Mapped to exact 1920x1080 design coordinates)
            step_links = [
                (fitz.Rect(800, 236, 1820, 324), f"{base_url}/prototype.html?flow=home"),
                (fitz.Rect(800, 334, 1820, 422), f"{base_url}/prototype.html?flow=voice"),
                (fitz.Rect(800, 432, 1820, 520), f"{base_url}/prototype.html?flow=target"),
                (fitz.Rect(800, 530, 1820, 618), f"{base_url}/prototype.html?flow=sim")
            ]
            for rect, url in step_links:
                page.insert_link({
                    'kind': fitz.LINK_URI,
                    'from': rect,
                    'uri': url
                })
                
            # Master Primary Hero Launcher Banner
            page.insert_link({
                'kind': fitz.LINK_URI,
                'from': fitz.Rect(800, 638, 1820, 758),
                'uri': f"{base_url}/prototype.html"
            })
            
            # Bottom QR Code and Link Area
            page.insert_link({
                'kind': fitz.LINK_URI,
                'from': fitz.Rect(800, 776, 1820, 980),
                'uri': f"{base_url}/prototype.html"
            })
            
    # Save optimized PDF with hyperlinks
    doc.save(out_pdf, deflate=True, garbage=4)
    doc.close()
    
    pdf_size_mb = os.path.getsize(out_pdf) / (1024 * 1024)
    print(f"SUCCESS: Generated interactive linked PDF -> {out_pdf} ({len(slide_files)} slides, {pdf_size_mb:.2f} MB)")

if __name__ == '__main__':
    export_slides_to_pdf()
