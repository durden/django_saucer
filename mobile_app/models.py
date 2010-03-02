from django.db import models

class Beer(models.Model):
    """Beer"""

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    style = models.CharField(max_length=100)
    descr = models.TextField()
    date = models.DateField(auto_now=True)
    avail = models.BooleanField()

    def __str__(self):
        """String representation beer"""
        return "%s (%s): " % (self.name, self.type)

    def get_absolute_url(self):
        """URL for object"""
        return "/beer/%d" % (self.id)
