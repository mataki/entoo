from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from google.appengine.api import urlfetch
from xml.etree.ElementTree import fromstring

from google.appengine.api import mail

from datetime import datetime, timedelta

class Entry(db.Model):
  target = db.StringProperty()
  created_at = db.DateTimeProperty(auto_now_add=True)
  email = db.StringProperty()
  target_time = db.StringProperty()
  user = db.UserProperty()

class CheckHandler(webapp.RequestHandler):

  def get(self):
    url = "http://twitter.com/statuses/user_timeline/train_kanto.xml"
    result = urlfetch.fetch(url, '', urlfetch.GET)

    elem = fromstring(result.content)

    twits = []
    for s in elem.findall('.//status'):
      text = s.findtext('./text').encode('utf-8')
      twits.append(text)

    timestr = (datetime.utcnow() + timedelta(hours=9)).strftime('%H:%M')

    entries = Entry.all().filter('target_time =', timestr)

    bodys = []
    for entry in entries:
      body = ''
      for t in twits:
        if t.find(entry.target.encode('utf-8')) > -1:
          body = body + t + '\n\n'
      if body and 0 < len(body.strip()):
        bodys.append(body)
        mail.send_mail(sender = 'entoo@mat-aki.net',
                       to =  entry.email,
                       subject = 'Entoo %s' % entry.target,
                       bcc = 'matsumura.aki+entoo@gmail.com',
                       body = body)

    self.response.out.write(template.render('check.html',{'entries':entries,'twits':twits,'bodys':bodys,'nowtime':timestr}))

application = webapp.WSGIApplication([('/check', CheckHandler)],
                                     debug=True)
def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
