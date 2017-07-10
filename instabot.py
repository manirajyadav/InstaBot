# written by Mani Raj Yadav
# importing required library
import requests
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from termcolor import colored


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
        # whether user is present
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
    print 'GET request url : %s' % request_url
    user_id = requests.get(request_url).json()
    # checking whether the request is successful
    if user_id['meta']['code'] == 200:
        # checking whether the user exist
        if len(user_id['data']):
            return user_id['data'][0]['id']
        else:
            return None
    # request unsuccessful
    else:
        print "Status code other than 200 received."


# function for getting info of user by its instagram username
def get_user_info(insta_username):
    # calling function to get user-id
    user_id= get_user_id(insta_username)

    # if user does not exist
    if user_id == None:
        print "User with the given name does not exist.You are being sent back to the HOME!"
        start_bot()
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

# function to get own posts
def get_own_post():
    # setting up endpoint url and accessing json object
    request_url = (base_url + 'users/self/media/recent/?access_token=%s') % (access_token)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()
    # if request is successful
    if own_media['meta']['code'] == 200:
        # if some posts exist
        if len(own_media['data']):
            c= True
            # loop to choose any post other than latest
            while c:
                answer= raw_input('Do you want to get the latest post? Reply: Y/N')
                if answer.upper()== 'Y':
                    x=0
                    c= False
                elif answer.upper()=='N':
                    print 'choose from the following\n'
                    print """2. Second last post\n3. Third last post..and so on.."""
                    x= raw_input()
                    if int(x) < len(own_media['data']) and x.isdigit():
                        x= int(x)
                        c= False
                    else:
                        print 'You did not choose appropriate option. Try again!'
                else:
                    print 'Press only y or n!!'
                    c= True

            image_name = own_media['data'][x]['id'] + '.jpeg'
            image_url = own_media['data'][x]['images']['standard_resolution']['url']
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
        start_bot()
    # making request and accessing obtained json object
    request_url = (base_url + 'users/%s/media/recent/?access_token=%s') % (user_id, access_token)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get( request_url ).json()
    # if request is successful
    if user_media['meta']['code'] == 200:
        # if posts exist
        if len( user_media['data'] ):
            c = True
            while c:
                answer = raw_input( 'Do you want to get the latest post?Reply: Y/N' )
                if answer.upper() == 'Y':
                    x = 0
                    c = False
                elif answer.upper() == 'N':
                    print 'choose from the following\n'
                    print """2. Second last post\n3. Third last post..and so on.."""
                    x = raw_input()
                    if int( x ) < len(user_media['data'] ) and x.isdigit():
                        x = int( x )
                        c = False
                    else:
                        print 'You did not choose appropriate option. Try again!'
                else:
                    print 'Press only y or n!!'
                    c = True

            image_name = user_media['data'][x]['id'] + '.jpeg'
            image_url = user_media['data'][x]['images']['standard_resolution']['url']
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
        print 'User does not exist!\n You are being sent back to the HOME!!'
        start_bot()
    # making request and accessing obtained json object
    request_url = (base_url + 'users/%s/media/recent/?access_token=%s') % (user_id, access_token)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    # check if the request is successful
    if user_media['meta']['code'] == 200:
        # check if media exist
        if len(user_media['data']):
            c = True
            while c:
                answer = raw_input( 'Do you want to get the latest post?Reply: Y/N' )
                if answer.upper() == 'Y':
                    x = 0
                    c = False
                elif answer.upper() == 'N':
                    print 'choose from the following\n'
                    print """2. Second last post\n3. Third last post..and so on.."""
                    x = raw_input()
                    if int( x ) < len( user_media['data'] ) and x.isdigit():
                        x = int( x )
                        c = False
                    else:
                        print 'You did not choose appropriate option. Try again!'
                else:
                    print 'Press only y or n!!'
                    c = True

            return user_media['data'][x]['id']

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
        print colored('Like was successful!', 'red')
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
        print colored('Successfully added a new comment!','blue')
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
            ans= raw_input('Do you want to delete comments containing a specific words? Reply Y/N')
            if ans.upper()=='Y':
                del_word= raw_input('Enter the Word!!')
                for x in range( 0, len( comment_info['data'] ) ):
                    # getting comment id
                    comment_id = comment_info['data'][x]['id']
                    # getting comment text
                    comment_text = comment_info['data'][x]['text']
                    if del_word in comment_text:
                        print "Comment containing the given word:"+ colored(comment_text, 'red')
                        # setting up endpoint url
                        delete_url = (base_url + 'media/%s/comments/%s/?access_token=%s') % (
                        media_id, comment_id, access_token)
                        print  "DELETE request url:%s" % (delete_url)
                        # accessing json object
                        delete_info = requests.delete( delete_url ).json()
                        # check whether request is successful
                        if delete_info['meta']['code'] == 200:
                            print 'Comment successfully deleted.'
                        # request not successful
                        else:
                            print 'Unable to delete comment.'
            else:
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
    media_id = get_post_id(insta_username)
    # setting endpoint url and accessing json object received
    request_url=(base_url+"media/%s/likes?access_token=%s") %(media_id,access_token)
    print "GET request url : %s" %(request_url)
    like_list= requests.get(request_url).json()
    # if likes accessed successfully
    if like_list['meta']['code']==200:
        # if any data of user liked the post present
        if len(like_list['data']):
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
    request_url=(base_url+'media/%s/comments?access_token=%s') %(media_id,access_token)
    print 'GET request url : %s' %(request_url)
    comment_list=requests.get(request_url).json()
    # if request is successful
    if comment_list['meta']['code'] ==200:
        # if there exist some comments
        if len(comment_list['data']):
            # displaying all the comments
            for x in range(len(comment_list['data'])):
                print "%s : %s" %(comment_list['data'][x]['from']['username'], comment_list['data'][x]['text'])
        # if no comment exist
        else:
            print 'There are no comments on this post yet!'
    # if request is unsuccessful
    else:
        print 'Status code other than 200 received.'


# function to list of recent media liked by the owner of the access_token
def list_own_like():
    # setting up endpoint url and accessing json object
    request_url= base_url+ 'users/self/media/liked?access_token=' + access_token
    print 'GET request url: %s' %(request_url)
    own_likes = requests.get(request_url).json()
    if own_likes['meta']['code']==200:
        print 'Posts liked by the user are:'
        for x in range(len(own_likes['data'])):
            print colored('Post-Id:%s\n%s from %s.\n','blue') %(own_likes['data'][x]['id'],own_likes['data'][x]['type'],own_likes['data'][x]['user']['full_name'],)


# function to get a post with least likes
def least_like(insta_username):
    # calling function to get user-id
    user_id = get_user_id( insta_username )
    # if user doesnt exit
    if user_id == None:
        print 'User does not exist!'
        start_bot()
    # making request and accessing obtained json object
    request_url = (base_url + 'users/%s/media/recent/?access_token=%s') % (user_id, access_token)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get( request_url ).json()
    # if request is successful
    if user_media['meta']['code'] == 200:
        # if posts exist
        if len(user_media['data']):
            least=user_media['data'][0]['likes']['count']
            c=0
            for x in range (1,len(user_media['data'])):
                likes= user_media['data'][x]['likes']['count']
                if likes < least:
                    least = likes
                    c=x

            print "\nPost with least likes is:\nId=%s\nlikes=%s" %(user_media['data'][c]['id'], least)
            print "Caption:%s" %(user_media['data'][c]['caption']['text'])
            image_name = user_media['data'][c]['id'] + '.jpeg'
            image_url = user_media['data'][c]['images']['standard_resolution']['url']
            # downloading the post
            urllib.urlretrieve( image_url, image_name )
            print 'And the post has been downloaded!!'

# search for a post with a particular tag
def search_post_via_tag(insta_username, search_tag):
    # calling function to get user-id
    user_id = get_user_id( insta_username )
    # if user doesnt exit
    if user_id == None:
        print 'User does not exist!'
        start_bot()
    # making request and accessing obtained json object
    request_url = (base_url + 'users/%s/media/recent/?access_token=%s') % (user_id, access_token)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get( request_url ).json()
    # if request is successful
    if user_media['meta']['code'] == 200:
        # if posts exist
        if len( user_media['data'] ):
            id = []
            for x in range(len(user_media['data'])):
                if search_tag in user_media['data'][x]['tags']:
                    id.append(user_media['data'][x]['id'])

            if len(id):
                for y in id:
                    request_url= base_url+ "media/%s?access_token=%s" %(y,access_token)
                    print "GET request url:%s" %(request_url)
                    tag_media = requests.get(request_url).json()

                    print 'Tag: '+ colored('#','blue')+colored(search_tag,'blue')
                    print '\nPost-Id:' + colored(y,'blue')
                    print '\nCaption:%s' % (tag_media['data']['caption']['text'])
                    image_name = y+'.jpeg'
                    image_url = tag_media['data']['images']['standard_resolution']['url']
                    # downloading the post
                    urllib.urlretrieve( image_url, image_name )
                    print '\nThe post has been downloaded!!'
            else:
                print "No media with '%s' tag found!!" %(search_tag)
        else:
            print "No media exist!!"
    else:
        print 'Status code other than 200 received'



# starting the application
def start_bot():

    print '\n'
    print 'Hey! Welcome to instaBot!'
    print 'YESS! You heard it right! "Insta-Bot".. Its way more smarter than you think it is!'
    print 'Try it yourself!!'
    while True:
        print '\n'
        print 'Here are your menu options:\n'
        print "1.Get your own details\n"
        print "2.Get details of a user by username\n"
        print "3.Get your own recent post\n"
        print "4.Get the recent post of a user by username\n"
        print "5.Get a list of people who have liked the recent post of a user\n"
        print "6.Like the recent post of a user\n"
        print "7.Get a list of comments on the recent post of a user\n"
        print "8.Make a comment on the recent post of a user\n"
        print "9.Delete negative comments from the recent post of a user\n"
        print "10.Get list of posts liked by the User.\n"
        print "11.Get the post with least like.\n"
        print "12.Search a post with a particular tag."
        print "13.Exit.\n"


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
            list_own_like()
        elif choice== 11:
            insta_username = raw_input( "Enter the username of the user: " )
            least_like(insta_username)
        elif choice== 12:
            insta_username = raw_input( "Enter the username of the user: " )
            search_tag = raw_input("Enter the tag you are looking for.")
            search_post_via_tag(insta_username,search_tag)
        elif choice == 13:
            exit()

        else:
            print "Please choose the correct option!!"

start_bot()



