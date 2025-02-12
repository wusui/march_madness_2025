# Copyright (C) 2025 Warren Usui, MIT License
"""
Use selenium to extract contents of a webpage
"""
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_webpage(html_page):
    """
    Use headless driver
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get(html_page)
    WebDriverWait(driver, 100).until(EC.presence_of_all_elements_located(
                (By.TAG_NAME, "div")))
    sleep(5)
    return driver
