from tkinter import *
import tweepy
import json
from Database import *
from datetime import date
from tkinter import messagebox
from tkinter.ttk import Progressbar
from tkinter import ttk
from PIL import ImageTk, Image

# Get database connection & cursor
connection, cursor = create_db_conn_cursor("twitter.db")
# authenticate with twitter api using our credentials
auth = tweepy.OAuthHandler("nqdW3F4y1NyCF2ouHNvK9r1cv",
                           "nWuVcOGkYUQGCDbZgRQcVssAmjT5NTkDvCo1UVftsY8AkToXcr")
auth.set_access_token("918437553803546624-5ptWbHIz8ZQw6W3cLemOokyqHWsorAR",
                      "Jg30ap2WlnjcNyKfokYqKDgL1w3Yg3Kd4npZSPpUdfOw9")
# Creating an API instance
api = tweepy.API(auth, wait_on_rate_limit=True)

# global variables needed at different places for the sake of GUI manipulation or decision making based on their values
main_frame = None
replies_frame = None
selected_keyword = None

# entry point of program


def main():
    global main_frame
    # create main window and set icon on top left corner of window as twitter image
    root = Tk()
    root.iconbitmap("gui_assets/twitter.ico")
    # set title of window
    root.title("Twitter bot")
    # set the size of main window and position fromwhere it should appear on screen
    root.geometry("1240x720+100+50")
    # set background color to white
    root.configure(bg='#ffffff')

    # define left menu frame
    menu_frame = Frame(root, highlightbackground="#00acee", highlightcolor="#00acee", bg="#ffffff",
                       highlightthickness=8, bd=0, relief="solid")
    menu_frame.pack(side=LEFT, fill=Y, padx=5, pady=10)
    # put buttons inside menu frame
    # create new database button
    new_database = Button(menu_frame, text="1. New Database", font=(
        "bold", 20), relief=RAISED, anchor=W, padx=2, command=new_db,  width="14")
    new_database.pack(padx=8, pady=4)
    new_database.config(highlightbackground="#24A0ED")
    # Create Get tweets button to get popular tweet on any keyword
    tweets_button = Button(menu_frame, text="2. Get Tweets", font=(
        "bold", 20), relief=RAISED, anchor=W, padx=2, width="14", command=lambda: reset_input(main_frame))
    tweets_button.pack(padx=8, pady=4)
    tweets_button.config(highlightbackground="#24A0ED")
    # Create Get Repliess button to get replies to popular tweets
    replies_button = Button(menu_frame, text="3. Get Replies", font=("bold", 20), relief=RAISED, anchor=W, padx=2,
                            width="14", command=get_replies)
    replies_button.pack(padx=8, pady=4)
    replies_button.config(highlightbackground="#24A0ED")
    # Display Relies buttons
    display_replies_btn = Button(menu_frame, text="4. Show Replies", font=("bold", 20),  relief=RAISED, anchor=W, padx=2,
                                 command=show_replies, width="14")
    display_replies_btn.pack(padx=8, pady=4)
    display_replies_btn.config(highlightbackground="#24A0ED")
    # Create Respond button to respond to replies of popular tweets
    response_button = Button(menu_frame, text="5. Respond", font=("bold", 20),  relief=RAISED, anchor=W, padx=2,
                             width="14", command=respond_replies)
    response_button.pack(padx=8, pady=4)
    response_button.config(highlightbackground="#24A0ED")

    # define instruction button
    instruction_button = Button(menu_frame, text="Instructions", font=("bold", 20),
                                relief=RAISED, anchor=W, padx=2,
                                command=lambda: instruction(root, False), width="14",)
    instruction_button.pack(padx=8, pady=4)
    instruction_button.config(highlightbackground="#24A0ED")

    # define input form frame for scraping popular tweets against keywords
    #input_form(root, True)
    instruction(root, True)
    # let the gui run an infinite loop to listen for events
    root.mainloop()

# This method is responsible for displaying instruction on how to use gui


def instruction(parent, need_border):
    global main_frame
    if need_border:
        main_frame = Frame(parent, highlightbackground="#00acee", highlightcolor="#00acee",
                           highlightthickness=8, bd=0, relief="solid", bg="#ffffff")
        main_frame.pack(fill=BOTH, padx=5, pady=10)
    else:
        clearwin(main_frame)

    title_label = Label(main_frame, text="Instructions to Run this Application", font=("Helvetica bold", 32),
                        bg="#00acee", fg="#ffffff")
    title_label.pack(fill=X, padx=10, pady=10)
    instruction_frame = Frame(main_frame, bd=0, padx=5, pady=5, bg="#ffffff")
    instruction_frame.pack(fill=BOTH, padx=10, pady=10)
    instruct1_label = Label(instruction_frame, anchor=W, bg="#ffffff", text="1. Click on the New Database to run GUI APP for first time", font=("Helvetica bold", 14),
                            fg="#00acee")
    instruct1_label.pack(fill=X, padx=10, pady=10)
    instruct2_label = Label(instruction_frame, anchor=W, bg="#ffffff", text="2. Type 10 keywords to get the top ten most popular tweets that relate to that specific keyword", font=("Helvetica bold", 14),
                            fg="#00acee")
    instruct2_label.pack(fill=X, padx=10, pady=10)
    instruct3_label = Label(instruction_frame, anchor=W, bg="#ffffff", text="3. Click Get Replies button. This will get all the replies for the popular tweets", font=("Helvetica bold", 14),
                            fg="#00acee")
    instruct3_label.pack(fill=X, padx=10, pady=10)
    instruct4_label = Label(instruction_frame, anchor=W, bg="#ffffff", text="4. NOTE: This will take sometime as i manipulated search api to get replies. Twitter api don't return replies. There will be loading sign/interrupt sign so you will have to wait a few minutes",
                            font=("Helvetica bold", 14),
                            fg="#00acee")
    instruct4_label.pack(fill=X, padx=10, pady=10)
    instruct5_label = Label(instruction_frame, anchor=W, bg="#ffffff", text="5. Once all the replies have been gathered it wil refresh to a replies page. You can check replies for any keyword", font=("Helvetica bold", 14),
                            fg="#00acee")
    instruct5_label.pack(fill=X, padx=10, pady=10)
    instruct6_label = Label(instruction_frame, anchor=W, bg="#ffffff", text="6. Now click on Respond button to respond to replies of any popular keyword", font=("Helvetica bold", 14),
                            fg="#00acee")
    instruct6_label.pack(fill=X, padx=10, pady=10)
    instruct7_label = Label(instruction_frame, anchor=W, bg="#ffffff", text="7. Fill form and clcik on respond button", font=("Helvetica bold", 14),
                            fg="#00acee")
    instruct7_label.pack(fill=X, padx=10, pady=10)
    instruct7_label = Label(instruction_frame, anchor=W, bg="#ffffff", text="8. To get 10 popular tweets for new keywords click on New database it will delete all records in Database", font=("Helvetica bold", 14),
                            fg="#00acee")
    instruct7_label.pack(fill=X, padx=10, pady=10)
    instruct8_label = Label(instruction_frame, anchor=W, bg="#ffffff", text="9. Do not click another button when an operation is in progress otherwise the system may get really slow", font=("Helvetica bold", 14),
                            fg="#00acee")
    instruct8_label.pack(fill=X, padx=10, pady=10)

# Show replies of popular tweets


def show_replies():
    # use global variables to manipulate gui as well as for retrieving records from database
    global main_frame
    global replies_frame
    global selected_keyword
    # this will hold value user selects from drop down
    selected_keyword = StringVar()
    # read all the keywords from database. we have replies for these keywords in database
    keywords = read_keywords(connection, cursor)
    keywords_list = [keyword[0] for keyword in keywords]
    # delete previous window elements so we can have replies record window
    clearwin(main_frame)
    # Top title on window
    title_label = Label(main_frame, text="Replies to Popular Tweets", font=("Helvetica bold", 32),
                        bg="#00acee", fg="#ffffff")
    title_label.pack(fill=X, padx=10, pady=5)
    # define keyword input frame to hold keyword drop down
    keyword_input_frame = Frame(main_frame, bd=0, padx=5, pady=5, bg="#ffffff")
    keyword_input_frame.pack(fill=X, padx=10, pady=3)
    # keywords_list.insert(0, "Select Keyword")
    slct_label = Label(keyword_input_frame, text="Choose Keyword", padx=3, pady=3,
                       font=("Helvetica bold", 20), bg="#ffffff", fg="#00acee")
    slct_label.grid(row=0, column=0, padx=5, pady=3)
    kwd_combo = ttk.Combobox(keyword_input_frame, font=("Times bold", 18), width=20,
                             values=keywords_list, textvariable=selected_keyword)
    kwd_combo.grid(row=0, column=1, padx=5, pady=5)
    kwd_combo.bind("<<ComboboxSelected>>", populate_replies)
    # define keyword input frame
    replies_frame = Frame(main_frame, bd=0, padx=5, pady=2, bg="#ffffff")
    replies_frame.pack(fill=BOTH, padx=10, pady=10)


# This function gets called whenever user select a keyword from drop down and populates window with  corresponding replies
def populate_replies(event):
    global replies_frame
    # clears replies section window so that replies for new selected keyword can be displayed
    clearwin(replies_frame)
    global selected_keyword
    # read 20 tweets from database
    tweets = read_limited_replies(
        connection, cursor, selected_keyword.get(), 20)
    # go through tweets and insert them in window
    for index, tweet in enumerate(tweets, start=0):
        row_ = index
        col = 0
        if index >= 10:
            row_ -= 10
            col = 2
        reply_lbl = Label(replies_frame, text="Reply "+str(index+1), padx=1, pady=1,
                          font=("Helvetica bold", 10), bg="#ffffff", fg="#00acee")
        reply_lbl.grid(row=row_, column=col, padx=2, pady=3, sticky=W)
        reply_text = Text(replies_frame, width=55, height=3, padx=3,
                          pady=3, font=("Times", 9), wrap=WORD)
        reply_text.grid(row=row_, column=col+1, padx=2, pady=3)
        reply_text.insert(END, tweet[3])
        reply_text.config(highlightbackground="#00acee")
# Respond to Replies of popular tweets


def respond_replies():

    global main_frame
    # to hold user choice of which keyword user choosen to respond
    selected_keyword = StringVar()
    # clear existing window so we can make
    clearwin(main_frame)
    # Now select available keywords with tweets from database
    keywords = read_keywords(connection, cursor)
    keywords_list = [keyword[0] for keyword in keywords]
    # keywords_list.insert(0, "Select Keyword")
    slct_label = Label(main_frame, text="Choose Keyword", padx=3, pady=3,
                       font=("Helvetica bold", 20), bg="#ffffff", fg="#00acee")
    slct_label.grid(row=0, column=0, padx=5, pady=5)
    kwd_combo = ttk.Combobox(main_frame, font=("Times bold", 18), width=20,
                             values=keywords_list, textvariable=selected_keyword)
    kwd_combo.current(0)
    kwd_combo.grid(row=0, column=1, padx=5, pady=5)
    # Replies input form frame
    input_form_frame = Frame(main_frame, bd=0, padx=2, pady=5, bg="#ffffff")
    input_form_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

    # Specify first response
    lbl_reply1 = Label(input_form_frame, text="Reply 1", padx=3, pady=3,
                       font=("Helvetica bold", 15), bg="#ffffff", fg="#00acee")
    lbl_reply1.grid(row=0, column=0, padx=5, pady=4, sticky=W)
    reply_text1 = Text(input_form_frame, width=55, height=3, padx=3, highlightthickness=2,
                       pady=3, font=("Times", 10), wrap=WORD)
    reply_text1.grid(row=0, column=1, padx=3, pady=4, columnspan=2)
    reply_text1.config(highlightbackground="#24A0ED")
    # Specify second response
    lbl_reply2 = Label(input_form_frame, text="Reply 2", padx=3, pady=3,
                       font=("Helvetica bold", 15), bg="#ffffff", fg="#00acee")
    lbl_reply2.grid(row=1, column=0, padx=5, pady=4, sticky=W)
    reply_text2 = Text(input_form_frame, width=55, height=3, padx=3, highlightthickness=2,
                       pady=3, font=("Times", 10), wrap=WORD)
    reply_text2.grid(row=1, column=1, padx=3, pady=4, columnspan=2)
    reply_text2.config(highlightbackground="#24A0ED")
    # Specify 3rd response
    lbl_reply3 = Label(input_form_frame, text="Reply 3", padx=3, pady=3,
                       font=("Helvetica bold", 15), bg="#ffffff", fg="#00acee")
    lbl_reply3.grid(row=2, column=0, padx=5, pady=4, sticky=W)
    reply_text3 = Text(input_form_frame, width=55, height=3, padx=3, highlightthickness=2,
                       pady=3, font=("Times", 10), wrap=WORD)
    reply_text3.grid(row=2, column=1, padx=3, pady=4, columnspan=2)
    reply_text3.config(highlightbackground="#24A0ED")
    # Specify 4th response
    lbl_reply4 = Label(input_form_frame, text="Reply 4", padx=3, pady=3,
                       font=("Helvetica bold", 15), bg="#ffffff", fg="#00acee")
    lbl_reply4.grid(row=3, column=0, padx=5, pady=4, sticky=W)
    reply_text4 = Text(input_form_frame, width=55, height=3, padx=3, highlightthickness=2,
                       pady=3, font=("Times", 10), wrap=WORD)
    reply_text4.grid(row=3, column=1, padx=3, pady=4, columnspan=2)
    reply_text4.config(highlightbackground="#24A0ED")
    # Specify 5th response
    lbl_reply5 = Label(input_form_frame, text="Reply 5", padx=3, pady=3,
                       font=("Helvetica bold", 15), bg="#ffffff", fg="#00acee")
    lbl_reply5.grid(row=4, column=0, padx=5, pady=4, sticky=W)
    reply_text5 = Text(input_form_frame, width=55, height=3, padx=3, highlightthickness=2,
                       pady=3, font=("Times", 10), wrap=WORD)
    reply_text5.grid(row=4, column=1, padx=3, pady=4, columnspan=2)
    reply_text5.config(highlightbackground="#24A0ED")
    # Specify 6th response
    lbl_reply6 = Label(input_form_frame, text="Reply 6", padx=3, pady=3,
                       font=("Helvetica bold", 15), bg="#ffffff", fg="#00acee")
    lbl_reply6.grid(row=5, column=0, padx=5, pady=4, sticky=W)
    reply_text6 = Text(input_form_frame, width=55, height=3, padx=3,
                       pady=3, font=("Times", 10), wrap=WORD, highlightthickness=2)
    reply_text6.grid(row=5, column=1, padx=3, pady=4, columnspan=2)
    reply_text6.config(highlightbackground="#24A0ED")
    # Specify 7th response
    lbl_reply7 = Label(input_form_frame, text="Reply 7", padx=3, pady=3,
                       font=("Helvetica bold", 15), bg="#ffffff", fg="#00acee")
    lbl_reply7.grid(row=6, column=0, padx=5, pady=4, sticky=W)
    reply_text7 = Text(input_form_frame, width=55, height=3, padx=3, highlightthickness=2,
                       pady=3, font=("Times", 10), wrap=WORD)
    reply_text7.grid(row=6, column=1, padx=3, pady=4, columnspan=2)
    reply_text7.config(highlightbackground="#24A0ED")
    # Specify 8th response
    lbl_reply8 = Label(input_form_frame, text="Reply 8", padx=3, pady=3,
                       font=("Helvetica bold", 15), bg="#ffffff", fg="#00acee")
    lbl_reply8.grid(row=7, column=0, padx=5, pady=4, sticky=W)
    reply_text8 = Text(input_form_frame, width=55, height=3, padx=3,
                       pady=3, font=("Times", 10), wrap=WORD, highlightthickness=2)
    reply_text8.grid(row=7, column=1, padx=3, pady=4, columnspan=2)
    reply_text8.config(highlightbackground="#24A0ED")
    # Specify 9th response
    lbl_reply9 = Label(input_form_frame, text="Reply 9", padx=3, pady=3,
                       font=("Helvetica bold", 15), bg="#ffffff", fg="#00acee")
    lbl_reply9.grid(row=8, column=0, padx=5, pady=4, sticky=W)
    reply_text9 = Text(input_form_frame, width=55, height=3, padx=3, highlightthickness=2,
                       pady=3, font=("Times", 10), wrap=WORD)

    reply_text9.grid(row=8, column=1, padx=3, pady=4, columnspan=2)
    reply_text9.config(highlightbackground="#24A0ED")
    # Define Reset and Respond button. reset button deletes all responses user typed
    # respond button will respond with user specified replies
    reset_button = Button(input_form_frame, text="Reset",
                          padx=2, pady=8, width=10, font=("Helvetica bold", 14),
                          command=lambda: reset_response(reply_text1, reply_text2, reply_text3, reply_text4, reply_text5,
                                                         reply_text6, reply_text7, reply_text8, reply_text9))
    reset_button.grid(row=9, column=1, padx=3, pady=4, sticky=E)
    respond_button = Button(input_form_frame, text="Respond",
                            command=lambda: respond_to_replies(selected_keyword.get(), reply_text1.get("1.0"), reply_text2.get(
                                "1.0"), reply_text3.get("1.0"),
                                reply_text4.get(
                                "1.0"), reply_text5.get("1.0"),
                                reply_text6.get("1.0"), reply_text7.get("1.0"), reply_text8.get("1.0"), reply_text9.get("1.0")),
                            padx=2, pady=8, width=10, font=("Helvetica bold", 14))
    respond_button.grid(row=9, column=2, padx=3, pady=4, sticky=W)
    reset_button.config(highlightbackground="#00acee")
    respond_button.config(highlightbackground="#00acee")

# This method respond to 9 replies of selected keyword with response user provides


def respond_to_replies(keyword, *responses):
    for response in responses:
        if response.strip() == "":
            messagebox.showerror(
                title="Empty Fields Error", message="All Responses are Required")
            return

    # Read 9 relies from database related too selected keyword
    replies = read_specific_replies(connection, cursor, keyword)
    index = 0
    # go through replies one by one and respond them
    for reply in replies:

        # 1st column of replies table it will be used to post a reply
        reply_id = int(reply[0])
        # corresponding keyword of that reply
        keyword = reply[-2].lower()
        # username from replies table it will be used to mention him/her in our response
        username = reply[-4]
        # update status
        api.update_status("@" + username + " " + responses[index].strip(),
                          in_reply_to_status_id=reply_id)
        index += 1
    # redirect user to success window to tell them respond operation successfull
    success_window("Succesfully Responded to Replies of Popular Tweets")


# This function is responsible for scraping replies to popular tweets
def get_replies():

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
        for reply in tweepy.Cursor(api.search, q='to:'+name, result_type='recent', timeout=999999).items(150):
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
    # redirect them to success window with success message
    success_window("Succesfully Scraped Replies to Popular Tweets")


# This method resets input form to original when we come back from other forms (e.g. response form) back to tweets form
def reset_input(parent):
    global main_frame
    clearwin(main_frame)
    input_form(parent, False)

# this method populates a form with 10 keywords user can specify to scrape most popular tweets


def input_form(parent, need_border):
    global main_frame
    # define popular tweets input keywords form
    # create main frame to hold title and input form frame
    if need_border:
        main_frame = Frame(parent, highlightbackground="#00acee", highlightcolor="#00acee",
                           highlightthickness=8, bd=0, relief="solid", bg="#ffffff")
        main_frame.pack(fill=BOTH, padx=5, pady=10)

    title_label = Label(main_frame, text="Get Popular Tweets", font=("Helvetica bold", 32),
                        bg="#00acee", fg="#ffffff")
    title_label.pack(fill=X, padx=10, pady=10)
    # define input form frame
    input_form_frame = Frame(main_frame, bd=0, padx=5, pady=5, bg="#ffffff")
    input_form_frame.pack(fill=BOTH, padx=10, pady=10)
    # Define input fields and labels for each keyword

    # input field for 1st keyword
    kw1_label = Label(input_form_frame, text="Keyword 1", padx=3, pady=3,
                      font=("Helvetica bold", 20), bg="#ffffff", fg="#00acee")
    kw1_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
    kw1_entry = Entry(input_form_frame, font=("Helvetica bold", 14), width=30)
    kw1_entry.grid(row=0, column=1, padx=5, pady=5, columnspan=3)
    kw1_entry.config(highlightbackground="#24A0ED")
    # input field for 2nd keyword
    kw2_label = Label(input_form_frame, text="Keyword 2", padx=3, pady=3,
                      font=("Helvetica bold", 20), bg="#ffffff", fg="#00acee")
    kw2_label.grid(row=1, column=0, padx=5, pady=5, sticky=W)
    kw2_entry = Entry(input_form_frame, font=("Helvetica bold", 14), width=30)
    kw2_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=3)
    kw2_entry.config(highlightbackground="#24A0ED")
    # input field for 3rd keyword
    kw3_label = Label(input_form_frame, text="Keyword 3", padx=3, pady=3,
                      font=("Helvetica bold", 20), bg="#ffffff", fg="#00acee")
    kw3_label.grid(row=2, column=0, padx=5, pady=5, sticky=W)
    kw3_entry = Entry(input_form_frame, font=("Helvetica bold", 14), width=30)
    kw3_entry.grid(row=2, column=1, padx=5, pady=5, columnspan=3)
    kw3_entry.config(highlightbackground="#24A0ED")
    # input field for 4th keyword
    kw4_label = Label(input_form_frame, text="Keyword 4",
                      padx=3, pady=3, font=("Helvetica bold", 20), bg="#ffffff", fg="#00acee")
    kw4_label.grid(row=3, column=0, padx=5, pady=5, sticky=W)
    kw4_entry = Entry(input_form_frame, font=("Helvetica bold", 14), width=30)
    kw4_entry.grid(row=3, column=1, padx=5, pady=5, columnspan=3)
    kw4_entry.config(highlightbackground="#24A0ED")
    # input field for 5th keyword
    kw5_label = Label(input_form_frame, text="Keyword 5", padx=3, pady=3,
                      font=("Helvetica bold", 20), bg="#ffffff", fg="#00acee")
    kw5_label.grid(row=4, column=0, padx=5, pady=5, sticky=W)
    kw5_entry = Entry(input_form_frame, font=("Helvetica bold", 14), width=30)
    kw5_entry.grid(row=4, column=1, padx=5, pady=5, columnspan=3)
    kw5_entry.config(highlightbackground="#24A0ED")
    # input field for 6th keyword
    kw6_label = Label(input_form_frame, text="Keyword 6", padx=3, pady=3,
                      font=("Helvetica bold", 20), bg="#ffffff", fg="#00acee")
    kw6_label.grid(row=5, column=0, padx=5, pady=5, sticky=W)
    kw6_entry = Entry(input_form_frame, font=("Helvetica bold", 14), width=30)
    kw6_entry.grid(row=5, column=1, padx=5, pady=5, columnspan=3)
    kw6_entry.config(highlightbackground="#24A0ED")
    # input field for 7th keyword
    kw7_label = Label(input_form_frame, text="Keyword 7", padx=3, pady=3,
                      font=("Helvetica bold", 20), bg="#ffffff", fg="#00acee")
    kw7_label.grid(row=6, column=0, padx=5, pady=5, sticky=W)
    kw7_entry = Entry(input_form_frame, font=("Helvetica bold", 14), width=30)
    kw7_entry.grid(row=6, column=1, padx=5, pady=5, columnspan=3)
    kw7_entry.config(highlightbackground="#24A0ED")
    # input field for 8th keyword
    kw8_label = Label(input_form_frame, text="Keyword 8", padx=3, pady=3,
                      font=("Helvetica bold", 20), bg="#ffffff", fg="#00acee")
    kw8_label.grid(row=7, column=0, padx=5, pady=5, sticky=W)
    kw8_entry = Entry(input_form_frame, font=("Helvetica bold", 14), width=30)
    kw8_entry.grid(row=7, column=1, padx=5, pady=5, columnspan=3)
    kw8_entry.config(highlightbackground="#24A0ED")
    # input field for 9th keyword
    kw9_label = Label(input_form_frame, text="Keyword 9", padx=3, pady=3,
                      font=("Helvetica bold", 20), bg="#ffffff", fg="#00acee")
    kw9_label.grid(row=8, column=0, padx=5, pady=5, sticky=W)
    kw9_entry = Entry(input_form_frame, font=("Helvetica bold", 14), width=30)
    kw9_entry.grid(row=8, column=1, padx=5, pady=5, columnspan=3)
    kw9_entry.config(highlightbackground="#24A0ED")
    # input field for 10th keyword
    kw10_label = Label(input_form_frame, text="Keyword 10", padx=3, pady=3,
                       font=("Helvetica bold", 20), bg="#ffffff", fg="#00acee")
    kw10_label.grid(row=9, column=0, padx=5, pady=5, sticky=W)
    kw10_entry = Entry(input_form_frame, font=("Helvetica bold", 14), width=30)
    kw10_entry.grid(row=9, column=1, padx=5, pady=5, columnspan=3)
    kw10_entry.config(highlightbackground="#24A0ED")
    # Define Reset and Get tweet button. get tweet hits api to get 10 popular tweets about keyword. reset button resets form contents
    reset_button = Button(input_form_frame, text="Reset",
                          padx=2, pady=8, width=13, font=("Helvetica bold", 14),
                          command=lambda: reset(kw1_entry, kw2_entry, kw3_entry, kw4_entry, kw5_entry, kw6_entry, kw7_entry, kw8_entry,
                                                kw9_entry, kw10_entry))
    reset_button.grid(row=10, column=2, padx=3, pady=3)
    tweet_button = Button(input_form_frame, text="Get Tweet", command=lambda: get_Tweets(kw1_entry,
                                                                                         kw2_entry, kw3_entry, kw4_entry, kw5_entry, kw6_entry, kw7_entry, kw8_entry, kw9_entry, kw10_entry), padx=2, pady=8, width=13, font=("Helvetica bold", 14))
    tweet_button.grid(row=10, column=3, padx=3, pady=3)
    reset_button.config(highlightbackground="#24A0ED")
    tweet_button.config(highlightbackground="#24A0ED")
# This will create a new database for the first time. if database already exist it will make tables empty (restore operation)


def new_db():
    # Creating Tables Tweets and replies
    create_table_tweets(connection, cursor)
    create_table_replies(connection, cursor)
    # Deleting all the records from tables tweet and replies
    empty_table(connection, cursor, "tweets")
    empty_table(connection, cursor, "replies")
    messagebox.showinfo("Database Refresh Notification",
                        "New Database has been created...")

# Show popular tweets for each keyword in GUI


def display_tweets(parent):
    main_frame = parent
    title_label = Label(main_frame, text="Most Popular Tweets", font=("Helvetica bold", 32),
                        bg="#00acee", fg="#ffffff")
    title_label.pack(fill=X, padx=10, pady=10)
    # define tweets frame
    tweets_frame = Frame(main_frame, bd=0, padx=3, pady=3, bg="#ffffff")
    tweets_frame.pack(fill=BOTH, padx=10, pady=10)
    # Define desired column labels
    keyword_label = Label(tweets_frame, text="Keyword", font=(
        "Helvetica bold", 13), bg="#00acee", fg="#ffffff", width=10)
    keyword_label.grid(row=0, column=0)
    name_label = Label(tweets_frame, text="User Name", font=(
        "Helvetica bold", 13), bg="#00acee", fg="#ffffff", width=10)
    name_label.grid(row=0, column=1, padx=5, pady=5)
    location_label = Label(tweets_frame, text="Location", font=(
        "Helvetica bold", 13), bg="#00acee", fg="#ffffff", width=10)
    location_label.grid(row=0, column=2, padx=5, pady=5)
    followers_label = Label(tweets_frame, text="Followers", font=(
        "Helvetica bold", 13), bg="#00acee", fg="#ffffff", width=10)
    followers_label.grid(row=0, column=3, padx=5, pady=5)
    tweet_label = Label(tweets_frame, text="Tweet", font=(
        "Helvetica bold", 13), bg="#00acee", fg="#ffffff", width=15)
    tweet_label.grid(row=0, column=4, padx=5, pady=5)

    # Now display popular tweets for each keyword
    row_counter = 1
    for tweet in read_tweets(connection, cursor):
        try:
            kw_val_lbl = Label(tweets_frame, text=tweet[-3], font=(
                "Helvetica bold", 12), bg="#ffffff", width=10)
            kw_val_lbl.grid(row=row_counter, column=0, padx=3, pady=6)
            name_val_lbl = Label(tweets_frame, text=tweet[-3], font=(
                "Helvetica bold", 12), bg="#ffffff", width=10)
            name_val_lbl.grid(row=row_counter, column=1, padx=3, pady=6)
            location_val_lbl = Label(tweets_frame, text=tweet[6], font=(
                "Helvetica bold", 12), bg="#ffffff", width=20)
            location_val_lbl.grid(row=row_counter, column=2, padx=3, pady=6)
            followers_val_lbl = Label(tweets_frame, text=tweet[5], font=(
                "Helvetica bold", 12), bg="#ffffff", width=10)
            followers_val_lbl.grid(row=row_counter, column=3, padx=3, pady=6)
            # tweet_val_btn = Button(tweets_frame, text=" Read Tweet", font=(
            #     "Helvetica bold", 14), bg="#00acee", fg="#ffffff", width=15, relief=RAISED, command=lambda: show_tweet(tweet[4]))
            # tweet_val_btn.grid(row=row_counter, column=4, padx=5, pady=6)
            tweet_val_text = Text(tweets_frame, width=55, height=3, padx=3,
                                  pady=3, font=("Times", 10), wrap=WORD)
            tweet_val_text.grid(row=row_counter, column=4,
                                padx=3, pady=4)
            tweet_val_text.insert(END, tweet[4])
            tweet_val_text.config(highlightbackground="#00ACEE")
        except:
            messagebox.showerror("Tweet rendering Error",
                                 "An error occured while rendering tweet")
        finally:
            row_counter += 1

# this method gets called when reset button is clicked. it resets everything


def clearwin(parent):
    main_frame = parent
    for child in main_frame.winfo_children():
        child.destroy()


# Reset response input form
def reset_response(*entries):
    for entry in entries:
        entry.delete("1.0", "end")

# resets tweets form


def reset(*entries):
    for entry in entries:
        entry.delete(0, END)

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

# This function gets called when you click on get tweets and stores most popular tweet for each keyword in database


def get_Tweets(*entries):

    global main_frame
    date_since = str(date.today())
    for entry in entries:
        if entry.get() == "":
            messagebox.showerror(
                title="Empty Fields Error", message="All Keywords are Required")
            return

    # Get tweets for each keyword
    for entry in entries:
        # takes 1 keyword out of 10 at a time
        # we also making a filter to exclude retweets
        new_search = entry.get().strip() + " -filter:retweets"
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
            on_data(json_data, entry.get().strip())

    clearwin(main_frame)
    display_tweets(main_frame)

# Display success message to user when bot finishes any task


def success_window(message):
    global main_frame
    clearwin(main_frame)
    title_label = Label(main_frame, text=message, font=("Helvetica bold", 25),
                        bg="#00acee", fg="#ffffff")
    title_label.pack(fill=X, padx=10, pady=10)

    # Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
    img = ImageTk.PhotoImage(Image.open("gui_assets/progress.png"))

    # The Label widget is a standard Tkinter widget used to display a text or image on the screen.
    panel = Label(main_frame, image=img, width=700, height=700, bg="#ffffff")
    panel.image = img
    # The Pack geometry manager packs widgets in rows or columns.
    panel.pack()


# Starting execution point
if __name__ == "__main__":
    main()
