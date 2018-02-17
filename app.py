import starling

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

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

    action = req.get("result").get("action")

    if action == "getBalance":
        # return getBalance(req)
        return {}

    elif action == "getSavingsGoals":
        # return getSavingsGoals(req)
        return {}

    else:
        return {}

def makeWebhookResult(data):

    if data == {}:
        return {}
        
    speech = data.speech

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "starlingBotAPI"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

app = StarlingAccount()

app.app.run(debug=False, port=port, host='0.0.0.0')
