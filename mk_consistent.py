# Copyright (C) 2024, 2025 Warren Usui, MIT License
"""
Convert team names from game results scraping names to abbreviations
used by the bracket pages
"""
import os
import json
from itertools import chain

def get_real(semireality):
    """
    Associate team abbreviation with full name used in brackets
    """
    def find_exact_abbrv(tpairs):
        def fes_inner(spair):
            def fes_inn2(abbrev):
                def fes_inn3(sname):
                    def matches():
                        #if sname.lower().startswith(abbrev.lower()):
                        #    return True
                        if abbrev.lower() in sname.lower():
                            return True
                        tminits = ''.join(list(map(lambda a: a[0],
                                                      sname.split())))
                        if abbrev in [tminits + 'U', 'U' + tminits, tminits]:
                            return True
                        ncomp = list(map(lambda a: sname.lower().find(a),
                                       list(abbrev.lower())))
                        if len(abbrev) > 2:
                            if len(list(filter(lambda a: a >= 0,
                                        ncomp))) == len(abbrev):
                                return True
                            if abbrev.endswith('U'):
                                if len(list(filter(lambda a: a >= 0,
                                        ncomp[0:-1]))) == len(abbrev) - 1:
                                    return True
                            if abbrev.startswith('U'):
                                if len(list(filter(lambda a: a >= 0,
                                        ncomp[1:]))) == len(abbrev) - 1:
                                    return True
                        return False
                    if matches():
                        return [sname, abbrev]
                    return []
                return list(map(fes_inn3, spair[1]))
            rmtch = list(filter(None, list(map(fes_inn2, spair[0]))))
            fmtch = list(map(lambda a: list(filter(None, a)), rmtch))
            nmtch = list(filter(None, fmtch))
            if nmtch:
                nmtch = list(map(lambda a: a[0], nmtch))
                if len(nmtch) == 1 and len(spair[0]) == 2:
                    sc1 = list(filter(lambda a: a != nmtch[0][0], spair[1]))[0]
                    ab1 = list(filter(lambda a: a != nmtch[0][1], spair[0]))[0]
                    nmtch += [[sc1, ab1]]
            else:
                print('Consistency Error: ', spair)
            return nmtch
        return list(map(fes_inner, tpairs))
    prefix = os.getcwd().split(os.sep)[-1]
    with open(f'{prefix}_brackets.json', 'r', encoding='utf-8') as pdata:
        pinfo = json.load(pdata)
    tlists = list(map(lambda a: pinfo[a], pinfo))
    ftlists = list(filter(lambda a: len(a) > 0, tlists))
    szlists = list(map(lambda a: a[0:32], ftlists))
    grp_tms = list(zip(*szlists))
    ptms = list(map(lambda a: list(set(list(a))), grp_tms))
    tpairs = list(zip(ptms, semireality[0:32]))
    matches = find_exact_abbrv(tpairs)
    return dict(list(chain.from_iterable(matches)))

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
        link_info = get_real(semireality)
    new_reality = list(map(lambda a: link_info[a[0]], semireality))
    if not os.path.isfile(lfile):
        json_data = json.dumps(link_info, indent=4)
        with open(lfile, 'w', encoding='utf-8') as outfile:
            outfile.write(json_data)
    reality = json.dumps(new_reality, indent=4)
    with open(f'{prefix}_reality.json', 'w', encoding='utf-8') as rfile:
        rfile.write(reality)
    return len(semireality)
