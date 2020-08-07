import tweepy
from Database import *
import csv

# Authentication with twitter API
auth = tweepy.OAuthHandler("nqdW3F4y1NyCF2ouHNvK9r1cv",
                           "nWuVcOGkYUQGCDbZgRQcVssAmjT5NTkDvCo1UVftsY8AkToXcr")
auth.set_access_token("918437553803546624-5ptWbHIz8ZQw6W3cLemOokyqHWsorAR",
                      "Jg30ap2WlnjcNyKfokYqKDgL1w3Yg3Kd4npZSPpUdfOw9")
# Creating an API
api = tweepy.API(auth)

# Create a Database connection and cursor so we can read all replies from database
connection, cursor = create_db_conn_cursor("twitter.db")

# All the keywords and response from csv file will be stored in response and keywords list
responses = []
keywords = []
# Read replies and keywords from csv file and save it in corresponding variables
with open('keyword_response.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        keywords.append(row[0].lower())
        responses.append(row[1])

# read replies from table and iterate over them one by one
counter = 1
for reply in read_replies(connection, cursor):
    if counter == 10:
        break
    # 1st column of replies table it will be used to post a reply
    reply_id = int(reply[0])
    # corresponding keyword of that reply
    keyword = reply[-2].lower()
    # username from replies table it will be used to mention him/her in our response
    username = reply[-4]
    # below two lines are to get appropriate response from response list based on keyword value
    response_index = keywords.index(keyword)
    response = responses[response_index]
    # update status
    api.update_status("@" + username + " " + response,
                      in_reply_to_status_id=reply_id)
    counter += 1
