import pandas as pd
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from selenium.webdriver.common.by import By 
from datetime import date
from selenium import webdriver
import re

from selenium.webdriver.chrome.options import Options

chrome_options = Options() 

chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")   # Required for AWS environments
chrome_options.add_argument("--disable-dev-shm-usage")  # Prevent resource issues
chrome_options.add_argument("--disable-gpu")  # Optional for headless
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--window-size=1920,1080")  # Necessary for headless rendering

def scrapeCars45(maxPage):

    allCars45Details = []
    driver = webdriver.Chrome(options=chrome_options)
    try:
        cars45Website = "https://www.cars45.com/listing?page=1"
        # Start from the first page
        currentPageNumber = 1

        while currentPageNumber <= maxPage:
            # Navigate to the current page
            driver.get(cars45Website)

            # Extract car links
            carOverviews = driver.find_elements(By.XPATH, "//section[@class='cars-grid grid']/a")
            hrefs = [carOverview.get_attribute("href") for carOverview in carOverviews]

            try:
                for href in hrefs:
                    try:
                        driver.get(href)  # navigate links
                    except WebDriverException as e:
                        print(f"Error loading page {href}: {e}")


                    try:
                        carId = href
                        dateScraped = date.today()
                        carBrand = driver.find_element(By.XPATH, "//h1[@itemprop='name']").text.split()[0]
                        modelElement = driver.find_element(By.XPATH, "//div[@itemprop='description']//span[normalize-space()='Model']")
                        # Navigate to the preceding sibling p tag to extract the engine size value
                        carModel = modelElement.find_element(By.XPATH, "./preceding-sibling::p").text.strip()

                        carModel = driver.find_element(By.XPATH, "//h1[@itemprop='name']").text.split()[1]
                        carCondition = driver.find_element(By.XPATH,"//div[@class='main-details__tags flex wrap']/span[1]").text
                        transmissionType = driver.find_element(By.XPATH,"//div[@class='main-details__tags flex wrap']/span[2]").text
                        try:
                            carMileage = driver.find_element(By.XPATH, "//div[@class='main-details__tags flex wrap']/span[3]").text
                        except NoSuchElementException:
                            carMileage = "0 km"

                        carColour = driver.find_element(By.XPATH, "//h1[@itemprop = 'name']").text.split()[-1]
                        fuelType = driver.find_element(By.XPATH, "//img[contains(@src, '/_ipx/_/images/diesel.png')]/../span[@class='tab-content__svg__title']").text.strip()
                        
                        # engineSize = self.driver.find_element(By.XPATH, "//div[@itemprop = 'description']/div[7]/p").text
                        # engineSizeSpanElement = self.driver.find_element(By.XPATH, "//div[@itemprop='description']//span[@class='general-info__value']").text
                        # try:
                        #     # engineSizeSpanElement = self.driver.find_element(By.XPATH, "//div[@itemprop='description']//span[normalize-space()='Number of Cylinders']")
                        #     engineSizeSpanElement = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@itemprop='description']//span[normalize-space()='Number of Cylinders']")))
                        #     engineSize = engineSizeSpanElement.find_element(By.XPATH, "./preceding-sibling::p").text.strip()
                        #     # engineSize = engineSizeSpanElement
                        # except :
                        #     engineSize = None

                        
                        """
                        fuelType = self.driver.find_element(By.XPATH, "//img[contains(@src, '/_ipx/_/images/diesel.png')]/../span[@class='tab-content__svg__title']").text.strip()
                        
                        # engineSize = self.driver.find_element(By.XPATH, "//div[@itemprop = 'description']/div[7]/p").text
                        enginSizeSpanElement = self.driver.find_element(By.XPATH, "//div[@itemprop='description']//span[normalize-space()='Engine Size']")

                        # Navigate to the preceding sibling p tag to extract the engine size value
                        engineSize = enginSizeSpanElement.find_element(By.XPATH, "./preceding-sibling::p").text.strip()


                        # Check if engineSize contains only alphabetic characters
                        # if re.match(r'^[a-zA-Z]+$', engineSize):
                        #     # If engineSize contains only alphabetic characters, replace it with "0"
                        #     searchEngineSizeRed = "0"
                        # else:
                        #     # Otherwise, keep the original value of engineSize
                        #     searchEngineSizeRed = "4-Cylinder" if int(engineSize) <= 2800 else "6-Cylinder" if int(engineSize) <= 3000 or int(engineSize) <= 3500 else "8-Cylinder"
                                                
                        # engineType = ["V4" if int(engineSize) <= 2800 else "V6" if int(engineSize) <= 3000 or int(engineSize) <= 3500 else "V8"]
                    
                        try:
                            carMileage = self.driver.find_element(By.XPATH, "//div[@class='main-details__tags flex wrap']/span[3]").text
                        except NoSuchElementException:
                            carMileage = "0 km"

                        carColour = self.driver.find_element(By.XPATH, "//h1[@itemprop = 'name']").text.split()[-1]
                        carLocation = self.driver.find_element(By.XPATH, "//div[@class = 'main-details']/p").text.split(",")[0].strip()
                        """
                        
                        yearOfManufacture = driver.find_element(By.XPATH, "//h1[@itemprop='name']").text
                        year_pattern = r'\b\d{4}\b'

                        # Search for the year pattern in the yearOfManufacture string
                        year_match = re.search(year_pattern, yearOfManufacture)
                        carYear = year_match.group()

                        Price = driver.find_element(By.XPATH, "//div[@class='main-details__name']/h5").text.strip("₦ ")
                        

                        # Create a dictionary to store the scraped data
                        # CarDetails = {
                        #     "Car Id" : carId, "Scraped Date":dateScraped,
                        #     "Brand": carBrand, "Model": carModel,
                        #     "Condition": carCondition, "Year": carYear, "Transmission": transmissionType,
                        #     "Fuel":fuelType, "Colour":carColour,"Location":carLocation, "Mileage":carMileage,"Engine Type":searchEngineSizeRed, "Price": Price}
                        CarDetails = {
                            "Car Id" : carId, "Scraped Date":dateScraped,
                            "Brand": carBrand, "Model": carModel,
                            "Condition": carCondition, "Year": carYear, "Transmission": transmissionType, "Color":carColour, "Mileage":carMileage,"Fuel Type":fuelType,
                            "Price": Price}
                        

                        # Append all car details
                        allCars45Details.append(CarDetails)
                    except ConnectionError as error:
                        print(f"This error Occured {error}")
                        

            except NoSuchElementException as e:
                print(f"Error scraping details: {e}")

            # print(f"Navigated to page {currentPageNumber}")

            # Construct the URL for the next page
            nextPageUrl = cars45Website.rsplit('=', 1)[0] + '=' + str(currentPageNumber + 1)
            # Navigate to the next page
            driver.get(nextPageUrl)

            cars45Website = nextPageUrl

            # Increment the page number for the next iteration
            currentPageNumber += 1
        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(allCars45Details)
        
        # self.driver.quit()

        return df

    except Exception as e:
        print(f"An error occurred: {e}")