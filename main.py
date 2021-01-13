import os
import json
import time
import psycopg2
from constants import *
from jobFinder import *
from db_queries import *
from cred import * # import database credentials

def main():

    jobs = ['software engineer', 'data scientist', 'data analyst', 'machine learning engineer', 'devops engineer']
    cities = ['New York, NY', 'Chicago, IL', 'Los Angeles, CA']

    print('Getting DB conn...')
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PS)
    cursor = conn.cursor()

    print('Creating table...')
    create_job_table(cursor)
    conn.commit()

    for city in cities:
        for job in jobs:
            print('Currently on ' + str(job) + ' in ' + str(city))
            job_finder = jobFinder()
            results = job_finder.search_jobs(job, city)

            for result in results:
                job_result = json.loads(result)
                try:
                    insert_job(cursor, job_result['job_id'],
                                       job_result['title'],
                                       job_result['company'],
                                       job_result['location'],
                                       job_result['salary'],
                                       job_result['date_listed'],
                                       job_result['date_scraped'],
                                       job_result['company_rating'],
                                       job_result['rank'],
                                       job_result['page_num'],
                                       job_result['url'],
                                       job_result['description'])
                except psycopg2.errors.UniqueViolation:
                    conn.rollback()
                    print('Found duplicate job_id: ', job_result['job_id'])
                    continue

                conn.commit()
                print('\nSearch successful. Sleeping for 30 min.\n')
                time.sleep(WAIT_30_MIN)

    cursor.close()
    print('Done...')

if __name__ == "__main__":
    main()
