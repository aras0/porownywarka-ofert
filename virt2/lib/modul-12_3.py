# -*- coding: utf-8 -*-

import sys
from xml.dom.minidom import parseString
import urllib , urllib2
#import lxml.etree
import getopt


#def main(argv):
#wywolanie
# python modul-12_2.py canon1100d a8839b1180ea00fa1cf7c6b74ca01bb5

def sortedDictValues3(adict):
    keys = adict.keys()
    keys.sort()
    return keys[0]


def downl(przedmiot, key_number):
	"""Return oferts
	>>>downl(canon1100d, a8839b1180ea00fa1cf7c6b74ca01bb5)
	35.0 http://www.nokaut.pl/ochrona-wyswietlacza-aparatu/oslona-na-wyswietlacz-canon-1100d.html
	"""
	a_url = 'http://api.nokaut.pl/?format=xml&key=' + key_number + '&method=nokaut.product.getByKeyword&keyword='+przedmiot+'&filters[price_min]'





	file = urllib.urlopen(a_url)
	data = file.read()

	file.close()

	dom = parseString(data)
	slownik=dict()
	price_min=float()

	cNodes = dom.childNodes
	price_min = dom.getElementsByTagName("price_min")[0].childNodes[0].toxml()

	for i in cNodes[0].getElementsByTagName("item"):
		li=list()

		li.extend([i.getElementsByTagName("name")[0].childNodes[0].toxml() , i.getElementsByTagName("url")[0].childNodes[0].toxml()])
		
		price_min = i.getElementsByTagName("price_min")[0].childNodes[0].toxml()
		price = price_min.replace(',','.')
		price_min = float(price)
		slownik.update({price_min:li})





	k=sortedDictValues3(slownik)


	for klucz, wartosc in slownik.items():
		if klucz==k:
			print klucz, wartosc[1]



if __name__ == '__main__':
	if len(sys.argv) != 3:
		raise SystemExit, "Wrong number of arguments"
	nazwa = str(sys.argv[1])
	num = str(sys.argv[2])
	print downl(nazwa , num)