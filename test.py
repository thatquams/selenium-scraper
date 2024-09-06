import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains as AC
import re


# Function to scroll the page
# def scroll_page(driver, scroll_pause_time, max_scrolls):
#     current_scrolls = 0
#     while current_scrolls < max_scrolls:
#         driver.execute_script("window.scrollBy(0, 1000);")
#         time.sleep(scroll_pause_time)
#         current_scrolls += 1

driver = webdriver.Chrome()
# driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)


website = "https://autochek.africa/ng/car/Mercedes-Benz-ML-350-ref-cBeN8_1Fl"
driver.get(website)

# carBrand = driver.find_element(By.TAG_NAME, "h5").text
allFeats = driver.find_element(By.TAG_NAME, "h5").text.split(maxsplit=3)
carBrand = allFeats[0]
model = allFeats[1:3] if len(allFeats) <= 4 else allFeats[1]
yearOfManufacture = driver.find_element(By.TAG_NAME, "h5").text.split(maxsplit=3)[-1]


# lambda x : x[1] if len(x) <=3 else x[1:3]

print(carBrand, " - ", " ".join(model).strip(" - "), " ", yearOfManufacture.strip(" - "))
# print(model)
