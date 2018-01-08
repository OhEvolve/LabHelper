
"""

Mix Class

"""


# standard libraries

# nonstandard libraries

# homegrown libraries
from methods import convert_volume,fill_reaction

#--------------------------------------#
#           Main     Methods           #
#--------------------------------------#

class Mix:

    def __init__(self,*args,**kwargs):

        """ Mix reagents """

        # mixture settings
        self.settings = {
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

        # warning
        self.warnings = {}

        # update settings
        for arg in args: self.settings.update(arg)
        self.settings.update(kwargs)

    def protocol(self):

        """ Print project """

        # local namespace
        filler = self.settings['filler']
        temperature = self.settings['temperature']
        total = self.settings['total']

        # find reaction volumes
        abs_reagents = [(k,convert_volume(v,total)) for k,v in self.settings['reagents'].items()]
        abs_reagents.append((filler,fill_reaction(total,*abs_reagents)))

        # build protocol
        protocol = []
        protocol.append('Combine the following reagents at {} {}:'.format(*temperature))
        for k,v in abs_reagents:
            protocol.append('  > {} - {} {}'.format(k,*v))
        protocol.append('Total reaction volume = {} {}'.format(*total))

        return '\n'.join(protocol)

#--------------------------------------#

if __name__ == '__main__':
    # mix protocol test
    mix = Mix()
    print mix.protocol()

