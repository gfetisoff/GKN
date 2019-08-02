#Fucking hell this is the third time im writing this
import logging
import webapp2
import os
import jinja2
import datetime

from google.appengine.api import users
from google.appengine.ext import ndb

#starts a jinja environment
jinjaEnv = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

#makes a class instance to be used in the ndb datastore database
class uPost(ndb.Model):
    userName = ndb.StringProperty()
    newsName = ndb.StringProperty()
    newsDesc = ndb.StringProperty()
    newsData = ndb.StringProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        #authentication
        current_user = users.get_current_user()
        login_url = users.create_login_url('/')
        logout_url = users.create_logout_url('/')
        #to be used on the main site.
        template_vars={
            #"posts": posts,
            "current_user": current_user,
            "logout_url": logout_url,
            "login_url": login_url,
        }
        #displays the main site...
        template = jinjaEnv.get_template('templates/index.html')
        self.response.write(template.render(template_vars))

class PostHandler(webapp2.RequestHandler):
    def get(self):
        #grabs all users and assigns them as a list.
        posts = uPost.query().fetch()
        #grabs the current user needed for "authentication"
        user = users.get_current_user()
        #pass on the data to write the "posts" page
        data = {
            'posts': posts,
            'user': user,
        }
        template = jinjaEnv.get_template('templates/post.html')
        self.response.write(template.render(data))

class NewPostHandler(webapp2.RequestHandler):
    def get(self):
        #generate the user view to take in user data
        template_vars ={}
        template = jinjaEnv.get_template('templates/new_post.html')
        self.response.write(template.render(template_vars))

    def post(self):
        user=str(users.get_current_user())
        #test cases
        # self.response.headers['Content-type']='text/plain'
        # self.response.write(user)

        title = self.request.get('title')
        caption = self.request.get('caption')
        post_img = self.request.get('post_img_url')
        #builds a uPost type to put into data store.
        build_uPost = uPost(userName = user, newsName=title, newsDesc=caption, newsData=post_img)
        #makes sure the title field is NOT empty
        if title != "":
            #puts into datastore.
            build_uPost.put()
        #redirects to the post page that displays all posts that have been inserted
        self.redirect('/post')

app = webapp2.WSGIApplication([
('/', MainHandler),
('/post', PostHandler),
('/new_post', NewPostHandler),
], debug=True)
