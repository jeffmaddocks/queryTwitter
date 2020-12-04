# queryTwitter
Uses TabPy to pull twitter feeds into Tableau Prep.

1. Setting up a virtual environment is a great idea! Here's an example using virtualenv in bash:
```
mkdir env && cd env
virtualenv -p python3 .
cd ..
source env/bin/actviate
```

2. Install required packages by running pip from the terminal: 
```
pip install -r 'requirements.txt'
```
3. Create a text file 'twitterkey.ini' as follows, [updating with your keys, secrets and tokens from Twitter](https://developer.twitter.com/en/docs/authentication/oauth-1-0a):
```
[Consume]
consumer_key    = __your_consumer_key_here__
consumer_secret = __your_consumer_secret_here__

[Access]
access_token  = __your_access_token_here__
access_secret = __your_access_secret_here__
```
4. Modify twitter_query.csv with the twitter handles you want to query, and how many records to request from the API. Note that multiple handles can be queried at once by adding a new line to the file.

5. Start TabPy, note that TabPy listens on port 9004:
```
tabpy
```

6. Open Tableau Prep Builder and ...
    - add twitter_query.csv as a data source
    - add a script step
    - choose Tableau Python (TabPy) Server
    - press the Connect To Server button
    - your TabPy service may be running locally, so enter localhost in the Server box
    - set the port to 9004
    - leave all other fields empty and press the Sign In button
    - press the Browse button and select queryTwitter.py
    - type 'queryTwitter' inot the Function Name

7. Enjoy!
