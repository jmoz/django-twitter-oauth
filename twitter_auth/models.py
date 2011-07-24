from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Based on http://www.numlock.ch/news/it/django-custom-model-field-for-an-unsigned-bigint-data-type/
#class PositiveBigIntegerField(models.PositiveIntegerField):
#    """Represents MySQL's unsigned BIGINT data type (works with MySQL only!)"""
#    empty_strings_allowed = False
#
#    def get_internal_type(self):
#        return "PositiveBigIntegerField"
#
#    def db_type(self, connection):
#        # This is how MySQL defines 64 bit unsigned integer data types
#        return "bigint UNSIGNED"

class MapTwitterToUser(models.Model):
    twitter_id  = models.BigIntegerField(null=False, blank=False)
    user        = models.ForeignKey(User)
  
    def __unicode__(self):
        return 'Twitter id: %s, User is: %s' % (self.twitter_id, self.user)
    
    class Meta:
        #ordering = ("-reverse_rank",)
        app_label = "twitter_auth"
        verbose_name = "maptwittertouser"
        verbose_name_plural = "maptwitteruserstotwitdegreeusers"

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