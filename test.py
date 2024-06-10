import re
import numpy as np
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd

cars45Website = "https://autochek.africa/ng/car/Toyota-Corolla-ref-BqcleAisE"

driver = webdriver.Chrome()
driver.get(cars45Website)

otherCarFeatures = driver.find_elements(By.XPATH, "//p[@class='MuiTypography-root MuiTypography-body1 css-1pldev7']")
carColour = otherCarFeatures[4].text               
print(carColour)

