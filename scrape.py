from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd


def scrape_cars45_data():
    # Initialize the WebDriver (e.g., Chrome)
    driver = webdriver.Chrome()
    allCarDetails = []  # Initialize an empty list to store the scraped car details
    try:
        # Initial URL
        website = "https://www.cars45.com/listing?page=1"
        maxPage = 10  # Define the maximum page number you want to navigate to

        # Start from the first page
        currentPageNumber = 1

        while currentPageNumber <= maxPage:
            # Navigate to the current page
            driver.get(website)

            # Extract car links
            carOverviews = driver.find_elements(By.XPATH, "//section[@class='cars-grid grid']/a")
            hrefs = [carOverview.get_attribute("href") for carOverview in carOverviews]

            for href in hrefs:
                driver.get(href)  # navigate links

                try:
                    carBrand = driver.find_element(By.XPATH, "//*[@itemprop='description']/div/p").text
                    carModel = driver.find_element(By.XPATH, "//*[@itemprop='description']/div[2]/p").text
                    yearOfManufacture = driver.find_element(By.XPATH, "//*[@itemprop='description']/div[3]/p").text
                    carBodyColour = driver.find_element(By.XPATH, "//div[@class='main-details__name']/h1").text.split()[-1]
                    carCondition = driver.find_element(By.XPATH, "//div[@class='main-details__tags flex wrap']/span[1]").text
                    transmissionType = driver.find_element(By.XPATH,"//div[@class='main-details__tags flex wrap']/span[2]").text
                    carMileage = driver.find_element(By.XPATH, "//div[@class='main-details__tags flex wrap']/span[3]").text.split()[0]
                    carPrices = driver.find_element(By.XPATH, "//div[@class='main-details__name']/h5").text

                    # Create a dictionary to store the scraped data
                    CarDetails = {
                        "carBrand": carBrand, "carModel": carModel, "carBodyColour": carBodyColour,
                        "carCondition": carCondition,
                        "yearOfManufacture": yearOfManufacture, "transmissionType": transmissionType,
                        "carMileage": carMileage, "carPrice": carPrices
                    }

                    # Append all car details
                    allCarDetails.append(CarDetails)

                except NoSuchElementException as e:
                    print(f"Error scraping details: {e}")

            print(f"Navigated to page {currentPageNumber}")

            # Construct the URL for the next page
            nextPageUrl = website.rsplit('=', 1)[0] + '=' + str(currentPageNumber + 1)
            # Navigate to the next page
            driver.get(nextPageUrl)

            # Increment the page number for the next iteration
            currentPageNumber += 1
        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(allCarDetails)

        # Save the DataFrame to a CSV file
        df.to_csv("cars45.csv", index=False)

        return df

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the WebDriver
        driver.quit()


# Call the function to execute the scraping
result = scrape_cars45_data()
print(result)