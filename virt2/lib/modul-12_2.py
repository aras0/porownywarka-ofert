# -*- coding: utf-8 -*-

import sys
from xml.dom.minidom import parseString
import urllib , urllib2
import lxml.etree

#wywolanie
# python modul-12_2.py canon1100d a8839b1180ea00fa1cf7c6b74ca01bb5

#zapytanie do Api 
#http://api.nokaut.pl/?format=FORMAT&key=KLUCZ_API&method=METODA&PARAMETR1=WARTOSC&PARAMETR2=WARTOSC

#method_download = nokaut.product.getByKeyword
#przedmiot = "canon1100d"
przedmiot = sys.argv[1]

#key_number = "a8839b1180ea00fa1cf7c6b74ca01bb5"
key_number = sys.argv[2]
#nokaut.Product - produkty, a nokaut.Price - ceny
#http://api.nokaut.pl/?format=xml&key=KLUCZ_API&method=metoda&keyword=przedmiot

#http://api.nokaut.pl/?format=xml&key=KLUCZ_API&method=metoda&keyword=canon250d
#http://api.nokaut.pl/?format=rest&key=102c0d165e3d544d52f9ce66c2a430a9&method=nokaut.product.getByKeyword&keyword=canon450d
#http://api.nokaut.pl/?format=xml&key=a8839b1180ea00fa1cf7c6b74ca01bb5&method=nokaut.product.getByKeyword&keyword&keyword=canon1000
#xmlTag = dom.getElementsByTagName('tagName')[0].toxml()
#xmlTag = dom.getElementsByTagName('name')[0].toxml()
#xmlData=xmlTag.replace('<name>','').replace('</name>','')
a_url = 'http://api.nokaut.pl/?format=xml&key=' + key_number + '&method=nokaut.product.getByKeyword&keyword='+przedmiot+'&filters[price_min]'


#http://api.nokaut.pl/?format=xml&key=a8839b1180ea00fa1cf7c6b74ca01bb5&method=nokaut.product.getByKeyword&keyword=canon110d

file = urllib.urlopen(a_url)
data = file.read()

file.close()

dom = parseString(data)

#def download_nokaut():

#a_url = 'http://api.nokaut.pl/?format=xml&key=' + key_number + '&method=nokaut.product.getByKeyword&keyword='+przedmiot

#for i in file:
	#xmlTag = dom.getElementsByTagName('name')[i].toxml()

#xmlTag = dom.getElementsByTagName('name')[0].toxml()
#xmlData=xmlTag.replace('<name>','').replace('</name>','')


#for i in cNodes[0].getElementsByTagName("items"):
slownik=dict()
price_min=float()
cNodes = dom.childNodes
price_min = dom.getElementsByTagName("price_min")[0].childNodes[0].toxml()
#print "{{{{{{{"+price_min
for i in cNodes[0].getElementsByTagName("item"):
	print i.getElementsByTagName("price_min")[0].childNodes[0].toxml()
	li=list()

	li.extend([i.getElementsByTagName("name")[0].childNodes[0].toxml() , i.getElementsByTagName("url")[0].childNodes[0].toxml()])
	
	price_min = i.getElementsByTagName("price_min")[0].childNodes[0].toxml()
	#price_min = unicodedata.numeric(price_min)
	print type(price_min)
	#print repr(price_min)
	#import pdb; pdb.set_trace()
	price = price_min.replace(',','.')

	price_min = float(price)
	print price_min
	print type(price_min)
	
	#if p_min < i.getElementsByTagName("price_min")[0].childNodes[0].toxml():
	
	
	print i.getElementsByTagName("name")[0].childNodes[0].toxml()
	#print i.getElementsByTagName("price_min")[0].childNodes[0].toxml()
	print i.getElementsByTagName("url")[0].childNodes[0].toxml()
	slownik.update({price_min:li})

	#tablLiczFish3.update({klucz:dodajlist})
#http://api.nokaut.pl/?format=xml&key=a8839b1180ea00fa1cf7c6b74ca01bb5&method=nokaut.product.getByKeyword.sort_direction("prince")&keyword&keyword=canon110d
#http://api.nokaut.pl/?format=xml&key=a8839b1180ea00fa1cf7c6b74ca01bb5&method=nokaut.product.getByKeyword&keyword&keyword=canon110d&&filters[price]


"""
print dom.getElementsByTagName("name")[0].childNodes[0].toxml()
print dom.getElementsByTagName("price_min")[0].childNodes[0].toxml()
print dom.getElementsByTagName("url")[0].childNodes[0].toxml()
"""
print "======================================="




# (IMHO) the simplest approach:
def sortedDictValues1(adict):
    items = adict.items()
    items.sort()
    return [value for key, value in items]

# an alternative implementation, which
# happens to run a bit faster for large
# dictionaries on my machine:
def sortedDictValues2(adict):
    keys = adict.keys()
    keys.sort()
    print [dict[key] for key in keys]
    return [dict[key] for key in keys]

# a further slight speed-up on my box
# is to map a bound-method:
def sortedDictValues3(adict):
    keys = adict.keys()
    keys.sort()
    print keys[0]
    return keys[0]
    #return map(adict.get, keys)


k=sortedDictValues3(slownik)

print k
print "======================================="
for klucz, wartosc in slownik.items():
	if klucz==k:
		print klucz, wartosc[1]
