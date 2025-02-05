# Copyright (C) 2025 Warren Usui, MIT License
"""
Create a _brackets.json file linkng entrants with html bracket locations
"""
import os
import time
import json
import configparser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def get_entries_from_driver_page(driver):
    """
    Extract webelements containing links to bracket files for a driver page
    """
    a_elems = driver.find_elements(By.TAG_NAME, 'a')
    h_pairs = list(map(lambda a: [a.text, a.get_attribute('href')], a_elems))
    h_pairs2 = list(filter(lambda a: a[1], h_pairs))
    return list(filter(lambda a: 'bracket?id=' in a[1], h_pairs2))

def get_buttons(driver):
    """
    Get the paging buttons on the bottom of the page
    """
    pg_btns = driver.find_elements(By.XPATH, "//*[@href='#']")
    return list(filter(lambda a: a.text.isnumeric(), pg_btns))

def parse_first_page(html_page):
    """
    Extract the bracket information
    """
    def follow_next_page(driver, button_info, pcount):
        npage = list(filter(lambda a: int(a.text) == pcount, button_info))
        if not npage:
            return []
        ActionChains(driver).move_to_element(npage[0]).click().perform()
        time.sleep(10)
        c_data = get_entries_from_driver_page(driver)
        binfo = get_buttons(driver)
        return c_data + follow_next_page(driver, binfo, pcount + 1)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get(html_page)
    WebDriverWait(driver,1000).until(EC.presence_of_all_elements_located(
                    (By.XPATH,"(//iframe)")))
    time.sleep(10)
    out_data = get_entries_from_driver_page(driver)
    button_info = get_buttons(driver)
    if not button_info:
        return dict(out_data)
    return dict(out_data + follow_next_page(driver, button_info, 2))

def get_brackets():
    """
    Wrap parse_first_page call in code that sets up the
    link to the html file containing the group infromation
    """
    exten = '-'
    if os.getcwd().split(os.sep)[-1] == 'womens':
        exten = '-women-'
    config = configparser.ConfigParser()
    config.read('group_info.ini')
    groupid = config.get('DEFAULT', 'groupid')
    html_page = ''.join(["https://fantasy.espn.com/games/",
                f"tournament-challenge-bracket{exten}2024/group?id=",
                f"{groupid}"])
    return parse_first_page(html_page)

def make_brackets():
    """
    Wrap get_brackets in code that saves the json file
    """
    prefix = os.getcwd().split(os.sep)[-1]
    with open(f"{prefix}_brackets.json", 'w', encoding='utf-8') as ofile:
        json.dump(get_brackets(), ofile, indent=4)
