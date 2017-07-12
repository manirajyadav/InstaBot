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
            print '\nUsername: %s' % (user_info['data']['username'])
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
    user_id = get_user_id(insta_username)

    # if user does not exist
    if user_id == None:
        print "User with the given name does not exist.You are being sent back to the HOME!"
        start_bot()
    # making request and accessing obtained json object
    request_url = (base_url+'users/%s?access_token=%s') % (user_id, access_token)
    print 'GET request url: %s' % request_url
    user_info = requests.get(request_url).json()

    # if request is successful
    if user_info['meta']['code'] == 200:
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
    request_url = (base_url + 'users/self/media/recent/?access_token=%s') % access_token
    print 'GET request url : %s' % request_url
    own_media = requests.get(request_url).json()
    # if request is successful
    if own_media['meta']['code'] == 200:
        # if some posts exist
        if len(own_media['data']):
            c = True
            # loop to avoid crashes on invalid insertion
            while c:
                # asking for post other than the latest
                answer= raw_input('Do you want to get the latest post? Reply: Y/N')
                if answer.upper() == 'Y':
                    x =1
                    c = False
                # letting user choose the post
                elif answer.upper() == 'N':
                    print 'choose from the following\n'
                    print "2. Second last post\n3. Third last post..\nand so on.."
                    x = raw_input()
                    # checking whether user entered valid post no.
                    if x.isdigit():
                        if x < len(own_media['data']):
                            x = int(x)
                            c = False
                        else:
                            print 'This post does not exist!'
                    # when invalid post no.
                    else:
                        print 'You did not choose appropriate option. Try again!'
                # option other than y and n entered
                else:
                    print 'Press only y or n!!'
                    c = True
            # downloading the post

            if own_media['data'][x-1]['type' ]== 'image':
                post_name = own_media['data'][x-1]['id'] + '.jpeg'
                post_url = own_media['data'][x-1]['images']['standard_resolution']['url']
                urllib.urlretrieve(post_url, post_name)
                print 'Your image has been downloaded!'

            else:
                post_name = own_media['data'][x-1]['id'] + '.mp4'
                post_url = own_media['data'][x-1]['videos']['standard_resolution']['url']
                urllib.urlretrieve(post_url, post_name)
                print 'Your video has been downloaded!'
        # if no post exist
        else:
            print 'Post does not exist!'
    # request unsuccessful
    else:
        print 'Status code other than 200 received!'


# function to access user posts and downloading
def get_user_post(insta_username):
    # calling function to get user-id
    user_id = get_user_id(insta_username)
    # if user doesnt exit
    if user_id == None:
        print 'User does not exist!'
        start_bot()
    # making request and accessing obtained json object
    request_url = (base_url + 'users/%s/media/recent/?access_token=%s') % (user_id, access_token)
    print 'GET request url : %s' % request_url
    user_media = requests.get(request_url).json()
    # if request is successful
    if user_media['meta']['code'] == 200:
        # if posts exist
        if len(user_media['data']):
            c = True
            # loop for avoiding crashes on entering wrong choice
            while c:
                # if user wants any post other than the latest one
                answer = raw_input( 'Do you want to get the latest post? Reply: Y/N' )
                if answer.upper() == 'Y':
                    x = 1
                    c = False
                elif answer.upper() == 'N':
                    print 'Choose from the following\n'
                    print "2. Second last post\n3. Third last post..\nand so on.."
                    x = raw_input()
                    if x.isdigit():
                        # checking whether user's choice does exist
                        if x <= len(user_media['data']) :
                            x = int(x)
                            c = False
                        else:
                            print 'This post does not Exist!!'
                    # when user chose a no. more than number of posts
                    else:
                        print 'You did not choose appropriate option. Try again!'
                # when user entered something except y and n
                else:
                    print 'Press only y or n!!'
                    c = True
            # downloading the post

            if user_media['data'][x-1]['type']== 'image':
                post_name = user_media['data'][x-1]['id'] + '.jpeg'
                post_url = user_media['data'][x-1]['images']['standard_resolution']['url']
                urllib.urlretrieve(post_url, post_name)
                print 'Your image has been downloaded!'

            else:
                post_name = user_media['data'][x-1]['id'] + '.mp4'
                post_url = user_media['data'][x-1]['videos']['standard_resolution']['url']
                urllib.urlretrieve(post_url, post_name)
                print 'Your video has been downloaded!'
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
    print 'GET request url : %s' % request_url
    user_media = requests.get(request_url).json()

    # check if the request is successful
    if user_media['meta']['code'] == 200:
        # check if media exist
        if len(user_media['data']):
            c = True
            # not letting application to terminate on a wrong choice
            while c:
                # in case user wants some other post than the latest one!
                answer = raw_input( 'Do you want to get the latest post? Reply: Y/N' )
                if answer.upper() == 'Y':
                    x = 1
                    c = False
                elif answer.upper() == 'N':
                    print 'Choose from the following\n'
                    print "2. Second last post\n3. Third last post..\nand so on.."
                    # taking input for post choice
                    x = raw_input()
                    # checking whether we have posts of users's choice
                    if x.isdigit():
                        # checking whether user's choice does exist
                        if x < len(user_media['data']):
                            x = int(x)
                            c = False
                        else:
                            print 'This post does not Exist!!'
                    else:
                        print 'You did not choose appropriate option. Try again!'
                else:
                    print 'Press only y or n!!'
                    c = True
            # returning media id
            return user_media['data'][x-1]['id']
        # no recent post of user
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
    request_url = (base_url + 'media/%s/likes') % media_id
    # creating required payload
    payload = {"access_token": access_token}
    print 'POST request url : %s' % request_url
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

    while True:
        # getting the comment by user
        comment_text = raw_input( "Your comment: " )
        if len(comment_text)>0 and comment_text.isspace()==False:
            # creating required payload
            payload = {"access_token":access_token, "text" : comment_text}
            # creating endpoint url
            request_url = (base_url + 'media/%s/comments') % (media_id)
            print 'POST request url : %s' % (request_url)
            # accessing json object
            make_comment = requests.post(request_url, payload).json()
            # if request successful
            if make_comment['meta']['code'] == 200:
                print colored('\nSuccessfully added a new comment!','blue')
            # if request unsuccessful
            else:
                print "Unable to add comment. Try again!"
            break
        else:
            print 'Cannot post an empty comment! Try again!'

# function to delete all negative comments from a post
def delete_negative_comment(insta_username):
    # calling the function for getting media id
    media_id=get_post_id(insta_username)
    # setting endpoint url and accessing json object
    request_url = (base_url + 'media/%s/comments/?access_token=%s') % (media_id, access_token)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get( request_url ).json()
    # if request successful
    if comment_info['meta']['code']==200:
        # if comment exists
        if len(comment_info['data']):
            ans= raw_input('Do you want to delete comments containing a specific words? Reply Y/N')
            if ans.upper()=='Y':
                while True:
                    del_word= raw_input('Enter the Word!!')
                    if len(del_word)>0 and del_word.isspace()== False:
                        for x in range( 0, len( comment_info['data'] ) ):
                            # getting comment id
                            comment_id = comment_info['data'][x]['id']
                            # getting comment text
                            comment_text = comment_info['data'][x]['text']
                            if del_word in comment_text:
                                print "Comment containing the given word: "+ colored(comment_text, 'red')
                                # setting up endpoint url
                                delete_url = (base_url + 'media/%s/comments/%s/?access_token=%s') % (
                                media_id, comment_id, access_token)
                                print  "DELETE request url:%s" % (delete_url)
                                # accessing json object
                                delete_info = requests.delete( delete_url ).json()
                                # check whether request is successful
                                if delete_info['meta']['code'] == 200:
                                    print '\nComment successfully deleted.'

                                # request not successful
                                else:
                                    print 'Unable to delete comment.'

                            else:
                                print 'There are no comments containing this word!'
                        break

                    else:
                        print 'You did not enter any word to search and delete comment for! Try again!'
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
                        print "Negative comment:"+colored(comment_text,'red')
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
                        print "Positive comment:"+colored(comment_text, 'green')
        # no comments found
        else:
            print "There are no comments on this post yet."
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

            print colored('\nFrom:','blue')+own_likes['data'][x]['user']['full_name']+colored('\nType:','blue')+own_likes['data'][x]['type']
            print colored('Post Id:','blue')+own_likes['data'][x]['id']
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
            print '\nAnd the post has been downloaded!!'

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
            # searching for the given hashtag and saving the post id
            for x in range(len(user_media['data'])):
                if search_tag in user_media['data'][x]['tags']:
                    id.append(user_media['data'][x]['id'])
            # if there was any post with given hashtag
            if len(id):
                # iterating through all the ids
                for y in id:
                    # setting up endpoint url and accessing json object
                    request_url= base_url+ "media/%s?access_token=%s" %(y,access_token)
                    print "GET request url:%s" %(request_url)
                    tag_media = requests.get(request_url).json()
                    # showing post with given hashtag and also downloading
                    print '\nTag: '+ colored('#','blue')+colored(search_tag,'blue')
                    print '\nPost-Id:' + colored(y,'blue')
                    print '\nCaption:%s' % (tag_media['data']['caption']['text'])
                    image_name = y+'.jpeg'
                    image_url = tag_media['data']['images']['standard_resolution']['url']
                    # downloading the post
                    urllib.urlretrieve( image_url, image_name )
                    print '\nThe post has been downloaded!!'
            # no media with given hashtag found
            else:
                print "No media with #"+colored(search_tag,'blue')+" tag found!!"
        # user doesnt have any media yet
        else:
            print "User has no media yet!!"
    # request unsuccessful
    else:
        print 'Status code other than 200 received'



# starting the application
def start_bot():
    # starting with the application and greeting
    print '\n'
    print 'Hey! Welcome to instaBot!'
    print 'YESS! You heard it right! "Insta-Bot".. Its way more smarter than you think it is!'
    print 'Try it yourself!!'
    while True:
        print '\n'
        # displaying menu
        print 'Here are your menu options:\n'
        print "1.Get your own details\n"
        print "2.Get details of a user by username\n"
        print "3.Download your own recent post\n"
        print "4.Download the recent post of a user by username\n"
        print "5.Get a list of people who have liked the recent post of a user\n"
        print "6.Like the recent post of a user\n"
        print "7.Get a list of comments on the recent post of a user\n"
        print "8.Make a comment on the recent post of a user\n"
        print "9.Delete negative comments from the recent post of a user\n"
        print "10.Get list of posts liked by the User.\n"
        print "11.Get the post with least like.\n"
        print "12.Search a post with a particular tag.\n"
        print "13.Exit.\n"

        # getting the choice from user to proceed with the app
        choice = raw_input("Enter you choice: ")
        if choice == '1':
            self_info()
        elif choice == '2':

            while True:
                insta_username = raw_input("Enter the username of the user: ")
                if len(insta_username)>0 and insta_username.isspace()==False:
                    get_user_info(insta_username)
                    break
                else:
                    print 'Enter a valid name!!'
        elif choice == '3':
            get_own_post()

        elif choice == '4':

            while True:
                insta_username = raw_input("Enter the username of the user: ")
                if len(insta_username)>0 and insta_username.isspace()==False:
                    get_user_post(insta_username)
                    break
                else:
                    print 'Enter a valid name!!'
        elif choice== '5':

            while True:
                insta_username = raw_input( "Enter the username of the user: " )
                if len( insta_username ) > 0 and insta_username.isspace() == False:
                    get_like_list(insta_username)
                    break
                else:
                    print 'Enter a valid name!!'

        elif choice== '6':

            while True:
                insta_username = raw_input( "Enter the username of the user: " )
                if len( insta_username ) > 0 and insta_username.isspace() == False:
                    like_a_post( insta_username )
                    break
                else:
                    print 'Enter a valid name!!'

        elif choice== '7':

            while True:
                insta_username = raw_input( "Enter the username of the user: " )
                if len( insta_username ) > 0 and insta_username.isspace() == False:
                    get_comment_list( insta_username )
                    break
                else:
                    print 'Enter a valid name!!'

        elif choice== '8':

            while True:
                insta_username = raw_input( "Enter the username of the user: " )
                if len( insta_username ) > 0 and insta_username.isspace() == False:
                    post_a_comment( insta_username )
                    break
                else:
                    print 'Enter a valid name!!'

        elif choice== '9':

            while True:
                insta_username = raw_input( "Enter the username of the user: " )
                if len( insta_username ) > 0 and insta_username.isspace() == False:
                    delete_negative_comment( insta_username )
                    break
                else:
                    print 'Enter a valid name!!'

        elif choice == '10':
            list_own_like()

        elif choice== '11':

            while True:
                insta_username = raw_input( "Enter the username of the user: " )
                if len( insta_username ) > 0 and insta_username.isspace() == False:
                    least_like( insta_username )
                    break
                else:
                    print 'Enter a valid name!!'

        elif choice== '12':

            while True:
                insta_username = raw_input( "Enter the username of the user:\n" )
                if len( insta_username ) > 0 and insta_username.isspace() == False:
                    while True:
                        search_tag = raw_input("Enter the tag you are looking for.")
                        if len(search_tag)>0 and search_tag.isspace()==False:
                            search_post_via_tag( insta_username, search_tag )
                            break
                        else:
                            print 'You did not enter any tag.Try again!!\n'
                else:
                    print 'Enter a valid name!!\n'

        elif choice == '13':
            exit()
        # wrong choice
        else:
            print "Please choose the correct option!!"

# starting the app by calling the function
start_bot()



