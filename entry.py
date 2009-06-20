#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import users

class RequestHandlerMetaclass(type):
    def __init__(cls, name, bases, dct):
        super(RequestHandlerMetaclass, cls).__init__(name, bases, dct)
        org_post = getattr(cls, 'post')
        def post(self, *params, **kws):
            verb = self.request.get('_method')
            if verb:
                verb = verb.upper()
                if verb ==  'DELETE':
                    self.delete(*params, **kws)
                elif verb == 'PUT':
                    self.put(*params, **kws)
            else:
                org_post(self, *params, **kws)
        setattr(cls, 'post', post)

class Entry(db.Model):
  target = db.StringProperty()
  created_at = db.DateTimeProperty(auto_now_add=True)
  email = db.StringProperty()
  user = db.UserProperty()

class EntriesHandler(webapp.RequestHandler):
  __metaclass__ = RequestHandlerMetaclass
  def get(self):
    key = self.request.get('key')
    if key:
      entry = Entry.get(key)
      if entry and entry.user == users.get_current_user():
        self.response.out.write(template.render('show.html',{'entry':entry}))
      else:
        self.response.out.write("NOT FOUND")
    else:
      q = Entry.all().filter("user =",users.get_current_user()).order('-created_at')
      entries = q.fetch(20)

      self.response.out.write(template.render('index.html',{'entries':entries, 'logout_url':users.create_logout_url('/')}))

  def post(self):
    key = self.request.get('key')
# change put method
    if key:
      entry = Entry.get(key)
      if entry and entry.user == users.get_current_user():
        entry = Entry.get(key)
        entry.target = self.request.get('target')
        entry.email = self.request.get('email')
        entry.put()

        self.redirect("/entries?key=%s" % key)
      else:
        self.response.out.write("NOT FOUND")
    else:
      entry = Entry()
      entry.user =  users.get_current_user()
      entry.target = self.request.get('target')
      entry.email = self.request.get('email')
      entry.put()

      self.redirect('/entries')

  def delete(self):
    key = self.request.get('key')
    if key:
      entry = Entry.get(key)
      if entry and entry.user == users.get_current_user():
        entry.delete()
        self.redirect('/entries')
      else:
        self.response.out.write("NOT FOUND")
    else:
      self.response.out.write("NOT FOUND")



application = webapp.WSGIApplication([('/entries', EntriesHandler)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
