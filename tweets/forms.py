from django.conf import settings

from django import forms
from .models import Tweet

MAX_TWEET_LENGHT = settings.MAX_TWEET_LENGHT
class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > MAX_TWEET_LENGHT:
            raise forms.ValidationError("The Tweet is too long!")
        return content