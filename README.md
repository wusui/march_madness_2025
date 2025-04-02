# March Madness 2025

This set of python scripts can be used to generate html pages displaying the chances
that a bracket will win a given NCAA pool.  The user should generate these pages after
the second, third, and fourth rounds of the tournament are completed.

## Installation

- Download the python and html files in this repo to a directory/folder of your choice
- Set PYTHONPATH to include this directory/folder
- Create a folder anywhere named either 'mens' or 'womens' depending on the associated tournament
- In the folder just created, add a file named group_id.ini where the DEFAULT section contains a groupid value equal to the id of this group
- Pip install bs4, json, configparser, selenium, jinja2, pandas, and itertools

## Execution

- cd to the 'mens' or 'womens' directory/folder created during the installation process.
- Start a python command line and execute the following:

```
from march_madness import march_madness

march_madness()
```

This should only be run after the first two rounds have been completed.  Note that this script
will take a long time to run the first time the script is executed in this directory because
it must first extract all of the brackets and store them locally.  The bracket name is printed
as it gets added locally.  After that, since brackets don't change once the tournament starts,
this step will be skipped.

## Further details

The following are steps run by march_madness. NAME in this section will be eitheer 'mens' or 'womens':

#### get_entries

The picks made by each entrant get extracted and a a file named NAME_brackets.json is created.
This file contains a dict indexed by entrant name.  The value of each entry is a list of picks
made (first round is the first 32 entries, second round is the next 16 entries...)

#### get_reality

A general bracket file is read to collect scores so far.  Results are saved in NAME_semireal.json

#### mk_consistent

NAME_semireal.json is not consistent with the abbreviations used in the brackets.  This code creates
a conversion table that converts NAME_semireal.json names to the format used by NAME_brackets.json.
This table is stored in NAME_link_info.json.  After that, the converted team names are stored in
NAME_reality.json.  After the first round, NAME_reality.json will be 32 team names long and contain the
32 winners in the first round.  After the second round, NAME_reality.json will be 48 team names long
with the 16 winners of round 2 attached to the end of the 32 first round winners.  8 more team names
will be added for round 3, and 4 more for round 2.

#### make_rpage

Creates the NAME_page.html with which you can do whatever your heart desires.  This script does
not run on the fifth round because it is usually pretty easy to work out things by hand then.  One can
manually add text to the NAME_page.html file to further clarify things.

## Other Info

- Written by Warren Usui (warrenusui@gmail.com)
- Licensed using the MIT license
