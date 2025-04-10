# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import pandas as pd
# from dataclasses import dataclass, asdict, field
# import argparse
# import time

# @dataclass
# class Business:
#     name: str = None
#     address: str = None
#     website: str = None
#     phone_number: str = None

# @dataclass
# class BusinessList:
#     business_list: list[Business] = field(default_factory=list)

#     def dataframe(self):
#         return pd.json_normalize((asdict(business) for business in self.business_list), sep='.')

#     def save_to_excel(self, filename):
#         self.dataframe().to_excel(f'{filename}.xlsx', index=False)

#     def save_to_csv(self, filename):
#         self.dataframe().to_csv(f'{filename}.csv', index=False)

# def scroll_to_load_results(driver, scrolls=10, pause=2):
#     try:
#         sidebar = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[role="main"]')))
#         for _ in range(scrolls):
#             driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", sidebar)
#             time.sleep(pause)
#     except Exception as e:
#         print(f"Error while scrolling: {e}")

# def main(search_for):
#     options = webdriver.ChromeOptions()
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     driver.get('https://www.google.com/maps')
#     time.sleep(5)
    
#     search_input = driver.find_element(By.ID, "searchboxinput")
#     search_input.clear()
#     search_input.send_keys(search_for)
#     search_input.send_keys(Keys.RETURN)
#     time.sleep(5)
    
#     scroll_to_load_results(driver, scrolls=15, pause=2)
    
#     business_list = BusinessList()
#     results = driver.find_elements(By.CSS_SELECTOR, 'a.hfpxzc')
#     print(f"Found {len(results)} results...")

#     for index, result in enumerate(results):
#         try:
#             driver.execute_script("arguments[0].click();", result)
#             time.sleep(5)

#             business_name = driver.find_element(By.CSS_SELECTOR, 'h1.DUwDvf').text
#             address = driver.find_element(By.CSS_SELECTOR, '[data-item-id="address"]').text

#             # Website (dynamic XPath)
#             website = None
#             try:
#                 website_element = WebDriverWait(driver, 5).until(
#                     EC.presence_of_element_located((By.XPATH, '//a[contains(@aria-label, "Website")]'))
#                 )
#                 website = website_element.get_attribute('href')
#                 print(f"Website found: {website}")
#             except Exception as e:
#                 print(f"Website not found: {e}")

#             # Phone number (dynamic XPath)
#             phone_number = None
#             try:
#                 phone_element = WebDriverWait(driver, 5).until(
#                     EC.presence_of_element_located((By.XPATH, '//button[@data-item-id="phone"]//div[contains(@class, "UsdlK")]'))
#                 )
#                 phone_number = phone_element.text
#                 print(f"Phone number found: {phone_number}")
#             except Exception as e:
#                 print(f"Phone number not found: {e}")

#             business = Business(
#                 name=business_name,
#                 address=address,
#                 website=website,
#                 phone_number=phone_number
#             )
#             business_list.business_list.append(business)
#             print(f"Added {business_name} to the list.")

#             driver.back()
#             time.sleep(3)
#             scroll_to_load_results(driver, scrolls=1, pause=1)
#             results = driver.find_elements(By.CSS_SELECTOR, 'a.hfpxzc')
#         except Exception as e:
#             print(f"Error while processing business at index {index}: {e}")
#             continue

#     filename = f"{search_for}_data"
#     business_list.save_to_csv(filename)
#     business_list.save_to_excel(filename)
#     print(f"Data saved to {filename}.csv and {filename}.xlsx")

#     input("Press Enter to close the browser...")
#     driver.quit()

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='Google Maps Business Data Scraper')
#     parser.add_argument('search_for', help='The search query for businesses to scrape from Google Maps')
#     args = parser.parse_args()
#     main(args.search_for)

import asyncio
import pandas as pd
from dataclasses import dataclass, asdict, field
from playwright.async_api import async_playwright

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
        self.dataframe().to_excel(f"{filename}.xlsx", index=False)

    def save_to_csv(self, filename):
        self.dataframe().to_csv(f"{filename}.csv", index=False)

async def scroll_results(page, scrolls=10):
    for _ in range(scrolls):
        await page.mouse.wheel(0, 10000)
        await page.wait_for_timeout(2000)

async def main(search_query: str):
    business_list = BusinessList()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.google.com/maps", timeout=60000)
        await page.wait_for_selector("input#searchboxinput")

        await page.fill("input#searchboxinput", search_query)
        await page.keyboard.press("Enter")

        await page.wait_for_selector('div[role="main"]')
        await scroll_results(page, scrolls=15)

        results = await page.query_selector_all('a.hfpxzc')
        print(f"Found {len(results)} results")

        for i in range(len(results)):
            try:
                results = await page.query_selector_all('a.hfpxzc')  # Refresh list
                if i >= len(results):
                    break

                await results[i].click()
                await page.wait_for_timeout(5000)

                name = await page.locator("h1.DUwDvf").text_content()
                address = await page.locator('[data-item-id="address"]').text_content()

                # Try to get website (using partial link text logic)
                try:
                    website_elem = await page.query_selector('//a[contains(@href, "http") and not(contains(@href, "google.com"))]')
                    website = await website_elem.get_attribute("href") if website_elem else None
                except:
                    website = None

                # Try to get phone number
                try:
                    phone_elem = await page.query_selector('//button[contains(@aria-label, "Phone") or contains(., "+") or contains(., "0")]')
                    phone_number = await phone_elem.text_content() if phone_elem else None
                except:
                    phone_number = None

                business = Business(
                    name=name,
                    address=address,
                    website=website,
                    phone_number=phone_number
                )
                business_list.business_list.append(business)
                print(f"Added: {name}")

                # Go back to results
                await page.go_back()
                await page.wait_for_timeout(3000)
                await scroll_results(page, scrolls=1)

            except Exception as e:
                print(f"Error on result {i}: {e}")
                continue

        filename = f"{search_query}_data"
        business_list.save_to_csv(filename)
        business_list.save_to_excel(filename)
        print(f"Saved to {filename}.csv and {filename}.xlsx")

        await browser.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python script.py 'search query'")
    else:
        query = sys.argv[1]
        asyncio.run(main(query))

