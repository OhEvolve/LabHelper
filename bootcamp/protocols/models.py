
'''
Models for the reagents app
'''

from django.db import models

from bootcamp.groups.models import Group
from django.contrib.auth.models import User

# library imports
from django.db import models
from django.forms import ModelMultipleChoiceField


class Protocol(models.Model):

    CHOICES = (
        ('Custom','Custom'),
        ('Miniprep','Miniprep'),
        ('Zymoprep','Zymoprep'),
        ('Transform','Transform'),
        ('Electroporation','Electroporation'),
        ('Transduction','Transduction'),
        ('RTPCR','RT-PCR'),
        ('Transciption','Transcription'),
        ('GelElectrophoresis','Gel Electrophoresis'),
        ('GelExraction','Gel Extraction'),
        ('PCR','PCR'),
        ('GibsonAssembly','Gibson Assembly'))

    IO_template = models.CharField(max_length=15,default='',null=True)

    groups = models.ManyToManyField(Group, through='ProtocolOwnership')
    creator = models.ForeignKey(User,on_delete=models.CASCADE,related_name='protocol_creator',default=1)

class ProtocolOwnership(models.Model):

    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE)
    group = models.ForeignKey(Group,on_delete=models.CASCADE)

    added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Ownership'
        unique_together = ["protocol", "group"]

class Step(models.Model):

    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE,default=None)

    CHOICES = (
        ('-----','-----'),
        ('Mix', 'Mix'),
        ('Incubate', 'Incubate'),
        ('Centrifuge', 'Centrifuge'),
        ('Decant', 'Decant'),
        ('Thermocycle', 'Thermocycle'),
        ('Resuspend', 'Resuspend'),
        ('Transfer', 'Transfer'),
        ('Operate', 'Operate'))


    # common features
    name        = models.CharField(max_length=255,choices=CHOICES,default='-----')
















