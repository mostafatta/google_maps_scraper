from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# BeautifulSoup imports
from bs4 import BeautifulSoup

# Pandas import
import pandas as pd
from dataclasses import dataclass, asdict, field
import argparse
import time

@dataclass
class Business:
    name: str = None
    address: str = None
    website: str = None
    phone_number: str = None

@dataclass
class BusinessList:
    business_list: list[Business] = field(default_factory=list)

    def dataframe(self):
        return pd.json_normalize((asdict(business) for business in self.business_list), sep='.')

    def save_to_excel(self, filename):
        self.dataframe().to_excel(f'{filename}.xlsx', index=False)

    def save_to_csv(self, filename):
        self.dataframe().to_csv(f'{filename}.csv', index=False)

def main():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # removed as requested
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get('https://www.google.com/maps?hl=en')
    time.sleep(5)


    input("Press Enter to close the browser...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--s", "--search", type=str, dest='search')
    parser.add_argument("--l", "--location", type=str, dest='location')
    args = parser.parse_args()

    if args.location and args.search:
        search_for = f'{args.search} {args.location}'
    else:
        search_for = 'real state cairo'

    main()
