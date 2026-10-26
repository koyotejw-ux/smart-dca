#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smart DCA Calculator - GitHub Pages Auto-Deployment Helper
Helper script to export fresh slides, PDF, and prepare for GitHub Pages deployment.
"""

import os
import subprocess
import sys

# Ensure UTF-8 output on Windows consoles
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run_cmd(cmd, desc=""):
    print(f"\n[INFO] {desc}...")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[ERROR] {res.stderr}")
        return False
    print(res.stdout.strip())
    return True

def main():
    print("=" * 60)
    print("  Smart DCA Calculator - GitHub Pages & Mobile Web Deployer")
    print("=" * 60)

    # 1. Check or ask for base URL
    base_url = os.environ.get("GITHUB_PAGES_BASE_URL", "")
    if not base_url:
        print("\nTip: Set GITHUB_PAGES_BASE_URL to customize your URL, for example:")
        print("  set GITHUB_PAGES_BASE_URL=https://<your-username>.github.io/average_down_calculator")
        base_url = "https://coyote-dev.github.io/average_down_calculator"
        print(f"Using default base URL: {base_url}")

    # 2. Re-render Slide 12 with live QR code
    print("\n1. Re-generating Slide 12 with high-contrast QR code...")
    run_cmd(f'python -c "import generate_behance_slides; generate_behance_slides.make_slide_12()"', "Rendering Slide 12")

    # 3. Export PDF with embedded hyperlinks
    print("\n2. Re-exporting interactive PDF with live links...")
    run_cmd(f'python export_portfolio_pdf.py', "Building PDF")

    # 4. Check git status
    print("\n3. Git Status:")
    run_cmd("git status -s", "Git changes")

    print("\n" + "=" * 60)
    print("  배포 준비가 완료되었습니다! (Deployment Ready)")
    print("=" * 60)
    print("""
[GitHub에 올려서 온라인 실시간 체험 활성화하는 방법]

1. GitHub에서 'average_down_calculator' 이름으로 새 공개(Public) 리포지토리를 생성합니다.
2. 아래 명령어로 원격 저장소(origin)를 연결하고 푸시합니다:
   
   git add .
   git commit -m "feat(portfolio): deploy mobile responsive prototype with live QR scan"
   git remote add origin https://github.com/<사용자ID>/average_down_calculator.git
   git push -u origin master

3. GitHub 리포지토리의 [Settings] -> [Pages] 메뉴로 이동하여:
   - Source: "GitHub Actions" (권장: 자동 빌드 및 배포)
     또는
   - Source: "Deploy from a branch" -> Branch: master / (root) 선택 후 [Save]

4. 완료 즉시 다음 주소로 전 세계 어디서든 모바일로 바로 체험할 수 있습니다:
   -> https://<사용자ID>.github.io/average_down_calculator/prototype.html
""")

if __name__ == '__main__':
    main()
