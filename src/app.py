from starling import account

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response
from flask import send_from_directory

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])

def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request received:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    
    print("Response sent:")
    print(res)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):

    acc = account("1rxRXmg4lNh5rphevZwWNG1CYbTwRC9juFJe3ZGEenYo1wuStaXh2UZgMpNs9Pta")

    action = req.get("result").get("action")
    data = {}

    if action == "getBalance":
        data = acc.returnBalance()

    elif action == "getSortCode":
        data = acc.returnAccSort()

    elif action == "getAccountNumber":
        data = acc.returnAccNumber()

    elif action == "getCurrency":
        data = acc.returnAccCurr()

    elif action == "getAllTransactions":
        data = acc.returnAllTransactions()
    
    elif action == "addSavingsGoal":
        data = acc.addSavingGoal(req)

    elif action == "getAllSavingGoals":
        data = acc.returnAllSavingGoals()

    elif action == "deleteSavingGoal":
        # temp
        req['goalName'] = "Trip to Paris"
        data = acc.deleteSavingGoal(req['goalName'])

    elif action == "getSavingsGoal":
        # temp
        req['goalName'] = "Trip to Paris"
        data = acc.returnSavingGoal(req['goalName'])

    elif action == "getAllPaymentSchedules":
        data = acc.returnAllPaymentSchedules()

    elif action == "csv":
        url = request.url_root + "downloadCSV"
        data = {"speech":url}

    else:
        return {}

    return makeWebhookResult(data)

def makeWebhookResult(data):

    if data == {}:
        return {}
        
    speech = data['speech']

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "starlingBotAPI"
    }

@app.route('/downloadCSV', methods=['GET'])
def downloadCSV():
    acc = account("wzebJBlstyLeJEi6pTYiC0XUf2DL5W77pi9xKpM8UkykLXVgsipLWYe1p37gRxZX")
    data = acc.setSpreadsheet()

    return send_from_directory(os.getcwd()+'/tmp', "bankData.csv", as_attachment=True)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
