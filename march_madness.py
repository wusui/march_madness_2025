"""
Stand alone bracket checker runner
"""
from get_entries import get_entries
from get_reality import get_reality
from mk_consistent import mk_consistent
from io_interface import make_rpage

def march_madness():
    """
    Step through all the calls
    """
    get_entries()
    get_reality()
    if mk_consistent() < 48:
        print("Can't generate pick table until Sweet 16 is completed")
        return
    make_rpage()

if  __name__ == '__main__':
    march_madness()

