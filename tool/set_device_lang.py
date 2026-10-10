import sqlite3
import subprocess
import time
import os

ADB = r"C:\Users\coyot\AppData\Local\Android\Sdk\platform-tools\adb.exe"
DEVICE = "100.65.0.126:32881"

def set_lang_and_currency(lang_code, curr_code):
    con = sqlite3.connect('device_assets.db')
    cur = con.cursor()
    cur.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('selected_language', ?)", (lang_code,))
    cur.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('selected_currency', ?)", (curr_code,))
    con.commit()
    con.close()

    with open('device_assets.db', 'rb') as f:
        data = f.read()

    subprocess.run([ADB, 'connect', DEVICE], capture_output=True)
    p = subprocess.Popen(
        [ADB, '-s', DEVICE, 'exec-in', 'run-as com.antigravity.smart_avg_down.average_down_calculator dd of=databases/assets.db'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = p.communicate(input=data)
    print(f"Set [{lang_code} / {curr_code}] dd code:", p.returncode, out, err)

    subprocess.run([ADB, '-s', DEVICE, 'shell', 'am', 'force-stop', 'com.antigravity.smart_avg_down.average_down_calculator'])
    subprocess.run([ADB, '-s', DEVICE, 'shell', 'am', 'start', '-n', 'com.antigravity.smart_avg_down.average_down_calculator/.MainActivity'])
    time.sleep(2)

if __name__ == '__main__':
    set_lang_and_currency('ja', 'jpy')
