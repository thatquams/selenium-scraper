from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from datetime import date
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome()

jijiWebsite = "https://jiji.ng/cars"
# website = "https://jiji.ng/ajah/cars/ford-explorer-2013-rX0yvhE30IGJPHutWgzptoNB.html?page=1&pos=1&cur_pos=1&ads_per_page=22&ads_count=93802&lid=2ghPA6tyaU9W5lpC&indexPosition=0"
allResults = []

   # Function to scroll the page
def scroll_page(driver, scroll_pause_time, max_scrolls):
    current_scrolls = 0
    while current_scrolls < max_scrolls:
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(scroll_pause_time)
        current_scrolls += 1

def scrapeJijiUsersProfile(website):
    
    driver.get(website)
    allResults = []
    
    # allCarsLinks = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@data-column='0']")))

    # scroll_page(driver, scroll_pause_time=2, max_scrolls=40)
    scroll_page(driver, scroll_pause_time=3, max_scrolls=50)

    a_tags_parent = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='masonry-item']/div/a")))

    href = [link.get_attribute("href") for link in a_tags_parent] 
        
    for link in href:
        
        dealershipLocation = driver.find_element(By.XPATH, "//div[@class='b-list-advert__region']/span").text.split(",")[0].strip()
        # dealershipLocation = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        #     (By.XPATH, "//div[@class='b-list-advert__region']/span"))).text.split(",")[0].strip()
        
        driver.get(link)
        # dealershipBusinessName = driver.find_element(By.XPATH, "//div[@class='b-seller-block__name']").text.strip()
        userProfile = driver.find_element(By.XPATH, "//a[@class='b-seller-block__avatar__wrapper']").get_attribute("href")
        
        driver.get(userProfile)
        
        phoneNumber = driver.title.split("|")[1].strip()
        dealershipBusinessName = driver.title.split("|")[0].strip()
        
        numberOfInventories = driver.find_element(By.XPATH, "//div[@class='b-seller-top-categories__item-center']").text.split()[0].strip("•")
        
        resultDict = {
            "Business Name" : dealershipBusinessName,
            "Location" : ''.join(dealershipLocation),
            "Phone Numbers" : phoneNumber,
            "Number Of Listings" : numberOfInventories
        }

        allResults.append(resultDict)
        
    resultDf = pd.DataFrame(allResults, columns=resultDict.keys(), index=range(0, len(allResults)))
    resultDf.drop_duplicates(inplace=True)
    resultDf.to_csv("Jiji Dealers Phone Numbers.csv")
    
    return resultDf


def scrapeJiji(website, *enginSizeFilterAttr):
    """
    allBrands = ["Toyota", "Lexus", "Mercedes-Benz", "Honda", "Hyundai", "Acura", 
          "BMW", "Audi", "Bentley", "Cadillac", "Brabus",
         "Chevrolet", "Changan", "Chrysler", "Dodge", "Ferrari",
         "Ford", "GAC", "GMC", "Infiniti", "Jaguar", "Jeep", "Kia", 
         "Land Rover", "Lamborghini", "Lincoln", "Maserati", "Mazda", "Mini",
         "Mitsubichi", "Nissan", "Opel", "Peugeot", "Pontiac", "Porsche", 
         "Rolls-Royce", "Rover", "Scion", "Subari", "Suzuki", "Volkswagen", "Volvo"]
         """
    
    driver.get(f"{website}?filter_attr_1363_engine_size={enginSizeFilterAttr}")
        
    # driver.get(website)

    # scroll_page(driver, scroll_pause_time=3, max_scrolls=150)

    carsOverview = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='masonry-item']/div/a")))[:10]
    
    carHrefs = [href.get_attribute("href") for href in carsOverview]

    for link in carHrefs:
        
        driver.get(link)
        
        # seeMoreButton = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME, "qa-fw-button")))
        seeMoreButton = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME, "fw-button.qa-fw-button.fw-button--type-primary-link-like")))
        time.sleep(2)
        
        # seeMoreButton = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME, "fw-button--type-primary-link-like")))
        if seeMoreButton.is_displayed():
            seeMoreButton.click()
            
            # otherElements = driver.find_elements(By.CLASS_NAME, "b-advert-attribute__value")

            try:
                """
                engineSize = [ele.text for ele in otherElements if "cc" in ele.text]; horsePower = [ele.text for ele in otherElements if "hp" in ele.text]
                # engineType = [ele.text for ele in otherElements if re.search(r"\d", ele.text)]
                engineType = [str(ele.text) for ele in otherElements if ele.text.strip() in ("4", "6", "8", "10", "12")]
                """
                carId = link
                dateScraped = date.today()
                # carLocation = driver.find_element(By.CLASS_NAME, "b-advert-info-statistics").text.split(",")[0].strip()
                carBrand = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='b-advert-attributes--tiles']//div[@itemprop='brand']"))).text.strip()
                carModel = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='b-advert-attributes--tiles']//div[@itemprop='model']"))).text.strip()
                carYear = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='b-advert-attributes--tiles']//div[@itemprop='productionDate']"))).text.strip()
                carBodyColor = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//h1[@itemprop='name']"))).text.split()[-1].strip()
                carCondition = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='b-advert-icon-attribute']//span[@itemprop='itemCondition']"))).text.strip()
                carTransmission = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='b-advert-icon-attribute']//span[@itemprop='vehicleTransmission']"))).text.strip()
                carPrice = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@itemprop='price']"))).text.strip()
                
            except NoSuchElementException as e:
                print(f"Element {e} Not Found!!!")
                    
        # scroll_page(driver, scroll_pause_time=3, max_scrolls=2)
        
        
        # Locate all elements with the class name "b-advert-attribute"
        # carModelTrimElements = driver.find_elements(By.CLASS_NAME, "b-advert-attribute")

        # Initialize a variable to store the car model trim if found
        # carModelTrim = None

        # Iterate through each located element
        # for car in carModelTrimElements:
        #     # Split the text content into lines
        #     lines = list(car.text.splitlines())
        #     # Check if the last line is "TRIM"
        #     if "TRIM" in lines:
        #         carModelTrim = lines[0]  # Get the first line as car model trim
        #         # carBrand = carBrand,  carModelTrim; 
        #         carModel = " ".join((carModel, carModelTrim))
                # break  # Exit the loop once found
            
        data = {
            "Car Id" : carId, "Scraped Date":dateScraped,
            "Brand": carBrand, "Model": carModel, "Condition": carCondition, "Year": carYear,
            "Transmission": carTransmission,"Colour":carBodyColor,"Price":carPrice
            }
        
        allResults.append(data)
        
    # resultDf = pd.DataFrame(allResults, columns=data.keys(), index=range(0, len(allResults)))
    # resultDf.drop_duplicates(inplace=True)
    # resultDf.to_csv("res.csv")

    
# return df[["Car Id", "Brand", "Model", "Colour"]]
    return allResults

# Car Id Scraped Date   Brand    Model     Condition  Year Transmission  Colour   Price

listOfEngineSize = list(range)
callJiji = scrapeJiji(jijiWebsite)


print(callJiji)