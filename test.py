import re
import numpy as np
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import date

cars45Website = "https://www.betacar.ng/all-used-cars#/pageSize=32&orderBy=10&pageNumber=1"

driver = webdriver.Chrome()
driver.get(cars45Website)


# for href in autoChekHrefs:
#     print(href)
betaCarsInventoriesOverview = driver.find_elements(By.XPATH, "//h2[@class='product-title']/a")
betaCarsHrefs = [href.get_attribute("href") for href in betaCarsInventoriesOverview]

for href in betaCarsHrefs:
    driver.get(href)
    
    carId = href
    dateScraped = date.today()
    carTitle = driver.find_element(By.XPATH, "//h1[@itemprop='name']").text
    carBrand = driver.find_element(By.XPATH, "//h1[@itemprop='name']").text.split(maxsplit=6)[1]
    carModel = driver.find_element(By.XPATH, "//h1[@itemprop='name']").text.split(maxsplit=6)[2]
    Year = driver.find_element(By.XPATH, "//h1[@itemprop='name']").text.split(maxsplit=6)[0]
    carCondition = lambda car : "Local Used" if ("Registered" in car) else "Foreign Used"
    
    otherFeatures = driver.find_elements(by=By.XPATH, value="//tr/td[2]")
    res = [feat.text for feat in otherFeatures]
    
    fuelType = res[1].split("(")[1].strip(")")
    carTransmission = res[2]
    carMileage = res[3]
    carColour = res[6]
    
    Price = driver.find_element(by=By.XPATH, value="//div[@class='product-price']/span[1]").text.strip("₦ ")
    # carId = f"BCars{carMileage[:3].replace(',','')}"


    carDetails = {
        "Car Id":carId, "Scraped Date" : dateScraped,
        "Brand": carBrand, "Model": carModel, "Condition": carCondition(carTitle),
        "Year": Year, "Transmission": carTransmission, "Fuel":fuelType,
        "Colour":carColour,"Location":"Lagos", "Mileage": carMileage, "Price": Price
    }

    print(carDetails)
    
