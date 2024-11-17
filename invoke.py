import pandas as pd
import pymysql
from betaCars import betaCar
from autochek import scrapeAutoChek
from cars45 import scrapeCars45
from car_lot import scrapeCarLots
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re

chrome_options = Options() 

chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")   # Required for AWS environments
chrome_options.add_argument("--disable-dev-shm-usage")  # Prevent resource issues
chrome_options.add_argument("--disable-gpu")  # Optional for headless
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--window-size=1920,1080")  # Necessary for headless rendering

driver = webdriver.Chrome(options=chrome_options)

def concatenateDataframes():
    # Call each scraping method to get the individual DataFrames
    
    df_cars45 = scrapeCars45(100); 
    df_autoChek = scrapeAutoChek(100); df_betaCars = betaCar(20)
    kingsleyCarLots = scrapeCarLots(10, "kingsley-awogbami", 7)
    kelvinCarLots = scrapeCarLots(10, "kelvin-obene", 26)
    
    combinedDf = pd.concat([df_autoChek, df_betaCars, kingsleyCarLots,kelvinCarLots, df_cars45], ignore_index=True,axis=0)

    # Filter rows where 'Price' contains digits
    combinedDf = combinedDf[combinedDf['Price'].astype(str).apply(lambda x: bool(re.search("\d+", x)))]
    # combinedDf.to_csv("test.csv")
    # combinedDf = pd.concat([df_autoChek, df_betaCars, kingsleyCarLots,kelvinCarLots, df_cars45], ignore_index=True,axis=0)
    
    driver.quit()
    return combinedDf


def connectToDB():
    extractedData = concatenateDataframes()

    mysqlConnection = pymysql.connect(host="16.171.196.125", user="forge", password="BuKmMOBmefOxBSC4fYDU", database="CarInfoHub")
    # return extractedData
    
    # for data in extractedData:
    
    # Prepare the SQL INSERT statement
    insert_query = """
    INSERT INTO carCatalogue (Id, created_at, Brand, Model, `Condition`, Year, Transmission, Colour, Mileage, `Fuel Type`,Price)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
    """
    
    try:
        # Create a cursor object to execute the queries
        with mysqlConnection.cursor() as cursor:
            cursor.execute("DELETE FROM carCatalogue")
            print("Table Cleared...........")
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
                    row['Price']
                ))
        
        # Commit the transaction
        mysqlConnection.commit()
        print("Data inserted successfully!")
        driver.quit()
        return extractedData
        # return pd.DataFrame(mysqlConnection)

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.quit()
       
combined_data = connectToDB()
print(combined_data)