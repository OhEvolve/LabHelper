
"""

Polymerase Class

"""


# standard libraries

# nonstandard libraries

# homegrown libraries
from methods import request_xlsx
from methods import dict_update
from methods import obj_update
from methods import comp

#--------------------------------------#
#           Main     Methods           #
#--------------------------------------#

class Polymerase:

    def __init__(self,*args,**kwargs):

        """ Restriction enzyme input """

        default_name = 'XhoI'
        database_fname = './database/restriction_enzymes.xlsx'

        # digestion settings
        self.settings = {
                    'name':None,
                    'sequence':None,
                    'source':None,
                    'size':None,
                    'default_size':None,
                    # current product info
                    'concentration':None,
                    'units_per_ml':None,
                    'cost':None,
                    # available product info 
                    'all_sizes':None,
                    'all_concentrations':None,
                    'all_units_per_ml':None,
                    'all_costs':None,
                    'active_temperature':None,
                    'inactive_temperature':None,
                    'inactive_time':None,
                    'url':None
                       }

        # update settings
        for arg in args: self.settings.update(arg)
        self.settings.update(kwargs)

        # TODO: consider taking out
        # set enzyme to default if no name is passed
        if self.settings['name'] == None:
            print 'No enzyme specified, using {}...'.format(default_name)
            self.settings['name'] = default_name

        # database request, update settings
        database = request_xlsx(self.settings['name'],database_fname)
        dict_update(self.settings,database) # dicts are mutably updated

        # update object attributes
        obj_update(self)

    def select_size(self,size = None):

        """ Select which reagent type """

        # local namespace
        all_sizes = self.settings['all_sizes']
        default_size = self.settings['default_size']

        # determine whether default size is used
        if size == None:
            print 'Using default enzyme size ({})...'.format(default_size)
            size = default_size

        # reassign based on product selection 
        assert size in all_sizes, "selected size not found in enzyme info!"

        # find location of info
        index = all_sizes.index(size)

        # pull values
        self.settings['size'] = size
        self.settings['concentration'] = self.settings['all_concentrations'][index]
        self.settings['units_per_ml'] = self.settings['all_units_per_ml'][index]
        self.settings['cost'] = self.settings['all_costs'][index]

        # update object attributes
        obj_update(self)

    def info(self,cc = 80,spacer = 80):

        """ Print information about the restriction enzyme """

        # create processable strings
        if self.site_type == 'internal':
            seq_uncut = [self.sequence,
                         comp(self.sequence)]
            seq_cut = [_insert(self.sequence,self.site_location,('|',' ')),
                       _insert(comp(self.sequence),self.site_location,(' ','|'))]

        elif self.site_type == 'external':
            loc = (min(0,*self.site_location),max(0,*self.site_location))
            sequence_adj = 'N'*int(-loc[0]) + \
                       self.sequence + \
                        'N'*int(loc[1])
            site_loc_adj = [s - loc[0] if s < 0  or (s == 0 and loc[1] < 0)
                        else s - loc[0] + len(self.sequence) for s,l in zip(self.site_location,loc)]
            seq_uncut = [sequence_adj,
                         comp(sequence_adj)]
            seq_cut = [_insert(sequence_adj,site_loc_adj,('|',' ')),
                       _insert(comp(sequence_adj),site_loc_adj,(' ','|'))]

        else:
            print 'Site type not recognized...'
            return None

        # building visual strings

        info = []
        info.append(spacer*'-')
        info.append('Restriction Enzyme - {}'.format(self.name))
        info.append(spacer*'-')
        info.append('Target Sequence:')
        info += list(seq_uncut)
        info.append('Cut Sequence:')
        info += list(seq_cut)
        info.append('Active Temperature: {} C'.format(self.active_temperature))
        info.append('Inactiving Temperature: {} min at {} C'.format(
            self.inactive_time,self.inactive_temperature))
        info.append('Distributor: {}'.format(self.source))
        info.append('More information: {}'.format(self.url))
        info.append(spacer*'-')

        if not self.size == None:
            info.append('======================')
            info.append('|  Selected Product  |')
            info.append('======================')
            info.append('*Selected product*')
            info.append('Reagent size: {}'.format(self.size))
            info.append('Units/sample: {}'.format(self.concentration))
            info.append('Units/mL: {}'.format(self.units_per_ml))
            info.append('Total cost: ${}'.format(self.cost))
        info.append(spacer*'-')

        info.append('======================')
        info.append('| Available Products |')
        info.append('======================')
        for s,c,u,t in zip(self.all_sizes,self.all_concentrations,self.all_units_per_ml,self.all_costs):
            if s == self.size: continue
            info.append('Reagent size: {}'.format(s))
            info.append('Units/sample: {}'.format(c))
            info.append('Units/mL: {}'.format(u))
            info.append('Total cost: ${}'.format(t))
            info.append(spacer*'-')
        info.append(spacer*'-')

        return '\n'.join([i.center(cc) for i in info])


#--------------------------------------#
#          Internal Methods            #
#--------------------------------------#

def _insert(my_str,indices,sss):

    """ Inserts substrings at specified location """

    # check if submissions are noniterable (and fix)
    if isinstance(indices,(int,float)): indices = (indices,)
    if isinstance(sss,str): sss = (sss,)

    sss_length = [len(ss) for ss in sss]

    for i,ind in enumerate(indices):
        ind2 = ind + sum([s for s,j in zip(sss_length[:i],indices[:i]) if j<ind])
        my_str = my_str[:int(ind2)] + sss[i] + my_str[int(ind2):]

    return my_str

#--------------------------------------#
#               Testing                #
#--------------------------------------#

if __name__ == "__main__":
    re = RestrictionEnzyme(name='BsmI')
    re.select_size()
    print re.info()

