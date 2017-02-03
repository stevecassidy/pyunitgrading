"""
@author: Martin Appleton 43555195
"""
import sqlite3
import re
import time
import datetime

def post_to_html(content):
    """Convert a post to safe HTML, quote any HTML code, convert
    URLs to live links and spot any @mentions or #tags and turn
    them into links.  Return the HTML string"""

    html_content = str(content)

    """Simple Char swap for &, < and >"""

    html_content = html_content.replace('&', '&amp;')
    html_content = html_content.replace('<', '&lt;')
    html_content = html_content.replace('>', '&gt;')

    """Link formatting"""

    link_re = r'(http://[\w./#]+)'
    link_match = re.findall(link_re, html_content)

    for match in link_match:
        link_output = "<a href='" + match + "'>" + match + '</a>'
        html_content = re.sub(link_re, link_output, html_content)

    """Mentions"""

    mention_re = r'@[\w.]+'
    mention_match = re.findall(mention_re, html_content)

    for match in mention_match:
        if match.endswith("."):
            mention_output = "<a href='/users/" + match[1:-1] + "'>" + match[:-1] + '</a>.'
        else:
            mention_output = "<a href='/users/" + match[1:] + "'>" + match + '</a>'
        html_content = re.sub(mention_re, mention_output, html_content)

    return html_content

def post_list(db, usernick=None, limit=50):
    """Return a list of posts ordered by date
    db is a database connection (as returned by COMP249Db())
    if usernick is not None, return only posts by this user
    return at most limit posts (default 50)

    Returns a list of tuples (id, timestamp, usernick, avatar,  content)
    """
    cursor = db.cursor()

    if usernick != None:
        sql = """SELECT id, timestamp, usernick, avatar, content
        FROM posts
        JOIN users ON posts.usernick=users.nick
        WHERE usernick=(?)
        ORDER by timestamp DESC
        LIMIT (?);"""
        cursor.execute(sql,(usernick, limit))
    else:
        sql = """SELECT id, timestamp, usernick, avatar, content
        FROM posts
        JOIN users ON posts.usernick=users.nick
        ORDER by timestamp DESC
        LIMIT (?);"""
        cursor.execute(sql, (limit,))

    result = []

    for row in cursor:
        result.append(row)

    return result



def post_list_mentions(db, usernick, limit=50):
    """Return a list of posts that mention usernick, ordered by date
    db is a database connection (as returned by COMP249Db())
    return at most limit posts (default 50)

    Returns a list of tuples (id, timestamp, usernick, avatar,  content)
    """
    cursor = db.cursor()
    search_nick = '%@' + usernick + '%'

    sql = """SELECT id, timestamp, usernick, avatar, content
    FROM posts JOIN users
    ON posts.usernick=users.nick
    WHERE content LIKE (?)
    ORDER BY timestamp
    DESC LIMIT (?);"""
    cursor.execute(sql, (search_nick, limit))

    result = []
    for row in cursor:
        result.append(row)
    return result




def post_add(db, usernick, message):
    """Add a new post to the database.
    The date of the post will be the current time and date.

    Return a the id of the newly created post or None if there was a problem"""

    cursor = db.cursor()

    sql = "SELECT max(id) FROM posts"
    cursor.execute(sql)

    for row in cursor:
        new_id = row[0] + 1

    if len(message) < 150:
        current_time = time.time()
        timestamp = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
        sql = 'INSERT INTO posts (id, timestamp, usernick, content) VALUES (?, ?, ?, ?)'
        cursor.execute(sql, (new_id, timestamp, usernick, message))
        return new_id
    else:
        return None



