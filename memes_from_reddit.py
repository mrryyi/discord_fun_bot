import praw
import os
import random

already_sent_memes = []

subreddits = ["196", "societylounge","dankmemes","memes","okpolarncp","whenthe"]

reddit = praw.Reddit(
    client_id=os.getenv('CLIENTID'),
    client_secret=os.getenv('CLIENTSECRET'),
    user_agent=os.getenv('USERAGENT')
)

def is_not_reddit_video(url):
    return "//v." not in url 

def get_meme_message():

        fresh = False
        while not fresh:
            subreddit = random.choice(subreddits)
            meme_submissions = reddit.subreddit(subreddit).hot()
            post_to_pick = random.randint(1,25)
            for i in range(0, post_to_pick):
                submission = next(x for x in meme_submissions if not x.stickied and is_not_reddit_video(x.url))
            if submission.url not in already_sent_memes:
                fresh = True
        
        already_sent_memes.append(submission.url)
        

        return "Titel: " + submission.title + "\n" + "Subreddit: " + subreddit + "\n\n" + submission.url