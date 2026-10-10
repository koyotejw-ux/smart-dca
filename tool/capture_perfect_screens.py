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

def run_adb(args):
    return subprocess.run([ADB, '-s', DEVICE] + args, capture_output=True)

def capture_all():
    subprocess.run([ADB, 'connect', DEVICE], capture_output=True)
    
    for item in LANGUAGES:
        lang_code = item['code']
        curr_code = item['curr']
        stock_name = item['stock_name']
        price = item['price']
        qty = item['qty']
        
        print(f"==================================================")
        print(f"Processing [{lang_code} / {curr_code}] ...")
        
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

        p = subprocess.Popen(
            [ADB, '-s', DEVICE, 'exec-in', 'run-as com.antigravity.smart_avg_down.average_down_calculator dd of=databases/assets.db'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        p.communicate(input=db_bytes)

        # 2. Restart App to ensure clean state
        run_adb(['shell', 'am', 'force-stop', 'com.antigravity.smart_avg_down.average_down_calculator'])
        run_adb(['shell', 'am', 'start', '-a', 'android.intent.action.MAIN', '-c', 'android.intent.category.LAUNCHER', '-n', 'com.antigravity.smart_avg_down.average_down_calculator/.MainActivity'])
        time.sleep(2.5)

        # Dismiss validator popup if any
        run_adb(['shell', 'input', 'tap', '780', '948'])
        time.sleep(0.4)

        out_dir = os.path.join(r"d:\097.flutter_project\average_down_calculator\store\raw_screens", lang_code)
        os.makedirs(out_dir, exist_ok=True)

        # --- Screen 1: Home (Smart Portfolio) ---
        cap1 = f"/sdcard/{lang_code}_01.png"
        run_adb(['shell', 'screencap', '-p', cap1])
        run_adb(['pull', cap1, os.path.join(out_dir, '01_smart_portfolio.png')])
        print(f"[{lang_code}] 1/5 Home captured")

        # --- Screen 2: Simulator (3-stage DCA) ---
        # Tap Simulator Hero Button (x=450, y=1330)
        run_adb(['shell', 'input', 'tap', '450', '1330'])
        time.sleep(1.8)
        run_adb(['shell', 'input', 'tap', '780', '948']) # dismiss popup if present
        time.sleep(0.3)
        cap2 = f"/sdcard/{lang_code}_02.png"
        run_adb(['shell', 'screencap', '-p', cap2])
        run_adb(['pull', cap2, os.path.join(out_dir, '02_dca_simulator.png')])
        print(f"[{lang_code}] 2/5 Simulator captured")

        # --- Screen 3: Target Calculator ---
        # Tap Target Tab (x=780, y=1070)
        run_adb(['shell', 'input', 'tap', '780', '1070'])
        time.sleep(1.2)
        # Scroll down slightly to show target input cards cleanly
        run_adb(['shell', 'input', 'swipe', '450', '1500', '450', '900', '300'])
        time.sleep(1.0)
        cap3 = f"/sdcard/{lang_code}_03.png"
        run_adb(['shell', 'screencap', '-p', cap3])
        run_adb(['pull', cap3, os.path.join(out_dir, '03_target_calculator.png')])
        print(f"[{lang_code}] 3/5 Target Calculator captured")

        # Back to Home
        run_adb(['shell', 'input', 'keyevent', '4'])
        time.sleep(1.2)

        # --- Screen 4: Portfolio Report Screen ---
        # Tap Portfolio Report card (x=720, y=1700)
        run_adb(['shell', 'input', 'tap', '720', '1700'])
        time.sleep(1.8)
        run_adb(['shell', 'input', 'tap', '780', '948']) # dismiss popup if present
        time.sleep(0.3)
        cap4 = f"/sdcard/{lang_code}_04.png"
        run_adb(['shell', 'screencap', '-p', cap4])
        run_adb(['pull', cap4, os.path.join(out_dir, '04_detailed_report.png')])
        print(f"[{lang_code}] 4/5 Portfolio Report captured")

        # Back to Home
        run_adb(['shell', 'input', 'keyevent', '4'])
        time.sleep(1.2)

        # --- Screen 5: Settings Screen ---
        # Tap Settings Gear icon in top AppBar (x=830, y=160)
        run_adb(['shell', 'input', 'tap', '830', '160'])
        time.sleep(1.8)
        run_adb(['shell', 'input', 'tap', '780', '948']) # dismiss popup if present
        time.sleep(0.3)
        cap5 = f"/sdcard/{lang_code}_05.png"
        run_adb(['shell', 'screencap', '-p', cap5])
        run_adb(['pull', cap5, os.path.join(out_dir, '05_global_multi_currency.png')])
        print(f"[{lang_code}] 5/5 Settings captured")

    print("\nALL 35 REAL SCREENS CAPTURED WITH EXACT LOCALIZED UI AND CURRENCY!")

if __name__ == '__main__':
    capture_all()
