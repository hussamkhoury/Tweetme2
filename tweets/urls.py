from django.urls import path

from .views import (
    home_tweets_list_view, 
    home_tweet_detail_view,
    tweet_create_view,
    tweet_delete_view,
    tweet_action_view
)
'''
CLIENT 
ENDPOINT api/tweets/
'''
urlpatterns = [
    path('', home_tweets_list_view, name='home_tweets_list_view'), # API to load dynamic content into main page(/home)
    path('action/', tweet_action_view),
    path('create/', tweet_create_view, name='tweet_create'), # create new tweets
    path('<int:tweet_id>/', home_tweet_detail_view, name='home_tweet_detail'), # view tweets details by tweet Id
    path('<int:tweet_id>/delete/', tweet_delete_view, name='tweet_delete') # view tweets details by tweet Id
]
