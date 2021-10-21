## Tweepy & Twitter API Tutorial

A tutorial written for [SociLabs](https://sean-doody.github.io/socilabs/p/tweepy-twitter-tutorial/) demonstrating how to use Python and Tweepy to scrape the Twitter API. The final script is available in the `tweepy_twitter_api.py` file.

**Table of Contents**
- [Introduction](#introduction)
  - [Prerequisites](#prerequisites)
- [Setting up the Environment](#setting-up-the-environment)
  - [Install Packages](#install-packages)
- [Setting Up Tweepy With Your Credentials](#setting-up-tweepy-with-your-credentials)
  - [Connect to the Twitter API](#connect-to-the-twitter-api)
- [Searching Twitter for Data](#searching-twitter-for-data)
  - [The search_tweets Method](#the-search_tweets-method)
  - [Navigating JSON & Dictionaries](#navigating-json--dictionaries)
  - [Paginating Twitter Data](#paginating-twitter-data)
- [A Working Example](#a-working-example)
  - [Refactoring Into a Function](#refactoring-into-a-function)
- [Saving the Data](#saving-the-data)
  - [Saving as JSON](#saving-as-json)
  - [Saving to a CSV](#saving-to-a-csv)
- [Putting it All Together](#putting-it-all-together)
- [Conclusion](#conclusion)

---

## Introduction

This advanced tutorial will go over how to create custom Twitter datasets by collecting data from the official Twitter API. It assumes you have already [installed Python and Anaconda](https://sean-doody.github.io/socilabs/p/install-python/) and are comfortable coding in Python. 

The coding examples contained in this codelab can be implemented in your favorite text editor and run as a standalone Python program, or integrated into an IDE or notebook environment like Jupyter Lab. 

**Note:** This tutorial uses the standard search features of the Twitter API. Users with academic credentials have access to Twitter's historical archive. To learn more about Twitter's academic project track, see both [Twitter's official documentation](https://developer.twitter.com/en/docs/projects/overview#product-track) and [Tweepy's official documentation](https://docs.tweepy.org/en/stable/client.html?highlight=academichttps://docs.tweepy.org/en/stable/client.html?highlight=academic).

### Prerequisites

- Twitter Developer Account
- Twitter API Keys
- Python coding knowledge
- Familiarity with coding loops, dictionary objects, and indexing
- Familiarity with functions

This tutorial will use the following packages and versions:

- Python 3.9
- Tweepy 4.1.0
- Pandas 1.3.4
- Twitter API v1.1

## Setting up the Environment

First, let's create a fresh conda environment to install our packages and dependencies. Open up your terminal
and execute the following command:

```bash
$ > conda create -n twitter-api python=3.9
```

Follow the prompt and type `y` to proceed. Now, activate the environment by executing the following
script:

```bash
$ > conda activate twitter-api
```

Your bash shell or terminal should look something like this:

```bash
(twitter-api) $ >
```

The environment name, in paretheses, indicates that we have successfully activated our environment.
Now we can begin installing our dependencies.

### Install Packages

First, ensure pip is updated:

```bash
(twitter-api) $ > pip install --upgrade pip
```

For this tutorial, we will need to install:
1. Tweepy
2. Pandas
3. NumPy

We can do this easily in one line:

```bash
(twitter-api) $ > pip install --upgrade tweepy pandas numpy
```

## Setting Up Tweepy With Your Credentials

First, let's make sure we import our libraries:

```python
import tweepy
import pandas as pd
import numpy as np
```

In order to access the Twitter API, you **must** provide the API key, the API secret, and the bearer token provided by Twitter at the time you set up your app in the Twitter Developer dashboard. You will also need to generate an **access token** from within the Twitter Developer dashboard after you have created your app. You will need both your **access token** and **access token secret** to access the API.

It is **never** a good idea to hardcode your credentials into your program. Instead, save them in a separate markup file, such as a JSON file, from which they can be read into your script without having to visibly hardcode them.

You can create a document called `keys.json` that contains the following contents:

```json
{
    "api_key": "<copy-and-paste-your-api-key-here>",
    "api_secret": "<copy-and-paste-your-api-secret-key-here>",
    "bearer_token": "<copy-and-paste-your-bearer-token-here>",
    "access_token": "<copy-and-pate-your-access-token-here>",
    "access_secret": "<copy-and-paste-your-access-secret-token-here>"
}
```

Then, we can load our credentials into our Python script using the following code:

```python
import json

# Set the path to your credentials JSON file:
credentials = "<path_to_your_credential_file>.json"
with open(credentials, "r") as keys:
    api_tokens = json.load(keys)

```

Now, instead of hardcoding the keys into our Python app, we can pull them from the JSON file we just loaded. JSON files are treated as [dictionaries](https://realpython.com/python-dicts/) when loaded into  Python, meaning we can index them by their keys to extract data.

To see a list of the keys contained in a dictionary, we can use the `.keys()` method this way: `api_tokens.keys()`. The keys will match exactly the keys from the JSON credentials file.

Let's grab our credentials from the dictionary using key indexing:

```python
# Grab the API keys:
API_KEY = api_tokens["api_key"]
API_SECRET = api_tokens["api_secret"]
BEARER_TOKEN = api_tokens["bearer_token"]
ACCESS_TOKEN = api_tokens["access_token"]
ACCESS_SECRET = api_tokens["access_secret"]
```

### Connect to the Twitter API

We can now connect to the Twitter API using our credentials. We do this by authenticating our app via Tweepy with our keys:

```python

# We use Tweepy's OAuthHandler method to authenticate our credentials:
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)

# Then, we set our access tokens by calling the auth object directly:
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# Finally, we can initialize the Twitter API. 
# NOTE: we will be using this `api` object to interact
# with Twitter from here on out:
api = tweepy.API(auth)
```

We should now be connected to the Twitter API. To verify that our connection works and our credentials have
been appropriately set up, let's just pull some tweets from your home timeline and print their text:

```python
test_tweets = api.home_timeline()

# Looping through the tweets:
for tweet in test_tweets:
    print(tweet.text + "\n")
```

Your console should return the text from a sample of tweets pulled from your timeline. **Note:** these will be specific to your followers.

Now that we're all set up, let's get started!

## Searching Twitter for Data

There are *lots* of ways you can search for data on Twitter. You can: follow and pull data from specific accounts; collect tweets grouped by hashtags; find tweets by keyword search; set custom filters; and so on. What sorts of data you need, and the methods you apply to obtain those data, will vary by each research project's use case.

Here, we will focus on using Tweepy's `search_tweets` method to use keyword queries, which can include hashtags, to search Twitter for tweets.

### The search_tweets Method

Hashtags and keywords are an excellent way to gather topically relevant Twitter data. In this example, we are going to be searcing for tweets related to COVID-19.

First, let's get a sense for how Tweepy handles Twitter searches and returns results. 

Let's pull 10 tweets that match the query `#covid19`. We do this by calling the `search_tweets()` method on our API object, setting a search query, and setting a count:

```python
tweets = api.search_tweets(
    q="#covid19",
    count=10
)
```

In this code snipper, `q` is short for query, which is set equal to `#covid19` in this example. `count` tells Tweepy how many tweets to fetch from the Twitter API. Here, we tell Tweepy to only grab 10 tweets.

Importantly, what is returned is not raw tweet text, but a list of Twitter `Status` objects. We can see this by checking the type of the first tweet—`type(tweet[0])`—which will return `tweepy.models.Status`. We will need to take a closer look at this object in order to iterate through it and pull out the data of interest.

### Navigating JSON & Dictionaries

Status objects are based on the JSON data containing tweet and user info for each object. They can be searched two ways: (a.) by calling methods on the status object where each method is a key in the JSON data dictionary; or (b.) grabbing the raw JSON itself and iterating over it directly.

For example, if we wanted to get the text of the first tweet, we could call the `text` method by
writing `tweets[0].text`. This corresponds to the `text` key in the Twitter JSON data. We can do this for other important parameters like `id`, `created_at` (the date of the tweet), and so on: *any* parameter returned by Twitter.

We can see every key available by iterating over the JSON dictionary and printing the key (the JSON is accessible by calling the `_json` method as illustrated below):

```python
for key in tweets[0]._json.keys():
    print(key)
```

You should see a list like this:

```text
created_at
id
id_str
text
truncated
entities
metadata
source
in_reply_to_status_id
in_reply_to_status_id_str
in_reply_to_user_id
in_reply_to_user_id_str
in_reply_to_screen_name
user
geo
coordinates
place
contributors
retweeted_status
is_quote_status
quoted_status_id
quoted_status_id_str
retweet_count
favorite_count
favorited
retweeted
lang
```

Great! Now we have a list of all the available data returned by Twitter. **However**, some of these keys return more, *nested* JSON. For example, the `user` key returns a nested JSON dictionary containing information about the poster. We must interact with this nested data the same way we interact with the top-level tweet data.

We can get a list of all the keys and the type of data they return with some simple Python code:

```python
for key in tweets[0]._json.keys():
    # We can use a functional string to print the key and its type:
    print(f"{key} :: type {type(tweets[0]._json[key])}")
```

You should see this:

```text
created_at :: type <class 'str'>
id :: type <class 'int'>
id_str :: type <class 'str'>
text :: type <class 'str'>
truncated :: type <class 'bool'>
entities :: type <class 'dict'>
metadata :: type <class 'dict'>
source :: type <class 'str'>
in_reply_to_status_id :: type <class 'NoneType'>
in_reply_to_status_id_str :: type <class 'NoneType'>
in_reply_to_user_id :: type <class 'NoneType'>
in_reply_to_user_id_str :: type <class 'NoneType'>
in_reply_to_screen_name :: type <class 'NoneType'>
user :: type <class 'dict'>
geo :: type <class 'NoneType'>
coordinates :: type <class 'NoneType'>
place :: type <class 'NoneType'>
contributors :: type <class 'NoneType'>
retweeted_status :: type <class 'dict'>
is_quote_status :: type <class 'bool'>
quoted_status_id :: type <class 'int'>
quoted_status_id_str :: type <class 'str'>
retweet_count :: type <class 'int'>
favorite_count :: type <class 'int'>
favorited :: type <class 'bool'>
retweeted :: type <class 'bool'>
lang :: type <class 'str'>
```

Now, we can see the type of data each key is associated with. `str` just means stirng, or text; `int` just means an integer; `bool` just means a value of either `True` or `False`; and `NoneType` just means the data is empty or not applicable and can safely be ignored. 

Importantly, though, notice that some keys contain class `dict`: this means that they are associated with a dictionary, and contain further nested data. Let's use `user` as an example.

To see all of the keys in the `user` data, you can use this code:

```python
for key in tweets[0].user._json.keys():
    print(key)
```

This returns all `user`-level keys:

```text
id
id_str
name
screen_name
location
description
url
entities
protected
followers_count
friends_count
listed_count
created_at
favourites_count
utc_offset
time_zone
geo_enabled
verified
statuses_count
lang
contributors_enabled
is_translator
is_translation_enabled
profile_background_color
profile_background_image_url
profile_background_image_url_https
profile_background_tile
profile_image_url
profile_image_url_https
profile_banner_url
profile_link_color
profile_sidebar_border_color
profile_sidebar_fill_color
profile_text_color
profile_use_background_image
has_extended_profile
default_profile
default_profile_image
following
follow_request_sent
notifications
translator_type
withheld_in_countries
```
Again, to see if there is anymore nested data, you can check the data type returned with each key:

```python
for key in tweets[0].user._json.keys():
    print(f"{key} :: type {type(tweets[0].user._json[key])}")
```

Which returns:

```text
id :: type <class 'int'>
id_str :: type <class 'str'>
name :: type <class 'str'>
screen_name :: type <class 'str'>
location :: type <class 'str'>
description :: type <class 'str'>
url :: type <class 'NoneType'>
entities :: type <class 'dict'>
protected :: type <class 'bool'>
followers_count :: type <class 'int'>
friends_count :: type <class 'int'>
listed_count :: type <class 'int'>
created_at :: type <class 'str'>
favourites_count :: type <class 'int'>
utc_offset :: type <class 'NoneType'>
time_zone :: type <class 'NoneType'>
geo_enabled :: type <class 'bool'>
verified :: type <class 'bool'>
statuses_count :: type <class 'int'>
lang :: type <class 'NoneType'>
contributors_enabled :: type <class 'bool'>
is_translator :: type <class 'bool'>
is_translation_enabled :: type <class 'bool'>
profile_background_color :: type <class 'str'>
profile_background_image_url :: type <class 'str'>
profile_background_image_url_https :: type <class 'str'>
profile_background_tile :: type <class 'bool'>
profile_image_url :: type <class 'str'>
profile_image_url_https :: type <class 'str'>
profile_banner_url :: type <class 'str'>
profile_link_color :: type <class 'str'>
profile_sidebar_border_color :: type <class 'str'>
profile_sidebar_fill_color :: type <class 'str'>
profile_text_color :: type <class 'str'>
profile_use_background_image :: type <class 'bool'>
has_extended_profile :: type <class 'bool'>
default_profile :: type <class 'bool'>
default_profile_image :: type <class 'bool'>
following :: type <class 'bool'>
follow_request_sent :: type <class 'bool'>
notifications :: type <class 'bool'>
translator_type :: type <class 'str'>
withheld_in_countries :: type <class 'list'>
```

It looks like the only further nested data for `user` is `entities`. To learn more about `entities` objects, [check out the official Twitter API documentation](https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/entities).

Familiarizing yourself with these keys and their associated data structure is essential for effectively navigating the Twitter API. Take some time to explore these keys and familiarize yourself with Python dictionary objects if this feels confusing. 

Choosing which data you need is specific to your use case and research project. However, some data is **absolutely necessary** to maintain the integrity of your dataset. Four **absolutely essential** data are:

1. The tweet `id`.
2. The tweet `created_at` UTC timestamp.
3. The tweet `text`.
4. The tweet `author`.
5. The weet `author_id`.

Almost certainly you will want and need more data, including hashtags, user mentions, whether or not a tweet is a retweet, favorite counts, and so on. Familiarizing yourself with the Twitter API, as well as Twitter itself, is absolutely necessary to determining which data you need.

### Paginating Twitter Data

In the simple example given above, we searched Twitter for 10 tweets relevant to the query `#covid19`. When Twitter returns tweets, it does so in batches of JSON. The max size a batch can be is 100, meaning Twitter will only return 100 tweets per batch. In order to return more batches of Tweets, you will need to paginate the Tweets using Tweepy's `Cursor()` method. Luckily, implementing pagination is extremely easy with Tweepy. Do note that you must be attentive to rate limitations on your API calls, which you can [read more about in the Twitter API documentation](https://developer.twitter.com/en/docs/twitter-api/rate-limits).

When searching and paginating Tweets with Tweepy's `Cursor()`, we use the following syntax:

```python
tweets = tweepy.Cursor(api.search_tweets,
                       q="#covid19",
                       count=100).items(500)
```

Using the `Cursor()` method, we instructed Tweepy to fetch 500 (`.items(500)`) total tweets in batches of 100 (`count=100`). In other words, we have 5 pages of Tweets. However, the tweets are not returned directly. Instead, Tweepy creates a [generator object](https://wiki.python.org/moin/Generators) that we have to iterate through to extract each tweet.

To see how this works, let's grab the text of the first 10 tweets:

```python
# Because it's a generator, we need to have a counter:
n_tweets = 0
for tweet in tweets:
    if n_tweets < 10:
        print(tweet.text + "\n")
        n_tweets += 1
    else:
        pass
```

The text of the first 10 tweets contained in the generator will be returned. We can simplify our code a bit by iterating over the generator a bit differently, as shown below:

```python
for tweet in tweepy.Cursor(api.search_tweet, q="#covid19", count=5).items(20):
    print(tweet.text)
```

This simplified syntax prevents us from having to create a seperate variable containing the Tweepy generator. Instead, we just loop through the generator and discard it after we're done. Easy!

Now let's combine these insights to build a full working example that includes aggregating the tweets into a Pandas dataframe and turning the tweets into a functional dataset.

## A Working Example

We're now going to bring these pieces together and add some more specificty (and slightly more coplexity) to our Twitter scrape. 

First, let's prepare the parameters for the `search_tweets()` method in separate variables. This allows us to change the content of the variable without having to manually change the query in our `api` object any time we want to modify our search terms. We will also tell Tweepy how many tweets we want per page and set the page limit. Importantly, we will introduce the parameter `tweet_mode` and set it to `extended` in order to get the full text of a tweet. While Twitter now allows 280 character tweets, by default, the Twitter API truncates tweets to 140 characters. We must override this. Additionally, the `text` parameter we have been using will now change to `full_text`.

```python
# We can use logical search operators in our query text.
# Let's add a series of hashtags with OR, meaning a tweet can
# contain any of the search terms:
query = "#covid19 OR #covid OR #covid-19 OR #coronavirus

# We will also add a new parameter that limits us to English
# results only:
lang = "en"

# Ensure extended is set to true:
tweet_mode = "extended"

# Let's limit ourselves to 100 tweets per page:
count = 100 

# Let's grab only 1000 tweets:
tweet_limit = 1000
```

Now, we can use these variables are parameters in our Tweepy API without needing to hardcode them directly. 

```python
for tweet in tweepy.Cursor(api.search_comments, q=query, lang=lang, tweet_mode=tweet_mode, count=count).items(tweet_limit):
    <...do something...>
```

While we have been simply printing the text of tweets, it is time to actually begin extracing the data we want from each tweet. Tweet data, such as a tweet's text and ID, are not nested and can be easily extracted. However, user-level data is nested in a sub-dictionary, and data like hashtags and user-mentions are nested in sub-dictionaries that themselves contain *further* sub-dictionaries. As mentioned earlier, familiarizing yourself with the JSON structure of the Tweet data and Python's dictionary class is essential. For now, let's see some working examples.

Let's map out the variables of interest At different levels:

- Tweet level:
  - `id`
  - `created_at`
  - `full_text`
  - `hashtags`
  - `user_mentions`
  - `in_reply_to_user_id`
  - `in_reply_to_screen_name`
  - `is_quote_status`
  - Whether or not the tweet is a retweet (and if so, that tweet's identifiers).
  - `retweet_count`
  - `favorite_count`

- User level:
  - The user's `id`
  - The user's `screen_name`
  - The user's `name`
  - `verified` status

Let's see how to access this data by refactoring our code and wrapping everything together into a nice function that takes arguments for the API parameters, iterates through the tweets, and returns a nicely formatted Pandas dataframe.

### Refactoring Into a Function

If you are not familiar with Python functions, consider [taking some time to learn more about them](https://www.learnpython.org/en/Functions). You are also free to follow along. Otherwise, let's get started!

Let's define a Tweet scraping function that takes all of our API parameters of interest as arguments:

```python
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

    # First, let's create a dictionary that will store our tweet data. We
    # are using a dictionary because we can easily generate a Pandas dataframe
    # from the dictionary keys.
    #
    # The dictionary will be formatted so that its keys are parameters associated with
    # each tweet and its values are lists to which we will append results for each tweet:

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
        """
        We need to start with user level variables, meaning we are going to iterate
        through the user dictionary. We can do this easily! Then, we are going to
        append the data to the list in our data dictionary. Let's see how it's
        done:
        """

        # User ID:
        data["user_id"].append(tweet.user.id)
        # Screen name:
        data["screen_name"].append(tweet.user.screen_name)
        # Name:
        data["name"].append(tweet.user.name)
        # verified status:
        data["verified"].append(tweet.user.verified)

        """
        Great! Now let's grab the tweet level data:
        """

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
        
        # NOTE: to get hashtags & user mentions, we need to iterate through
        # the entities sub dictionary. Then, we need to iterate through
        # the hashtag sub dictionary. It sounds bad, but it's not! 
        # We will save the hashtags to a list and append the list
        # to our data dictionary:

        hashtags = []
        # Try to get hashtags; if there is an error, then there are no hashtags
        # and we can pass:
        try:
            for hashtag in tweet.entities["hashtags"]:
                hashtags.append(hashtag["text"])
        except Exception:
            pass
        
        # Now append the hashtag list to our dataset! If there are no
        # hashtags, just set it equal to NaN:
        if len(hashtags) == 0:
            data["hashtags"].append(np.nan)
        else:
            data["hashtags"].append(hashtags)

        # We do the same thing for user mentions:
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

        # We need to check if a tweet is a retweet ourselves. We can do this by checking
        # if the retweeted_status key is present in the JSON:
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
            # Set is_retweet to false and all other values to np.nan:
            data["is_retweet"].append(False)
            data["retweet_og_id"].append(np.nan)
            data["retweet_og_author_id"].append(np.nan)
            data["retweet_og_author_screen_name"].append(np.nan)
            data["retweet_og_author_name"].append(np.nan)
            data["retweet_og_date"].append(np.nan)
            data["retweet_og_full_text"].append(np.nan)
            data["retweet_og_retweet_count"].append(np.nan)
            data["retweet_og_favorite_count"].append(np.nan)
    
    # Whoo! That's a lot of code. Now, let's turn our data dictionary into a Pandas dataframe
    # and then return it:

    df = pd.DataFrame(data)

    # Now send it out:
    return df

```

We made it! Let's call the function and save our data. We can preset our function arguments as separate variables, which will allow us to override default function values if we like, and then pass them into the function itself:

```python

# Set the function parameters:
query = "#covid19 OR #covid OR #covid-19 OR #coronavirus
lang = "en"
tweet_mode = "extended"
count = 100 
tweet_limit = 1000

# Call the function using our parameters:
df = tweet_scraper(query=query, lang=lang, tweet_mode=tweet_mode, count=count, tweet_limit=tweet_limit)
```
Awesome! We now have our Tweet data in a structured, tabular, dataframe. Let's inspect our data by calling Pandas's `head()` method. This method allows you to the see the top `N` samples in your dataframe. By default, this is set to 5, but we can override ths by passing an argument into the parentheses. Let's look at the top 10 posts:

```python
df.head(10)
```

You should see a result like this:

|      |    user_id | screen_name   | name              | verified |                  id | ... |
| ---: | ---------: | :------------ | :---------------- | :------- | ------------------: | --- |
|    0 |   45823110 | jude5456      | Jude 🇪🇺 💙🌹         | False    | 1450854059968184336 | ... |
|    1 | 4904619394 | Suzyistdaheim | 𝕊𝕦𝕫𝕪™ 😷💉💉🏠🍀       | False    | 1450854059963977731 | ... |
|    2 |  138468171 | captainpt     | Peter Schultz     | False    | 1450854058856751106 | ... |
|    3 | 2253036106 | CRCrangelc    | Clodovaldo Rangel | False    | 1450854058407956480 | ... |
|    4 | 3082370998 | BeckyRae12345 | Becca             | False    | 1450854058009534464 | ... |
|  ... |        ... | ...           | ...               | ...      |                 ... | ... |

I have truncated the columns and rows. In total, we have 23 columns of data. You can see this for yourself simply by printing the length of the `.columns` attribute of the Pandas dataframe:

```python
print(f"There are {len(df.columns)} columns")
```
Which returns:

```text
There are 23 columns
```

You can also see all the columns in the dataframe by printing them:

```python
for column in df.columns:
    print(columns)
```

Which should produce:

```text
user_id
screen_name
name
verified
id
created_at
full_text
retweet_count
favorite_count
hashtags
user_mentions
in_reply_to_user_id
in_reply_to_screen_name
is_quote_status
is_retweet
retweet_og_id
retweet_og_author_id
retweet_og_author_screen_name
retweet_og_author_name
retweet_og_date
retweet_og_full_text
retweet_og_retweet_count
retweet_og_favorite_count
```

Excellent! Now, we can move on to saving our data.

## Saving the Data

Pandas makes saving dataframes as local files extremely easy. I strongly advise that we save our dataframe in JSON format because our dataframe contains columns populated by lists. Specifically, the `hashtags` and `user_mentions` columns both contain lists of hashtags and mentioned users, respectively. JSON natively supports lists. If we save the dataframe as a CSV file, these lists will be converted to plaintext strings. We **do not** want this.

There is a workaround, however: we can turn the lists into strings using Python's `join()` method, and then re-split the strings into lists again as needed. We illustrate how to do this below.

### Saving as JSON

To save as JSON without changing the list variabels, simply call the `to_json()` method:

```python
df.to_json("twitter_data.json")
```
And we're done! You can name your datafile whatever you like. 

When you're ready to load your json file again, we call the `read_json()` method and save it to a variable:

```python
df = pd.read_json("twitter_data.json")
```

Voila! The data is back. 

### Saving to a CSV

If you insist on saving your data in CSV format, you need to deal with the lists in the `hashtags` and `user_mentions` columns. To do this, we are going to create a function that converts the list to a string, where each list item is separated by a comma (`,`). In the future, if we want to convert the columns back to a list, we can simply split on the comma. 

Let's see how this works:

```python
# Let's create a function that cleans up the lists:
def list_cleaner(list_object):
    """
    This function takes one argument: list_object, which is list.
    """

    # Let's try to join the list. Note that we nest the join in a Try/Except
    # pattern. This is because not all Tweets contain either hashtags or user mentions.
    # In this case, they simply have a NaN missing value. This will throw an error if 
    # not dealt with:

    try:
        output = ",".join(list_object)
    except Exception:
        output = list_object
    
    return output
```

Now we can use Pandas's `apply()` method to map the function to the columns and fix the lists. We do this by calling `apply()` on the column of interest and passing our function, *wihout parentheses*, as an argument:

```python
# Fix hashtags list:
df["hashtags"] = df["hashtags"].apply(list_cleaner)

# Fix mentions list:
df["user_mentions"] = df["user_mentions"].apply(list_cleaner)
```

Awesome! Our lists are now strings and can safely be saved as CSV. This is a simple one-liner:

```python
df.to_csv("twitter_data.csv")
```

And if we wanted to load the CSV file when we're ready:

```python
df = pd.read_csv("twitter_data.csv")
```

To re-split the data back into a list after re-loading the CSV, we can write on more simple helper function:

```python
def split_into_list(text):
    # We need exception handling again for missing values:
    try:
        # Remember: we joined on a comma, so let's split on a comma:
        output = text.split(",")
    except Exception:
        output = text
    
    return output
```

And then apply it to our columns again:

```python
# Split hashtags back into a list:
df["hashtags"] = df["hashtags"].apply(split_into_list)

# Split mentions back into list:
df["user_mentions"] = df["user_mentions"].apply(split_into_list)
```

Fantastic! Our hashtags and user mentions are back into a list.

## Putting it All Together

Here's what the final, combined, script will look like in a single Python file:

```python
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
```

That's it! A complete Twitter scraping program.

## Conclusion

This tutorial covered how to build custom Twitter datasets using the Tweepy package in Python and the Twitter API. We covered a lot of ground and dug in to some complex coding examples. This is just the tip of the iceberg: there is so much more to cover! I strongly recommend you [check out the official Tweepy documentation](https://docs.tweepy.org/en/stable/) to familiarize yourself the ins and outs of the package. 

Also, make sure you spend time reading through the official [Twitter API documentation](https://developer.twitter.com/en/docs/twitter-api/v1) to learn all the nuances of Twitter's developer platform. Going directly to the source is usually the best course of action!

Future tutorial series will look at different ways to analyze Twitter data. For now, though, thank you for reading this tutorial. Feel free to reach out if you have any questions.

Happy coding! 