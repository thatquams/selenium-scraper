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


def scrapeAutoChek(maxPage):

    driver = webdriver.Chrome(options=chrome_options)
    allAutoChekDetails = []
    try:
        autoChekWebsite = "https://autochek.africa/ng/cars-for-sale?page_number=1"
        currentPageNumber = 1

        while currentPageNumber <= maxPage:
            driver.get(autoChekWebsite)

            autoChekInventoriesOverview = driver.find_elements(By.XPATH, "//*[@class='MuiBox-root css-1jke4yk']/a")
            autoChekHrefs = [href.get_attribute("href") for href in autoChekInventoriesOverview]

            for href in autoChekHrefs:
                try:
                    driver.get(href)

                    carId = href
                    dateScraped = date.today()
                    
                    # get all cars features and store in list("allFeats")
                    allFeats = driver.find_element(By.TAG_NAME, "h5").text.split(maxsplit=3)
                    carBrand = allFeats[0]
                    carModel = allFeats[1:3] if len(allFeats) <= 4 else allFeats[1]
                    yearOfManufacture = driver.find_element(By.TAG_NAME, "h5").text.split(maxsplit=3)[-1].split(" - ")[-1].strip()

                    
                    Price = driver.find_element(By.XPATH, "//*[@class='MuiTypography-root MuiTypography-body1 css-14bhqez']").text.strip("₦ ")
                    Condition = driver.find_element(By.XPATH, "//div[@class='MuiStack-root css-j7qwjs']").text.split("\n",maxsplit=3)[0] + " Used"
                    otherCarFeatures = driver.find_elements(By.XPATH, "//p[@class='MuiTypography-root MuiTypography-body1 css-1pldev7']")
                    carTransmission = otherCarFeatures[1].text
                    fuelType = otherCarFeatures[2].text
                    carColour = otherCarFeatures[4].text
                    carMileage = driver.find_element(By.XPATH, "//*[@class='MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-1 css-tuxzvu']").text.split('\n')[1]
                    # engineType = self.driver.find_element(By.XPATH, "//p[@class='MuiTypography-root MuiTypography-body1 css-1pldev7']").text
                    # engineSize = "4-Cylinder" if "4" in engineType else "6-Cylinder" if "6" in engineType else "8-Cylinder"
                    # engineSize = "4" if "4" in engineType else "6" if "6" in engineType else "8" if "8" in engineType else "10" if "10" in engineType else "12"

                    """
                    fuelType = otherCarFeatures[2].text
                    carColour = otherCarFeatures[4].text
                    carMileage = self.driver.find_element(By.XPATH, "//*[@class='MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-1 css-tuxzvu']").text.split('\n')[1]
                    carLocation = self.driver.find_element(By.XPATH, "//div[@id = 'state-city']/span[2]").text.split(",")[0]
                    engineType = self.driver.find_element(By.XPATH, "//p[@class='MuiTypography-root MuiTypography-body1 css-1pldev7']").text
                    engineSize = "4-Cylinder" if "4" in engineType else "6-Cylinder" if "6" in engineType else "8-Cylinder"
                    """

                    carDetails = {
                        "Car Id":carId, "Scraped Date":dateScraped,
                        "Brand": carBrand, "Model": " ".join(carModel).strip(" - "), "Condition": Condition,
                        "Year": "".join(yearOfManufacture).strip(" - "), "Transmission": carTransmission, "Color":carColour, "Mileage":carMileage,"Fuel Type":fuelType,
                        "Price": Price
                    }


                    allAutoChekDetails.append(carDetails)

                except NoSuchElementException as e:
                    print(f"Error scraping details: {e}")

            # Construct the URL for the next page
            nextPageUrl = autoChekWebsite.rsplit('=', 1)[0] + '=' + str(currentPageNumber + 1)

            # Navigate to the next page
            driver.get(nextPageUrl)

            # Update autoChekWebsite for the next iteration
            autoChekWebsite = nextPageUrl

            # Increment the page number for the next iteration
            currentPageNumber += 1
            # print(f"Navigated to page {currentPageNumber}")

        # Convert the list of dictionaries to a DataFrame
        autoChekDf = pd.DataFrame(allAutoChekDetails)

        driver.quit()
        return autoChekDf
    except Exception as e:
        print(f"An error occurred: {e}")