# Code for the Udacity Full Stack Web Developer Project : Logs Analysis
# Author: Tebby Thomas
import sys
#sys.path.append('/usr/local/lib/python2.7/dist-packages/')
import psycopg2

# Our database is named news
DBNAME = "news"

# Storing the required SQL statemtns in strings

# Variables related to Query 1: What are the most popular three articles of all time?

view_query_1 = """CREATE OR REPLACE VIEW popular_article_view AS
SELECT title, author, COUNT(*) AS views FROM articles, log
WHERE log.path LIKE CONCAT('%',articles.slug)
GROUP BY title, author ORDER BY views DESC;"""

sql_query_1 = "SELECT title, views FROM popular_article_view LIMIT 3;"

# Variables related to Query 2: Who are the most popular article authors of all time?

sql_query_2 = """SELECT name, SUM(views) AS views FROM authors, popular_article_view
WHERE popular_article_view.author = authors.id
GROUP BY name ORDER BY views DESC;"""

# Variables related to Query 2: On which days did more than 1% of requests lead to errors?

view_query_3a = """CREATE OR REPLACE VIEW log_fail_status_count_view AS
SELECT time::date as date, count(*) as total_fail FROM log
WHERE status NOT LIKE '%200 OK%' GROUP BY time::date;"""

view_query_3b = """CREATE OR REPLACE VIEW log_status_count_view AS
SELECT time::date as date, count(*) as total FROM log
GROUP BY time::date;"""

sql_query_3 = """SELECT log_status_count_view.date, ROUND((total_fail * 100.0 / total),2) AS error_percent
FROM log_fail_status_count_view, log_status_count_view
WHERE log_fail_status_count_view.date = log_status_count_view.date AND
(total_fail * 100.0 / total) > 1.0;"""

# Results are stored as dictionary variables
query_1 = dict()
query_1['title'] = "\n1. The three most popular articles of all time are:\n"

query_2 = dict()
query_2['title'] = "\n2. The most popular article authors of all time are:\n"

query_3 = dict()
query_3['title'] = "\n3. The Days on which more than 1% of requests lead to errors are:\n"


def execute_sql_stmt(sql_stmt):
    # All sql statements are executed here
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(sql_stmt)
    try:
        result = c.fetchall()
        db.close()
    except psycopg2.ProgrammingError:
        #Exception is raised in case of view creation statements in this code
        db.close()
        return
    return result

def print_output(op, percent):
    # Printing the title of the result
    print (op['title'])
    if percent == "false":
        for result in op['result']:
            print (str(result[0]) + ' -- ' + str(result[1]) + ' views')
    elif percent == "true":
        for result in op['result']:
            print (str(result[0]) + ' -- ' + str(result[1]) + '%'+' errors')


if __name__ == "__main__":
    execute_sql_stmt(view_query_1)
    query_1['result'] = execute_sql_stmt(sql_query_1)
    print_output(query_1, "false")
    query_2['result'] = execute_sql_stmt(sql_query_2)
    print_output(query_2, "false")
    execute_sql_stmt(view_query_3a)
    execute_sql_stmt(view_query_3b)
    query_3['result'] = execute_sql_stmt(sql_query_3)
    print_output(query_3, "true")
