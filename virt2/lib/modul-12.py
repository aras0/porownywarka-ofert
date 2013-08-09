# -*- coding: utf-8 -*-
from xml.dom import minidom
import urllib.request
import sys
from xml.dom.minidom import parseString
import urllib

#wywolanie
# python modul-12_2.py canon250d a8839b1180ea00fa1cf7c6b74ca01bb5


#zapytanie do Api 
#http://api.nokaut.pl/?format=FORMAT&key=KLUCZ_API&method=METODA&PARAMETR1=WARTOSC&PARAMETR2=WARTOSC

method_download = nokaut.product.getByKeyword
przedmiot = "canon250d"
key_number = "a8839b1180ea00fa1cf7c6b74ca01bb5"
#nokaut.Product - produkty, a nokaut.Price - ceny
#http://api.nokaut.pl/?format=xml&key=KLUCZ_API&method=metoda&keyword=przedmiot

#http://api.nokaut.pl/?format=xml&key=KLUCZ_API&method=metoda&keyword=canon250d
#http://api.nokaut.pl/?format=rest&key=102c0d165e3d544d52f9ce66c2a430a9&method=nokaut.product.getByKeyword&keyword=canon450d
#http://api.nokaut.pl/?format=xml&key=a8839b1180ea00fa1cf7c6b74ca01bb5&method=nokaut.product.getByKeyword&keyword&keyword=canon1000
#xmlTag = dom.getElementsByTagName('tagName')[0].toxml()
#xmlTag = dom.getElementsByTagName('name')[0].toxml()
#xmlData=xmlTag.replace('<name>','').replace('</name>','')
a_url = 'http://api.nokaut.pl/?format=xml&key=' + key_number + '&method=nokaut.product.getByKeyword&keyword='+przedmiot

file = urllib.urlopen(a_url)
data = file.read()

file.close()

dom = parseString(data)

#def download_nokaut():

#a_url = 'http://api.nokaut.pl/?format=xml&key=' + key_number + '&method=nokaut.product.getByKeyword&keyword='+przedmiot

for i in file:
	xmlTag = dom.getElementsByTagName('name')[i].toxml()

xmlTag = dom.getElementsByTagName('name')[0].toxml()
xmlData=xmlTag.replace('<name>','').replace('</name>','')


#for i in cNodes[0].getElementsByTagName("items"):

cNodes = dom.childNodes

for i in cNodes[0].getElementsByTagName("item"):
	print i.getElementsByTagName("imie")[0].childNodes[0].toxml()

