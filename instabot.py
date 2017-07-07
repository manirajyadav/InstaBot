import requests, urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

access_token ='2067625876.f1530e6.7c216946d050453d8a315f180a7c44b8'
base_url = 'https://api.instagram.com/v1/'

def self_info():

    url_req = base_url+"users/self/?access_token="+access_token
    x= requests.get(url_req)
    user_info = x.json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'

def get_user_id(insta_username):
    request_url = (base_url+'users/search?q=%s&access_token=%s') % (insta_username,access_token)
    print 'GET request url : %s' % (request_url)
    user_id= requests.get(request_url).json()

    if user_id['meta']['code']==200:
        if len(user_id['data']):
            return user_id['data'][0]['id']
        else:
            return None
    else:
        print "Status code other than 200 received."
        exit()


def get_user_info(insta_username):

    user_id= get_user_id(insta_username)
    if user_id==None:
        print "User with the given name does not exist"
        exit()

    request_url = (base_url+'users/%s?access_token=%s') % (user_id,access_token)
    print 'GET request url: %s' %(request_url)
    user_info=requests.get(request_url).json()

    if user_info['meta']['code']==200:
        if len(user_info['data']):
            print "Username: %s" % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'


def get_own_post():
    request_url = (base_url + 'users/self/media/recent/?access_token=%s') % (access_token)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'



def get_user_post(insta_username):
    user_id=get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()

    request_url = (base_url + 'users/%s/media/recent/?access_token=%s') % (user_id, access_token)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get( request_url ).json()

    if user_media['meta']['code'] == 200:
        if len( user_media['data'] ):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve( image_url, image_name )
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (base_url + 'users/%s/media/recent/?access_token=%s') % (user_id, access_token)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()



def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (base_url+ 'media/%s/likes') % (media_id)
    payload = {"access_token": access_token}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'


def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token":access_token, "text" : comment_text}
    request_url = (base_url + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"


def delete_negative_comment(insta_username):
    media_id=get_post_id(insta_username)
    request_url = (base_url + 'media/%s/comments/?access_token=%s') % (media_id, access_token)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get( request_url ).json()

    if comment_info['meta']['info']==200:
        if len(comment_info['data']):
            for x in range(0,len(comment_info['data'])):
                comment_id=comment_info['data'][x]['id']
                comment_text=comment_info['data'][x]['text']
                blob=TextBlob(comment_text,analyzer=NaiveBayesAnalyzer())
                if (blob.sentences.p_neg>blob.sentiment.p_pos):
                    print "Negative comment:%s" %(comment_text)
                    delete_url = (base_url+ 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, access_token)
                    print  "DELETE request url:%s" %(delete_url)
                    delete_info = requests.delete( delete_url ).json()

                    if delete_url['meta']['code']==200:
                        print 'Comment successfully deleted.'
                    else:
                        print 'Unable to delete comment.'
                else:
                    print "Positive comment:%s" %comment_text

        else:
            print "there are no comments on this post yet."
    else:
        print "Status code other than 200 received."



