import webapp2
import jinja2
import os

from google.appengine.api import urlfetch
import json

from google.appengine.api import users
from google.appengine.ext import ndb

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class CssiUser(ndb.Model):
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)

# class Article(ndb.Model):
#     author =
#     text =


class SecretHandler(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			email_address = user.nickname()
			cssi_user = CssiUser.query().filter(CssiUser.email == email_address).get()
			if cssi_user:

				key_word = "sports"
				news_endpoint = "https://newsapi.org/v2/everything?q=" + key_word + "&from=2019-06-30&sortBy=publishedAt&apiKey=77a427c4c640471ab1430f9de35df425"
				news_response = urlfetch.fetch(news_endpoint).content
				news_as_json = json.loads(news_response)
				first_article = news_as_json["articles"][0]
				first_article_description = first_article["description"]



				self.response.write("Article Description: " + first_article_description)
				return
				self.error(403)
				return

class MainHandler(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
	        # If the user is logged in...
		if user:
			signout_link_html = '<a href="%s">sign out</a>' %(users.create_logout_url('/'))
			email_address = user.nickname()
			cssi_user = CssiUser.query().filter(CssiUser.email == email_address).get()
                        # If the user is registered...
			if cssi_user:
                            # Greet them with their personal information
                             user = users.get_current_user()
                             cssi_user = CssiUser(
                                             first_name=self.request.get('first_name'),
                                             last_name=self.request.get('last_name'),
                                             email=user.nickname())
                             cssi_user.put()
                             signed_in_template = the_jinja_env.get_template('templates/index.html')
                             variable_dict = {
                             "username" : cssi_user.first_name
                             }
                             self.response.write(signed_in_template.render(variable_dict))

			# If the user isn't registered...
			else:
                            # Offer a registration form for a first-time visitor:
		  		self.response.write('''
					Welcome to our site, %s!  Please sign up! <br>
					<form method="post" action="/">
					<input placeholder="First Name"  type="text" name="first_name">
					<input placeholder="Last Name" type="text" name="last_name">
					<input type="submit">
					</form><br> %s <br>
					''' % (email_address, signout_link_html))
		else:
		# If the user isn't logged in...
			login_url = users.create_login_url('/')
			login_html_element = '<a href="%s">Sign in</a>' % login_url
	  # Prompt the user to sign in.
	  		self.response.write('Please log in.<br>' + login_html_element)

	def post(self):
		  # Code to handle a first-time registration from the form:
		user = users.get_current_user()
		cssi_user = CssiUser(
				first_name=self.request.get('first_name'),
				last_name=self.request.get('last_name'),
				email=user.nickname())
		cssi_user.put()
		signed_in_template = the_jinja_env.get_template('templates/index.html')
		variable_dict = {
		"username" : cssi_user.first_name
		}
		self.response.write(signed_in_template.render(variable_dict))

app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/new', SecretHandler),
	], debug=True)
