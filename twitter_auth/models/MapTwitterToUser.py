from django.db import models
from django.contrib.auth.models import User

# Based on http://www.numlock.ch/news/it/django-custom-model-field-for-an-unsigned-bigint-data-type/
# I am not 100% about this. Hasn't been tested yet.
class PositiveBigIntegerField(models.PositiveIntegerField):
    """Represents MySQL's unsigned BIGINT data type (works with MySQL only!)"""
    empty_strings_allowed = False

    def get_internal_type(self):
        return "PositiveBigIntegerField"

    def db_type(self, connection):
        # This is how MySQL defines 64 bit unsigned integer data types
        return "bigint UNSIGNED"

class MapTwitterToUser(models.Model):
    twitter_id  = PositiveBigIntegerField()
    user        = models.ForeignKey(User)
  
    def __unicode__(self):
        return 'Twitter id: %s, User is: %s' % (self.twitter_id, self.user)
    
    class Meta:
        #ordering = ("-reverse_rank",)
        app_label = "twitter_auth"
        verbose_name = "maptwittertouser"
        verbose_name_plural = "maptwitteruserstotwitdegreeusers"