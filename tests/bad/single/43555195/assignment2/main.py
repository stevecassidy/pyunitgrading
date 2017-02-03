__author__ = 'Steve Cassidy'

from bottle import Bottle, template, static_file, request, response, HTTPError
import interface
import users
from database import COMP249Db

db = COMP249Db()
application = Bottle(catchall=False)

@application.route('/')
def index():

    posts = interface.post_list(db)
    return template('general', title="Welcome to Psst", posts=posts)

@application.route('/users/<usernick>')
def user_page(usernick):
    """generate the users posts"""
    user_posts = interface.post_list(db, usernick)
    return template('general', title=usernick + "'s Posts", posts=user_posts)

@application.route('/mentions/<usernick>')
def mentions_page(usernick):
    """generate the users posts"""
    mentions_posts = interface.post_list_mentions(db, usernick)
    return template('general', title="Posts mentioning " + usernick, posts=mentions_posts)

@application.route('/static/<filename:path>')
def static(filename):

    return static_file(filename=filename, root='static')




if __name__ == '__main__':
    application.run(debug=True)