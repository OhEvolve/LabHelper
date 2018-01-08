
from protocols.digest import Digest
from database.restriction_enzyme import RestrictionEnzyme

re = RestrictionEnzyme(name='XhoI')

digest = Digest(enzyme = 'XhoI')

print 'This is a digestion protocol:'
print digest.protocol()
print digest.output.info()

