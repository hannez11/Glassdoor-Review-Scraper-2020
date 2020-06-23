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
        # self.pages = [("https://www.glassdoor.com/Reviews/Papa-John-s-Reviews-E2363_P280.htm?sort.sortType=RD&sort.ascending=false", "ewr")]

        self.pages = [('"https://www.glassdoor.com/Reviews/PRA-Group-Reviews-E975783.htm"', 'PRAGroup'), ('"https://www.glassdoor.com/Reviews/PRA-Health-Sciences-Reviews-E7380.htm"', 'PRAHealthSciences'), ('"https://www.glassdoor.com/Reviews/Precigen-Reviews-E2445665.htm"', 'Precigen'), ('"https://www.glassdoor.com/Reviews/Preferred-Apartment-Communities-Reviews-E354632.htm"', 'PreferredApartmentCommunities'), ('"https://www.glassdoor.com/Reviews/Preformed-Line-Products-Reviews-E21452.htm"', 'PreformedLineProductsCompany'), ('"https://www.glassdoor.com/Reviews/Premier-Reviews-E2076567.htm"', 'Premier'), ('"https://www.glassdoor.com/Reviews/Premier-Financial-Bancorp-Reviews-E6051.htm"', 'PremierFinancialBancorp'), ('"https://www.glassdoor.com/Reviews/Prevail-Therapeutics-Reviews-E2207217.htm"', 'PrevailTherapeutics'), ('"https://www.glassdoor.com/Reviews/PriceSmart-Reviews-E7189.htm"', 'PriceSmart'), ('"https://www.glassdoor.com/Reviews/PrimeEnergy-Reviews-E5002.htm"', 'PrimeEnergyResources'), ('"https://www.glassdoor.com/Reviews/Primerica-Reviews-E13616.htm"', 'Primerica'), ('"https://www.glassdoor.com/Reviews/Principal-Financial-Group-Reviews-E2941.htm"', 'PrincipalFinancialGroup'), ('"https://www.glassdoor.com/Reviews/Priority-Payment-Systems-Reviews-E405672.htm"', 'PriorityTechnologyHoldings'), ('"https://www.glassdoor.com/Reviews/ProAssurance-Reviews-E1239.htm"', 'ProAssurance'), ('""', 'ProfessionalHoldingCorp.'), ('"https://www.glassdoor.com/Reviews/Progress-Reviews-E2083.htm"', 'ProgressSoftware'), ('"https://www.glassdoor.com/Reviews/Prologis-Reviews-E2631.htm"', 'Prologis'), ('"https://www.glassdoor.com/Reviews/Proofpoint-Reviews-E39140.htm"', 'Proofpoint'), ('"https://www.glassdoor.com/Reviews/ProPetro-Services-Reviews-E710481.htm"', 'ProPetroHoldingCorp.'), ('"https://www.glassdoor.com/Reviews/ProSight-Specialty-Insurance-Reviews-E1695.htm"', 'ProSightGlobal'), ('"https://www.glassdoor.com/Reviews/Protagonist-Therapeutics-Reviews-E1924707.htm"', 'ProtagonistTherapeutics'), ('"https://www.glassdoor.com/Reviews/Protective-Insurance-Reviews-E1164.htm"', 'ProtectiveInsurance'), ('"https://www.glassdoor.com/Reviews/Prothena-Reviews-E1036145.htm"', 'Prothena')
        ]

        #('"https://www.glassdoor.com/Reviews/PayPal-Reviews-E9848.htm"',"PayPalHoldings"),('"https://www.glassdoor.com/Reviews/Parsons-Corporation-Reviews-E4006.htm"',"Parsons"),
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
            if i % 2 == 0 and i % 3 != 0: #even
                print("CURRENT FIRM P2:", page[1]) 
                command = "python main.py --headless --start_from_url" + " -f " + page[1] + ".csv" + " --url " + f'"{page[0]}?sort.sortType=RD&sort.ascending=false"' #DOESNT DISPLAY BROWSER
                os.system(command)
                self.done.append(page[1])
                print("Process 2 done so far:", self.done)

        print("Process 2 done")

    def process3(self):
        os.chdir("F://Coding//Projects//Glassdoor//Glassdoor3")
        for i, page in enumerate(self.pages, 1):
            if i % 3 == 0: #divisable by 3
                print("CURRENT FIRM P3:", page[1]) 
                command = "python main.py --headless --start_from_url" + " -f " + page[1] + ".csv" + " --url " + f'"{page[0]}?sort.sortType=RD&sort.ascending=false"' #DOESNT DISPLAY BROWSER
                os.system(command)
                self.done.append(page[1])
                print("Process 3 done so far:", self.done)

        print("Process 3 done")

    def start(self):
        if __name__ == "__main__": 
            p1 = multiprocessing.Process(target=self.process1, args=())
            p2 = multiprocessing.Process(target=self.process2, args=())
            p3 = multiprocessing.Process(target=self.process3, args=())

            # starting process 1
            p1.start()
            # starting process 2
            p2.start() #uncomment to use second process
            # starting process 3
            p3.start() #uncomment to use third process

            
Multi().start()
