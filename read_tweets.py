
import re

import tweepy
from tweepy import Cursor
from creds import key, secretKey
from creds import accessToken, accessTokenSecret



# v2 api
# client = tweepy.Client(
#     consumer_key=key,
#     consumer_secret=secretKey,
#     access_token=accessToken,
#     access_token_secret=accessTokenSecret
# )

# tweets = client.get_users_tweets(id='thatVIstunna', max_results=100)




user_list = [
    {'name': 'dog_feelings', 'file': 'dog_tweets.txt'},
    {'name': 'feline_feelings', 'file': 'cat_tweets.txt'}
]



auth = tweepy.OAuthHandler(key, secretKey)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

# test authentication
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")


for user in user_list:

    # friend = api.get_user(screen_name=user['name'])
    # print("User details:")
    # print(friend.name)
    # print(friend.description)
    # print(friend.location)

    allTweets = []

    num_status = 100
    for status in Cursor(api.user_timeline, id=user['name']).items(num_status):
        # remove breaks and urls
        cleanStat = re.sub(r"http\S+", "", status.text)
        cleanStat = cleanStat.replace('\n','')

        # print(cleanStat)
        allTweets.append(cleanStat)

    with open(user['file'], 'w') as f:
        allTweets = [ s + '\n' for s in allTweets ]
        f.writelines( allTweets)

# print( allTweets)

# text = allTweets[0]
# text =  re.sub(r"http\S+", "", text)

# text
