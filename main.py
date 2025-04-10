from selenium import webdriver
# from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
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
def scroll_to_load_results(driver,scrolls=10,pause=2):
    try: 
     sidebar=webdriver(driver,15).until(EC.presence_of_all_elements_located(By.CSS_SELECTOR,'[role="main"]'))
     for _ in range(scrolls):
        driver.execute_script("arguments[0].scrolltop=arguments[0].scrollHight",sidebar)
        time.sleep(pause)
    except Exception as e:
        print(f"Error while scrolling:{e}")    



def main(search_for):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # removed as requested
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get('https://www.google.com/maps')
    time.sleep(5)
    search_button=driver.find_element(By.ID,"searchboxinput")
    search_button.clear()
    search_button.send_keys(search_for)
    search_button.send_keys(Keys.RETURN)
    time.sleep(5)
    scroll_to_load_results(driver,scrolls=15,pause=2)
    business_list=BusinessList()
    results = driver.find_elements(By.CSS_SELECTOR, 'a.hfpxzc')
    print(f"Found {len(results)} results...")
    for result in results:
        try:
            driver.execute_script("arguments[0].click();",result)
            time.sleep(4)
            business_name=driver.find_element(By.CSS_SELECTOR,'h1.DUwDvf').text
            address = driver.find_element(By.CSS_SELECTOR, '[data-item-id="address"]').text
            element = driver.find_element(By.CSS_SELECTOR, '[data-item-id="authority"] a')
            website = element.get_attribute('href')
            element2 = driver.find_element(By.CSS_SELECTOR, 'a[data-tooltip="Copy phone number"]')
            phoneNumber = element.get_attribute('aria-label')
            business = Business(name=business_name, address=address, website=website, phone_number=phoneNumber)
            business_list.business_list.append(business)
            print(f"Added {business_name} to the list...")
            driver.back()
            time.sleep(3)
            scroll_to_load_results(driver,scrolls=1,pause=1)
            results=driver.find_elements(By.CSS_SELECTOR,'a.hfpxzc')
        except Exception as e:
            print(f"Error while processing {business_name}: {e}")
            continue
    business_list.save_to_csv(f"{business_name}_data")
    print("Data saved to business_data.csv")


    



    


    input("Press Enter to close the browser...")
    driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--s", "--search", type=str, dest='search')
    parser.add_argument("--l", "--location", type=str, dest='location')
    args = parser.parse_args()

    if args.location and args.search:
        search_for = f'{args.search} {args.location}'
    else:
        search_for = 'real state cairo'

    main(search_for)
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
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
#     # Wait for the results container to be loaded
#     try:
#         sidebar = WebDriverWait(driver, 15).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Search results"]'))
#         )
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

#     search_box = driver.find_element(By.ID, "searchboxinput")
#     search_box.clear()
#     search_box.send_keys(search_for)
#     search_box.send_keys(Keys.RETURN)
#     time.sleep(5)

#     scroll_to_load_results(driver, scrolls=15, pause=2)

#     business_list = BusinessList()

#     results = driver.find_elements(By.CSS_SELECTOR, 'a.hfpxzc')
#     print(f"Found {len(results)} results...")

#     for index, result in enumerate(results[:30]):  # adjust this to scrape more businesses
#         try:
#             driver.execute_script("arguments[0].click();", result)
#             time.sleep(4)

#             name = driver.find_element(By.CSS_SELECTOR, 'h1.DUwDvf').text
#             address = driver.find_element(By.CSS_SELECTOR, '[data-item-id="address"]').text
#             website = driver.find_element(By.CSS_SELECTOR, '[data-item-id="authority"]').text
#             phone = driver.find_element(By.CSS_SELECTOR, '[data-tooltip="Copy phone number"]').text

#             business = Business(name=name, address=address, website=website, phone_number=phone)
#             business_list.business_list.append(business)

#             print(f"[{index + 1}] {name} ✔️")

#             driver.back()
#             time.sleep(3)
#             scroll_to_load_results(driver, scrolls=1, pause=1)  # to keep results visible
#             results = driver.find_elements(By.CSS_SELECTOR, 'a.hfpxzc')

#         except Exception as e:
#             print(f"⚠️ Error scraping business {index + 1}: {e}")
#             continue

#     business_list.save_to_csv("business_data")
#     print("✅ Data saved to business_data.csv")

#     input("Press Enter to close the browser...")
#     driver.quit()

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--s", "--search", type=str, dest='search')
#     parser.add_argument("--l", "--location", type=str, dest='location')
#     args = parser.parse_args()

#     if args.location and args.search:
#         search_for = f'{args.search} {args.location}'
#     else:
#         search_for = 'real estate cairo'

#     main(search_for)
