from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class TwitterAuthUserProfile(models.Model):
    user                = models.ForeignKey(User, unique=True)
    access_token        = models.CharField(max_length=255, blank=True, null=True, editable=False)
    profile_image_url   = models.URLField(blank=True, null=True)
    location            = models.CharField(max_length=100, blank=True, null=True)
    url                 = models.URLField(blank=True, null=True)
    description         = models.CharField(max_length=160, blank=True, null=True)
    last_update         = models.DateTimeField(blank=False, auto_now=True)
    
    def __str__(self):
        return '%s\'s profile' % self.user
        
    #Let's make this an abstract class    
    class Meta(object):
        abstract = True

#def create_user_profile(sender, instance, created, **kwargs):
#	if created:
#		profile, created = TwitterAuthUserProfile.objects.get_or_create(user=instance)

#post_save.connect(create_user_profile, sender=User)