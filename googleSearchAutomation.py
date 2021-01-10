from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
searchField = input("Enter something you want to search")
print("Initiating")
driver = webdriver.Chrome(r"C:\Users\L K PATNAIK\Desktop\shantanu\pyth\Web_Automation\Browsers\chromedriver.exe")
driver.maximize_window()
driver.get("https://google.com/")
driver.find_element_by_name("q").send_keys(searchField)
time.sleep(3)
enterButton = driver.find_element_by_name("btnK")
time.sleep(3)
enterButton.send_keys(Keys.RETURN)
driver.close()
print("Sucessful")