
"""
from protocols.digest import Digest
from database.restriction_enzyme import RestrictionEnzyme

re = RestrictionEnzyme(name='XhoI')

digest = Digest(enzyme = 'XhoI')

print 'This is a digestion protocol:'
print digest.protocol()
print digest.output.info()
"""

from protocols.basics import basics

settings = {}

settings['mix'] = {
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

settings['incubate'] = {
        'time':(5,'min'),
        'movement':'stationary'
        }

settings['centrifuge'] = {
        'time':(5,'min'),
        'speed':(1000,'g')
        }

settings['decant'] = {
        'action':'discard'
        }

settings['thermocycle'] = {
        'steps':[{'mode':'hold','temperature':(23,'C'),'time':(5,'min')},
                 {'mode':'hold','temperature':(72,'C'),'time':(30,'sec')},
                 {'mode':'hold','temperature':(55,'C'),'time':(30,'sec')},
                 {'mode':'goto','step':2,'repeat':24},
                 {'mode':'hold','temperature':(4,'C'),'time':('inf','')}]
        }

settings['resuspend'] = {
    'reagents':{'dH2O':(100,'uL')}
        }
        
settings['transfer'] = {
    'container':'Miniprep column'
    }

settings['operate'] = {
    'machine':'FPLC',
    'instructions':['Turn on',
                    'Run first protocol',
                    'Turn off']
    }

basics = basics()

for key,value in settings.items():
    print '{}: {}'.format(key,basics[key](value))






