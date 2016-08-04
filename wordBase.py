import time
import urllib2
from urllib2 import urlopen
import re
import cookielib
from cookielib import CookieJar
import datetime
import sqlite3
import nltk


# Opens up the urllib2 so that we can get information from
# thesaurus.com wich is a synonym-website
cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

# Connects to the knowledgeBase database.
conn = sqlite3.connect('knowledgeBase.db')
c = conn.cursor()

def pos_words():
    # This function uses the positive/negative word list that is taken from
    # Minqing Hu and Bing Liu. "Mining and Summarizing Customer Reviews." 
    # Proceedings of the ACM SIGKDD International Conference on Knowledge 
    # Discovery and Data Mining (KDD-2004), Aug 22-25, 2004, Seattle, 
    # Washington, USA.
    pos_words = open('positive-words.txt', 'r')
    x = 1
    for line in pos_words:
        # Strip each line so we dont have to deal with \n in the words
        word = line.strip()
        # Send each word in to the mainloop
        main(word)
        print 'Positive word count: ' + str(x)
        x += 1
        time.sleep(5)

def main(word):
    # Since this is for the positive word list the WordValuable is 1.
    # For Neutral it's 0, and for Negative it's -1
    WordVal = 1
    try:
        # connecto to the page for the specifik word
        page = 'http://thesaurus.com/browse/'+word+'?s=t'
        print page
        sourceCode = opener.open(page).read()

        try:
            # Split the data up because we don't need all the html-code
            synoNym = sourceCode.split('<div class="synonym-description">')
            x=1
            while x < len(synoNym):
                try:
                    # This splits it again so now we have a start-split and an end-split
                    synoNymSplit = synoNym[x].split('complexity="1" data-length="1"')[1]
                    # Using regular-expressions to just get the text(word) without
                    # any html-tags.
                    SynoNyms = re.findall(r'\.*?"text">(\w*?)</span>', synoNymSplit)
                    
                    
                    for eachSyn in SynoNyms:
                        # Selects the table from the database and look for that word
                        query = "SELECT * FROM wordVals WHERE word =?"
                        c.execute(query, [(eachSyn)])
                        data = c.fetchone()
                        
                        if data is None:
                            # if word isn't in the database, then add it and it's value
                            print 'not here yet, let us add it'
                            c.execute("INSERT INTO wordVals (word, value) VALUES (?,?)",
                                      (eachSyn, WordVal))
                            conn.commit()

                        else:
                            # it the word is in the database, just print and pass
                            print 'word already here!'

                except Exception, e:
                    print str(e)
                    print "failed in 3rd try"

                x+=1

        except Exception, e:
            print str(e)
            print "failed 2nd try"
        
    except Exception, e:
        print str(e)
        print "failed the main loop"

# To run this script we use this(when adding negative we use neg_words()
# wich is basically the same function, just different word-list.
pos_words()

conn.commit()
