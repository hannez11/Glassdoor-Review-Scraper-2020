'''
multiscrape.py
----------
Jeremiah Haremza
May 9, 2018

Given a tuple of items use main.py to scrape reviews from multiple companies on Glassdoor.
Use 1 tuple per company.
List of tuples to itterate over for each command execution is named pages
each tuple in the list takes the format (url, limit, output_file_name)
each Item in the tuple is a string, hence it will need to be enclosed in quotes.
'''

'''
!!!
CHECK WHETHER CHROMIUM COOKIES FOLDER IS DIFFERENT FOR EACH PROCESS
chrome_options.add_argument("user-data-dir=XYZ)

CHECK WHETHER CSV SAVE PATH IS DIFFERENT FOR EACH PROCESS
export_path = os.path.join("C:/Users/hannez/Glassdoor/csvs/", args.file)
!!!
'''

import os
import multiprocessing 

pages1 = [
            ('"https://www.glassdoor.com/Overview/Working-at-Amazon-EI_IE6036.11,17.htm"', "5", "amazon"), 
            ('"https://www.glassdoor.com/Overview/Working-at-Chipotle-EI_IE15228.11,19.htm"', "5", "chiptole"),
            ('"https://www.glassdoor.com/Overview/Working-at-Sherwin-Williams-EI_IE599.11,27.htm"', "5", "microsoft"),
        ]

pages2 = [
            ('"https://www.glassdoor.com/Overview/Working-at-Amazon-EI_IE6036.11,17.htm"', "5", "amazon"), 
            ('"https://www.glassdoor.com/Overview/Working-at-Chipotle-EI_IE15228.11,19.htm"', "5", "chiptole"),
            ('"https://www.glassdoor.com/Overview/Working-at-Sherwin-Williams-EI_IE599.11,27.htm"', "5", "microsoft"),
        ]

def process1(liste):
    for page in liste:
        os.chdir("F://Coding//Projects//Glassdoor//Glassdoor1")
        command = "python main.py --url " + page[0] + " --limit " + page[1] + " -f " + page[2] + ".csv"
        # command = "python main.py --headless --url " + page[0] + " --limit " + page[1] + " -f " + page[2] + ".csv"
        # command = "python main.py --start_from_url" + " --limit " + page[1] + " -f " + page[2] + ".csv" + " --url " + f'"{page[0]}?sort.sortType=RD&sort.ascending=false"'
        os.system(command)

    print("Process 1 done")

def process2(liste):
    for page in liste:
        os.chdir("F://Coding//Projects//Glassdoor//Glassdoor1//Glassdoor2")
        command = "python main.py --url " + page[0] + " --limit " + page[1] + " -f " + page[2] + ".csv"
        # command = "python main.py --headless --url " + page[0] + " --limit " + page[1] + " -f " + page[2] + ".csv"
        # command = "python main.py --start_from_url" + " --limit " + page[1] + " -f " + page[2] + ".csv" + " --url " + f'"{page[0]}?sort.sortType=RD&sort.ascending=false"'
        os.system(command)

    print("Process 2 done")

if __name__ == "__main__": 
    p1 = multiprocessing.Process(target=process1, args=(pages1, )) 
    p2 = multiprocessing.Process(target=process2, args=(pages2, )) 

    # starting process 1 
    p1.start() 
    # starting process 2 
    # p2.start() 