from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from google.appengine.api import urlfetch
from xml.etree.ElementTree import fromstring

from google.appengine.api import mail

class Entry(db.Model):
  target = db.StringProperty()
  created_at = db.DateTimeProperty(auto_now_add=True)
  email = db.StringProperty()
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

    entries = Entry.all()
    bodys = []
    for entry in entries:
      body = ''
      for t in twits:
        if t.find(entry.target.encode('utf-8')) > -1:
          body = body + t + '\n\n'
      if body and 0 < len(body.strip()):
        bodys.append(body)
        mail.send_mail('entoo@mat-aki.net', entry.email, 'Entoo %s' % entry.target, body)

    self.response.out.write(template.render('check.html',{'send_obj':bodys}))

application = webapp.WSGIApplication([('/check', CheckHandler)],
                                     debug=True)
def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
