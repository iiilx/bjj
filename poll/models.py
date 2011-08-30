from django.db import models

class Poll(models.Model):
    question = models.CharField('Poll Question', max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add = True)
    open = models.BooleanField(default = True)

    def __unicode__(self):
        return self.question
 
class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField(max_length=5, default=0)
    
    def __unicode__(self):
        return "%s: %s" % (self.poll, self.choice)

class Vote(models.Model):
    poll = models.ForeignKey(Poll)
    ip = models.IPAddressField()
   
    def __unicode__(self):
        return "%s: %s" %(self.poll, self.ip) 
    
    class Meta:
        unique_together = ("ip", "poll")
