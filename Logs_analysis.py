#!/usr/bin/env python3

# Code for the Udacity Full Stack Web Developer Project : Logs Analysis
# Author: Tebby Thomas
import sys
import psycopg2

# The database is named news
DBNAME = "news"

# Storing the required SQL statemtns in strings

# Variables related to Query 1: What are the most popular three articles of all
# time?

view_query_1 = """CREATE OR REPLACE VIEW popular_article_view AS
SELECT title, author, COUNT(*) AS views FROM articles, log
WHERE log.path = concat('/article/%', articles.slug)
GROUP BY title, author ORDER BY views DESC;"""

sql_query_1 = "SELECT title, views FROM popular_article_view LIMIT 3;"

# Variables related to Query 2: Who are the most popular article authors of all
# time?

sql_query_2 = """SELECT name, SUM(views) AS views
FROM authors, popular_article_view
WHERE popular_article_view.author = authors.id
GROUP BY name ORDER BY views DESC;"""

# Variables related to Query 2: On which days did more than 1% of requests lead
# to errors?

view_query_3a = """CREATE OR REPLACE VIEW log_fail_status_count_view AS
SELECT time::date as date, count(*) as total_fail FROM log
WHERE status NOT LIKE '%200 OK%' GROUP BY time::date;"""

view_query_3b = """CREATE OR REPLACE VIEW log_status_count_view AS
SELECT time::date as date, count(*) as total FROM log
GROUP BY time::date;"""

sql_query_3 = """select to_char(date, 'FMMonth FMDD, YYYY'), err/total as ratio
       from (select time::date as date,
                    count(*) as total,
                    sum((status != '200 OK')::int)::float as err
                    from log
                    group by date) as errors
       where err/total > 0.01;"""

# Results are stored as dictionary variables
query_1 = dict()
query_1['title'] = "\n1. The three most popular articles of all time are:\n"

query_2 = dict()
query_2['title'] = "\n2. The most popular article authors of all time are:\n"

query_3 = dict()
query_3['title'] = """\n3. The Days on which more than 1% of requests lead to
errors are:\n"""


# Helper DB views are created in this method
def execute_view_creation(sql_stmt):
    db = psycopg2.connect(database=DBNAME)
    try:
        c = db.cursor()
        c.execute(sql_stmt)
        db.close()
    except psycopg2.ProgrammingError:
        print("Database related error: psycopg2 programming error occurred")
    return


# Function to query the most popular authors
def top_authors(sql_stmt):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(sql_stmt)
    try:
        result = c.fetchall()
        db.close()
    except psycopg2.ProgrammingError:
        print("Database related error: psycopg2 programming error occurred")
        return
    return result


# Function to query the most popular articles
def top_articles(sql_stmt):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(sql_stmt)
    try:
        result = c.fetchall()
        db.close()
    except psycopg2.ProgrammingError:
        print("Database related error: psycopg2 programming error occurred")
        return
    return result


# Function to query the days with too many errors
def days_with_many_errors(sql_stmt):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(sql_stmt)
    try:
        result = c.fetchall()
        db.close()
    except psycopg2.ProgrammingError:
        print("Database related error: psycopg2 programming error occurred")
        return
    return result


# Printing the title of the result
def print_output(op, percent):
    print(op['title'])
    if percent == "false":
        for result in op['result']:
            print(str(result[0]) + ' -- ' + str(result[1]) + ' views')
    elif percent == "true":
        for result in op['result']:
            print(str(result[0]) + ' -- ' + str(round(result[1]*100, 2)) +
                  '%' + ' errors')


execute_view_creation(view_query_1)
query_1['result'] = top_articles(sql_query_1)
print_output(query_1, "false")
query_2['result'] = top_authors(sql_query_2)
print_output(query_2, "false")
execute_view_creation(view_query_3a)
execute_view_creation(view_query_3b)
query_3['result'] = days_with_many_errors(sql_query_3)
print_output(query_3, "true")
