import webapp2
import cgi
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import db

import webapp2_extras.auth
import models
import modul_13_1 as allegro
import modul_12_3 as nokaut
import creatUser
import ast
import urllib
from datetime import date
import json

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


JINJA_ENVIRONMENT = jinja2.Environment(\
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),\
    extensions=['jinja2.ext.autoescape'])
    #loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates')))


class Render(webapp2.RequestHandler):
    def __init__(self, *args, **kwargs):
        webapp2.RequestHandler.__init__(self, *args, **kwargs)
    def render_template(self, template_file, template_values = None):
        template = JINJA_ENVIRONMENT.get_template(template_file)
        self.response.write(template.render(template_values))


MAIN_PAGE_FOOTER_TEMPLATE = """\
 <head>
     <script src="/script/jquery-1.10.2.min.js"></script>

    <script src="/script/angular/angular.js"></script>
    <script src="/script/angular/angular-resource.js"></script>
    <script src="/script/script.js"></script>
    <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
</head>
<body>


         <p name="user">User: %s</p>
      <a href="%s">%s</a>

    <form action="/results" method="get">
      <div><input type="text" id="content" name="content" rows="3" cols="60"></div>
      <div><input type="submit" name="search" value="Search" onclick="sprawdz(form)"></div>
      


    </form>

    <input type="button" id="getitButton" value="get it" />
    <div id="result">

    </div>

    <script type="text/javascript" >
    function sprawdz(form){
    if(form.content.value.length!=0){
        query = document.getElementById('content').value;
        string = query.replace(/\s+|\s+$/g, '');
        $("#content").val(string);
        }
    }
    </script>
  </body>
</html>
"""

class ResultsUserPage(Render):
    def post(self):
        first_name = self.request.get("first_name")
        last_name = self.request.get("last_name")
        nick = self.request.get("nick")
        email = self.request.get("email")
        password = self.request.get("password")
        typ = self.request.get("typ")
        SearchUser(first_name, last_name, nick, email, password, typ)

        template_values = {
        'first_name': first_name,
        'last_name': last_name,
        'nick': nick,
        'email': email,
        'password': password,
        'typ': typ,
        }
        self.render_template('index_results.html', template_values = template_values)


class Object(db.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    author = db.StringProperty()
    content = db.StringProperty(multiline=True)
    dates = db.DateProperty(auto_now_add=True)


def Login(self, user):

    if user:
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'

    else:
        url = users.create_login_url(self.request.uri)
        url_linktext = 'Login'
    #self.response.write(MAIN_PAGE_FOOTER_TEMPLATE %(user,url, url_linktext))
    return url, url_linktext

class MainPage(Render):
    def get(self):


        user = users.get_current_user()
        #greetings_query =db.filter(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        #greetings = greetings_query.fetch(10)

        url, url_linktext = Login(self, user)

        self.response.write(MAIN_PAGE_FOOTER_TEMPLATE %(user,url, url_linktext))









class ResultsPage(Render):
    def get(self):

        g = Object()
        zmienna = self.request.get('content')
        user = users.get_current_user()
        #greeting = Object(author = user.nickname())
        #user.author = users.get_current_user()



        url, url_linktext = Login(self, user)
        #uzykownik = users.User(federated_identity = user.federated_identity())
        #if user:
            #Object.author = users.get_current_user()
        
        #self.response.write(cgi.escape(self.request.get('content')))






        allegro1 = allegro.loadAlegro(zmienna)
        allegro2 = str(allegro1)
        allegro3 = [item.encode('ascii') for item in ast.literal_eval(allegro2)]
        
        #self.response.write(allegro3)
        nok = nokaut.downlNokaut(self.request.get('content'), 'a8839b1180ea00fa1cf7c6b74ca01bb5')

        cenaAll = allegro3[0]
        linkAll = allegro3[1]
        imgAll = allegro3[2]


        cenaNok = nok[0]
        Nok = nok[1]
        linkNok = Nok[0]
        imgNok = Nok[1]


        cenaAll = float(cenaAll)
        cenaNok = float(cenaNok)

        if cenaAll < cenaNok:
            cenaMin = cenaAll
            linkMin = linkAll
        else:
            cenaMin = cenaNok
            linkMin = linkNok




        if user:
            aut = user.nickname()
            self.response.write('<b> user: %s </b>' % aut)
            g.author = aut
            g.content = zmienna
            g.put()
            q = Object.all()
            


            wynik = q.filter('author =', aut).order('-dates' )

            limitData = date.today()

            limitData2 = date(limitData.year, limitData.month, limitData.day-1)
            wynik.filter('dates >', limitData2)
            results = wynik.fetch(5)
            for user in results:
                user.dates
                self.response.write('<blockquote>%s time: %s</blockquote>' % (user.content, user.dates) )
                self.response.write('<a href ="%s"> allegro </a>' % linkAll)
                self.response.write('<a href ="%s"> nokaut </a>' % linkNok)
            d=dict()
            n=0
            q2 = Object.all()
            

        #     pr = q2.order('content' )
        #     produkty = q2.order('content' ).count()

        #     for p in pr:
        #         n=1
        #         print p.content
        #         d.update({p.content: n})
        #         print p.content
        #         for key in d:
        #             print "--" + p.content 
        #             print key
        #             if p.content == key:
        #                 n=d[key]+1
        #                 print "dodaj"
        #                 d.update({p.content: n})
        #         for k in d:
        #             print k, d[k]
        #                 #print d
        #                 #print p.content
        # db.delete(db.Query())


        # if self.request.get('fmt') =='json':
        #     response={'Price':54,'Cost':'99'}
        #     self.response.out.headers['Content-Type'] ='text/json'
        #     #self.response.out.write(json.dumps(['Price',{'Cost':'99'}]))
        #     self.response.out.write(json.dumps(response))
        #     return

        template_values = {
            'zmienna':zmienna,
            'allegro3': allegro3,
            'imgAll': imgAll,
            'linkAll': linkAll,
            'cenaAll':cenaAll,
            'imgNok': imgNok,
            'linkNok': linkNok,
            'cenaNok':cenaNok,
            'cenaMin': cenaMin,
            'linkMin': linkMin,
            'url': url,
            'url_linktext': url_linktext,
            #'produkty': produkty,
        }

        self.render_template('index_results.html', template_values = template_values)



class MyHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                        (user.nickname(), users.create_logout_url('/')))
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url('/'))

        self.response.out.write('<html><body>%s</body></html>' % greeting)



application = webapp2.WSGIApplication([
    ('/results', ResultsPage),
    ('/search/', MainPage),
    ('/results_user', ResultsUserPage),
    ('/', MyHandler),
], debug=True)