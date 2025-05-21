import requests
import subprocess
import paramiko
import time
import os
import re
import json
import sys
from bs4 import BeautifulSoup
import pandas as pd
import re
from dotenv import load_dotenv
from colorama import Fore, Style
from playwright.sync_api import sync_playwright

base_path = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_path, "config.env")
load_dotenv()
load_dotenv(env_path)

class TixcraftCleaner:
    def __init__(self):
        self.events = os.getenv("EVENTS", "").split(",")
        self.activity = os.getenv("ACTIVITY", "")
        self.keywords = os.getenv("KEYWORDS", "").split(",")
        self.headers = {
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.session = requests.Session()
        print(f"{Fore.YELLOW} Activity: {Fore.CYAN}{self.activity}{Style.RESET_ALL}")

    def get_page_content(self, url):
        response = self.session.get(url, headers=self.headers)
        response.encoding = 'utf-8'
        return BeautifulSoup(response.text, 'html.parser')

    def send_release_tickets(self):
        lines = []
        url = f"https://tixcraft.com/activity/game/{self.activity}"
        soup = self.get_page_content(url)

        tickets = soup.find('div', id='gameList').find_all('tr')

        for ticket in tickets:
            ticketId = ticket.get('data-key')
            if ticketId:
                hasLink = ticket.find('button')
                if hasLink:
                    tds = ticket.find_all('td')
                    link = f"https://tixcraft.com/ticket/area/{self.activity}/{ticketId}"
                    lines.append(f"{tds[0].text[:10]}__{tds[1].text}_\n{link}\n\n")

        if lines:
            url = f"https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}/sendMessage"
            payload = {
                "chat_id": os.getenv('CHAT_ID'),
                "text": f"*-- {os.getenv('TITLE', '')} --*\n{''.join(lines)}",
                "parse_mode": "Markdown",
                "disable_web_page_preview": True
            }
            response = requests.post(url, json=payload)
            print(response.text)

def main():
    interval = os.getenv("INTERVAL", "10")

    # url = f"https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}/sendMessage"
    # payload = {
    #     "chat_id": 1001969334,
    #     "text": f"*--------*\n{"".join(['橙208區5880 1 seat(s) remaining_\nhttps://tixcraft.com/ticket/ticket/25_yanzi/19611/6/3\n\n'])}",
    #     "parse_mode": "Markdown"
    # }
    # response = requests.post(url, json=payload)
    while True:
        cleaner = TixcraftCleaner()
        cleaner.send_release_tickets()

        time.sleep(int(interval))
    # Uncomment and add your PTT credentials to send messages

if __name__ == "__main__":
    main()
