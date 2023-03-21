#!/usr/bin/python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import csv
import json
import praw
import prawcore
import prawcore.exceptions
import datetime as dt
import time

# Create a Reddit instance using PRAW
reddit = praw.Reddit(
    client_id="xxxxxxxxxxx",
    client_secret="xxxxxxxxxxx",
    password="xxxxxxxxxxx",
    user_agent="xxxxxxxxxxx",
    username="xxxxxxxxxxxxx",
    timeout=30,)
    
subreddit_names = ['TheBidenshitshow', 'TheDonaldTrump2024', 'TheLEFTISTshitshow', 'Trumped']
# Get created_utc for each subreddit
created_utc = []
for subreddit_name in subreddit_names:
    subreddit = reddit.subreddit(subreddit_name)
    utc = subreddit.created_utc
    created_utc.append(utc)

# Define function to scrape data from a subreddit
def scrape_subreddit(subreddit_name, start_time, end_time):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    for post in subreddit.new():
        if start_time < post.created_utc < end_time:
            posts.append([post.id, post.title, post.score, post.num_comments, post.created_utc])
    posts_df = pd.DataFrame(posts, columns=['id', 'title', 'score', 'num_comments', 'created_utc'])
    return posts_df

# initialize an empty list to store the scraped data
posts = []

redditors = []
karma = 0

for submission in subreddit.top(time_filter='month', limit=100):
    redditor = reddit.redditor(submission.author.name)
    if redditor not in redditors:
        redditors.append(redditor)
for redditor in redditors:
    try:
        comment_karma = redditor.comment_karma
        karma += comment_karma
        print(f"{redditor.name}: {comment_karma}")
    except:
        print(f"{redditor.name}: failed to get karma")

print("Total comment karma of unique authors: ", karma)

# loop through each subreddit
for subreddit_name in subreddit_names:
    subreddit = reddit.subreddit(subreddit_name)
    hot_posts = subreddit.hot(limit=10)

    # loop through each post
    for post in hot_posts:
        # determine the type of post
        post_type = 'text'  # assume it is a text post by default
        if post.url.endswith(('.jpg', '.jpeg', '.png', '.gif', '.gifv')):
            post_type = 'image'
        elif post.url.startswith('https://www.reddit.com/gallery/'):
            post_type = 'gallery'
        elif post.url.startswith('https://v.redd.it/'):
            post_type = 'video'
        elif post.url.startswith('https://www.youtube.com/'):
            post_type = 'youtube'
        elif 'poll_data' in post.url:
            post_type = 'poll'
        elif 'predictions' in post.url:
            post_type = 'prediction'
        
        # append the post data to the posts list
        posts.append([post.title, post_type, post.score, post.author.name, post.url, post.num_comments, post.selftext, post.created_utc])

# create a DataFrame from the posts list
df = pd.DataFrame(posts, columns=['title', 'type', 'score', 'author', 'url', 'num_comments', 'body', 'created_utc'])

# print the DataFrame
print(df)

# convert the posts list into a pandas DataFrame
df = pd.DataFrame(posts, columns=['title', 'type', 'score', 'author', 'url', 'num_comments', 'body', 'created_utc'])

# print the first 5 rows of the DataFrame
print(df.head())

# Loop over each subreddit and scrape data
data = []
for i, subreddit_name in enumerate(subreddit_names):
    start_time = created_utc[i]
    end_time = int(dt.datetime.utcnow().timestamp())
    df = scrape_subreddit(subreddit_name, start_time, end_time)
    df['subreddit'] = subreddit_name
    
    # Get top-level comments for each subreddit
    subreddit = reddit.subreddit(subreddit_name)
    top_comments = {}
    for submission in subreddit.top(time_filter='month', limit=10):
        submission.comments.replace_more(limit=0)
        top_comments[submission.id] = [comment.id for comment in submission.comments if not comment.author is None]
    
    # Loop through top-level comments and extract Redditor info
    for submission_id, comment_ids in top_comments.items():
        for comment_id in comment_ids[:10]:
            try:
                # Get the Redditor object for the author of the comment
                comment = reddit.comment(comment_id)
                redditor = comment.author
            except praw.exceptions.PRAWException:
                print(f"Skipping deleted or banned user")
                continue

# Loop through top 10 comments
for top_level_comment in submission.comments[:10]:
    try:
        # Get the Redditor object for the author of the comment
        redditor = reddit.redditor(top_level_comment.author.name)
    except prawcore.exceptions.NotFound:
        print(f"Skipping deleted or banned user {top_level_comment.author.name}")
        continue

    # Print the Redditor's name and karma
    print(f"Redditor: {redditor.name}, Karma: {redditor.link_karma}")
    
    data.append(df)

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
    data.append({
        'created_utc': top_level_comment.created_utc,
        'body': top_level_comment.body,
        'score': top_level_comment.score,
        'author': top_level_comment.author.name,
        'author_karma': redditor.link_karma,
        'num_replies': num_replies
    })

# Loop over each subreddit and scrape data
data = []
for i, subreddit_name in enumerate(subreddit_names):
    start_time = created_utc[i]
    end_time = int(dt.datetime.utcnow().timestamp())
    df = scrape_subreddit(subreddit_name, start_time, end_time)
    df['subreddit'] = subreddit_name
    data.append(df)

# Combine data into a single dataframe
data_df = pd.concat(data, ignore_index=True)

# Get the created_utc for each subreddit
created_utcs = [reddit.subreddit(subreddit_name).created_utc for subreddit_name in subreddit_names]

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

# Define the usernames of the moderators to exclude
moderator_usernames = ['StinkyPete312', 'Disastrous_Blood1998', 'TheRealPotHead37', 'Buy_reddit_next_elon', 'Secretrider', 'ToeKneeh', 'gelber_Bleistift', 'ZeRo76Liberty', 'RaisinL', 'Allan_QuartermainSr', 'sailor-jackn', 'AutoModerator', 'onionbutter1', 'Plantsrmedicine72', 'PNWSparky1988', 'pointsouturhypocrisy', 'Jim_Eagle_Laws']

# Define the subreddits to scrape
subreddit_names = ['TheBidenshitshow', 'TheDonaldTrump2024', 'TheLEFTISTshitshow', 'Trumped']

# Create an empty dataframe to store the data
data = pd.DataFrame(columns=['id', 'title', 'score', 'num_comments', 'created_utc', 'subreddit'])

# Create a list to store the post and comment counts
post_count = []
comment_count = []

# Create lists to store the top posters and commenters
num_top_posters = 5
top_posters = []
top_commenters = []

# Get created_utc for each subreddit
created_utc = []
for subreddit_name in subreddit_names:
    subreddit = reddit.subreddit(subreddit_name)
    utc = subreddit.created_utc
    created_utc.append(utc)

# Define function to scrape data from a subreddit
def scrape_subreddit(subreddit_name, start_time, end_time):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    for post in subreddit.new(limit=None):
        if start_time <= post.created_utc <= end_time:
            posts.append([post.id, post.title, post.score, post.num_comments, post.created_utc])
    posts_df = pd.DataFrame(posts, columns=['id', 'title', 'score', 'num_comments', 'created_utc'])
    return posts_df

# Loop over each subreddit and gather the data
for subreddit_name in subreddit_names:
    subreddit = reddit.subreddit(subreddit_name)

    # Set the start and end times for the data to be scraped
    end_time = min(created_utc)
    start_time = end_time - 2592000  # Scrape data from the past 30 days

    # Scrape the data for the subreddit and append it to the dataframe
    df = scrape_subreddit(subreddit_name, start_time, end_time)
    df['subreddit'] = subreddit_name
    data.append(df, ignore_index=True)
    time.sleep(1)
    
    # Get the number of posts and comments in the time period
    post_count.append(len(list(subreddit.new(limit=None))))
    comment_count.append(len(list(subreddit.comments(limit=None))))

    # Get the top posters and commenters in the time period
    top_posters.append([str(submission.author) for submission in subreddit.top(time_filter='month', limit=num_top_posters) if str(submission.author) not in moderator_usernames])
    top_commenters.append([[(str(comment.author), comment.score) for comment in sorted(submission.comments, key=lambda comment: comment.score, reverse=True)[:10] if str(comment.author) not in moderator_usernames] for submission in subreddit.top(time_filter='month', limit=num_top_posters)])


    # Get the number of times each post flair was used in the time period
    for post in subreddit.new(limit=None):
        if post.link_flair_text:
            if post.link_flair_text in flair_counts:
                flair_counts[post.link_flair_text] += 1
            else:
                flair_counts[post.link_flair_text] = 1
           
# Define the usernames of the moderators to exclude
moderator_usernames = ['StinkyPete312', 'Disastrous_Blood1998', 'TheRealPotHead37', 'Buy_reddit_next_elon', 'Secretrider', 'ToeKneeh', 'gelber_Bleistift', 'ZeRo76Liberty', 'RaisinL', 'Allan_QuartermainSr', 'sailor-jackn', 'AutoModerator', 'onionbutter1', 'Plantsrmedicine72', 'PNWSparky1988', 'pointsouturhypocrisy', 'Jim_Eagle_Laws']

# Scrape the mod logs for each user and calculate their infraction rate
moderation_data = []
potential_moderators = set()
subreddits = ['TheBidenshitshow', 'TheDonaldTrump2024', 'TheLEFTISTshitshow', 'Trumped']
for subreddit_name in subreddits:
    subreddit = reddit.subreddit(subreddit_name)
    mod_actions = subreddit.mod.log(limit=1000)

    for action in mod_actions:
        if action.action == 'add' and action.mod.name not in moderator_usernames:
            potential_moderators.add(action.mod.name)

# Scrape the mod logs for each user and calculate their infraction rate
moderation_data = []
potential_moderators = set()
subreddits = ['TheBidenshitshow', 'TheDonaldTrump2024', 'TheLEFTISTshitshow', 'Trumped']
for subreddit_name in subreddits:
    subreddit = reddit.subreddit(subreddit_name)
    mod_actions = subreddit.mod.log(limit=1000)
    print(f"Subreddit: {subreddit_name}")

    mod_actions = subreddit.mod.log(limit=1000, mod=None)
for action in mod_actions:
        if action.action == 'add' and action.mod.name not in moderator_usernames:
            potential_moderators.add(action.mod.name)
            print(f"Potential moderator added: {action.mod.name}")

for moderator in subreddit.moderator():
        if moderator.name not in moderator_usernames and moderator.name not in potential_moderators:
            try:
                infractions = 0
                total_actions = 0
                if isinstance(moderator, praw.models.Redditor):
                    mod_log = reddit.request(method='GET', path=f'r/{subreddit_name}/about/log/', params={'mod': moderator.name})
                    for log in mod_log['data']:
                        if log['action'] in ['removecomment', 'removelink', 'spamcomment', 'spamlink', 'banuser', 'unbanuser']:
                            infractions += 1
                        total_actions += 1
                    infraction_rate = infractions / total_actions
                    moderation_data.append((moderator, infractions, total_actions, infraction_rate))
            except Exception as e:
                print('Error: {}'.format(e))

moderation_data = sorted(moderation_data, key=lambda x: x[3], reverse=True)

            
# Convert the data to Pandas dataframes
df_post_count = pd.DataFrame(post_count, index=subreddits, columns=['Post Count'])
df_comment_count = pd.DataFrame(comment_count, index=subreddits, columns=['Comment Count'])
for posters in top_posters:
    if len(posters) < num_top_posters:
        posters += ['None'] * (num_top_posters - len(posters))
df_top_posters = pd.DataFrame(top_posters, index=subreddits, columns=['Top Poster {}'.format(i) for i in range(1, 6)])
df_top_commenters = pd.DataFrame(top_commenters, index=subreddits, columns=['Rank', 'Username', 'Comments', 'Submissions', 'Total'])


# Create a dataframe from the flair_counts dictionary and sort it in descending order
df_flair_counts = pd.DataFrame.from_dict(flair_counts, orient='index', columns=['Flair Count']).sort_values(by='Flair Count', ascending=False)

# Print the dataframes
print(df_post_count)
print(df_comment_count)
print(df_top_posters)
print(df_top_commenters)
print(df_flair_counts)

# Export the dataframes to a single CSV file
df = pd.concat([df_post_count, df_comment_count, df_top_posters, df_top_commenters, df_flair_counts], axis=1)
df.to_csv('reddit_data.csv')

# Get the moderators for the subreddit
moderators = reddit.subreddit(subreddits[0]).moderator()

# Get a list of users who have been moderators in the past
moderators = []
for mod in reddit.subreddit('TheDonaldTrump2024').moderator():
    moderators.append(mod.name)
    
# Get the mod log for the subreddit
mod_log = reddit.subreddit(subreddits[0]).mod.log(limit=None)

# Scrape the mod logs for each user and calculate their infraction rate
moderation_data = []
for moderator in moderators:
    try:
        infractions = 0
        total_actions = 0
        if isinstance(moderator, praw.models.Redditor):
            for log in reddit.redditor(moderator).mod.log(limit=None):
                if log.action in ['removecomment', 'removelink', 'spamcomment', 'spamlink', 'banuser', 'unbanuser']:
                    infractions += 1
                total_actions += 1
            infraction_rate = infractions / total_actions
            moderation_data.append((moderator, infractions, total_actions, infraction_rate))
    except Exception as e:
        print('Error: {}'.format(e))

# Define the list of actions to consider
actions = ['approve', 'remove', 'spam', 'banuser', 'unbanuser']

# Find potential moderators who are active in the given subreddits
potential_moderators = set()
for subreddit_name in subreddits:
    subreddit = reddit.subreddit(subreddit_name.replace('_', ' '))
    for top_contributor in subreddit.top(time_filter='month', limit=10):
        if str(top_contributor.author) not in moderator_usernames and str(top_contributor.author) not in potential_moderators:
            try:
                if top_contributor.author.total_karma > 100:
                    potential_moderators.add(str(top_contributor.author))
            except Exception as e:
                print('Error: {}'.format(e))

# Initialize dictionary to hold moderator activity
mod_activity = {}

# Loop over the moderators and gather their activity
for mod in moderators:
    if isinstance(mod, praw.models.Redditor):
        mod_activity[mod.name] = {action: 0 for action in actions}
        for item in reddit.subreddit("mod").mod.stream.edited():
            print(item)
            for item in mod_log:
                if isinstance(item.mod, praw.models.Redditor) and item.mod.name == mod.name and item.action in actions:
                    mod_activity[mod.name][item.action] += 1
                    
# Convert the moderator activity to a dataframe
df_mod_activity = pd.DataFrame.from_dict(mod_activity, orient='index')

# Calculate the total actions for each moderator and sort the dataframe
df_mod_activity['Total'] = df_mod_activity.sum(axis=1)
df_mod_activity = df_mod_activity.sort_values(by='Total', ascending=False)

# Print the moderator activity dataframe
print(df_mod_activity)

# Determine the top candidates for new moderators
top_candidates = df_mod_activity[df_mod_activity['Total'] == df_mod_activity['Total'].max()].index.tolist()

# Print the top moderator candidates
print('Top moderator candidates: ' + ', '.join(top_candidates))

# Convert the moderation data to a Pandas dataframe
df_moderation_data = pd.DataFrame(moderation_data, columns=['Username', 'Infractions', 'Total Actions', 'Infraction Rate']).set_index('Username')

# Sort the moderation data by infraction rate
df_moderation_data.sort_values(by='Infraction Rate', ascending=True, inplace=True)

# Print the moderation data
print(df_moderation_data)

# Find the users who are not current moderators and have the lowest infraction rates
best_moderators = list(df_moderation_data[df_moderation_data.index.isin(moderator_usernames)==False].head(num_top_posters).index)

# define a list of top users
top_users = ['user1', 'user2', 'user3', 'user4', 'user5']

# define a function to evaluate the users based on certain criteria
def evaluate_user(user):
    # define the criteria to evaluate the users on
    criteria = {
        'active': True,
        'helpful': True,
        'knowledgeable': True,
        'friendly': True
    }
    
    # evaluate the user based on the criteria
    score = 0
    if criteria['active']:
        # check if the user is active on the platform
        if user['activity'] >= 10:
            score += 1
    if criteria['helpful']:
        # check if the user has a history of providing helpful answers
        if user['helpful_answers'] >= 100:
            score += 1
    if criteria['knowledgeable']:
        # check if the user has a high knowledge score
        if user['knowledge_score'] >= 80:
            score += 1
    if criteria['friendly']:
        # check if the user has a friendly demeanor
        if user['friendly_score'] >= 90:
            score += 1
            
    # return the user's score
    return score

# define a function to suggest moderators based on the evaluation
def suggest_moderators(users):
    # sort the users based on their evaluation scores
    users.sort(key=evaluate_user, reverse=True)
    
    # suggest the top 3 users as moderators
    return users[:3]

# define a list of users with their corresponding scores for the criteria
users = [
    {'name': 'user1', 'activity': 20, 'helpful_answers': 150, 'knowledge_score': 85, 'friendly_score': 95},
    {'name': 'user2', 'activity': 15, 'helpful_answers': 120, 'knowledge_score': 75, 'friendly_score': 90},
    {'name': 'user3', 'activity': 12, 'helpful_answers': 100, 'knowledge_score': 90, 'friendly_score': 80},
    {'name': 'user4', 'activity': 10, 'helpful_answers': 80, 'knowledge_score': 70, 'friendly_score': 85},
    {'name': 'user5', 'activity': 8, 'helpful_answers': 50, 'knowledge_score': 60, 'friendly_score': 75}
]

# suggest the moderators
suggested_moderators = suggest_moderators(users)

# print the suggested moderators
print('The following users are suggested to become moderators:')
for moderator in suggested_moderators:
    print('- {}'.format(moderator['name']))


# Print the list of best moderators
print('The following users would make good moderators:')
for moderator in best_moderators:
    print(moderator)

# Export the dataframes to a single CSV file
df.to_csv('reddit_data.csv')
df_moderation_data.to_csv('moderation_data.csv')
