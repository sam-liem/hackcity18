import httplib

def printText(txt):
    lines = txt.split('\n')
    for line in lines:
        print (line.strip())

httpServ = httplib.HTTPConnection("http://0.0.0.0:5000/", 80)
httpServ.connect()

quote = "test"
httpServ.request('POST', '/cgi_form.cgi', 'name=Brad&quote=%s' % quote)

response = httpServ.getresponse()
if response.status == httplib.OK:
    print ("Output from CGI request")
    printText (response.read())

httpServ.close()
