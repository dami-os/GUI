# import sqlite3 library so we can create database, tables and do other operations on database
import sqlite3


def create_db_conn_cursor(db_name):
    '''
        Takes db_name as input
        creates a database and returns connection & cusrsor to that db
    '''
    connection = sqlite3.connect(db_name)
    return connection, connection.cursor()


def read_replies(connection, cursor):
    """Given a connection and cursor name
       this will retrieve all the records from tweets table
    """
    cursor.execute("SELECT * FROM replies")
    return cursor.fetchall()


def read_tweets(connection, cursor):
    """Given a connection and cursor name
       this will retrieve all the records from tweets table
    """
    cursor.execute("SELECT * FROM tweets")
    return cursor.fetchall()


def read_keywords(connection, cursor):
    """Given a connection and cursor names
       it reads and return keywords from tweets table"""
    cursor.execute("SELECT keyword FROM tweets")
    return cursor.fetchall()


def read_specific_replies(connection, cursor, keyword):
    "Returns tweets matching with keyword"
    cursor.execute(
        f"SELECT * FROM replies where keyword = \'{keyword}\' Limit 9")
    return cursor.fetchall()


def read_limited_replies(connection, cursor, keyword, limit):
    "Returns limited tweets matching with keyword"
    cursor.execute(
        f"SELECT * FROM replies where keyword = \'{keyword}\' Limit {limit}")
    return cursor.fetchall()


def create_table_tweets(connection, cursor):
    """Takes a cursor as input
       creates a table names Tweets to info
    """
    tb_create = """CREATE TABLE IF NOT EXISTS Tweets(id_str, 
                                                      created_at,
                                                      retweeted, 
                                                      source,
                                                      text,
                                                      user_followers_count,
                                                      user_location,
                                                      keyword, 
                                                      user_screen_name, 
                                                      user_friends_count)"""
    cursor.execute(tb_create)
    connection.commit()


def empty_table(connection, cursor, tbl_name):
    """
        Given a name of table
        It deletes all the records in that table
    """
    deletion_query = f"DELETE FROM {tbl_name}"
    cursor.execute(deletion_query)
    connection.commit()


def create_table_replies(connection, cursor):
    "Creates a new table Replies in database"

    tb_create = """CREATE TABLE IF NOT EXISTS Replies(id_str, 
                                                      created_at,
                                                      source,
                                                      text,
                                                      user_followers_count,
                                                      user_location, 
                                                      user_screen_name, 
                                                      user_friends_count,
                                                      keyword,
                                                      original_id_str,
                                                      FOREIGN KEY (original_id_str) 
                                                        REFERENCES tweets (id_Str) 
                                                        ON DELETE CASCADE 
                                                        ON UPDATE NO ACTION)"""
    cursor.execute(tb_create)
    connection.commit()


def insert_reply_record(connection, cursor, **columns):
    "Takes values and inserts into scraper table"
    insertion_query = '''INSERT INTO replies(id_str, created_at, source, text,
                                             user_followers_count, user_location,
                                             user_screen_name, user_friends_count, keyword, original_id_str)
                                             VALUES (?,?,?,?,?,?,?,?,?,?)'''
    id_str = columns["id_str"]
    created_at = columns["created_at"]
    source = columns["source"]
    text = columns["text"]
    user_followers_count = columns["user_followers_count"]
    user_location = columns["user_location"]
    user_screen_name = columns["user_screen_name"]
    user_friends_count = columns["user_friends_count"]
    keyword = columns["keyword"]
    original_id_str = columns["original_id_str"]
    cursor.execute(insertion_query, (id_str, created_at,
                                     source, text, user_followers_count, user_location,
                                     user_screen_name, user_friends_count, keyword, original_id_str))
    connection.commit()


def insert_tweet_record(connection, cursor, **columns):
    "Takes values and inserts into scraper table"
    insertion_query = '''INSERT INTO Tweets(id_str, created_at, retweeted, source, text,
                                             user_followers_count, user_location, keyword,
                                             user_screen_name, user_friends_count)
                                             VALUES (?,?,?,?,?,?,?,?,?,?)'''
    id_str = columns["id_str"]
    created_at = columns["created_at"]
    retweeted = columns["retweeted"]
    source = columns["source"]
    text = columns["text"]
    user_followers_count = columns["user_followers_count"]
    user_location = columns["user_location"]
    keyword = columns["keyword"]
    user_screen_name = columns["user_screen_name"]
    user_friends_count = columns["user_friends_count"]

    cursor.execute(insertion_query, (id_str, created_at, retweeted,
                                     source, text, user_followers_count, user_location, keyword,
                                     user_screen_name, user_friends_count))
    connection.commit()
