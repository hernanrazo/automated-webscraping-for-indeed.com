import psycopg2
from psycopg2 import sql


def create_job_table(cursor):
    cursor.execute('CREATE TABLE IF NOT EXISTS jobs(jobID varchar(20) PRIMARY KEY, title text, company text, location text, salary varchar(30), dateListed varchar(15), dateScraped timestamptz, companyRating numeric(3,2), rank real, pageNum real, url text, description text)')


def insert_job(cursor, job_id, title, company, location, salary, date_listed, date_scraped, company_rating, rank, page_num, url, description):
    cursor.execute('INSERT INTO jobs(jobID, title, company, location, salary, dateListed, dateScraped, companyRating, rank, pageNum, url, description) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (job_id, title, company, location, salary, date_listed, date_scraped,  company_rating, rank, page_num, url, description))


def drop_jobs_table(cursor):
    cursor.execute('DROP TABLE IF EXISTS jobs')
