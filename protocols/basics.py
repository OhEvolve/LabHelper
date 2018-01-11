
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
# ---------------------------------------------------------------------------- #

def finalize(protocol,settings):
    """ Add prefix and suffix to protocol """
    if settings['prefix']: protocol = settings['prefix'] + protocol
    if settings['suffix']: protocol = protocol + settings['suffix'] 
    return protocol

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

    return finalize(protocol,settings)

# ---------------------------------------------------------------------------- #

def incubate(*args,**kwargs):

    """ Basic method: incubate """

    # method properties
    settings = shared_properties() 
    settings['time'] = None
    settings['movement'] = None
    
    update(settings,args,kwargs) # update settings using inputs

    protocol = 'Incubate at {}{} for {} {} while {}.'.format(
            *settings['temperature'] + settings['time'] + (settings['movement'],))

    return finalize(protocol,settings)

# ---------------------------------------------------------------------------- #

def my_method(*args,**kwargs):

    """ Basic method: my_method """

    # method properties
    settings = shared_properties() 
    settings['attr'] = None
    
    update(settings,args,kwargs) # update settings using inputs

    protocol = ''

    return finalize(protocol,settings)

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

def centrifuge(*args,**kwargs):

    """ Basic method: centrifuge """

    # method properties
    settings = shared_properties() 
    settings['time'] = None
    settings['speed'] = None
    
    update(settings,args,kwargs) # update settings using inputs

    protocol = 'At {}{}, centrifuge sample at {} {} for {} {}.'.format(
            *settings['temperature'] + settings['speed'] + settings['time'])

    return finalize(protocol,settings)

# ---------------------------------------------------------------------------- #

def decant(*args,**kwargs):

    """ Basic method: decant """

    # method properties
    settings = shared_properties() 
    settings['action'] = None
    
    update(settings,args,kwargs) # update settings using inputs

    protocol = 'At {}{}, decant sample and {} supernatent.'.format(
            *settings['temperature'] + (settings['action'],))

    return finalize(protocol,settings)
# ---------------------------------------------------------------------------- #

def thermocycle(*args,**kwargs):

    """ Basic method: centrifuge """

    # method properties
    settings = shared_properties() 
    settings['steps'] = None
    
    update(settings,args,kwargs) # update settings using inputs

    protocol = 'Thermocycle sample:' # start protocol

    for i,step in enumerate(settings['steps']):
        if step['mode'] == 'hold':
            if step['time'] == 'inf': step['time'] = ('inf','')
            protocol += '\n\t> Step {}: Hold at {}{} for {} {}'.format(
                    *(i+1,) + step['temperature'] + step['time'])
        elif step['mode'] == 'goto':
            protocol += '\n\t> Step {}: Goto step {} (repeat x {})'.format(
                    i+1,step['step'],step['repeat'])

    return finalize(protocol,settings)

# ---------------------------------------------------------------------------- #

def resuspend(*args,**kwargs):

    """ Basic method: resuspend"""

    # method properties
    settings = shared_properties() 
    settings['reagents'] = None

    update(settings,args,kwargs) # update settings using inputs

    # build protocol
    protocol = 'At {}{}, resuspend sample with:'.format(*settings['temperature'])
    for k,v in settings['reagents'].items():
        protocol += '\n\t> {} - {} {}'.format(k,*v)

    return finalize(protocol,settings)

# ---------------------------------------------------------------------------- #

def transfer(*args,**kwargs):

    """ Basic method: transfer """

    # method properties
    settings = shared_properties() 
    settings['container'] = None
    
    update(settings,args,kwargs) # update settings using inputs

    protocol = 'Transfer sample to {}.'.format(settings['container'])

    return finalize(protocol,settings)

# ---------------------------------------------------------------------------- #

def operate(*args,**kwargs):

    """ Basic method: operate """

    # method properties
    settings = shared_properties() 
    settings['machine'] = None
    settings['instructions'] = None
    
    update(settings,args,kwargs) # update settings using inputs

    letters = 'abcdefghijklmnopqrstruvwxyz'

    protocol = 'Using the {}:'.format(settings['machine'])

    for i,instruct in enumerate(settings['instructions']):
        protocol += '\n\t{}) {}'.format(letters[i],instruct)

    return finalize(protocol,settings)

# ---------------------------------------------------------------------------- #
    
if __name__ == "__main__":

    mix_settings = {
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

    incubate_settings = {
            'time':(5,'min'),
            'movement':'stationary'
            }

    centrifuge_settings = {
            'time':(5,'min'),
            'speed':(1000,'g')
            }

    decant_settings = {
            'action':'discard'
            }

    thermocycle_settings = {
            'steps':[{'mode':'hold','temperature':(23,'C'),'time':(5,'min')},
                     {'mode':'hold','temperature':(72,'C'),'time':(30,'sec')},
                     {'mode':'hold','temperature':(55,'C'),'time':(30,'sec')},
                     {'mode':'goto','step':2,'repeat':24},
                     {'mode':'hold','temperature':(4,'C'),'time':('inf')}]
            }

    resuspend_settings = {
        'reagents':{'dH2O':(100,'uL')}
            }
            
    transfer_settings = {
        'container':'Miniprep column'
        }

    operate_settings = {
        'machine':'FPLC',
        'instructions':['Turn on',
                        'Run first protocol',
                        'Turn off']
        }




    print 'Mix:',mix(settings)
    print 'Incubate:',incubate(settings)
    print 'Centrifuge:',centrifuge(settings)
    print 'Decant:',decant(settings)
    print 'Thermocycle:',thermocycle(settings)
    print 'Resuspend:',resuspend(settings)
    print 'Transfer:',transfer(settings)
    print 'Operate:',operate(settings)

















