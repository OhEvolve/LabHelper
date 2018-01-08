
"""
~/database/reagents/restriction_enzymes

Update method for restriction enzymes
"""


# standard libraries
import os
import requests

# homegrown libraries
from reagents.methods import text_from_url
from reagents.methods import bookend_list


def update():
    neb_update()



def neb_update(*args):
    # declare url
    url = "https://www.neb.com/tools-and-resources/selection-charts/alphabetized-list-of-recognition-specificities"

    # split html from url into lines
    data = text_from_url(url)
    data = bookend_list(data,'Enzyme','Support')
    data = dict([(tuple(data[i+1].split(' ')),data[i]) for i in xrange(0,len(data),2)])

    for ks,v in data.items():
        for k in ks:
            with open('./reagents/restriction_enzymes/{}.txt'):

#
if __name__ == '__main__':
    neb_scrap()
