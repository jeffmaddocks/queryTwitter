# queryTwitter
Allows TabPy to easily query twitter handles

Install required packages by running: 
```
pip install -r 'requirements.txt'
```
Create a text file 'twitterkey.ini' as follows, [updating with your keys, secrets and tokens from Twitter](https://developer.twitter.com/en/docs/authentication/oauth-1-0a):
```
[Consume]
consumer_key    = __your_consumer_key_here__
consumer_secret = __your_consumer_secret_here__

[Access]
access_token  = __your_access_token_here__
access_secret = __your_access_secret_here__
```
modify twitter_qery.csv with the twitter handles you want to query, and how many records to request from the API
