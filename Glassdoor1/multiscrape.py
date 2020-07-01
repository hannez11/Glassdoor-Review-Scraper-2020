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
        self.pages = [("https://www.glassdoor.com/Reviews/Goodyear-Reviews-E292_P1.htm?sort.sortType=RD&sort.ascending=false", "TheGoodyearTireANDRubberCompany"), ('"https://www.glassdoor.com/Reviews/Waddell-and-Reed-Reviews-E7617.htm"', 'WaddellANDReedFinancial'), ('"https://www.glassdoor.com/Reviews/Wyndham-Hotels-and-Resorts-Reviews-E2310228.htm"', 'WyndhamHotelsANDResorts'), ('"https://www.glassdoor.com/Reviews/Pacific-Gas-and-Electric-Reviews-E15208.htm"',"PGANDE"), ('"https://www.glassdoor.com/Reviews/R-R-Donnelley-Reviews-E554.htm"',"R.R.DonnelleyANDSonsCompany"), ('"https://www.glassdoor.com/Reviews/Reliance-Steel-Reviews-E3693.htm"',"RelianceSteelANDAluminumCo"), ('"https://www.glassdoor.com/Reviews/S-and-P-Global-Reviews-E1259396.htm"',"SANDPGlobal"),]

        # self.pages = [
        #('"https://www.glassdoor.com/Reviews/PayPal-Reviews-E9848.htm"',"PayPalHoldings1"),
        #('"https://www.glassdoor.com/Reviews/PayPal-Reviews-E9848_P300.htm?sort.sortType=RD&sort.ascending=false"',"PayPalHoldings2"),
        #('"https://www.glassdoor.com/Reviews/Parsons-Corporation-Reviews-E4006.htm"',"Parsons"), 
        #('"https://www.glassdoor.com/Reviews/Starbucks-Reviews-E2202.htm"', 'Starbucks1'), 
        #('"https://www.glassdoor.com/Reviews/Starbucks-Reviews-E2202_P300.htm?sort.sortType=RD&sort.ascending=false"', 'Starbucks2'), 
        #('"https://www.glassdoor.com/Reviews/Starbucks-Reviews-E2202_P600.htm?sort.sortType=RD&sort.ascending=false"', 'Starbucks3'), 
        #('"https://www.glassdoor.com/Reviews/Starbucks-Reviews-E2202_P900.htm?sort.sortType=RD&sort.ascending=false"', 'Starbucks4'), 
        #('"https://www.glassdoor.com/Reviews/Starbucks-Reviews-E2202_P1200.htm?sort.sortType=RD&sort.ascending=false"', 'Starbucks5'), 
        #('"https://www.glassdoor.com/Reviews/Starbucks-Reviews-E2202_P1500.htm?sort.sortType=RD&sort.ascending=false"', 'Starbucks6'), 
        #('"https://www.glassdoor.com/Reviews/Starbucks-Reviews-E2202_P1800.htm?sort.sortType=RD&sort.ascending=false"', 'Starbucks7'), 
        #('"https://www.glassdoor.com/Reviews/Starbucks-Reviews-E2202_P2100.htm?sort.sortType=RD&sort.ascending=false"', 'Starbucks8'), 
        #('"https://www.glassdoor.com/Reviews/Starbucks-Reviews-E2202_P2400.htm?sort.sortType=RD&sort.ascending=false"', 'Starbucks9'), 
        #('"https://www.glassdoor.com/Reviews/Target-Reviews-E194_P1.htm?sort.sortType=RD&sort.ascending=false"', 'Target1'), 
        #('"https://www.glassdoor.com/Reviews/Target-Reviews-E194_P300.htm?sort.sortType=RD&sort.ascending=false"', 'Target2'), 
        #('"https://www.glassdoor.com/Reviews/Target-Reviews-E194_P600.htm?sort.sortType=RD&sort.ascending=false"', 'Target3'), 
        #('"https://www.glassdoor.com/Reviews/Target-Reviews-E194_P900.htm?sort.sortType=RD&sort.ascending=false"', 'Target4'), 
        #('"https://www.glassdoor.com/Reviews/Target-Reviews-E194_P1200.htm?sort.sortType=RD&sort.ascending=false"', 'Target5'), 
        #('"https://www.glassdoor.com/Reviews/Target-Reviews-E194_P1500.htm?sort.sortType=RD&sort.ascending=false"', 'Target6'), 
        #('"https://www.glassdoor.com/Reviews/Target-Reviews-E194_P1800.htm?sort.sortType=RD&sort.ascending=false"', 'Target7'), 
        #('"https://www.glassdoor.com/Reviews/Target-Reviews-E194_P2100.htm?sort.sortType=RD&sort.ascending=false"', 'Target8'), 
        #('"https://www.glassdoor.com/Reviews/Target-Reviews-E194_P2400.htm?sort.sortType=RD&sort.ascending=false"', 'Target9'), 
        #('"https://www.glassdoor.com/Reviews/Target-Reviews-E194_P2700.htm?sort.sortType=RD&sort.ascending=false"', 'Target10'), 
        #('"https://www.glassdoor.com/Reviews/Target-Reviews-E194_P3000.htm?sort.sortType=RD&sort.ascending=false"', 'Target11'), 
        #('"https://www.glassdoor.com/Reviews/Target-Reviews-E194_P3300.htm?sort.sortType=RD&sort.ascending=false"', 'Target12'), 
        #('"https://www.glassdoor.com/Reviews/Walmart-Reviews-E715_P1.htm?sort.sortType=RD&sort.ascending=false"', 'Walmart1'), 
        #('"https://www.glassdoor.com/Reviews/Walmart-Reviews-E715_P300.htm?sort.sortType=RD&sort.ascending=false"', 'Walmart2'), 
        #('"https://www.glassdoor.com/Reviews/Walmart-Reviews-E715_P600.htm?sort.sortType=RD&sort.ascending=false"', 'Walmart3'), 
        #('"https://www.glassdoor.com/Reviews/Walmart-Reviews-E715_P900.htm?sort.sortType=RD&sort.ascending=false"', 'Walmart4'), 
        #('"https://www.glassdoor.com/Reviews/Walmart-Reviews-E715_P1200.htm?sort.sortType=RD&sort.ascending=false"', 'Walmart5'), 
        #('"https://www.glassdoor.com/Reviews/Walmart-Reviews-E715_P1500.htm?sort.sortType=RD&sort.ascending=false"', 'Walmart6'), 
        #('"https://www.glassdoor.com/Reviews/Walmart-Reviews-E715_P1800.htm?sort.sortType=RD&sort.ascending=false"', 'Walmart7'), 
        #('"https://www.glassdoor.com/Reviews/Walmart-Reviews-E715_P2100.htm?sort.sortType=RD&sort.ascending=false"', 'Walmart8'), 
        #('"https://www.glassdoor.com/Reviews/Walmart-Reviews-E715_P2400.htm?sort.sortType=RD&sort.ascending=false"', 'Walmart9'), 
        #('"https://www.glassdoor.com/Reviews/Walmart-Reviews-E715_P2700.htm?sort.sortType=RD&sort.ascending=false"', 'Walmart10'), 
        #('"https://www.glassdoor.com/Reviews/Walmart-Reviews-E715_P3000.htm?sort.sortType=RD&sort.ascending=false"', 'Walmart11'), 
        #('"https://www.glassdoor.com/Reviews/Walmart-Reviews-E715_P3300.htm?sort.sortType=RD&sort.ascending=false"', 'Walmart12'), 
        #('"https://www.glassdoor.com/Reviews/Walmart-Reviews-E715_P3600.htm?sort.sortType=RD&sort.ascending=false"', 'Walmart14'), 
        #('"https://www.glassdoor.com/Reviews/Walmart-Reviews-E715_P3900.htm?sort.sortType=RD&sort.ascending=false"', 'Walmart15'), 
        #('"https://www.glassdoor.com/Reviews/Walmart-Reviews-E715_P4200.htm?sort.sortType=RD&sort.ascending=false"', 'Walmart16'), 
        #('"https://www.glassdoor.com/Reviews/Walmart-Reviews-E715_P4500.htm?sort.sortType=RD&sort.ascending=false"', 'Walmart17'), 
        #('"https://www.glassdoor.com/Reviews/The-Home-Depot-Reviews-E655_P1.htm?sort.sortType=RD&sort.ascending=false"', 'TheHomeDepot1'), 
        #('"https://www.glassdoor.com/Reviews/The-Home-Depot-Reviews-E655_P300.htm?sort.sortType=RD&sort.ascending=false"', 'TheHomeDepot2'), 
        #('"https://www.glassdoor.com/Reviews/The-Home-Depot-Reviews-E655_P600.htm?sort.sortType=RD&sort.ascending=false"', 'TheHomeDepot3'), 
        #('"https://www.glassdoor.com/Reviews/The-Home-Depot-Reviews-E655_P900.htm?sort.sortType=RD&sort.ascending=false"', 'TheHomeDepot4'), 
        #('"https://www.glassdoor.com/Reviews/The-Home-Depot-Reviews-E655_P1200.htm?sort.sortType=RD&sort.ascending=false"', 'TheHomeDepot5'), 
        #('"https://www.glassdoor.com/Reviews/The-Home-Depot-Reviews-E655_P1500.htm?sort.sortType=RD&sort.ascending=false"', 'TheHomeDepot6'), 
        #('"https://www.glassdoor.com/Reviews/The-Home-Depot-Reviews-E655_P1800.htm?sort.sortType=RD&sort.ascending=false"', 'TheHomeDepot7'), 
        #('"https://www.glassdoor.com/Reviews/The-Home-Depot-Reviews-E655_P2100.htm?sort.sortType=RD&sort.ascending=false"', 'TheHomeDepot8'), 
        #('"https://www.glassdoor.com/Reviews/Wells-Fargo-Reviews-E8876_P1.htm?sort.sortType=RD&sort.ascending=false"', 'WellsFargoANDCompany1'), 
        #('"https://www.glassdoor.com/Reviews/Wells-Fargo-Reviews-E8876_P300.htm?sort.sortType=RD&sort.ascending=false"', 'WellsFargoANDCompany2'), 
        #('"https://www.glassdoor.com/Reviews/Wells-Fargo-Reviews-E8876_P600.htm?sort.sortType=RD&sort.ascending=false"', 'WellsFargoANDCompany3'), 
        #('"https://www.glassdoor.com/Reviews/Wells-Fargo-Reviews-E8876_P900.htm?sort.sortType=RD&sort.ascending=false"', 'WellsFargoANDCompany4'), 
        #('"https://www.glassdoor.com/Reviews/Wells-Fargo-Reviews-E8876_P1200.htm?sort.sortType=RD&sort.ascending=false"', 'WellsFargoANDCompany5'), 
        #('"https://www.glassdoor.com/Reviews/Wells-Fargo-Reviews-E8876_P1500.htm?sort.sortType=RD&sort.ascending=false"', 'WellsFargoANDCompany6'), 
        #('"https://www.glassdoor.com/Reviews/Wells-Fargo-Reviews-E8876_P1800.htm?sort.sortType=RD&sort.ascending=false"', 'WellsFargoANDCompany7'), 
        #('"https://www.glassdoor.com/Reviews/Wells-Fargo-Reviews-E8876_P2100.htm?sort.sortType=RD&sort.ascending=false"', 'WellsFargoANDCompany8'), 
        #('"https://www.glassdoor.com/Reviews/Wells-Fargo-Reviews-E8876_P2300.htm?sort.sortType=RD&sort.ascending=false"', 'WellsFargoANDCompany9'), 
        #('"https://www.glassdoor.com/Reviews/The-Coca-Cola-Company-Reviews-E161_P1.htm?sort.sortType=RD&sort.ascending=false"', 'TheCoca-ColaCompany1'), 
        #('"https://www.glassdoor.com/Reviews/The-Coca-Cola-Company-Reviews-E161_P300.htm?sort.sortType=RD&sort.ascending=false"', 'TheCoca-ColaCompany2'), 
        #('"https://www.glassdoor.com/Reviews/Boeing-Reviews-E102_P1.htm?sort.sortType=RD&sort.ascending=false"', 'TheBoeingCompany1'), 
        #('"https://www.glassdoor.com/Reviews/Boeing-Reviews-E102_P300.htm?sort.sortType=RD&sort.ascending=false"', 'TheBoeingCompany2'), 
        #('"https://www.glassdoor.com/Reviews/Boeing-Reviews-E102_P600.htm?sort.sortType=RD&sort.ascending=false"', 'TheBoeingCompany3'), 
        #('"https://www.glassdoor.com/Reviews/Goldman-Sachs-Reviews-E2800_P1.htm?sort.sortType=RD&sort.ascending=false"', 'TheGoldmanSachsGroup1'), 
        #('"https://www.glassdoor.com/Reviews/Goldman-Sachs-Reviews-E2800_P300.htm?sort.sortType=RD&sort.ascending=false"', 'TheGoldmanSachsGroup2'), 
        #('"https://www.glassdoor.com/Reviews/Xerox-Reviews-E747_P1.htm?sort.sortType=RD&sort.ascending=false"', 'XeroxHoldings1'), 
        #('"https://www.glassdoor.com/Reviews/Xerox-Reviews-E747_P300.htm?sort.sortType=RD&sort.ascending=false"', 'XeroxHoldings2'), 
        #('"https://www.glassdoor.com/Reviews/Xerox-Reviews-E747_P600.htm?sort.sortType=RD&sort.ascending=false"', 'XeroxHoldings3'), 
        #('"https://www.glassdoor.com/Reviews/Procter-and-Gamble-Reviews-E544_P1.htm?sort.sortType=RD&sort.ascending=false"', 'TheProcterANDGambleCompany1'), 
        #('"https://www.glassdoor.com/Reviews/Procter-and-Gamble-Reviews-E544_P300.htm?sort.sortType=RD&sort.ascending=false"', 'TheProcterANDGambleCompany2'), 
        #('"https://www.glassdoor.com/Reviews/Procter-and-Gamble-Reviews-E544_P600.htm?sort.sortType=RD&sort.ascending=false"', 'TheProcterANDGambleCompany3'), 
        #('"https://www.glassdoor.com/Reviews/UPS-Reviews-E3012_P1000.htm?sort.sortType=RD&sort.ascending=false"', 'UnitedParcelService2'), 
        #('"https://www.glassdoor.com/Reviews/UPS-Reviews-E3012_P1300.htm?sort.sortType=RD&sort.ascending=false"', 'UnitedParcelService3'), 
        #('"https://www.glassdoor.com/Reviews/Kraft-Heinz-Company-Reviews-E1026712_P1.htm?sort.sortType=RD&sort.ascending=false"', 'TheKraftHeinzCompany'), 
        #('"https://www.glassdoor.com/Reviews/Kroger-Reviews-E386_P1000.htm?sort.sortType=RD&sort.ascending=false"', 'TheKrogerCo2'), 
        #('"https://www.glassdoor.com/Reviews/The-Cheesecake-Factory-Reviews-E2229.htm"', 'TheCheesecakeFactory')]


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
            p2.start() #uncomment to use second process
            # starting process 3
            p3.start() #uncomment to use third process
            # starting process 4
            p4.start() #uncomment to use third process

            
Multi().start()
