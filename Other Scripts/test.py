from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
import os
import time
from selenium.webdriver import ActionChains


os.chdir("F://Coding//Projects//Glassdoor//Glassdoor1")

chrome_options = wd.ChromeOptions()
# chrome_options.add_argument("user-data-dir=selenium1") #saves cookies -> set language the United States in the bottom right
chrome_options.add_argument('--remote-debugging-port=45447') #use different port for different processes
chrome_options.add_argument('--headless')
browser = wd.Chrome(options=chrome_options)

browser.get("https://www.glassdoor.com/Reviews/PagerDuty-Reviews-E704466_P7.htm?sort.sortType=RD&sort.ascending=false")
time.sleep(1)

#page navigation
# x = browser.find_element_by_css_selector('.pagination__PaginationStyle__pagination li:nth-of-type(2) a:nth-child(1)')
# y = browser.find_element_by_class_name('pagination__PaginationStyle__current')
# print("test", y.text)

#get total number of reviews
# y = browser.find_element_by_css_selector('.col-6.my-0') #get total number of reviews
# z = browser.find_element_by_css_selector('.col-6.my-0').text.split()[0]
# print("test", y.text)

#remove line break error of pros/cons
reviews = browser.find_elements_by_class_name('empReview')

#recommends (recommends, outloook, ceoapproval)
for index, review in enumerate(reviews, 1):
    if index < 6:
            res = review.find_element_by_class_name('recommends').text
            res = res.split('\n')
            print("all", res) #list?
            if "Recommends" in res[0]:
                print("recommends", res[0])
            else:
                print("recommends not found")




#overallrating
for index, review in enumerate(reviews, 1):
    if index < 4:
        print(f"review {index}")
        # ratings = review.find_element_by_class_name('gdStars')

        x = review.find_element_by_class_name("v2__EIReviewsRatingsStylesV2__ratingNum").text
        print(x)
        # overall = ratings.find_element_by_class_name('rating').find_element_by_tag_name('span').get_attribute('title')
        # print(overall)

#subratings
# for index, review in enumerate(reviews, 1):
#     if index < 4:
#         print(f"review {index}")
#         ratings = review.find_element_by_class_name('gdStars')

        # subratings = review.find_element_by_class_name('subRatings').find_elements_by_tag_name('li')
        # print(len(subratings))
        # this_one = subratings.find_elements_by_tag_name('li')[i]
        
        # for i in subratings:
            # print(i.get_attribute('innerHTML'))
            # print(i.find_element_by_tag_name('div').get_attribute('innerText')) #.text doesnt work since element isnt present in the viewport

            # print("rating", i.find_element_by_class_name('gdBars').get_attribute('title'))
        #     if i.find_element_by_tag_name('div').get_attribute('innerText') == "Work/Life Balance": #.text doesnt work since element isnt present in the viewport
                # balance_rating = i.find_element_by_class_name('gdBars').get_attribute('title') #get float value of current sub rating
        #         print(i.find_element_by_tag_name('div').get_attribute('innerText'))



# for index, review in enumerate(reviews, 1):
#     print(review.text)
    # pros = review.find_element_by_class_name('v2__EIReviewDetailsV2__fullWidth').text
    # pros2 = pros.replace("Pros\n", "").replace("\n",". ").strip()
    # if "\n" in pros2:
    #     print("yes", index, pros2)
    # else:
    #     print("no", index, pros2)

#get infos about reviewer
# for index, review in enumerate(reviews, 1):
#     if index == 7 or index == 8 or index == 10:
#         author = review.find_element_by_class_name('authorInfo') 
#         print(index, author.text)
#         # if 'Anonymous Employee' not in review.text:
#         #     res = author.find_element_by_class_name('authorJobTitle').text.split('-')[1]
#         # print(review.text)
#         # if 'in' in review.text:
#         loc = author.find_element_by_class_name('authorLocation').text
#         print("location", loc)
#         # if "Employee" in author.text:
#         #     status = author.text.split('-')[0]
#         #     print("status", status, len(status), len(status.strip()))


# get advice to management (hidden under continue button)
# for index, review in enumerate(reviews, 1):
#     if index < 6:
#         print("index:", index)
#         print("lenge1", len(review.find_elements_by_class_name('v2__EIReviewDetailsV2__fullWidth')))
        
#         try:
#             # more_link.click()
#             javaScript = "document.getElementsByClassName('v2__EIReviewDetailsV2__continueReading')[0].click();"
#             browser.execute_script(javaScript)
#             print("lenge", len(review.find_elements_by_class_name('v2__EIReviewDetailsV2__fullWidth')))
#             advice = review.find_elements_by_class_name('v2__EIReviewDetailsV2__fullWidth')[2].text
#             if len(review.find_elements_by_class_name('v2__EIReviewDetailsV2__fullWidth')) == 4:
#                 advice2 = review.find_elements_by_class_name('v2__EIReviewDetailsV2__fullWidth')[3].text
#                 print("2", advice2)
#             print("1", advice)
#         except Exception as e:
#             print(getattr(e, 'message', repr(e)))
#             print(getattr(e, 'message', str(e)))




browser.quit() #quit current chromium session

