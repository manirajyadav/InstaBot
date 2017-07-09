# written by Mani Raj Yadav
# importing required library
import requests
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

# making a variable for received access token
access_token = '2067625876.f1530e6.7c216946d050453d8a315f180a7c44b8'
# setting the base url that is to be used everywhere
base_url = 'https://api.instagram.com/v1/'


# function to display own information
def self_info():
    # setting the url according to the endpoint documentation
    url_req = base_url+"users/self/?access_token="+access_token
    # getting response from url
    x = requests.get(url_req)
    # getting json object
    user_info = x.json()
    # checking whether request is successful or not by getting status code
    if user_info['meta']['code'] == 200:
        # checking whether user is present
        if len(user_info['data']):
            # printing user information
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        # if user is not present
        else:
            print 'User does not exist!'
    # request not successful
    else:
        print 'Status code other than 200 received!'


# function to get user-id by given user name
def get_user_id(insta_username):
    # setting endpoint and creating and accessing json object
    request_url = (base_url+'users/search?q=%s&access_token=%s') % (insta_username , access_token)
    print 'GET request url : %s' % (request_url)
    user_id= requests.get(request_url).json()
    # checking whether the request is successful
    if user_id['meta']['code']==200:
        # checking whether the user exist
        if len(user_id['data']):
            return user_id['data'][0]['id']
        else:
            return None
    # request unsuccessful
    else:
        print "Status code other than 200 received."
        exit()

# function for getting info of user by its instagram username
def get_user_info(insta_username):
    # calling function to get user-id
    user_id= get_user_id(insta_username)
    # if user does not exist
    if user_id==None:
        print "User with the given name does not exist"
        exit()
    # making request and accessing obtained json object
    request_url = (base_url+'users/%s?access_token=%s') % (user_id,access_token)
    print 'GET request url: %s' %(request_url)
    user_info=requests.get(request_url).json()

    # if request is successful
    if user_info['meta']['code']==200:
        # if user-info is present
        if len(user_info['data']):
            print "Username: %s" % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        # user does not exist
        else:
            print 'There is no data for this user!'
    # request unsuccessful
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


# function to access user posts and downloading
def get_user_post(insta_username):
    # calling function to get user-id
    user_id=get_user_id(insta_username)
    # if user doesnt exit
    if user_id == None:
        print 'User does not exist!'
        exit()
    # making request and accessing obtained json object
    request_url = (base_url + 'users/%s/media/recent/?access_token=%s') % (user_id, access_token)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get( request_url ).json()
    # if request is successful
    if user_media['meta']['code'] == 200:
        # if posts exist
        if len( user_media['data'] ):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            # downloading the post
            urllib.urlretrieve( image_url, image_name )
            print 'Your image has been downloaded!'
        # post does not exist
        else:
            print 'Post does not exist!'
    # request unsuccessful
    else:
        print 'Status code other than 200 received!'

# function to get id of post
def get_post_id(insta_username):
    # calling function to get user id
    user_id = get_user_id(insta_username)
    # checking whether user exist
    if user_id == None:
        print 'User does not exist!'
        exit()
    # making request and accessing obtained json object
    request_url = (base_url + 'users/%s/media/recent/?access_token=%s') % (user_id, access_token)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    # check if the request is successful
    if user_media['meta']['code'] == 200:
        # check if media exist
        if len(user_media['data']):

            return user_media['data'][0]['id']

        else:
            print 'There is no recent post of the user!'
            exit()
    # request unsuccessful
    else:
        print 'Status code other than 200 received!'
        exit()


# function to like a post
def like_a_post(insta_username):
    # calling functions to get recent posts id
    media_id = get_post_id(insta_username)
    # creating the endpoint url
    request_url = (base_url+ 'media/%s/likes') % (media_id)
    # creating required payload
    payload = {"access_token": access_token}
    print 'POST request url : %s' % (request_url)
    # accessing json object
    post_a_like = requests.post(request_url, payload).json()

    # check whether the request is successful
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    # when request is unsuccessful
    else:
        print 'Your like was unsuccessful. Try again!'

# function to post a comment
def post_a_comment(insta_username):
    # getting media id
    media_id = get_post_id(insta_username)
    # getting the comment by user
    comment_text = raw_input("Your comment: ")
    # creating required payload
    payload = {"access_token":access_token, "text" : comment_text}
    # creating endpoint url
    request_url = (base_url + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)
    # accessing json object
    make_comment = requests.post(request_url, payload).json()
    # if request successful
    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    # if request unsuccessful
    else:
        print "Unable to add comment. Try again!"

# function to delete all negative comments from a post
def delete_negative_comment(insta_username):
    # calling the function for getting media id
    media_id=get_post_id(insta_username)
    # setting endpoint url and accessing json object
    request_url = (base_url + 'media/%s/comments/?access_token=%s') % (media_id, access_token)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get( request_url ).json()
    # if request successful
    if comment_info['meta']['info']==200:
        # if comment exists
        if len(comment_info['data']):
            # iterating over all comments
            for x in range(0,len(comment_info['data'])):
                # getting comment id
                comment_id=comment_info['data'][x]['id']
                # getting comment text
                comment_text=comment_info['data'][x]['text']
                # analysing comment by 'TextBlob'
                blob=TextBlob(comment_text,analyzer=NaiveBayesAnalyzer())
                # checking whether sentiments of comment are more negative than positive
                if (blob.sentiment.p_neg>blob.sentiment.p_pos):
                    print "Negative comment:%s" %(comment_text)
                    # setting up endpoint url
                    delete_url = (base_url+ 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, access_token)
                    print  "DELETE request url:%s" %(delete_url)
                    # accessing json object
                    delete_info = requests.delete( delete_url ).json()
                    # check whether request is successful
                    if delete_info['meta']['code']==200:
                        print 'Comment successfully deleted.'
                    # request not successful
                    else:
                        print 'Unable to delete comment.'
                # positive sentiments are greater than negative sentiments!
                else:
                    print "Positive comment:%s" %comment_text
        # no comments found
        else:
            print "there are no comments on this post yet."
    # request unsuccessful
    else:
        print "Status code other than 200 received."


# function to get list of people who liked a post
def get_like_list(insta_username):
    # getting media id
    media_id= get_post_id(insta_username)
    # setting endpoint url and accessing json object received
    request_url=base_url+"media/"+media_id+"/likes?access_token="+access_token
    print "GET request url:%s" %request_url
    like_list= requests.get(request_url).json()
    # if likes accessed successfully
    if like_list['meta']['code']==200:
        # if any data of user liked the post present
        if like_list['data']:
            # displaying people who liked the post
            for x in range(len(like_list['data'])):
                print 'People who liked this post:'
                print '%d. %s' %(x+1, like_list['data'][x]['username'])
        else:
            print 'No one liked this post yet! Be the first one to like.'
    else:
        print 'Status code other than 200 received.'


# function to get list of comments
def get_comment_list(insta_username):
    # getting media id by caliing function
    media_id= get_post_id(insta_username)
    # setting endpoint url and accessing j.son object
    request_url=base_url+'media/'+media_id+'/comments?access_token='+access_token
    comment_list=requests.get(request_url).json()
    # if request is successful
    if comment_list['meta']['code'] ==200:
        # if there exist some comments
        if comment_list['data']:
            # displaying all the comments
            for x in range(len(comment_list['data'])):
                print "%s : %s" %(comment_list['data'][x]['from']['username'], comment_list['data'][x]['text'])
        # if no comment exist
        else:
            print 'There are no comments on this post yet!'
    # if request is unsuccessful
    else:
        print 'Status code other than 200 received.'




# starting the application
def start_bot():

    print '\n'
    print 'Hey! Welcome to instaBot!'
    print 'YESS! You heard it right! "Insta-Bot".. Its way more smarter than you think it is!'
    print 'Try it yourself!!'
    while True:
        print 'Here are your menu options:'
        print "1.Get your own details\n"
        print "2.Get details of a user by username\n"
        print "3.Get your own recent post\n"
        print "4.Get the recent post of a user by username\n"
        print "5.Get a list of people who have liked the recent post of a user\n"
        print "6.Like the recent post of a user\n"
        print "7.Get a list of comments on the recent post of a user\n"
        print "8.Make a comment on the recent post of a user\n"
        print "9.Delete negative comments from the recent post of a user\n"
        print "10.Exit"

        choice = int(raw_input("Enter you choice: "))
        if choice == 1:
            self_info()
        elif choice == 2:
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice == 3:
            get_own_post()
        elif choice == 4:
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice== 5:
           insta_username = raw_input("Enter the username of the user: ")
           get_like_list(insta_username)
        elif choice== 6:
           insta_username = raw_input("Enter the username of the user: ")
           like_a_post(insta_username)
        elif choice== 7:
           insta_username = raw_input("Enter the username of the user: ")
           get_comment_list(insta_username)
        elif choice== 8:
           insta_username = raw_input("Enter the username of the user: ")
           post_a_comment(insta_username)
        elif choice== 9:
           insta_username = raw_input("Enter the username of the user: ")
           delete_negative_comment(insta_username)
        elif choice == 10:
            exit()
        else:
            print "Please choose the correct option!!"

start_bot()



