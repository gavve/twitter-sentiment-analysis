import sqlite3
import time

conn = sqlite3.connect('knowledgeBase.db')
c = conn.cursor()

negativeWords = []
positiveWords = []


sql = "SELECT * FROM wordVals WHERE value =?"


def loadWordLists():
    for negRow in c.execute(sql, [-1]):
        negativeWords.append(negRow[0])
    print 'negative words loaded'

    for posRow in c.execute(sql, [1]):
        positiveWords.append(posRow[0])
    print 'positive words loaded'
    

def Sentiment():
    readFile = open('positiveIMDB.txt', 'r').read()

    sentCounter = 0

    for eachPosWord in positiveWords:
        if eachPosWord in readFile:
            sentCounter += .3

    for eachNegWord in negativeWords:
        if eachNegWord in readFile:
            sentCounter -= 1.3

    if sentCounter > 0:
        print "this text is positive"

    if sentCounter == 0:
        print "this text is neutral.."

    if sentCounter < 0:
        print "this text is negative"

    print sentCounter

loadWordLists()
Sentiment()

