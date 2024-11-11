import os
import pyfiglet
from colorama import Fore, Style, init
import json
import requests
import time 
from urllib.parse import urlparse, parse_qs
from user_agent import generate_user_agent

# Initialize Colorama
init(autoreset=True)

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

# Modified main_wcoin function to accept a query ID directly
def main_wcoin(query_id, amount, key):
    identifier = str(query_id)
    json_data = {
        'identifier': identifier,
        'password': identifier,
    }
    # First API call for authentication
    res = requests.post('https://starfish-app-fknmx.ondigitalocean.app/wapi/api/auth/local', json=json_data).json()
    # Second API call
    r = requests.post('http://77.37.63.209:5000/api', json={'initData': query_id, 'serverData': res, 'amount': amount, 'key': key})
    return (r.json())

# Function to create a gradient banner
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

# Function to print social media info in a box format
def print_info_box(social_media_usernames):
    colors = [Fore.CYAN, Fore.MAGENTA, Fore.LIGHTYELLOW_EX, Fore.BLUE, Fore.LIGHTWHITE_EX]
    box_width = max(len(social) + len(username) for social, username in social_media_usernames) + 4
    print(Fore.WHITE + Style.BRIGHT + '+' + '-' * (box_width - 2) + '+')
    
    for i, (social, username) in enumerate(social_media_usernames):
        color = colors[i % len(colors)]
        print(color + f'| {social}: {username} |')
    
    print(Fore.WHITE + Style.BRIGHT + '+' + '-' * (box_width - 2) + '+')

# Main execution
if __name__ == "__main__":
    banner_text = "WHYWETAP"
    os.system('cls' if os.name == 'nt' else 'clear')
    create_gradient_banner(banner_text)
    
    # Display social media usernames
    social_media_usernames = [
        ("CryptoNews", "@ethcryptopia"),
        ("Auto Farming", "@whywetap"),
        ("Auto Farming", "@autominerx"),
        ("Coder", "@demoncratos"),
    ]
    
    print_info_box(social_media_usernames)
    
    # Get user input for query ID instead of session
    query_id = input("\nEnter Query ID: ")
    balance_input = input("Enter Coin Amount: ")
    key = input("Enter Authorization Key  : ")
    
    # Call main_wcoin with query_id
    data = main_wcoin(query_id, int(balance_input), key)
    os.system('cls' if os.name == 'nt' else 'clear')
    create_gradient_banner('Done')
    
    # Display user data
    try:
        print(Fore.GREEN + Style.BRIGHT + "=== User Information ===")
        print(Fore.YELLOW + f"Username: {data['username']}")
        print(Fore.CYAN + f"Email: {data['email']}")
        print(Fore.MAGENTA + f"Telegram Username: {data['telegram_username']}")
        print(Fore.BLUE + f"Balance: {data['balance']}") 
        print(Fore.LIGHTWHITE_EX + f"Clicks: {data['clicks']}")
        print(Fore.WHITE + f"Max Energy: {data['max_energy']}")
        print(Fore.GREEN + Style.BRIGHT + f"Created At: {data['createdAt']}")
        print(Fore.GREEN + Style.BRIGHT + "========================")
    except:
        print(Fore.RED + Style.BRIGHT + data.get('error', 'An unexpected error occurred'))
