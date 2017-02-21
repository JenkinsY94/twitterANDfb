import facebook
#coding:utf-8

def token_entend(old_token):
    app_id = '861265274016410'
    app_secret = 'e3fe3e2ee13543322f5b8c46c8f9a36f'
    graph = facebook.GraphAPI(access_token=old_token)
    new_token = graph.extend_access_token(app_id,app_secret)
    return new_token

def login_FB(token):
    graph = facebook.GraphAPI(access_token=token)
    my_info = graph.get_object('me')
    #return(my_info['email'])
    #print(my_info['id'])
    return graph

def getNewsFeeds(graph):
    pages = graph.get_connections(id='me', connection_name='likes')
    txts = []
    for page in pages['data']:
        pid = page['id']
        txt = [page['name']]
        posts = graph.get_connections(id=pid, connection_name='posts')
        if 'message' in posts['data'][0]:
            txt.append(posts['data'][0]['message'])
        #pid = pages['data'][0]['id']
        #posts = graph.get_connections(id=pid, connection_name='posts')
        txt.append(posts['data'][0]['created_time'])
        txts.append(txt)
    return txts
#post message
#graph.put_object(parent_object='me',connection_name='feed',message='Test')

#get post info
#posts = graph.get_connections(id='me', connection_name='posts')
#print(posts['data'][0]['message'])

#post photo
#graph.put_photo(image=open('./p1.jpg','rb'), message = "天虎劍令")

if __name__ == "__main__": 
    token = 'EAAMPUPK3EpoBAPhleJ2yZA7OvZByN2sq0VezW59SKQGeH3rZBtrVqrFuKH5oq3FXXpZAZArLw1ZCZCUOQng4n2lf97p7fdB3qpauAW3MyL9vwrooPK4LfHTi0VleHADc8EGj0cCS0Ph1T0VsAlZCUScrHoU8Tinohy0ZD'
    #token = token_entend(token)
    mygraph = login_FB(token);
    news_Posts = getNewsFeeds(mygraph)
    with open("./NewsPosts.txt",'w', encoding='UTF-8') as f:
        for page in news_Posts:
            f.write('='*20)
            f.write(page[0])
            f.write('='*20)
            f.write('\n')
            for x in range(1,len(page)):
                f.write(page[x])
                f.write('\n')
            f.write('\n')
            f.write('\n')
        f.close()
