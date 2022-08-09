"""tweetme2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from tweets.views import (
    home_view, 
    home_tweets_list_view, 
    home_tweet_detail_view,
    tweet_create_view,
    tweet_delete_view,
    tweet_action_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home_view, name='home_view'), # main page
    path('tweets/', home_tweets_list_view, name='home_tweets_list_view'), # API to load dynamic content into main page(/home)
    path('home/<int:tweet_id>', home_tweet_detail_view, name='home_tweet_detail'), # view tweets details by tweet Id
    path('create-tweet/', tweet_create_view, name='tweet_create'), # create new tweets
    path('api/tweet/<int:tweet_id>/delete', tweet_delete_view, name='tweet_delete'), # view tweets details by tweet Id
    path('api/tweet/action', tweet_action_view)
]
