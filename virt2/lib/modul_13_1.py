#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import getopt
import urllib
import urllib2
import xml_tree as xtre
import mechanize
from BeautifulSoup import BeautifulSoup

def loadAlegro(obiekt):
    #br = mechanize.Browser()
    #r = br.open("http://allegro.pl/")
    #r = br.open("http://allegro.pl/listing/listing.php?string=CANNON+1100D")
    #html = r.read()
    #Pokaz zrzdło
    #print br.response().read()
    #Show the html title
    #print br.title()
    #print br.geturl()
    a_url = 'http://allegro.pl/listing/listing.php?offerTypeBuyNow=1&order=p&standard_allegro=1&string='+obiekt
    #a_url = 'http://allegro.pl/listing/listing.php?standard_allegro=1&offerTypeBuyNow=1&string='+obiekt
    response = urllib2.urlopen(a_url)
    html = response.read()
    #print html
    #f=open('aa', 'w')
    #print "zapisz do pliku"
    #f.write(str(html))


    #pomidorowa = BeautifulSoup(html)
    #kluski = html.find("span",{"class" : "item-ico item-sa icon-as"})
    #for kluska in kluski:
        #print kluska.contents[0]
    soup = BeautifulSoup(html)
    #print soup.find("div", {"class" : "excerpt"})
    #html3 = soup.findAll("section", {"class" : "offers"})[1]
    html4= soup.findAll("section", {"class" : "offers"})[1].find("div", {"class" : "excerpt"})
    #html4 = html3.find("div", {"class" : "excerpt"})
    cena = html4.find("span", {"class" : "buy-now dist"}).span.nextSibling

    #html3 = soup.findAll('h2', {"class" : "listing-header"})[1]
    #html3 = soup.findAll("div", {"class" : "excerpt"})
    html2 = soup.find("div", {"class" : "excerpt"})
    #print html3
    #print soup.find("span",{"class" : "offers"})
    #f2=open('aaa.html', 'w')
    #print "zapisz do pliku"
    #f2.write(str(html4))
    #print"=========="
    print cena
    #cena = html2.find("span", {"class" : "buy-now dist"}, {"class" : "label"}).span.nextSibling

    #link = html2.find(html2.find('a', href=obiekt))
    #print cena
    link = html4.find("div", {"class" : "details"}).header.h2.a['href']
    #print link
    print "www.allegro.pl"+link
    #<a href="/dekielek-do-korpusu-canon-1100d-1000d-650d-600d-1d-i3395172116.html">
    #print html4.div

    #print html2('span', {"class" : "buy-now dist"})[0].string

    #link = soup.html.article.div.a['href']
    #link = soup.html.article.div.a['href']
    #print "www.allegro.pl"+link

def usage():
        usage = """
        -h --help                 Prints this help
        -o --objects              Print objects
        -a --argument -API key    Print argument
        """
        print usage

def end():
    sys.exit(2)

def main():
    """main
    >>>main()

    """
    i = 0
    try:
        opts, argsy = getopt.getopt(sys.argv[1:], 'ho:a:', ["help"])

    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, args in opts:

        if opt in ("--help", "-h"):
            return usage()

        if opt in ("-o"):
            nazwa = args
            i = i + 1
        else:
            print args
            nazwa = args
            print nazwa

    if i == 1:
        print nazwa
        return loadAlegro(nazwa)

    if i == 0:
        nazwa = sys.argv[1]
        print nazwa

        return loadAlegro(nazwa)


if __name__ == '__main__':

    main()