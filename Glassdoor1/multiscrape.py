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
import time

class Multi:
    def __init__(self):
        self.pages = [
            # ('"https://www.glassdoor.com/Reviews/Cognizant-Technology-Solutions-Reviews-E8014_P2493.htm"', 'CognizantTechnologySolutionsXX6'), #1519 1901 1903 2474 2492
            # ('"https://www.glassdoor.com/Reviews/Amazon-Reviews-E6036_P1192.htm"', 'AmazonXX7'), #1104,1107 1109 1112buggy? Found 0 reviews on page 1159, 1191
            # ('"https://www.glassdoor.com/Reviews/Cisco-Systems-Reviews-E1425_P1279.htm"', 'CiscoSystemsXX4'), #1133 1273 buggy CHECK
            # ('"https://www.glassdoor.com/Reviews/CVS-Health-Reviews-E437_P339.htm"', 'CVSHealthXX4'), #Found 0 reviews on page 338, 343
            ('"https://www.glassdoor.com/Reviews/GE-Reviews-E277_P191.htm"', 'GeneralElectricCompanyXX3')
            # ('"https://www.glassdoor.com/Reviews/AT-and-T-Reviews-E613_P1701.htm"', 'ATANDTXX3'), #strange error?!
            # ('"https://www.glassdoor.com/Reviews/Apple-Reviews-E1138_P844.htm"', 'AppleXX5'), #done except 843 buggy?
        ]

        self.done = [] #is not shared between processes

    def process1(self):
        os.chdir("F://Coding//Projects//Glassdoor//Glassdoor1")
        for i, page in enumerate(self.pages, 1):
            if i % 2 != 0 and i % 3 != 0: #uneven
                print("CURRENT FIRM P1:", page[1]) 
                # command = "python main.py --url " + page[0] + " --limit " + page[1] + " -f " + page[2] + ".csv"
                # command = "python main.py --headless --url " + page[0] + " --limit " + page[1] + " -f " + page[2] + ".csv"
                # command = "python main.py --start_from_url" + " --limit " + page[1] + " -f " + page[2] + ".csv" + " --url " + f'"{page[0]}?sort.sortType=RD&sort.ascending=false"'
                # command = "python main.py --start_from_url" + " -f " + page[1] + ".csv" + " --url " + f'"{page[0]}?sort.sortType=RD&sort.ascending=false"' #DISPLAYS BROWSER
                command = "python main.py --headless --start_from_url" + " -f " + page[1] + ".csv" + " --url " + f'"{page[0]}?sort.sortType=RD&sort.ascending=false"' #DOESNT DISPLAY BROWSER
                os.system(command)
                self.done.append(page[1])
                print("Process 1 done so far:", self.done)

        print("Process 1 done")

    def process2(self):
        os.chdir("F://Coding//Projects//Glassdoor//Glassdoor2")
        for i, page in enumerate(self.pages, 1):
            if i % 2 == 0 and i % 3 != 0 and i % 4 != 0: #even
                print("CURRENT FIRM P2:", page[1]) 
                command = "python main.py --headless --start_from_url" + " -f " + page[1] + ".csv" + " --url " + f'"{page[0]}?sort.sortType=RD&sort.ascending=false"' #DOESNT DISPLAY BROWSER
                os.system(command)
                self.done.append(page[1])
                print("Process 2 done so far:", self.done)

        print("Process 2 done")

    def process3(self):
        os.chdir("F://Coding//Projects//Glassdoor//Glassdoor3")
        for i, page in enumerate(self.pages, 1):
            if i % 3 == 0 and i % 4 != 0: #divisable by 3
                print("CURRENT FIRM P3:", page[1]) 
                command = "python main.py --headless --start_from_url" + " -f " + page[1] + ".csv" + " --url " + f'"{page[0]}?sort.sortType=RD&sort.ascending=false"' #DOESNT DISPLAY BROWSER
                os.system(command)
                self.done.append(page[1])
                print("Process 3 done so far:", self.done)

        print("Process 3 done")

    def process4(self):
        os.chdir("F://Coding//Projects//Glassdoor//Glassdoor4")
        for i, page in enumerate(self.pages, 1):
            if i % 4 == 0: #divisable by 4
                print("CURRENT FIRM P4:", page[1]) 
                command = "python main.py --headless --start_from_url" + " -f " + page[1] + ".csv" + " --url " + f'"{page[0]}?sort.sortType=RD&sort.ascending=false"' #DOESNT DISPLAY BROWSER
                os.system(command)
                self.done.append(page[1])
                print("Process 4 done so far:", self.done)

        print("Process 3 done")

    def start(self):
        if __name__ == "__main__": 
            p1 = multiprocessing.Process(target=self.process1, args=())
            p2 = multiprocessing.Process(target=self.process2, args=())
            p3 = multiprocessing.Process(target=self.process3, args=())
            p4 = multiprocessing.Process(target=self.process4, args=())

            # starting process 1
            p1.start()
            # starting process 2
            time.sleep(2)
            p2.start() #uncomment to use second process
            # starting process 3
            time.sleep(4)
            p3.start() #uncomment to use third process
            # starting process 4
            time.sleep(7)
            p4.start() #uncomment to use third process

            
Multi().start()
