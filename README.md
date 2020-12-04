# queryTwitter
Uses [TabPy](https://github.com/tableau/TabPy) to pull twitter mentions (posts that mention a twitter handle) into Tableau Prep. The result includes:
- id
- search_handle
- author_name
- author_handle
- created_at
- tweet_text
- retweet_count
- favorite_count

Future features include [insert safe harbor state here] ... [jk this is all free and no warranty or support is implied]:
- pulling a user feed (posts made by a twitter handle) is a different exercise that may be added in a future version
- word tokenization with NLTK will be released shortly
- sentiment analysis would be neat

## Setup
1. Setting up a virtual environment is a great idea! You may have TabPy configured already and simply need to install the requirements in step 2, so jump down there now, silly. You may live dangerously and decide not to use a virtual environment; you plan to install packages as error messages pop up and so you've already skipped to step 3, you rebel!

    The rest of us may want to [at least see all the different ways TabPy can be setup](https://github.com/tableau/TabPy). Let's get started using virtualenv in bash:
    ```
    mkdir env
    virtualenv -p python3 ./env
    source env/bin/activate
    ```
    There's even [instructions for Windows](https://programwithus.com/learn/python/pip-virtualenv-windows).

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
    - press the Browse button and select 'queryTwitter.py'
    - type 'queryTwitter' into the Function Name

7. Enjoy!
