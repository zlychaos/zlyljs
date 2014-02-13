import urllib2
import base64
import json
import sys

#Provide your account key here
accountKey = 'wzQz8YO7jqhGSx1UpWwYRiVwlb3KuGOxavRpambmZY8'
accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
headers = {'Authorization': 'Basic ' + accountKeyEnc}

#messages
search_promt = "Please type the search key words: "
target_promt = "Please input the target( 0.1 ~ 1 ): "
relevant_promt = "Is this result relevant? [Y/n]"
invalid_yes_no = "Please respond with 'yes' or 'no'"

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

def bool_promt(question):
    print question
    yes = set(['yes','y','Y'])
    no = set(['no','n','N'])
    
    while True:
        choice = raw_input().lower()
        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            print invalid_yes_no

def display(result):
    i = 0
    rel = 0
    for item in result:
        i = i+1
        print "--------------------"
        print i
        print "--------------------"
        print "Title:  "+item[u'Title']
        print "Description:"
        print item[u'Description']
        print item[u'Url']
        item[u'relevant'] = bool_promt(relevant_promt)
        if item[u'relevant']:
            rel = rel + 1
    return rel

if __name__ =="__main__":
    print search_promt
    line = sys.stdin.readline()
    target = float(raw_input(target_promt))

    while line:
        words = line.split()
        query = ''
        for word in words:
            query = query + word + '%27'
        result = getResult(query)
        rel = display(result)
        if rel >= target*10:
            print "succeed!"
        print search_promt
        line = sys.stdin.readline()
        target = float(raw_input(target_promt))
