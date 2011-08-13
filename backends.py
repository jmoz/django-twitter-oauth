#!/usr/bin/env python
#Based on http://djangosnippets.org/snippets/1473/

from django.conf import settings
from django.contrib.auth.models import User
from twitter_auth.models import MapTwitterToUser
from twitter_auth.util.twitterutils import get_or_create_user
import twitter


CONSUMER_KEY = getattr(settings, 'CONSUMER_KEY', 'YOUR_KEY')
CONSUMER_SECRET = getattr(settings, 'CONSUMER_SECRET', 'YOUR_SECRET')

class TwitterBackend:
    """TwitterBackend for authentication
    """
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False
    
    def authenticate(self, oauth_access_token = None):
        """
        Authenticates the token by requesting user information from twitter
        """
        if oauth_access_token is None:
            print '1'
            return None

        api = twitter.Api(consumer_key=CONSUMER_KEY, 
                          consumer_secret=CONSUMER_SECRET, 
                          access_token_key=oauth_access_token.key, 
                          access_token_secret=oauth_access_token.secret)
        try:
            twitter_user = api.VerifyCredentials()
            if twitter_user is None:
                print '2'                
                return None
        except:
            # If we cannot get the user information, user cannot be authenticated
            print '3'
            return None
        
        #TODO - as a possible optimization, return the user and profile to save on a sql call
        user = get_or_create_user(twitter_user)
        
        if user is not None:
            userprofile = user.get_profile()
            userprofile.access_token = oauth_access_token.to_string()
            userprofile.save()
        
        return user
        

        
    def get_user(self, id):
        try:
            return User.objects.get(pk=id)
        except:
            return None
