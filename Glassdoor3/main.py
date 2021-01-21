'''
main.py
----------
Matthew Chatham
June 6, 2018

Given a company's landing page on Glassdoor and an output filename, scrape the
following information about each employee review:

Review date
Employee position
Employee location
Employee status (current/former)
Review title
Employee years at company
Number of helpful votes
Pros text
Cons text
Advice to mgmttext
Ratings for each of 5 categories
Overall rating
'''

import time
import pandas as pd
from argparse import ArgumentParser
import argparse
import logging
import logging.config
from selenium import webdriver as wd
import selenium
from selenium.webdriver import ActionChains
import numpy as np
from schema import SCHEMA #list of all relevant variables located in the same dir/schema.py
import json
import urllib
import datetime as dt
import os

start = time.time()

DEFAULT_URL = ('https://www.glassdoor.com/Overview/Working-at-'
               'Premise-Data-Corporation-EI_IE952471.11,35.htm')

parser = ArgumentParser()
parser.add_argument('-u', '--url',
                    help='URL of the company\'s Glassdoor landing page.',
                    default=DEFAULT_URL)
parser.add_argument('-f', '--file', default='glassdoor_ratings.csv',
                    help='Output file.')
parser.add_argument('--headless', action='store_true',
                    help='Run Chrome in headless mode.')
parser.add_argument('--username', help='Email address used to sign in to GD.')
parser.add_argument('-p', '--password', help='Password to sign in to GD.')
parser.add_argument('-c', '--credentials', help='Credentials file')
parser.add_argument('-l', '--limit', default=50000,
                    action='store', type=int, help='Max reviews to scrape')
parser.add_argument('--start_from_url', action='store_true',
                    help='Start scraping from the passed URL.')
parser.add_argument(
    '--max_date', help='Latest review date to scrape.\
    Only use this option with --start_from_url.\
    You also must have sorted Glassdoor reviews ASCENDING by date.',
    type=lambda s: dt.datetime.strptime(s, "%Y-%m-%d"))
parser.add_argument(
    '--min_date', help='Earliest review date to scrape.\
    Only use this option with --start_from_url.\
    You also must have sorted Glassdoor reviews DESCENDING by date.',
    type=lambda s: dt.datetime.strptime(s, "%Y-%m-%d"))
args = parser.parse_args() #e.g. args.file or args.url

if not args.start_from_url and (args.max_date or args.min_date):
    raise Exception(
        'Invalid argument combination:\
        No starting url passed, but max/min date specified.'
    )
elif args.max_date and args.min_date:
    raise Exception(
        'Invalid argument combination:\
        Both min_date and max_date specified.'
    )

if args.credentials:
    with open(args.credentials) as f:
        d = json.loads(f.read())
        args.username = d['username']
        args.password = d['password']
else:
    try:
        with open('secret.json') as f:
            d = json.loads(f.read())
            args.username = d['username']
            args.password = d['password']
    except FileNotFoundError:
        msg = 'Please provide Glassdoor credentials.\
        Credentials can be provided as a secret.json file in the working\
        directory, or passed at the command line using the --username and\
        --password flags.'
        raise Exception(msg)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)
formatter = logging.Formatter(
    # 'PROCESS1 %(asctime)s %(levelname)s %(lineno)d: %(filename)s(%(process)d) - %(message)s')
    'PROCESS3 %(asctime)s - %(message)s', "%H:%M:%S")
ch.setFormatter(formatter)

logging.getLogger('selenium').setLevel(logging.CRITICAL)
logging.getLogger('selenium').setLevel(logging.CRITICAL)


def scrape(field, review, author):

    def company_name(review):
        return args.file.split(".")[0] #e.g. Microsoft.csv -> Microsoft

    def scrape_date(review):
        return review.find_element_by_tag_name('time').get_attribute('datetime')

    def scrape_emp_title(review): #get employee titel from .authorJobTitle
        if 'Anonymous Employee' not in author.text: #Former Employee - Anonymous Employee
            if "Employee" in author.text and "-" in author.text: #Former Employee - Director 
                res = author.find_element_by_class_name('authorJobTitle').text.split('-')[1]
            else:
                try:
                    res = author.find_element_by_class_name('authorJobTitle').text
                except Exception:
                    # logger.warning('Failed to scrape employee_title')
                    res = np.nan
        else:
            res = np.nan
        return res

    def scrape_location(review): #get location from .authorLocation
        try:
            res = author.find_element_by_class_name(
                'authorLocation').text
        except Exception:
            res = np.nan
        return res

    def scrape_status(review): #get status from the first part of .authorJobTitle
        try:
            if "Current Employee" in author.text or "Former Employee" in author.text:
                res = author.text.split('-')[0].strip()
            else:
                res = np.nan
        except Exception:
            # logger.warning('Failed to scrape employee_status')
            res = np.nan
        return res

    def scrape_rev_title(review):
        return review.find_element_by_class_name('summary').text.strip('"')

    def scrape_years(review):
        res = review.find_element_by_class_name('mainText').text.strip('"')
        return res

    def scrape_helpful(review):
        try:
            helpful = review.find_element_by_class_name('helpfulCount').text.replace('"','')
            res = helpful[helpful.find('(') + 1: -1]
        except Exception:
            res = 0
        return res

    def expand_show_more():
        try:
            # more_content = section.find_element_by_class_name('moreContent')
            # more_link = review.find_element_by_class_name('v2__EIReviewDetailsV2__continueReading')
            # more_link.click() #doesnt work in headless mode since "Continue reading" is not clickable due to an overlay -> use javascript click
            continue_reading = "document.getElementsByClassName('v2__EIReviewDetailsV2__continueReading')[0].click();"
            browser.execute_script(continue_reading)
        except Exception:
            pass

    def scrape_pros(review):
        try:
            pros = review.find_element_by_class_name('v2__EIReviewDetailsV2__fullWidth')
            res = pros.text.replace("Pros\n", "").replace("\n",". ").replace(";",".").strip() #otherwise headline ("Pros\n") of every review is also copied. if user has line breaks in his review, these will be replaced with dots.
        except Exception:
            res = np.nan
        return res

    def scrape_cons(review):
        try:
            cons = review.find_elements_by_class_name('v2__EIReviewDetailsV2__fullWidth')[1]
            res = cons.text.replace("Cons\n", "").replace("\n",". ").replace(";",".").strip() #otherwise headline ("Pros\n") of every review is also copied. if user has line breaks in his review, these will be replaced with dots.
        except Exception:
            res = np.nan
        return res

    def scrape_advice(review):
        if len(review.find_elements_by_class_name('v2__EIReviewDetailsV2__fullWidth')) < 3: #no response, otherwise >= 3 if there is a reponse
            try:
                expand_show_more()
                advice = review.find_elements_by_class_name('v2__EIReviewDetailsV2__fullWidth')[2] #can only be found if continue reading is clicked first
                res = advice.text.replace("Advice to Management\n", "").replace("\n",". ").replace(";",".").strip() #otherwise headline ("Pros\n") of every review is also copied. if user has line breaks in his review, these will be replaced with dots.
            except Exception: #as e
                # print(getattr(e, 'message', repr(e)))
                # print(getattr(e, 'message', str(e)))
                res = np.nan
        elif len(review.find_elements_by_class_name('v2__EIReviewDetailsV2__fullWidth')) >= 3: #expand already executed from prior if part?
            try:
                expand_show_more()
                advice = review.find_elements_by_class_name('v2__EIReviewDetailsV2__fullWidth')[2] #can only be found if continue reading is clicked first
                if "Advice to Management" in advice.text:
                    res = advice.text.replace("Advice to Management\n", "").replace("\n",". ").replace(";",".").strip() #otherwise headline ("Pros\n") of every review is also copied. if user has line breaks in his review, these will be replaced with dots.
                else:
                    res = np.nan
            except Exception: #as e
                # print(getattr(e, 'message', repr(e)))
                # print(getattr(e, 'message', str(e)))
                res = np.nan
        else:
            res = np.nan

        return res

    def scrape_response(review):
        if len(review.find_elements_by_class_name('v2__EIReviewDetailsV2__fullWidth')) == 4: #advice to mngmt and response
            try:
                response = review.find_elements_by_class_name('v2__EIReviewDetailsV2__fullWidth')[3]
                res = response.text.replace("\n",". ").replace(";",".").strip() #otherwise headline ("Pros\n") of every review is also copied. if user has line breaks in his review, these will be replaced with dots.
            except Exception: #as e
                # print(getattr(e, 'message', repr(e)))
                # print(getattr(e, 'message', str(e)))
                res = np.nan
        elif len(review.find_elements_by_class_name('v2__EIReviewDetailsV2__fullWidth')) == 3 and "Advice to Management" not in review.find_elements_by_class_name('v2__EIReviewDetailsV2__fullWidth')[2].text: #only response
            try:
                response = review.find_elements_by_class_name('v2__EIReviewDetailsV2__fullWidth')[2]
                res = response.text.replace("\n",". ").replace(";",".").strip() #otherwise headline ("Pros\n") of every review is also copied. if user has line breaks in his review, these will be replaced with dots.
            except Exception: #as e
                # print(getattr(e, 'message', repr(e)))
                # print(getattr(e, 'message', str(e)))
                res = np.nan
        else:
            res = np.nan
        
        return res

    def scrape_overall_rating(review):
        try:
            overall = review.find_element_by_class_name("v2__EIReviewsRatingsStylesV2__ratingNum").text
            res = overall
        except Exception:
            res = np.nan
        return res

    def _scrape_subrating(subratingtext, subratingindex):
        try:
            ratings = review.find_element_by_class_name('gdStars') #info with the 5 rating subcategories
            subratings = ratings.find_element_by_class_name('subRatings').find_elements_by_tag_name('li') #each subrating has an own list item
            if(len(subratingtext)) == 5: # if there are all 5 subratings, then the order of them will always be identical
                res = subratings[subratingindex].find_element_by_class_name('gdBars').get_attribute('title')
                return res
            else: # if there is atleast one subrating missing, all of them need to be iterated through
                for i in subratings:
                    if i.find_element_by_tag_name('div').get_attribute('innerText') == subratingtext: #.text doesnt work since element isnt present in the viewport
                        res = i.find_element_by_class_name('gdBars').get_attribute('title') #get float value of current sub rating
                        return res
                    res = np.nan #will not get here if element has already been found
        except Exception:
            res = np.nan
        return res

        #old approach. doesnt work when review is missing >= 1 of the subrating-categories (subratings get mismatched)
        # try:
        #     ratings = review.find_element_by_class_name('gdStars')
        #     subratings = ratings.find_element_by_class_name('subRatings').find_element_by_tag_name('ul')
        #     this_one = subratings.find_elements_by_tag_name('li')[i]
        #     res = this_one.find_element_by_class_name('gdBars').get_attribute('title')
        # except Exception:
        #     res = np.nan

    def scrape_work_life_balance(review):
        return _scrape_subrating("Work/Life Balance", 0) #go for subratingindex if all 5 subratings exist

    def scrape_culture_and_values(review):
        return _scrape_subrating("Culture & Values", 1)

    def scrape_career_opportunities(review):
        return _scrape_subrating("Career Opportunities", 2)

    def scrape_comp_and_benefits(review):
        return _scrape_subrating("Compensation and Benefits", 3)

    def scrape_senior_management(review):
        return _scrape_subrating("Senior Management", 4)

    def scrape_recommends(review):
        try:
            res = review.find_element_by_class_name('recommends').text
            res = res.split('\n')
            if "Recommend" in res[0]: #recommends always takes the first index // ["Doesn't Recommend", 'Recommends']
                return res[0]
            else:
                return np.nan
        except:
            return np.nan
    
    def scrape_outlook(review):
        try:
            res = review.find_element_by_class_name('recommends').text
            res = res.split('\n')
            if len(res) == 3 and "Outlook" in res[1]: #standard case
                return res[1]
            elif len(res) < 3:
                if "Outlook" in res[0]: #outlook and approval
                    return res[0]
                elif "Outlook" in res[1]: #recommends and outlook
                    return res[1]
                else: 
                    return np.nan
            # if len(res) == 2 or len(res) == 3:
            #     if 'CEO' in res[1]:
            #         return np.nan
            #     return res[1]
            # return np.nan
        except:
            return np.nan
    
    def scrape_approve_ceo(review):
        try:
            res = review.find_element_by_class_name('recommends').text
            res = res.split('\n')
            if len(res) == 3:
                return res[2]
            elif len(res) < 3:
                if "CEO" in res[0]: #only CEO
                    return res[0]
                elif "CEO" in res[1]: #recommends OR outlook and ceo
                    return res[1]
                else:
                    return np.nan
        except:
            return np.nan

    funcs = [
        company_name,
        scrape_date,
        scrape_emp_title,
        scrape_location,
        scrape_status,
        scrape_rev_title,
        scrape_years,
        scrape_pros,
        scrape_cons,
        scrape_overall_rating,
        scrape_work_life_balance,
        scrape_culture_and_values,
        scrape_career_opportunities,
        scrape_comp_and_benefits,
        scrape_senior_management,
        scrape_recommends,
        scrape_outlook,
        scrape_approve_ceo,
        scrape_helpful,
        scrape_advice,
        scrape_response,
    ]

    fdict = dict((s, f) for (s, f) in zip(SCHEMA, funcs))

    return fdict[field](review)


def extract_from_page():

    def is_featured(review):
        try:
            review.find_element_by_class_name('featuredFlag')
            return True
        except selenium.common.exceptions.NoSuchElementException:
            return False

    def extract_review(review):
        try:
            author = review.find_element_by_class_name('authorInfo') #consisting of .authorJobTitle and .authorLocation
            res = {}
            # import pdb;pdb.set_trace()
            for field in SCHEMA:
                res[field] = scrape(field, review, author)

            assert set(res.keys()) == set(SCHEMA)
            return res
        except: #if a review is blocked by glassdoor
            res = {}
            for index, field in enumerate(SCHEMA):
                if index == 0:
                    res[field] = args.file.split(".")[0] #e.g. Microsoft.csv -> Microsoft
                elif index == 1:
                    res[field] = "ERROR (Content Blocked)"
                else:
                    res[field] = ""
            return res

    # logger.info(f'Extracting reviews from page {page[0]}')

    res = pd.DataFrame([], columns=SCHEMA)

    global reviews #set reviews as global variable so that it can be used in main() to check whether there are any reviews on the current page
    reviews = browser.find_elements_by_class_name('empReview') #len(reviews) == 0 if there are no reviews on the current page
    logger.info(f'{args.file}: Found {len(reviews)} reviews on page {page[0]}')


    for review in reviews:
        if not is_featured(review):
            data = extract_review(review)
            # logger.info(f'Scraped data for "{data["review_title"]}" ({data["date"]})') #spams the log since every review is displayed
            res.loc[idx[0]] = data
        else:
            logger.info('Discarding a featured review')
        idx[0] = idx[0] + 1

    if args.max_date and \
        (pd.to_datetime(res['date']).max() > args.max_date) or \
            args.min_date and \
            (pd.to_datetime(res['date']).min() < args.min_date):
        logger.info('Date limit reached, ending process')
        date_limit_reached[0] = True

    return res


def more_pages():
    # outdated selector (before dec 2020)
    # try:
    #     # paging_control = browser.find_element_by_class_name('pagingControls')
    #     next_ = browser.find_element_by_class_name('pagination__PaginationStyle__next')
    #     next_.find_element_by_tag_name('a')
    #     return True
    # except selenium.common.exceptions.NoSuchElementException:
    #     return False
    try:
        # if len(reviews) == 0:
        #     return False
        # else:
        #     return True

        # alternative from git (jan 2021)
        current = browser.find_element_by_class_name('selected')
        pages = browser.find_element_by_class_name('pageContainer').text.split()
        if int(pages[-1]) != int(current.text): #current page unequal last clickable page in the site navigation pane
            return True
        else:
            return False
    except selenium.common.exceptions.NoSuchElementException:
        return False


def go_to_next_page():
    # logger.info(f'{args.file}: Going to page {page[0] + 1}')
    # paging_control = browser.find_element_by_class_name('pagingControls')
    # next_ = browser.find_element_by_class_name(
    #     'pagination__PaginationStyle__next').find_element_by_tag_name('a')
    # browser.get(next_.get_attribute('href')) #The driver.get method will navigate to a page given by the URL
    next_ = browser.find_element_by_class_name('nextButton')
    current_before = int(browser.find_element_by_class_name('selected').text)
    # logger.info(f"current_before page before click: {current_before}")
    ActionChains(browser).click(next_).perform() #click next button
    time.sleep(2)
    current_after = int(browser.find_element_by_class_name('selected').text)
    # logger.info(f"current_after page after click: {current_after}")
    if current_after == current_before: #apparently the next button is hidden the first time a page is loaded in headless mode?!
        # logger.info(f"reclick next button")
        go_to_next_page()
    else:
        page[0] = page[0] + 1


def no_reviews():
    return False
    # TODO: Find a company with no reviews to test on


def navigate_to_reviews():
    logger.info('Navigating to company reviews')

    browser.get(args.url)
    time.sleep(1)

    if no_reviews():
        logger.info('No reviews to scrape. Bailing!')
        return False

    reviews_cell = browser.find_element_by_xpath(
        '//a[@data-label="Reviews"]')
    reviews_path = reviews_cell.get_attribute('href')
    
    # reviews_path = driver.current_url.replace('Overview','Reviews')
    browser.get(reviews_path)
    time.sleep(1)
    return True


def sign_in():
    logger.info(f'Signing in to {args.username}')

    url = 'https://www.glassdoor.com/profile/login_input.htm'
    # url = 'https://www.glassdoor.com'
    browser.get(url)

    # time.sleep(120) #in order the set glassdoor to english and avoid country redirect, activate the sleep, start the script for one company, and then set language in the bottom right of the webpage in the non-headless chromium

    # import pdb;pdb.set_trace()

    email_field = browser.find_element_by_name('username')
    password_field = browser.find_element_by_name('password')
    submit_btn = browser.find_element_by_xpath('//button[@type="submit"]')

    email_field.send_keys(args.username)
    password_field.send_keys(args.password)
    submit_btn.click()

    time.sleep(3)
    browser.get(args.url)


def get_browser():
    logger.info('Configuring browser')
    chrome_options = wd.ChromeOptions()
    if args.headless: #dont set user-data-dir, otherwise chromium wont load for whatever reason. headless still uses cookies though
        chrome_options.add_argument('--remote-debugging-port=45449') #use different port for different processes
        chrome_options.add_argument('--headless')
    else:
        chrome_options.add_argument("user-data-dir=selenium3") #saves cookies -> set language the United States in the bottom right
    chrome_options.add_argument('log-level=3')
    # chrome_options.add_argument('--no-sandbox') # Bypass OS security model
    browser = wd.Chrome('F://Coding//Projects//Glassdoor//Glassdoor3//chromedriver.exe', options=chrome_options) #change for each process
    return browser


def get_current_page():
    # logger.info('Getting current page number')
    # paging_control = browser.find_element_by_class_name('eiReviews__EIReviewsPageStyles__pagination noTabover mt')
    try:
        current = int(browser.find_element_by_class_name('selected').text)
        logger.info(f"current page: {current}")
        return current
    except selenium.common.exceptions.NoSuchElementException: #if there is only one review page, there will be no page indicator
        logger.info("0")
        return 0


def verify_date_sorting():
    logger.info('Date limit specified, verifying date sorting')
    ascending = urllib.parse.parse_qs(
        args.url)['sort.ascending'] == ['true']

    if args.min_date and ascending:
        raise Exception(
            'min_date required reviews to be sorted DESCENDING by date.')
    elif args.max_date and not ascending:
        raise Exception(
            'max_date requires reviews to be sorted ASCENDING by date.')


browser = get_browser()
page = [1]
idx = [0]
date_limit_reached = [False]
# valid_page = [True]


def main():

    # logger.info(f'Scraping up to {args.limit} reviews.')

    res = pd.DataFrame([], columns=SCHEMA)

    # time.sleep(120) #to set cookies
    # sign_in()

    if not args.start_from_url:
        reviews_exist = navigate_to_reviews()
        if not reviews_exist:
            return
    elif args.max_date or args.min_date:
        verify_date_sorting()
        browser.get(args.url)
        page[0] = get_current_page()
        logger.info(f'Starting from page {page[0]:,}.')
        time.sleep(1)
    else: #1. opens page
        browser.get(args.url)
        try:
            total_english_reviews = browser.find_element_by_css_selector('.col-6.my-0').text.split()[0] #eg 175 English reviews out of 191 -> 175
        except:
            total_english_reviews = 0
        logger.info(f'Scraping {total_english_reviews} total reviews from {args.file.split(".")[0]}')
        # res = res.append({"company_name": args.file.split(".")[0], "date": "TOTAL", "employee_title": total_english_reviews}, ignore_index=True) #save total amount of english reviews in the 2nd row of the csv file
        page[0] = get_current_page()
        logger.info(f'Starting from page {page[0]:,}.')
        time.sleep(5)

    reviews_df = extract_from_page() #2. extracts and appends reviews to dataframe from current page
    res = res.append(reviews_df)

    # import pdb;pdb.set_trace()

    #3. rinse and repeat if there are more pages
    while more_pages() and\
            len(res) + 1 < args.limit and\
            len(reviews) !=0 and\
            not date_limit_reached[0]:
        go_to_next_page() #replace with browser.get(f"xyz_P{20}.htm?sort.sortType=RD&sort.ascending=false&filter.iso3Language=eng")
        reviews_df = extract_from_page()
        res = res.append(reviews_df)
        # logger.info(len(res)) #19, 29,39,... last digit can be random due to discarded reviews
        if int(len(res)/10) % 5 == 0: #save after every 50 scraped reviews
            logger.info(f"Saved state after {len(res)} reviews")
            export_path = os.path.join("F://Coding//Projects//Glassdoor//Glassdoor3//csvs", args.file)
            res.to_csv(path_or_buf = export_path, index=False, encoding='utf-8')

    logger.info(f'Writing {len(res)} reviews to file {args.file}')
    export_path = os.path.join("F://Coding//Projects//Glassdoor//Glassdoor3//csvs", args.file)
    res.to_csv(path_or_buf = export_path, index=False, encoding='utf-8')
    # res.to_excel(export_path, index=False)

    browser.quit() #quit current chromium session

    end = time.time()
    logger.info(f'Finished in {end - start} seconds')


if __name__ == '__main__':
    main()
