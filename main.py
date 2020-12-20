import os

from jobFinder import *



def main():

    job_finder = jobFinder()
    job = job_finder.search_jobs('engineer', 'New York, NY')
    print(job.title)




if __name__ == "__main__":
    main()
