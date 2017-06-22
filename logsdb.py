# Database code for the Logs Analysis

import psycopg2

DBNAME = "news"


def db_connect():
    """Connect to the database"""
    try:
        db = psycopg2.connect(database=DBNAME)
        c = db.cursor()
        return db, c
    except:
        print("There was an error connecting to the database")


def get_top_articles():
    """Return three most popular articles sorted with most popular first"""
    db, c = db_connect()
    c.execute("""
            SELECT * FROM article_views LIMIT 3
            """)
    articles = c.fetchall()
    db.close()
    return articles


def get_top_authors():
    """Return most popular article authors sorted with most popular first"""
    db, c = db_connect()
    c.execute("""
            SELECT author_articles.name, SUM(article_views.views) AS views
            FROM author_articles, article_views
            WHERE article_views.title = author_articles.title
            GROUP BY author_articles.name
            ORDER BY views DESC
            """)
    authors = c.fetchall()
    db.close()
    return authors


def get_error_log():
    """Return the days with more than 1% of requests lead to errors"""
    db, c = db_connect()
    c.execute("""
            SELECT date, error_value
            FROM daily_error_rate
            WHERE error_value >= 1
            """)
    errors = c.fetchall()
    db.close()
    return errors
