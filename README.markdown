# django-twitter-oauth (forked from http://github.com/henriklied/django-twitter-oauth)

([Original snippet](http://www.djangosnippets.org/snippets/1353/) based on [Simon Willison's Fire Eagle views](http://www.djangosnippets.org/snippets/655/) )

This will still be worked on by me as I'm using this Django app for a website I am building. Give me some time to work out the kinks but I am fairly confident that it works decently well.
## Requirements
- Django 1.3 (others may work, but I am using 1.3 right now)
- twitter-python http://code.google.com/p/python-twitter/
- You must [register a new Twitter oAuth application](http://twitter.com/oauth_clients/). Set your application's Callback URL to "http://mysite.com/twitter/return/".


## Installation
Add the 'twitter_app' directory somewhere on your 'PYTHONPATH', put it into 'INSTALLED_APPS' in your settings file.
Fill in your CONSUMER_KEY and CONSUMER_SECRET in your settings file.

- Add this line to your Django project's urlconf: 
    url(r'^twitter/', include('twitter_app.urls')),

You're good to go!

## API Usage
from twitter_auth.util.utils import *


Then with an authenticated user in the request object:
    

    #This gets the authenticated twitter.Api object
    api = get_twitter_api(request)
    users = api.GetFriends()
