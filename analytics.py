class Analytics(object):
    def __init__ (self, transactions):
        self.transactions = transactions

    
     def analyse(self):
         self.alterDates()
         self.processTransactions()

     #Get a datetime object based on the first data and time noticed
     def getBaseDate (self):
         date = self.transactions[0]['created']
         date[date.index("T")] = '-'
         #format: yyyy-mm-ddThh-mm-ss
         tokens = date.split("-")
         datetimeObj = datetime(tokens[0],
                                tokens[1],
                                tokens[2],
                                tokens[3]
                                tokens[4],
                                tokens[5])
                                
     def alterDates (self):
         dateObj = getBaseDate()
         
         #To alter a data, I'll take the start data and time
         #Then I need to increase the time and dat
        
     def processTransactions(self):
         self.alterDates()
