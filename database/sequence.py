
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

        self.database_folder = './sequences/'

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
                'origin':None,
                'codon':None,
                'source':None,
                'url':None
                   }

        # update settings
        for arg in args: self.settings.update(arg)
        self.settings.update(kwargs)

        # update object attributes with internal settings
        obj_update(self)

    def save(self,size = None):

        """ Select which reagent type """

        pass

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
        info.append('Distributor: {}'.format(self.source))
        info.append('More information: {}'.format(self.url))
        info.append(spacer*'-')

        # TODO: improve sequence display
        info.append('Sequence:')
        info += [self.sequence[i:i+cc] for i in xrange(0,len(self.sequence),cc)]

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

