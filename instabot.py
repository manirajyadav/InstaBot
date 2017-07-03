import requests

api_token ='2067625876.f1530e6.7c216946d050453d8a315f180a7c44b8'
base_url = 'https://api.instagram.com/v1/'

def self_info():

    url_req = base_url+"users/self/?access_token="+api_token
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
  request_url = (base_url+'users/search?q=%s&access_token=%s') % (insta_username,api_token)
  print 'GET request url : %s' % (request_url)
  user_info = requests.get(request_url).json()
self_info()