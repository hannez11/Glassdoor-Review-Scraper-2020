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
1 CHECK WHETHER CHROMIUM COOKIES FOLDER IS DIFFERENT FOR EACH PROCESS
chrome_options.add_argument("user-data-dir=processnumber)

2 CHANGE PORT (for headless mode)
chrome_options.add_argument('--remote-debugging-port=45450') #use different port for different processes

3 CHANGE chromedriver folder
browser = wd.Chrome('F://Coding//Projects//Glassdoor//Glassdoor3//chromedriver.exe', options=chrome_options) #change for each process

4 CHECK WHETHER CSV SAVE PATH IS DIFFERENT FOR EACH PROCESS (not necessary)
export_path = os.path.join("C:/Users/hannez/Glassdoor/csvs/", args.file)
!!!
'''

import os
import multiprocessing 
import time

class Multi:
    def __init__(self):
        self.pages = [('"https://www.glassdoor.com/Reviews/Endo-Pharmaceuticals-Reviews-E11705.htm"',"Endo_International_plc"), ('"https://www.glassdoor.com/Reviews/Post-Holdings-Reviews-E826249.htm"',"Post_Holdings"), ('"https://www.glassdoor.com/Reviews/Insight-Reviews-E3823.htm"',"Insight_Enterprises"), ('"https://www.glassdoor.com/Reviews/Halliburton-Reviews-E307.htm"',"Halliburton_Company"), ('"https://www.glassdoor.com/Reviews/Owens-and-Minor-Reviews-E501.htm"',"Owens_AND_Minor"), ('"https://www.glassdoor.com/Reviews/Endo-Pharmaceuticals-Reviews-E11705.htm"',"Endo_International_plc"), ('"https://www.glassdoor.com/Reviews/Moody-s-Corporation-Reviews-E11303.htm"',"Moodys"), ('"https://www.glassdoor.com/Reviews/MACOM-Reviews-E19802.htm"',"MACOM_Technology_Solutions_Holdings"), ('"https://www.glassdoor.com/Reviews/OSI-Systems-Reviews-E6973.htm"',"OSI_Systems"), ('"https://www.glassdoor.com/Reviews/Renasant-Reviews-E2163.htm"',"Renasant"), ('"https://www.glassdoor.com/Reviews/Universal-Logistics-Holdings-Reviews-E37852.htm"',"Universal_Logistics_Holdings"), ('"https://www.glassdoor.com/Reviews/ON-Semiconductor-Reviews-E9708.htm"',"ON_Semiconductor"), ('"https://www.glassdoor.com/Reviews/FOSSIL-GROUP-Reviews-E3160185.htm"',"Fossil_Group"), ('"https://www.glassdoor.com/Reviews/Skyworks-Solutions-Reviews-E762.htm"',"Skyworks_Solutions"), ('"https://www.glassdoor.com/Reviews/Boston-Scientific-Reviews-E2187.htm"',"Boston_Scientific"), ('"https://www.glassdoor.com/Reviews/First-Merchants-Reviews-E1414.htm"',"First_Merchants"), ('"https://www.glassdoor.com/Reviews/Hilltop-Holdings-Reviews-E29440.htm"',"Hilltop_Holdings"), ('"https://www.glassdoor.com/Reviews/Univest-Reviews-E6917.htm"',"Univest_Financial"), ('"https://www.glassdoor.com/Reviews/Cpsi-Reviews-E14935.htm"',"Computer_Programs_and_Systems"), ('"https://www.glassdoor.com/Reviews/VOXX-International-Reviews-E776.htm"',"VOXX_International"), ('"https://www.glassdoor.com/Reviews/Brookline-Bancorp-Reviews-E7475.htm"',"Brookline_Bancorp"), ('"https://www.glassdoor.com/Reviews/KKR-Reviews-E2865.htm"',"KKR_AND_Co"), ('"https://www.glassdoor.com/Reviews/Pacific-Premier-Reviews-E6696.htm"',"Pacific_Premier_Bancorp"), ('"https://www.glassdoor.com/Reviews/Stamps-com-Reviews-E8800.htm"',"Stampscom"), ('"https://www.glassdoor.com/Reviews/Quanta-Services-Reviews-E7594.htm"',"Quanta_Services"), ('"https://www.glassdoor.com/Reviews/Philip-Morris-International-Reviews-E7745.htm"',"Philip_Morris_International"), ('"https://www.glassdoor.com/Reviews/Middleby-Reviews-E946.htm"',"The_Middleby"), ('"https://www.glassdoor.com/Reviews/PTC-Reviews-E1855.htm"',"PTC"), ('"https://www.glassdoor.com/Reviews/Heartland-Financial-USA-Reviews-E16292.htm"',"Heartland_Financial_USA"), ('"https://www.glassdoor.com/Reviews/Middleby-Reviews-E946.htm"',"The_Middleby"), ('"https://www.glassdoor.com/Reviews/Providence-Service-Reviews-E15586.htm"',"The_Providence_Service"), ('"https://www.glassdoor.com/Reviews/ProAssurance-Reviews-E1239.htm"',"ProAssurance"), ('"https://www.glassdoor.com/Reviews/CoreLogic-Reviews-E30994.htm"',"CoreLogic"), ('"https://www.glassdoor.com/Reviews/Motorola-Solutions-Reviews-E427189.htm"',"Motorola_Solutions"), ('"https://www.glassdoor.com/Reviews/Fidelity-National-Financial-Reviews-E39083.htm"',"Fidelity_National_Financial"), ('"https://www.glassdoor.com/Reviews/Helen-of-Troy-Reviews-E1482.htm"',"Helen_of_Troy_Limited"), ('"https://www.glassdoor.com/Reviews/Columbus-McKinnon-Reviews-E5683.htm"',"Columbus_McKinnon"), ('"https://www.glassdoor.com/Reviews/Align-Technology-Reviews-E12898.htm"',"Align_Technology"), ('"https://www.glassdoor.com/Reviews/Altair-Engineering-Reviews-E20320.htm"',"Altair_Engineering"), ('"https://www.glassdoor.com/Reviews/Viatris-Reviews-E4143192.htm"',"Viatris"), ('"https://www.glassdoor.com/Reviews/Precigen-Reviews-E2445665.htm"',"Precigen"), ('"https://www.glassdoor.com/Reviews/Accenture-Reviews-E4138.htm"',"Accenture_plc"), ('"https://www.glassdoor.com/Reviews/Calix-Reviews-E13819.htm"',"Calix"), ('"https://www.glassdoor.com/Reviews/The-E-W-Scripps-Company-Reviews-E1355.htm"',"The_EW_Scripps_Company"), ('"https://www.glassdoor.com/Reviews/Mercantile-Bank-Reviews-E7088.htm"',"Mercantile_Bank"), ('"https://www.glassdoor.com/Reviews/LabCorp-Reviews-E1679.htm"',"Laboratory_of_America_Holdings"), ('"https://www.glassdoor.com/Reviews/ACI-Worldwide-Reviews-E4024.htm"',"ACI_Worldwide"), ('"https://www.glassdoor.com/Reviews/1-800-Flowers-com-Reviews-E4117.htm"',"1-800-FLOWERSCOM"), ('"https://www.glassdoor.com/Reviews/Tetra-Tech-Reviews-E1775.htm"',"Tetra_Tech"), ('"https://www.glassdoor.com/Reviews/TransDigm-Reviews-E22279.htm"',"TransDigm_Group"), ('"https://www.glassdoor.com/Reviews/CalAmp-Reviews-E1219.htm"',"CalAmp"), ('"https://www.glassdoor.com/Reviews/Apollo-Global-Management-Reviews-E2715.htm"',"Apollo_Global_Management"), ('"https://www.glassdoor.com/Reviews/G-III-Apparel-Reviews-E1126.htm"',"G-III_Apparel_Group"), ('"https://www.glassdoor.com/Reviews/Micron-Technology-Reviews-E1648.htm"',"Micron_Technology"), ('"https://www.glassdoor.com/Reviews/Berkshire-Bank-Reviews-E12187.htm"',"Berkshire_Hills_Bancorp"), ('"https://www.glassdoor.com/Reviews/McKesson-Reviews-E434.htm"',"McKesson"), ('"https://www.glassdoor.com/Reviews/Twitter-Reviews-E100569.htm"',"Twitter"), ('"https://www.glassdoor.com/Reviews/Chesapeake-Utilities-Reviews-E1250.htm"',"Chesapeake_Utilities"), ('"https://www.glassdoor.com/Reviews/Knowles-Corporation-Reviews-E25451.htm"',"Knowles"), ('"https://www.glassdoor.com/Reviews/Deluxe-Corporation-Reviews-E198.htm"',"Deluxe"), ('"https://www.glassdoor.com/Reviews/Green-Plains-Reviews-E40862.htm"',"Green_Plains"), ('"https://www.glassdoor.com/Reviews/MasTec-Reviews-E1198.htm"',"MasTec"), ('"https://www.glassdoor.com/Reviews/Protolabs-Reviews-E388685.htm"',"Proto_Labs"), ('"https://www.glassdoor.com/Reviews/PPL-Reviews-E520.htm"',"PPL"), ('"https://www.glassdoor.com/Reviews/Methode-Electronics-Reviews-E1146245.htm"',"Methode_Electronics"), ('"https://www.glassdoor.com/Reviews/Nasdaq-Reviews-E12152.htm"',"Nasdaq")
        ]

        self.done = [] #is not shared between processes

    def process1(self):
        os.chdir("F://Coding//Projects//Glassdoor//Glassdoor1")
        for i, page in enumerate(self.pages, 1):
            if i % 2 != 0 and i % 3 != 0: #uneven
                print("CURRENT FIRM P1:", page[1]) 
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
            if i % 3 == 0 and i % 4 != 0: #divisible by 3
                print("CURRENT FIRM P3:", page[1]) 
                command = "python main.py --headless --start_from_url" + " -f " + page[1] + ".csv" + " --url " + f'"{page[0]}?sort.sortType=RD&sort.ascending=false"' #DOESNT DISPLAY BROWSER
                os.system(command)
                self.done.append(page[1])
                print("Process 3 done so far:", self.done)

        print("Process 3 done")

    def process4(self):
        os.chdir("F://Coding//Projects//Glassdoor//Glassdoor4")
        for i, page in enumerate(self.pages, 1):
            if i % 4 == 0: #divisible by 4
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
            time.sleep(7)
            # starting process 2
            p2.start() #uncomment to use second process
            time.sleep(9)
            # starting process 3
            p3.start() #uncomment to use third process
            time.sleep(12)
            # starting process 4
            p4.start() #uncomment to use third process

            
Multi().start()
