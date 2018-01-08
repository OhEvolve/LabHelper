
"""

Protocol for restriction enzyme digests

"""

def procedure(*args,**kwargs):
    
    # reagent listing
    reagents = {
            'sample':(10,'units'),
            'dsDNA':(1,'ug'),
            'buffer':(5,'uL'),
            'total':(50,'uL')
            }
    
    # reaction conditions
    reaction = {
            'preparation':'gently mix',
            'temperature':None,
            'time':(1,'hour'),
            'movement':'stationary',
            }

    # case recommendations 
    recommendations = {
            'low quality dsDNA':
                {
                    ('reaction','time'):('*5,*10')
                }
            }

    # warnings
    warnings = {
            ('reaction','preparation'):'Do not centrifuge',
            ('reagents','total'):'Glycerol should not exceed 10%'
            }
    
    recommended_digestion = {
