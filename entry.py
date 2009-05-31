#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

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
    entry = Entry()
    entry.user =  users.get_current_user()
    entry.target = self.request.get('target')
    entry.email = self.request.get('email')
    entry.put()

    self.redirect('/entries')

  def put(self):
    key = self.request.get('key')
    if key:
      self.redirect("/entries?key=%s" % key)
    else:
      self.response.out.write("BUT REQUEST")

application = webapp.WSGIApplication([('/entries', EntriesHandler)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
