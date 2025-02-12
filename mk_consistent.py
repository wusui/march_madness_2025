# Copyright (C) 2024, 2025 Warren Usui, MIT License
"""
Convert team names from game results scraping names to abbreviations
used by the bracket pages
"""
import os
import json
from itertools import chain

def scomp(spair):
    """
    Compare the combinations of different team formats in one matchup
    to find the corresponding abbreviated team name
    """
    def get_match(cap_ver):
        def rate_vs(long_ver):
            tscan = long_ver.lower().find(cap_ver.strip('U').lower())
            if tscan == 0 or tscan == 1 and long_ver[0] == 'U':
                return [long_ver, cap_ver]
            initials = ''.join(list(map(lambda a: a[0], long_ver.split())))
            if len(initials) > 1:
                if cap_ver.find(initials) == 0:
                    return [long_ver, cap_ver]
                if cap_ver.find(initials) == 1 and cap_ver[0] == 'U':
                    return [long_ver, cap_ver]
            return ['notf', long_ver, cap_ver]
        return list(map(rate_vs, spair[1]))
    return list(map(get_match, spair[0]))

def get_real(semireality):
    """
    Find combinations of different ids for the same team.
    """
    def fix_em1(xdata):
        def countl(text):
            retv = {}
            for letr in list(text.lower()):
                if letr not in retv:
                    retv[letr] = 1
                else:
                    retv[letr] += 1
            return retv
        def find2(idict):
            return [key for key, value in idict.items() if value == 2]
        def cnt_sml(solv):
            return solv[0].lower().count(combv[0]) < 2 and \
                    solv[1].lower().count(combv[0]) < 2
        def cnt_2v(solv):
            return solv[0].lower().count(combv[0]) >= 2 and \
                    solv[1].lower().count(combv[0]) >= 2
        def text_ord_okay(entry):
            llocs = list(map(lambda a: entry[0].lower().find(a),
                     list(entry[1].lower().strip('u'))))
            return -1 not in llocs and llocs == sorted(llocs)
        notf = list(filter(lambda a: a[0] == 'notf', xdata))
        fnotf = list(map(lambda a: a[1:3], notf))
        solu = list(filter(lambda a: a not in notf, xdata))
        if len(notf) == 2 and len(xdata) == 2:
            return list(filter(text_ord_okay,
                              list(map(lambda a: a[1:], notf))))
        if len(notf) == 3:
            return solu + list(filter(lambda a: a[0] not in solu[0] and
                                      a[1] not in solu[0], fnotf))
        if len(solu) == 4:
            shorts = list(set(list(map(lambda a: a[1], solu))))
            dletter = list(map(countl, shorts))
            lval = list(map(find2, dletter))
            combv = lval[0] + lval[1]
            return list(filter(cnt_sml, solu)) + list(filter(cnt_2v, solu))
        return solu
    def flatten(nlexp):
        if len(nlexp) == 1:
            return nlexp[0]
        return nlexp[0] + nlexp[1]
    prefix = os.getcwd().split(os.sep)[-1]
    with open(f'{prefix}_brackets.json', 'r', encoding='utf-8') as pdata:
        pinfo = json.load(pdata)
    tlists = list(map(lambda a: pinfo[a], pinfo))
    ftlists = list(filter(lambda a: len(a) > 0, tlists))
    szlists = list(map(lambda a: a[0:32], ftlists))
    grp_tms = list(zip(*szlists))
    ptms = list(map(lambda a: list(set(list(a))), grp_tms))
    tpairs = list(zip(ptms, semireality[0:32]))
    nlex = list(map(scomp, tpairs))
    xlations = list(map(flatten, nlex))
    tlinks = list(map(fix_em1, xlations))
    return dict(list(chain.from_iterable(tlinks)))

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
