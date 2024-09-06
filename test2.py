import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

def is_page_scrollable(driver):
    # Check if page is scrollable
    window_height = driver.execute_script("return window.innerHeight")
    page_height = driver.execute_script("return document.body.scrollHeight")
    return page_height > window_height

def scroll_page(driver, scroll_pause_time=2, max_scrolls=30):
    scrolls = 0
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while scrolls < max_scrolls:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait for new page segment to load
        time.sleep(scroll_pause_time)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            # If the page height hasn't changed, it means no more content is loading
            print(f"Scroll stopped after {scrolls} scrolls")
            break
        
        last_height = new_height
        scrolls += 1

def scrapeJiji(website,size):
    allResults = []
    
    # listOfEnginSizes = list(range(2000, 3000,100)) 
    listOfEnginSizes = [2000,2100]
    # + list(range(4200, 4900,100)) + [5300,5400,5500,5600, 5700, 6000, 6500]
    # listOfEnginSizes = list(range(3000, 3300, 100))
    """
    allBrands = ["Lexus", "Toyota", "Mercedes-Benz", "Honda", "Hyundai", "Acura", 
            "BMW", "Audi", "Bentley", "Cadillac", "Brabus",
            "Chevrolet", "Changan", "Chrysler", "Dodge", "Ferrari",
            "Ford", "GAC", "GMC", "Infiniti", "Jaguar", "Jeep", "Kia", 
            "Land Rover", "Lamborghini", "Lincoln", "Maserati", "Mazda", "Mini",
            "Mitsubichi", "Nissan", "Opel", "Peugeot", "Pontiac", "Porsche", 
            "Rolls-Royce", "Rover", "Scion", "Subari", "Suzuki", "Volkswagen", "Volvo"]
    """
    
    driver.get(website + f"?filter_attr_1363_engine_size={size}")

    # Check if the page is scrollable
    if is_page_scrollable(driver):
        scroll_page(driver, scroll_pause_time=2, max_scrolls=50)
    else:
        print("Page is not scrollable, collecting available data")

    carsOverview = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='masonry-item']/div/a")))
    carHrefs = [href.get_attribute("href") for href in carsOverview]

    for link in carHrefs:
        driver.get(link)

        try:
            seeMoreButton = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "fw-button.qa-fw-button.fw-button--type-primary-link-like.fw-button--size-small")))
            if seeMoreButton.is_displayed():
                seeMoreButton.click()
        except Exception as e:
            print(f"See more button not found: {str(e)}")
        
        otherElements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "b-advert-attribute__value")))
        # cylinders = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "b-advert-attribute")))
        cylinders = driver.find_elements(By.CLASS_NAME, "b-advert-attribute")

        engineSize = [ele.text for ele in otherElements if "cc" in ele.text]; horsePower = [ele.text for ele in otherElements if "hp" in ele.text]

        engineType = " ".join(
            ele.text
            for ele in cylinders
            if "CYLINDERS" in ele.find_element(By.CLASS_NAME, "b-advert-attribute__key").text)
# )            engineType = [item for sublist in engineType for item in sublist]
        
        carId = link
        dateScraped = time.strftime('%Y-%m-%d')
        carBrand = driver.find_element(By.XPATH, "//div[@class='b-advert-attributes--tiles']//div[@itemprop='brand']").text.strip()
        carModel = driver.find_element(By.XPATH, "//div[@class='b-advert-attributes--tiles']//div[@itemprop='model']").text.strip()
        carYear = driver.find_element(By.XPATH, "//div[@class='b-advert-attributes--tiles']//div[@itemprop='productionDate']").text.strip()
        carBodyColor = driver.find_element(By.XPATH, "//h1[@itemprop='name']").text.split()[-1].strip()
        carCondition = driver.find_element(By.XPATH, "//div[@class='b-advert-icon-attribute']//span[@itemprop='itemCondition']").text.strip()
        carTransmission = driver.find_element(By.XPATH, "//div[@class='b-advert-icon-attribute']//span[@itemprop='vehicleTransmission']").text.strip()
        carPrice = driver.find_element(By.XPATH, "//div[@itemprop='price']").text.strip()

        # Locate all elements with the class name "b-advert-attribute"
        carModelTrimElements = driver.find_elements(By.CLASS_NAME, "b-advert-attribute")

        # Initialize a variable to store the car model trim if found
        carModelTrim = None

        # Iterate through each located element
        for car in carModelTrimElements:
            # Split the text content into lines
            lines = list(car.text.splitlines())
            # Check if the last line is "TRIM"
            if "TRIM" in lines:
                carModelTrim = lines[0]  # Get the first line as car model trim
                # carModel = " ".join((carModel, carModelTrim))

        data = {
            "Car Id": carId, "Scraped Date": dateScraped,"Brand": carBrand,
            "Model": carModel,"Trim":carModelTrim, "Condition": carCondition, "Year": carYear,
            "Transmission": carTransmission, "Colour": carBodyColor, 
            "Engine Size":"".join(engineSize), "Horse Power":"".join(horsePower), 
            "Engine Type": engineType, "Price": carPrice
        }

        allResults.append(data)
    
    resultDf = pd.DataFrame(allResults, columns=data.keys(), index=range(0, len(allResults)))
    resultDf.drop_duplicates(inplace=True)
    resultDf.to_csv(f"{size}ccCars.csv")
    
    return allResults

jijiWebsite = "https://www.jiji.ng/cars"

# Call the scrape function
callJiji = scrapeJiji(jijiWebsite, 3400)

# Print the result DataFrame
print(callJiji)
