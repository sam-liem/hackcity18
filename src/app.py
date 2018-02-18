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

@app.route('/dashboard')
def dashboard():

    action = request.args.get('action')

    res = dashboard_processRequest(action)
    res = json.dumps(res, indent=4)
    
    print("Response sent:")
    print(res)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def dashboard_processRequest(action):

    acc = account("1rxRXmg4lNh5rphevZwWNG1CYbTwRC9juFJe3ZGEenYo1wuStaXh2UZgMpNs9Pta")

    if action == "getAllTransactions":
        return acc.getAllTransactions()

    if action == "getUserInfo":
        return acc.getUserInfo()


@app.route('/dialogFlow', methods=['POST'])
def dialogFlow():
    req = request.get_json(silent=True, force=True)

    print("Request received:")
    print(json.dumps(req, indent=4))

    res = dialogFlow_processRequest(req)

    res = json.dumps(res, indent=4)
    
    print("Response sent:")
    print(res)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def dialogFlow_processRequest(req):

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
    
    elif action == "getRecentTransaction":
        data = acc.returnRecentTransaction()

    elif action == "addSavingsGoal":
        goalName = req.get("result").get("parameters").get("goalName")
        goalAmount = req.get("result").get("parameters").get("goalAmount")
        data = acc.addSavingsGoal(goalName, goalAmount)

    elif action == "getAllSavingsGoals":
        data = acc.returnAllSavingsGoals()

    elif action == "deleteSavingsGoal":
        goalName = req.get("result").get("parameters").get("goalName")
        data = acc.deleteSavingsGoal(goalName)

    elif action == "getSavingsGoal":
        goalName = req.get("result").get("parameters").get("goalName")
        data = acc.returnSavingsGoal(goalName)

    elif action == "getAllPaymentSchedules":
        data = acc.returnAllPaymentSchedules()

    elif action == "csv":
        url = request.url_root + "downloadCSV"
        data = {"speech":url}

    elif action == "transfer":
        contactName = req.get("result").get("parameters").get("contactName")
        transactionAmount = req.get("result").get("parameters").get("transactionAmount")
        transactionReference = req.get("result").get("parameters").get("transactionReference")
        # data = acc.transfer(contactName,transactionAmount,transactionReference)
        # can't get good uuid in sandbox
        data = {"speech":"Transfer successful."}
    else:
        return {}

    return dialogFlow_makeWebhookResult(data)

def dialogFlow_makeWebhookResult(data):

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
