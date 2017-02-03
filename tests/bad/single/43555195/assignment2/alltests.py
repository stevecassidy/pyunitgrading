'''
@author: Steve Cassidy

'''
import unittest
from webtest import TestApp
import bottle

import interface
from database import COMP249Db
import main
import os

class LevelAUnitTests(unittest.TestCase):
    
    
    def setUp(self):
        # open an in-memory database for testing
        self.db = COMP249Db(':memory:')
        self.db.create_tables()
        self.db.sample_data(random=False)


        self.posts = self.db.posts

    def test_post_list(self):
        """Test that post_list returns all posts"""

        # first get all posts
        posts = interface.post_list(self.db)

        self.assertEqual(len(self.posts), len(posts))


    def test_post_list_user(self):
        """Test that post_list works with a usernick argument"""

        # now restrict to one user
        posts = interface.post_list(self.db, usernick='Mandible')
        self.assertEqual(3, len(posts))

        # try a user with no posts
        posts = interface.post_list(self.db, usernick='jb@up.com')
        self.assertEqual(0, len(posts))

        # try a user who doesn't exist
        posts = interface.post_list(self.db, usernick='not@real.com')
        self.assertEqual(0, len(posts))


    def test_post_list_limit(self):
        """Test that post list works with the limit argument"""

        # now look at the limit argument
        posts = interface.post_list(self.db, limit=3)
        self.assertEqual(3, len(posts))

        posts = interface.post_list(self.db, limit=1)
        self.assertEqual(1, len(posts))

        # limit higher than number of posts
        posts = interface.post_list(self.db, limit=100)
        self.assertEqual(10, len(posts))


    def test_post_list_mentions(self):
        """Test getting a list of posts mentioning a user"""

        user1 = 'Contrary'
        user2 = 'Bobalooba'
        user3 = 'Mandible'

        posts = interface.post_list_mentions(self.db, usernick=user1)
        # should include only posts with @Contrary
        self.assertEqual(2, len(posts))
        self.assertListEqual([2, 5], [p[0] for p in posts])



    def test_post_html(self):
        """Test conversion of posts to HTML: tags and &"""

        # plain text doesn't change
        text = "Hello World!"
        self.assertEqual(text, interface.post_to_html(text))

        # quoting HTML
        text = "<p>Hello World</p>"
        html = interface.post_to_html(text)
        self.assertEqual("&lt;p&gt;Hello World&lt;/p&gt;", html)

        # quoting HTML with attributes
        text = "<p class='foo'>Hello World</p>"
        html = interface.post_to_html(text)
        self.assertEqual("&lt;p class='foo'&gt;Hello World&lt;/p&gt;", html)

        # quoting HTML entities
        text = "Fish & Chips"
        html = interface.post_to_html(text)
        self.assertEqual("Fish &amp; Chips", html)

    def test_post_html_links(self):
        """More tests on conversion of posts: links"""
        
        # links
        text = "<p>Hello World http://example.org/ is it</p>"
        html = interface.post_to_html(text)
        self.assertEqual("&lt;p&gt;Hello World <a href='http://example.org/'>http://example.org/</a> is it&lt;/p&gt;", html)

        # links with stuff
        text = "<p>Hello World http://example.org/home_page.html is it</p>"
        html = interface.post_to_html(text)
        self.assertEqual("&lt;p&gt;Hello World <a href='http://example.org/home_page.html'>http://example.org/home_page.html</a> is it&lt;/p&gt;", html)


    def test_post_html_mentions(self):
        """Test conversion of @mentions in posts to HTML"""

        # mentions
        text = "<p>Hello World @Bobolooba</p>"
        html = interface.post_to_html(text)
        self.assertEqual("&lt;p&gt;Hello World <a href='/users/Bobolooba'>@Bobolooba</a>&lt;/p&gt;", html)

        # word internal period is allowed
        text = "<p>Hello World @steve.cassidy</p>"
        html = interface.post_to_html(text)
        self.assertEqual("&lt;p&gt;Hello World <a href='/users/steve.cassidy'>@steve.cassidy</a>&lt;/p&gt;", html)

        # word final period is not part of the name
        text = "Hello World @Cat."
        html = interface.post_to_html(text)
        self.assertEqual("Hello World <a href='/users/Cat'>@Cat</a>.", html)

        # word final period followed by space is not part of the name
        text = "Hello World @Cat. Hi!"
        html = interface.post_to_html(text)
        self.assertEqual("Hello World <a href='/users/Cat'>@Cat</a>. Hi!", html)


class Level2FunctionalTests(unittest.TestCase):

    def setUp(self):
        self.app = TestApp(main.application)
        # init database
        self.db = COMP249Db()
        self.db.create_tables()
        self.db.sample_data(random=False)
        self.users = self.db.users
        self.posts = self.db.posts
        
        bottle.TEMPLATES.clear()
        #print("TEMPLATE_PATH: ", [os.path.realpath(p) for p in bottle.TEMPLATE_PATH])

    def testHomepage(self):
        """As a visitor to the site, when I load the
         home page I see a banner with "Welcome to Psst"."""

        response = self.app.get('/')
        self.assertEqual('200 OK', response.status)
        self.assertIn("Welcome to Psst", response)

    def testHomePageListsPosts(self):
        """As a visitor to the site, when I load the home page I see a list of
        up to 50 posts from all users in order of time, most recent first
        """
        
        result = self.app.get('/')
        # should contain text of all posts, need to look for the words because
        # #tags and @mentions will be encoded
        for post in self.posts:
            for word in post[3]:
                self.assertIn(word, result)

    def testHomePageListsPostsOrder(self):
        """As a visitor to the site, when I load the home page I see a list of
        up to 50 posts from all users in order of time, most recent first
        
        -- check ordering
        """
        
        result = self.app.get('/')
        # check the order of posts, look for the date strings
        # and check that they occur in order
        lastloc = -1
        for post in self.posts:
            loc = result.text.find(post[1])
            self.assertNotEqual(-1, loc, "date string '%s' not found in page" % post[1])
            self.assertGreater(loc, lastloc, "date string '%s' occurs out of order" % post[1])
            lastloc = loc


        # not yet checking the 'up to 50' part

    def testUserPage(self):
        """As a visitor to the site, when I load the page for a user I
        see their name and avatar and a list of their posts in order, newest first
        """

        (passwd, nick, avatar) = self.users[0]

        response = self.app.get('/users/%s' % nick)

        # look for the nick
        self.assertIn(nick, response)
        # look for the avatar in an image tag
        self.assertRegex(response.text, "<img src=['\"]?%s['\"]?" % avatar)

        # should contain all posts for this user, check for the date strings
        # also messages for other users should not be there
        # check that dates are in order
        lastloc = -1
        for id, date, msgnick, message in self.posts:
            if msgnick == nick:
                loc = response.text.find(date)
                self.assertIn(date, response.text)
                self.assertGreater(loc, lastloc, "date string '%s' occurs out of order" % date)
            else:
                self.assertNotIn(date, response.text)

    def testUserMentions(self):
        """As a visitor to the site, when I load the mentions
        page for a user, I see a list of all posts that contain the
        @ character followed by the user name
        """

        # choose user Contrary which has two mentions
        (passwd, nick, avatar) = self.users[2]

        response = self.app.get('/mentions/%s' % nick)

        # should contain all posts for this user, check for the date strings
        # also messages for other users should not be there
        for id, date, msgnick, message in self.posts:
            if '@'+nick in message:
                self.assertIn(date, response.text)
            else:
                self.assertNotIn(date, response.text)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()