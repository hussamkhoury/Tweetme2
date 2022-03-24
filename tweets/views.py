from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render

from .models import Tweet
def home_detail_view(request, tweet_id):
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
