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
    
    driver.get(f"{website}?filter_attr_1363_engine_size={enginSizeFilterAttr}")
        
    carsOverview = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='masonry-item']/div/a")))[:10]
    
    carHrefs = [href.get_attribute("href") for href in carsOverview]

    for link in carHrefs:
        
        driver.get(link)
        
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
                    
        data = {
            "Car Id" : carId, "Scraped Date":dateScraped,
            "Brand": carBrand, "Model": carModel, "Condition": carCondition, "Year": carYear,
            "Transmission": carTransmission,"Colour":carBodyColor,"Price":carPrice
            }
        
        allResults.append(data)
        return allResults