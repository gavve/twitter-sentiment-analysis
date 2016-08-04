import time
import urllib2
from urllib2 import urlopen
import re
import cookielib
from cookielib import CookieJar
import datetime
import sqlite3
import nltk

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0')]


conn = sqlite3.connect('knowledgeBase.db')
c = conn.cursor()


visitedLinks = []

def createDB():
    c.execute("CREATE TABLE knowledgeBase(unix, dateStamp, namedEntity, relatedWord)")



def processor(data):
    try:
        tokenized = nltk.word_tokenize(data)
        tagged = nltk.pos_tag(tokenized)
        namedEnt = nltk.ne_chunk(tagged, binary=True)

        entities = re.findall(r'NE\s(.*?)/', str(namedEnt))
        #     ('
        descriptives = re.findall(r'\(\'(\w*)\'.\s\'JJ\w?\'',str(tagged))
        if len(entities) > 1:
            pass
        elif len(entities) == 0:
            pass
        elif str(entities) == '_blank':
            pass
        else:
            print 'Named: ', entities[0]
            print 'Description: '
            for eachDesc in descriptives:
                print eachDesc
                currentTime = time.time()
                dateStamp = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H:%M:%S')
                namedEntity = entities[0]
                relatedWord = eachDesc
                c.execute("INSERT INTO knowledgeBase (unix, dateStamp, namedEntity, relatedWord) VALUES (?,?,?,?)",
                          (currentTime, dateStamp, namedEntity, relatedWord))

                conn.commit()


                

    except Exception, e:
        print 'failed in the first try of processor'
        print str(e)



def huffingtonRSSvisit():
    try:
        page = 'http://feeds.huffingtonpost.com/huffingtonpost/raw_feed'
        sourceCode = opener.open(page).read()
        try:
            links = re.findall(r'<link.*href=\"(.*?)\"', sourceCode)
            for link in links:
                if '.rdf' in link:
                    pass
                
                elif link in visitedLinks:
                    print "Already visited this link..."
                    
                else:
                    visitedLinks.append(link)
                    print 'visiting the link'
                    print '####################'

                    linkSource = opener.open(link).read()
                    linesOfInterest = re.findall(r'<p>(.*?)</p>', str(linkSource))
                    print 'Content: '
                    for eachLine in linesOfInterest:
                        if '<img width' in eachLine:
                            pass
                        elif '<a href=' in eachLine:
                            pass
                        else:
                            processor(eachLine)


        except Exception, e:
            print "failed 2nd loop of huffingtonRSS"
            print str(e)
        


    except Exception, e:
        print "failed main loop of huffingtonRSS"
        print str(e)

createDB()
while 1 < 2:
    currentTime = time.time()
    dateStamp = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H:%M:%S')
    huffingtonRSSvisit()

    time.sleep(5)
    print 'sleeping'
    print dateStamp
