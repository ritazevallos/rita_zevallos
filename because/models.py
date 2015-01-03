from django.db import models

class Beginning(models.Model):
    text = models.TextField()
    lat = models.FloatField(blank=True,null=True)
    lng = models.FloatField(blank=True,null=True)

    def __unicode__( self ):
        return self.text

class Ending(models.Model):
    text = models.TextField()
    beginning = models.ForeignKey(Beginning)
    lat = models.FloatField(blank=True,null=True)
    lng = models.FloatField(blank=True,null=True)

    def __unicode__( self ):
        return self.text