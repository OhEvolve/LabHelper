
# standard libraries

# nonstandard libraries

# homegrown libraries
from methods import convert_volume,fill_reaction,capitalize

"""
Common attributes:
scale - "basic"
temperature - None
preamble - None
postamble - None

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
    action - str "discard" 

Thermocycle-
    steps - list [('Initial Degradation',(23,'C'),(5,'min')),
                  ('Goto','Initial Degradation',24),
                  ('Hold',(23,'C'))]

Resuspend-
    reagents - dictionary {str:tuple}
    filler - str "dH2O"
    total - tuple (50,'uL')

Transfer-
    container - str

Operate- 
    instructions - list [str, str, str ... ] 
"""

def basics():
    return {
            'add':add,
            'mix':mix,
            'incubate':incubate,
            'centrifuge':centrifuge,
            'decant':decant,
            'thermocycle':thermocycle,
            'resuspend':resuspend,
            'transfer':transfer,
            'operate':operate,
            'save':save,
            'plate':plate,
            'inoculate':inoculate
           }



# ---------------------------------------------------------------------------- #

def finalize(protocol,settings):
    """ Add preamble and postamble to protocol """


    # add temperature indication
    if settings['temperature']: protocol = 'At {}{}, '.format(*settings['temperature']) + protocol
    if settings['preamble']: protocol = '{}.\n '.format(settings['preamble']) + protocol
    if settings['postamble']: protocol = protocol + '\n {}.'.format(settings['postamble'])

    # return capitalized protocol
    return capitalize(protocol)

def update(my_dict,args,kwargs):
    """ Update settings using args/kwargs """
    for arg in args: my_dict.update(arg)
    my_dict.update(kwargs)

def shared_properties():
    """ Shared properties among all methods """
    return {
            'preamble':None,
            'postamble':None,
            'temperature':None,
            'scale':'basic'
           }


# ---------------------------------------------------------------------------- #

def add(*args,**kwargs):

    """ Basic method: add """

    # method properties
    settings = shared_properties() 
    settings['reagents'] = None
    settings['filler'] = None
    settings['total'] = None
    settings['target'] = 'sample'
    
    # update settings
    update(settings,args,kwargs) # update settings using inputs

    ### Find reagent volumes ###
    # check if only one of (filler,total) are None
    if bool(settings['filler']) != bool(settings['total']):
        print 'Filler and total not simulatenously filled, resetting variables...'
        settings['filler'],settings['total'] = None,None

    # find reaction volumes if filler is used
    if settings['filler'] and settings['total']:
        abs_reagents = [(k,convert_volume(v,settings['total'])) 
                for k,v in settings['reagents'].items()]
        abs_reagents.append((settings['filler'],fill_reaction(settings['total'],*abs_reagents)))
    else:
        abs_reagents = [(k,v) for k,v in settings['reagents'].items()]

    ### Build Protocol ###
    # if only one reagent, concise description
    if len(abs_reagents) == 1:
        for k,v in abs_reagents:
            protocol = 'add {} {} of {} to {}.'.format(v[0],v[1],k,settings['target'])
    # if multiple reagents, list
    else:
        protocol = 'add the following reagents to {}:'.format(settings['target'])
        for k,v in abs_reagents:
            protocol += '\n\t> {} - {} {}'.format(k,*v)
        protocol += '\nTotal reaction volume: {} {}'.format(*settings['total'])

    # add temperature indication
    if settings['temperature']:
        protocol = 'At {}{}, '.format(*settings['temperature']) + protocol

    # capatilize the first letter

    return finalize(protocol,settings)

# ---------------------------------------------------------------------------- #

def mix(*args,**kwargs):

    """ Basic method: add """

    # method properties
    settings = shared_properties() 
    settings['reagents'] = None
    settings['filler'] = None
    settings['total'] = None
    
    # update settings
    update(settings,args,kwargs) # update settings using inputs

    ### Find reagent volumes ###
    # check if only one of (filler,total) are None
    if bool(settings['filler']) != bool(settings['total']):
        print 'Filler and total not simulatenously filled, resetting variables...'
        settings['filler'],settings['total'] = None,None

    # find reaction volumes if filler is used
    if settings['filler'] and settings['total']:
        abs_reagents = [(k,convert_volume(v,settings['total'])) 
                for k,v in settings['reagents'].items()]
        abs_reagents.append((settings['filler'],fill_reaction(settings['total'],*abs_reagents)))
    else:
        abs_reagents = [(k,v) for k,v in settings['reagents'].items()]

    ### Build Protocol ###
    # if only one reagent, concise description
    if len(abs_reagents) == 1:
        for k,v in abs_reagents:
            protocol = 'mix {} {} of {} to the sample.'.format(v[0],v[1],k)
    # if multiple reagents, list
    else:
        protocol = 'mix the following reagents:'
        for k,v in abs_reagents:
            protocol += '\n\t> {} - {} {}'.format(k,*v)
        protocol += '\nTotal reaction volume: {} {}'.format(*settings['total'])

    # capatilize the first letter

    return finalize(protocol,settings)

# ---------------------------------------------------------------------------- #

def incubate(*args,**kwargs):

    """ Basic method: incubate """

    # method properties
    settings = shared_properties() 
    settings['time'] = None
    settings['movement'] = None
    settings['target'] = None
    
    update(settings,args,kwargs) # update settings using inputs

    if settings['movement']:
        protocol = 'Incubate {} for {} {} while {}.'.format(
                *(settings['target'],) + settings['time'] + (settings['movement'],))
    else:
        protocol = 'Incubate {} for {} {}.'.format(
                *(settings['target'],) + settings['time'])

    return finalize(protocol,settings)

# ---------------------------------------------------------------------------- #

def centrifuge(*args,**kwargs):

    """ Basic method: centrifuge """

    # method properties
    settings = shared_properties() 
    settings['time'] = None
    settings['speed'] = None
    settings['target'] = 'sample' 
    
    update(settings,args,kwargs) # update settings using inputs

    protocol = 'centrifuge {} at {} {} for {} {}.'.format(
                        *(settings['target'],) + 
                        settings['speed'] + 
                        settings['time'])

    return finalize(protocol,settings)

# ---------------------------------------------------------------------------- #

def decant(*args,**kwargs):

    """ Basic method: decant """

    # method properties
    settings = shared_properties() 
    settings['action'] = 'discard' 
    
    update(settings,args,kwargs) # update settings using inputs

    protocol = 'decant sample and {} supernatent.'.format(settings['action'])

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
    settings['target'] = 'sample'

    update(settings,args,kwargs) # update settings using inputs

    # if no reagents, just resuspend with available liquid
    if len(settings['reagents']) == 0:
        protocol = 'Resuspend {}.'.format(settings['target'])
    # if only one reagent, concise description
    elif len(settings['reagents']) == 1:
        for k,v in settings['reagents'].items():
            protocol = 'Resuspend {} with {} {} of {}.'.format(settings['target'],v[0],v[1],k)
    # if multiple reagents, list...
    else:
        protocol = 'Resuspend {} with:'.format(settings['target'])
        for k,v in settings['reagents'].items():
            protocol += '\n\t> {} - {} {}'.format(k,*v)

    # build protocol

    return finalize(protocol,settings)

# ---------------------------------------------------------------------------- #

def transfer(*args,**kwargs):

    """ Basic method: transfer """

    # method properties
    settings = shared_properties() 
    settings['container'] = None
    settings['target'] = 'sample'
    
    update(settings,args,kwargs) # update settings using inputs

    protocol = 'Transfer {} to {}.'.format(settings['target'],settings['container'])

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

def save(*args,**kwargs):
    
    """ Basic method: save """

    # method properties
    settings = shared_properties() 
    settings['target'] = 'sample'
    
    update(settings,args,kwargs) # update settings using inputs

    protocol = 'Save {}.'.format(settings['target'])

    return finalize(protocol,settings)

# ---------------------------------------------------------------------------- #

def plate(*args,**kwargs):
    
    """ Basic method: plate """

    # method properties
    settings = shared_properties() 
    settings['target'] = 'sample'
    settings['onto'] = None 
    
    update(settings,args,kwargs) # update settings using inputs

    if settings['onto']:
        protocol = 'Plate {} onto {}.'.format(settings['target'],settings['onto'])
    else:
        protocol = 'Plate {}.'.format(settings['target'],)

    return finalize(protocol,settings)

# ---------------------------------------------------------------------------- #

def inoculate(*args,**kwargs):
    
    """ Basic method: inoculate """

    # method properties
    settings = shared_properties() 
    settings['target'] = 'sample'
    settings['reagents'] = None 
    
    update(settings,args,kwargs) # update settings using inputs


    # if only one reagent, concise description
    if len(settings['reagents']) == 1:
        for k,v in settings['reagents'].items():
            protocol = 'Inoculate {} {} of {} with {}.'.format(v[0],v[1],k,settings['target'])
    # if multiple reagents, list...
    else:
        protocol = 'Inoculate {} into:'.format(settings['target'])
        for k,v in settings['reagents'].items():
            protocol += '\n\t> {} - {} {}'.format(k,*v)

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
    
def unit_tests():

    add_settings = {
        'reagents':
            {
            'buffer':(100,'uL'),
            },
        'temperature':(23,'C')
        }

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

    save_settings = {
        'target':'elution',
        'temperature':(4,'C')
        }

    plate_settings = {
        'target':'sample',
        'onto':'appropriate plates'
        }

    inoculate_settings = {
        'target':'sample',
        'reagents':{'LB':(100,'mL')}
        }

    print 'Add:',add(add_settings)
    print 'Mix:',mix(mix_settings)
    print 'Incubate:',incubate(incubate_settings)
    print 'Centrifuge:',centrifuge(centrifuge_settings)
    print 'Decant:',decant(decant_settings)
    print 'Thermocycle:',thermocycle(thermocycle_settings)
    print 'Resuspend:',resuspend(resuspend_settings)
    print 'Transfer:',transfer(transfer_settings)
    print 'Operate:',operate(operate_settings)
    print 'Save:',save(save_settings)
    print 'Plate:',plate(plate_settings)
    print 'Inoculate:',inoculate(inoculate_settings)

















