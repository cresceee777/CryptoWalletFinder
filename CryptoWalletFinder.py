from hdwallet import HDWallet
from hdwallet.symbols import BTC as BTC_SYMBOL, LTC as LTC_SYMBOL, ETH as ETH_SYMBOL, DOGE as DOGE_SYMBOL
from hdwallet.utils import generate_mnemonic
from typing import Optional
from colorama import Fore
import json, requests, os
from datetime import datetime
from time import sleep
import random, threading
import hdwallet

E = '\033[1;31m'
B = '\033[2;36m'
G = '\033[1;32m'
S = '\033[1;33m'
def clear():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")

if not os.path.isfile('config.json'):
    clear()
    print(f"{Fore.RED}The config.json file is missing or it's not in the same path!{Fore.RESET}")
    input("Press enter to exit...")
    exit()

with open('config.json') as config_file:
    data = json.load(config_file)
    b_config_strenght = data["settings"]["bruteforcer"]["strenght"]
    b_config_language = data["settings"]["bruteforcer"]["language"]
    b_config_passphere = data["settings"]["bruteforcer"]["passphere"]
    c_config_file_name = data["settings"]["checker"]["filename"]
    config_failed = data["settings"]["general"]["failed"]
    config_success = data["settings"]["general"]["success"]
    config_address = data["settings"]["general"]["addresstype"]
    api_urls = data["settings"]["general"]["api"]

def center(var: str, space: int = None):
    if not space:
        space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines())/2)])) // 2
    return "\n".join((' ' * int(space)) + var for var in var.splitlines())

def ui():
    clear()
    font = """
⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣴⣶⣾⣿⣿⣿⣿⣷⣶⣦⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣠⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⠀⠀⠀⠀⠀
⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀
⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⠟⠿⠿⡿⠀⢰⣿⠁⢈⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀
⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣤⣄⠀⠀⠀⠈⠉⠀⠸⠿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀
⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⢠⣶⣶⣤⡀⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿⡆
⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠼⣿⣿⡿⠃⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣷
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⢀⣀⣀⠀⠀⠀⠀⢴⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢿⣿⣿⣿⣿⣿⣿⣿⢿⣿⠁⠀⠀⣼⣿⣿⣿⣦⠀⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿⡿
⠸⣿⣿⣿⣿⣿⣿⣏⠀⠀⠀⠀⠀⠛⠛⠿⠟⠋⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⠇
⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⣤⡄⠀⣀⣀⣀⣀⣠⣾⣿⣿⣿⣿⣿⣿⣿⡟⠀
⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣄⣰⣿⠁⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀
⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀
⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⢿⣿⣿⣿⣿⡿⠿⠟⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀"""
    faded = ''
    red = 0
    for line in font.splitlines():
        faded += (f"\033[38;2;{red};10;230m{line}\033[0m\n")
        if red < 255:
            red += 10
            if red > 110:
                red = 255
    print(center(faded))
    print(center(f'{Fore.LIGHTYELLOW_EX}\nYup\n{Fore.RESET}'))

def errorfile():
    clear()
    print(f"{Fore.RED}[!] FATAL ERROR! A text file in the directory is missing, please make sure the files: {config_failed} | {config_success} | {c_config_file_name} are there, or are in the same path! {Fore.RESET}")
    input(f"{Fore.LIGHTRED_EX}[!] Press enter to exit... {Fore.RESET}")
    exit()

ui()
settings = 'B'#input(f"{Fore.YELLOW}[?]{Fore.RESET} {Fore.LIGHTWHITE_EX}Make a choice between Checker and Bruteforcer [C] - [B] > {Fore.RESET}")

def check_balance(symbol, address, api_urls):
    if symbol == "BTC":
        api_url = api_urls['btc']
    elif symbol == "LTC":
        api_url = api_urls['ltc']
    elif symbol == "DOGE":
        api_url = api_urls['doge']
    elif symbol == "ETH":
        api_url = api_urls['eth']
    else:
        return 0, 0
    response = requests.get(f"{api_url}/{address}")
    if response.status_code == 404:
        #print(f"Error: Received 404 status code for URL {response.url}")
        #print("The API endpoint might be incorrect or the address may not exist.")
        pass
        return 0, 0
    elif response.status_code != 200:
        #print(f"Error: Received {response.status_code} status code for URL {response.url}")
        #print(f"Response content: {response.text}")
        pass
        return 0, 0
    try:
        get_info = response.json()
    except json.decoder.JSONDecodeError:
        print(f"Error parsing JSON response: {response.text}")
        return 0, 0
    
    if symbol == "BTC":
        balance = get_info.get('chain_stats', {}).get('funded_txo_sum', 0)
        all_time_balance = get_info.get('chain_stats', {}).get('spent_txo_sum', 0)
    elif symbol == "LTC":
        balance = get_info.get('chain_stats', {}).get('funded_txo_sum', 0)
        all_time_balance = get_info.get('chain_stats', {}).get('spent_txo_sum', 0)
    elif symbol == "DOGE":
        balance = get_info.get('balance', 0)
        all_time_balance = get_info.get('received', 0)
    elif symbol == "ETH":
        balance = get_info.get('balance', 0) / 1e18  # Convert wei to ETH
        all_time_balance = get_info.get('total_received', 0) / 1e18  # Convert wei to ETH
    else:
        balance = 0
        all_time_balance = 0

    return balance, all_time_balance

def main():
    if settings.lower() == "b":
        if not (os.path.isfile(config_failed) and os.path.isfile(config_success) and os.path.isfile(c_config_file_name)):
            errorfile()
        print(f'''{G}{B}[+] Type Of Addresses : {S}{config_address}
{B}[+] Language : {S}{b_config_language}
{B}[+] Strength : {S}{b_config_strenght}''')
        print("\n")
        STRENGTH = b_config_strenght
        LANGUAGE = b_config_language
        PASSPHRASE = None if b_config_passphere == "None" else b_config_passphere
        s = requests.Session()
        def whisper():
            now_time = datetime.now()
            current = now_time.strftime("%H:%M:%S")
            symbol=random.choice([LTC_SYMBOL,DOGE_SYMBOL,ETH_SYMBOL,BTC_SYMBOL])
            MNEMONIC = generate_mnemonic(language=LANGUAGE, strength=STRENGTH)
            hdwallet = HDWallet(symbol=symbol, use_default_path=False)
            hdwallet.from_mnemonic(mnemonic=MNEMONIC, language=LANGUAGE, passphrase=PASSPHRASE)
            btc_address = hdwallet.p2pkh_address()
            btc_wif = hdwallet.dumps()['wif']
            btc_seed = hdwallet.dumps()['mnemonic']
            btc_entropy = hdwallet.dumps()['entropy']
            btc_privatekey = hdwallet.dumps()['private_key']
            balance, all_time_balance = check_balance("BTC", btc_address, api_urls)
            if str(balance) == "0" or str(all_time_balance) == "0":
                with open(config_failed, "a") as fail:
                    fail.write(f"{symbol} | {btc_address} | {balance}$ | {all_time_balance}$ | {btc_seed} | {btc_privatekey} | {btc_entropy} | {btc_wif} \n")
                    print(f'''{B}[+] Coin : {G}{symbol}
{S}[+] Seed Phrase : {B}{btc_seed}
{S}[+] Address : {B}{btc_address}
{S}[+] Balance : {E}{balance}$ | {all_time_balance}$
{S}[+] Private Key : {B}{btc_privatekey}
{S}{'='*30}
''')
            else:
                with open(config_success, "a") as valid:
                    valid.write(f"{symbol} | {btc_address} | {balance}$ | {all_time_balance}$ | {btc_seed} | {btc_privatekey} | {btc_entropy} | {btc_wif} \n")
                    print(f'''{B}[+] Coin : {G}{symbol}
{B}[+] Seed Phrase : {G}{btc_seed}
{B}[+] Address : {G}{btc_address}
{B}[+] Balance : {G}{balance}$ | {all_time_balance}$
{B}[+] Private Key : {G}{btc_privatekey}
{E}{'='*30}
''')
    for _ in range(9999999999999):
     threading.Thread(target=whisper).start()
#     for _ in range(9999999999999):
#      threading.Thread(target=whisper).start()
main()