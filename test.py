import urllib2
import base64
import json
import sys

#Provide your account key here
accountKey = '----Your-Bing-Search-Account-Key-----'

accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
headers = {'Authorization': 'Basic ' + accountKeyEnc}

def getResult(query):
    bingUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27' + query + '&$top=10&$format=json'
    req = urllib2.Request(bingUrl, headers = headers)
    response = urllib2.urlopen(req)
    content = response.read()
    #content contains the xml/json response from Bing. 
    #print content
    json_content = json.loads(content)
    result = json_content["d"]["results"]
    return result

def display(result):
    i = 0
    for item in result:
        i = i+1
        print "--------------------"
        print i
        print "--------------------"
        print "Title:  "+item[u'Title']
        print "Description:"
        print item[u'Description']
        print item[u'Url']


if __name__ =="__main__":
    line = sys.stdin.readline()
    while line:
        words = line.split()
        query = ''
        for word in words:
            query = query + word + '%27'
        result = getResult(query)
        display(result)
        line = sys.stdin.readline()

