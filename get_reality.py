# Copyright (C) 2025 Warren Usui, MIT License
"""
Create a list of game results and save the data in a local reality.json file
"""
import os
import json
from bs4 import BeautifulSoup
from get_webpage import get_webpage

def parse_results(bracket):
    """
    Parse a scoring bracket and extract winners
    """
    def parse_game(ginfo):
        if ginfo[0] % 2 == 1:
            return ginfo[1].text
        return ginfo[1].find('div', class_='BracketOutcome-score').text
    def wrap_game(game_sec):
        labels = game_sec.find_all('label')
        fields = list(map(parse_game, enumerate(labels)))
        if int(fields[0]) > int(fields[2]):
            return [fields[1], fields[3]]
        return [fields[3], fields[1]]
    driver = get_webpage(bracket)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    sections = soup.find_all('section',
                             class_='BracketProposition-matchupSection')
    return list(map(wrap_game, sections))

def set_reality():
    """
    Parse_results wrapper that switches to the correct tournament
    based on current directory, and makes sure the results are complete
    for the most recent Sweet Sixteen, Elite Eight, or Final Four
    """
    sw_prefix = {'mens': '-', 'womens': '-women-'}
    prefix = os.getcwd().split(os.sep)[-1]
    header = 'https://fantasy.espn.com/games/tournament-challenge-bracket'
    switcher = f'{sw_prefix[prefix]}2024/bracket'
    bracket = ''.join([header, switcher])
    tbracket = parse_results(bracket)
    if len(tbracket) >= 60:
        return tbracket[0:60]
    if len(tbracket) >= 56:
        return tbracket[0:56]
    if len(tbracket) >= 48:
        return tbracket[0:48]
    return tbracket

def get_reality():
    """
    Set_reality wrapper that saves results into a local json file
    """
    prefix = os.getcwd().split(os.sep)[-1]
    with open(f'{prefix}_semireal.json', 'w', encoding='utf-8') as f_real:
        json.dump(set_reality(), f_real, ensure_ascii=False, indent=4)
