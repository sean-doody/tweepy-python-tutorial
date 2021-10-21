# Author: Sean Doody
# Email: sdoody@gmu.edu
# License: MIT

import json
import tweepy
import numpy as np
import pandas as pd

# Load credentials:
credentials = "keys.json"
with open(credentials, "r") as keys:
    api_tokens = json.load(keys)

# Grab the API keys:
API_KEY = api_tokens["api_key"]
API_SECRET = api_tokens["api_secret"]
BEARER_TOKEN = api_tokens["bearer_token"]
ACCESS_TOKEN = api_tokens["access_token"]
ACCESS_SECRET = api_tokens["access_secret"]

# Connect to the Twitter API:
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# Set the function parameters:
query = "#covid19 OR #covid OR #covid-19 OR #coronavirus
lang = "en"
tweet_mode = "extended"
count = 100 
tweet_limit = 1000

# Define the scraping function:
def tweet_scraper(query=None, lang="en", tweet_mode="extended", count=100, tweet_limit=1000):
    """
    This function takes Tweepy search_tweets parameters as arguments and returns a Pandas
    dataframe containing tweet data.

    :param query: a keyword search phrase (string)
    :param lang: limit results by language (default: English)
    :param tweet_mode: choose whether to extend tweets to full 280 characters.
    :param count: the number of tweets to return per page (default: 100; max: 100)
    :param tweet_limit: the maximum number of tweets to return (default: 1000).
    """

    # Data dictionary for collecting results:
    data = {
        "user_id": [], 
        "screen_name": [],
        "name": [],
        "verified": [],
        "id": [],
        "created_at": [],
        "full_text": [],
        "retweet_count": [],
        "favorite_count": [],
        "hashtags": [],
        "user_mentions": [],
        "in_reply_to_user_id": [],
        "in_reply_to_screen_name": [],
        "is_quote_status": [],
        "is_retweet": [], # we will have to build this parameter ourselves; see below
        "retweet_og_id": [], # the ID of the original retweeted tweet
        "retweet_og_author_id": [], # the original author ID of a retweeted tweet
        "retweet_og_author_screen_name": [], # the original author screen name of a retweeted tweet
        "retweet_og_author_name": [], # the original author's name of a retweeted tweet
        "retweet_og_date": [], # the date of the original tweet
        "retweet_og_full_text": [], # OG full text of the retweet
        "retweet_og_retweet_count": [], # OG retweet count
        "retweet_og_favorite_count": [] # OG favorite count
    }

    # Search the tweets as we've already done, but this time, plug in the paremeter values
    # from the function arguments:

    for tweet in tweepy.Cursor(api.search_tweets, q=query, tweet_mode=tweet_mode, count=count).items(tweet_limit):
        # User ID:
        data["user_id"].append(tweet.user.id)
        # Screen name:
        data["screen_name"].append(tweet.user.screen_name)
        # Name:
        data["name"].append(tweet.user.name)
        # verified status:
        data["verified"].append(tweet.user.verified)

        # Tweet ID:
        data["id"].append(tweet.id)
        # Date:
        data["created_at"].append(tweet.created_at)
        # Full text of tweet:
        data["full_text"].append(tweet.full_text)
        # Get retweet count:
        data["retweet_count"].append(tweet.retweet_count)
        # Get favorite count:
        data["favorite_count"].append(tweet.favorite_count)
        
        # Get hashtags:
        hashtags = []
        try:
            for hashtag in tweet.entities["hashtags"]:
                hashtags.append(hashtag["text"])
        except Exception:
            pass
        
        if len(hashtags) == 0:
            data["hashtags"].append(np.nan)
        else:
            data["hashtags"].append(hashtags)

        # Get user mentions:
        mentions = []
        try:
            for mention in tweet.entities["user_mentions"]:
                mentions.append(mention["screen_name"])
        except Exception:
            pass
        
        if len(mentions) == 0:
            data["user_mentions"].append(np.nan)
        else:
            data["user_mentions"].append(mentions)

        # In reply to user id:
        data["in_reply_to_user_id"].append(tweet.in_reply_to_user_id)
        # In reply to user screen name:
        data["in_reply_to_screen_name"].append(tweet.in_reply_to_screen_name)
        # Check if quote status:
        data["is_quote_status"].append(tweet.is_quote_status)

        # Check retweeted status:
        if "retweeted_status" in tweet._json.keys():
            # Then it is a retweet:
            data["is_retweet"].append(True)
            # Get OG tweet id:
            data["retweet_og_id"].append(tweet.retweeted_status.id)
            # Get OG author ID:
            data["retweet_og_author_id"].append(tweet.retweeted_status.user.id)
            # Get OG author screen name:
            data["retweet_og_author_screen_name"].append(tweet.retweeted_status.user.screen_name)
            # Get OG author name:
            data["retweet_og_author_name"].append(tweet.retweeted_status.user.name)
            # Get date of OG tweet:
            data["retweet_og_date"].append(tweet.retweeted_status.created_at)
            # Get OG full text:
            data["retweet_og_full_text"].append(tweet.retweeted_status.full_text)
            # Get OG retweet count:
            data["retweet_og_retweet_count"].append(tweet.retweeted_status.retweet_count)
            # Get OG favorite count:
            data["retweet_og_favorite_count"].append(tweet.retweeted_status.favorite_count)
        else:
            data["is_retweet"].append(False)
            data["retweet_og_id"].append(np.nan)
            data["retweet_og_author_id"].append(np.nan)
            data["retweet_og_author_screen_name"].append(np.nan)
            data["retweet_og_author_name"].append(np.nan)
            data["retweet_og_date"].append(np.nan)
            data["retweet_og_full_text"].append(np.nan)
            data["retweet_og_retweet_count"].append(np.nan)
            data["retweet_og_favorite_count"].append(np.nan)

    # Save to Pandas dataframe:
    df = pd.DataFrame(data)

    return df


# Call the function and save results:
df = tweet_scraper(query=query, lang=lang, tweet_mode=tweet_mode, count=count, tweet_limit=tweet_limit)

# Save our results:
df.to_json("twitter_data".json")