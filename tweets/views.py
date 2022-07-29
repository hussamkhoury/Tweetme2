from random import randint
from django.http import HttpResponse, Http404, JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from rest_framework.authentication import SessionAuthentication 
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from .models import Tweet
from .forms import TweetForm
from .serializer import TweetSerializer

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_view(request):
    template = 'home.html'
    context = {}
    return render(request, template, context)

# ----- using rest_fromework ------#
@api_view(['GET'])
# @authentication_classes([SessionAuthentication])  # included in default authentication in settings
@permission_classes([IsAuthenticated])
def home_tweet_detail_view(request, tweet_id):
    """
    Rest API to be Consumed by javascipt
    to get a single tweet.
    """
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    serializer = TweetSerializer(qs.first())
    return Response(serializer.data, status=200)
    
@api_view(['GET'])
# @authentication_classes([SessionAuthentication])  # included in default authentication in settings
@permission_classes([IsAuthenticated])
def home_tweets_list_view(request):
    """
    Rest API to be Consumed bu javascipt
    to get all tweets.
    """
    qs = Tweet.objects.all()
    if not qs.exists():
        return Response({}, status=404)
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
# @authentication_classes([SessionAuthentication])  # included in default authentication in settings
@permission_classes([IsAuthenticated])
def tweet_create_view(request):
    serializer = TweetSerializer(data=request.POST or None)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return JsonResponse(serializer.data, status=201)
    return JsonResponse({}, status=400)    

#------ using pure django ---------#
def tweet_create_view_pure_django(request):
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

def home_tweets_list_view_pure_django(request):
    """
    Rest API to be Consumed by javascipt
    """
    tweets = [tweet.serialize() for tweet in Tweet.objects.all()]
    data = {
        "response" : tweets
    }
    return JsonResponse(data)

def home_tweet_detail_view_pure_django(request, tweet_id):
    """
    Rest API to be Consumed by javascipt
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