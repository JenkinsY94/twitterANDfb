import tweepy
import sqlite3

# twitter token configuration
consumer_key = "c43sHTF6pwfXu9uiPyrWeMc95" 
consumer_secret = "c0viwHlmcm63qlIgVtniVUSIpa1ihEp8wdEy2FUspNBNL8EXUr"
access_token = "2730924608-X1AXFfLS7sgyxNxj3APqP8PEbUYgH0u1puhfuB1"
access_secret = "oqNCgBz1aBnzBm98xuVod946iV3IVMJ40IEGd5vKIKYtK"

auth = tweepy.OAuthHandler(consumer_key=consumer_key, \
                           consumer_secret=consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

# tweets: a list of status object 
def storeToDB(tweets):
    # database configuration
    conn = sqlite3.connect('cmsc5702db.sqlite')
    cur = conn.cursor()
    # cur.execute('''
    # DROP TABLE IF EXISTS Twitter''')
    cur.execute('''CREATE TABLE IF NOT EXISTS Twitter 
                   (tweet TEXT, 
                    createTime TEXT, 
                    user TEXT, 
                    id INTEGER NOT NULL PRIMARY KEY UNIQUE)''')
    
    for tweet in tweets:
        cur.execute(''' INSERT INTO Twitter (tweet, createTime, user, id) 
                        VALUES (?,?,?,?)''',\
                        (tweet.text, tweet.created_at, tweet.user.screen_name, tweet.id))
    conn.commit()
    cur.close()

# return a list of json data 
def get_home_timeline():
    public_tweets = api.home_timeline()
    newTweets = []
    for tweet in public_tweets:
        data = {'tweet': tweet.text,
                'createTime': tweet.created_at,
                'user': tweet.user.screen_name,
                'id': tweet.id}
        newTweets.append(data)
    # print newTweets
    # storeToDB(public_tweets)
    return newTweets


if __name__ == '__main__':
    newTweets = get_home_timeline()
    for t in newTweets:
        print t
