#!/usr/bin/env python
"""Twitter Authentication backend for Django

Requires:
AUTH_PROFILE_MODULE to be defined in settings.py

The profile models should have following fields:
        access_token
        url
        location
        description
        profile_image_url
"""
#Based on http://djangosnippets.org/snippets/1473/

from django.conf import settings
from django.contrib.auth.models import User
from twitter_auth.models.MapTwitterToUser import MapTwitterToUser
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
        '''authenticates the token by requesting user information from twitter
        '''
        if oauth_access_token is None:
            return None

        api = twitter.Api(consumer_key=CONSUMER_KEY, 
                          consumer_secret=CONSUMER_SECRET, 
                          access_token_key=oauth_access_token.key, 
                          access_token_secret=oauth_access_token.secret)
        try:
            twitter_user = api.VerifyCredentials()
            if twitter_user is None:
                return None
        except:
            # If we cannot get the user information, user cannot be authenticated
            return None

        mtu = None
        try:
            mtu = MapTwitterToUser.objects.get(twitter_id=twitter_user.id)
        except MapTwitterToUser.DoesNotExist:
            u = User.objects.create_user(twitter_user.screen_name,
                                         '%s@example.com' % twitter_user.screen_name,
                                         User.objects.make_random_password(length=12))
            u.save()
            mtu = MapTwitterToUser()
            mtu.twitter_id = twitter_user.id
            mtu.user = u
            mtu.save()

        user = User.objects.get(pk=mtu.user.id)
        
        # Let's update the user object with any new info.
        # This would not be needed if Twitter disallowed username changes.
        user.first_name = twitter_user.name
        user.username = twitter_user.screen_name
        user.email ='%s@example.com' % twitter_user.screen_name
        user.save()

        # Get the user profile and update it
        userprofile = user.get_profile()
        userprofile.access_token = oauth_access_token.to_string()
        userprofile.url = twitter_user.url
        userprofile.location = twitter_user.location
        userprofile.description = twitter_user.description
        userprofile.profile_image_url = twitter_user.profile_image_url
        userprofile.save()

        return user
        
    def get_user(self, id):
        try:
            return User.objects.get(pk=id)
        except:
            return None
