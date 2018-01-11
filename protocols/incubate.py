
"""

Incubate Class

"""


# standard libraries

# nonstandard libraries

# homegrown libraries
from methods import convert_volume,fill_reaction

#--------------------------------------#
#           Main     Methods           #
#--------------------------------------#

class Incubate:

    def __init__(self,*args,**kwargs):

        """ Hold mixture at certain condition """

        self.settings = {
            'preparation':'Gently mix by flicking.',
            'temperature':(23,'C'),
            'time':(1,'hour'),
            'movement':'stationary',
            }

        # warnings
        self.warnings = {}

        # update settings
        for arg in args: self.settings.update(arg)
        self.settings.update(kwargs)

    def protocol(self):

        """ Print project """

        # local namespace
        preparation = self.settings['preparation']
        temperature = self.settings['temperature']
        time = self.settings['time']
        movement = self.settings['movement']

        # build protocol
        protocol = []
        protocol.append(preparation)
        protocol.append('Incubate at {} {} for {} {} while {}.'.format(*temperature + time + (movement,)))

        return '\n'.join(protocol)

#--------------------------------------#

if __name__ == "__main__":

    # incubate protocol test
    incubate = Incubate()
    print incubate.protocol()

