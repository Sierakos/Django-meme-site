from selenium import webdriver
import time

PATH = "C:\Program Files (86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("http://127.0.0.1:8000/")
time.sleep(5)