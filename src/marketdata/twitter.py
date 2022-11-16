import os
import tweepy


# get the twiiter secrets
TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_APIKEY')
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

# Create the auth credentials

auth = tweepy.OAuth1UserHandler(
    TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
)

api = tweepy.API(auth)

# get public tweets
public_tweets = api.home_timeline()

for tweet in public_tweets:
    print(tweet.text)
