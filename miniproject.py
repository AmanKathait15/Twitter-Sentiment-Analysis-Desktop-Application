# imported module

import re , tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
from matplotlib import pyplot as plt

class TwitterClient(): 

    def __init__(self): 
 
        consumer_key = 'If3ljZl8ECSi2v3IBxBg8iZEk'
        consumer_secret = 'g1N2eRo5peUBZkEWAXJTCSIg0Pxg49FPI9a94KF939gi5mfysn'
        access_token = '1167253468165206016-rS16iSgUMZhPzNCEAlp60n5dUwc4Ds'
        access_token_secret = 'dvtBvEIrhnJMsLRchwpZzXIFOnInflOlABRUK4wn5fHdf'

        self.polarity = []
        self.count = 0
        self.query = ''

        # attempt authentication 
        try: 
            # create OAuthHandler object 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
            self.auth.set_access_token(access_token, access_token_secret) 
            # create tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed") 

    def clean_tweet(self, tweet): 

        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

    def get_tweet_sentiment(self, tweet): 
 
        analysis = TextBlob(self.clean_tweet(tweet))
        self.polarity.append(analysis.sentiment.polarity)

        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'

    def get_tweets(self): 

        tweets = []

        try: 
            # call twitter api to fetch tweets 
            fetched_tweets = self.api.search(q = self.query, count = self.count) 

            # parsing tweets one by one 
            for tweet in fetched_tweets: 
                # empty dictionary to store required params of a tweet 
                parsed_tweet = {} 

                # saving text of tweet 
                parsed_tweet['text'] = tweet.text 
                # saving sentiment of tweet 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 

                # appending parsed tweet to tweets list 
                if tweet.retweet_count > 0: 
                    # if tweet has retweets, ensure that it is appended only once 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 

            # return parsed tweets 
            return tweets 

        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e))

    def plotPieChart(self,positive, negative, neutral):

        labels = ['Positive [' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]','Negative [' + str(negative) + '%]']
        sizes = [positive, neutral, negative]
        colors = ['green', 'orange', 'red']
        plt.figure(1)
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('pie - chart')
        plt.axis('equal')
        #plt.show()

    def plotgraph(self):
        fig = plt.figure(2)
        axis = fig.add_subplot(1,1,1)
        axis.plot(range(0,self.count),self.polarity)
        plt.xlabel('tweet number')
        plt.ylabel('polarity')
        #plt.show()

    def plotbargraph(self):
        plt.figure(3)
        plt.hist(self.polarity,bins=7,color='green',histtype = 'barstacked')
        plt.ylabel('number of tweets')
        plt.xlabel('polarity of tweets')
        #plt.show()


def main(): 
    # creating object of TwitterClient Class 
    api = TwitterClient()
    
    # input for term to be searched and how many tweets to search
    api.query = input("Enter Twitter #Tag to search about: ")
    api.count = int(input("Enter number of tweets to fetch from twitter database: "))
    # calling function to get tweets 
    tweets = api.get_tweets() 
    
    # picking positive tweets from tweets 
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
    # percentage of positive tweets 
    positive = 100*len(ptweets)/len(tweets)
    print("Positive tweets percentage: {} %".format(positive,'.2f'))

    # picking negative tweets from tweets 
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
    # percentage of negative tweets
    negative = 100*len(ntweets)/len(tweets)
    print("Negative tweets percentage: {} %".format(negative,'.2f')) 

    # percentage of neutral tweets 
    neutral = 100 - positive - negative
    print("Neutral tweets percentage: {} %".format(neutral,'.2f')) 

    # printing first 5 positive tweets 
    print("\n\nPositive tweets:") 
    for tweet in ptweets[:10]: 
        print(tweet['text'])

    # printing first 5 negative tweets 
    print("\n\nNegative tweets:") 
    for tweet in ntweets[:10]: 
        print(tweet['text']) 

    api.plotPieChart(positive,negative,neutral)
    api.plotgraph()
    api.plotbargraph()

    plt.show()

if __name__ == "__main__": 
    # calling main function 
    main() 
