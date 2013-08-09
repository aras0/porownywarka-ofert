#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import re
import os
import urllib2
import urlparse
import django
import threading
import sqlite3 as sqlite
import robotparser
from parser import Parser
# Try to import psyco for JIT compilation
try:
    import psyco
    psyco.full()
except ImportError:
    print "Continuing without psyco JIT compilation!"

"""
The program should take arguments
1) database file name
2) start url
3) crawl depth
4) keyword 
5) verbose (optional)
Start out by checking to see if the args are there and
set them to their variables
"""
if len(sys.argv) < 5:
    sys.exit("Not enough arguments!")
else:
    dbname = sys.argv[1]
    starturl = sys.argv[2]
    crawldepth = int(sys.argv[3])
    searchWord = sys.argv[4]
if len(sys.argv) == 6:
    if (sys.argv[5].upper() == "TRUE"):
        verbose = True
    else:
        verbose = False
else:
    verbose = False
# urlparse the start url
#print starturl
surlparsed = urlparse.urlparse(starturl)
hostname = surlparsed.netloc

#delete old file! - very ugly line, kill it!
os.remove(dbname)

# Connect to the db and create the tables if they don't already exist
connection = sqlite.connect(dbname)
cursor = connection.cursor()
# crawl_index: holds all the information of the urls that have been crawled
cursor.execute('CREATE TABLE IF NOT EXISTS crawl_index (crawlid INTEGER, parentid INTEGER, url VARCHAR(256), title VARCHAR(256), price VARCHAR(256),currency VARCHAR(256), date VARCHAR(256) )')
# queue: this should be obvious
cursor.execute('CREATE TABLE IF NOT EXISTS queue (id INTEGER PRIMARY KEY, parent INTEGER, depth INTEGER, url VARCHAR(256))')
# status: Contains a record of when crawling was started and stopped. 
# Mostly in place for a future application to watch the crawl interactively.
cursor.execute('CREATE TABLE IF NOT EXISTS status ( s INTEGER, t TEXT )')
connection.commit()

# Compile keyword and link regex expressions
keywordregex = re.compile('<meta\sname=["\']keywords["\']\scontent=["\'](.*?)["\']\s/>')
linkregex = re.compile('<a\s*href=[\'|"](.*?)[\'"].*?>')
crawled = []

# set crawling status and stick starting url into the queue
cursor.execute("INSERT INTO status VALUES ((?), (?))", (1, "datetime('now')"))
cursor.execute("INSERT INTO queue VALUES ((?), (?), (?), (?))", (None, 0, 0, starturl))
connection.commit()

web_parser = Parser()

def remove_polish(text):
    no_polish_text = text.replace("Ăł","o").replace("Ĺ","l").replace("Ä","a").replace("Ä","e").replace("Ä","c").replace("Ĺ","n").replace("Ĺ","s").replace("Ĺş","z").replace("Ĺź","z")
    no_polish_text = no_polish_text.replace("Ă","O").replace("Ĺ","L").replace("Ä","A").replace("Ä","E").replace("Ä","C").replace("Ĺ","N").replace("Ĺ","S").replace("Ĺš","Z").replace("Ĺť","Z")   
    return no_polish_text

# insert starting url into queue

class threader ( threading.Thread ):
    
    # Parser for robots.txt that helps determine if we are allowed to fetch a url
    rp = robotparser.RobotFileParser()

    """
    run()
    Args:
        none
    the run() method contains the main loop of the program. Each iteration takes the url
    at the top of the queue and starts the crawl of it. 
    """
    def run(self):
        while 1:
            try:
                # Get the first item from the queue
                cursor.execute("SELECT * FROM queue LIMIT 1")
                crawling = cursor.fetchone()
                # Remove the item from the queue
                cursor.execute("DELETE FROM queue WHERE id = (?)", (crawling[0], ))
                connection.commit()
                if verbose:
                    print crawling[3]
            except KeyError:
                raise StopIteration
            except:
                pass
            
            # if theres nothing in the que, then set the status to done and exit
            if crawling == None:
                cursor.execute("INSERT INTO status VALUES ((?), datetime('now'))", (0,))
                connection.commit()
                sys.exit("Done!")
            # Crawl the link
            self.crawl(crawling)
        
    """
    crawl()
    Args:
        crawling: this should be a url
    
    crawl() opens the page at the "crawling" url, parses it and puts it into the databes.
    It looks for the page title, keywords, and links.
    """
    def crawl(self, crawling):
        # crawler id
        cid = crawling[0]
        if verbose:
            print cid
        # parent id. 0 if start url
        pid = crawling[1]
        # current depth
        curdepth = crawling[2]
        # crawling urL
        curl = crawling[3]
        # Split the link into its sections
        url = urlparse.urlparse(curl)
        
        #correct not openable link - given as relative
        url = urlparse.urlparse(curl)   

        try:
            # Have our robot parser grab the robots.txt file and read it
            self.rp.set_url('http://' + url[1] + '/robots.txt')
            self.rp.read()
        
            # If we're not allowed to open a url, return the function to skip it
            if not self.rp.can_fetch('PyCrawler', curl):
                if verbose:
                    print curl + " not allowed by robots.txt"
                return
        except:
            pass
            
        try:
            # Add the link to the already crawled list if its not on list
            if curl not in crawled: 
                crawled.append(curl.decode('utf-8'))
            else: 
                return
        except MemoryError:
            # If the crawled array is too big, deleted it and start over
            del crawled[:]
        try:
            #check if link contains word given without polish letters           
            searchWordPos = curl.find(remove_polish(searchWord))
            if searchWordPos == -1: 
                return
            # Create a Request object
            request = urllib2.Request(curl)
            # Add user-agent header to the request
            request.add_header("User-Agent", "PyCrawler")
            # Build the url opener, open the link and read it into msg
            opener = urllib2.build_opener()
            msg = opener.open(request).read()
            
        except:
            # If it doesn't load, skip this url
            print "Can't load: " + curl
            return

        # Get the links
        links = linkregex.findall(msg)
        # queue up the links
        self.queue_links(curl, links, cid, curdepth)
        
        # here we start parser for results
        [ptitle,pdate,pprice,pcurrency] = web_parser.run(msg)
        
        # add data found to base    
        try:
                
            cursor.execute("INSERT INTO crawl_index VALUES( (?), (?), (?), (?), (?),(?), (?) )", (cid, pid, curl.decode('utf-8'), ptitle.decode('utf-8'), pprice.decode('utf-8'),pcurrency.decode('utf-8'), pdate.decode('utf-8')))
            connection.commit()
        except:
            print ptitle, pprice, pdate     
            pass
        
## Start parser instead of code below
    """     
            # Find what's between the title tags
            startPos = msg.find('<title>')
            if startPos != -1:
                endPos = msg.find('</title>', startPos+7)
                if endPos != -1:
                    title = msg[startPos+7:endPos]
                
        
            # Start keywords list with whats in the keywords meta tag if there is one
            keywordlist = keywordregex.findall(msg)
            if len(keywordlist) > 0:
                keywordlist = keywordlist[0]
            else:
                keywordlist = ""
                
            try:
                #check if title contains word given         
                cursor.execute("INSERT INTO crawl_index VALUES( (?), (?), (?), (?), (?) )", (cid, pid, curl, title.decode('utf-8'), keywordlist.decode('utf8')))
                connection.commit()
            except:
                print 'BUG!'        
                pass
    """ 
##          
            
    def queue_links(self, url, links, cid, curdepth):
        if curdepth < crawldepth:
            # Read the links and inser them into the queue
            for link in links:
                cursor.execute("SELECT url FROM queue WHERE url=?", [link])
                for row in cursor:
                    if row[0].decode('utf-8') == url:
                        continue
                #relative link - add http and host to it
                if link.startswith('/'):
                    link = 'http://' + hostname + link
                #link starts with hash - on this page only              
                elif link.startswith('#'):
                    continue
                #link starts with javascript - no use to search it
                elif link.startswith('javascript:'):
                    continue
                elif not link.startswith('http'):
                    link = urlparse.urljoin(url,link)
                
                if link not in crawled:
                    try:
                        cursor.execute("INSERT INTO queue VALUES ( (?), (?), (?), (?) )", (None, cid, curdepth+1, link))
                        connection.commit()
                    except:
                        print "Alredy crawled!"
                        continue
        else:
            pass

if __name__ == '__main__':
    # Run main loop
    threader().run()
