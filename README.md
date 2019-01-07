# Udacity Full Stack Nanodegree Project: Logs Analysis

## Description:
This project is supposed to mimic an internal reporting tool for a newspaper website that can be used to generate various types of metrics for the content of the newspaper website.
The database called **news** contains the following tables:

**1. Authors:**

*Columns:* name, bio, id


**2. Articles:**

*Columns:* author, title, slug, lead, body, time, id



**3. Log:**

*Columns:* path, ip, method, status, time, id


**Questions to be answered:**

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

The code is written in **Python 3** and connects to a **PostgreSQL** database via the adapter **psycopg2**.
The code was run on a **Linux** platform virtually using **vagrant**.

**Steps to run:**

Setup the environment and load the database. Then login to the vm, navigate to the vagrant directory and run the code via :
```
$ python3 Logs_analysis.py
```

Sample output file:

logs_analysis_output.txt
