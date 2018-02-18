from datetime import datetime
import random

class Analytics(object):
    def __init__ (self, transactions):
        self.transactions = transactions

    
    def analyse(self):
         self.processTransactions()

    #Get a datetime object based on the first data and time noticed
    def getBaseDate (self):
        date = self.transactions[0]['created']
        date = date[0:date.index(".")]
        date = list(date)
        date[date.index("T")] = '-'
        for i in range(2):
            date[date.index(":")] = '-'
        date = ''.join(date)
        #format: yyyy-mm-ddThh-mm-ss
        tokens = date.split("-")
        datetimeObj = datetime(int(tokens[0]),
                               int(tokens[1]),
                               int(tokens[2]),
                               int(tokens[3]),
                               int(tokens[4]),
                               int(tokens[5]))

        return datetimeObj
                                
    def alterDates (self):
        dateObj = self.getBaseDate()
        self.transactions[0]['created'] = dateObj
      
        for trans in range(1,len(self.transactions)):
            dateObj = self.transactions[trans-1]['created']
            seconds = dateObj.timestamp()
            rand = self.getRandomTime()
            self.transactions[trans]['created'] = datetime.fromtimestamp(rand+seconds)
        

    
    def getRandomTime(self):
        fiveMinutes = 300
        twoDays = 172800
        fiveDays = 432000
        tenDays = 864000
        
        #90% chance picking between 300 seconds and five days
        num = random.randint(1,100)
        if num < 80 :
            return  random.randint (fiveMinutes, twoDays)

        elif num < 95:
            return random.randint (twoDays, fiveDays)

        else:
            return random.randint (fiveDays, tenDays)
        
    def processTransactions(self):
        self.alterDates()


   
        
