#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from mechanize import ParseResponse, urlopen, urljoin

"""
The program should take arguments
1) adres of service, for example: 'http://allegro.pl'
2) keyword, for example : lodĂłwka
Start out by checking to see if the args are there and
set them to their variables
"""
if len(sys.argv) < 3:
    sys.exit("Not enough arguments!")
else:
    uri = sys.argv[1]
    word = sys.argv[2]



def remove_polish(text):
    no_polish_text = text.replace("Ăł","o").replace("Ĺ","l").replace("Ä","a").replace("Ä","e").replace("Ä","c").replace("Ĺ","n").replace("Ĺ","s").replace("Ĺş","z").replace("Ĺź","z")
    no_polish_text = no_polish_text.replace("Ă","O").replace("Ĺ","L").replace("Ä","A").replace("Ä","E").replace("Ä","C").replace("Ĺ","N").replace("Ĺ","S").replace("Ĺš","Z").replace("Ĺť","Z")   
    return no_polish_text

class FormManager:

    def main(self):
        keyword = remove_polish(word)
        openable = 1
        response = urlopen(uri)
        forms = ParseResponse(response, backwards_compat=False)
        if len(forms)==0:
            os.system("python PyCrawler.py"+" baza.db '"+ uri+"' 1 "+ keyword)
            return
        form = forms[0]

        # search for text input in form and put keyword there
        control = form.find_control(type="text")

        control.value = keyword

        # form.click() returns a mechanize.Request object
        # (see HTMLForm.click.__doc__ if you want to use only the forms support, and
        # not the rest of mechanize)
        request2 = form.click()  # mechanize.Request object
        try:
            response2 = urlopen(request2)
        except:
            print "Nie mozna otworzyc formularza"
            openable = 0
            pass

        #get the url of page
        if not openable:
            search_url=uri
        else:
            search_url = response2.geturl()

        #start crawler on it
        os.system("python PyCrawler.py"+" baza.db '"+ search_url+"' 1 "+ keyword)

FormManager().main()
