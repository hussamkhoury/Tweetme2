from random import randint
from django.http import HttpResponse, Http404, JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .models import Tweet
from .forms import TweetForm

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_view(request):
    template = 'home.html'
    context = {}
    return render(request, template, context)

def home_tweets_list_view(request):
    """
    Rest API to be Consumed bu javascipt
    """
    tweets = [tweet.serialize() for tweet in Tweet.objects.all()]
    data = {
        "response" : tweets
    }
    return JsonResponse(data)

def home_tweet_detail_view(request, tweet_id):
    """
    Rest API to be Consumed bu javascipt
    """
    data = {
        "id" : tweet_id 
    }
    status = 200
    try:
        tweet = Tweet.objects.get(id=tweet_id)
        data['content'] = tweet.content
    except:
        data['message'] = 'Tweet Not Found'
        status = 404
        # raise Http404
    return JsonResponse(data, status=status)

def tweet_create_view(request):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status= 401) # 401 -> not authenticated
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next")
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
        obj.save()
        form = TweetForm()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201) # 201 == created Items
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS): # if not allowed host will redirect to the form action url
            return redirect(next_url)
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status = 400)
    template = 'components/form.html'
    context = {'form': form}
    return render(request, template, context)
