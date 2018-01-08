
"""

Updates existing databases based on the data presented in sources

"""

# standard libraries
import os
import re

# nonstandard libraries
import urllib2
from bs4 import BeautifulSoup

# homegrown libraries

def main(*args,**kwargs):

    settings = {
            'silent':False,
            'overwrite':False,
            'path_sources':'./database/sources/',
            'path_enzymes':'./database/enzymes/'
            }

    # update settings
    for arg in args: settings.update(arg)
    settings.update(kwargs)


    # define the source path name
    path_sources = './database/sources/'

    # iterate through available files in sources
    for fname in os.listdir(path_sources):

        if fname.startswith('restriction_enzymes'):
            """ Funnel restriction enzyme classification """
            restriction_enzymes(path_sources + fname,settings)

        if fname.startswith('dna_polymerases'):
            """ Funnel DNA polymerase classification """
            pass#dna_polymerases(path_sources + fname,settings)

        else:
            continue

        print 'Finished analysis on {}!'.format(fname)

#------------------#
# Internal Methods #
#------------------#

def dna_polymerases(fname,settings):
    
    """ Process loaded enzyme table for NEB """

    # local namespace variables
    silent = settings['silent']
    overwrite = settings['overwrite']
    path_enzymes = './database/enzymes/'

    # delimiters
    rs = '\n\xae\xc2'
    ss = ' :'

    with open(fname) as f:
        body,header = readlines_wo_header(f)
        renzymes = ([(r_and_s(l,rs,ss)) for l in body]) # format each line in body
        renzymes = [(n,r[0]) for r in renzymes for n in r[1:]] # map to dictionary tuples
        renzymes_dict = dict(renzymes) # convert to dictionary

def restriction_enzymes(fname,settings):

    """ Process loaded enzyme table for NEB """

    # local namespace variables
    silent = settings['silent']
    overwrite = settings['overwrite']
    path_enzymes = './database/enzymes/'

    # delimiters
    rs = '\n\xae\xc2'
    ss = ' :'

    with open(fname) as f:
        body,header = readlines_wo_header(f)
        renzymes = ([(r_and_s(l,rs,ss)) for l in body]) # format each line in body
        renzymes = [(n,r[0]) for r in renzymes for n in r[1:]] # map to dictionary tuples
        renzymes_dict = dict(renzymes) # convert to dictionary

        # result
        url = 'https://www.neb.com/tools-and-resources/selection-charts/alphabetized-list-of-recognition-specificities' 

        resp = urllib2.urlopen(url)
        soup = BeautifulSoup(resp, from_encoding=resp.info().getparam('charset'))

        links = [link['href'] for link in soup.find_all('a', href=True)]

        skip_index = 0 # for failures

        # Generate files
        for k,v in renzymes_dict.items():
            ename = path_enzymes + '{}.txt'.format(k)
            if not os.path.isfile(ename) or overwrite:

                # figure out what the targetsite is
                if '(' in v and ')' in v:
                    site = 'external,{},{}'.format(*(v[v.index('(')+1:v.index(')')]).split('/'))
                elif '/' in v:
                    site = 'internal,{},{}'.format(v.index('/'),len(v) - v.index('/') - 1)
                else:
                    site = 'Error'
                    print 'Error on processing {},{}, skipping...'.format(k,v)
                    #continue

                # get user heads-up on overwrite
                if not silent and os.path.isfile(ename):
                    print 'Overwriting {}.txt...'.format(ename)

                txt = open(ename,'w') # open file

                # add header information
                #for k2,v2 in header.items(): txt.write('{}:{}\n'.format(k2,v2))
                # add personal information

                sururl = 'https://www.neb.com'
                my_links = [l for l in links if k.lower().decode('utf-8') in l]
                my_links.sort(key=len, reverse=False)

                conc_tag = ('concentration">',' units/ml')
                size_tag = ('data-size="',' units">')
                price_tag = ('data-price="','">$')
                temp_tag = ('Incubate at ','&deg;C')
                heat_tag = ('<h4>Heat Inactivation</h4>\n','&deg;C for ')
                time_tag = ('&deg;C for ',' min\n')

                skips = ['ntbspqi','ntalwi','bsssai','bsrfai','bclihf',
                         'ntbstnbi','ntbbvci','btsai','narl','ddel','taqi','ntbsmai']

                if len(my_links) > 0 and k == 'BstZ17I-HF':#renzymes_dict.items().index((k,v)) > 119:
                    f = urllib2.urlopen(sururl+my_links[0])
                    data = f.read()
                    '''
                    print find_sss(data,*conc_tag),
                    print find_sss(data,*size_tag),
                    print ind_until_ss(data,*price_tag),
                    print find_until_ss(data,*temp_tag),
                    print find_sss(data,*heat_tag),
                    print find_sss(data,*time_tag),
                    '''
                
                    print k,';',''.join([c for c in v if not c in '/(1234567890-.)']),';',
                    print site,';',
                    print find_sss(data,*conc_tag),';',
                    print find_sss(data,*size_tag),';',
                    print find_until_ss(data,*price_tag),';',
                    print find_until_ss(data,*temp_tag),';',
                    print find_sss(data,*heat_tag),';',
                    print find_sss(data,*time_tag),';',
                    print sururl + my_links[0]

                else:
                    continue
                    sururl = 'https://www.neb.com'
                    skip_key = skips[skip_index]
                    my_links = [l for l in links if skip_key in l]
                    my_links.sort(key=len, reverse=False)
                    if len(my_links) > 0:
                        pass#print 'Fixed',k,skips[skip_index]
                    else:
                        pass#print 'Broken',k,skips[skip_index]
                    skip_index += 1

                    f = urllib2.urlopen(sururl+my_links[0])
                    data = f.read()
                    print k,';',''.join([c for c in v if not c in '/(1234567890-.)']),';',
                    print site,';',
                    print find_sss(data,*conc_tag),';',
                    print find_sss(data,*size_tag),';',
                    print find_until_ss(data,*price_tag),';',
                    print find_until_ss(data,*temp_tag),';',
                    print find_sss(data,*heat_tag),';',
                    print find_sss(data,*time_tag),';',
                    print sururl + my_links[0]
                #txt.write('TAGS:restriction,enzyme,reagent\n')
                #txt.write('TARGET:dsDNA,{}\n'.format(''.join([c for c in v if c in 'ATCG'])))
                #txt.write('SITE:\n')

                #print k,',',''.join([c for c in v if not c in '/(1234567890-.)']),',',site



                txt.close() # close file

                if not silent:
                    print 'Finished {}!'.format(ename)

#---------------- #
# Factory Methods #
#-----------------#

def find_until_ss(data,a,b):
    s1 = [m.start() for m in re.finditer(a,data)]
    val = [data[i+len(a):i+data[i:].index(b)] for i in s1]
    return [float(v.replace('<b>','').replace(',','')) for v in val]

def find_sss(data,a,b):
    s1 = [m.start() for m in re.finditer(a,data)]
    s2 = [m.start() for m in re.finditer(b,data)]
    val = [data[i+len(a):j] for i,j in zip(s1,s2)]
    return [float(v.replace('<b>','').replace(',','')) for v in val]

def r_and_s(my_str,rs,ss,remove=True,maxsplit=None):

    """ Removes rs characters, splits at ss characters, removes blanks """

    #assert len(rs) > 0 and len(ss) > 0, "Cannot pass empty objects to function"

    for r in rs: my_str = my_str.replace(r,'') # remove rs characters 
    for s in ss: my_str = my_str.replace(s,ss[0]) # substitute split characters to standard
    if maxsplit == None: my_str = my_str.split(ss[0]) # split at substitute characters
    else: my_str = my_str.split(ss[0],maxsplit) # split at substitute characters
    if remove: my_str = filter(None,my_str) # remove empty characters if called
    return my_str # return final value

def readlines_wo_header(f,marker=':'):
    """ Readlines after removing a header, defined by having marker in line """
    data = f.readlines()
    body = [l for l in data if not marker in l]
    header = dict([tuple(r_and_s(l,'\n',marker,maxsplit=1)) for l in data if marker in l])
    return body,header


if __name__ == "__main__":
    # settings dictionary
    settings = {
            'overwrite':True,
            'silent':True
            }

    # run update
    main(settings)



