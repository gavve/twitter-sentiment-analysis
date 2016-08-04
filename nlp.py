import nltk
import re
import time
import sqlite3

exampleArray = ['The incredibly intimidating NLP scares people away who are sissies.']

#Connecting to the database
conn = sqlite3.connect('knowledgeBase.db')
c = conn.cursor()


sql = "SELECT tweetEntity FROM knowledgeBase"

c.execute(sql)

data = c.fetchall()
contentArray = []

for tweet in data:
    contentArray.append(tweet[0])
conn.commit()


def processLanguage():
    try:
        for item in contentArray:
            tokenized = nltk.word_tokenize(item)
            tagged = nltk.pos_tag(tokenized)
            print tagged


            namedEnt = nltk.ne_chunk(tagged)
            namedEnt.draw()
            
            

            #time.sleep(555)


    except Exception, e:
        print str(e)



processLanguage()
