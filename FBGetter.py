import facebook
import sqlite3
#coding:utf-8

def storeToDB(feeds):
    connection = sqlite3.connect('cmsc5702db.sqlite')
    cur = connection.cursor()
    # DROP TABLE IF EXISTS FB
    cur.execute('''CREATE TABLE IF NOT EXISTS FB
                   (id TEXT NOT NULL PRIMARY KEY UNIQUE,
                    name TEXT,
                    createTime TEXT,
                    message TEXT )''')
    
    for feed in feeds:
        cur.execute('''INSERT INTO FB (id, name, createTime, message)
                       VALUES (?,?,?,?)''',\
                       (feed[0], feed[1], feed[2], feed[3]))
    
    #cur.execute('''SELECT * FROM FB ORDER BY datetime(createTime) DESC Limit 1''')
    connection.commit()
    cur.close()
    
#get a extened token
def token_entend(old_token):
    app_id = '861265274016410'
    app_secret = 'e3fe3e2ee13543322f5b8c46c8f9a36f'
    graph = facebook.GraphAPI(access_token=old_token)
    new_token = graph.extend_access_token(app_id,app_secret)
    return new_token

#login using the token
def login_FB(token):
    graph = facebook.GraphAPI(access_token=token)
    my_info = graph.get_object('me')
    #print(my_info['email'])
    return graph

#search news feeds from the liked pages
def getNewsFeeds(graph,k):
    #get id of liked pages
    pages = graph.get_connections(id='me', connection_name='likes')
    txts = []
    for page in pages['data']:
        pid = page['id']
        length = k
        txt = []
        #get the posts of the page
        posts = graph.get_connections(id=pid, connection_name='posts')
        #search last k feeds, or length of the pages' posts if the amount of posts smaller than k
        if(len(posts['data'])<k):
            length = len(posts['data'])
        #retrive the infomation of each post
        for i in range (0,length):
            txt.append(posts['data'][i]['id'])
            txt.append(page['name'])
            txt.append(posts['data'][i]['created_time'])
            if 'message' in posts['data'][i]:
                txt.append(posts['data'][i]['message'])
            else:
                txt.append('NULL')
            txts.append(txt)
            txt = []
    storeToDB(txt)
    return txts
    
#post message
def postToFB(graph, txt):
    graph.put_object(parent_object='me',connection_name='feed',message=txt)

#post photo
#graph.put_photo(image=open('./p1.jpg','rb'), message = "天虎劍令")

if __name__ == "__main__": 
    token = 'EAAMPUPK3EpoBAPhleJ2yZA7OvZByN2sq0VezW59SKQGeH3rZBtrVqrFuKH5oq3FXXpZAZArLw1ZCZCUOQng4n2lf97p7fdB3qpauAW3MyL9vwrooPK4LfHTi0VleHADc8EGj0cCS0Ph1T0VsAlZCUScrHoU8Tinohy0ZD'
    #token = token_entend(token)
    mygraph = login_FB(token);
    news_feeds = getNewsFeeds(mygraph,10)
    with open("./NewsPosts.txt",'w', encoding='UTF-8') as f:
        for feed in news_feeds:
            for x in range(1,len(feed)):
                if x==1:
                    f.write('='*20)
                    f.write(feed[x])
                    f.write('='*20)
                    f.write('\n')
                f.write(feed[x])
                f.write('\n')
            f.write('\n')
            f.write('\n')
        f.close()
