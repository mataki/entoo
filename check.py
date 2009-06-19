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

    send_obj = []
    elem = fromstring(result.content)
    entries = Entry.all()
    for s in elem.findall('.//status'):
      text = s.findtext('./text').encode('utf-8')
      for entry in entries:
        if text.find(entry.target.encode('utf-8')) > -1:
          send_obj.append({'entry':entry, 'tweet':text})

    for s in send_obj:
      mail.send_mail(sender = 'matsumura.aki+entoo@gmail.com',
                     to = s['entry'].email,
                     subject = 'Entoo %s' % s['entry'].target,
                     body = s['tweet'],
                     )

    self.response.out.write(template.render('check.html',{'send_obj':send_obj}))

application = webapp.WSGIApplication([('/check', CheckHandler)],
                                     debug=True)
def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
