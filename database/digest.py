
"""

Digest Experiment

"""


# standard libraries
from re import finditer

# nonstandard libraries

# homegrown libraries
from mix import Mix
from incubate import Incubate
from sequence import Sequence
from restriction_enzyme import RestrictionEnzyme
from methods import rcomp

#--------------------------------------#
#           Main     Methods           #
#--------------------------------------#

class Digest:

    def __init__(self,*args,**kwargs):

        """ Digest input """

        # digestion settings
        settings = {
                'input':None,
                'enzyme':None
                   }

        # update settings
        for arg in args: settings.update(arg)
        settings.update(kwargs)

        # use defaults if input and enzymes not selected
        if settings['input'] == None:
            settings['input'] = 'XhoI-Plasmid'
        if settings['enzyme'] == None:
            settings['enzyme'] = 'XhoI'

        # check database for sequences
        if isinstance(settings['input'],str):
            sequence = Sequence(name=settings['input'])
            sequence.load()
        elif isinstance(settings['input'],object):
            sequence = settings['input']
        else:
            raise TypeError('Unknpwn input type passed to function <{}>!'.format(
                type(settings['input'])))

        # check database for enzyme
        # TODO: add compatibility for multiple enzyme reaction
        if isinstance(settings['enzyme'],str):
            enzyme = RestrictionEnzyme(name=settings['enzyme'])
            enzyme.select_size()
            enzyme_name = enzyme.name
            enzyme_volume = (1./enzyme.units_per_ml,'mL')
            enzyme_temp = (enzyme.active_temperature,'C')
        elif isinstance(settings['enzyme'],object):
            sequence = settings['enzyme']
        else:
            raise TypeError('Unknpwn enzyme type passed to function <{}>!'.format(
                type(settings['enzyme'])))


        # TODO: break sequence at site

        # reagent listing
        mix_settings = {
                'reagents':
                    {
                    enzyme_name:enzyme_volume,
                    'NEBuffer':(10,'X'),
                    },
                'filler':'dH2O',
                'total':(50,'uL'),
                'temperature':(-4,'C')
                    }

        incubate_settings = {
            'preparation':'Gently mix by flicking.',
            'temperature':enzyme_temp,
            'time':(1,'hour'),
            'movement':'stationary'
            }

        # sinc
        self.protocols = [Mix(mix_settings),
                          Incubate(incubate_settings)]


        # build output dictionary

        output = _cut(sequence,enzyme)

        return output


    def protocol(self):

        """ Returns readable protocol """

        protocol = [p.protocol() for p in self.protocols]

        return '\n-----\n'.join(protocol)

#--------------------------------------#
#           Internal  Method           #
#--------------------------------------#

def _cut(seq_obj,enzyme_obj):
    
    """ Output fragments of sequence based on input """

    # assertion check
    assert isinstance(seq_obj,object),"Did not pass _cut sequence object"
    assert isinstance(enzyme_obj,object),"Did not pass _cut enzyme object"

    # only allow recognition at dsDNA sites
    if seq_obj.form == 'dsDNA':
        ds_sequence = seq_obj.sequence
    elif all(f in "'|," for f in seq_obj.form):
        assert len(seq_obj.form) == len(seq_obj.sequence)
        ds_sequence = ''.join(s if f == '|' else '-' 
                for s,f in zip(seq_obj.sequence,seq_obj.form))

    ecs = enzyme_obj.sequence # shorthard for enzyme cutsite

    # look for cutsites in both 5'->3' and 3'->5' directions, unique starts
    cutsite_indices  = [m.start() 
            for m in finditer(ecs,ds_sequence)]
    cutsite_indices_rev = [m.start()
            for m in finditer(rcomp(ecs),rcomp(ds_sequence))]

    # find relative location of break
    if enzyme_obj.site_type == 'internal':
        site_location = enzyme_obj.site_location
    if enzyme_obj.site_type == 'external':

        esl = enzyme_obj.site_location

        if any(e == 0 for e in esl):
            if all(e >= 0 for e in esl):
                site_location = tuple(s + len(ecs) for s in esl)
            elif all(e <= 0 for e in esl):
                site_location = tuple(s for s in esl)

        else:
            site_location = tuple(s if s < 0 else s + len(ecs) for s in esl)
    
    # find break sites
    break5 = list(set([0] + [c + site_location[0] for c in cutsite_indices] + \
             [len(ds_sequence) - (c + site_location[1]) for c in cutsite_indices_rev]))
    break3 = list(set([0] + [c + site_location[1] for c in cutsite_indices] + \
             [len(ds_sequence) - (c + site_location[0]) for c in cutsite_indices_rev]))

    # create new sequence objects
    assert len(break5) == len(break3), "Number of 5'/3' breaks not equal"

    for i in xrange(1,len(break5)):
        

    return 

    # check if there actually is a cutsite in sequence

    # check for overlaps


#--------------------------------------#
#               Testing                #
#--------------------------------------#

if __name__ == '__main__':

    digest = Digest(enzyme='BsmI')
    print digest.protocol()
