from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from .models import Tweet

User = get_user_model()

class TweetTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user_one', password='simplepassword')
        self.other_user = User.objects.create_user(username='user_other', password='simplepasswordother')
        Tweet.objects.create(content='first Tweet', user=self.user)
        Tweet.objects.create(content='seond Tweet', user=self.user)
        Tweet.objects.create(content='third Tweet', user=self.other_user)
        self.current_tweets_count = Tweet.objects.all().count()    
        
    def test_user_created(self):
        tweet_object = Tweet.objects.create(content='Test 1: Create Tweet', user=self.user)
        self.assertEqual(tweet_object.user, self.user)
        self.assertEqual(tweet_object.content, 'Test 1: Create Tweet')

    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='simplepassword') 
        return client
    
    def test_tweets_list(self):
        client = self.get_client()
        response = client.get('/api/tweets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_action_like(self):
        client = self.get_client()
        response = client.post('/api/tweets/action/', {"id":1, "action":"like"})
        self.assertEqual(response.status_code, 200)
        likes_count = response.json().get("likes")
        self.assertEqual(likes_count, 1)

    def test_action_unlike(self):
        #login
        client = self.get_client()
        
        # do like
        response = client.post('/api/tweets/action/', {"id":2, "action":"like"})
        self.assertEqual(response.status_code, 200)
        
        # do unlike
        response = client.post('/api/tweets/action/', {"id":2, "action":"unlike"})
        self.assertEqual(response.status_code, 200)
        
        likes_count = response.json().get("likes")
        self.assertEqual(likes_count, 0)

    def test_action_retweet(self):
        client = self.get_client()
        response = client.post('/api/tweets/action/', {"id":3, "action":"retweet"})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertNotEqual(data.get("id"), 3)
        self.assertEqual(self.current_tweets_count + 1, 4)
        
    def test_tweet_create_api_view(self):
        client = self.get_client()
        request_data = {"content": "Test for createing tweet"}
        response = client.post('/api/tweets/create/', request_data)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_tweet_id = data.get("id")
        self.assertEqual(self.current_tweets_count + 1, new_tweet_id)

    def test_tweet_details_api_view(self):
        client = self.get_client()
        response = client.get('/api/tweets/1/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        _id = data.get("id")
        self.assertEqual(_id, 1)

    def test_tweet_delete_api(self):
        client = self.get_client()
        response = client.delete('/api/tweets/1/delete/')
        self.assertEqual(response.status_code, 200)

        response_incorrect_owner = client.delete('/api/tweets/3/delete/')
        self.assertEqual(response_incorrect_owner.status_code, 403)