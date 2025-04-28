import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import csv

url = 'https://www.tokopedia.com/search?st=&q=iphone%2015%20pro%20ibox&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource='

# Initialize the Chrome driver
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome()
driver.get(url) 
time.sleep(25)   

# Scroll down to load more products
for _ in range(10):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(20)       

# Wait for product elements to load
try:
    WebDriverWait(driver, 100).until(
        ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.css-jza1fo')))
except Exception as e:
    print(f"Error waiting for products: {e}")

# Find all product elements
products = driver.find_elements(By.CSS_SELECTOR, 'div.css-jza1fo')
print(f"Number of products found: {len(products)}")

# Extract product details
product_list = []
for idx, product in enumerate(products):
    try:
        title = product.find_element(By.CSS_SELECTOR, 'div[class="_6+OpBPVGAgqnmycna+bWIw=="]').text
        price = product.find_element(By.CSS_SELECTOR, 'div[class="XvaCkHiisn2EZFq0THwVug=="]').text
        link = product.find_element(By.TAG_NAME,'a').get_attribute('href')
        product_list.append({'title': title, 'price': price, 'link': link})
    except Exception as e:
        print(f"Error extracting product at index {idx}: {e}")

print(f"Found {len(product_list)} products.")

# Close the driver
driver.quit()

# Save to CSV
with open('products.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['title', 'price', 'link']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for product in product_list:
        writer.writerow(product)

# Read from CSV
with open('products.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row)
