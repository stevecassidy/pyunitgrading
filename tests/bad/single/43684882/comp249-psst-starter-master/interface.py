"""
@author: Junaid Ahmad
"""


def post_to_html(content):
    """Convert a post to safe HTML, quote any HTML code, convert
    URLs to live links and spot any @mentions or #tags and turn
    them into links.  Return the HTML string"""
    import re
    text = str(content)
    # replacing characters with entities
    str1 = text.replace('<', '&lt;')
    str2 = str1.replace('>', '&gt;')
    str3 = str2.replace(' & ', ' &amp; ')
    str4 = str3

    mention_re = r'\@[a-z_.A-Z0-9]+' #regex to find mentions in a post
    link_re = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+' #regex to find links in a post

    list = re.findall(mention_re, str3)
    for item in list:
        if item[-1] == '.':
            item = item[:-1]
        String = "<a href='/users/" + str(item[1:]) + "'>" + str(item) + "</a>" #constructing a link to to a user page
        str4 = str3.replace(item, String)

    list2 = re.findall(link_re,str4)
    for item in list2:
        String = "<a href='" + item + "'>" + item + "</a>" #constructing a link to to another webpage
        str4 = str3.replace(item, String)

    return str4

def post_list(db, usernick= None, limit=50):
    """Return a list of posts ordered by date
    db is a database connection (as returned by COMP249Db())
    if usernick is not None, return only posts by this user
    return at most limit posts (default 50)

    Returns a list of tuples (id, timestamp, usernick, avatar,  content)
    """

    cursor = db.cursor()
    if usernick != None:
        sql = """select id, timestamp, posts.usernick, avatar, content from posts,
         users where posts.usernick = users.nick and posts.usernick = ? order by timestamp desc"""
        cursor.execute(sql, (usernick,))
        query = cursor.fetchall()
        length = len(query)
        for item in range(limit,length):
            query.pop()
        return query
    else:
        sql = """select id, timestamp, posts.usernick, avatar, content from posts,
        users where posts.usernick = users.nick order by timestamp desc"""
        cursor.execute(sql)
        query = cursor.fetchall()
        length1 = len(query)
        for item in range(limit,length1):
            query.pop()
        return query

def post_list_mentions(db, usernick, limit=50):
    """Return a list of posts that mention usernick, ordered by date
    db is a database connection (as returned by COMP249Db())
    return at most limit posts (default 50)

    Returns a list of tuples (id, timestamp, usernick, avatar, content)
    """
    list = []
    cursor = db.cursor()
    sql = """select id, timestamp, usernick, avatar, content from posts,
    users where posts.usernick = users.nick order by timestamp desc"""
    cursor.execute(sql)
    query = cursor.fetchall()
    length = len(query)
    for index in range(length):
        if usernick in query[index][4]:
            list.append(query[index])
    return list

def post_add(db, usernick, message):
    """Add a new post to the database.
    The date of the post will be the current time and date.

    Return a the id of the newly created post or None if there was a problem"""


post_to_html("")
