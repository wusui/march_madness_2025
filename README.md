# March Madness 2025

This set of python scripts can be used to generate html pages displaying the chances
that a bracket will win a given NCAA pool.  The user should generate these pages after
the second, third, and fourth rounds of the tournament are completed.

## Installation

- Download the python and html files in this repo to a directory/folder of your choice
- Set PYTHONPATH to include this directory/folder
- Create a folder anywhere named either 'mens' or 'womens' depending on the associated tournament
- In the folder just created, add a file name group_id.ini where the DEFAULT section contains a groupid value equal to the id of this group

## Execution

In all of these steps, cd to the 'mens' or 'womens' directory/folder created during the installation process.
The text NAME in the file names below should be replaced by the directory/folder name chosen.
The python scripts listed here should not affect things if run multiple times.

#### Save brackets picked

Once the tournament starts, execute the following python script:
```
from get_entries import make_brackets

make_brackets()
```

This only needs to be run once (when the tournament starts).  When completed, a NAME_brackets.json file
will be created which contains a directory indexed by entrant name.  The data in this dictionary will
be a link to the html file containing the bracket.

#### Save actual player picks
```
pass # Code needs to be added here
```
This also only needs to be run once (when the tournament starts).  When completed, a NAME_picks.json file
will be created which contains a directory indexed by entrant name.  The data in this dictionary will
be a list of the picks made in the bracket (the first 32 entries will be the first round picks made in
bracket layout order, the next 16 entries will be the second round picks...).

#### Update the games played so far

After the end of the second, third, and fourth rounds, the information on games played needs to be updated.
Execute the following python script:
```
from get_reality import get_reality

get_reality()
```

This updates a list of teams that have won.  The first 32 entries will be the teams that won the first round,
in bracket order (top to bottom, left side then ringht side of the bracket page).  The next 16 entries will
be the teams that won the second round in bracket order.  At this point, the Sweet Sixteen results
can be displayed.  After 8 more entries the Elite Eight results can be displayed and after 4 more entries
the Final Four can be displayed.  Note that it is possible for this list to be updated by hand.  This
data is saved in NAME.reality.json

#### Create the html page

Once the second round has finished, execute the following python script:
```
from io_interface import make_rpage

make_rpage()
```
  
This creates the NAME_page.html with which you can do whatever your heart desires.  This script does
not run on the fifth round because it is usually pretty easy to work out things by hand then.  One can
add text to the NAME_page.html file to further clarify things.

## Other Info

- Written by Warren Usui (warrenusui@gmail.com)
- Licensed using the MIT license
