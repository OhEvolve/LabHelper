
"""

PCR Experiment

"""


# standard libraries
#from re import finditer
#from copy import deepcopy

# nonstandard libraries

# homegrown libraries
from protocols.mix import Mix
from protocols.incubate import Incubate
from database.sequence import Sequence
from database.restriction_enzyme import RestrictionEnzyme
from methods import rcomp
from methods import obj_update

#--------------------------------------#
#           Main     Methods           #
#--------------------------------------#

class PCR:

    def __init__(self,*args,**kwargs):

        """ PCR input """

        # digestion settings
        settings = {
                'sequence':None,
                'enzyme':None
                   }

        # update settings
        for arg in args: settings.update(arg)
        settings.update(kwargs)

        # use defaults if input and enzymes not selected
        if settings['sequence'] == None:
            settings['sequence'] = 'XhoI-Plasmid'
        if settings['enzyme'] == None:
            settings['enzyme'] = 'XhoI'

        # check database for sequences
        if isinstance(settings['sequence'],str):
            sequence = Sequence(name=settings['sequence'])
            sequence.load()
        elif isinstance(settings['sequence'],object):
            sequence = settings['sequence']
        else:
            raise TypeError('Unknpwn sequence type passed to function <{}>!'.format(
                type(settings['sequence'])))

        # check database for enzyme
        if isinstance(settings['enzyme'],str):
            enzyme = Polymerase(name=settings['enzyme'])
        elif isinstance(settings['enzyme'],object):
            enzyme = settings['enzyme']
        else:
            raise TypeError('Unknpwn enzyme type passed to function <{}>!'.format(
                type(settings['enzyme'])))
        
        enzyme.select_size()
        enzyme_name = enzyme.name
        enzyme_volume = (1./enzyme.units_per_ml,'mL')
        enzyme_temp = (enzyme.active_temperature,'C')


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

        # Output cut sequence object (breaks in backbone)

        cut_sequence = deepcopy(sequence) # copies the sequence

        breaks = _cut(cut_sequence,enzyme) # add backbone breaks

        obj_update(cut_sequence,breaks) # add breaks to sequence
        cut_sequence.add_origin('digest with {}'.format(enzyme.name)) # add origin

        self.output = cut_sequence


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
    break5 = list(set([c + site_location[0] for c in cutsite_indices] + \
             [len(ds_sequence) - (c + site_location[1]) for c in cutsite_indices_rev]))
    break3 = list(set([c + site_location[1] for c in cutsite_indices] + \
             [len(ds_sequence) - (c + site_location[0]) for c in cutsite_indices_rev]))

    # create new sequence objects
    assert len(break5) == len(break3), "Number of 5'/3' breaks not equal"

    return {"break_5":break5,"break_3":break3}

    # check if there actually is a cutsite in sequence

    # check for overlaps


#--------------------------------------#
#               Testing                #
#--------------------------------------#

if __name__ == '__main__':

    digest = Digest(enzyme='BsmI')
    print digest.protocol()
