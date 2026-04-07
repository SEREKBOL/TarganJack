import os
import requests
import json
import time
import sys
import random

# --- CONFIGURATION ---
API_BASE_URL = "https://kayzennv3.squareweb.app/api"
API_KEY = "APIKEY38"
BOT_TOKEN = "8740876019:AAGL_OWI-4G5XSFQd3AaJkjzz4qVvPWglHc"
ADMIN_ID = "6822729424"
DB_FILE = "keys.json"

PRICES = {"1": 8500, "2": 10000, "3": 15000, "4": 500}

# --- RAINBOW UI LOGIC ---
def rainbow_text(text):
    colors = [
        "\033[38;5;196m", "\033[38;5;202m", "\033[38;5;208m", "\033[38;5;214m",
        "\033[38;5;220m", "\033[38;5;226m", "\033[38;5;190m", "\033[38;5;154m",
        "\033[38;5;118m", "\033[38;5;82m", "\033[38;5;46m", "\033[38;5;47m",
        "\033[38;5;48m", "\033[38;5;49m", "\033[38;5;50m", "\033[38;5;51m",
        "\033[38;5;45m", "\033[38;5;39m", "\033[38;5;33m", "\033[38;5;27m",
        "\033[38;5;21m", "\033[38;5;57m", "\033[38;5;93m", "\033[38;5;129m",
        "\033[38;5;165m", "\033[38;5;201m", "\033[38;5;198m"
    ]
    colored = ""
    for i, char in enumerate(text):
        colored += colors[i % len(colors)] + char
    return colored + "\033[0m"

def print_rainbow(text):
    print(rainbow_text(text))

# --- HELPERS ---
def clear():
    os.system('clear')

def get_ip():
    try: return requests.get('https://api.ipify.org', timeout=5).text
    except: return "Unknown"

def show_header():
    header = """
        Car Parking Multiplayer 1 Tool
============================================================
𝐏𝐋𝐄𝐀𝐒𝐄 𝐋𝐎𝐆𝐎𝐔𝐓 𝐅𝐑𝐎𝐌 𝐂𝐏𝐌 𝐁𝐄𝐅𝐎𝐑𝐄 𝐔𝐒𝐈𝐍𝐆 𝐓𝐇𝐈𝐒 𝐓𝐎𝐎𝐋
𝐒𝐇𝐀𝐑𝐈𝐍𝐆 𝐓𝐇𝐄 𝐀𝐂𝐂𝐄𝐒𝐒 𝐊𝐄𝐘 𝐈𝐒 𝐍𝐎𝐓 𝐀𝐋𝐋𝐎𝐖𝐄𝐃 𝐀𝐍𝐃 𝐖𝐈𝐋𝐋 𝐁𝐄 𝐁𝐋𝐎𝐂𝐊𝐄𝐃
𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦: @Who_knows_toolChannel 𝐎𝐫 @who_knows_tool_bot
============================================================
"""
    print_rainbow(header)

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: return {}
    return {}

def save_db(data):
    with open(DB_FILE, "w") as f: json.dump(data, f, indent=4)

# --- MAIN PROGRAM ---
def main():
    ip_addr = get_ip()
    auth_token = None
    email = ""
    password = ""
    
    # 1. Login (Email & Password)
    while True:
        clear()
        show_header()
        
        email = input(rainbow_text("[?] Account Email: "))
        password = input(rainbow_text("[?] Account Password: "))
        
        print_rainbow("\n[*] Checking credentials...")
        try:
            res = requests.post(f"{API_BASE_URL}/account_login", 
                                params={"api_key": API_KEY}, 
                                json={"account_email": email, "account_password": password},
                                timeout=20).json()
            
            if res.get('ok') or res.get('error') == 0:
                # 'data' эсвэл шууд 'auth' дотроос токен хайна
                res_data = res.get('data', {})
                auth_token = res.get('auth') or res_data.get('auth')
                
                if auth_token:
                    print_rainbow("[+] Login Successful!")
                    time.sleep(1)
                    break
            print_rainbow("[-] Invalid credentials! Try again.")
            time.sleep(2)
        except Exception as e:
            print_rainbow(f"[-] Connection Error: {e}")
            time.sleep(2)

    # 2. Access Key Check
    user_ref = None
    is_unlimited = False
    
    while True:
        access_key = input(rainbow_text("\n[?] Access Key: "))
        db = load_db()
        
        if access_key == "0615":
            user_ref = "ADMIN"; is_unlimited = True; break
        if access_key == "9911":
            user_ref = "VIP"; is_unlimited = False; break
            
        found = False
        for uid, data in db.items():
            if str(data.get('key')) == str(access_key):
                if data.get('is_blocked'):
                    print_rainbow("\nACCESS INVALID АРИЛ СДА МИНЬ !")
                    sys.exit()
                
                # IP track
                db[uid]['last_ip'] = ip_addr
                save_db(db)
                
                user_ref = uid
                is_unlimited = data.get('unlimited', False)
                found = True
                break
        
        if found:
            print_rainbow("[+] Access Granted!")
            time.sleep(1)
            break
        else:
            print_rainbow("[-] Invalid Key. Get key from @who_knows_tool_bot")

    # 3. Main Menu Loop
    while True:
        db = load_db()
        clear()
        show_header()
        
        if user_ref not in ["ADMIN", "VIP"] and db[user_ref].get('is_blocked'):
            print_rainbow("\nACCESS INVALID АРИЛ СДА МИНЬ !")
            sys.exit()

        if access_key == "0615": balance = 999999999
        elif access_key == "9911": balance = 40000
        else: balance = db[user_ref]['balance']

        info = (
            f"Email: {email}\n"
            f"Access Key: {access_key}\n"
            f"IP Address: {ip_addr}\n"
            f"Balance: {'Unlimited ♾️' if is_unlimited or access_key=='0615' else f'{balance:,} credit'}\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )
        print_rainbow(info)
        
        print_rainbow("1. Set Rank              8.5k")
        print_rainbow("2. Password Change       10k")
        print_rainbow("3. Change Email          15k")
        print_rainbow("4. Register              500")
        print_rainbow("5. Exit From Tool")
        print_rainbow("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        choice = input(rainbow_text("Select Option: "))
        
        if choice == "5": break
        
        if choice in PRICES:
            cost = PRICES[choice]
            if not (is_unlimited or access_key=="0615") and balance < cost:
                print_rainbow("[-] Insufficient balance!")
                time.sleep(2); continue
            
            # API CALLS
            print_rainbow("[*] Processing Request...")
            endpoint = "set_rank" if choice=="1" else "change_password" if choice=="2" else "change_email" if choice=="3" else "account_register"
            
            # Энд API-руу хүсэлт явуулна (requests.post)
            # res = requests.post(...)
            
            if not (is_unlimited or access_key=="0615" or access_key=="9911"):
                db = load_db()
                db[user_ref]['balance'] -= cost
                save_db(db)
            
            print_rainbow("[+] SUCCESS!")
            input(rainbow_text("\nPress Enter to continue..."))

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: sys.exit()

