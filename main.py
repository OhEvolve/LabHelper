
"""
from protocols.digest import Digest
from database.restriction_enzyme import RestrictionEnzyme

re = RestrictionEnzyme(name='XhoI')

digest = Digest(enzyme = 'XhoI')

print 'This is a digestion protocol:'
print digest.protocol()
print digest.output.info()
"""

from protocols.basics import mix

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




