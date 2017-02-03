"""
@author:
"""


def post_to_html(content):

    """Convert a post to safe HTML, quote any HTML code, convert
    URLs to live links and spot any @mentions or #tags and turn
    them into links.  Return the HTML string"""

    content = content.replace("&", "&amp;")
    content = content.replace("<", "&lt;")
    content = content.replace(">", "&gt;")



    #return '<a class="comurl" href="' + url + '" target="_blank" rel="nofollow">' + text + '<img class="imglink" src="/images/linkout.png"></a>'

    import re

    r = re.compile(r"(http://[^ ]+)")
    return r.sub(r'<a href="\1">\1</a>', content)

    #nearly there replace ' with " and done.

    #content = content.replace("http://", "<a href='http://")

    return content


def post_list(db, usernick=None, limit=50):


    """Return a list of posts ordered by date
    db is a database connection (as returned by COMP249Db())
    if usernick is not None, return only posts by this user
    return at most limit posts (default 50)

    Returns a list of tuples (id, timestamp, usernick, avatar,  content)
    """


def post_list_mentions(db, usernick, limit=50):
    """Return a list of posts that mention usernick, ordered by date
    db is a database connection (as returned by COMP249Db())
    return at most limit posts (default 50)

    Returns a list of tuples (id, timestamp, usernick, avatar,  content)
    """




def post_add(db, usernick, message):
    """Add a new post to the database.
    The date of the post will be the current time and date.

    Return a the id of the newly created post or None if there was a problem"""


