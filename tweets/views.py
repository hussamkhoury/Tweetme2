from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render

from .models import Tweet

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

def home_tweets_list_view(request):
    tweets = [{ "id" : tweet.id, "content" : tweet.content} for tweet in Tweet.objects.all()]
    data = {
        "response" : tweets
    }
    template = 'home.html'
    return render(request, template, data, status=200)