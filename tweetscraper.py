import sys
from bs4 import BeautifulSoup
import urllib2 
import os
import time 
import re

def parse(s): 
    reduce1 = re.findall(">.*?<", s)
    new_s = ""
    for st in reduce1: 
        st2 = st[1:-1]
        if st2[:4] != "http":
            new_s += st2.lower()
        
    return new_s
def writeToSingleFile(path, fn): 
    text_file = open(fn, "w") 
    for filename in os.listdir(path):
        new_p = path + "\\" + filename 
        with open(new_p) as f:
            cdnpoli = f.readlines()
            for line in cdnpoli: 
                s1 = parse(line) 
                text_file.write("%s\n" %s1)

def get_subtopics(soup):
    guideText = soup.findAll('span', {"class":"guideText"})
    
    sub_topics = []
    for guide in guideText:
        sub_topics.append(str(guide.contents[0]))
    
    print sub_topics

def get_liked(soup): 
    
    Tweets = soup.findAll('p')
    return Tweets
    

def query_twitter(query_term='art'):
    response = urllib2.urlopen(url)
    html_page = response.read()
    soup = BeautifulSoup(html_page)
    return soup
    
def save_files(urlList, pth,name): 
    directory = pth + name 
    if not os.path.exists(directory):
        os.makedirs(directory)
    directory += "\\"
    for i in range(len(urlList)):
        url = urlList[i]
        filename = directory + "pic" + str(i) + ".jpg"
        fo = open(filename, "w") 
        im = urllib2.urlopen(url)
        

def enter_taglist(): 
    s = "" 
    tag_list = []
    while s !="fin": 
        s = raw_input("Please enter a tag you would like to find tweets on, or the word 'fin' if you are finished: ")
        tag_list.append(s)
        
    return tag_list[:-1]


if __name__ == '__main__':
    print "hi"
    cdnpoli = [] 
    pth = raw_input("Please enter a fresh directory which you would like to save the tweets to: ") 
    try:
        os.makedirs(pth)
    except WindowsError as e: 
        print "Please enter a directory path that doesn't already exist"
        pth = raw_input("Please enter a fresh directory which you would like to save the tweets to: ") 

    #EXAMPLE HASHTAG LIST BELOW
    #hashtag_list = ["harper", "cdnpoli", "elxn42", "stevenharper", "justintrudeau",
    #"trudeau", "mulcair", "thomasmulcair", "tommulcair", "ndp", "Conservative", "Liberal", 
    #"cpc", "lpc", "realchange", "justnotready", "primeminister", "elxn42"] 
    #a
    hashtag_list = enter_taglist() 
    timeInt = raw_input("Please enter a time interval you would like to scrap tweets after i.e. 60 = 1m scrapes the most recent tweets every minute for as many minutes as specified in the next step: ") 
    repNum = raw_input("Please enter the multiple of times you would like to scrape tweets after the specified time interval: ") 
    baseURL = "https://twitter.com/hashtag/%s?f=tweets&vertical=default"
    for i in range(int(repNum)): 
        time.sleep(float(timeInt))
        for tag in hashtag_list:
            url = baseURL %tag
            sup = query_twitter()
            x = get_liked(query_twitter())
            cdnpoli.append(x)
            ss = tag + str(i) + "10-12"    
            fn = pth + "\\" + "%s.txt" %str(ss) 
            text_file = open(fn, "w") 
            for item in x: 
                s1 = str(item)
                text_file.write("%s\n" %s1)
                
    print("finished, files saved to %s successfully" %pth) 
    fn = raw_input("Please enter a filename you would like the tweets saved into (no need to add .txt): ") 
    fn = pth + "\\" + fn + ".txt" 
    writeToSingleFile(pth, fn) 
    with open(fn) as f:
        tweets = f.readlines() 
        unique = list(set(tweets))
    tf = open(fn, "w")
    for item in unique: 
        tf.write("%s\n" %item)
    
    

        
    