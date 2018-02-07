
def Quikchange(inputs):

    """ Manage inputs and outputs """
   
    necessary_keys = ['primer5','primer3','plasmid']

    # check input is valid
    if _check_missing_keys(inputs,necessary_keys):
        return None
    
    # 
    
        

# ------------------------ #
# --- Internal Methods --- #
# ------------------------ #

def _check_missing_keys(my_dict,necessary_keys):

    """ Check for keys in input dictionary """ 
    
    if not isinstance(inputs,dict):
        print "Input not type <dict>"
        return True 

    for key in necessary_keys:
        if not key in my_dict.keys():
            print '{} key missing from input'.format(key)
            return True 

    return False

# ------------------------ #

