# written by Sean Chow
# www.chowsean.com
# sentiment.py

import tweepy
from textblob import TextBlob
import sys

# helper function to read words from text file
def read_words(words_file):
    return [word for line in open(words_file, 'r') for word in line.split()]

#Authenticate
consumer_key= 'consumer_key'
consumer_secret= 'consumer_secret'

access_token='access_token'
access_token_secret='access_token_secret'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

if (len(sys.argv) < 3):
    print("incorrect usage, python sentiment.py 'query' 'maxtweets'")
    exit(1)

# vars
negative_counter = 0
positive_counter = 0
neutral_counter = 0
non_english = 0
query = sys.argv[1];
max_tweets = int(sys.argv[2]);
public_tweets = list()

if (max_tweets < 100):
    count = max_tweets
else:
    count = 100

# search by handle or by search term
if ("@" in query):
    while (count <= max_tweets):
        public_tweets.extend(api.user_timeline(screen_name = query,count=count))
        count += 100
else:
    while (count <= max_tweets):
        public_tweets.extend(api.search(q = query,count=count))
        count += 100

# put the most common english words into a list
common_words = read_words("commonwords.txt")

for tweet in public_tweets:
    if any(word in tweet.text for word in common_words):
        analysis = TextBlob(tweet.text)
        attributes = vars(analysis.sentiment)
        if (attributes['polarity'] < 0):
            negative_counter += 1
        elif (attributes['polarity'] > 0):
            positive_counter += 1
        else:
            neutral_counter += 1
    else:
        non_english +=1

# ===== summary =====
print("Results for " + str(max_tweets) + " tweets including: " + query)
print("")
print("Positive Tweets: " + str(positive_counter))
print("Negative Tweets: " + str(negative_counter))
print("Neutral Tweets: " + str(neutral_counter))
print("Non-English Tweets: " + str(non_english))
