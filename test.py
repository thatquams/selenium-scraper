import re
import numpy as np
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd

cars45Website = "https://autochek.africa/ng/car/Toyota-Highlander-ref-F1edqpUqz"

driver = webdriver.Chrome()
driver.get(cars45Website)

carLocation = driver.find_element(By.XPATH, "//div[@id = 'state-city']/span[2]").text.split(",")[0]
              
print(carLocation)

