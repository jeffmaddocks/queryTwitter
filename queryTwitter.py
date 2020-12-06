import pandas as pd
import tweepy
import json
import configparser

import re, string, random

from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk import TweetTokenizer
from nltk import FreqDist, classify, NaiveBayesClassifier

def train_model(stop_words):
    # https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk
    # https://github.com/sdaityari/sentiment.analysis.tutorial/blob/master/Sentiment%20Analysis%20in%20Python%203.ipynb
    # Shaumik Daityari

    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []

    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    all_pos_words = get_all_words(positive_cleaned_tokens_list)

    freq_dist_pos = FreqDist(all_pos_words)
    print(freq_dist_pos.most_common(10))

    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(tweet_dict, "Positive")
                         for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Negative")
                         for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset

    random.shuffle(dataset)

    train_data = dataset[:7000]
    test_data = dataset[7000:]

    classifier = NaiveBayesClassifier.train(train_data)

    print("Accuracy is:", classify.accuracy(classifier, test_data))

    print(classifier.show_most_informative_features(10))

    return classifier

def remove_noise(tweet_tokens, stop_words):
    # print(f'noisy: {tweet_tokens}')
    addnl_noise = ['…', '“', '”']
    cleaned_tokens = []
    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*(),]|'
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        skip = 0 # skip provides additional conditions for the token to be ignored
        for x in addnl_noise: # check for additional noisy characters which should not be tokens
            if x == token: skip = 1

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
            # skip = 1 # we're not processing anything other than nouns and verbs

        if skip == 1: continue # unless this token was skipped, continue processing
        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    # print(f'quiet: {cleaned_tokens}')
    return cleaned_tokens

def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

def queryTwitter(df): # the initial df is the csv containing the twitter handles to query
    stop_words = stopwords.words('english')
    classifier = train_model(stop_words)
    df_final = pd.DataFrame() # the final df will hold all tweets across all handles
    for i in df.iterrows(): # iterate thru the handles
        print('processing: '+ i[1][0])
        df2 = get_tweets(i[1][0]+' -filter:retweets', i[1][1]) # create a new df to hold the tweets for each handle
        df2.insert(1,'search_handle', i[1][0])
        df2 = df2.astype({'created_at': str})

        # taking out dataframe insert and will try assign instead
        # df2.insert(len(df2.columns), 'tokens', '[]')
        df2 = df2.assign(tokens = '[]')
        df2 = df2.assign(sentiment = '')

        df2 = clean_tweets(classifier, df2, stop_words)

        df_final = df_final.append(df2, ignore_index=True)

    return df_final

def get_output_schema():
    return pd.DataFrame({
        'id': prep_string(),
        'author_name': prep_string(),
        'author_handle': prep_string(),
        'created_at': prep_string(),
        'search_handle': prep_string(),
        'tweet_text': prep_string(),
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
        # print('    ' + tweet.text)
        outtweets = [tweet.id_str, tweet.author.name, '@'+tweet.author.screen_name, tweet.created_at, tweet.text, tweet.retweet_count, tweet.favorite_count]
        alltweets.append(outtweets)

    df = pd.DataFrame(data=alltweets, columns=['id','author_name', 'author_handle', 'created_at','tweet_text','retweet_count','favorite_count'])
    return df

def clean_tweets(classifier, df, stop_words):
    tknzr = TweetTokenizer()
    for i in df.iterrows():
        # print('tweet: '+df['tweet_text'][i[0]])
        tokens = tknzr.tokenize(i[1]['tweet_text']) # using NLTK tweet tokenizer

        custom_tokens = remove_noise(tokens, stop_words)
        df['tokens'][i[0]] =  custom_tokens # need to fix this warning later
        # SettingWithCopyWarning: 
        # A value is trying to be set on a copy of a slice from a DataFrame

        # See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy

        # grabs the current row: df.loc[i[0]]
        # grabs the tokens column of the current row: df.loc[i[0]]['tokens']
        # this is a python object of type array: df.loc[df.id == i[0], 'tokens']

        # df.loc[df.id == i[0], 'tokens'] = remove_noise(tokens, stop_words)

        score = classifier.classify(dict([token, True] for token in custom_tokens))
        df['sentiment'][i[0]] = score

    return df

if __name__ == "__main__":
    import pandas as pd
    df = pd.read_csv('twitter_query.csv')
    df2 = queryTwitter(df)
    df2.to_json('tweets.json', orient='table')
    df2.to_excel('tweets.xlsx')
