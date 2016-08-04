import re
import datetime
import sqlite3
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time

#Connecting to the database
conn = sqlite3.connect('knowledgeBase.db')
c = conn.cursor()

#### - Loading in the negative/positive wordlists - ####
negativeWords = []
positiveWords = []

sql = "SELECT * FROM wordVals WHERE value =?"

def loadWordLists():
    for negRow in c.execute(sql, [-1]):
        negativeWords.append(negRow[0])
    print 'negative words loaded' + str(len(negativeWords))

    for posRow in c.execute(sql, [1]):
        positiveWords.append(posRow[0])
    print 'positive words loaded' + str(len(positiveWords))

#### - End of loading negative/positive wordlists - ####

ckey = 'Z1nSU52hbZysLZEjZx3Tyw'
csecret = 'XExquBNXBCEEpvTTVUgKjB6IoqOA4N5mKIm1nBs'
atoken = '1364230326-1PjnRMfyCh802GFdmGmZlpv0cKAmZmXHAmHlxVz'
asecret = 'f3ethELCYoTvyhicJYQ8nVfDAgMvgPxnrNjTxFLuMGick'


class listener(StreamListener):

    def on_data(self, data):
        try:
            # split the tweet to collect the actual tweet
            tweet = data.split(',"text":"')[1].split('","source')[0]

            # First delete the username from the tweetcontent
            deleteUsername = re.sub(r'@(.*):', '', tweet)

            # After deleting the http-links we only have the text of the tweet
            onlyTweetText = re.sub(r'(http)(.*)', '', deleteUsername)
            print "---------------"
            print tweet

            # send the tweet to the processor
            processor(onlyTweetText)
            
            #open up the database and where we save the timestamp+tweet
            return True
        except BaseException, e:
            print 'failed because internet,',str(e)
            #make it sleep for a while then reconnect
            time.sleep(5)

    def on_error(self, status):
        print status


def processor(data):
    try:
        # Making the Sentiment Analysis
        analyzedScore = 0
            #print row[0]
        for eachPosWord in positiveWords:
            if eachPosWord in data:
                analyzedScore += .42
        for eachNegWord in negativeWords:
            if eachNegWord in data:
                analyzedScore -= .575

        if analyzedScore > 0:
            #print "this tweet is positive: ", data
            pass

        if analyzedScore == 0:
            #print "this tweet is neutral: ", data
            pass

        if analyzedScore < 0:
            #print "this tweet is negative: ", data
            pass

        
        # Insert the data to the Database
        currentTime = time.time()
        dateStamp = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H:%M:%S')
        tweetContent = data
        c.execute("INSERT INTO knowledgeBase (unix, dateStamp, tweetEntity, analyzed) VALUES (?,?,?,?)",
                  (currentTime, dateStamp, tweetContent, analyzedScore))

        conn.commit()
                

    except Exception, e:
        print 'failed in the first try of processor'
        print str(e)


loadWordLists()

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["florida"])

