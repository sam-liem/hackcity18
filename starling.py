import requests

class account:
    def __init__ (self,token):
        self.loggin = False
        self.token = token
        
    # def testRedirection2(self):
    #     url1 = "https://oauth.starlingbank.com/?client_id="+self.client_secret+"&response_type=code&state=$state&redirect_uri=$https://google.com"
    #     url2 = "https://oauth.starlingbank.com/?client_id=ecb8ffbf-2c5b-4e2b-8635-0a75d3b6e485&response_type=code&state=$state&redirect_uri=$https://google.com"
    #     foo = urlopen(url)
    #     print(urlopen(url).read())

    def getBalance(self):
        headers = {"Accept": "application/json","Content-Type": "application/json","Authorization": "Bearer "+self.token}
        req = requests.get('https://api-sandbox.starlingbank.com/api/v1/accounts/balance', headers=headers)
        print(req)

acc = account("1rxRXmg4lNh5rphevZwWNG1CYbTwRC9juFJe3ZGEenYo1wuStaXh2UZgMpNs9Pta")
acc.getBalance()
