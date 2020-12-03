import pandas as pd
import tweepy
import json
import configparser

def queryTwitter(df):
    df_final = pd.DataFrame()
    for i in df.iterrows():
        print('processing: '+ i[1][0])
        df2 = get_tweets(i[1][0]+' -filter:retweets', i[1][1])
        df2.insert(1,'search_handle', i[1][0])
        df2 = df2.astype({'created_at': str})
        df_final = df_final.append(df2, ignore_index=True)

    return df_final

def get_output_schema():
    return pd.DataFrame({
        'id': prep_string(),
        'author_name': prep_string(),
        'author_handle': prep_string(),
        'created_at': prep_string(),
        'search_handle': prep_string(),
        'text': prep_string(),
        'retweet_count': prep_int(),
        'favorite_count': prep_int()
    })

def get_tweets(string_serch, int_returnrows):
    # http://docs.tweepy.org/en/v3.9.0/getting_started.html
    config = configparser.ConfigParser()
    config.read('twitterkeys.ini')
    # Consume:
    consumer_key    = config['Consume']['consumer_key']
    consumer_secret = config['Consume']['consumer_secret']
    # Access:
    access_token  = config['Access']['access_token']
    access_secret = config['Access']['access_secret']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    alltweets = []  
    for tweet in tweepy.Cursor(api.search, q=string_serch).items(int_returnrows):
        print('    ' + tweet.text)
        outtweets = [tweet.id_str, tweet.author.name, '@'+tweet.author.screen_name, tweet.created_at, tweet.text, tweet.retweet_count, tweet.favorite_count]
        alltweets.append(outtweets)

    df = pd.DataFrame(data=alltweets, columns=['id','author_name', 'author_handle', 'created_at','text','retweet_count','favorite_count'])
    return df

if __name__ == "__main__":
    import pandas as pd
    df = pd.read_csv('twitter_query.csv')
    df2 = queryTwitter(df)
    df2.to_json('tweets.json', orient='table')
    df2.to_excel('tweets.xlsx')
