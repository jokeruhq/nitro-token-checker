import ctypes
import time
import concurrent.futures
import platform
from colorama import init, Fore, Style
from datetime import datetime
import tls_client

init()

# Set console title in a cross-platform way
if platform.system() == "Windows":
    try:
        ctypes.windll.kernel32.SetConsoleTitleW("Discord Nitro Checker by j0k3r")
    except:
        pass
elif platform.system() == "Linux":
    print("\033]0;Discord Nitro Checker by j0k3r\007", end="", flush=True)
elif platform.system() == "Darwin":  # macOS
    print("\033]0;Discord Nitro Checker by j0k3r\007", end="", flush=True)

blue = Fore.BLUE
red = Fore.RED
warn = Fore.YELLOW
green = Fore.GREEN
gray = Fore.LIGHTBLACK_EX
white_red = Fore.LIGHTRED_EX
white_green = Fore.LIGHTGREEN_EX
white_warn = Fore.LIGHTYELLOW_EX
white_blue = Fore.LIGHTBLUE_EX
reset_colors = Style.RESET_ALL

THREADS = 200
requests = tls_client.Session(client_identifier="chrome120", random_tls_extension_order=True)
boost1 = 0
boost2 = 0
noboost = 0
nonitro = 0
locked = 0
invalid = 0
ratelimited = 0

class Console:
    def __init__(self, debug=False):
        self.debug = debug
        
    def error(self, x):
        if self.debug:
            print(f"{red}[- ERROR -]{reset_colors} - {gray}[{datetime.now().strftime('%Y-%m-%d - %H:%M:%S')}]{reset_colors} |\t {white_red}{x}{reset_colors}")
        else:
            print(f"{red}[-]{reset_colors}\t {red+x}{reset_colors}")
            
    def success(self, x):
        if self.debug:
            print(f"{green}[+ Success +]{reset_colors} - {gray}[{datetime.now().strftime('%Y-%m-%d - %H:%M:%S')}]{reset_colors} |\t {white_green+x}{reset_colors}")
        else:
            print(f"{green}[+]{reset_colors}\t {white_green+x}{reset_colors}")
            
    def warn(self, x, t=0):
        if self.debug:
            print(f"{warn}[! {'WARNING' if t == 0 else 'FAILED'} !]{reset_colors} - {gray}[{datetime.now().strftime('%Y-%m-%d - %H:%M:%S')}]{reset_colors} |\t {white_warn+x}{reset_colors}")
        else:
            print(f"{warn}[!]{reset_colors}\t {white_warn+x}{reset_colors}")
            
    def info(self, x):
        if self.debug:
            print(f"{blue}[* INFO *]{reset_colors} - {gray}[{datetime.now().strftime('%Y-%m-%d - %H:%M:%S')}]{reset_colors} |\t {white_blue+x}{reset_colors}")
        else:
            print(f"{blue}[*]{reset_colors}\t {white_blue+x}{reset_colors}")

console = Console(debug=True)

class Utils:
    @staticmethod
    def calculate_time_remaining(date):
        date = datetime.strptime(date.split("T")[0], '%Y-%m-%d')
        current_date = datetime.now()
        time_remaining = date - current_date
        days = time_remaining.days
        return f"{days} days"
    
    @staticmethod
    def format_credential(credential):
        parts = credential.strip().split(':')
        if len(parts) == 3:
            return parts
        return None
        
class Checker:
    def __init__(self):
        self.utils = Utils()
        self.sp = 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIwLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjI1NjIzMSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0='
        self.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'referer': 'https://discord.com/channels/@me',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-US',
            'x-super-properties': self.sp,
        }
    
    def check_boosts_in_token(self, token, proxy=None):
        global noboost, boost2, boost1
        boosts = 0
        headers = self.headers.copy()
        headers['authorization'] = token
        
        try:
            request = requests.get('https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots', headers=headers, proxy=proxy)
            if request.status_code == 200:
                js = request.json()
                boosts = sum(1 for boost in js if not boost.get("cooldown_ends_at"))
                
            if boosts == 0:
                noboost += 1
            elif boosts == 1:
                boost1 += 1
            elif boosts == 2:
                boost2 += 1
                
            return boosts
        except Exception as e:
            console.error(f"Error checking boosts: {str(e)}")
            return 0
    
    def check(self, credential, proxy=None):
        global boost1, boost2, noboost, nonitro, locked, invalid, ratelimited
        
        token_parts = self.utils.format_credential(credential)
        if not token_parts:
            console.error("Invalid credential format. Expected email:pass:token.")
            return 0
            
        email, password, token = token_parts
        has_nitro = False
        nitro_time = None
        is_locked = True
        boosts = 0
        
        headers = self.headers.copy()
        headers['authorization'] = token
        
        try:
            request = requests.get('https://discord.com/api/v9/users/@me/billing/subscriptions', headers=headers, proxy=proxy)
            status_code = request.status_code
            
            if status_code == 401:
                is_locked = 401
                invalid += 1
                console.info(f"{credential[:20]}**** | {gray}Info :{reset_colors} [{gray}Status : {red}INVALID{reset_colors}, {gray}Nitro : {red}NO{reset_colors}, {gray}Subscription Date Expire in : {white_blue}None{reset_colors}]")
                with open("output/invalid.txt", "a") as f:
                    f.write(f"{credential}\n")
                return 0
                
            if status_code == 429:
                ratelimited += 1
                console.warn(f"{credential[:20]}**** | Ratelimited [Ratelimit number : {ratelimited}]")
                return 0
                
            if status_code == 200:
                is_locked = False
                js = request.json()
                
                if len(js) != 0:
                    has_nitro = True
                    nitro_time = self.utils.calculate_time_remaining(js[0]["current_period_end"])
                    boosts = self.check_boosts_in_token(token, proxy)
                
                status_text = f'{white_green}UNLOCKED{reset_colors}' if not is_locked else f'{red}LOCKED{reset_colors}'
                nitro_text = f'{white_green}YES{reset_colors}, {gray}Subscription Date Expire in : {reset_colors}{white_blue}{nitro_time}{reset_colors}' if has_nitro else f'{red}NO{reset_colors}, {gray}Subscription Date Expire in : {reset_colors}{white_blue}None{reset_colors}'
                
                console.info(f"{credential[:20]}**** | {gray}Info :{reset_colors} [{gray}Status : {status_text}, {gray}Nitro : {reset_colors}{nitro_text}, {gray}Boosts left : {green}{boosts}{reset_colors}]")
                
                if has_nitro:
                    with open(f"output/{boosts}boosts.txt", "a") as f:
                        f.write(f"{credential}\n")
                else:
                    nonitro += 1
                    with open("output/nonitro.txt", "a") as f:
                        f.write(f"{credential}\n")
                        
                if is_locked:
                    locked += 1
                    with open("output/locked.txt", "a") as f:
                        f.write(f"{credential}\n")
                        
                return 1
                
        except Exception as e:
            console.error(f"Error checking token: {str(e)}")
            return 0

checker = Checker()

def main():
    try:
        # Make sure output directory exists
        import os
        os.makedirs("output", exist_ok=True)
        
        with open("tokens.txt", "r") as file:
            credentials = [line.strip() for line in file if line.strip()]
        
        if not credentials:
            console.error("No tokens found in tokens.txt")
            return
            
        console.info(f"Starting check of {len(credentials)} tokens with {THREADS} threads")
        console.info("Discord Nitro Checker by j0k3r")
        
        start = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
            results = list(executor.map(checker.check, credentials))
        end = time.time() - start
        
        console.success(f"Checked {len(credentials)} credentials in {end:.2f}s")
        console.info(f"1 Boost: {boost1} | 2 Boosts: {boost2} | No Nitro: {nonitro} | Locked: {locked} | Invalid: {invalid} | Ratelimited {ratelimited} time(s)")
        
    except Exception as e:
        console.error(f"Error in main function: {str(e)}")

if __name__ == "__main__":
    main()
