from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from selenium.webdriver.common.by import By 
from datetime import date
from selenium import webdriver
import pandas as pd
import re
from selenium.webdriver.chrome.options import Options

chrome_options = Options() 

chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")   # Required for AWS environments
chrome_options.add_argument("--disable-dev-shm-usage")  # Prevent resource issues
chrome_options.add_argument("--disable-gpu")  # Optional for headless
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--window-size=1920,1080")  # Necessary for headless rendering


def betaCar(maxPageNumber):

    driver = webdriver.Chrome(options=chrome_options)
    try:
        betaCarsDetails = []
        betaCarsWebsite = "https://www.betacar.ng/all-used-cars#/pageSize=32&orderBy=10&pageNumber=1"
        currentPageNumber = 1

        while currentPageNumber <= maxPageNumber:
            # navigate to beta cars website
            driver.get(betaCarsWebsite)

            betaCarsInventoriesOverview = driver.find_elements(By.XPATH, "//h2[@class='product-title']/a")
            betaCarsHrefs = [href.get_attribute("href") for href in betaCarsInventoriesOverview]

            for href in betaCarsHrefs:
                driver.get(href)

                try:
                    carId = href
                    dateScraped = date.today()
                    carTitle = driver.find_element(By.XPATH, "//h1[@itemprop='name']").text
                    carBrand = driver.find_element(By.XPATH, "//h1[@itemprop='name']").text.split(maxsplit=6)[1]
                    carModel = driver.find_element(By.XPATH, "//h1[@itemprop='name']").text.split(maxsplit=6)[2]
                    Year = driver.find_element(By.XPATH, "//h1[@itemprop='name']").text.split(maxsplit=6)[0]
                    carCondition = lambda car : "Local Used" if ("Registered" in car) else "Foreign Used"
                    
                    otherFeatures = driver.find_elements(by=By.XPATH, value="//tr/td[2]")
                    res = [feat.text for feat in otherFeatures]
                    carTransmission = res[2]
                    fuelType = res[1].split("(")[1].strip(")")
                    carMileage = res[3]
                    carColour = res[6]
                    # engineType = self.driver.find_element(By.XPATH, "//*[@id='quickTab-default']/div/table/tbody/tr[1]/td[2]").text
                    # engineSize = "4" if "4" in engineType else "6" if "6" in engineType else "8" if "8" in engineType else "10" if "10" in engineType else "12"
                    
                    """
                    fuelType = res[1].split("(")[1].strip(")")
                    carMileage = res[3]
                    carColour = res[6]
                    
                    engineType = self.driver.find_element(By.XPATH, "//*[@id='quickTab-default']/div/table/tbody/tr[1]/td[2]").text
                    engineSize = "4-Cylinder" if "4" in engineType else "6-Cylinder" if "6" in engineType else "8-Cylinder"
                    """
                    Price = driver.find_element(by=By.XPATH, value="//div[@class='product-price']/span[1]").text.strip("₦ ")
                    
                    carDetails = {
                        "Car Id":carId, "Scraped Date" : dateScraped,
                        "Brand": carBrand, "Model": carModel, "Condition": carCondition(carTitle),
                        "Year": Year, "Transmission": carTransmission, "Color":carColour, "Mileage":carMileage,"Fuel Type":fuelType,
                        "Price": Price
                    }

                    betaCarsDetails.append(carDetails)

                except NoSuchElementException as e:
                    print(f"Error scraping details: {e}")

            # Construct the URL for the next page
            nextPageUrl = betaCarsWebsite.rsplit('=', 1)[0] + '=' + str(currentPageNumber + 1)
            # Navigate to the next page
            driver.get(nextPageUrl)

            betaCarsWebsite = nextPageUrl

            # Increment the page number for the next iteration
            currentPageNumber += 1
            # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(betaCarsDetails)
        driver.quit()
        return df

    except Exception as e:
        print(f"An error occurred: {e}")