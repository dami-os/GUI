# import all the libraries
import tweepy
import json
from Database import *
import argparse
from datetime import date

# This code is defining the arguments which we can send from command line
# for example we can specify keyword 1 using -k1 shortcut
ap = argparse.ArgumentParser()
ap.add_argument("-k1", "--keyword 1", required=True,
                help="first keyword to use")
ap.add_argument("-k2", "--keyword 2", required=True,
                help="2nd keyword to use search tweets on twitter")
ap.add_argument("-k3", "--keyword 3", required=True,
                help="3rd keyword to use search tweets on twitter")
ap.add_argument("-k4", "--keyword 4", required=True,
                help="4th keyword to use search tweets on twitter")
ap.add_argument("-k5", "--keyword 5", required=True,
                help="5th keyword to use search tweets on twitter")
ap.add_argument("-k6", "--keyword 6", required=True,
                help="6th keyword to use search tweets on twitter")
ap.add_argument("-k7", "--keyword 7", required=True,
                help="7th keyword to use search tweets on twitter")
ap.add_argument("-k8", "--keyword 8", required=True,
                help="8th keyword to use search tweets on twitter")
ap.add_argument("-k9", "--keyword 9", required=True,
                help="9th keyword to use search tweets on twitter")
ap.add_argument("-k10", "--keyword 10", required=True,
                help="10th keyword to use search tweets on twitter")


# https://pythonprogramming.net/twitter-api-streaming-tweets-python-tutorial/
# To view tweets in database format, install DB Browser for SQLite

# 1. Authentification
auth = tweepy.OAuthHandler("nqdW3F4y1NyCF2ouHNvK9r1cv",
                           "nWuVcOGkYUQGCDbZgRQcVssAmjT5NTkDvCo1UVftsY8AkToXcr")
auth.set_access_token("918437553803546624-5ptWbHIz8ZQw6W3cLemOokyqHWsorAR",
                      "Jg30ap2WlnjcNyKfokYqKDgL1w3Yg3Kd4npZSPpUdfOw9")
# Creating an API
api = tweepy.API(auth)

# We want to crawl through specific information about the tweets and the users
# without exposing the users real names.
connection, cursor = create_db_conn_cursor("twitter.db")
# Creating Tables Tweets and replies
create_table_tweets(connection, cursor)
create_table_replies(connection, cursor)
# Deleting all the records from tables tweet and replies
empty_table(connection, cursor, "tweets")
empty_table(connection, cursor, "replies")


# class WebScraper(tweepy.StreamListener):

#     def on_status(self, status):
#         print(status)

#     def on_error(self, status_code):
#         print(status_code)
# # Parsing the day so that we can break down the text into meaningful chunks of data that can
# # then be analysed.

#     def on_data(self, data):
#         all_data = json.loads(data)
#         id_str = all_data['id_str']
#         created_at = all_data['created_at']
#         retweeted = all_data['retweeted']
#         source = all_data['source']
#         text = all_data['text']
#         user_followers_count = all_data['user']['followers_count']
#         user_location = all_data['user']['location']
#         user_screen_name = all_data['user']['screen_name']
#         user_friends_count = all_data['user']['friends_count']
#         # insert record
#         insert_tweet_record(connection, cursor, id_str=id_str, created_at=created_at, retweeted=retweeted, source=source,  text=text,
#                             user_followers_count=user_followers_count, user_location=user_location, user_screen_name=user_screen_name,
#                             user_friends_count=user_friends_count)


# 4. Print
# We can select the key words to that we enter in twitter to view specific tweet topics
#stream_listener = WebScraper()
#stream = tweepy.Stream(auth=api.auth, listener=stream_listener)

# keywords = vars(ap.parse_args())
# for keyword in keywords:
#     print(keywords[keyword])
#     stream.filter(track=[keywords[keyword]], languages=['en'])

# This code receives data of a tweet in json variable and unpacks desired values from it and stores in database
def on_data(data, keyword):
    all_data = json.loads(data)
    # unpacking desired data from json variable
    id_str = all_data['id_str']
    created_at = all_data['created_at']
    retweeted = all_data['retweeted']
    source = all_data['source']
    text = all_data['text']
    user_followers_count = all_data['user']['followers_count']
    user_location = all_data['user']['location']
    user_screen_name = all_data['user']['screen_name']
    user_friends_count = all_data['user']['friends_count']
    # insert record in database tweets table
    insert_tweet_record(connection, cursor, id_str=id_str, created_at=created_at, retweeted=retweeted, source=source,  text=text,
                        user_followers_count=user_followers_count, user_location=user_location, keyword=keyword,
                        user_screen_name=user_screen_name, user_friends_count=user_friends_count)


# Receiving all the keywords from command line in keywords variable
keywords = vars(ap.parse_args())
# Getting current date converting it in to text format
# this will be used to search tweet about keywords not earlier then today
date_since = str(date.today())
for keyword in keywords:
    # takes 1 keyword out of 8 at a time
    # we also making a filter to exclude retweets
    new_search = keywords[keyword] + " -filter:retweets"
    # Search popular tweets
    tweets = tweepy.Cursor(api.search,
                           q=new_search,
                           result_type="popular",
                           lang="en",
                           since=date_since).items(1)
    # This code is dynamic so you can get 1 or more then one tweets on a keyword
    for tweet in tweets:
        # Gets _json value of a tweet
        json_data = json.dumps(tweet._json)
        # on_data is responsible to unpack desired values
        # and stores it in database
        on_data(json_data, keywords[keyword])
