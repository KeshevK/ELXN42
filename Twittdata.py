import csv, string 
import nltk, nltk.classify.util, nltk.metrics
from nltk.classify import MaxentClassifier
from nltk.corpus import nps_chat  
from nltk.corpus.reader.nps_chat import NPSChatCorpusReader
from nltk.corpus import sentiwordnet as swn 
from nltk.corpus import stopwords 
#from nltk.metrics import BigramAssocMeasures
#from nltk.probability import FreqDist, ConditionalFreqDist
from sklearn.feature_extraction.text import CountVectorizer
import textmining 
import re
from collections import Counter

def classybroad(): 
    with open('C:\\Users\\Keshev\\Documents\\BDU\\training.1600000.processed.noemoticon.csv', 'rb') as csvfile:
    #with open('C:\\Users\\Keshev\\Documents\\BDU\\testdata.manual.2009.06.14.csv', 'rb') as csvfile:
        sentiments = csv.DictReader(csvfile, header=False)
        positive = [] 
        negative = []
        tdms = [] 
        TDM = textmining.TermDocumentMatrix()
        i = 0
        j=0  
        for row in sentiments:
            if i<6000:
                if row['0'] == '0': 
                    tw = row["@switchfoot http://twitpic.com/2y1zl - Awww, that's a bummer.  You shoulda got David Carr of Third Day to do it. ;D"].lower() 
                    tw = tw.split(" ")[1:] 
                    DM = Counter(tw)
                    #TDM.add_doc(''.join(tw.strip())) 
                    negative.append((DM, 0))
                    i+=1 
            elif j<6000 and i>=6000: 
                if row['0'] == '4': 
                    tw = row["@switchfoot http://twitpic.com/2y1zl - Awww, that's a bummer.  You shoulda got David Carr of Third Day to do it. ;D"]
                    tw = tw.split(" ")[1:] 
                    DM = Counter(tw)
                    #TDM.add_doc(''.join(tw.strip())) 
                    positive.append((DM, 1))
                    j+=1 
                    
            else: 
                break 
                
        
        training = positive + negative
        algorithm = nltk.classify.MaxentClassifier.ALGORITHMS[0]
        classifier = nltk.MaxentClassifier.train(training, algorithm,max_iter=3)
        
        #       negative.append(row["@switchfoot http://twitpic.com/2y1zl - Awww, that's a bummer.  You shoulda got David Carr of Third Day to do it. ;D"])
        #   elif row['0'] == '4': 
        #     positive.append(row["@switchfoot http://twitpic.com/2y1zl - Awww, that's a bummer.  You shoulda got David Carr of Third Day to do it. ;D"]) 
    
    
def tokenize(s): 
    #pre-process s and return a dict of new tokens with word counts
    pass
    

 
def cleanup(s): 
    '''remove punctuation and unwanted characters or hyperlinks from list of string s'''
    return s.translate(string.maketrans("",""), string.punctuation)
            
def get_bigr(): 
    r = NPSChatCorpusReader 
    pass
    
def _clean_up(word_list): 
    '''Return a list of strings cleaned_words which consists of the words from a list of 
    strings word_list with stop words and punctuation removed'''
    cleaned_words = [cleanup(word) for word in word_list if (word not in stopwords.words('english') and 
                     word not in list(string.punctuation))]
    return cleaned_words
    
def format_train(trainData):
    '''Return a list of Tuples of tweets in csv.DictReader trainData
    where the first entry is a dictionary of wordcounts and the second 
    is the class value'''
    tweet_list = [] 
    for row in trainData: 
        tweet = row["text"]
        twl = _clean_up(tweet.split())
        cat = row["class"]
        features = Counter(twl) 
        if cat == "0": 
            tup = (features, "negative") 
        else: 
            tup = (features, "positive") 
        tweet_list.append(tup) 
    return tweet_list
    
with open('C:\\Users\\Keshev\\Documents\\BDU\\Sentiment140.200000.csv', 'rb') as csvfile:
    trainData = csv.DictReader(csvfile) 
    dat = format_train(trainData)


train1 = dat[:80000] + dat[120000:]
test = dat[80000:120000] 
algorithm = nltk.classify.MaxentClassifier.ALGORITHMS[0]
classifier = nltk.MaxentClassifier.train(train1, algorithm,max_iter=3)
right = 0 
for case in test: 
    cla = classifier.classify(case[0])
    if cla == case[1]: 
        right += 1 
