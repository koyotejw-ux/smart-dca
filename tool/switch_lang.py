import sqlite3
import base64
import subprocess
import time

def set_lang(lang_code):
    con = sqlite3.connect('real_assets.db')
    cur = con.cursor()
    cur.execute('INSERT OR REPLACE INTO settings (key, value) VALUES ("selected_language", ?)', (lang_code,))
    con.commit()
    con.close()
    
    with open('real_assets.db', 'rb') as f:
        db_bytes = f.read()
    
    p = subprocess.Popen(
        ['adb', '-s', '100.65.0.126:43845', 'exec-in', 'run-as com.antigravity.smart_avg_down.average_down_calculator dd of=databases/assets.db'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = p.communicate(input=db_bytes)
    print(f"[{lang_code}] dd result:", p.returncode, stdout, stderr)
    
    # Restart app
    subprocess.run(['adb', '-s', '100.65.0.126:43845', 'shell', 'am', 'force-stop', 'com.antigravity.smart_avg_down.average_down_calculator'], check=True)
    subprocess.run(['adb', '-s', '100.65.0.126:43845', 'shell', 'monkey', '-p', 'com.antigravity.smart_avg_down.average_down_calculator', '-c', 'android.intent.category.LAUNCHER', '1'], check=True)
    time.sleep(2)

if __name__ == '__main__':
    set_lang('en')
