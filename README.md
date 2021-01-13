Webscraping Indeed.com
===

This project scrapes Indeed.com for job postings and stores them in a postgreSQL database. This project was inspired by [this repo by skylersinclair.](https://github.com/skylersinclair/webscrape) The script accesses Indeed.com using Selenium and hosts the database in Heroku. To start a search, the script types in a city and job title. The city and job title are predetermined and stored in lists. The script types each city and job title pair each time it runs.  The script then iterates through every resulting page and grabs each entry. There are timers that sleep the process after every search to help work around Indeed's measures to prevent webscraping.  

Requirements
---

I used a conda environment when working on this but a python virtualenv will work also. All requirements are in the `requirements.txt` file. You will also need to install Google Chrome and download a corresponding chromedriver. Also, you will need the credentials to your Heroku database.  

Data Collection
---

The `jobFinder.py` file has all the code that scrapes data off of Indeed.com. This file initiates the chrome webdriver in headless mode. The next step is to go to the Indeed homepage and insert the city and job title search query. The `search_jobs()` function does all the scraping from the HTML. All other functions help navigate through result pages or help manipulate data to the desired output format. The end result of this script is a JSON object of the extracted data.

The `main.py` script should be run to initiate webscraping. This file has all the database insertion code and specific search query values.  


For each entry, only the jobID, title, company name, location, salary, date listed, date scraped, company rating, rank, url and description are saved. See the database table schema below.

Database Schema
---
'''
jobid             varchar(20) primary key
title             text
company           text
location          text
salary            varchar(30)
dateListed        varchar(15)
dateScraped       timestampz
companyRating     numeric(3,2)
rank              real
pageNum           real
url               text
description       text
'''

See the `structs.py` file for the associated JobInfo struct.

Resources and helpful Links
---
[skylersinclair's Webscraping Repo](https://github.com/skylersinclair/webscrape)  
[Heroku Postgres Resource](https://devcenter.heroku.com/articles/heroku-postgresql)  
[Selenium Resources](https://selenium-python.readthedocs.io/)  
[Chromedriver Downloads](https://chromedriver.chromium.org/downloads)
