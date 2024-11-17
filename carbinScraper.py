from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
import time
import pandas as pd
import re
from selenium.webdriver.chrome.options import Options
import pymysql

options = Options()
options.headless = True

class CarbinWebscraper:
    def __init__(self):
        self.betaCarsDetails = []
        self.allCars45Details = []
        self.allAutoChekDetails = []
        self.allJijiDetails = []
        self.allCarsInformation = []

        self.driver = webdriver.Chrome(options=options)
        
    # Function to scroll the page
    def scroll_page(self, scroll_pause_time=3, max_scrolls=10):
        current_scrolls = 0
        while current_scrolls < max_scrolls:
            # Using self.driver to call execute_script since it's the WebDriver object
            self.driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(scroll_pause_time)
            current_scrolls += 1
            
    def restart_driver(self):
        self.driver.quit()
        # Initialize driver again
        return self.driver
    
    def scrapeCars45(self, maxPage):

        try:
            cars45Website = "https://www.cars45.com/listing?page=1"
            # Start from the first page
            currentPageNumber = 1

            while currentPageNumber <= maxPage:
                # Navigate to the current page
                self.driver.get(cars45Website)

                # Extract car links
                carOverviews = self.driver.find_elements(By.XPATH, "//section[@class='cars-grid grid']/a")
                hrefs = [carOverview.get_attribute("href") for carOverview in carOverviews]

                try:
                    for href in hrefs:
                        try:
                            self.driver.get(href)  # navigate links
                        except WebDriverException as e:
                            print(f"Error loading page {href}: {e}")


                        try:
                            carId = href
                            dateScraped = date.today()
                            carBrand = self.driver.find_element(By.XPATH, "//h1[@itemprop='name']").text.split()[0]
                            modelElement = self.driver.find_element(By.XPATH, "//div[@itemprop='description']//span[normalize-space()='Model']")
                            # Navigate to the preceding sibling p tag to extract the engine size value
                            carModel = modelElement.find_element(By.XPATH, "./preceding-sibling::p").text.strip()

                            carModel = self.driver.find_element(By.XPATH, "//h1[@itemprop='name']").text.split()[1]
                            carCondition = self.driver.find_element(By.XPATH,"//div[@class='main-details__tags flex wrap']/span[1]").text
                            transmissionType = self.driver.find_element(By.XPATH,"//div[@class='main-details__tags flex wrap']/span[2]").text
                            try:
                                carMileage = self.driver.find_element(By.XPATH, "//div[@class='main-details__tags flex wrap']/span[3]").text
                            except NoSuchElementException:
                                carMileage = "0 km"

                            carColour = self.driver.find_element(By.XPATH, "//h1[@itemprop = 'name']").text.split()[-1]
                            fuelType = self.driver.find_element(By.XPATH, "//img[contains(@src, '/_ipx/_/images/diesel.png')]/../span[@class='tab-content__svg__title']").text.strip()
                            
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
                            
                            yearOfManufacture = self.driver.find_element(By.XPATH, "//h1[@itemprop='name']").text
                            year_pattern = r'\b\d{4}\b'

                            # Search for the year pattern in the yearOfManufacture string
                            year_match = re.search(year_pattern, yearOfManufacture)
                            carYear = year_match.group()

                            Price = self.driver.find_element(By.XPATH, "//div[@class='main-details__name']/h5").text.strip("₦ ")
                            

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
                            self.allCars45Details.append(CarDetails)
                        except ConnectionError as error:
                            print(f"This error Occured {error}")
                            

                except NoSuchElementException as e:
                    print(f"Error scraping details: {e}")

                # print(f"Navigated to page {currentPageNumber}")

                # Construct the URL for the next page
                nextPageUrl = cars45Website.rsplit('=', 1)[0] + '=' + str(currentPageNumber + 1)
                # Navigate to the next page
                self.driver.get(nextPageUrl)

                cars45Website = nextPageUrl

                # Increment the page number for the next iteration
                currentPageNumber += 1
            # Convert the list of dictionaries to a DataFrame
            df = pd.DataFrame(self.allCars45Details)
            
            # self.driver.quit()

            return df

        except Exception as e:
            print(f"An error occurred: {e}")

    def scrapeAutoChek(self, maxPage):

        try:
            autoChekWebsite = "https://autochek.africa/ng/cars-for-sale?page_number=1"
            currentPageNumber = 1

            while currentPageNumber <= maxPage:
                self.driver.get(autoChekWebsite)

                autoChekInventoriesOverview = self.driver.find_elements(By.XPATH, "//*[@class='MuiBox-root css-1jke4yk']/a")
                autoChekHrefs = [href.get_attribute("href") for href in autoChekInventoriesOverview]

                for href in autoChekHrefs:
                    try:
                        self.driver.get(href)

                        carId = href
                        dateScraped = date.today()
                        
                        # get all cars features and store in list("allFeats")
                        allFeats = self.driver.find_element(By.TAG_NAME, "h5").text.split(maxsplit=3)
                        carBrand = allFeats[0]
                        carModel = allFeats[1:3] if len(allFeats) <= 4 else allFeats[1]
                        yearOfManufacture = self.driver.find_element(By.TAG_NAME, "h5").text.split(maxsplit=3)[-1].split(" - ")[-1].strip()

                        
                        Price = self.driver.find_element(By.XPATH, "//*[@class='MuiTypography-root MuiTypography-body1 css-14bhqez']").text.strip("₦ ")
                        Condition = self.driver.find_element(By.XPATH, "//div[@class='MuiStack-root css-j7qwjs']").text.split("\n",maxsplit=3)[0] + " Used"
                        otherCarFeatures = self.driver.find_elements(By.XPATH, "//p[@class='MuiTypography-root MuiTypography-body1 css-1pldev7']")
                        carTransmission = otherCarFeatures[1].text
                        fuelType = otherCarFeatures[2].text
                        carColour = otherCarFeatures[4].text
                        carMileage = self.driver.find_element(By.XPATH, "//*[@class='MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-1 css-tuxzvu']").text.split('\n')[1]
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


                        self.allAutoChekDetails.append(carDetails)

                    except NoSuchElementException as e:
                        print(f"Error scraping details: {e}")

                # Construct the URL for the next page
                nextPageUrl = autoChekWebsite.rsplit('=', 1)[0] + '=' + str(currentPageNumber + 1)

                # Navigate to the next page
                self.driver.get(nextPageUrl)

                # Update autoChekWebsite for the next iteration
                autoChekWebsite = nextPageUrl

                # Increment the page number for the next iteration
                currentPageNumber += 1
                # print(f"Navigated to page {currentPageNumber}")

            # Convert the list of dictionaries to a DataFrame
            autoChekDf = pd.DataFrame(self.allAutoChekDetails)

            self.driver.quit()
            return autoChekDf
        except Exception as e:
            print(f"An error occurred: {e}")

    def betaCars(self, maxPageNumber):

        try:
            betaCarsWebsite = "https://www.betacar.ng/all-used-cars#/pageSize=32&orderBy=10&pageNumber=1"
            currentPageNumber = 1

            while currentPageNumber <= maxPageNumber:
                # navigate to beta cars website
                self.driver.get(betaCarsWebsite)

                betaCarsInventoriesOverview = self.driver.find_elements(By.XPATH, "//h2[@class='product-title']/a")
                betaCarsHrefs = [href.get_attribute("href") for href in betaCarsInventoriesOverview]

                for href in betaCarsHrefs:
                    self.driver.get(href)

                    try:
                        carId = href
                        dateScraped = date.today()
                        carTitle = self.driver.find_element(By.XPATH, "//h1[@itemprop='name']").text
                        carBrand = self.driver.find_element(By.XPATH, "//h1[@itemprop='name']").text.split(maxsplit=6)[1]
                        carModel = self.driver.find_element(By.XPATH, "//h1[@itemprop='name']").text.split(maxsplit=6)[2]
                        Year = self.driver.find_element(By.XPATH, "//h1[@itemprop='name']").text.split(maxsplit=6)[0]
                        carCondition = lambda car : "Local Used" if ("Registered" in car) else "Foreign Used"
                        
                        otherFeatures = self.driver.find_elements(by=By.XPATH, value="//tr/td[2]")
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
                        Price = self.driver.find_element(by=By.XPATH, value="//div[@class='product-price']/span[1]").text.strip("₦ ")
                        
                        carDetails = {
                            "Car Id":carId, "Scraped Date" : dateScraped,
                            "Brand": carBrand, "Model": carModel, "Condition": carCondition(carTitle),
                            "Year": Year, "Transmission": carTransmission, "Color":carColour, "Mileage":carMileage,"Fuel Type":fuelType,
                            "Price": Price
                        }

                        self.betaCarsDetails.append(carDetails)

                    except NoSuchElementException as e:
                        print(f"Error scraping details: {e}")

                # Construct the URL for the next page
                nextPageUrl = betaCarsWebsite.rsplit('=', 1)[0] + '=' + str(currentPageNumber + 1)
                # Navigate to the next page
                self.driver.get(nextPageUrl)

                betaCarsWebsite = nextPageUrl

                # Increment the page number for the next iteration
                currentPageNumber += 1
                # Convert the list of dictionaries to a DataFrame
            df = pd.DataFrame(self.betaCarsDetails)
            self.driver.quit()
            return df

        except Exception as e:
            print(f"An error occurred: {e}")
    
    def scrapeJiji(self):
        try:
            self.driver.get("https://jiji.ng/cars?filter_attr_3_mileage__min=500&filter_attr_1165_fuel=Petrol")
            self.scroll_page()

            carsOverview = WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='masonry-item']/div/a")))
            carHrefs = [href.get_attribute("href") for href in carsOverview]

            for link in carHrefs:
                self.driver.get(link)

                try:
                    seeMoreButton = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "(//span[@class='fw-button__content'])[4]")))
                    if seeMoreButton.is_displayed():
                        seeMoreButton.click()
                except WebDriverException as e:
                    print(f"An Error Occurred: {e}")

                carId = link
                dateScraped = date.today()
                
                carBrand = self.driver.find_element(By.XPATH, "//div[@class='b-advert-attributes--tiles']//div[@itemprop='brand']").text.strip()
                carModel = self.driver.find_element(By.XPATH, "//div[@class='b-advert-attributes--tiles']//div[@itemprop='model']").text.strip()
                carYear = self.driver.find_element(By.XPATH, "//div[@class='b-advert-attributes--tiles']//div[@itemprop='productionDate']").text.strip()
                carMileage = self.driver.find_element(By.XPATH, "//span[@itemprop='mileageFromOdometer']").text.strip()
                carBodyColor = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, "//h1[@itemprop='name']"))).text.split()[-1].strip()
                carCondition = self.driver.find_element(By.XPATH, "//div[@class='b-advert-icon-attribute']//span[@itemprop='itemCondition']").text.strip()
                carTransmission = self.driver.find_element(By.XPATH, "//div[@class='b-advert-icon-attribute']//span[@itemprop='vehicleTransmission']").text.strip()
                carPrice = self.driver.find_element(By.XPATH, "//div[@itemprop='price']").text.strip()
                
                # engineSizeDivElement = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='b-advert-attribute']//div[normalize-space()='Number of Cylinders']")))
                # carEngineSize = engineSizeDivElement.find_element(By.XPATH, "./preceding-sibling::div").text.strip() if engineSizeDivElement else None
                
                data = {
                    "Car Id": carId, "Scraped Date": dateScraped,
                    "Brand": carBrand, "Model": carModel, "Condition": carCondition,
                    "Year": carYear, "Transmission": carTransmission, "Color": carBodyColor, 
                    "Mileage": carMileage, "Price": carPrice
                }
                
                self.allJijiDetails.append(data)

            # Create and return the DataFrame at the end
            df = pd.DataFrame(self.allJijiDetails)
            return df

        except Exception as e:
            print(f"Error encountered: {e}")
            return pd.DataFrame(self.allJijiDetails)  # Return what data was collected so far, if any
    
    def scrapeCarLots(self, delay, dealer, maxPage=2):
        currentPage = 1

        try:
            # Initialize the website URL
            base_url = f"https://carlots.ng/dealer-filter/{dealer}/city,;category,;page,1;"
            self.driver.get(base_url)

            while currentPage <= maxPage:
                print(f"Scraping Page {currentPage}/{maxPage}")

                try:
                    # Get car overview links
                    carOverview = WebDriverWait(self.driver, delay).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, "title"))
                    )[:3]
                    carLinks = [overview.get_attribute("href") for overview in carOverview]

                    # Scrape details for each car
                    for link in carLinks:
                        self.driver.get(link)

                        try:
                            if str(dealer) == "kingsley-awogbami":
                            
                                carDetails = self.driver.find_element(By.XPATH, "//h1[@class='row']").text
                                carParentAttrs = WebDriverWait(self.driver, delay).until(
                                    EC.presence_of_all_elements_located((By.CLASS_NAME, "cap-show-data"))
                                )

                                carBrand = carParentAttrs[0].text.split()[-1]
                                carModel = carParentAttrs[1].text.split()[-1]
                                carTransmission = carParentAttrs[3].text.split()[-1]
                                carPrice = self.driver.find_element(By.CLASS_NAME, "price-row").text
                            
                                fuelType = carParentAttrs[5].text.split()[-1]
                                carColour = carParentAttrs[6].text.split()[-1]
                                carYear = carParentAttrs[7].text.split()[-1]

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
                                    "Car Details": carDetails, "Brand": carBrand, "Model": carModel,
                                    "Year": carYear, "Transmission": carTransmission, "Condition": carCondition,
                                    "Fuel Type": fuelType, "Mileage": "", "Colour": carColour, "Price": carPrice}
                                
                                self.allCarsInformation.append(carsInformation)
                                
                            else:
                                carDetails = self.driver.find_element(By.XPATH, "//h1[@class='row']").text
                                carParentAttrs = WebDriverWait(self.driver, delay).until(
                                    EC.presence_of_all_elements_located((By.CLASS_NAME, "cap-show-data"))
                                )

                                carBrand = carParentAttrs[0].text.split()[-1]
                                carModel = carParentAttrs[1].text.split()[-1]
                                carTransmission = carParentAttrs[3].text.split()[-1]
                                carPrice = self.driver.find_element(By.CLASS_NAME, "price-row").text
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
                                
                                carsInformation = {
                                    "Car Details": carDetails, "Brand": carBrand, "Model": carModel,
                                    "Year": carYear, "Transmission": carTransmission, "Condition": carCondition,
                                    "Fuel Type": fuelType, "Mileage": "", "Colour": carColour, "Price": carPrice}
                                
                                self.allCarsInformation.append(carsInformation)
                                
                                
                            

                        except NoSuchElementException as ne:
                            print(f"Error extracting car details: {ne}")
                        except TimeoutException as te:
                            print(f"Timeout while extracting car details: {te}")

                    # Prepare next page URL
                    nextPageUrl = f"https://carlots.ng/dealer-filter/{dealer}/city,;category,;page,{currentPage + 1};"
                    self.driver.get(nextPageUrl)

                    # Increment the page counter
                    currentPage += 1

                except NoSuchElementException as ne:
                    print(f"Error navigating page: {ne}")
                    
                    break
                except TimeoutException as te:
                    print(f"Timeout while loading page: {te}")
                    break

                df = pd.DataFrame(self.allCarsInformation)
            # Return the scraped data as a DataFrame
            print(df)
            return df

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
    def concatenateDataframes(self):
        # Call each scraping method to get the individual DataFrames
        
        df_cars45 = self.scrapeCars45(100)
        df_autoChek = self.scrapeAutoChek(100) 
        df_betaCars = self.betaCars(20)
        
        # df_cars45 = self.scrapeCars45(1)
        # df_autoChek = self.scrapeAutoChek(1) 
        # df_betaCars = self.betaCars(1)
        # Concatenate the individual DataFrames into one
        combinedDf = pd.concat([df_cars45, df_autoChek, df_betaCars], ignore_index=True,axis=0)
        
        self.driver.quit()
        return combinedDf


    def connectToDB(self):
        # extractedData = self.concatenateDataframes()
        extractedData = self.scrapeCars45(1)

        # extractedData = pd.concat([df_cars45, df_betaCars, df_autoChek], axis=0, ignore_index=True)
        
        mysqlConnection = pymysql.connect(host="16.171.196.125", user="forge", password="BuKmMOBmefOxBSC4fYDU", database="CarInfoHub")
        # return extractedData
        
        # for data in extractedData:
        
        # Prepare the SQL INSERT statement
        insert_query = """
        INSERT INTO carCatalogue (Id, created_at, Brand, Model, `Condition`, Year, Transmission, Colour, Mileage, `Fuel Type`,Price)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)
        """
        
        try:
            # Create a cursor object to execute the queries
            with mysqlConnection.cursor() as cursor:
                # Loop through each row in the DataFrame and insert the data
                for index, row in extractedData.iterrows():
                    cursor.execute(insert_query, (
                        row["Car Id"],
                        row['Scraped Date'],
                        row['Brand'],
                        row['Model'],
                        row['Condition'],
                        row['Year'],
                        row['Transmission'],
                        row['Color'],
                        row['Mileage'],
                        row['Fuel Type'],
                        row['Engine Type'],
                        row['Price']
                    ))
            
            # Commit the transaction
            mysqlConnection.commit()
            print("Data inserted successfully!")
            self.driver.quit()
            return extractedData
            # return pd.DataFrame(mysqlConnection)

        except Exception as e:
            print(f"An error occurred: {e}")
            self.driver.quit()
        
scraper = CarbinWebscraper()
# combined_data = scraper.connectToDB()
combined_data = scraper.scrapeCarLots(10, "kelvin-obene")
print(combined_data)
