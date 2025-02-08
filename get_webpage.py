# Copyright (C) 2025 Warren Usui, MIT License
"""
Use selenium to extract contents of a webpage
"""
from selenium import webdriver

def get_webpage():
    """
    Use headless driver
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    return webdriver.Chrome(options=options)
