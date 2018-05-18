import webapp2

from handlers import MainPage, AdminPage


APPLICATION = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)


ADMIN_APPLICATION = webapp2.WSGIApplication([
    ('/admin/?', AdminPage)
], debug=True)
