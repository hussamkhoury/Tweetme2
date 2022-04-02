from random import randint
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render

from .models import Tweet
from .forms import TweetForm

def home_view(request):
    template = 'home.html'
    context = {}
    return render(request, template, context)

def home_tweets_list_view(request):
    """
    Rest API to be Consumed bu javascipt
    """
    tweets = [{ "id" : tweet.id, "content" : tweet.content, "likes": randint(0,100)} for tweet in Tweet.objects.all()]
    print(tweets)
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
    form = TweetForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        form = TweetForm()
    template = 'components/form.html'
    context = {'form': form}
    return render(request, template, context)
