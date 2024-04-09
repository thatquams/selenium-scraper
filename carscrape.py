from datetime import time

import numpy as np
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd

website = "https://www.cars45.com/listing?page=1"
path = "/Users/XPS 15/OneDrive/Documents/chrome-win_win64"

driver = webdriver.Chrome()

driver.get(website)

allCarDetails = []

while True:

    car_overviews = driver.find_elements(By.XPATH, "//section[@class='cars-grid grid']/a")

    # all car links
    hrefs = [car_overview.get_attribute("href") for car_overview in car_overviews]

    # path = "/Users/XPS 15/OneDrive/Documents/carbin africa/carbin_webscraping"

    for href in hrefs:
        driver.get(href)     # navigate links

        try:
            carBrand = driver.find_element(by=By.XPATH, value="//*[@itemprop='description']/div/p").text
            carModel = driver.find_element(by=By.XPATH, value="//*[@itemprop='description']/div[2]/p").text
            yearOfManufacture = driver.find_element(by=By.XPATH, value="//*[@itemprop='description']/div[3]/p").text
            carBodyColour = driver.find_element(by=By.XPATH, value="//div[@class='main-details__name']/h1").text.split()[-1]
            carCondition = driver.find_element(by=By.XPATH, value="//div[@class='main-details__tags flex wrap']/span[1]").text
            transmissionType = driver.find_element(by=By.XPATH, value="//div[@class='main-details__tags flex wrap']/span[2]").text
            carMileage = driver.find_element(by=By.XPATH, value="//div[@class='main-details__tags flex wrap']/span[3]").text.split()[0]

            carPrices = driver.find_element(by=By.XPATH, value="//div[@class='main-details__name']/h5").text # get car prices

            # create a dictionary to store the scraped data
            CarDetails = {
                "carBrand": carBrand, "carModel": carModel, "carBodyColour": carBodyColour,
                "carCondition": carCondition,
                "yearOfManufacture": yearOfManufacture, "transmissionType": transmissionType, "carMileage": carMileage,
                "carPrice": carPrices}

            # append all car details
            allCarDetails.append(CarDetails)

        except NoSuchElementException as e:
            print(f"Error scraping details: {e}")

    try:
        # Initial URL
        website = "https://www.cars45.com/listing?page=1"
        max_page = 2  # Define the maximum page number you want to navigate to

        # Start from the first page
        current_page_number = 1

        while current_page_number <= max_page:
            # Navigate to the current page
            driver.get(website)

            # Construct the URL for the next page
            next_page_url = website.rsplit('=', 1)[0] + '=' + str(current_page_number + 1)

            # Navigate to the next page
            driver.get(next_page_url)

            # Increment the page number for the next iteration
            current_page_number += 1

            print(f"Navigated to page {current_page_number}")

            df = pd.DataFrame(allCarDetails)
            df.to_csv("cars45.csv", index=False)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the WebDriver
        driver.quit()




# driver.find_element(by=By.LINK_TEXT, value="//*[@class='pagination__next']")
# nextPageHref = clickNextPage.get_attribute("href")
# driver.get(nextPageHref)
# driver.quit()
"""
otherFeatures = driver.find_elements(by=By.XPATH, value="//img[@src='/_ipx/_/images/keys.png']")

if otherFeatures != "":
    carBodyType = driver.find_element(by=By.XPATH, value="//div[@class='svg flex']/div/span").text
else:
    carBodyType = "Not Specified"
print(carBodyType)
"""

# //*[@class='tab-content__svg__title'][1]
# //*[@itemprop='description']/div
