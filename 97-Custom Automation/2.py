import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

book = {}

path = 'D:\\development\\chromedriver.exe'

driver = webdriver.Chrome(path)
for page in range(1,23):
    url = f'https://www.yellowpages.com.eg/en/category/6th-of-october-supermarkets/33/p{page}'
    driver.get(url)
    try:
        cards = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'mar-bot-15'))
        )
    finally:
        for card in cards:
            names = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'companyName'))
        )
            address = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'company_address'))
        )
            for one in range(len(names)):
                book[names[one].text] = address[one].text


print(book)

df = pd.DataFrame(book.items(), columns=['Mart_Name', 'Address'])

df.to_excel('mart_book.xlsx')

driver.quit()
