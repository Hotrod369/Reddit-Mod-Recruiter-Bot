"""
This module contains functions for recommending potential moderators on Reddit
based on their activity in specific subreddits.
"""
# pylint: disable=invalid-name
#!/usr/bin/python

import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
import praw
import prawcore
import prawcore.exceptions
import datetime as dt
import time
import sys
import logging

# Set up logging
logging.basicConfig(
    filename="reddit_scraper.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s",
)

# Create a Reddit instance using PRAW
reddit = praw.Reddit(
    client_id="your_client_id",
    client_secret="your_client_secret",
    username="your_username",
    password="your_password",
    user_agent="your_user_agent",
)


# Input subreddit name
subreddit_name = input("Enter the name of the subreddit to scrape: ")

# Initialize subreddits list
subreddits = []
subreddit_names = [subreddit_name]

# Get subreddit instances
for subreddit_name in subreddit_names:
    subreddit = reddit.subreddit(subreddit_name)
    subreddits.append(subreddit)

# Create subreddit object
subreddit = reddit.subreddit(subreddit_name)

# Define posts
posts = []
NUM_POSTS = 10

for subreddit in subreddits:
    for submission in subreddit.new(limit=NUM_POSTS):
        posts.append(submission)

# Define iteration
data = []
moderators = []

# Loop through all subreddits and posts
for subreddit in subreddits:
    for post in posts:
        # Exclude moderator posts and comments
        if post.author.name in moderators:
            continue

        # Append post data to the list
        post_data = (
            post.title,
            getattr(post, "post_hint", None),
            post.score,
            post.author.name,
            post.url,
            post.num_comments,
            post.selftext,
            post.created_utc,
        )
        data.append(post_data)

        # Loop through all comments of the post
        post.comments.replace_more(limit=None)
        for comment in post.comments.list():
            # Exclude moderator comments
            if comment.author.name in moderators:
                continue

            # Append comment data to the list
            comment_data = (
                comment.body,
                comment.score,
                comment.author.name,
                comment.created_utc,
                post.id,
                subreddit.display_name,
            )
            data.append(comment_data)

# Get the top 10 hot posts from the subreddit
hot_posts = subreddit.hot(limit=10)

# Create a list of unique commenters from the hot posts
commenters = []
for post in hot_posts:
    post_comments = post.comments
    for comment in post_comments:
        if comment.author not in commenters:
            commenters.append(comment.author)

# Print the list of unique commenters
print(commenters)

# Get created_utc for each subreddit
created_utc = []
for subreddit_name in subreddit_names:
    subreddit = reddit.subreddit(subreddit_name)
    utc = subreddit.created_utc
    created_utc.append(utc)

authors = []
commenters = []
karmas = []
submissions = []
submission = []
title = []
score = []
post_id = []
url = []
created_utc = []

for sub_name in subreddits:
    if isinstance(sub_name, str):
        subreddit = reddit.subreddit(sub_name)
        for submission in subreddit.top(limit=40):
            submission.comment_sort = "top"
            submission.comment_limit = 10
            for comment in submission.comments:
                if isinstance(comment, praw.models.MoreComments):
                    continue
                if comment.author is not None:
                    authors.append(comment.author.name)
                if comment.score is not None:
                    karmas.append(comment.score)
                if comment.author is not None:
                    commenters[comment.author.name] = [comment.score]

            # Extract required information from the submission object
            author = submission.author.name
            upvotes = submission.score
            downvotes = submission.downs
            ratio = submission.upvote_ratio

            # Print out the information for each post
            print(f"Title: {submission.title}")
            print(f"Author: {author}")
            print(f"Upvotes: {upvotes}")
            print(f"Downvotes: {downvotes}")
            print(f"Ratio: {ratio}\n")

if isinstance(commenters, dict):
    # Print out the information for each commenter
    for commenter, votes in commenters.items():
        print(f"Commenter: {commenter}")
        print(f"Upvotes: {sum(votes)}")
        print(f"Downvotes: {len(votes) - sum(votes)}")
        print(f"Ratio: {sum(votes)/len(votes)}\n")
else:
    print("Commenters is not a dictionary")



# Get the subreddit names and remove any prefix
subreddit_names = [sub[2:] if sub.startswith("r/") else sub for sub in subreddit_names]

# Get the top posts in each subreddit
top_posts = []
TIME_FILTER = "month"
for subreddit_name in subreddit_names:
    subreddit = reddit.subreddit(subreddit_name)
    top_posts += subreddit.top(limit=100, time_filter=TIME_FILTER)

# Get post details
for post in top_posts:
    title.append(post.title)
    score.append(post.score)
    post_id.append(post.id)
    url.append(post.url)
    created_utc.append(post.created_utc)

print(title)
print(score)
print(post_id)
print(url)
print(created_utc)


for post in top_posts:
    print(post.title)

# Print the titles of the top posts
for post in top_posts:
    print(post.title)

# Print title and score of each post
for post in top_posts:
    print(post.title, post.score)

# Print the titles of the scraped posts
for post in posts:
    print(post.title)

# Create lists to store the top posters and commenters
NUM_TOP_POSTERS = 5
top_posters = []
top_commenters = []
authors = []
karmas = []
data = []

# pylint moderator_suggestor_reddit.py

# Submissions List
submissions = []
df = pd.DataFrame
for submission in subreddit.top(limit=NUM_TOP_POSTERS):
    submissions.append(submission)
    subreddit_values = [subreddit_names[0]]
    df = pd.DataFrame.subreddit = [subreddit_values]
    submissions.append(submission.score)
    submissions.append(submission.num_comments)

# Get created_utc for each subreddit
created_utc = []
for subreddit_name in subreddit_names:
    subreddit = reddit.subreddit(subreddit_name)
    utc = subreddit.created_utc
    created_utc.append(utc)

for sub_name in subreddit_names:
    subreddit = reddit.subreddit(sub_name)
    for submission in subreddit.top(limit=10):
        submission.comment_sort = "top"
        submission.comment_limit = 10
        for comment in submission.comments:
            if isinstance(comment, praw.models.MoreComments):
                continue
            if comment.author is not None:
                authors.append(comment.author.name)
            if comment.score is not None:
                karmas.append(comment.score)

unique_authors = set(authors)
total_karma = sum(karmas)

# Get the top 10 redditors who have posted in the subreddits in the last month
redditors = []
for subreddit_name in subreddit_names:
    subreddit_name = reddit.subreddit(subreddit_name)
    for submission in subreddit_name.top(time_filter="month", limit=10):
        redditor = reddit.redditor(submission.author.name)
        if redditor not in redditors:
            redditors.append(redditor)


def scrape_subreddit(subreddit_name, start_time, end_time):
    """
    Scrape data from a list of subreddits within the last month.

    Parameters:
    subreddit_names (list): a list of subreddit names to scrape

    Returns:
    pandas.DataFrame: a DataFrame containing information about the scraped posts
    """
    # calculate start and end times
    end_time = int(dt.datetime.utcnow().timestamp())
    start_time = int((dt.datetime.utcnow() - dt.timedelta(days=30)).timestamp())

    scraped_posts = []
    for subreddit_name in subreddit_names:
        subreddit = reddit.subreddit(subreddit_name)  # create subreddit object
        for scraped_post in subreddit.new(limit=None):
            if start_time < scraped_post.created_utc < end_time:
                scraped_posts.append(
                    [
                        scraped_post.title,
                        scraped_post.link_flair_text,
                        scraped_post.score,
                        scraped_post.author.name
                        if scraped_post.author
                        else "[deleted]",
                        scraped_post.url,
                        scraped_post.num_comments,
                        scraped_post.selftext,
                        scraped_post.created_utc,
                    ]
                )

    # convert the scraped posts list into a pandas DataFrame with column names
    df = pd.DataFrame(
        scraped_posts,
        columns=[
            "title",
            "type",
            "score",
            "author",
            "url",
            "num_comments",
            "body",
            "created_utc",
        ],
    )
    df = subreddit = subreddit_names
    return df


# Define iteration
data = []
for post in posts:
    data.append(
        (
            post.title,
            getattr(post, "post_hint", None),
            post.score,
            post.author.name,
            post.url,
            post.num_comments,
            post.selftext,
            post.created_utc,
        )
    )

# pass a list of subreddit objects to the function instead of subreddit names

for subreddit_name in subreddit_names:
    subreddit = reddit.subreddit(subreddit_name)
    start_time = created_utc
    end_time = int(dt.datetime.utcnow().timestamp())
    df = scrape_subreddit(subreddit_name, start_time, end_time)
    data.append(df)

# initialize an empty list to store the scraped data
posts = []
redditors = []
karma = 0

for submission in subreddit.top(time_filter="month", limit=100):
    redditor = reddit.redditor(submission.author.name)
    if redditor not in redditors:
        redditors.append(redditor)
subreddit_names = []
for submission in subreddit.top(time_filter="month", limit=100):
    if submission.subreddit.display_name not in subreddit_names:
        subreddit_names.append(submission.subreddit.display_name)

data = []
for i, subreddit_name in enumerate(subreddit_names):
    start_time = created_utc[i]
    end_time = int(dt.datetime.utcnow().timestamp())
    df = scrape_subreddit(subreddit_name, start_time, end_time)
    data.append(df)

for redditor in redditors:
    try:
        comment_karma = redditor.comment_karma
        karma += comment_karma
        print(f"{redditor.name}: {comment_karma}")
    except:
        print(f"{redditor.name}: failed to get karma")

    hot_posts = subreddit.hot(limit=10)
    for post in hot_posts:
        posts.append(post)

print("Total comment karma of unique authors: ", karma)

# loop through each subreddit
for subreddit_name in subreddit_names:
    try:
        posts = []  # reinitialize posts as an empty list for each subreddit
        sub = reddit.subreddit(subreddit_name)
        hot_posts = sub.hot(limit=100)

        for post in hot_posts:
            # determine the type of post
            post_type = "text"  # assume it is a text post by default
            if post.url.endswith((".jpg", ".jpeg", ".png", ".gif", ".gifv")):
                post_type = "image"
            elif post.url.startswith("https://www.reddit.com/gallery/"):
                post_type = "gallery"
            elif post.url.startswith("https://v.redd.it/"):
                post_type = "video"
            elif post.url.startswith("https://www.youtube.com/"):
                post_type = "youtube"
            elif "poll_data" in post.url:
                post_type = "poll"
            elif "predictions" in post.url:
                post_type = "prediction"

            # append the post data to the posts list
            posts.append(
                [
                    post.title,
                    post_type,
                    post.score,
                    post.author.name,
                    post.url,
                    post.num_comments,
                    post.selftext,
                    post.created_utc,
                ]
            )
    except Exception as e:
        print(f"Error processing subreddit {subreddit_name}: {e}")

data = [
    (
        post[0],
        getattr(post, "post_hint", None),
        post[2],
        post[3],
        post[4],
        post[5],
        post[6],
        post[7],
    )
    for post in posts
]
df = pd.DataFrame(
    data,
    columns=[
        "title",
        "type",
        "score",
        "author",
        "url",
        "num_comments",
        "body",
        "created_utc",
    ],
)

# print the DataFrame
print(df)

# print the first 5 rows of the DataFrame
print(df)
print(df.shape)

# Loop over each subreddit and scrape data
data = []
for i, subreddit_name in enumerate(subreddit_names):
    start_time = created_utc[i]
    end_time = int(dt.datetime.utcnow().timestamp())
    posts = scrape_subreddit(subreddit_name, start_time, end_time)
    data += [
        (
            post[0],
            getattr(post, "post_hint", None),
            post[2],
            post[3],
            post[4],
            post[5],
            post[6],
            post[7],
        )
        for post in posts
    ]

df = pd.DataFrame(
    data,
    columns=[
        "title",
        "type",
        "score",
        "author",
        "url",
        "num_comments",
        "body",
        "created_utc",
    ],
)


# Loop through top 10 comments
for top_level_comment in submission.comments[:10]:
    try:
        # Get the Redditor object for the author of the comment
        redditor = reddit.redditor(top_level_comment.author.name)
        # Check if the Redditor object is valid
        if not redditor:
            print(f"Skipping invalid Redditor {top_level_comment.author.name}")
            continue
        # Get the link karma of the author of the comment
        author_karma = redditor.link_karma
    except (
        prawcore.exceptions.NotFound,
        praw.exceptions.PRAWException,
        AttributeError,
    ):
        print(f"Skipping deleted or banned user {top_level_comment.author.name}")
        continue

    # Get the number of replies to the comment
    num_replies = 0
    for reply in top_level_comment.replies:
        try:
            reply.replies
        except praw.exceptions.PRAWException:
            print(f"Skipping deleted or banned user {reply.author.name}")
            continue
        num_replies += 1

    # Append the data to the list
    data.append(
        {
            "created_utc": top_level_comment.created_utc,
            "body": top_level_comment.body,
            "score": top_level_comment.score,
            "author": top_level_comment.author.name,
            "author_karma": author_karma,
            "num_replies": num_replies,
        }
    )

# Loop over each subreddit and scrape data
data = []
for i, subreddit_name in enumerate(subreddit_names):
    start_time = created_utc[i]
    end_time = int(dt.datetime.utcnow().timestamp())
    df = pd.DataFrame()
    df = scrape_subreddit(subreddit_name, start_time, end_time)
if isinstance(df, pd.DataFrame):
    df["subreddit"] = subreddit_name
else:
    print("df is not a DataFrame")
    data.append(df)

posts = reddit.subreddit(subreddit_name).hot(limit=100)

data = []
for post in posts:
    title = post.title
    post_hint = post.post_hint if hasattr(post, "post_hint") else None
    score = post.score
    author = post.author.name
    url = post.url
    num_comments = post.num_comments
    body = post.selftext
    created_utc = post.created_utc
    data.append([title, post_hint, score, author, url, num_comments, body, created_utc])

# Combine data into a single dataframe
df = pd.DataFrame(
    data,
    columns=[
        "title",
        "type",
        "score",
        "author",
        "url",
        "num_comments",
        "body",
        "created_utc",
    ],
)

print(df)
print(df.shape)
print(type(df))

# Get the created_utc for each subreddit
created_utcs = [
    reddit.subreddit(subreddit_name).created_utc for subreddit_name in subreddit_names
]

# Calculate the start epoch based on the minimum value
start_epoch = min(created_utcs)

end_epoch = int(pd.Timestamp.utcnow().timestamp())

# Initialize data arrays
post_count = []
comment_count = []
top_posters = []
top_commenters = []
flair_counts = {}
mod_logs = {}

# Create an empty dataframe to store the data
data = pd.DataFrame(
    columns=[
        "title",
        "score",
        "post_id",
        "subreddit",
        "url",
        "num_comments",
        "body",
        "created",
    ]
)

# Create a list to store the post and comment counts
post_count = []
comment_count = []

# Create lists to store the top posters and commenters
NUM_TOP_POSTERS = 5
top_posters = []
top_commenters = []

# Get created_utc for each subreddit
authors = []
commenters = {}
karmas = []
submissions = []
submission = []
title = []
score = []
post_id = []
url = []
scraped_posts = []
subreddit = []

for sub_name in subreddits:
    if isinstance(sub_name, str):
        subreddit = reddit.subreddit(sub_name)
        for submission in subreddit.top(limit=40):
            submission.comment_sort = "top"
            submission.comment_limit = 10
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                if comment.author is not None:
                    authors.append(comment.author.name)
                if comment.score is not None:
                    karmas.append(comment.score)
                if comment.author is not None:
                    if comment.author.name in commenters:
                        commenters[comment.author.name].append(comment.score)
                    else:
                        commenters[comment.author.name] = [comment.score]

            # Extract required information from the submission object
            author = submission.author.name
            upvotes = submission.score
            downvotes = submission.downs
            ratio = submission.upvote_ratio

            # Print out the information for each post
            print(f"Title: {submission.title}")
            print(f"Author: {author}")
            print(f"Upvotes: {upvotes}")
            print(f"Downvotes: {downvotes}")
            print(f"Ratio: {ratio}\n")

            # Print out the information for each commenter
            for commenter, votes in commenters.items():
                print(f"Commenter: {commenter}")
                print(f"Upvotes: {sum(votes)}")
                print(f"Downvotes: {len(votes) - sum(votes)}")
                print(f"Ratio: {sum(votes)/len(votes)}\n")
    else:
        print(f"{sub_name} is not a valid subreddit name")

# Print title and score of each post
for top_post in top_posts:
    print(top_post.title, top_post.score)


# calculate start and end times
end_time = int(dt.datetime.utcnow().timestamp())
start_time = int((dt.datetime.utcnow() - dt.timedelta(days=30)).timestamp())


def scrape_subreddits(subreddit_names):
    scraped_posts = []
    for subreddit_name in subreddit_names:
        subreddit = reddit.subreddit(subreddit_name)  # create subreddit object
        for scraped_post in subreddit.new(limit=None):
            if start_time < scraped_post.created_utc < end_time:
                scraped_posts.append(
                    [
                        scraped_post.title,
                        scraped_post.link_flair_text,
                        scraped_post.score,
                        scraped_post.author.name
                        if scraped_post.author
                        else "[deleted]",
                        scraped_post.url,
                        scraped_post.num_comments,
                        scraped_post.selftext,
                        scraped_post.created_utc,
                    ]
                )

    # convert the scraped posts list into a pandas DataFrame with column names
    df = pd.DataFrame(
        scraped_posts,
        columns=[
            "title",
            "type",
            "score",
            "author",
            "url",
            "num_comments",
            "body",
            "created_utc",
        ],
    )
    return df


# Get the number of times each post flair was used in the time period
for subreddit in subreddits:
    for post in subreddit.new(limit=None):
        if post.link_flair_text:
            if post.link_flair_text in flair_counts:
                flair_counts[post.link_flair_text] += 1
            else:
                flair_counts[post.link_flair_text] = 1

# Define iteration
data = []
moderators = []
moderator_usernames = []

# Loop through all subreddits and posts
for subreddit in subreddits:
    for post in posts:
        # Exclude moderator posts and comments
        if post.author.name in moderators:
            continue

        # Append post data to the list
        post_data = (
            post.title,
            getattr(post, "post_hint", None),
            post.score,
            post.author.name,
            post.url,
            post.num_comments,
            post.selftext,
            post.created_utc,
        )
        data.append(post_data)

        # Loop through all comments of the post
        post.comments.replace_more(limit=None)
        for comment in post.comments.list():
            # Exclude moderator comments
            if comment.author.name in moderators:
                continue

            # Append comment data to the list
            comment_data = (
                comment.body,
                comment.score,
                comment.author.name,
                comment.created_utc,
                post_id.id,
                subreddit.display_name,
            )
            data.append(comment_data)

# Scrape the mod logs for each user and calculate their infraction rate
moderation_data = []
potential_moderators = set()
for subreddit_name in subreddit_names:
    sub = reddit.subreddit(subreddit_name)
    mod_actions = sub.mod.log(limit=1000, mod=None)
    print(f"Subreddit: {subreddit_name}")

    for action in mod_actions:
        if action.action == "add" and action.mod.name not in moderator_usernames:
            potential_moderators.add(action.mod.name)
            print(f"Potential mod added: {action.mod.name}")

    for moderator in sub.moderator():
        if moderator.name in moderator_usernames:
            continue  # skip this moderator
    try:
        INFRACTIONS = 0
        TOTAL_ACTIONS = 0
        mod_log = reddit.request(
            method="GET",
            path=f"r/{subreddit_name}/about/log/",
            params={"mod": moderator.name},
        )
        for log in mod_log["data"]["children"]:
            if log["data"]["action"] in [
                "removecomment",
                "removelink",
                "spamcomment",
                "spamlink",
                "banuser",
                "unbanuser",
            ]:
                INFRACTIONS += 1
            TOTAL_ACTIONS += 1
        if TOTAL_ACTIONS == 0:
            infraction_rate = 0
        else:
            infraction_rate = INFRACTIONS / TOTAL_ACTIONS
        moderation_data.append((moderator, INFRACTIONS, TOTAL_ACTIONS, infraction_rate))
    except prawcore.exceptions.PrawcoreException as e:
        print(f"Subreddit: {subreddit_name}")

moderation_data = sorted(moderation_data, key=lambda x: x[3], reverse=True)

# Convert the data to Pandas dataframes
df_post_count = pd.DataFrame(post_count, index=subreddits, columns=["Post Count"])
df_comment_count = pd.DataFrame(
    comment_count, index=subreddits, columns=["Comment Count"]
)
for posters in top_posters:
    if len(posters) < NUM_TOP_POSTERS:
        posters += ["None"] * (NUM_TOP_POSTERS - len(posters))
df_top_posters = pd.DataFrame(
    top_posters, index=subreddits, columns=[f"Top Poster {i}" for i in range(1, 6)]
)
df_top_commenters = pd.DataFrame(
    top_commenters,
    index=subreddits,
    columns=["Rank", "Username", "Comments", "Submissions", "Total"],
)

# Create a dataframe from the flair_counts dictionary and sort it in descending order
DF_FLAIR_COUNTS = pd.DataFrame.from_dict(
    flair_counts, orient="index", columns=["Flair Count"]
).sort_values(by="Flair Count", ascending=False)

# Print the dataframes
print(df_post_count)
print(df_comment_count)
print(df_top_posters)
print(df_top_commenters)
print(DF_FLAIR_COUNTS)

# Export the dataframes to a single CSV file
df = pd.concat(
    [
        df_post_count,
        df_comment_count,
        df_top_posters,
        df_top_commenters,
        DF_FLAIR_COUNTS,
    ],
    axis=1,
)
df.to_csv("reddit_data.csv")

# Get the moderators for the subreddit
moderators = reddit.subreddit(subreddit_names[0]).moderator()

# Get a list of users who have been moderators in the past
moderators = []
for subreddit_name in subreddit_names:
    for mod in reddit.subreddit(subreddit_name).moderator():
        moderators.append(mod.name)

# Get the mod log for the subreddit
subreddit_name = subreddits[0].display_name  # extract the name of the subreddit
mod_log = reddit.subreddit(subreddit_name).mod.log(limit=None)

# Scrape the mod logs for each user and calculate their infraction rate
moderation_data = []
for moderator in moderators:
    try:
        INFRACTIONS = 0
        TOTAL_ACTIONS = 0
        if isinstance(moderator, praw.models.Redditor):
            for log in reddit.redditor(moderator).mod.log(limit=None):
                if log.action in [
                    "removecomment",
                    "removelink",
                    "spamcomment",
                    "spamlink",
                    "banuser",
                    "unbanuser",
                ]:
                    INFRACTIONS += 1
                TOTAL_ACTIONS += 1
            infraction_rate = INFRACTIONS / TOTAL_ACTIONS
            moderation_data.append(
                (moderator, INFRACTIONS, TOTAL_ACTIONS, infraction_rate)
            )
    except prawcore.exceptions.PrawcoreException as e:
        print(f"Subreddit: {subreddit_name}")

# Define the list of actions to consider
actions = ["approve", "remove", "spam", "banuser", "unbanuser"]

# Find potential moderators who are active in the given subreddits
potential_moderators = set()
for subreddit_name in subreddits:
    if isinstance(subreddit_name, str):
        sub = reddit.subreddit(subreddit_name)
    else:
        sub = subreddit_name
    for top_contributor in subreddit_name.top(time_filter="month", limit=10):
        if (
            str(top_contributor.author) not in moderator_usernames
            and str(top_contributor.author) not in potential_moderators
        ):
            try:
                if top_contributor.author.total_karma > 100:
                    potential_moderators.add(str(top_contributor.author))
            except prawcore.exceptions.PrawcoreException as e:
                print(f"Subreddit: {subreddit_name}")

# Initialize dictionary to hold moderator activity
mod_activity = {}

# Loop over the moderators and gather their activity
for mod in moderators:
    if isinstance(mod, praw.models.Redditor):
        mod_activity[mod.name] = {action: 0 for action in actions}
        for item in reddit.subreddit("mod").mod.stream.edited():
            print(item)
            for item in mod_log:
                if (
                    isinstance(item.mod, praw.models.Redditor)
                    and item.mod.name == mod.name
                    and item.action in actions
                ):
                    mod_activity[mod.name][item.action] += 1

# Convert the moderator activity to a dataframe
df_mod_activity = pd.DataFrame.from_dict(mod_activity, orient="index")

# Calculate the total actions for each moderator and sort the dataframe
df_mod_activity["Total"] = df_mod_activity.sum(axis=1)
DF_MOD_ACTIVITY = df_mod_activity.sort_values(by="Total", ascending=False)

# Print the moderator activity dataframe
print(df_mod_activity)

# Determine the top candidates for new moderators
top_candidates = df_mod_activity[
    df_mod_activity["Total"] == df_mod_activity["Total"].max()
].index.tolist()

# Print the top moderator candidates
print("Top moderator candidates: " + ", ".join(top_candidates))

# Convert the moderation data to a Pandas dataframe
DF_MODERATION_DATA = pd.DataFrame(
    moderation_data,
    columns=["Username", "Infractions", "Total Actions", "Infraction Rate"],
).set_index("Username")

# Sort the moderation data by infraction rate
DF_MODERATION_DATA.sort_values(by="Infraction Rate", ascending=True, inplace=True)

# Print the moderation data
print(DF_MODERATION_DATA)

# Find the users who are not current moderators and have the lowest infraction rates
best_moderators = list(
    DF_MODERATION_DATA.loc[~DF_MODERATION_DATA.index.isin(moderator_usernames)]
    .head(NUM_TOP_POSTERS)
    .index
)

# define a list of top users
top_users = ["user1", "user2", "user3", "user4", "user5"]


# Define a function to evaluate the users based on certain criteria
def evaluate_user(user):
    """
    Evaluate a user based on certain criteria.

    Args:
        user (str): The name of the user to evaluate.

    Returns:
        bool: True if the user meets all criteria, False otherwise.
    """
    # Define the criteria to evaluate the users on
    criteria = {
        "active": True,
        "helpful": True,
        "knowledgeable": True,
        "friendly": True,
    }

    # evaluate the user based on the criteria
    score = 0
    if criteria["active"]:
        # check if the user is active on the platform
        if user["activity"] >= 10:
            score += 1
    if criteria["helpful"]:
        # check if the user has a history of providing helpful answers
        if user["helpful_answers"] >= 100:
            score += 1
    if criteria["knowledgeable"]:
        # check if the user has a high knowledge score
        if user["knowledge_score"] >= 80:
            score += 1
    if criteria["friendly"]:
        # check if the user has a friendly demeanor
        if user["friendly_score"] >= 90:
            score += 1

    # return the user's score
    return score


# define a function to suggest moderators based on the evaluation
def suggest_moderators(users):
    """
    Suggest moderators based on the evaluation scores of users.

    Args:
        users (list): A list of dictionaries containing information about users.

    Returns:
        list: A sorted list of user dictionaries based on their evaluation scores.
    """
    # sort the users based on their evaluation scores
    users.sort(key=evaluate_user, reverse=True)

    # suggest the top 5 users as moderators
    return users[:5]


# define a list of users with their corresponding scores for the criteria
users = [
    {
        "name": "user1",
        "activity": 20,
        "helpful_answers": 150,
        "knowledge_score": 85,
        "friendly_score": 95,
    },
    {
        "name": "user2",
        "activity": 15,
        "helpful_answers": 120,
        "knowledge_score": 75,
        "friendly_score": 90,
    },
    {
        "name": "user3",
        "activity": 12,
        "helpful_answers": 100,
        "knowledge_score": 90,
        "friendly_score": 80,
    },
    {
        "name": "user4",
        "activity": 10,
        "helpful_answers": 80,
        "knowledge_score": 70,
        "friendly_score": 85,
    },
    {
        "name": "user5",
        "activity": 8,
        "helpful_answers": 50,
        "knowledge_score": 60,
        "friendly_score": 75,
    },
]

# suggest the moderators
suggested_moderators = suggest_moderators(users)

# suggest the moderators
suggested_moderators = suggest_moderators(users)
print(suggested_moderators)  # add this line to check if the function returns any values

# print the suggested moderators
print("The following users are suggested to become moderators:")
if suggested_moderators:
    for moderator in suggested_moderators:
        print(f"- {moderator['name']}")
else:
    print(
        "No suggested moderators found"
    )  # add this line to indicate if there are no suggested moderators

# Export the dataframes to a single CSV file
df.to_csv("reddit_data.csv")
DF_MODERATION_DATA.to_csv("moderation_data.csv")

print("Script completed successfully!")
