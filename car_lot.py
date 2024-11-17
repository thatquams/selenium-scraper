from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from selenium.webdriver.common.by import By 
from datetime import date
from selenium import webdriver
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re
import datetime
from selenium.webdriver.chrome.options import Options

chrome_options = Options() 

chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")   # Required for AWS environments
chrome_options.add_argument("--disable-dev-shm-usage")  # Prevent resource issues
chrome_options.add_argument("--disable-gpu")  # Optional for headless
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--window-size=1920,1080")  # Necessary for headless rendering


def scrapeCarLots(delay, dealer, maxPage):
    allCarsInformation = []
    driver = webdriver.Chrome(options=chrome_options)
    
    currentPage = 1
    try:
        # Initialize the website URL
        base_url = f"https://carlots.ng/dealer-filter/{dealer}/city,;category,;page,1;"
        driver.get(base_url)

        while currentPage <= maxPage:
            print(f"Scraping Page {currentPage}/{maxPage}")

            try:
                # Get car overview links
                carOverview = WebDriverWait(driver, delay).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "title"))
                )[:3]
                carLinks = [overview.get_attribute("href") for overview in carOverview]

                # Scrape details for each car
                for link in carLinks:
                    driver.get(link)

                    try:
                        if str(dealer) == "kingsley-awogbami":
                        
                            carDetails = driver.find_element(By.XPATH, "//h1[@class='row']").text
                            carParentAttrs = WebDriverWait(driver, delay).until(
                                EC.presence_of_all_elements_located((By.CLASS_NAME, "cap-show-data"))
                            )

                            carBrand = carParentAttrs[0].text.split()[-1]
                            carModel = carParentAttrs[1].text.split()[-1]
                            carTransmission = carParentAttrs[3].text.split()[-1]
                            carPrice = driver.find_element(By.CLASS_NAME, "price-row").text
                        
                            fuelType = carParentAttrs[5].text.split()[-1]
                            carColour = carParentAttrs[6].text.split()[-1]
                            carYear = carParentAttrs[7].text.split()[-1]
                            dateScraped = datetime.date.today()

                            # Determine car condition
                            def getCarCondition(details):
                                if re.search(r"[pP]re-[Oo]wned|Nigerian", details):
                                    return "Nigerian Used"
                                elif re.search(r"[Tt]okunbo|Foreign", details):
                                    return "Foreign Used"
                                else:
                                    return "Brand New"

                            carCondition = getCarCondition(carDetails)
                            # Append car information

                            carsInformation = {
                                                "Car Id" : link, "Scraped Date":dateScraped,
                                                "Brand": carBrand, "Model": carModel,
                                                "Condition": carCondition, "Year": carYear, "Transmission": carTransmission, "Color":carColour,
                                                "Mileage": "", "Fuel Type":fuelType, "Price": carPrice
                            }
                            
                            allCarsInformation.append(carsInformation)
                            
                        else:
                            carDetails = driver.find_element(By.XPATH, "//h1[@class='row']").text
                            carParentAttrs = WebDriverWait(driver, delay).until(
                                EC.presence_of_all_elements_located((By.CLASS_NAME, "cap-show-data"))
                            )

                            carBrand = carParentAttrs[0].text.split()[-1]
                            carModel = carParentAttrs[1].text.split()[-1]
                            carTransmission = carParentAttrs[3].text.split()[-1]
                            carPrice = driver.find_element(By.CLASS_NAME, "price-row").text
                            fuelType = carParentAttrs[4].text.split()[-1]
                            carColour = carParentAttrs[5].text.split()[-1]
                            carYear = carParentAttrs[6].text.split()[-1]
                            
                            # Determine car condition
                            def getCarCondition(details):
                                if re.search(r"[pP]re-[Oo]wned|Nigerian", details):
                                    return "Nigerian Used"
                                elif re.search(r"[Tt]okunbo|Foreign", details):
                                    return "Foreign Used"
                                else:
                                    return "Brand New"
                            carCondition = getCarCondition(carDetails)
                            dateScraped = datetime.date.today()
                            
                            carsInformation = {
                                                "Car Id" : link, "Scraped Date":dateScraped,
                                                "Brand": carBrand, "Model": carModel,
                                                "Condition": carCondition, "Year": carYear, "Transmission": carTransmission, "Color":carColour,
                                                "Mileage": "", "Fuel Type":fuelType, "Price": carPrice
                            }
                            
                            allCarsInformation.append(carsInformation)
                            
                    except NoSuchElementException as ne:
                        print(f"Error extracting car details: {ne}")
                    except TimeoutException as te:
                        print(f"Timeout while extracting car details: {te}")

                # Prepare next page URL
                nextPageUrl = f"https://carlots.ng/dealer-filter/{dealer}/city,;category,;page,{currentPage + 1};"
                driver.get(nextPageUrl)

                # Increment the page counter
                currentPage += 1

            except NoSuchElementException as ne:
                print(f"Error navigating page: {ne}")
                
                break
            except TimeoutException as te:
                print(f"Timeout while loading page: {te}")
                break

            df = pd.DataFrame(allCarsInformation)
            # df.to_csv("test_data.csv")
        # Return the scraped data as a DataFrame
        return df

    except Exception as e:
        print(f"An unexpected error occurred: {e}")