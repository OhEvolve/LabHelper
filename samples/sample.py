

global cc
cc = 80

class Sample:
    
    def __init__(self):

        # metadata
        self.name = 'Sample'
        self.author = 'PVH'
        # content types
        self.contents = []
        # overall attributes
        self.volume = 0

    def __iadd__(self,item):

        self.contents.append(item)
        return self
         
    def list_contents(self,**kwargs):
        settings = {
                'concise':False
                }

        linebreak = '\n{}\n'.format('-----'.center(cc)) # define linebreak str 

        info   = 'Sample name: {}'.format(self.name).center(cc) + '\n'
        info  += 'Author: {}'.format(self.author).center(cc) + '\n\n'
        info  += '--- Contents ---'.center(cc) + '\n'

        if len(self.contents) == 0:
            info += '(None)'.center(cc)
        else:
            info += linebreak.join([content.info()
                for content in self.contents])

        print info



class DNA:

    def __init__(self,):
        self.type = 'DNA' 


class Cell:

    def __init__(self,name,species,count):

        self.name = name
        self.species = species
        self.count = count

    def info(self):

        #  create string with info about object
        info = []
        info.append(' --- CELLS ---'.center(cc))
        info.append('Solution: {}'.format(self.name).center(cc))
        info.append('Volume: {}'.format(self.volume).center(cc))

        return '\n'.join(info)


class Solution:

    def __init__(self,name,volume):

        self.name = name
        self.volume = volume

    def info(self):

        #  create string with info about object
        info = []
        info.append(' --- SOLUTION ---'.center(cc))
        info.append('Name: {}'.format(self.name).center(cc))
        info.append('Volume: {}'.format(self.volume).center(cc))

        return '\n'.join(info)


sample = Sample()
elution_buffer = Solution('Elution Buffer','50 uL')


sample += elution_buffer


sample.list_contents()












