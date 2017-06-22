#!/usr/bin/env python3

from flask import Flask, request, redirect, url_for
from logsdb import get_top_articles, get_top_authors, get_error_log

app = Flask(__name__)

# HTML template for the log analysis page
HTML_WRAP = '''
<!DOCTYPE html>
<html>
    <head>
        <title>Log Analysis</title>
    </head>
    <body>
        <h1>Log Analysis</h1>
        <!-- post content will go here -->
        <h3>Top 3 Articles</h3>
        %s
        <h3>Top 3 Authors</h3>
        %s
        <h3>Day(s) With More Than 1&#37; Error</h3>
        %s
    </body>
</html>
'''

# HTML for top 3 articles/authors
TOP_POSTS = '''
    <div>%s -- %s views</div>
'''

ERROR_POSTS = '''
    <div>%s -- %s&#37; errors</div>
'''


@app.route('/', methods=['GET'])
def main():
    """Main page"""
    top_articles = "".join(TOP_POSTS % (name, count)
                           for name, count in get_top_articles())
    top_authors = "".join(TOP_POSTS % (name, count)
                          for name, count in get_top_authors())
    errors = "".join(ERROR_POSTS % (date, count)
                     for date, count in get_error_log())
    html = HTML_WRAP % (top_articles, top_authors, errors)
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
