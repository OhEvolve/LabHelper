
# standard libraries

# nonstandard libraries

# homegrown libraries
from methods import convert_volume,fill_reaction

"""
Common attributes:
scale - "basic"
temperature - None
prefix - None
suffix - None

Mix-
    reagents - dictionary {str:tuple}
    filler - str "dH2O"
    total - tuple (50,'uL')

Incubate-
    temperature - tuple (23,'C')
    time - tuple (5,'min')
    movement - str "stationary"

Centrifuge-
    temperature - tuple (23,'C')
    time - tuple (5,'min')
    speed - tuple (1000,'g')

Decant-

Thermocycle-
    steps - list [('Initial Degradation',(23,'C'),(5,'min')),
                  ('Goto','Initial Degradation',24),
                  ('Hold',(23,'C'))]

Resuspend-
    reagents - dictionary {str:tuple}

Transfer-
    container - str

Operate- 
    instructions - list [str, str, str ... ] 
"""

def update(my_dict,args,kwargs):
    """ Update settings using args/kwargs """
    for arg in args: my_dict.update(arg)
    my_dict.update(kwargs)

def shared_properties():
    """ Shared properties among all methods """
    return {
            'prefix':None,
            'suffix':None,
            'temperature':(23,'C'),
            'scale':'basic'
           }

# ---------------------------------------------------------------------------- #

def mix(*args,**kwargs):

    """ Basic method: mix """

    # method properties
    settings = shared_properties() 
    settings['reagents'] = None
    settings['filler'] = None
    settings['total'] = None
    
    update(settings,args,kwargs) # update settings using inputs

    # find reaction volumes
    abs_reagents = [(k,convert_volume(v,settings['total'])) 
            for k,v in settings['reagents'].items()]
    abs_reagents.append((settings['filler'],fill_reaction(settings['total'],*abs_reagents)))

    # build protocol
    protocol = 'At {}{}, mix the following reagents:'.format(*settings['temperature'])
    for k,v in abs_reagents:
        protocol += '\n\t> {} - {} {}'.format(k,*v)
    protocol += '\nTotal reaction volume: {} {}'.format(*settings['total'])

    return protocol

# ---------------------------------------------------------------------------- #

def incubate(

# ---------------------------------------------------------------------------- #

def mix(*args,**kwargs):

    """ Basic method: mix """

    # method properties
    settings = shared_properties() 
    settings['reagents'] = None

    update(settings,args,kwargs) # update settings using inputs

    # find reaction volumes
    abs_reagents = [(k,convert_volume(v,settings['total'])) 
            for k,v in settings['reagents'].items()]
    abs_reagents.append((settings['filler'],fill_reaction(settings['total'],*abs_reagents)))

    # build protocol
    protocol = 'At {}{}, mix the following reagents:'.format(*settings['temperature'])
    for k,v in abs_reagents:
        protocol += '\n\t> {} - {} {}'.format(k,*v)
    protocol += '\nTotal reaction volume: {} {}'.format(*settings['total'])

    return protocol

# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
    
if __name__ == "__main__":

    settings = {
        'reagents':
            {
            'sample':(1,'uL'),
            'dNTP':(100,'X'),
            'buffer':(10,'X'),
            },
        'filler':'dH2O',
        'total':(50,'uL'),
        'temperature':(23,'C')
        }

    print mix(settings)

















