import oauth
#import urllib
import urllib2
import httplib
import twitter

try:
    import simplejson
except ImportError:
    try:
        import json as simplejson
    except ImportError:
        try:
            from django.utils import simplejson
        except:
            raise "Requires either simplejson, Python 2.6 or django.utils!"


from django.conf import settings
from twitter_auth.models.MapTwitterToUser import MapTwitterToUser
from django.contrib.auth.models import User


signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()

SERVER = getattr(settings, 'OAUTH_SERVER', 'twitter.com')
REQUEST_TOKEN_URL = getattr(settings, 'OAUTH_REQUEST_TOKEN_URL', 'https://%s/oauth/request_token' % SERVER)
ACCESS_TOKEN_URL = getattr(settings, 'OAUTH_ACCESS_TOKEN_URL', 'https://%s/oauth/access_token' % SERVER)
AUTHORIZATION_URL = getattr(settings, 'OAUTH_AUTHORIZATION_URL', 'http://%s/oauth/authorize' % SERVER)

CONSUMER_KEY = getattr(settings, 'CONSUMER_KEY', 'YOUR_KEY')
CONSUMER_SECRET = getattr(settings, 'CONSUMER_SECRET', 'YOUR_SECRET')

CONSUMER = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET)
CONNECTION = httplib.HTTPSConnection(SERVER)


def request_oauth_resource(url, access_token, parameters=None, signature_method=signature_method, http_method="GET"):
    """
    usage: request_oauth_resource( consumer, '/url/', your_access_token, parameters=dict() )
    Returns a OAuthRequest object
    """
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(
        consumer, token=access_token, http_method=http_method, http_url=url, parameters=parameters,
    )
    oauth_request.sign_request(signature_method, consumer, access_token)
    return oauth_request


def fetch_response(oauth_request):
    try:
        url = oauth_request.to_url()
        response = urllib2.urlopen(url) 
        s = response.read()
        return s
    except IOError, e:
        if hasattr(e, 'code'): # HTTPError
            print 'http error code: ', e.code
        elif hasattr(e, 'reason'): # URLError
            print "can't connect, reason: ", e.reason
        raise
    return None

def get_unauthorised_request_token():
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(
        CONSUMER, http_url=REQUEST_TOKEN_URL
    )
    oauth_request.sign_request(signature_method, CONSUMER, None)
    resp = fetch_response(oauth_request)
    token = oauth.OAuthToken.from_string(resp)
    return token


def get_authorisation_url(token):
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(
        CONSUMER, token=token, http_url=AUTHORIZATION_URL
    )
    oauth_request.sign_request(signature_method, CONSUMER, token)
    return oauth_request.to_url()

def get_oauth_url(oauth_request):
    return fetch_response(oauth_request)

def exchange_request_token_for_access_token(request_token, signature_method=signature_method, params={}):
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(
        CONSUMER, token=request_token, http_url=ACCESS_TOKEN_URL, parameters=params
    )
    oauth_request.sign_request(signature_method, CONSUMER, request_token)
    resp = get_oauth_url(oauth_request)
    return oauth.OAuthToken.from_string(resp)

def get_oauth_token_from_string(string):
    token = oauth.OAuthToken.from_string(string)
    return token

def get_twitter_api_from_request(request):
    api = None
    if request.user.is_authenticated():
        #If the user is logged in, then we can use the authenicated Twitter API.
        token = get_oauth_token_from_string(request.user.get_profile().access_token)
        api = twitter.Api(consumer_key=CONSUMER_KEY, 
                          consumer_secret=CONSUMER_SECRET, 
                          access_token_key=token.key, 
                          access_token_secret=token.secret)
    else:
        #otherwise we have limited access
        api = twitter.Api(consumer_key=CONSUMER_KEY, 
                          consumer_secret=CONSUMER_SECRET)
    return api


def get_twitter_user_from_twitter(twitter_user_name, api):
    """
    Returns the twitter.User user associated with the twitter_user_name.
    """
    twitter_user = api.GetUser(twitter_user_name)
    if twitter_user is None:
        return None
    
    return twitter_user
        
        
def get_or_create_user(twitter_user, create_if_not_found = True):
    """
    Given the twitter.User twitter_user, return the System's user if found.
    If not found and if create_if_not_found is True, create the System
    user and return it, otherwise return None
    """
    mtu = None
    # If we've just created the user, no need to update the user
    # Flag for that
    update = True
    try:
        mtu = MapTwitterToUser.objects.get(twitter_id=twitter_user.id)
    except MapTwitterToUser.DoesNotExist:
        if not create_if_not_found:
            return None
        # If we want to import this user into the system, do it here and return it
        #u = User.objects.create_user(twitter_user.screen_name)
        #u.save()
        u = User.objects.create_user(twitter_user.screen_name,
                                     '%s@example.com' % twitter_user.screen_name,
                                     User.objects.make_random_password(length=12))        
        mtu = MapTwitterToUser()
        mtu.twitter_id = twitter_user.id
        mtu.user = u
        mtu.save()
        update = False


    user = User.objects.get(pk=mtu.user.id)
    user_profle = user.get_profile()
    
    if update is True:
        user.first_name = twitter_user.name
        user.username = twitter_user.screen_name
        user.save()

    # Get the user profile and update it
    userprofile = user.get_profile()
    userprofile.url = twitter_user.url
    userprofile.location = twitter_user.location
    userprofile.description = twitter_user.description
    userprofile.profile_image_url = twitter_user.profile_image_url
    userprofile.save()

    return user