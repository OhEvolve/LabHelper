
"""

Restriction Enzyme Class

"""


# standard libraries

# nonstandard libraries

# homegrown libraries
from methods import dict_update
from methods import obj_update

#--------------------------------------#
#           Main     Methods           #
#--------------------------------------#

class Sequence:

    def __init__(self,*args,**kwargs):

        """ Restriction enzyme input """

        self.database_folder = './database/sequences/'

        # digestion settings
        self.settings = {
                'name':None,
                'author':None,
                'description':None,
                'sequence':None,
                'codon_set':None,
                'elements':None,
                'concentration':None,
                'form':None,
                'tags':None,
                'origin':None, # what experiments produced fragment
                'source':None, # what website, author, etc
                'url':None, # background information
                'break_5':None, # 5' backbone breaks
                'break_3':None  # 3' backbone breaks
                   }

        # update settings
        for arg in args: self.settings.update(arg)
        self.settings.update(kwargs)

        # update object attributes with internal settings
        obj_update(self)

    def save(self,size = None):

        """ Select which reagent type """

        pass

    def add_origin(self,origin):

        """ Recursively add origin to sample """

        if self.origin == None:
            self.origin = [origin]
        elif isinstance(self.origin,str):
            self.origin = [self.origin,origin]
        elif isinstance(self.origin,list):
            self.origin.append(origin)

    def load(self,name = None):

        # set sequence to default if no name is passed
        if self.settings['name'] == None and name == None:
            print 'No sequence name specified, exiting...'
            return None
        elif name == None:
            print 'Using {} as sequence name...'.format(self.settings['name'])
            name = self.settings['name']

        # build fname to call
        fname = self.database_folder + name + '.txt'

        # sequence file, update settings
        database = _load_sequence_file(fname)
        dict_update(self.settings,database) # dicts are mutably updated
        obj_update(self)

    def info(self,cc = 80,spacer = 80):

        """ Print information about the sequence """

        # building visual strings

        info = []

        info.append(spacer*'-')
        info.append('Sequence Name - {}'.format(self.name))
        info.append(spacer*'-')
        info.append('Description: {}'.format(self.description))
        info.append('Form: {}'.format(self.form))
        info.append('Concentration: {}'.format(self.concentration))

        info.append('Tags: {}'.format(self.tags))
        info.append('Codon set: {}'.format(self.codon_set))
        info.append('Origin: {}'.format(self.source))
        info.append("5' strand breaks: {}".format(self.break_5))
        info.append("3' strand breaks: {}".format(self.break_3))
        info.append('Distributor: {}'.format(self.source))
        info.append('More information: {}'.format(self.url))
        info.append(spacer*'-')

        # TODO: improve sequence display
        info.append('Sequence:')

        ### CREATING SEQUENCE INTERPRETER ###

        # interpret sequence form
        if self.form == 'dsDNA':
            form_disp = ':'*len(self.sequence)
        elif len(self.form) == len(self.sequence):
            form_disp = self.form
        else:
            print 'Unknown sequence form, leaving blank...'
            form_disp = ' '*len(self.sequence)

        # check for matching elements
        notes = []
        element_disp = ' '*len(self.sequence)
        for element in self.elements:
            el_len = len(element['sequence'])
            try:
                ind = self.sequence.index(element['sequence'])
                if el_len >= len(element['name']) + 2:
                    name = '|' + element['name'].center(el_len-2) + '|'
                else:
                    name = '|' + str(len(notes) + 1).center(el_len-2) + '|'
                    notes.append('{} : {}'.format(len(notes) + 1,element['name']))
                if element_disp[ind:ind+el_len] == ' '*el_len:
                    element_disp = element_disp[:ind] + name + element_disp[ind+el_len:]
                else:
                    raw_input('Overlapping element...')
            except ValueError:
                continue

        # create ruler
        ruler_disp = ''.join(['{: <10}'.format(i) for i in xrange(1,len(self.sequence)+1,10)])

        # create lines to display text
        for i in xrange(0,len(self.sequence),cc):
            info.append(element_disp[i:i+cc])
            info.append(self.sequence[i:i+cc])
            info.append(ruler_disp[i:i+cc])
            info.append(form_disp[i:i+cc])
            info.append('')

        # 
        if len(notes) > 0:
            info += [''] + notes + ['']

        info.append(spacer*'-')

        info.append('Elements:')
        for element in self.elements:
            info += ['{}: {}'.format(k.title(),v) for k,v in element.items()]
            info.append(spacer*'-')

        info.append(spacer*'-')

        # center each line and add line breaks
        return '\n'.join([i.center(cc) for i in info])


#--------------------------------------#
#          Internal Methods            #
#--------------------------------------#

def _load_sequence_file(fname):

    # initialize variables
    my_dict,sub_dict = {},{}
    subscope = False
    last_key = ['']

    # load data
    with open(fname,'r') as f:
        data = [l.strip('\n').split(':') for l in f.readlines()]

    # iterate through lines on the file
    for d in data:
        if d == ['{']:
            subscope,sub_dict = True,{}
        elif d == ['}']:
            subscope = False
            my_dict[last_key].append(sub_dict)

        # values
        elif len(d) == 2 and d[1].strip(' ') == '' and subscope == False:
            last_key = d[0].lower()
            my_dict[last_key] = []

        # else, treat as entry
        elif len(d) == 2:
            if subscope == True:
                sub_dict[d[0].lower()] = d[1]
            elif subscope == False:
                my_dict[d[0].lower()] = d[1]

        else:
            continue

    # replace empty lists with empty strings
    for k,v in my_dict.items():
        if v == []: my_dict[k] = ''

    return my_dict

#--------------------------------------#
#               Testing                #
#--------------------------------------#

if __name__ == "__main__":
    sq = Sequence(name='XhoI-Plasmid')
    sq.load()
    print sq.info()

