import os
import requests
import json
import time
import sys
import random

# --- ТОХИРГОО ---
API_BASE_URL = "https://kayzennv3.squareweb.app/api"
API_KEY = "APIKEY38"
DB_FILE = "access.json"

PRICES = {
    "1": 30500,  # SET RANK
    "2": 25500,  # CHANGE EMAIL
    "3": 6000,   # CHANGE PASSWORD
    "4": 0       # REGISTER FREE
}

# --- RAINBOW UI ---
def rainbow_text(text):
    colors = [
        "\033[38;5;196m", "\033[38;5;202m", "\033[38;5;208m", "\033[38;5;214m",
        "\033[38;5;220m", "\033[38;5;226m", "\033[38;5;190m", "\033[38;5;154m",
        "\033[38;5;118m", "\033[38;5;82m", "\033[38;5;46m", "\033[38;5;47m",
        "\033[38;5;48m", "\033[38;5;49m", "\033[38;5;50m", "\033[38;5;51m",
        "\033[38;5;45m", "\033[38;5;39m", "\033[38;5;33m", "\033[38;5;27m"
    ]
    return "".join([random.choice(colors) + char for char in text]) + "\033[0m"

def print_rainbow(text):
    print(rainbow_text(text))

# --- HELPERS ---
def clear(): os.system('clear')

def get_ip():
    try: return requests.get('https://api.ipify.org', timeout=5).text
    except: return "127.0.0.1"

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: return {}
    return {}

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f: json.dump(data, f, indent=4)

def show_header():
    header = """====================================================
PLEASE LOGOUT FROM CPM BEFORE USING THIS TOOL
SHARING THE ACCESS KEY IS NOT ALLOWED AND WILL BE BLOCKED
Telegram: @BaldanShopChannel Or @BaldanShopChat
===================================================="""
    print_rainbow(header)

# --- MAIN ---
def main():
    ip_addr = get_ip()
    
    while True: # Home Loop
        auth_token = None
        user_id_ref = None
        is_unlimited = False
        
        # 1. LOGIN SCREEN
        while True:
            clear()
            show_header()
            email = input(rainbow_text("[?] Account Email: "))
            password = input(rainbow_text("[?] Account Password: "))
            access_key = input(rainbow_text("[?] Access Key: "))

            if not email or not password or not access_key:
                print_rainbow("\n[!] Note: make sure you filled out the fields !")
                time.sleep(2)
                continue

            print_rainbow("\n[*] Verifying...")
            db = load_db()
            
            # Verify Access Key
            key_found = False
            if access_key == "0615":
                key_found = True; user_id_ref = "ADMIN"; is_unlimited = True
            else:
                for uid, data in db.items():
                    if data.get('key') == access_key:
                        if data.get('is_blocked'):
                            print_rainbow("\nACCESS INVALID АРИЛ СДА МИНЬ !"); sys.exit()
                        user_id_ref = uid
                        is_unlimited = data.get('unlimited', False)
                        key_found = True; break
            
            if not key_found:
                print_rainbow("[✘] Trying to Login: TRY AGAIN.")
                time.sleep(2); continue

            # Verify CPM Account
            try:
                res = requests.post(f"{API_BASE_URL}/account_login", 
                                    params={"api_key": API_KEY}, 
                                    json={"account_email": email, "account_password": password}).json()
                
                if res.get('ok') or res.get('error') == 0:
                    auth_token = res.get('auth') or res.get('data', {}).get('auth')
                    print_rainbow("{%} Trying to Login: SUCCESSFUL")
                    time.sleep(1); break
                else:
                    print_rainbow("[✘] Trying to Login: TRY AGAIN.")
                    time.sleep(2)
            except:
                print_rainbow("[✘] Server Error."); time.sleep(2)

        # 2. MENU SCREEN
        while True:
            clear()
            show_header()
            db = load_db()
            # Блок шалгах
            if user_id_ref != "ADMIN" and db[user_id_ref].get('is_blocked'): sys.exit()
            
            balance = 999999999 if is_unlimited else db[user_id_ref]['balance']
            
            print_rainbow(f"EMAIL : {email}")
            print_rainbow(f"PASSWORD : {password}")
            print_rainbow(f"ACCESS KEY : {access_key}")
            print_rainbow(f"telegram id : {user_id_ref}")
            print_rainbow(f"IP ADRESS {ip_addr}")
            print_rainbow(f"BALANCE : {'Unlimited ♾️' if is_unlimited else balance}")
            print_rainbow("-" * 52)
            print_rainbow("1. SET RANK               30.5K")
            print_rainbow("2. CHANGE EMAIL         25.5K")
            print_rainbow("3. CHANGE PASSWORD           6K")
            print_rainbow("4. REGISTER                           FREE")
            print_rainbow("5. LOGOUT FROM ACCOUNT")
            print_rainbow("6. EXIT FROM TOOL")
            print_rainbow("-" * 52)

            choice = input(rainbow_text("Select Option: "))

            # EXIT & LOGOUT
            if choice == "6":
                print_rainbow("exit from tool you")
                sys.exit()
            if choice == "5":
                print_rainbow("{ You account sign out} successful")
                time.sleep(1); break

            # ACTIONS
            if choice in PRICES:
                cost = PRICES[choice]
                if balance < cost:
                    print_rainbow("[×] Insufficient balance!"); time.sleep(2); continue

                res_act = {"ok": False}
                if choice == "1":
                    print_rainbow("{%} GIVING YOU KING RANK ..")
                    res_act = requests.post(f"{API_BASE_URL}/set_rank", params={"api_key": API_KEY}, json={"account_auth": auth_token}).json()
                    if res_act.get('ok'): print_rainbow("{%} GIVING YOU KING RANK .. SUCCESSFUL")
                    else: print_rainbow("[×] giving you king rank ... Again")
                
                elif choice == "2":
                    new_e = input(rainbow_text("{%} cpm your email new email change: "))
                    print_rainbow(f"your new email {new_e}")
                    res_act = requests.post(f"{API_BASE_URL}/change_email", params={"api_key": API_KEY}, json={"account_auth": auth_token, "new_email": new_e}).json()
                    if res_act.get('ok'): print_rainbow("(%) Change email.. Successful")
                    else: print_rainbow("[×} change email ... Again")

                elif choice == "3":
                    new_p = input(rainbow_text("{%} cpm your password new password change: "))
                    print_rainbow(f"your new password {new_p}")
                    res_act = requests.post(f"{API_BASE_URL}/change_password", params={"api_key": API_KEY}, json={"account_auth": auth_token, "new_password": new_p}).json()
                    if res_act.get('ok'): print_rainbow("{√} Password change ..... Successful")
                    else: print_rainbow("{×} password change .... Again")

                elif choice == "4":
                    re = input(rainbow_text("Register email: "))
                    rp = input(rainbow_text("Register password: "))
                    print_rainbow("{ You new account register}")
                    res_act = requests.post(f"{API_BASE_URL}/account_register", params={"api_key": API_KEY}, json={"account_email": re, "account_password": rp}).json()
                    if res_act.get('ok'): print_rainbow("{√} register... register successfully")
                    else: print_rainbow("{x} register... Register again")

                # Баланс хасах
                if res_act.get('ok') and not is_unlimited:
                    db = load_db(); db[user_id_ref]['balance'] -= cost; save_db(db)

                # Шат дараалсан асуулт
                exit_choice = input(rainbow_text("\n{ Do you want exit } y/n (n): ")).lower()
                if exit_choice == 'y':
                    print_rainbow("{ You account sign out} successful")
                    time.sleep(1)
                    break # Go to home
                else:
                    continue # Stay in menu

        if choice == "5" or (choice in PRICES and exit_choice == 'y'):
            continue # Restart to home screen

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print_rainbow("\nexit from tool you"); sys.exit()

