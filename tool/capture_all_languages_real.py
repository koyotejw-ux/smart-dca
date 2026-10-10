import sqlite3
import subprocess
import time
import os

ADB = r"C:\Users\coyot\AppData\Local\Android\Sdk\platform-tools\adb.exe"
DEVICE = "100.65.0.126:32881"

LANGUAGES = [
    {'code': 'ko', 'curr': 'krw', 'stock_name': '삼성전자', 'price': 68500, 'qty': 45},
    {'code': 'en', 'curr': 'usd', 'stock_name': 'Apple Inc.', 'price': 185.5, 'qty': 50},
    {'code': 'ja', 'curr': 'jpy', 'stock_name': 'トヨタ自動車', 'price': 2850, 'qty': 200},
    {'code': 'zh', 'curr': 'usd', 'stock_name': '腾讯控股', 'price': 380, 'qty': 100},
    {'code': 'es', 'curr': 'eur', 'stock_name': 'Banco Santander', 'price': 4.5, 'qty': 1500},
    {'code': 'vi', 'curr': 'vnd', 'stock_name': 'Vinamilk', 'price': 68000, 'qty': 500},
    {'code': 'id', 'curr': 'idr', 'stock_name': 'Bank Central Asia', 'price': 9800, 'qty': 1000},
]

def capture_for_lang(item):
    lang_code = item['code']
    curr_code = item['curr']
    stock_name = item['stock_name']
    price = item['price']
    qty = item['qty']

    # 1. Update SQLite DB
    con = sqlite3.connect('device_assets.db')
    cur = con.cursor()
    cur.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('selected_language', ?)", (lang_code,))
    cur.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('selected_currency', ?)", (curr_code,))
    cur.execute("DELETE FROM assets")
    cur.execute(
        "INSERT INTO assets (id, name, symbol, initialPrice, initialQuantity, type) VALUES (1, ?, 'TICKER', ?, ?, 'stock')",
        (stock_name, price, qty)
    )
    con.commit()
    con.close()

    with open('device_assets.db', 'rb') as f:
        db_bytes = f.read()

    # 2. Push DB to device
    subprocess.run([ADB, 'connect', DEVICE], capture_output=True)
    p = subprocess.Popen(
        [ADB, '-s', DEVICE, 'exec-in', 'run-as com.antigravity.smart_avg_down.average_down_calculator dd of=databases/assets.db'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    p.communicate(input=db_bytes)

    # 3. Restart App
    subprocess.run([ADB, '-s', DEVICE, 'shell', 'am', 'force-stop', 'com.antigravity.smart_avg_down.average_down_calculator'])
    subprocess.run([ADB, '-s', DEVICE, 'shell', 'am', 'start', '-a', 'android.intent.action.MAIN', '-c', 'android.intent.category.LAUNCHER', '-n', 'com.antigravity.smart_avg_down.average_down_calculator/.MainActivity'])
    time.sleep(2.5)

    # Dismiss validator popup
    subprocess.run([ADB, '-s', DEVICE, 'shell', 'input', 'tap', '780', '948'])
    time.sleep(0.5)

    out_dir = os.path.join(r"d:\097.flutter_project\average_down_calculator\store\raw_screens", lang_code)
    os.makedirs(out_dir, exist_ok=True)

    # Capture 1: Home (Smart Portfolio)
    home_cap = f"/sdcard/{lang_code}_01_home.png"
    subprocess.run([ADB, '-s', DEVICE, 'shell', 'screencap', '-p', home_cap])
    subprocess.run([ADB, '-s', DEVICE, 'pull', home_cap, os.path.join(out_dir, '01_smart_portfolio.png')])

    # Capture 2: Simulator (3-stage DCA)
    # Tap Simulator button on Home (approx y=550)
    subprocess.run([ADB, '-s', DEVICE, 'shell', 'input', 'tap', '500', '550'])
    time.sleep(1.5)
    subprocess.run([ADB, '-s', DEVICE, 'shell', 'input', 'tap', '780', '948']) # dismiss if popup
    time.sleep(0.3)
    sim_cap = f"/sdcard/{lang_code}_02_sim.png"
    subprocess.run([ADB, '-s', DEVICE, 'shell', 'screencap', '-p', sim_cap])
    subprocess.run([ADB, '-s', DEVICE, 'pull', sim_cap, os.path.join(out_dir, '02_dca_simulator.png')])

    # Capture 3: Target Calculator (Tab 2 inside simulator)
    # Simulator tab bar has 3 tabs: [일반 물타기] [목표 평단가] [보유 자산]
    subprocess.run([ADB, '-s', DEVICE, 'shell', 'input', 'tap', '500', '150'])
    time.sleep(1.0)
    target_cap = f"/sdcard/{lang_code}_03_target.png"
    subprocess.run([ADB, '-s', DEVICE, 'shell', 'screencap', '-p', target_cap])
    subprocess.run([ADB, '-s', DEVICE, 'pull', target_cap, os.path.join(out_dir, '03_target_calculator.png')])

    # Back to Home
    subprocess.run([ADB, '-s', DEVICE, 'shell', 'input', 'keyevent', '4']) # BACK
    time.sleep(1.0)

    # Capture 4: Portfolio Report Screen
    # Tap Portfolio Report button on Home (approx x=750, y=700)
    subprocess.run([ADB, '-s', DEVICE, 'shell', 'input', 'tap', '730', '710'])
    time.sleep(1.5)
    subprocess.run([ADB, '-s', DEVICE, 'shell', 'input', 'tap', '780', '948']) # dismiss if popup
    time.sleep(0.3)
    rep_cap = f"/sdcard/{lang_code}_04_report.png"
    subprocess.run([ADB, '-s', DEVICE, 'shell', 'screencap', '-p', rep_cap])
    subprocess.run([ADB, '-s', DEVICE, 'pull', rep_cap, os.path.join(out_dir, '04_detailed_report.png')])

    # Back to Home
    subprocess.run([ADB, '-s', DEVICE, 'shell', 'input', 'keyevent', '4']) # BACK
    time.sleep(1.0)

    # Capture 5: Settings Screen
    # Tap Bottom Navigation Bar - Settings tab (4th tab, approx x=800, y=950)
    subprocess.run([ADB, '-s', DEVICE, 'shell', 'input', 'tap', '800', '950'])
    time.sleep(1.2)
    subprocess.run([ADB, '-s', DEVICE, 'shell', 'input', 'tap', '780', '948']) # dismiss if popup
    time.sleep(0.3)
    set_cap = f"/sdcard/{lang_code}_05_settings.png"
    subprocess.run([ADB, '-s', DEVICE, 'shell', 'screencap', '-p', set_cap])
    subprocess.run([ADB, '-s', DEVICE, 'pull', set_cap, os.path.join(out_dir, '05_global_multi_currency.png')])

    print(f"Captured all 5 real screens for [{lang_code} / {curr_code}] successfully!")

if __name__ == '__main__':
    for l in LANGUAGES:
        print(f"--- Starting capture for {l['code']} ---")
        capture_for_lang(l)
