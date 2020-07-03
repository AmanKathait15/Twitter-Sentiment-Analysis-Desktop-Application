
################################# imported modules ###################################

import tweepy                                       #### used to fetch tweet from twitter ####
import emoji                                        #### to convert emoji into text ####
import joblib                                       #### to load save machine learning model ####
import requests                                     #### to make https connection ####
import csv                                          #### to save result into csv file ####
import operator                                     
import itertools                                    
import re                                           #### used to filter unwanted things(like handle , url etc) from tweet ####

from config import *                                #### contain authentication keys of twitter developer account #### 
from tweepy import OAuthHandler                     #### used to make connection with twitter ####
from textblob import TextBlob                       #### for finding tweet sentiment and polarity ####
from matplotlib import pyplot as plt                #### used to display data in pie-chart , bar graph and scatter plot ####
from tkinter import *                               #### used to develop GUI ####
from tkinter import ttk                             #### used to develop GUI ####
from threading import Thread                        #### used to divide process into different thread ####
from numpy import array                             #### used to covert list into numpy array ####
from bs4 import BeautifulSoup                       #### to fetch treanding #tag from twitter ####
from googletrans import Translator                  #### to translate language other then english ####
from time import strftime,localtime                 #### to find local time ####

################################# End of imported modules ###################################

class TwitterClient(): 

    """    
    ################# docstring for TwitterClient Class #################

    varibale 	type 			use to

    query 	string 			store #tag that user enter in tag_field

    count 	integer			store number of tweets to fetch from twitter

    ploarity 	list 			store sentiment score of all tweets range from -1 to +1

    positive 	list 			store postive sentiment score of different ml model used

    negative 	list 			store negative sentiment score of different ml model used

    neutral 	list 			store neutral sentiment score of different ml model used

    model 	string 			store model which is currently selected in combobox

    nbc 	undefined   		used to store naviebayes classifier object

    rf  	undefined   		used to store random forest classifier object

    dt  	undefined   		used to store decission tree classifier object

    ################# class function #################

    function 			work / task						run/call

    __init__			this function is a constructor of TwitterClient		run when TwitterClient class object is created	
    				class and it work is to allocate memory to 
    				TwiiterClient object and initailze class variables

    authentication  		this function make connection with twitter by tweepy	run after TwitterClient object is created
    				OAuthHamdler method with the help of credentials of
    				twitter developer account

    load_dict_smileys		this function make dictionary of emoticon with 		call inside clean_tweet function
    				emoticon as key and meaning as value so can be 
    				used in preprocessing phase

    load_dict_contractions  	this function make dictionary of contractions with 	call inside clean_tweet function
    				contraction like doesn't as key and meaning (does not) 
    				as value so can be used in preprocessing phase

    clean_tweet			this function is used to preprocess data . this 	call before finding ploarity of each tweet
    				function filter tweet by removinf handle , url 
    				, retweet tag and hash tag which not useful in 
    				sentiment analysis and convert emoticon , emoji
    				and contraction to thier meaning in text

    get_tweet_sentiment 	used to find sentimet of tweet i.e positive , 		call inside get_tweets function
    				negative or neutral and append sentiment score in 
    				ploarity

    get_tweets 			this function fetched tweets by using self.search()	call inside back_end function
    				and then call clean_tweet() to claen tweets and
    				find sentiment score using get_tweet_sentiment()
    				and save this to fetched_tweet.csv file

    back_end			this function start the back_end process work by 	call by main_thread function
    				calling get_tweets function and changing labels 
    				value so that user can Know some magic is 
    				hapening inside

    main_thread			this function divide the process into different 	run when search button is clicked in GUI
    				threads basically it reduce the load of GUI by 
    				calling back_end in different thread 

    plot_PieChart		this function display our data in pie chart form 	run when pie chart icon clicked in GUI
    				ie show value of +ve , -ve and 0 score in our data

    plot_histogram 		this function display ploarity in histogram form 	run when histogram icon clicked in GUI
    				so that user can visualize which sentiment score
    				range tweet is more .

    scatter_plot 		this function display polarity in scatter plot 		run when scatter plot icon clicked in GUI
    				graph make easy to visualize flow of sentiments
    				of twitter users on that query

    select_model 		this function return the current value of model_list	run each time when mode_list current value changes

    select_no_of_tweets		this function return the current value of choice 	run each time when choice current value changes
				combobox 

    select_trending_tag 	this function return the vlaue of selected trending 	run each time when trending_tag combobox current
				tag out of top 10 					value changes

    clear_tag	 		this function clear the value of tag_field 		run when clear button clicked in GUI

    check_tag 			this function check tag enter is valid or not 		run when tag_field value changes

    trending_tag 		this function fetch list of top 10 trending #tag 	run when program execute
				from web and display it in trending_tag combobox

    open_twitter 		this function open twitter website in default browser 	run when twitter icon is clicked in GUI

    open_fetched_tweets 	this function open fetched_tweet csv file in your 	run when open fetched tweets button is clicked in GUI
				default text editor 

    open_log_file 		this function open log_file.csv 			run when open log file button is clicked in GUI

    open_testing_dataset 	this function open test.csv 				run when open test dataset button is clicked in GUI

    open_training_dataset 	this function open train.csv 				run when open train dataset button is clicked in GUI

    check_internet 		this function check you are connected to internet 	run before creating GUI 
				or not if not then show error message
				as this program needs internet to fetched tweets

    ################# non-class function #################

    set_bg_to_<color> 		this function change the backgroud color of GUI 	run when color icon is clicked in GUI

    if__name__=="__main__"      In this function most of GUI coding is done. 		execution of program begin from this function



    """

    def __init__(self):  

    	# attempt authentication 
    	try:

    		self.polarity = [[],[],[],[]]
    		
    		self.count = 0
    		
    		self.query = None
    		
    		self.positive = [0,0,0,0]
    		
    		self.negative = [0,0,0,0]
    		
    		self.neutral = [0,0,0,0]
    		
    		self.nbc = None
    		
    		self.rf = None
    		
    		self.dt = None
    		
    		self.model = None

    		self.main_window = None

    		self.topframe = None

    		self.middleframe = None

    		self.bottomFrame = None

    		self.set_bg_frame = None

    		self.frame = None

    		self.newframe = None

    		self.leftframe = None

    		self.rightframe = None

    		self.tag_var = None

    		self.number_of_tweets = None

    		self.model_var = None

    		self.tag_field = None

    		self.topic = None

    		self.search_button = None

    		self.clear_button = None

    		self.piechart_button = None

    		self.histogram_button = None

    		self.scatterplot_button = None

    		self.btn1 = None

    		self.radioVar = None

    		self.labels1 = None

    		self.label3 = None

    		self.trending_tags = None

    		self.url_flag = 1

    		self.emoticon_flag = 1

    		self.emoji_flag = 1

    		self.hastags_flag = 1

    		self.handle_flag = 1

    		# create OAuthHandler object 
    		self.auth = OAuthHandler(consumer_key, consumer_secret)

    		# set access token and secret
    		self.auth.set_access_token(access_token, access_token_secret)

    		# create tweepy api object to fetch tweets
    		self.api = tweepy.API(self.auth) 


    	except Exception as e:

            print("authentication failed please check your network and try again \nerror detail : "+str(e))

            msg = str(strftime("%Y-%m-%d %H:%M:%S", localtime()))+","+str(e)+"\n" 
            
            f = open("csv_files/logbook.csv","a")

            f.write(msg)

            f.close()
 

    # emoticons
    def load_dict_smileys(self):
        
        return {
            ":‑)":"smiley",
            ":-]":"smiley",
            ":-3":"smiley",
            ":->":"smiley",
            "8-)":"smiley",
            ":-}":"smiley",
            ":)":"smiley",
            ":]":"smiley",
            ":3":"smiley",
            ":>":"smiley",
            "8)":"smiley",
            ":}":"smiley",
            ":o)":"smiley",
            ":c)":"smiley",
            ":^)":"smiley",
            "=]":"smiley",
            "=)":"smiley",
            ":-))":"smiley",
            ":‑D":"smiley",
            "8‑D":"smiley",
            "x‑D":"smiley",
            "X‑D":"smiley",
            ":D":"smiley",
            "8D":"smiley",
            "xD":"smiley",
            "XD":"smiley",
            ":‑(":"sad",
            ":‑c":"sad",
            ":‑<":"sad",
            ":‑[":"sad",
            ":(":"sad",
            ":c":"sad",
            ":<":"sad",
            ":[":"sad",
            ":-||":"sad",
            ">:[":"sad",
            ":{":"sad",
            ":@":"sad",
            ">:(":"sad",
            ":'‑(":"sad",
            ":'(":"sad",
            ":‑P":"playful",
            "X‑P":"playful",
            "x‑p":"playful",
            ":‑p":"playful",
            ":‑Þ":"playful",
            ":‑þ":"playful",
            ":‑b":"playful",
            ":P":"playful",
            "XP":"playful",
            "xp":"playful",
            ":p":"playful",
            ":Þ":"playful",
            ":þ":"playful",
            ":b":"playful",
            "<3":"love"
            }

    # self defined contractions
    def load_dict_contractions(self):
        
        return {
            "ain't":"is not",
            "amn't":"am not",
            "aren't":"are not",
            "can't":"cannot",
            "'cause":"because",
            "couldn't":"could not",
            "couldn't've":"could not have",
            "could've":"could have",
            "daren't":"dare not",
            "daresn't":"dare not",
            "dasn't":"dare not",
            "didn't":"did not",
            "doesn't":"does not",
            "don't":"do not",
            "e'er":"ever",
            "em":"them",
            "everyone's":"everyone is",
            "finna":"fixing to",
            "gimme":"give me",
            "gonna":"going to",
            "gon't":"go not",
            "gotta":"got to",
            "hadn't":"had not",
            "hasn't":"has not",
            "haven't":"have not",
            "he'd":"he would",
            "he'll":"he will",
            "he's":"he is",
            "he've":"he have",
            "how'd":"how would",
            "how'll":"how will",
            "how're":"how are",
            "how's":"how is",
            "I'd":"I would",
            "I'll":"I will",
            "I'm":"I am",
            "I'm'a":"I am about to",
            "I'm'o":"I am going to",
            "isn't":"is not",
            "it'd":"it would",
            "it'll":"it will",
            "it's":"it is",
            "I've":"I have",
            "kinda":"kind of",
            "let's":"let us",
            "mayn't":"may not",
            "may've":"may have",
            "mightn't":"might not",
            "might've":"might have",
            "mustn't":"must not",
            "mustn't've":"must not have",
            "must've":"must have",
            "needn't":"need not",
            "ne'er":"never",
            "o'":"of",
            "o'er":"over",
            "ol'":"old",
            "oughtn't":"ought not",
            "shalln't":"shall not",
            "shan't":"shall not",
            "she'd":"she would",
            "she'll":"she will",
            "she's":"she is",
            "shouldn't":"should not",
            "shouldn't've":"should not have",
            "should've":"should have",
            "somebody's":"somebody is",
            "someone's":"someone is",
            "something's":"something is",
            "that'd":"that would",
            "that'll":"that will",
            "that're":"that are",
            "that's":"that is",
            "there'd":"there would",
            "there'll":"there will",
            "there're":"there are",
            "there's":"there is",
            "these're":"these are",
            "they'd":"they would",
            "they'll":"they will",
            "they're":"they are",
            "they've":"they have",
            "this's":"this is",
            "those're":"those are",
            "'tis":"it is",
            "'twas":"it was",
            "wanna":"want to",
            "wasn't":"was not",
            "we'd":"we would",
            "we'd've":"we would have",
            "we'll":"we will",
            "we're":"we are",
            "weren't":"were not",
            "we've":"we have",
            "what'd":"what did",
            "what'll":"what will",
            "what're":"what are",
            "what's":"what is",
            "what've":"what have",
            "when's":"when is",
            "where'd":"where did",
            "where're":"where are",
            "where's":"where is",
            "where've":"where have",
            "which's":"which is",
            "who'd":"who would",
            "who'd've":"who would have",
            "who'll":"who will",
            "who're":"who are",
            "who's":"who is",
            "who've":"who have",
            "why'd":"why did",
            "why're":"why are",
            "why's":"why is",
            "won't":"will not",
            "wouldn't":"would not",
            "would've":"would have",
            "y'all":"you all",
            "you'd":"you would",
            "you'll":"you will",
            "you're":"you are",
            "you've":"you have",
            "Whatcha":"What are you",
            "luv":"love",
            "sux":"sucks"
            }


    def clean_tweet(self,tweet):    
        
        try:
            
            #Esctcng HTML characters
            
            if(self.url_flag.get()):
            
            	tweet = re.sub(r"http\S+", "", tweet)
            
            #Special case not handled previously.
            tweet = tweet.replace('\x92',"'")

            #removing retweet tag
            tweet = tweet.replace('RT',"")
            
            #Removal of hastags

            if(self.hastags_flag.get()):

                tweet = re.sub(r"#[A-Za-z0-9]+", "", tweet)

            #Removal of handle

            if(self.handle_flag.get()):

                tweet = re.sub(r"@[A-Za-z0-9_:]+", "", tweet,10)
            
            #Removal of address
            tweet = re.sub("(\w+:\/\/\S+)", " ", tweet)
            
            #Removal of Punctuation
            tweet = re.sub("[\.\,\!\?\:\;\-\=]", " ", tweet)
            
            #Lower case
            tweet = tweet.lower()
            
            #CONTRACTIONS source: https://en.wikipedia.org/wiki/Contraction_%28grammar%29
            CONTRACTIONS = self.load_dict_contractions()

            tweet = tweet.replace("’","'")
            
            words = tweet.split()
            
            reformed = [CONTRACTIONS[word] if word in CONTRACTIONS else word for word in words]
            
            tweet = " ".join(reformed)
            
            # Standardizing words
            tweet = ''.join(''.join(s)[:2] for _, s in itertools.groupby(tweet))
            
            #Deal with emoticons source: https://en.wikipedia.org/wiki/List_of_emoticons

            if(self.emoticon_flag.get()):

                SMILEY = self.load_dict_smileys()  
            
                words = tweet.split()
            
                reformed = [SMILEY[word] if word in SMILEY else word for word in words]
            
                tweet = " ".join(reformed)
            
            #Deal with emojis

            if(self.emoji_flag.get()):

                tweet = emoji.demojize(tweet)

                tweet = tweet.replace("[:_]","")
            
                tweet = ' '.join(tweet.split())

            #Removal of Punctuation
            tweet = re.sub("[_:]", " ", tweet)

            return tweet

        except Exception as e:
        
            raise e
            
            print("<<<<<<<<<<<<<<<< Error occured while cleaning tweet >>>>>>>>>>>>>>>>>>>>>>>>>")

            msg = str(strftime("%Y-%m-%d %H:%M:%S", localtime()))+","+str(e)+"\n" 
            
            f = open("csv_files/logbook.csv","a")

            f.write(msg)

            f.close()

    def get_tweet_sentiment_1(self,text,index): 
    
        analysis = TextBlob(text)

        pol = analysis.sentiment.polarity

        self.polarity[index].append(pol)

        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            
            tag = 'positive'

            self.positive[index]+=1
        
        elif analysis.sentiment.polarity == 0: 
            
            tag = 'neutral'

            self.neutral[index]+=1
        
        else: 
            
            tag = 'negative'

            self.negative[index]+=1

        return (tag,pol)

    def get_tweet_sentiment_2(self,text,index):

        prob_dist = self.nbc.prob_classify(text)

        pos = round(prob_dist.prob("pos"), 1)

        neg = round(prob_dist.prob("neg"), 1)

        pol = max(pos,neg)

        # set sentiment 
        if pos==neg: 
            
            tag = 'neutral'

            self.neutral[index]+=1

            pol = 0

        elif pos>neg:

            tag = 'positive'

            self.positive[index]+=1
        
        else: 
            
            tag = 'negative'

            self.negative[index]+=1

            pol = -(pol)

        self.polarity[index].append(pol)

        return (tag,pol)

    def get_tweet_sentiment_3(self,text,index):

        prob_dist = self.rf.prob_classify(text)

        pos = round(prob_dist.prob("pos"), 1)

        neg = round(prob_dist.prob("neg"), 1)

        pol = max(pos,neg)

        # set sentiment 
        if pos==neg: 
            
            tag = 'neutral'

            self.neutral[index]+=1

            pol = 0

        elif pos>neg:

            tag = 'positive'

            self.positive[index]+=1
        
        else: 
            
            tag = 'negative'

            self.negative[index]+=1

            pol = -(pol)

        self.polarity[index].append(pol)

        return (tag,pol)

    def get_tweet_sentiment_4(self,text,index):

        prob_dist = self.dt.prob_classify(text)

        pos = round(prob_dist.prob("pos"), 1)

        neg = round(prob_dist.prob("neg"), 1)

        pol = max(pos,neg)

        # set sentiment 
        if pos==neg: 
            
            tag = 'neutral'

            self.neutral[index]+=1

            pol = 0

        elif pos>neg:

            tag = 'positive'

            self.positive[index]+=1
        
        else: 
            
            tag = 'negative'

            self.negative[index]+=1

            pol = -(pol)

        self.polarity[index].append(pol)

        return (tag,pol)

    def get_tweets(self): 

        self.polarity = [[],[],[],[]]
        self.positive = [0,0,0,0]
        self.negative = [0,0,0,0]
        self.neutral = [0,0,0,0]

        try:

        	self.query = self.tag_var.get()

        	self.count = self.number_of_tweets.get()

        	self.model = self.model_var.get()

        	print("<<<<<<<<<<<<<<< Query : "+self.query+" >>>>>>>>>>>>>>>>>\n")

        	print("<<<<<<<<<<<<<<< {} : >>>>>>>>>>>>>>>\n ".format(self.count))

        	self.query += " -filter:retweets"

        	with open("csv_files/fetched_tweet.csv","w") as wf:

        		print(self.model)

        		if(self.model == "compare all"):

        			wf.write("lang,tweet,textblob.sentiment,NaiveBayesClassifier,RandomForest,DecisionTree,combine sentiment score\n")

        		else:

        			wf.write("lang,tweet,sentiment,sentiment score\n")

        		fetched_tweets = None

        		ch = self.radioVar.get()

        		if(ch=="2"):

        			fetched_tweets = self.api.search(q = self.query,count = self.count, truncated = False, tweet_mode = 'extended')

        		else:

        			fetched_tweets = self.api.search(q = self.query, lang = 'en', count = self.count, truncated = False, tweet_mode = 'extended')

        		print(len(fetched_tweets))

        		for tweet in fetched_tweets: 

        			text = tweet.full_text

        			if(ch == "2"):

        				try:

        					translator = Translator()

        					print(text)

        					obj = translator.translate(text)

        					text = obj.text

        				except Exception as e:

        					print("Exception handle")

        					self.count-=1

        					msg = str(strftime("%Y-%m-%d %H:%M:%S", localtime()))+","+str(e)+"\n" 

        					f = open("csv_files/logbook.csv","a")

        					f.write(msg)

        					f.close()

        					continue

        			text = self.clean_tweet(text)

        			print(text)

        			print()

        			if(self.model == "compare all"):

        				tags = ""

        				pol = 0

        				tmp = self.get_tweet_sentiment_1(text,0)

        				tags += "," + tmp[0]

        				pol += tmp[1]

        				tmp = self.get_tweet_sentiment_2(text,1)

        				tags += "," + tmp[0]

        				pol += tmp[1]

        				tmp = self.get_tweet_sentiment_3(text,2)

        				tags += "," + tmp[0]

        				pol += tmp[1]

        				tmp = self.get_tweet_sentiment_4(text,3)

        				tags += "," + tmp[0]

        				pol += tmp[1]

        				pol/=2

        				wf.write(tweet.lang+","+text+tags+","+str(pol)+"\n")

        			elif(self.model == "NaiveBayesClassifier"):

        				tag = ","

        				tmp = self.get_tweet_sentiment_2(text,0)

        				tag += tmp[0]

        				wf.write(tweet.lang+","+text+tag+","+str(tmp[1])+"\n")

        			elif(self.model == "RandomForest"):

        				tag = ","

        				tmp = self.get_tweet_sentiment_3(text,0)

        				tag += tmp[0]

        				wf.write(tweet.lang+","+text+tag+","+str(tmp[1])+"\n")

        			elif(self.model == "DecisionTree"):

        				tag = ","

        				tmp = self.get_tweet_sentiment_4(text,0)

        				tag += tmp[0]

        				wf.write(tweet.lang+","+text+tag+","+str(tmp[1])+"\n")

        			elif(self.model == "textblob.sentiment"):

        				tag = ","

        				tmp = self.get_tweet_sentiment_1(text,0)

        				tag += tmp[0]

        				wf.write(tweet.lang+","+text+tag+","+str(tmp[1])+"\n")

        	if(self.model == "compare all"):

        		l = len(self.positive)

        		for i in range(4):

        			self.positive[i]*= 100/self.count

        			self.negative[i]*= 100/self.count

        			self.neutral[i]*= 100/self.count

        	else:

        		self.positive[0]*= 100/self.count

        		self.negative[0]*= 100/self.count

        		self.neutral[0]*= 100/self.count

        except tweepy.TweepError as e: 
            
            print("Error occured while fetching tweets ")

            msg = str(strftime("%Y-%m-%d %H:%M:%S", localtime()))+","+str(e)+"\n" 
            
            f = open("csv_files/logbook.csv","a")

            f.write(msg)

            f.close()

    def plot_PieChart(self):

        if(self.model == "compare all"):

            fig, axs = plt.subplots(2, 2)

            labels = ['Positive {:.2f} %'.format(self.positive[0]) , 'Neutral {:.2f} %'.format(self.neutral[0]) ,'Negative {:.2f} %'.format(self.negative[0])]
            
            sizes = [self.positive[0], self.neutral[0], self.negative[0]]
            
            colors = ['green', 'orange', 'red']

            labels1 = ['Positive {:.2f} %'.format(self.positive[1]) , 'Neutral {:.2f} %'.format(self.neutral[1]) ,'Negative {:.2f} %'.format(self.negative[1])]
            
            sizes1 = [self.positive[1], self.neutral[1], self.negative[1]]
            
            colors = ['green', 'orange', 'red']

            labels2 = ['Positive {:.2f} %'.format(self.positive[2]) , 'Neutral {:.2f} %'.format(self.neutral[2]) ,'Negative {:.2f} %'.format(self.negative[2])]
            
            sizes2 = [self.positive[2], self.neutral[2], self.negative[2]]
            
            colors = ['green', 'orange', 'red']

            labels3 = ['Positive {:.2f} %'.format(self.positive[3]) , 'Neutral {:.2f} %'.format(self.neutral[3]) ,'Negative {:.2f} %'.format(self.negative[3])]
            
            sizes3 = [self.positive[3], self.neutral[3], self.negative[3]]
            
            colors = ['green', 'orange', 'red']

            patches,texts = axs[0, 0].pie(sizes, colors=colors, startangle=90)

            axs[0, 0].legend(patches, labels, loc="best")
            
            axs[0, 0].set_title('textblob.sentiment')
            
            patches,texts = axs[0, 1].pie(sizes1, colors=colors, startangle=135)

            axs[0, 1].legend(patches, labels1, loc="best")
            
            axs[0, 1].set_title('NaiveBayesClassifier')
            
            patches,texts = axs[1, 0].pie(sizes2, colors=colors, startangle=45)

            axs[1, 0].legend(patches, labels2, loc="best")
            
            axs[1, 0].set_title('RandomForest')
            
            patches,texts = axs[1, 1].pie(sizes3, colors=colors, startangle=180)

            axs[1, 1].legend(patches, labels3, loc="best")
            
            axs[1, 1].set_title('DecisionTree')

            # Hide x labels and tick labels for top plots and y ticks for right plots.
            for ax in axs.flat:
                ax.label_outer()

            plt.show()

        else:

            labels = ['Positive {:.2f} %'.format(self.positive[0]) , 'Neutral {:.2f} %'.format(self.neutral[0]) ,'Negative {:.2f} %'.format(self.negative[0])]
            
            sizes = [self.positive[0], self.neutral[0], self.negative[0]]
            
            colors = ['green', 'orange', 'red']
            
            plt.figure(1)
            
            patches, texts = plt.pie(sizes, colors=colors, startangle=90)
            
            plt.legend(patches, labels, loc="best")
            
            plt.title('pie - chart')
            
            plt.axis('equal')
            
            plt.show()

    def scatter_plot(self):

        if(self.model == "compare all"):

            fig, axs = plt.subplots(2, 2)

            x = array(range(0,len(self.polarity[0])))
            
            y = array(self.polarity[0])

            x1 = array(range(0,len(self.polarity[1])))
            
            y1 = array(self.polarity[1])

            x2 = array(range(0,len(self.polarity[2])))
            
            y2 = array(self.polarity[2])

            x3 = array(range(0,len(self.polarity[3])))
            
            y3 = array(self.polarity[3])

            axs[0, 0].plot(x, y)
            
            axs[0, 0].set_title('textblob.sentiment')
            
            axs[0, 1].plot(x1, y1, 'tab:orange')
            
            axs[0, 1].set_title('NaiveBayesClassifier')
            
            axs[1, 0].plot(x2, y2, 'tab:green')
            
            axs[1, 0].set_title('RandomForest')
            
            axs[1, 1].plot(x3, y3, 'tab:red')
            
            axs[1, 1].set_title('DecisionTree')

            for ax in axs.flat:
                ax.set(xlabel='tweet number', ylabel='polarity')

            # Hide x labels and tick labels for top plots and y ticks for right plots.
            for ax in axs.flat:
                ax.label_outer()

            plt.show()

        else:

            fig = plt.figure(2)
            
            axis = fig.add_subplot(1,1,1)
            
            x = array(range(0,len(self.polarity[0])))
            
            y = array(self.polarity[0])

            axis.plot(x,y)
            
            plt.xlabel('tweet number')
            
            plt.ylabel('polarity')
            
            plt.show()

    def plot_histogram(self):

        if(self.model == "compare all"):

            fig, axs = plt.subplots(2, 2)

            axs[0, 0].hist(self.polarity[0],bins=7,color='green',histtype = 'barstacked')
            
            axs[0, 0].set_title('textblob.sentiment')
            
            axs[0, 1].hist(self.polarity[1],bins=7,color='brown',histtype = 'barstacked')
            
            axs[0, 1].set_title('NaiveBayesClassifier')
            
            axs[1, 0].hist(self.polarity[2],bins=7,color='red',histtype = 'barstacked')
            
            axs[1, 0].set_title('RandomForest')
            
            axs[1, 1].hist(self.polarity[3],bins=7,color='blue',histtype = 'barstacked')
            
            axs[1, 1].set_title('DecisionTree')

            for ax in axs.flat:
                ax.set(xlabel='polarity of tweets', ylabel='number of tweets')

            # Hide x labels and tick labels for top plots and y ticks for right plots.
            for ax in axs.flat:
                ax.label_outer()

            plt.show()
        
        else:

            plt.hist(self.polarity[0],bins=7,color='green',histtype = 'barstacked')
            
            plt.ylabel('number of tweets')
            
            plt.xlabel('polarity of tweets')
            
            plt.show()

    def select_model(self,event = None):

        return self.model_var.get()

    def check_tag(self):

    	if(len(self.tag_var.get())<1):

    		self.label3.config(text = " Url field is empty ",bg="red",fg="yellow")

    		self.search_button.config(state = DISABLED)

    		print("url field is empty")

    		return

    	self.label3.config(text="Enter Twitter #tag to search",fg="red",bg="yellow",font=("",12,"bold"))

    	self.search_button.config(state = NORMAL)

    def clear_tag(self):
        
        self.tag_field.delete(0,END)

        self.histogram_button.config(state = DISABLED)

        self.piechart_button.config(state = DISABLED)

        self.scatterplot_button.config(state = DISABLED)

        self.btn1.config(state = DISABLED)

        self.search_button.config(state = DISABLED)

    def select_no_of_tweets(self,event = None):

        return self.number_of_tweets.get()

    def select_trending_tag(self,event = None):

        self.query = str(self.topic.get())

        self.tag_field.delete(0,END)

        self.tag_field.insert(0,self.query)

    def back_end(self): 

        try:

            print(self.query,self.count,len(self.polarity))

            self.search_button.config(text = "fetching..")
            
            self.search_button.config(state = DISABLED)

            self.clear_button.config(text = "wait pls..")
            
            self.clear_button.config(state = DISABLED)
            
            # calling function to get tweets 
            self.get_tweets()

            if(self.model=="compare all"):

                data = csv.reader(open('csv_files/fetched_tweet.csv',encoding = "latin-1"))

                sorted_data = sorted(data, key=operator.itemgetter(6),reverse=True)

                print("\nPOSTIVE TWEETS : \n")

                for tweet in sorted_data[1:11]:

                    print(tweet[1])

                print("\nNEGAIVE TWEETS : \n")

                for tweet in sorted_data[:-10:-1]:

                    print(tweet[1])

            else:

                data = csv.reader(open('csv_files/fetched_tweet.csv',encoding = "latin-1"))

                sorted_data = sorted(data, key=operator.itemgetter(3),reverse = True)

                print("\nPOSTIVE TWEETS : \n")

                for tweet in sorted_data[1:11]:

                    print(tweet[1])

                print("\nNEGATIVE TWEETS : \n")

                for tweet in sorted_data[:-10:-1]:

                    print(tweet[1])

            self.search_button.config(text = "Search")
            
            self.search_button.config(state = NORMAL)

            self.clear_button.config(text = "Clear")
            
            self.clear_button.config(state = NORMAL)

            self.histogram_button.config(state = NORMAL)

            self.piechart_button.config(state = NORMAL)

            self.scatterplot_button.config(state = NORMAL)

            self.btn1.config(state = NORMAL)

        except Exception as e:
            
            raise e

            print(str(e))

            msg = str(strftime("%Y-%m-%d %H:%M:%S", localtime()))+","+str(e)+"\n" 
            
            f = open("csv_files/logbook.csv","a")

            f.write(msg)

            f.close()

    def main_thread(self):

        thread1 = Thread(target = self.back_end)
        
        thread1.start()

    def trending_tag(self): 

        try:

            url = "https://trends24.in/india/"

            response = requests.get(url)

            print("<<<<<<<< request send to web >>>>>>>>>>>>>")

            bs = BeautifulSoup(response.text,'html.parser')

            tag = bs.find("div",class_ = "trend-card").find_all("a")
            
            self.trending_tags = []

            for i in tag:

                text = i.get_text()

                print("<<<<<<<<<<<<< fetching trending_tag >>>>>>>>>>>>>>>>")

                #translator = Translator()

                #Text = translator.translate(text)

                self.trending_tags.append(text)

            print("<<<<<<<<<< connected to internt >>>>>>>>>")

        except Exception as e:
        
        	raise e

        	print("\n<<<<<<<<<<<<< Error :  Not Connected to Internt >>>>>>>>>>>>>\n")

        	print("\n this Application required actve internt connection to work. So please try again with active internt connection \n\n")

        	msg = str(strftime("%Y-%m-%d %H:%M:%S", localtime()))+","+str(e)+"\n" 

        	f = open("csv_files/logbook.csv","a")

        	f.write(msg)

        	f.close()

        	exit()

    def open_twitter(self):

        twitter_url = "https://twitter.com/"

        import subprocess, sys

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

    def open_fetched_tweets(self):

        url = "csv_files/fetched_tweet.csv"

        import subprocess, sys

        if sys.platform.startswith('linux'):
            
            subprocess.Popen(['xdg-open', url],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        elif sys.platform.startswith('win32'):
            
            os.startfile(url)
        
        elif sys.platform.startswith('cygwin'):
            
            os.startfile(url)
        
        elif sys.platform.startswith('darwin'):
            
            subprocess.Popen(['open', url],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            
            subprocess.Popen(['xdg-open', url],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def open_training_dataset(self):

        url = "csv_files/train.csv"

        import subprocess, sys

        if sys.platform.startswith('linux'):
            
            subprocess.Popen(['xdg-open', url],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        elif sys.platform.startswith('win32'):
            
            os.startfile(url)
        
        elif sys.platform.startswith('cygwin'):
            
            os.startfile(url)
        
        elif sys.platform.startswith('darwin'):
            
            subprocess.Popen(['open', url],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            
            subprocess.Popen(['xdg-open', url],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def open_testing_dataset(self):

        url = "csv_files/test.csv"

        import subprocess, sys

        if sys.platform.startswith('linux'):
            
            subprocess.Popen(['xdg-open', url],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        elif sys.platform.startswith('win32'):
            
            os.startfile(url)
        
        elif sys.platform.startswith('cygwin'):
            
            os.startfile(url)
        
        elif sys.platform.startswith('darwin'):
            
            subprocess.Popen(['open', url],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            
            subprocess.Popen(['xdg-open', url],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def open_log_file(self):

        url = "csv_files/logbook.csv"

        import subprocess, sys

        if sys.platform.startswith('linux'):
            
            subprocess.Popen(['xdg-open', url],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        elif sys.platform.startswith('win32'):
            
            os.startfile(url)
        
        elif sys.platform.startswith('cygwin'):
            
            os.startfile(url)
        
        elif sys.platform.startswith('darwin'):
            
            subprocess.Popen(['open', url],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            
            subprocess.Popen(['xdg-open', url],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def load_models(self):

    	print("<<<<<<<<<<<<<< checking internt >>>>>>>>>>>>>>\n")

    	self.trending_tag()

    	print("\n<<<<<<<<<<<<<<  Loading Save modal from hardisck to main memory >>>>>>>>>>>>>>>>>>>>>>>\n")

    	print("<<<<<<<<<<<<<<  loading NaiveBayesClassifier.pkl file to main memory >>>>>>>>>>>>>>>>>>>>>>>>>>>\n")

    	self.nbc = joblib.load('save_model/NaiveBayesClassifier.pkl') 

    	print("<<<<<<<<<<<<<<  NaiveBayesClassifier.pkl file loaded to main memory >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")

    	print("<<<<<<<<<<<<<<  loading RandomForest.pkl file to main memory >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")

    	self.rf = joblib.load('save_model/RandomForest.pkl') 

    	print("<<<<<<<<<<<<<<  RandomForest.pkl file loaded to main memory >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")

    	print("<<<<<<<<<<<<<<  loading DecisionTree.pkl file to main memory >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")

    	self.dt = joblib.load('save_model/DecisionTree.pkl') 

    	print("<<<<<<<<<<<<<<  DecisionTree.pkl file loaded to main memory >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")

    	print("<<<<<<<<<<<<<<  All model are succesfully loaded :) >>>>>>>>>>>>>>>>>>>>>>>\n")


    def set_bg_to_orange(self):

     	self.main_window.configure(background="orange")

     	self.topframe.configure(background="orange")

     	self.set_bg_frame.configure(background="orange")

     	self.frame.configure(background="orange")

     	self.middleframe.configure(background="orange")

     	self.bottomFrame.configure(background="orange")

     	self.newframe.configure(background="orange")

     	self.leftframe.configure(background="orange")

     	self.rightframe.configure(background="orange")

    def set_bg_to_violet(self):

    	self.main_window.configure(background="violet")

    	self.topframe.configure(background="violet")

    	self.set_bg_frame.configure(background="violet")

    	self.frame.configure(background="violet")

    	self.middleframe.configure(background="violet")

    	self.bottomFrame.configure(background="violet")

    	self.newframe.configure(background="violet")

    	self.leftframe.configure(background="violet")

    	self.rightframe.configure(background="violet")

    def set_bg_to_yellow(self):

    	self.main_window.configure(background="yellow")

    	self.topframe.configure(background="yellow")

    	self.set_bg_frame.configure(background="yellow")

    	self.frame.configure(background="yellow")

    	self.middleframe.configure(background="yellow")

    	self.bottomFrame.configure(background="yellow")

    	self.newframe.configure(background="yellow")

    	self.leftframe.configure(background="yellow")

    	self.rightframe.configure(background="yellow")

    def set_bg_to_lightgreen(self):

    	self.main_window.configure(background="lightgreen")

    	self.topframe.configure(background="lightgreen")

    	self.set_bg_frame.configure(background="lightgreen")

    	self.frame.configure(background="lightgreen")

    	self.middleframe.configure(background="lightgreen")

    	self.bottomFrame.configure(background="lightgreen")

    	self.newframe.configure(background="lightgreen")

    	self.leftframe.configure(background="lightgreen")

    	self.rightframe.configure(background="lightgreen")

    def set_bg_to_grey(self):

        self.main_window.configure(background="grey")

        self.topframe.configure(background="grey")

        self.set_bg_frame.configure(background="grey")

        self.frame.configure(background="grey")

        self.middleframe.configure(background="grey")

        self.bottomFrame.configure(background="grey")

        self.newframe.configure(background="grey")

        self.leftframe.configure(background="grey")

        self.rightframe.configure(background="grey")

    def set_bg_to_red(self):

        self.main_window.configure(background="red")

        self.topframe.configure(background="red")

        self.set_bg_frame.configure(background="red")

        self.frame.configure(background="red")

        self.middleframe.configure(background="red")

        self.bottomFrame.configure(background="red")

        self.newframe.configure(background="red")

        self.leftframe.configure(background="red")

        self.rightframe.configure(background="red")

    def set_bg_to_pink(self):

        self.main_window.configure(background="pink")

        self.topframe.configure(background="pink")

        self.set_bg_frame.configure(background="pink")

        self.frame.configure(background="pink")

        self.middleframe.configure(background="pink")

        self.newframe.configure(background="pink")

        self.bottomFrame.configure(background="pink")

        self.leftframe.configure(background="pink")

        self.rightframe.configure(background="pink")

    def set_bg_to_brown(self):

        self.main_window.configure(background="brown")

        self.topframe.configure(background="brown")

        self.set_bg_frame.configure(background="brown")

        self.frame.configure(background="brown")

        self.middleframe.configure(background="brown")

        self.bottomFrame.configure(background="brown")

        self.newframe.configure(background="brown")

        self.leftframe.configure(background="brown")

        self.rightframe.configure(background="brown")


    def set_bg_to_green(self):

        self.main_window.configure(background="green")

        self.topframe.configure(background="green")

        self.set_bg_frame.configure(background="green")

        self.frame.configure(background="green")

        self.middleframe.configure(background="green")

        self.bottomFrame.configure(background="green")

        self.newframe.configure(background="green")

        self.leftframe.configure(background="green")

        self.rightframe.configure(background="green")

    def set_bg_to_blue(self):

        self.main_window.configure(background="lightblue")

        self.topframe.configure(background="lightblue")

        self.set_bg_frame.configure(background="lightblue")

        self.frame.configure(background="lightblue")

        self.middleframe.configure(background="lightblue")

        self.bottomFrame.configure(background="lightblue")

        self.newframe.configure(background="lightblue")

        self.leftframe.configure(background="lightblue")

        self.rightframe.configure(background="lightblue")


    def GUI(self):

    	print("<<<<<<<<<<<<< start of GUI >>>>>>>>>>>>>>>>>>>>>")

    	self.main_window = Tk()

    	self.main_window.title("Twitter Sentiment Analysis Desktop Application")

    	self.main_window.geometry("850x650")
    	
    	self.main_window.resizable(width = False , height = False)
    	
    	self.main_window.configure(background = "lightblue")

    	label1 = Label(self.main_window,text="Twitter Sentiment Analysis",fg="blue",bg="skyblue",font=("",15,"bold"))
    	
    	label1.pack(side=TOP,pady=20)

    	self.topframe = Frame(self.main_window,background="lightblue")
    	
    	self.topframe.pack()

    	self.set_bg_frame = Frame(self.topframe,background="lightblue",height=150,width=150)

    	self.set_bg_frame.pack(side = LEFT)

    	darkcolor = Frame(self.set_bg_frame)

    	darkcolor.pack()

    	lightcolor = Frame(self.set_bg_frame)

    	lightcolor.pack()

    	red_image = PhotoImage(file = "image_resource/red.png")
    	   
    	brown_image = PhotoImage(file = "image_resource/brown.png")
    	   
    	pink_image = PhotoImage(file = "image_resource/pink.png")

    	grey_image = PhotoImage(file = "image_resource/grey.png")

    	green_image = PhotoImage(file = "image_resource/green.png")

    	blue_image = PhotoImage(file = "image_resource/blue.png")

    	violet_image = PhotoImage(file = "image_resource/violet.png")

    	orange_image = PhotoImage(file = "image_resource/orange.png")

    	yellow_image = PhotoImage(file = "image_resource/yellow.png")

    	lightgreen_image = PhotoImage(file = "image_resource/lightgreen.png")

    	red_image = red_image.subsample(4,4)
    	   
    	brown_image = brown_image.subsample(4,4)
    	   
    	pink_image = pink_image.subsample(4,4)

    	grey_image = grey_image.subsample(4,4)

    	green_image = green_image.subsample(4,4)

    	blue_image = blue_image.subsample(4,4)

    	violet_image = violet_image.subsample(4,4)

    	orange_image = orange_image.subsample(4,4)

    	yellow_image = yellow_image.subsample(4,4)

    	lightgreen_image = lightgreen_image.subsample(4,4)

    	red_button = Button(darkcolor,image = red_image,command = self.set_bg_to_red)
    	   
    	red_button.pack(side = LEFT)

    	brown_button = Button(darkcolor, image = brown_image,command = self.set_bg_to_brown)
    	   
    	brown_button.pack(side = LEFT)

    	green_button = Button(darkcolor,image = green_image,command = self.set_bg_to_green)
    	   
    	green_button.pack(side = LEFT)

    	orange_button = Button(darkcolor,image = orange_image,command = self.set_bg_to_orange)
    	   
    	orange_button.pack(side = LEFT)

    	violet_button = Button(darkcolor,image = violet_image,command = self.set_bg_to_violet)
    	   
    	violet_button.pack(side = LEFT)

    	pink_button = Button(lightcolor,image = pink_image,command = self.set_bg_to_pink)
    	   
    	pink_button.pack(side = LEFT)

    	grey_button = Button(lightcolor, image = grey_image,command = self.set_bg_to_grey)
    	   
    	grey_button.pack(side = LEFT)

    	blue_button = Button(lightcolor,image = blue_image,command = self.set_bg_to_blue)
    	   
    	blue_button.pack(side = LEFT)

    	yellow_button = Button(lightcolor,image = yellow_image,command = self.set_bg_to_yellow)
    	   
    	yellow_button.pack(side = LEFT)

    	lightgreen_button = Button(lightcolor,image = lightgreen_image,command = self.set_bg_to_lightgreen)
    	   
    	lightgreen_button.pack(side = LEFT)

    	twitter_img = PhotoImage(file="image_resource/twitter.png")

    	twitter_img = twitter_img.subsample(1,1)

    	twitter_button = Button(self.topframe,image = twitter_img,command = self.open_twitter)

    	twitter_button.pack(side = LEFT,padx = (40,60))

    	self.frame = Frame(self.topframe,background="lightblue")

    	self.frame.pack(side = LEFT)

    	label6 = Label(self.frame,text="Trending #tag",fg="red",bg="blue",font=("",12,"bold"))

    	label6.pack(side = TOP , pady = 10)

    	self.topic = StringVar()

    	trending_topics = ttk.Combobox(self.frame , textvariable = self.topic , width = 20, height = 10)

    	trending_topics['values'] = self.trending_tags

    	trending_topics.pack()

    	trending_topics.current(0)

    	trending_topics.bind("<<ComboboxSelected>>",self.select_trending_tag)

    	print("<<<<<<<<<<< top frame completed >>>>>>>>>>>>>>>>")

    	self.label3 = Label(self.main_window,text="Enter Twitter #tag to search",fg="red",bg="yellow",font=("",12,"bold"))
    	
    	self.label3.pack(side=TOP,pady=(25,10))

    	inputframe = Frame(self.main_window,background="black")

    	inputframe.pack()

    	self.radioVar = StringVar(inputframe,"1")

    	eng_lang = Radiobutton(inputframe,text="english",variable = self.radioVar,value = "1",fg = "black",bg="white",font = ("",10,"bold"))

    	eng_lang.pack(side = LEFT)

    	all_lang = Radiobutton(inputframe,text="all",variable = self.radioVar,value = "2",fg = "black",bg="white",font = ("",10,"bold"))

    	all_lang.pack(side = LEFT)

    	self.tag_var = StringVar()

    	self.tag_var.trace("w", lambda name, index, mode, sv=self.tag_var: self.check_tag())

    	self.tag_field = Entry(inputframe,justify=CENTER,width = 35,textvariable = self.tag_var,font = ("verdana","13","bold"))
    	
    	self.tag_field.pack(side = LEFT)

    	self.model_var = StringVar()

    	model_list = ttk.Combobox(inputframe , textvariable = self.model_var , width = 20, height = 10)

    	model_list['values'] = ("textblob.sentiment","NaiveBayesClassifier","RandomForest","DecisionTree","compare all")

    	model_list.pack()

    	model_list.current(0)

    	print("<<<<<<<<<<<<<<<< middle frame completed >>>>>>>>>>>>>>>>>>>>>>")

    	model_list.bind("<<ComboboxSelected>>",self.select_model)

    	self.middleframe = Frame(self.main_window,background="lightblue")
    	
    	self.middleframe.pack()

    	self.search_button = Button(self.middleframe,text="Search",fg="white",bg="black",height=1,width=10,font=("verdana",10,"bold"),state=DISABLED,command = self.main_thread)
    	
    	self.search_button.pack(side = LEFT,padx=5,pady=5)

    	self.clear_button = Button(self.middleframe,text="Clear",fg="white",bg="black",height=1,width=10,font=("verdana",10,"bold"),command = self.clear_tag)
    	
    	self.clear_button.pack(side = LEFT,padx=5,pady=5)

    	self.newframe = Frame(self.main_window,background="lightblue")

    	self.newframe.pack(side = LEFT,padx=(50,0),pady = (0,25))

    	self.leftframe = Frame(self.newframe,background="lightblue")

    	self.leftframe.pack(side = LEFT,padx = (0,10))

    	label7 = Label(self.leftframe,text="#preprocessing",fg="red",bg="yellow",font=("",11,"bold"))

    	label7.pack(side=TOP,pady = (0,10))

    	self.emoji_flag = IntVar()

    	cb1 = Checkbutton(self.leftframe,text = " emoji   ", variable = self.emoji_flag , font = ("",10,"bold"),bg = "lightblue",fg = "black")

    	cb1.select()

    	cb1.pack(side = TOP, pady = (0,10))

    	self.emoticon_flag = IntVar()

    	cb2 = Checkbutton(self.leftframe,text = " emoticon", variable = self.emoticon_flag,font = ("",10,"bold"),bg = "lightblue",fg = "black")
    	
    	cb2.select()

    	cb2.pack(side = TOP, pady = (0,10))

    	self.url_flag= IntVar()

    	cb3 = Checkbutton(self.leftframe,text = " url     ", variable = self.url_flag, font = ("",10,"bold"),bg = "lightblue",fg = "black" )
    	
    	cb3.select()
    	
    	cb3.pack(side = TOP, pady = (0,10))

    	self.hastags_flag = IntVar()

    	cb4 = Checkbutton(self.leftframe,text = " hastags ", variable =  self.hastags_flag, font = ("",10,"bold"),bg = "lightblue",fg = "black")
    	
    	cb4.select()
    	
    	cb4.pack(side = TOP, pady = (0,10))

    	self.handle_flag = IntVar()

    	cb5 = Checkbutton(self.leftframe,text = " handle  ",variable = self.handle_flag,font = ("",10,"bold"),bg = "lightblue",fg = "black")
    	
    	cb5.select()
    	
    	cb5.pack(side = TOP, pady = (0,10))

    	self.rightframe = Frame(self.newframe,background = "lightblue")

    	self.rightframe.pack(side = LEFT)

    	label4 = Label(self.rightframe,text="Select number of tweets to fetch from twitter",fg="red",bg="yellow",font=("",12,"bold"))
    	
    	label4.pack(side=TOP,pady=10)

    	Values = (50,75,100,150,200,250,500,750,1000)

    	self.number_of_tweets = IntVar()

    	choices = ttk.Combobox(self.rightframe,textvariable = self.number_of_tweets,height=10)

    	choices['values'] = Values
    	
    	choices.pack()

    	choices.current(2)

    	choices.bind("<<ComboboxSelected>>",self.select_no_of_tweets)

    	label5 = Label(self.rightframe,text="Select appropriate diagram to dislpay ",fg="red",bg="yellow",font=("",12,"bold"))
    	
    	label5.pack(side=TOP,pady=10)

    	self.bottomFrame = Frame(self.rightframe,background="lightblue",width=700,height=150)
    	
    	self.bottomFrame.pack(side = TOP,pady = 20)

    	piechart_image = PhotoImage(file = "image_resource/piechart.png")
    	
    	scatterplot_image = PhotoImage(file = "image_resource/scatter.png")
    	
    	histogram_image = PhotoImage(file = "image_resource/histogram.png")

    	piechart_image = piechart_image.subsample(2,2)
    	
    	scatterplot_image = scatterplot_image.subsample(2,2)
    	
    	histogram_image = histogram_image.subsample(2,2)

    	self.piechart_button = Button(self.bottomFrame,image = piechart_image,state=DISABLED,command = self.plot_PieChart)
    	
    	self.piechart_button.pack(side = LEFT,padx=20)

    	self.scatterplot_button = Button(self.bottomFrame, image = scatterplot_image,state=DISABLED,command = self.scatter_plot)
    	
    	self.scatterplot_button.pack(side = LEFT,padx=20)

    	self.histogram_button = Button(self.bottomFrame,image = histogram_image,state=DISABLED,command = self.plot_histogram)
    	
    	self.histogram_button.pack(side = LEFT,padx=20)

    	label8 = Label(self.newframe,text="#Dataset used",fg="red",bg="yellow",font=("",12,"bold"))

    	label8.pack(side=TOP,pady=(0,20))

    	self.btn1 = Button(self.newframe,text="fetched tweets",bg="black",fg="white",font=("",10,"bold"),state=DISABLED,command = self.open_fetched_tweets)

    	self.btn1.pack(side=TOP,pady = (0,20))

    	btn2 = Button(self.newframe,text="train dataset ",bg="black",fg="white",font=("",10,"bold"),command = self.open_training_dataset)

    	btn2.pack(side=TOP,pady = (0,20))

    	btn3 = Button(self.newframe,text=" test dataset ",bg="black",fg="white",font=("",10,"bold"),command = self.open_testing_dataset)

    	btn3.pack(side=TOP,pady = (0,20))

    	btn4 = Button(self.newframe,text="   log file   ",bg="black",fg="white",font=("",10,"bold"),command = self.open_log_file)

    	btn4.pack(side=TOP,pady = (0,20))

    	print("<<<<<<<<<<<<<<<<<<<<<< bottomFrame completed >>>>>>>>>>>>>>>>>>>>>>>")

    	self.main_window.mainloop()

if __name__ == "__main__": 

    # execution begin from here 

    # creating object of TwitterClient Class 
    tc = TwitterClient()

    print(tc.__doc__)

    thread1 = Thread(target = tc.load_models()).start()

    thread2 = Thread(target = tc.GUI()).start()
