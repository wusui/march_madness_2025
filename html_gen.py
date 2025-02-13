# Copyright (C) 2024, 2025 Warren Usui, MIT License
"""
Generate the html file used to output results.

The data input to make_html consists of records that will be formatted into
the table header and individual rows of the table, and text to be added to
the text header.
"""
import os
import datetime
from jinja2 import Environment, FileSystemLoader
import pandas as pd

def df_columns(solution):
    """
    Generate the columns for the dataframe
    """
    def mk_games():
        def igms():
            return list(map(lambda a: list(a.keys()), solution[0]['games']))
        return list(map(lambda a: '<div>' + a[0] + '</div><div>' + \
                        a[1] + '</div>', igms()))
    return ['NAME', '<div>Winning</div>\n<div>Outcomes</div>',
            '<div>Probable</div>\n<div>Payoff</div>\n'] + mk_games()

def get_ccode(fgame):
    """
    Handle the colors used by the individual cells in the table.
    """
    def gc_inner(dvals):
        def setf_dvals(cnumbs):
            def setbg_vals(icol):
                if icol < 256:
                    return f'#{icol:02x}ff00'
                return f'#ff{max(511 - icol, 0):02x}00'
            return setbg_vals(int(512 * cnumbs[0] / cnumbs[1] + .5))
        return setf_dvals([abs(dvals[0] - dvals[1]), dvals[0] + dvals[1]])
    return gc_inner(list(fgame.values()))

def df_rows(solution):
    """
    Generate the individual rows in the table
    """

    def strfy(nfloat):
        return f'{nfloat:.6f}'
    def const_row(row):
        def left_cols():
            return [row['name'], row['w_outcomes'], strfy(row['pct_pt'])]
        def game_field(fgame):
            def gstyle(style_data):
                if style_data[0][1] == 0:
                    return '#000000;color:#ffffff'
                return get_ccode(fgame)
            def get_style(teams):
                if teams[0][1] == teams[1][1]:
                    return '*'
                return f'<div style=background-color:{gstyle(teams)}>' + \
                        f'{teams[1][0]}</div>'
            return get_style(sorted(list(zip(fgame.keys(), fgame.values())),
                            key=lambda a: a[1]))
        return left_cols() + list(map(game_field, row['games']))
    return list(map(const_row, solution))

def make_html(solution):
    """
    String together all the pieces that compose the html data returned
    as a string.
    """
    def set_level(fields):
        return {11: 'Sweet Sixteen', 7: 'Elite Eight', 5: 'Final Four'}[
                    len(fields)]
    def get_template():
        pythonpath_os = os.environ.get('PYTHONPATH')
        if 'madlib' in pythonpath_os:
            return f'..{os.sep}madlib'
        return '.'
    environment = Environment(loader=FileSystemLoader(get_template()))
    template = environment.get_template('template.html')
    oheader = df_columns(solution[0])
    dframe = pd.DataFrame(df_rows(solution[0]), columns=oheader)
    tourn = solution[1]
    tlevel = set_level(oheader)
    tyear = datetime.date.today().year
    return template.render(tourn=tourn, out_table=dframe.to_html(
            escape=False, index=False), tyear=tyear, tlevel=tlevel)
