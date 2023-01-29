import tweepy
from textblob import TextBlob
import preprocessor as prep
import statistics
from typing import List
from secrets import consumer_key, consumer_secret, access_key, access_secret
# Authentication:
# auth= tweepy.AppAuthHandler(consumer_key, consumer_secret)
# api = tweepy.API(auth)

api_key = ""
api_key_secret = ""
access_token = ""
access_token_secret = ""

authenticator = tweepy.OAuthHandler(api_key, api_key_secret)
authenticator.set_access_token(access_token, access_token_secret)

api = tweepy.API(authenticator, wait_on_rate_limit=True)

def get_tweets(keyword: str) -> List[str]:
    all_tweets=[]
    for tweet in tweepy.Cursor(api.search_tweets, q=keyword, tweet_mode='extended', lang='en').items(10):
        all_tweets.append(tweet.full_text)
    return all_tweets

def clean_tweets(all_tweets: List[str]) -> List[str]:
    tweets_clean=[]
    for tweet in all_tweets:
        tweets_clean.append(prep.clean(tweet))
    return tweets_clean

def get_sentiment(all_tweets: List[str]) -> List[float]:
    sentiment_scores=[]
    for tweet in all_tweets:
        blob = TextBlob(tweet)
        sentiment_scores.append(blob.sentiment.polarity)
    return sentiment_scores

def generate_average_sentiment_score(keyword: str) -> int:
    tweets = get_tweets(keyword)
    tweets_clean = clean_tweets(tweets)
    sentiment_scores = get_sentiment(tweets_clean)
    average_score = statistics.mean(sentiment_scores)
    return average_score


if __name__ == "__main__":
    print("What does the world prefer?")
    first_thing = input()
    print("...or...")
    second_thing = input()
    print("\n")

    first_score = generate_average_sentiment_score(first_thing)
    second_score = generate_average_sentiment_score(second_thing)   

    if(first_score > second_score):
        print(f"The humanity prefers {first_thing} over {second_thing}")
    else:
        print(f"The humanity prefers {second_thing} over {first_thing}")  

