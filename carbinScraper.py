from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd


class CarbinWebscraper:
    def __init__(self):
        self.betaCarsDetails = []
        self.allCars45Details = []
        self.allAutoChekDetails = []

        self.driver = webdriver.Chrome()

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

                for href in hrefs:
                    self.driver.get(href)  # navigate links

                    try:
                        carBrand = self.driver.find_element(By.XPATH, "//*[@itemprop='description']/div/p").text
                        carModel = self.driver.find_element(By.XPATH, "//*[@itemprop='description']/div[2]/p").text
                        yearOfManufacture = self.driver.find_element(By.XPATH, "//*[@itemprop='description']/div[3]/p").text
                        carCondition = self.driver.find_element(By.XPATH,"//div[@class='main-details__tags flex wrap']/span[1]").text
                        transmissionType = self.driver.find_element(By.XPATH,"//div[@class='main-details__tags flex wrap']/span[2]").text
                        Price = self.driver.find_element(By.XPATH, "//div[@class='main-details__name']/h5").text.strip("₦ ")

                        # Create a dictionary to store the scraped data
                        CarDetails = {
                            "Brand": carBrand, "Model": carModel,
                            "Condition": carCondition, "Year": yearOfManufacture, "Transmission": transmissionType,
                            "Price": Price}

                        # Append all car details
                        self.allCars45Details.append(CarDetails)

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

            return df

        except Exception as e:
            print(f"An error occurred: {e}")

        # finally:
            # Close the WebDriver
            # self.driver.quit()

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

                        carBrand = self.driver.find_element(By.XPATH, "//*[@class='MuiTypography-root MuiTypography-h6 css-1g399u0']").text.split()[1]
                        carModel = self.driver.find_element(By.XPATH, "//*[@class='MuiTypography-root MuiTypography-h6 css-1g399u0']").text.split(maxsplit=2)[2]
                        yearOfManufacture = self.driver.find_element(By.XPATH, "//*[@class='MuiTypography-root MuiTypography-h6 css-1g399u0']").text.split()[0]

                        Price = self.driver.find_element(By.XPATH, "//*[@class='MuiTypography-root MuiTypography-body1 css-14bhqez']").text.strip("₦ ")
                        Condition = self.driver.find_element(By.XPATH, "//div[@class='MuiStack-root css-j7qwjs']").text.split("\n",maxsplit=3)[0] + " Used"

                        otherCarFeatures = self.driver.find_elements(By.XPATH, "//p[@class='MuiTypography-root MuiTypography-body1 css-1pldev7']")
                        carTransmission = otherCarFeatures[1].text

                        carDetails = {
                            "Brand": carBrand, "Model": carModel, "Condition": Condition,
                            "Year": yearOfManufacture, "Transmission": carTransmission,
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

            return autoChekDf
        except Exception as e:
            print(f"An error occurred: {e}")

        # finally:
            # Close the WebDriver
            # self.driver.quit()

    def betaCars(self, maxPageNumber):

        try:
            betaCarsWebsite = "https://www.betacar.ng/foreign-used-car#/pageSize=32&orderBy=10&pageNumber=1"
            currentPageNumber = 1

            while currentPageNumber <= maxPageNumber:
                # navigate to beta cars website
                self.driver.get(betaCarsWebsite)

                betaCarsInventoriesOverview = self.driver.find_elements(By.XPATH, "//h2[@class='product-title']/a")
                betaCarsHrefs = [href.get_attribute("href") for href in betaCarsInventoriesOverview]

                for href in betaCarsHrefs:
                    self.driver.get(href)

                    try:
                        carBrand = self.driver.find_element(By.XPATH, "//h1[@itemprop='name']").text.split(maxsplit=6)[1]
                        carModel = self.driver.find_element(By.XPATH, "//h1[@itemprop='name']").text.split(maxsplit=6)[2]
                        Year = self.driver.find_element(By.XPATH, "//h1[@itemprop='name']").text.split(maxsplit=6)[0]
                        Price = self.driver.find_element(by=By.XPATH, value="//div[@class='product-price']/span[1]").text.strip("₦ ")
                        condition = "Foreign Used"
                        otherFeatures = self.driver.find_elements(by=By.XPATH, value="//tr/td[2]")
                        res = [feat.text for feat in otherFeatures]
                        carTransmission = res[2]

                        carDetails = {
                            "Brand": carBrand, "Model": carModel, "Condition": condition,
                            "Year": Year, "Transmission": carTransmission, "Price": Price
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

            return df

        except Exception as e:
            print(f"An error occurred: {e}")

        # finally:
        #     # Close the WebDriver
        #     self.driver.quit()

    def concatenateDataframes(self):
        try:
            # Call each scraping method to get the individual DataFrames
            df_cars45 = self.scrapeCars45(97)
            df_autoChek = self.scrapeAutoChek(70)
            df_betaCars = self.betaCars(2)

            # Concatenate the individual DataFrames into one
            combinedDf = pd.concat([df_cars45, df_autoChek, df_betaCars], ignore_index=True,axis=0)
            return combinedDf

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            # Close the WebDriver
            self.driver.quit()


scraper = CarbinWebscraper()
combined_data = scraper.concatenateDataframes()
print(combined_data)
