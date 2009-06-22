from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class InfoHandler(webapp.RequestHandler):
  def get(self):
    self.response.out.write(template.render('info.html', {}))

class AboutHandler(webapp.RequestHandler):
  def get(self):
    self.response.out.write(template.render('about.html', {}))

application = webapp.WSGIApplication([('/', InfoHandler),
                                      ('/about', AboutHandler)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
