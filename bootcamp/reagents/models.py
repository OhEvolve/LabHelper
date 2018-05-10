from django.db import models

'''
Models for the reagents app
'''

# library imports
from django.db import models
from django.forms import ModelMultipleChoiceField


SEQUENCE_FORM_CHOICES = (("  plasmid  ",     "plasmid"),
                         ("  genomic  ",     "genomic"),
                         ("recombinant", "recombinant"))
                         
SEQUENCE_SHAPE_CHOICES = (("circular",   "circular"),
                          (" linear ",     "linear"))

SEQUENCE_MATERIAL_CHOICES = ((" dsDNA ",       "dsDNA"),
                             (" ssDNA ",       "ssDNA"),
                             (" dsRNA ",       "dsRNA"),
                             (" ssRNA ",       "ssRNA"),
                             ("protein",     "protein"))                          

SOLUTION_CONTENT_CHOICES = ((" liquid "," liquid "),
                            ("  solid ","  solid "),
                            ("biologic","biologic"))

MORPHOLOGY_CHOICES = (("fibro", "fibroblastic"),
                      ("epith", "epithelial-like"),
                      ("lymph", "lymphoblast-like"))

""" UNIT CHOICES """

VOLUME_UNITS_CHOICES = (("uL","uL"),
                        ("mL","mL"),
                        (" L"," L"))

MASS_UNITS_CHOICES = (("ng/L","ng/L"),
                      ("ug/L","ug/L"),
                      ("mg/L","mg/L"),
                      (" g/L"," g/L"),
                      (" nM "," nM "),
                      (" uM "," uM "),
                      (" mM "," mM "),
                      ("  M ","  M "))

MW_UNITS_CHOICES = (("kg/mol","kg/mol"),
                    (" g/mol"," g/mol"))

TIME_UNITS_CHOICES = (("  s","s"),
                      ("min","min"),
                      ("  h","h"),
                      ("  d","y"))

class Matter(models.Model):

    """ Matter reference object (base class) """

    name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255,blank=True)

    def __str__(self):
            #return '{} - {}'.format(type(self).__name__,self.name)
            return self.name

class Liquid(Matter):
	
    """ Liquid reference object """
    
    pass
	
	
class Solid(Matter):
	
    """ Solid reference object """
    
    mw       = models.FloatField(default=0,verbose_name='Molecular weight')
    mw_units = models.CharField(max_length=6,choices=MW_UNITS_CHOICES,default=' g/mol',verbose_name='Units')
    
	
class Biologic(Matter):
   	
   """ Biologic refernce object """
   
   sequence = models.TextField(max_length=10000)
   form = models.CharField(max_length = 11,choices = SEQUENCE_FORM_CHOICES)
   shape = models.CharField(max_length = 8,choices = SEQUENCE_SHAPE_CHOICES)
   material = models.CharField(max_length = 7,choices = SEQUENCE_MATERIAL_CHOICES)
                  		   

class Cell(Matter):
   	
   """ Biologic refernce object """

   biologics = models.ManyToManyField(Biologic,through='CellBiologicContent',symmetrical=False)
   
   species = models.TextField(max_length=255,default='E.Coli')
   morphology = models.CharField(max_length = 5,choices = MORPHOLOGY_CHOICES,default='-----')
   shaken = models.BooleanField(default=False)
   media_preference = models.CharField(max_length = 50,default='')
   doubling_time = models.FloatField(default=1)
   doubling_time_units = models.CharField(max_length=3,choices=TIME_UNITS_CHOICES,default='  h')
   culture_environment = models.CharField(max_length = 255,default='')
                  		   
class Solution(Matter):

    liquids   = models.ManyToManyField(Liquid,through='LiquidContent',symmetrical=False)
    solids    = models.ManyToManyField(Solid,through='SolidContent',symmetrical=False)
    biologics = models.ManyToManyField(Biologic,through='BiologicContent',symmetrical=False)

""" Through object definition """

class LiquidContent(models.Model):
    reagent  = models.ForeignKey(Liquid,on_delete=models.CASCADE) # may be wrong on_delete behavior
    solution = models.ForeignKey(Solution,on_delete=models.CASCADE) # may be wrong on_delete behavior
    volume       = models.FloatField(default=1)
    volume_units = models.CharField(max_length=2,choices=VOLUME_UNITS_CHOICES,default=' L')

class SolidContent(models.Model):
    reagent  = models.ForeignKey(Solid,on_delete=models.CASCADE) # may be wrong on_delete behavior
    solution = models.ForeignKey(Solution,on_delete=models.CASCADE) # may be wrong on_delete behavior
    mass       = models.FloatField(default=0)
    mass_units = models.CharField(max_length=4,choices=MASS_UNITS_CHOICES,default=' g/L')
            
class BiologicContent(models.Model):
    reagent  = models.ForeignKey(Biologic,on_delete=models.CASCADE) # may be wrong on_delete behavior
    solution = models.ForeignKey(Solution,on_delete=models.CASCADE) # may be wrong on_delete behavior
    mass       = models.FloatField(default=0)
    mass_units = models.CharField(max_length=4,choices=MASS_UNITS_CHOICES,default=' g/L')

class CellBiologicContent(models.Model):
    reagent  = models.ForeignKey(Biologic,on_delete=models.CASCADE) # may be wrong on_delete behavior
    cell = models.ForeignKey(Cell,on_delete=models.CASCADE) # may be wrong on_delete behavior
    #media preference, doubling time, morphology, adherent vs suspension, environment, shaken vs. not shaken)
