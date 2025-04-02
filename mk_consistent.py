# Copyright (C) 2024, 2025 Warren Usui, MIT License
"""
Convert team names from game results scraping names to abbreviations
used by the bracket pages
"""
import os
import json

def mk_xlate_tbl():
    """
    Make a table of abbreviations indexed by name using *_script.txt information
    """
    def get_ab_nm(sloc):
        def get_field(bdata):
            field = sdata[0:bdata].rfind('":') + 2
            relv_data = sdata[field:field + 100]
            relv_data = relv_data[relv_data.find('":"') + 3:]
            relv_data = relv_data[0:relv_data.find(',') - 1]
            return relv_data
        abbrev = get_field(sdata[0:sloc].rfind('"abbrev":'))
        name = get_field(sloc + sdata[sloc:].find('"name":'))
        return [name, abbrev]
    prefix = os.getcwd().split(os.sep)[-1]
    with open(f'{prefix}_script.txt', 'r', encoding='utf-8') as afile:
        sdata = afile.read()
    matchp = [i for i in range(len(sdata)) if sdata.startswith(
        '"matchupPosition":', i)]
    return dict(list(map(get_ab_nm, matchp)))

def mk_consistent():
    """
    Handle all the file io necessary.  Wrapper for get_real calls
    """
    prefix = os.getcwd().split(os.sep)[-1]
    lfile = f'{prefix}_link_info.json'
    link_info = []
    if os.path.isfile(lfile):
        with open(lfile, 'r', encoding='utf-8') as filed:
            link_info = json.load(filed)
    with open(f'{prefix}_semireal.json', 'r', encoding='utf-8') as semir:
        semireality = json.load(semir)
    if len(semireality) < 32:
        return len(semireality)
    if not link_info:
        link_info = mk_xlate_tbl()
    new_reality = list(map(lambda a: link_info[a[0]], semireality))
    if not os.path.isfile(lfile):
        json_data = json.dumps(link_info, indent=4)
        with open(lfile, 'w', encoding='utf-8') as outfile:
            outfile.write(json_data)
    reality = json.dumps(new_reality, indent=4)
    with open(f'{prefix}_reality.json', 'w', encoding='utf-8') as rfile:
        rfile.write(reality)
    return len(semireality)
