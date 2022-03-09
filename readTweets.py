
import re

import tweepy
from tweepy import Cursor
from creds import key, secretKey 
from creds import accessToken, accessTokenSecret

auth = tweepy.OAuthHandler(key, secretKey)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)


friendName = "dog_feelings"
friend = api.get_user(screen_name=friendName)


# print("User details:")
# print(friend.name)
# print(friend.description)
# print(friend.location)

allTweets = []

numStatuses = 100
for status in Cursor(api.user_timeline, id=friendName).items(numStatuses):
    cleanStat = re.sub(r"http\S+", "", status.text)
    
    print(cleanStat)
    allTweets.append(cleanStat)



# print( allTweets)

# text = allTweets[0]
# text =  re.sub(r"http\S+", "", text)

# text