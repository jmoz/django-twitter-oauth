# django-twitter-oauth (forked from http://github.com/henriklied/django-twitter-oauth)

([Original snippet](http://www.djangosnippets.org/snippets/1353/) based on [Simon Willison's Fire Eagle views](http://www.djangosnippets.org/snippets/655/) )

I wanted to learn Python and Django so I decided to work on a web app in my free time. What I wanted to do included Twitter authentication and all information I found I felt were bits and pieces of the full puzzle, or parts were a bit out of date. I put everything I could together into a Django app I forked and am releasing it back. Thank you to all those that have code in this mashup. I am still in the middle of working on it so it may change, possibly significantly, over time. Give me some time to work out the kinks but I am confident that it works well.
## Requirements
- Django 1.3 (others may work, but I am using 1.3 right now)
- twitter-python http://code.google.com/p/python-twitter/
- You must [register a new Twitter oAuth application](http://twitter.com/oauth_clients/). Set your application's Callback URL to "http://mysite.com/twitter/return/".

## Installation
Add the 'twitter_app' directory somewhere on your 'PYTHONPATH', put it into 'INSTALLED_APPS' in your settings file.
Fill in your CONSUMER_KEY and CONSUMER_SECRET in your settings file.

- Add this line to your Django project's urlconf: 
    url(r'^twitter/', include('twitter_app.urls')),
By default, things should just work (as long as you specify the proper template location and what not).
To use this in a production-type application, you are going to want to specify two settings in your settings.py file:
TWITTER_AUTH_HOME - the named url pattern of where your home view is (useful when the user logs out, for instance)
TWITTER_AUTH_AUTHENTICATED - the named url pattern of where you are sent when you are redirected back after being authenticated by twitter or if you try to access a page once you are already logged in.


I've added a TwitterAuthUserProfile.py file that you can extend in your application to add supplemental user profile fields. If you don't require anything extra, you can extend TwitterAuthUserProfile and leave it blank. If you are specifying a Meta inner class, set abstract = False. At the bottom of your app specific profile class, put:

  def create_user_profile(sender, instance, created, **kwargs):
  	if created:
  		profile, created = <YOUR_APP_PROFILE>.objects.get_or_create(user=instance)

  post_save.connect(create_user_profile, sender=User)

Now you should be good to go!

## API Usage
from twitter_auth.util.utils import *


Then with an authenticated user in the request object:
    

    #This gets the authenticated twitter.Api object
    api = get_twitter_api(request)
    users = api.GetFriends()
