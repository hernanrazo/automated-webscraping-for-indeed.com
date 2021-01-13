import os
import json
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

from constants import *
from structs import JobInfo
'''
Main code to scrape data off of indeed.com. Data is retreived 'as is' and 
will need to be cleaned later if user plans to do data analysis or something
useful with the resulting data.
'''

class jobFinder:

    # init the chrome webdriver in headless mode
    def __init__(self):

        options = Options()
        options.headless = True
        options.add_argument('--window-size=1920,1200')

        self.driver = webdriver.Chrome(options=options, executable_path=os.path.abspath('chromedriver'))
        self.current_url = None


    # function that helps with getting the job description
    def get_description(self, url):
        try:
            self.driver.get(url)
            description = self.driver.find_element_by_id('jobDescriptionText')
            page_soup = BeautifulSoup(description.get_attribute('innerHTML'), features='html.parser')
        except NoSuchElementException:
            return 'None'

        return page_soup.get_text("\t", strip=True).lower()


    # boolean that rectifies if there is another
    # page in the search results
    def next_page_exists(self):
        self.driver.implicitly_wait(WAIT_5_SEC)
        self.driver.get(self.current_url)
        self.driver.implicitly_wait(WAIT_5_SEC)

        num_pages = self.driver.find_elements_by_xpath("//*[@aria-label='Next']")

        if len(num_pages) == 0:
            return False
        else:
            return True


    #change the current url to the next page in the search
    def get_next_page(self):

        next_page_button = self.driver.find_element_by_xpath("//*[@aria-label='Next']")
        self.driver.execute_script("arguments[0].click();", next_page_button)

        self.driver.implicitly_wait(WAIT_5_SEC)
        self.current_url = self.driver.current_url

    # search and collect job listings
    def search_jobs(self, job, location):

        # go to indeed.com home page (duhh)
        self.driver.get('https://www.indeed.com/')
        self.driver.implicitly_wait(30)

        # type in given job
        job_search_text_box = self.driver.find_element_by_id('text-input-what')
        job_search_text_box.clear()
        job_search_text_box.send_keys(job)

        # type in given location
        location_search_text_box = self.driver.find_element_by_id('text-input-where')
        location_search_text_box.clear()
        for i in range(1):
            location_search_text_box.send_keys(Keys.BACK_SPACE * 30)

        location_search_text_box.send_keys(location)

        # click the Find Jobs button
        find_jobs_button = self.driver.find_element_by_xpath('//button[text()="Find jobs"]')
        find_jobs_button.click()
        self.driver.implicitly_wait(WAIT_5_SEC)


        # get the first page's url right after the search loads results
        self.current_url = self.driver.current_url


        # start collecting attributes of job results
        page_num = 1
        rank = 1
        job_list = []

        while 1==1: # infinite loop ensures every single result is scraped
        #while page_num <=1:
            print('Current page: ', page_num)

            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            for job in soup.find_all('div', class_='jobsearch-SerpJobCard unifiedRow row result clickcard'):

                # get job ID assigned by indeed
                job_id = job.attrs['data-jk']

                # get title
                title = job.find('a', class_='jobtitle turnstileLink')['title']

                # get company name
                try:
                    company = job.find('span', class_='company').text.strip()
                except AttributeError:
                    company = 'None'

                # get location
                location = job.find('div', class_="recJobLoc")['data-rc-loc']

                # get salary
                try:
                    salary = job.find('span', attrs={'class':'salaryText'}).string.strip()
                except AttributeError:
                    salary = 'None'

                # get date listed
                date_listed = job.find('span', attrs={'class':'date'}).text.strip()

                # get company review rating
                try:
                    company_rating = float(job.find('span', attrs={'class':'ratingsContent'}).text.strip().replace(',', '.'))
                except AttributeError:
                    company_rating = 0.00

                # get indeed url
                url = 'http://indeed.com' + job.find('a', class_="jobtitle turnstileLink")['href']

                # get description
                description = self.get_description(url)

                job_info = json.dumps({'job_id' : job_id,
                                       'title' : title,
                                       'company' : company,
                                       'location' : location,
                                       'salary' : salary,
                                       'date_listed' : date_listed,
                                       'date_scraped' : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                       'company_rating' : company_rating,
                                       'rank' : rank,
                                       'page_num' : page_num,
                                       'url' : url,
                                       'description' : description})
                job_list += [job_info]
                rank +=1
            if self.next_page_exists():
                self.get_next_page()
                page_num +=1
            else:
                break
        return job_list
        self.driver.close()
