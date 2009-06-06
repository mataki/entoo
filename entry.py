#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import users

class Entry(db.Model):
  target = db.StringProperty()
  created_at = db.DateTimeProperty(auto_now_add=True)
  email = db.StringProperty()
  user = db.UserProperty()

class EntriesHandler(webapp.RequestHandler):
  def get(self):
    key = self.request.get('key')
    if key:
      entry = Entry.get(key)
      self.response.out.write(template.render('show.html',{'entry':entry}))
    else:
      entries = Entry.all()
      self.response.out.write(template.render('index.html',{'entries':entries}))

  def post(self):
    key = self.request.get('key')
    if key:
      entry = Entry.get(key)
      entry.target = self.request.get('target')
      entry.email = self.request.get('email')
      entry.put()

      self.redirect("/entries?key=%s" % key)
    else:
      entry = Entry()
      entry.user =  users.get_current_user()
      entry.target = self.request.get('target')
      entry.email = self.request.get('email')
      entry.put()

      self.redirect('/entries')

application = webapp.WSGIApplication([('/entries', EntriesHandler)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
