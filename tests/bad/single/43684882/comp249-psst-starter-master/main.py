__author__ = 'Steve Cassidy'

from bottle import Bottle, template, static_file, request, response, HTTPError
import interface
import os
import users
from database import COMP249Db

application = Bottle()

@application.route('/')
def index():

    db = COMP249Db()
    cont = interface.post_list(db,None,50) # grab the posts from the database
    posts = []
    for row in cont:
        li = list(row)  #converting each tuple into a list
        print(li[4])
        li[4] = interface.post_to_html(li[4]) #converting the post message into suitable html
        posts.append(li) #populating a list with data ready to display in the template
        print(li)
    print('posts below')
    print(posts)
    return template(os.path.join('views','general'), title="Welcome to Psst!", content=posts)

@application.route('/users/<user>')
def posts(user):
    db = COMP249Db()
    cont = interface.post_list(db,user,50) # grab the posts from the database for the user specified
    posts = []
    for row in cont:
        li = list(row) #converting each tuple into a list
        print(li[4])
        li[4] = interface.post_to_html(li[4]) #converting the post message into suitable html
        posts.append(li)  #populating a list with data ready to display in the template
        print(li)
    print('posts below')
    print(posts)
    return template(os.path.join('views','general'), title="Welcome to Psst!", content=posts)

@application.route('/mentions/<user>')
def posts(user):
    db = COMP249Db()
    cont = interface.post_list_mentions(db,user,50) # grab the posts from the database which mention the user specified
    posts = []
    for row in cont:
        li = list(row) #converting each tuple into a list
        print(li[4])
        li[4] = interface.post_to_html(li[4]) #converting the post message into suitable html
        posts.append(li) #populating a list with data ready to display in the template
        print(li)
    print('posts below')
    print(posts)
    return template(os.path.join('views','general'), title="Welcome to Psst!", content=posts)


@application.route('/static/<filename:path>')
def static(filename):
    return static_file(filename=filename, root='static')


if __name__ == '__main__':
    application.run(debug=True)