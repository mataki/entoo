from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class CheckHandler(webapp.RequestHandler):
  def get(self):
    self.response.out.write("CHECK")

application = webapp.WSGIApplication([('/check', CheckHandler)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
