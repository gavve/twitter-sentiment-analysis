import urllib2
from urllib2 import urlopen
import re
import cookielib
from cookielib import CookieJar
import datetime
import sqlite3
import nltk
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time

ckey = 'Z1nSU52hbZysLZEjZx3Tyw'
csecret = 'XExquBNXBCEEpvTTVUgKjB6IoqOA4N5mKIm1nBs'
atoken = '1364230326-1PjnRMfyCh802GFdmGmZlpv0cKAmZmXHAmHlxVz'
asecret = 'f3ethELCYoTvyhicJYQ8nVfDAgMvgPxnrNjTxFLuMGick'

#Connecting to the database
conn = sqlite3.connect('knowledgeBase.db')
c = conn.cursor()
#def createDB():
#    c.execute("CREATE TABLE knowledgeBase(unix, dateStamp, tweetEntity, relatedWord)")

class listener(StreamListener):

    def on_data(self, data):
        try:
            #print data

            # split the tweet to collect the actual tweet
            tweet = data.split(',"text":"')[1].split('","source')[0]
            processor(tweet)
            # including the time stamp for each tweet
            saveThis = []
            #tweetInString = str(time.time())+'::'+tweet
            #tweetTime = tweetInString.split('::')[0]
            #tweetContent = tweetInString.split('::')[1]

            #process = saveThis[tweetTime, tweetContent]
            #print process
            
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
        tokenized = nltk.word_tokenize(data)
        tagged = nltk.pos_tag(tokenized)
        namedEnt = nltk.ne_chunk(tagged)
        print namedEnt

        #entities = re.findall(r'\s(.*?)NN/', str(namedEnt))
        #     ('
        #descriptives = re.findall(r'\(\'(\w*)\'.\s\'JJ\w?\'',str(tagged))
        if len(entities) > 1:
            pass
        elif len(entities) == 0:
            pass
        else:
            print 'Named: ', entities[0]
            print 'Description: '
            for eachDesc in descriptives:
                print eachDesc
                currentTime = time.time()
                dateStamp = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H:%M:%S')
                tweetEntity = entities[0]
                relatedWord = eachDesc
                c.execute("INSERT INTO knowledgeBase (unix, dateStamp, tweetEntity, relatedWord) VALUES (?,?,?,?)",
                          (currentTime, dateStamp, tweetEntity, relatedWord))

                conn.commit()


                

    except Exception, e:
        print 'failed in the first try of processor'
        print str(e)

#createDB()
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["Barack Obama"])

