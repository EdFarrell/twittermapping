import json
import tweepy
from tweepy import OAuthHandler

# These are the credentials needed to make requests using the Twitter API. These
# are considered you API keys
# To obtain your own credentials, you need to register an app with Twitter at apps.twitter.com
consumer_key = 'Z1fB6taapkl02oxrldaGwvuyX'
consumer_secret = 'HBjIckV80PMPr1kDyQWzV2r9lZG8K7o1V3d4i041v7ixMCl3oE'
access_token = '3912791837-MI0oWsfNOEplAbrv3S0kTmiRxsxTzXOpapGuPDG'
access_secret = 'wCLsJegdtnzt4DPO1yeNEV48h4pTS57bx3qgUDY86vl1K'

# Use OAuth to set your access token.
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

# Create the tweepy api object. Use the access token as input.
api = tweepy.API(auth)

# Create a search term to query the Twitter Search API
query = "%23appgis"     # the %23 stands for #.

# Ask twitter to give us the first tweet that uses the #appgis hashtag
tweets = api.search(q=query, count=2)
# how many records where returned? Should be 1
print len(tweets)
# inpect the tweets object to see what it is.
print type(tweets)
# <class 'tweepy.models.SearchResults'> This is a special tweepy object called SearchResults. You can iterate through this object.

# Using the json module will make the response more readable. Print the first item in the tweets SearchResult object.
print(json.dumps(tweets[1]._json, indent=2, sort_keys=True))

# If you had many tweets that you wanted to process, you can iterate through the tweets object
for tweet in tweets:
    print 'Status object:', tweet  # This is a Status object that contains all of the information posted in the tweet
    print 'Status text: ', tweet.text  # The text of the tweet
    print 'Status geo: ', tweet.geo  # The precise location of the tweet, if provided. If not, None
    print 'Status place: ', tweet.place # The place location of the tweet, if provided.
    print 'Status place coords: ', tweet.place.bounding_box.coordinates

# Lets turn our tweet into a dictionary so that we can work with it using pure Python
tweet_dict = tweets[0]._json
print type(tweet_dict)
print tweet_dict['text']





