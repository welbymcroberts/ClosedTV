from django.db import models

# Create your models here.

class Area(models.Model):
    #areaid = models.IntegerField(unique)
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return "%d - %s" % (self.id, self.name)
class Region(models.Model):
    area = models.ForeignKey(Area)
    regionid = models.IntegerField()

class Channel(models.Model):
    region = models.ForeignKey(Region)
    number = models.IntegerField()
    nid = models.IntegerField()
    tid = models.IntegerField()
    sid = models.IntegerField()
    name = models.CharField(max_length=50)

class ScannedChannel(models.Model):
    fec = models.CharField(max_length=10)
    diseqc=models.CharField(max_length=10)
    diseqcrawdata=models.CharField(max_length=10)
    freq = models.CharField(max_length=10)
    lnbsel = models.CharField(max_length=10)
    lof = models.CharField(max_length=10)
    mod = models.CharField(max_length=10)
    sr = models.IntegerField()
    pol = models.CharField(max_length=1)
    nid = models.IntegerField()
    tid = models.IntegerField()
    sid = models.IntegerField()
    encrypt = models.IntegerField()
    type = models.IntegerField()
    chnum = models.IntegerField()
    chsubnum = models.IntegerField()
    ecm_pid = models.IntegerField()
    lof1 = models.CharField(max_length=10)
    lof2 = models.CharField(max_length=10)
    lofsw = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    provider = models.CharField(max_length=30)

