from django.conf.urls.defaults import *

from twitter_auth.views.views import *

urlpatterns = patterns('twitter_app.views',
   url(r'^$',
        view=main,
        name='twitter_oauth_main'),

    url(r'^login/$',
        view=login_,
        name='twitter_oauth_login'),

    url(r'^return/$',
        view=return_,
        name='twitter_oauth_return'),

    url(r'^list/$',
        view=friend_list,
        name='twitter_oauth_friend_list'),

   url(r'^logout/$',
        view=logout_,
        name='twitter_oauth_logout'),
)
