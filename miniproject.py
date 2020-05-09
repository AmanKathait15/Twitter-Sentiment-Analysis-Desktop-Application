
################################# imported module ###################################

import re , tweepy
import bs4,requests
import subprocess, sys
import config

from tweepy import OAuthHandler 
from textblob import TextBlob 
from matplotlib import pyplot as plt
from tkinter import *
from tkinter import ttk
from threading import Thread
from numpy import array


class TwitterClient(): 

    def __init__(self): 
 
        consumer_key = config.consumer_key
        
        consumer_secret = config.consumer_secret
        
        access_token = config.access_token
        
        access_token_secret = config.access_token_secret

        self.polarity = []
        self.count = 0
        self.query = 'lockdown'
        self.positive = 0
        self.negative = 0
        self.neutral = 0

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

            f = open("logbook.txt","a")

            f.write("\n"+str(e))

            f.close()

    def plotPieChart(self):

        labels = ['Positive {:.2f} %'.format(self.positive) , 'Neutral {:.2f} %'.format(self.neutral) ,'Negative {:.2f} %'.format(self.negative)]
        
        sizes = [self.positive, self.neutral, self.negative]
        
        colors = ['green', 'orange', 'red']
        
        plt.figure(1)
        
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        
        plt.legend(patches, labels, loc="best")
        
        plt.title('pie - chart')
        
        plt.axis('equal')
        
        plt.show()

    def scatter_plot(self):

        fig = plt.figure(2)
        
        axis = fig.add_subplot(1,1,1)
        
        x = array(range(0,len(self.polarity)))
        
        y = array(self.polarity)

        axis.plot(x,y)
        
        plt.xlabel('tweet number')
        
        plt.ylabel('polarity')
        
        plt.show()

    def plothistogram(self):

        plt.figure(3)
        
        plt.hist(self.polarity,bins=7,color='green',histtype = 'barstacked')
        
        plt.ylabel('number of tweets')
        
        plt.xlabel('polarity of tweets')
        
        plt.show()

def cleartag():
    
    tag.delete(0,END)

def Select_number_of_tweets(event = None):

    return number_of_tweets.get()

def Select_trending_topic(event = None):

    api.query = str(topic.get())

    tag.delete(0,END)

    tag.insert(0,api.query)

def main(): 

    user_input = str(tag.get())

    if(len(user_input)>1):
        
        api.query = str(user_input)

    api.count = Select_number_of_tweets()

    api.polarity = []

    print(api.query,api.count,len(api.polarity))

    search_button.config(text = "fetching..")
    
    search_button.config(state = DISABLED)

    clear_button.config(text = "Wait")
    
    clear_button.config(state = DISABLED)
    
    # calling function to get tweets 
    tweets = api.get_tweets() 
    
    # picking positive tweets from tweets 
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
    
    # percentage of positive tweets 
    api.positive = 100*len(ptweets)/len(tweets)
    
    print("Positive tweets percentage: {:.2f} %".format(api.positive))

    # picking negative tweets from tweets 
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
    
    # percentage of negative tweets
    api.negative = 100*len(ntweets)/len(tweets)
    
    print("Negative tweets percentage: {:.2f} %".format(api.negative)) 

    # percentage of neutral tweets 
    api.neutral = 100 - api.positive - api.negative
    
    print("Neutral tweets percentage: {:.2f} %".format(api.neutral)) 

    # printing first 5 positive tweets 
    print("\n\nPositive tweets:") 
    
    for tweet in ptweets[:10]: 
        print(tweet['text'])

    # printing first 5 negative tweets 
    print("\n\nNegative tweets:") 
    
    for tweet in ntweets[:10]: 
        print(tweet['text'])

    search_button.config(text = "Search")
    
    search_button.config(state = NORMAL)

    clear_button.config(text = "Clear")
    
    clear_button.config(state = NORMAL)

def main_thread():

    thread = Thread(target = main)
    
    thread.start()

def get_html(url):

    response = requests.get(url)

    return response

def get_detail():

    try:

        url = "https://trends24.in/india/"

        response = get_html(url)

        bs = bs4.BeautifulSoup(response.text,'html.parser')

        tag = bs.find("div",class_ = "trend-card").find_all("a")

        trending = []

        for i in tag:

            trending.append(i.get_text())

        return trending

    except Exception as e:
        
        print(e)

        f = open("logbook.txt","a")

        f.write("\n"+str(e))

        f.close()

def set_bg_to_grey():

    root.configure(background="grey")

    topframe.configure(background="grey")

    set_bg_frame.configure(background="grey")

    frame.configure(background="grey")

    middleframe.configure(background="grey")

    bottomFrame.configure(background="grey")

def set_bg_to_red():

    root.configure(background="red")

    topframe.configure(background="red")

    set_bg_frame.configure(background="red")

    frame.configure(background="red")

    middleframe.configure(background="red")

    bottomFrame.configure(background="red")

def set_bg_to_pink():

    root.configure(background="pink")

    topframe.configure(background="pink")

    set_bg_frame.configure(background="pink")

    frame.configure(background="pink")

    middleframe.configure(background="pink")

    bottomFrame.configure(background="pink")

def set_bg_to_brown():

    root.configure(background="brown")

    topframe.configure(background="brown")

    set_bg_frame.configure(background="brown")

    frame.configure(background="brown")

    middleframe.configure(background="brown")

    bottomFrame.configure(background="brown")


def set_bg_to_green():

    root.configure(background="green")

    topframe.configure(background="green")

    set_bg_frame.configure(background="green")

    frame.configure(background="green")

    middleframe.configure(background="green")

    bottomFrame.configure(background="green")

def set_bg_to_blue():

    root.configure(background="lightblue")

    topframe.configure(background="lightblue")

    set_bg_frame.configure(background="lightblue")

    frame.configure(background="lightblue")

    middleframe.configure(background="lightblue")

    bottomFrame.configure(background="lightblue")

def open_twitter():

    twitter_url = "https://twitter.com/"

    if sys.platform.startswith('linux'):
        
        subprocess.Popen(['xdg-open', twitter_url],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    elif sys.platform.startswith('win32'):
        
        os.startfile(twitter_url)
    
    elif sys.platform.startswith('cygwin'):
        
        os.startfile(twitter_url)
    
    elif sys.platform.startswith('darwin'):
        
        subprocess.Popen(['open', twitter_url],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        
        subprocess.Popen(['xdg-open', twitter_url],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)


'''
def plotpiechart():

    thread = Thread(target = api.plotPieChart)
    thread.start()

def scatter_plot():

    thread = Thread(target = api.plotbargraph)
    thread.start()

def plothistogram():

    thread = Thread(target = api.plothistogram)
    thread.start()'''

if __name__ == "__main__": 

    # calling main function 

    # creating object of TwitterClient Class 
    api = TwitterClient()
    
    root = Tk()

    root.title("Twitter Sentiment Analysis Desktop Application")

    root.geometry("800x600")
    
    root.resizable(width = False , height = False)
    
    root.configure(background = "lightblue")

    label1 = Label(root,text="Twitter Sentiment Analysis",fg="blue",bg="skyblue",font=("",15,"bold"))
    
    label1.pack(side=TOP,pady=20)

    topframe = Frame(root,background="lightblue")
    
    topframe.pack()

    set_bg_frame = Frame(topframe,background="lightblue",height=150,width=150)

    set_bg_frame.pack(side = LEFT)

    #Label(set_bg_frame,text="Select background color",fg="red",bg="blue",font=("",12,"bold")).pack()

    darkcolor = Frame(set_bg_frame)

    darkcolor.pack()

    lightcolor = Frame(set_bg_frame)

    lightcolor.pack()

    red_image = PhotoImage(file = "red.png")
    
    brown_image = PhotoImage(file = "brown.png")
    
    pink_image = PhotoImage(file = "pink.png")

    grey_image = PhotoImage(file = "grey.png")

    green_image = PhotoImage(file = "green.png")

    blue_image = PhotoImage(file = "blue.png")

    red_image = red_image.subsample(4,4)
    
    brown_image = brown_image.subsample(4,4)
    
    pink_image = pink_image.subsample(4,4)

    grey_image = grey_image.subsample(4,4)

    green_image = green_image.subsample(4,4)

    blue_image = blue_image.subsample(4,4)

    red_button = Button(darkcolor,image = red_image,command = set_bg_to_red)
    
    red_button.pack(side = LEFT)

    brown_button = Button(darkcolor, image = brown_image,command = set_bg_to_brown)
    
    brown_button.pack(side = LEFT)

    green_button = Button(darkcolor,image = green_image,command = set_bg_to_green)
    
    green_button.pack(side = LEFT)

    pink_button = Button(lightcolor,image = pink_image,command = set_bg_to_pink)
    
    pink_button.pack(side = LEFT)

    grey_button = Button(lightcolor, image = grey_image,command = set_bg_to_grey)
    
    grey_button.pack(side = LEFT)

    blue_button = Button(lightcolor,image = blue_image,command = set_bg_to_blue)
    
    blue_button.pack(side = LEFT)

    twitter_img = PhotoImage(file="twitter.png")

    twitter_img = twitter_img.subsample(1,1)

    twitter_button = Button(topframe,image = twitter_img,command = open_twitter)

    twitter_button.pack(side = LEFT,padx = (100,60))

    frame = Frame(topframe,background="lightblue")

    frame.pack(side = LEFT)

    label6 = Label(frame,text="Trending #tag",fg="red",bg="blue",font=("",12,"bold"))

    label6.pack(side = TOP , pady = 10)

    topic = StringVar()

    trending_topics = ttk.Combobox(frame , textvariable = topic , width = 20, height = 10)

    #tmp = ["game","movies","politics","lockdown","bitcoin"]

    trending_topics['values'] = get_detail()

    trending_topics.pack()

    trending_topics.current(0)

    trending_topics.bind("<<ComboboxSelected>>",Select_trending_topic)

    label3 = Label(root,text="Enter Twitter #tag to search",fg="red",bg="yellow",font=("",12,"bold"))
    
    label3.pack(side=TOP,pady=10)

    tag = Entry(root,justify=CENTER,font = ("verdana","15","bold"))
    
    tag.pack(side = TOP)

    middleframe = Frame(root,background="lightblue")
    
    middleframe.pack()

    search_button = Button(middleframe,text="Search",fg="white",bg="black",height=1,width=10,font=("verdana",10,"bold"),command = main_thread)
    
    search_button.pack(side = LEFT,padx=5,pady=5)

    clear_button = Button(middleframe,text="Clear",fg="white",bg="black",height=1,width=10,font=("verdana",10,"bold"),command = cleartag)
    
    clear_button.pack(side = LEFT,padx=5,pady=5)

    label4 = Label(root,text="Select number of tweets to fetch from twitter",fg="red",bg="yellow",font=("",12,"bold"))
    
    label4.pack(side=TOP,pady=10)

    Values = (50,75,100,150,200,250,500,750,1000)

    number_of_tweets = IntVar()

    choices = ttk.Combobox(root,textvariable = number_of_tweets,height=10)

    choices['values'] = Values
    
    choices.pack()

    choices.current(2)

    choices.bind("<<ComboboxSelected>>",Select_number_of_tweets)

    label5 = Label(root,text="Select appropriate diagram to dislpay ",fg="red",bg="yellow",font=("",12,"bold"))
    
    label5.pack(side=TOP,pady=10)

    bottomFrame = Frame(root,background="lightblue",width=700,height=150)
    
    bottomFrame.pack(side = TOP,pady = 20)

    piechart_image = PhotoImage(file = "/home/aman/Documents/my_projects/Sentiment Analysis in python/piechart.png")
    
    scatterplot_image = PhotoImage(file = "/home/aman/Documents/my_projects/Sentiment Analysis in python/scatter.png")
    
    histogram_image = PhotoImage(file = "/home/aman/Documents/my_projects/Sentiment Analysis in python/histogram.png")

    piechart_image = piechart_image.subsample(2,2)
    
    scatterplot_image = scatterplot_image.subsample(2,2)
    
    histogram_image = histogram_image.subsample(2,2)

    piechart_button = Button(bottomFrame,image = piechart_image,command = api.plotPieChart)
    
    piechart_button.pack(side = LEFT,padx=20)

    scatterplot_button = Button(bottomFrame, image = scatterplot_image,command = api.scatter_plot)
    
    scatterplot_button.pack(side = LEFT,padx=20)

    histogram_button = Button(bottomFrame,image = histogram_image,command = api.plothistogram)
    
    histogram_button.pack(side = LEFT,padx=20)
    '''
    if(flag):
        piechart_button.config(state = DISABLED)
        scatterplot_button.config(state = DISABLED)
        histogram_button.config(state = DISABLED)
    else:
        piechart_button.config(state = NORMAL)
        scatterplot_button.config(state = NORMAL)
        histogram_button.config(state = NORMAL)'''

    root.mainloop()
