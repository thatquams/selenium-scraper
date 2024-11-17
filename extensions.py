from selenium import webdriver 
import time

driver = webdriver.Chrome()

# Function to scroll the page
def scroll_page( scroll_pause_time=3, max_scrolls=10):
    current_scrolls = 0
    while current_scrolls < max_scrolls:
        # Using self.driver to call execute_script since it's the WebDriver object
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(scroll_pause_time)
        current_scrolls += 1
        
def restart_driver():
    driver.quit()
    # Initialize driver again
    return driver