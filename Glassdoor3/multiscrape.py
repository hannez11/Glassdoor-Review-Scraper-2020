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
            # ('"https://www.glassdoor.com/Reviews/AbbVie-Reviews-E649837.htm"', "AbbVie"),
            ('"https://www.glassdoor.com/Reviews/Momenta-Pharmaceuticals-Reviews-E33102.htm"', "Momenta"),
            ('"https://www.glassdoor.com/Reviews/Monarch-Casino-and-Resort-Reviews-E2390.htm"', "Monarch"),
            ('"https://www.glassdoor.com/Reviews/Allakos-Reviews-E2601148.htm', "AllakosZeroReviews"),
        ]

pages2 = [
            ('"https://www.glassdoor.com/Reviews/Bain-and-Company-Reviews-E3752.htm"', "bain"),
            ('"https://www.glassdoor.com/Reviews/Tesla-Reviews-E43129.htm"', "tesla"),
            ('"https://www.glassdoor.com/Reviews/Goldman-Sachs-Reviews-E2800.htm"', "gs"),
        ]

def process1(liste):
    for page in liste:
        os.chdir("F://Coding//Projects//Glassdoor//Glassdoor1")
        # command = "python main.py --url " + page[0] + " --limit " + page[1] + " -f " + page[2] + ".csv"
        # command = "python main.py --headless --url " + page[0] + " --limit " + page[1] + " -f " + page[2] + ".csv"
        # command = "python main.py --start_from_url" + " --limit " + page[1] + " -f " + page[2] + ".csv" + " --url " + f'"{page[0]}?sort.sortType=RD&sort.ascending=false"'
        # command = "python main.py --start_from_url" + " -f " + page[1] + ".csv" + " --url " + f'"{page[0]}?sort.sortType=RD&sort.ascending=false"' #DISPLAYS BROWSER
        command = "python main.py --headless --start_from_url" + " -f " + page[1] + ".csv" + " --url " + f'"{page[0]}?sort.sortType=RD&sort.ascending=false"' #DOESNT DISPLAY BROWSER
        os.system(command)

    print("Process 1 done")

def process2(liste):
    for page in liste:
        os.chdir("F://Coding//Projects//Glassdoor//Glassdoor2")
        # command = "python main.py --url " + page[0] + " --limit " + page[1] + " -f " + page[2] + ".csv"
        # command = "python main.py --headless --url " + page[0] + " --limit " + page[1] + " -f " + page[2] + ".csv"
        # command = "python main.py --start_from_url" + " --limit " + page[1] + " -f " + page[2] + ".csv" + " --url " + f'"{page[0]}?sort.sortType=RD&sort.ascending=false"'
        command = "python main.py --headless --start_from_url" + " -f " + page[2] + ".csv" + " --url " + f'"{page[0]}?sort.sortType=RD&sort.ascending=false"'
        os.system(command)

    print("Process 2 done")

if __name__ == "__main__": 
    p1 = multiprocessing.Process(target=process1, args=(pages1, )) 
    p2 = multiprocessing.Process(target=process2, args=(pages2, )) 

    # starting process 1 
    p1.start() 
    # starting process 2 
    # p2.start() #uncomment to use second process