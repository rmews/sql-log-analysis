# PostgreSQL Log Analysis
This project uses Python and PostgreSQL to query a database and display useful data to the user.

The database has three tables:
1. **Articles** table - includes information on the articles being submitted
2. **Authors** table - includes information on the authors
3. **Log** table - includes server request information

The problems the specific queries in this repo set to solve are:
1. What are the three most popular articles of all time
2. What are the most popular article authors of all time
3. What days did more than 1% of requests lead to errors

## Installation and Setup:
1. Install [Python 2.7](https://www.python.org/downloads/), [Vagrant](https://www.vagrantup.com) and [Virtual Box](https://www.virtualbox.org/wiki/Downloads)
2. Clone this repo
4. Start the virtual machine. From terminal, run command `vagrant up` within the repo directory. This will cause Vagrant to download the Linux operating system and install it.
5. Log in the virtual machine. From terminal, run command `vagrant ssh` within the repo directory.
6. Setup the database. First unzip newsdata.zip within repo. Then from terminal, run command `psql -d news -f newsdata.sql;` within the repo directory.
7. Access the database. From terminal, run command `psql -d news` within the repo directory.
8. Create SQL views. Run the following SQL statements to setup views that are used by this repo:

```
CREATE OR REPLACE VIEW article_views AS
SELECT title, count(*) AS views
FROM articles, log
WHERE log.path LIKE concat('%',articles.slug)
GROUP BY articles.title
ORDER BY views desc;
```

```
CREATE OR REPLACE VIEW author_articles AS
SELECT authors.name, articles.title
FROM articles, authors
WHERE articles.author = authors.id;
```

```
CREATE OR REPLACE VIEW total_requests AS
SELECT to_char(time, 'Month DD, YYYY') AS date, count(*) AS total
FROM log
GROUP BY date
ORDER BY date ASC;
````

```
CREATE OR REPLACE VIEW error_requests AS
SELECT to_char(time, 'Month DD, YYYY') AS date, status, count(*) AS errors
FROM log
WHERE status != '200 OK'
GROUP BY date, status
ORDER BY date ASC;
```

```
CREATE OR REPLACE VIEW daily_error_rate AS
SELECT error_requests.date, ROUND(((error_requests.errors * 100)/total_requests.total::NUMERIC),2) AS error_value
FROM error_requests, total_requests
WHERE error_requests.date = total_requests.date
ORDER BY date ASC;
```

9. Run the Application. From terminal, run `python log_analysis.py` within the repro directory. Open up [localhost](http://localhost:8000) in your browser.
