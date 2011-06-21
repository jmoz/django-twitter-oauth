import oauth, time, datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from twitter_auth.util.utils import *

def main(request):
    if request.session.has_key('access_token'):
        return HttpResponseRedirect(reverse('twitter_oauth_friend_list'))
    else:
        return render_to_response('twitter_auth/base.html')

def logout_(request):
    logout(request)
    request.session.clear()
    return HttpResponseRedirect(reverse('twitter_oauth_main'))

def login_(request):
    "/auth/"
    token = get_unauthorised_request_token()
    auth_url = get_authorisation_url(token)
    response = HttpResponseRedirect(auth_url)
    request.session['unauthed_token'] = token.to_string()
    return response

def return_(request):
    "/return/"
    unauthed_token = request.session.get('unauthed_token', None)
    if not unauthed_token:
        return HttpResponse("No un-authed token cookie")

    token = get_oauth_token_from_string(unauthed_token)
    if token.key != request.GET.get('oauth_token', 'no-token'):
        return HttpResponse("Something went wrong! Tokens do not match")
    verifier = request.GET.get('oauth_verifier')
    access_token = exchange_request_token_for_access_token(token, params={'oauth_verifier':verifier})
    user = authenticate(oauth_access_token=access_token)
    if user is not None:
        login(request, user)
    else:
        return HttpResponse("Something went wrong! Could not log you in") 
    response = HttpResponseRedirect(reverse('twitter_oauth_friend_list'))
    return response

def friend_list(request):
    api = get_twitter_api(request)
    users = api.GetFriends()
    return render_to_response('twitter_auth/list.html', {'users': users})
