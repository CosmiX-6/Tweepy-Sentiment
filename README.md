# Tweepy-Sentiment

### Application view :
[Visit Tweepy Sentiment](https://c6-tweepy-sentiment.herokuapp.com "Tweepy Sentiment's Homepage")

![alt text](https://github.com/CosmiX-6/Tweepy-Sentiment/blob/master/app/server/static/images/cover.png "Preview")


### Content
```
├── .env
├── Procfile 
├── app
│   ├── __init__.py
│   ├── main.py
│   └── server
│       ├── __init__.py
│       ├── app.py
│       ├── models
│       │   ├── __init__.py
│       │   ├── models.py
│       │   ├── Sentiment-LR.pickle
│       │   └── tfidf-ngram-(1,2).pickle
│       ├── routes
│       │   ├── __init__.py
│       │   └── gettweets.py
│       ├── sentiment
│       │   ├── __init__.py
│       │   └── sentiment_analyzer.py
│       ├── static
│       │   ├── css
│       │   ├── images
│       │   └── js
│       └── templates
├── README.md
└── requirements.txt
```


### Introduction
   Twitter is a popular social networking site where users post and interact with messages called "tweets". It serves as a means for individuals to express their thoughts or feelings on various topics. Various parties, such as consumers and marketers, perform sentiment analysis on these tweets to gather product information or conduct market analysis. Tweepy sentiment helps to find and analyze the sentiment for user searched topics. 


### Methodology
   The model built for this machine learning application uses the Logistic Regression algorithm.


### How to use
 + Clone the repository.
     - `git clone https://github.com/CosmiX-6/Tweepy-Sentiment.git`

 + Install the dependencies provided in this repo.
     - `pip install -r requirements.txt`

 + Update the twitter api credentials in '.env' file and place it to root directory.
     - _To run this app on localhost or using main.py, go to app directory >> create a file with name `.env` and paste the credentials._<br>
               
               api_key = '<--place-key-in-between-quotes-->'
               api_secret_key = '<--place-key-in-between-quotes-->'
               access_token = '<--place-key-in-between-quotes-->'
               access_token_secret = '<--place-key-in-between-quotes-->'
               

     - _To deploy project on heroku use the Procfile_
     - Update the credential in heroku app `Config Vars` under app settings.

 + Execute the main.py using python.


### Result
    Accuracy : 79%
    Vectorizer : ngram_range=(1,2)
