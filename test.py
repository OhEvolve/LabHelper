

import requests


url = 'https://www.genscript.com/tools/codon-frequency-table'
data = dict(organism="Mouse-mouse")

r = requests.post(url, data=data, allow_redirects=True)
print r.content

# TODO: strip space and lowercase
species_dict = {
                "e.coli":"Escherichia coli-bac",
                "yeast":"Yeast-yeast"
                "insect":"Insect-inv"
                "c.elegans":"C.elegans-celegans"
                "drosophilia":"Drosophila melanogaster-drosophila"
                "human":"Human-human"
                "mouse":"Mouse-mouse"
                "rat":"Rat-rat"
                "pig":"Pig-pig"
                "pichia":"Pichia pastoris-pichia"
                "arabidopsis":"Arabidopsis thaliana-arabidopsis"
                "streptomyces":"Streptomyces-streptomyces"
                "corn":"Zea mays (Maize)-maize"
                "tobacco":"Nicotiana tabacum (Tabacco)-tobacco"
                "yeast":"Saccharomyces cerevisiae (gbpln)-gbpln"
                "hamster":"Cricetulus griseus (CHO)-cho"
               }

