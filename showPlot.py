import re
import datetime
import sqlite3


#Connecting to the database
conn = sqlite3.connect('knowledgeBase.db')
c = conn.cursor()


sql = "SELECT analyzed FROM knowledgeBase"

c.execute(sql)

data = c.fetchall()

# Negative data
neg = 0
negForAvg = 0

# Positive data
pos = 0
posForAvg = 0

# Neutral data
neu = 0

for line in data:
    x = float(0.0)
    if line[0] < x:
        print "One negative: ", line[0]
        neg += 1
        negForAvg += line[0]
    if line[0] == x:
        print "One neutral: ", line[0]
        neu += 1
    if line[0] > x:
        print "One positive: ", line[0]
        pos += 1
        posForAvg += line[0]

print "We got this many positive", pos
print "We got this many neutral", neu
print "We got this many negative", neg

# Ecuation to get the avarage sentiment of the tweets from the DB
totScore = posForAvg - negForAvg

finalScore = totScore / (pos + neg + neu)

print "### - Total Score : ", totScore
print "##################################"
print "### - Final score (Total Score / number of tweets): ", finalScore

conn.commit()

    
