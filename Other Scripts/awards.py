from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
import os
import time


os.chdir("C:\\Users\\hannez\\Glassdoor")

chrome_options = wd.ChromeOptions()
chrome_options.add_argument("user-data-dir=selenium") #saves cookies -> set language the United States in the bottom right
browser = wd.Chrome(options=chrome_options)

# browser.get("https://www.glassdoor.com/Reviews/UBS-Reviews-E3419_P3.htm?sort.sortType=RD&sort.ascending=false")
# time.sleep(1)
# # x = browser.find_element_by_css_selector('.pagination__PaginationStyle__pagination li:nth-of-type(2) a:nth-child(1)')
# y = browser.find_element_by_class_name('pagination__PaginationStyle__current')
# print("test", y.text)

browser.get("https://www.glassdoor.com/Overview/Working-at-NVIDIA-EI_IE7633.11,17.htm")
x = browser.find_elements_by_css_selector("a[href*='Award']")

for link in x:
    print(link.get_attribute("href"))
    print(link.text)
