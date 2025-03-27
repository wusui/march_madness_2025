# Copyright (C) 2025 Warren Usui, MIT License
"""
Create a _brackets.json file linkng entrants with html bracket locations
"""
import os
from time import sleep
from datetime import datetime
import json
import configparser
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from get_webpage import get_webpage

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
        sleep(10)
        c_data = get_entries_from_driver_page(driver)
        binfo = get_buttons(driver)
        return c_data + follow_next_page(driver, binfo, pcount + 1)
    driver = get_webpage(html_page)
    out_data = get_entries_from_driver_page(driver)
    button_info = get_buttons(driver)
    if not button_info:
        return out_data
    return out_data + follow_next_page(driver, button_info, 2)

def get_brackets():
    """
    Wrap parse_first_page call in code that sets up the
    link to the html file containing the group information
    """
    exten = '-'
    if os.getcwd().split(os.sep)[-1] == 'womens':
        exten = '-women-'
    config = configparser.ConfigParser()
    config.read('group_info.ini')
    groupid = config.get('DEFAULT', 'groupid')
    ynow = datetime.now().year
    html_page = ''.join(["https://fantasy.espn.com/games/",
                f"tournament-challenge-bracket{exten}{ynow}/group?id=",
                f"{groupid}"])
    return parse_first_page(html_page)

def parse_entry(bracket):
    """
    Extract picks from page
    """
    driver = get_webpage(bracket)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    pix = soup.find_all('span',
                        class_='BracketPropositionHeader-pickName')
    return list(map(lambda a: a.text, pix))

def html_to_list(html_file):
    """
    Convert bracket info from individual webpage to a list of picks
    that are eventually a player's entry in the brackets json file
    """
    def html_inner(bracket):
        print(bracket[0])
        return [bracket[0], parse_entry(bracket[1])]
    hlist = list(map(html_inner, html_file))
    valid_pix = list(filter(lambda a: a[1], hlist))
    return dict(valid_pix)

def make_brackets():
    """
    Wrap get_brackets in code that saves the json file
    """
    prefix = os.getcwd().split(os.sep)[-1]
    with open(f"{prefix}_brackets.json", 'w', encoding='utf-8') as ofile:
        json.dump(html_to_list(get_brackets()), ofile, indent=4)

def get_entries():
    """
    Skip making brackets if bracket file exists (takes too long)
    """
    prefix = os.getcwd().split(os.sep)[-1]
    if os.path.isfile(f"{prefix}_brackets.json"):
        print('Individual player brackets have been saved')
    else:
        make_brackets()

if __name__ == "__main__":
    get_entries()
