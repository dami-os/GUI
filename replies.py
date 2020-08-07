# Import libraries
import tweepy
import json
from Database import *
from datetime import date
# Get Database Connection
connection, cursor = create_db_conn_cursor("twitter.db")

# Authentication with twitter API
auth = tweepy.OAuthHandler("nqdW3F4y1NyCF2ouHNvK9r1cv",
                           "nWuVcOGkYUQGCDbZgRQcVssAmjT5NTkDvCo1UVftsY8AkToXcr")
auth.set_access_token("918437553803546624-5ptWbHIz8ZQw6W3cLemOokyqHWsorAR",
                      "Jg30ap2WlnjcNyKfokYqKDgL1w3Yg3Kd4npZSPpUdfOw9")
# Creating an API
api = tweepy.API(auth)
# Get Current Date
# To be used in Displaying todays tweets with replies
today = str(date.today())

# This loop is reading all the tweets from database and gets replies for each tweet
for tweet in read_tweets(connection, cursor):
    # get id of original tweet. it will be compared to check if a tweet is reply to this tweet
    original_id_str = tweet[0]
    # Name of perosn who tweeted
    name = tweet[-2]
    # Keyword this tweet belongs to
    keyword = tweet[-3]
    # Actual text of tweet
    tweet_text = tweet[4]
    # Formatting output to be readable
    print("__________________________________________________________________________________________________")
    print(
        f"______________________{today}_{keyword}_tweet_replies____________________________________________")
    print("__________________________________________________________________________________________________")
    print("Twitter Handle, Tweet")
    # print name of person and his tweet
    print(f"{name}, {tweet_text}")
    print("__________________________________________________________________________________________________")
    print("____________________________________Replies_______________________________________________________")
    # Search for replies
    for reply in tweepy.Cursor(api.search, q='to:'+name, result_type='recent', timeout=999999).items(1000):
        # it checks if this tweet is reply to other tweet
        if hasattr(reply, 'in_reply_to_status_id_str'):
            # check if this tweet is reply to our desired tweet
            if (reply.in_reply_to_status_id_str == original_id_str):
                # Unpack desired values from reply tweet to store in database
                id_str = reply.id_str
                created_at = reply.created_at
                source = reply.source
                text = reply.text
                text.encode("utf-8")
                user_followers_count = reply.user.followers_count
                user_location = reply.user.location
                user_screen_name = reply.user.screen_name
                user_screen_name.encode("utf-8")
                user_friends_count = reply.user.friends_count
                # save record in database
                insert_reply_record(connection, cursor, id_str=id_str, created_at=created_at, source=source, text=text,                                        user_followers_count=user_followers_count, user_location=user_location,
                                    user_screen_name=user_screen_name, user_friends_count=user_friends_count, keyword=keyword,
                                    original_id_str=original_id_str)
                # print reply with replier name
                print(
                    "__________________________________________________________________________________________________")
                print("Replier Name, Reply")
                print(f"{user_screen_name}, {text}")
                print(
                    "__________________________________________________________________________________________________")
    print()
    print()
    print()
    print()
