import requests
import json

# REQUEST functions
def get_req(tok, url):
    h = getHeader(tok)
    r = requests.get(url, headers=h)
    if (r.status_code != 200):
        return {}
    else:
        return json.loads(r.text)

def put_req(tok, url, d):
    h = getHeader(tok)
    r = requests.put(url, headers=h, data=json.dumps(d))
    if (r.status_code != 200):
        return {}
    else:
        return json.loads(r.text)

def post_req (tok, url, d):
    h = getHeader(tok)
    r = reuests.post(url, headers=h, data=json.dumps(d))
    if status_code != 200:
        return []
    else:
        return json.loads(r.text)

def delete_req(tok, url):
    h = getHeader(tok)
    r = requests.delete(url, headers=h)
    return {}

def getHeader(tok):
    return {"Accept": "application/json","Content-Type": "application/json","Authorization": "Bearer "+tok}