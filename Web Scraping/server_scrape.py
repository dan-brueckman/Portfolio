

import datetime
import locale
from bs4 import BeautifulSoup as bs
import smtplib
import requests as req
import string
from apscheduler.schedulers.blocking import BlockingScheduler

open_url = 'https://www.opentable.com/true-food-kitchen-austin?page=1'
yelp_url = 'https://www.yelp.com/biz/true-food-kitchen-austin-2?sort_by=date_desc'
from_address = 'dan.brueckman@gmail.com'
to_address = 'dan.brueckman@gmail.com'
sched = BlockingScheduler()


def open_table_scrape():
    response = req.get(open_url)
    soup = bs(response.text, 'html.parser')
    results = soup.find_all('div', class_="reviewBodyContainer _73484bf6")
    counter = 0
    for result in results:
        if counter < 10:
            review = result.find('p').text
            for c in string.punctuation:
                reviews = review.replace(c," ")
            if (" Dan" in reviews) or (" dan" in reviews):
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login("dan.brueckman@gmail.com", "")
                server.sendmail(from_address, to_address, review)
                server.quit()
            counter += 1



def yelp_scrape():
    response = req.get(yelp_url)
    soup = bs(response.text, 'html.parser')
    results = soup.find_all('div', class_="review-content")
    counter = 0
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("dan.brueckman@gmail.com", "")
    for result in results:
        if counter < 10:
            review = result.find('p').text
            for c in string.punctuation:
                reviews = review.replace(c," ")
            if (" Dan" in reviews) or (" dan" in reviews):
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login("dan.brueckman@gmail.com", "")
                server.sendmail(from_address, to_address, review)
                server.quit()
            counter += 1

#sched.add_job(yelp_scrape, 'interval', days = 2)
#sched.add_job(open_table_scrape, 'interval', days = 2)
#sched.start()

open_table_scrape()
#yelp_scrape()

