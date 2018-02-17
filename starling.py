class StarlingAccount(object):
    # Flask app should start in global layout
    app = Flask(__name__)
    @app.route('/webhook', methods=['POST'])
    #Step one, user needs to login

    def __init__ (self):
        self.loggin = False

    def testRedirection(self):
        url = "https://oauth.starlingbank.com/?client_id=TJ71XnestPKk1kYi4aEM&response_type=json&state=$state&redirect_uri=$https://google.com"
        
    def testRedirection2(self):
        #What i did
        url1 = "https://oauth.starlingbank.com/?client_id=TJ71XnestPKk1kYi4aEM&response_type=code&state=$state&redirect_uri=$https://google.com"
        url2 = "https://oauth.starlingbank.com/?client_id=ecb8ffbf-2c5b-4e2b-8635-0a75d3b6e485&response_type=code&state=$state&redirect_uri=$https://google.com"
        foo = urlopen(url)
        print(urlopen(url).read())