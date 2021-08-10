import os
import tweepy
from dotenv import load_dotenv
import pandas as pd
import stopwords
import nltk
from nltk.stem import WordNetLemmatizer
import pickle

nltk.download('stopwords')
nltk.download('wordnet')

stop = set(stopwords.get_stopwords('english'))
stop.update(set(nltk.corpus.stopwords.words('english')))
stopword = list(stop)

wordLemm = WordNetLemmatizer()

def create_connection():
    '''
    Returns twitter api connection objects.
    '''
    try:
        load_dotenv()
        auth = tweepy.OAuthHandler(os.getenv('api_key'), os.getenv('api_secret_key'))
        auth.set_access_token(os.getenv('access_token'), os.getenv('access_token_secret'))
        return tweepy.API(auth)
    except Exception as e:
        return False

def fetch_tweets(query):
    '''
    Returns the search result in status object.
    '''
    query = query.strip()
    query = query + ' -filter:retweets'
    try:
        return tweepy.Cursor(create_connection().search, q=query, lang='en', tweet_mode="extended")
    except:
        return False

def pre_process(textlist):
    '''
    This function takes a string input and returns the string in lowercase with
    removal of username, no punctuation, eliminated stopwords.
    '''
    processedtext = []
    for text in textlist:
        nopunct = ' '.join([(''.join([char for char in word if char.isalpha() or char == '-' or char == '_' or char == '/' or char == '.']))
                            for word in text.lower().replace('\n', ' ').split() if not word.startswith('@') if not word.startswith('http') if word not in stopword])
        for punct in ['-', '_', '/', '.']:
            nopunct = nopunct.replace(punct, ' ')
        nopunct = ' '.join([i for i in nopunct.strip().split() if i not in stopword])
        text = ''
        for word in nopunct.split():
            if len(word) > 2:
                word = wordLemm.lemmatize(word)
                text += (word+' ')
        processedtext.append(text.strip())
    return processedtext

def search_tweet(query):
    '''
    Return Bool value True and Dataframe with search result for the recieved query.
    '''
    tweets = fetch_tweets(query)
    # If cursor fails function will return False
    if tweets != False:
        tweet_dict = {'date':[], 'tweets':[], 'likes':[], 'retweets':[], 'author':[], 'location':[]}
        for tweet in tweets.items(300):
            tweet_dict['date'].append(tweet.created_at)
            tweet_dict['tweets'].append(tweet.full_text)
            tweet_dict['likes'].append(tweet.favorite_count)
            tweet_dict['retweets'].append(tweet.retweet_count)
            tweet_dict['author'].append(tweet.author.name)
            tweet_dict['location'].append(tweet.author.location)
        df = pd.DataFrame(data = tweet_dict)
        # if nothing found in result return false
        if df.shape[0] == 0:
            return (False, "No Data Found")
        df['date'] = df['date'].dt.date
        return (True, df)
    else:
        return (False, "Cursor Failure!")

def load_vectorizer():
    '''
    Returns vectorizer.
    '''
    # Loads vectorizer
    file = open('./app/server/models/tfidf-ngram-(1,2).pickle', 'rb')
    vectorizer = pickle.load(file)
    file.close()
    print("Vectorizer loaded successfully.")
    return vectorizer

def load_model():
    '''
    Returns model.
    '''
    # Loads the model
    file = open('./app/server/models/Sentiment-LR.pickle', 'rb')
    model = pickle.load(file)
    file.close()
    print("Model loaded successfully.")
    return model

def predict(search):
    recieved_tweets = search_tweet(search)
    if recieved_tweets[0] == False:
        return None
    recieved_tweets = recieved_tweets[1]
    try:
        textdata = load_vectorizer().transform(pre_process(recieved_tweets['tweets']))
        recieved_tweets['sentiment'] = load_model().predict(textdata)

        recieved_tweets['sentiment'].replace({0:"Negative",4:"Positive"}, inplace=True)
        
        tweet_list = []
        for date, text, location, sentiment in zip(list(recieved_tweets['date']),list(recieved_tweets['tweets']),list(recieved_tweets['location']),list(recieved_tweets['sentiment'])):
            tweet_list.append({'date':date, 'text':text, 'location':location, 'sentiment':sentiment})
            
        total_data = len(recieved_tweets)
        total_days = recieved_tweets['date'].nunique()
        pos = len(recieved_tweets[recieved_tweets['sentiment']=='Positive'])
        neg = len(recieved_tweets[recieved_tweets['sentiment']=='Negative'])
        pos_per = (pos/total_data)*100
        return  {"pos": pos, "neg": neg, "pos_per": f'{pos_per:.2f}', "neg_per": f'{(100-pos_per):.2f}', "days": total_days, "length": total_data, "data" : tweet_list}
    except:
        return False
