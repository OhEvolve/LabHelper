
"""
from protocols.digest import Digest
from database.restriction_enzyme import RestrictionEnzyme

re = RestrictionEnzyme(name='XhoI')

digest = Digest(enzyme = 'XhoI')

print 'This is a digestion protocol:'
print digest.protocol()
print digest.output.info()
"""

from protocols.basics import * 

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
                 {'mode':'hold','temperature':(4,'C'),'time':('inf','')}]
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




print 'Mix:',mix(mix_settings)
print 'Incubate:',incubate(incubate_settings)
print 'Centrifuge:',centrifuge(centrifuge_settings)
print 'Decant:',decant(decant_settings)
print 'Thermocycle:',thermocycle(thermocycle_settings)
print 'Resuspend:',resuspend(resuspend_settings)
print 'Transfer:',transfer(transfer_settings)
print 'Operate:',operate(operate_settings)




