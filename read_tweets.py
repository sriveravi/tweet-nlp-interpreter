
import re

import tweepy
from tweepy import Cursor
from creds import key, secretKey
from creds import accessToken, accessTokenSecret

auth = tweepy.OAuthHandler(key, secretKey)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)


user_list = [
    {'name': 'dog_feelings', 'file': 'dog_tweets.txt'},
    {'name': 'feline_feelings', 'file': 'cat_tweets.txt'}
]

for user in user_list:

    friend = api.get_user(screen_name=user['name'])

    # print("User details:")
    # print(friend.name)
    # print(friend.description)
    # print(friend.location)

    allTweets = []

    numStatuses = 100
    for status in Cursor(api.user_timeline, id=user['name']).items(numStatuses):
        cleanStat = re.sub(r"http\S+", "", status.text)

        # print(cleanStat)
        allTweets.append(cleanStat)

    with open(user['file'], 'w') as f:
        f.writelines(allTweets)

# print( allTweets)

# text = allTweets[0]
# text =  re.sub(r"http\S+", "", text)

# text
