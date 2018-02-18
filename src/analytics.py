
from datetime import datetime
import random
import operator


class Accumulation(object):
    def __init__(self, day, cumulative_total, balance, dateRef):
        self.day_num = day
        self.cumulative_total = cumulative_total
        self.balance = balance
        self.dateRef = dateRef
        
class Analytics(object):
    def __init__ (self, transactions):
         self.transactions = transactions
         self.outbounds = []
         self.inbounds = []
         self.outbounds_cumulative = []
         self.inbounds_cumulative = []
         self.processed = False

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
        random.seed(1)
        dateObj = self.getBaseDate()
        self.transactions[0]['created'] = dateObj
      
        for trans in range(1,len(self.transactions)):
            dateObj = self.transactions[trans-1]['created']
            seconds = dateObj.timestamp()
            rand = self.getRandomTime()
            self.transactions[trans]['created'] = datetime.fromtimestamp(rand+seconds)
            if self.transactions[trans]['direction'] == "OUTBOUND":
                self.outbounds += [self.transactions[trans]['direction']]

            else:
                self.inbounds += [self.transactions[trans]['direction']]
        """
        for trans in self.transactions:
            print ("Date: ", trans['created']," type: ", trans['direction'], "amount: ", trans['amount'])
        """
        
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

    def process (self):
        self.analyse()

    def interpolate (self, inbound_outbounds, day):
        for trans in range(1,len(inbound_outbounds)):
            prev = inbound_outbounds[trans-1]
            curr = inbound_outbounds[trans]

            if prev.day_num == day or curr.day_num == day:
                return prev.cumulative_total

            if not (prev.day_num < day and day < curr.day_num):
                continue

            dayDiff = curr.day_num - prev.day_num
            frequencyDiff = curr.cumulative_total - prev.cumulative_total

            frequencyPerWidth = frequencyDiff/dayDiff
            freqWidth = day - prev.day_num
            return prev.cumulative_total + frequencyPerWidth*freqWidth

        return None


    def getTotalInbound (self, day):
        return (self.interpolate(self.inbounds_cumulative, self.inbounds_cumulative[-1].day_num-1)-
               self.interpolate (self.inbounds_cumulative, self.inbounds_cumulative[-1].day_num-day))

    def getTotalOutbound (self, days):
        return (self.interpolate(self.outbunds_cumulative, self.outbounds_cumulative[-1].day_num - 1) -
                self.interpolate(self.outbounds_cumulative, self.bounds_cumulative[-1].day_num - day))

    def getAverage (self, inbound_outbound, day_inverval):
        #Gets average amount of money in total every day_interval days
        currentDay = inbound_outbound[-1].day_num

        avg = 0
        count = 0
        while currentDay >= inbound_outbound[0].day_num:
            currentAmount = self.interpolate(inbound_outbound,currentDay)

            if currentDay-day_inverval > inbound_outbound[0].day_num:
                if day_inverval == 1:
                    smallerAmount = self.interpolate(inbound_outbound,currentDay-day_inverval)
                else:
                    smallerAmount = self.interpolate(inbound_outbound,currentDay-day_inverval+1)

            else:
                if day_inverval == 1:
                    smallerAmount = 0

                else:
                    break

            avg += (currentAmount-smallerAmount)
            count += 1

            currentDay -= 1

        return avg/count

    def getAverageInbound (self, dayInterval):
        return self.getAverage(self.inbounds_cumulative, dayInterval)

    def getAverageOutbound (self, dayInterval):
        return self.getAverage(self.outbounds_cumulative, dayInterval)

    def getDayDifference (self, d1, d2):
        diff = (d1 - d2).days

        if diff == 0:
            return 1

        else:
            return diff

    def analyse(self):
        self.alterDates()
        day = 0
        inboundTotal = 0
        outboundTotal = 0
        mostRecent = None
        #I get the cumulative inbound and outbounds
        #The interval will be one day
        for trans in range(len(self.transactions)):
            balance = self.transactions[trans]['balance']
            currDate = self.transactions[trans]['created']
            cash_diff = self.transactions[trans]['amount']

            if self.transactions[trans]['direction'] == "OUTBOUND":
                cash_diff *= -1
                inbound_outbound = self.outbounds_cumulative
                outboundTotal += cash_diff
                total = outboundTotal

            else:
                inbound_outbound = self.inbounds_cumulative
                inboundTotal += cash_diff
                total = inboundTotal

            if inbound_outbound == []:
                if mostRecent != None:
                    dayDiff = self.getDayDifference(currDate, mostRecent['created'])
                    day += dayDiff
                inbound_outbound += [Accumulation(day,total,balance,currDate)]
            else:
                prev = inbound_outbound[-1].dateRef
                if (currDate.year == prev.year and
                    currDate.month == prev.month and
                    currDate.day == prev.day):
                    inbound_outbound[-1].cumulative_total = total
                    inbound_outbound[-1].balance = balance

                else:
                    dayDiff = self.getDayDifference (currDate, mostRecent['created'])
                    day += dayDiff
                    inbound_outbound += [Accumulation(day, total, balance, currDate)]
            mostRecent = self.transactions[trans]


        """
        print ("Getting inbounds accumulation: ")
        for trans in self.inbounds_cumulative:
            print ("Day: " , trans.day_num , " total: ", trans.cumulative_total)


        print ("Getting outbounds accumulation: ")
        for trans in self.outbounds_cumulative:
            print("Day: ", trans.day_num, " total: ", trans.cumulative_total)

        """



    def highestExpense(self, transactions):
        transactions = transactions['_embedded']['transactions']

        # get most recent month's transactions?
        narrativeCostTable = {}
        for transaction in transactions:
            if (transaction['direction'] == "OUTBOUND") and (transaction['narrative'] != "External Payment") and (transaction['narrative'] != "Mastercard"):
                if (transaction['narrative'] in narrativeCostTable):
                    narrativeCostTable[transaction['narrative']] += int(transaction['amount'])
                else:
                    narrativeCostTable[transaction['narrative']] = int(transaction['amount'])

        narrativeCostTable = sorted(narrativeCostTable.items(), key=operator.itemgetter(1))

        name, spent = narrativeCostTable[0]
        speech = "You spent " + str(spent * -1) + " on " + name + ". Consider switching to cheaper alternatives."


