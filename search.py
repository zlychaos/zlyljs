#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import base64
import json
import sys
import string
import re
from rocchio import rocchio

#Provide your account key here
accountKey = 'wzQz8YO7jqhGSx1UpWwYRiVwlb3KuGOxavRpambmZY8'
accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
headers = {'Authorization': 'Basic ' + accountKeyEnc}

#messages
search_promt = "Please type the search key words: "
target_promt = "Please input the target( 0.1 ~ 1 ): "
relevant_promt = "Is this result relevant? [Y/N]"
invalid_yes_no = "Please respond with 'yes' or 'no'"

def getResult(query):
    bingUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27' + query + '&$top=10&$format=json'
    print "The request url: " + bingUrl
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
    print "Total number of results: " + str(len(result))
    for item in result:
        i = i+1
        print "--------------------"
        print "result " + str(i)
        print "--------------------"
        print "Title:  "+item[u'Title']
        print "Description:"
        print item[u'Description'].encode('utf-8')
        print item[u'Url']
        item[u'relevant'] = bool_promt(relevant_promt)
        if item[u'relevant']:
            rel = rel + 1
        
    return rel

def getQuery():
    print search_promt
    line = sys.stdin.readline()
    target = float(raw_input(target_promt))
    words = line.split()
    query = ''
    query_list = []
    for word in words:
        query = query + word + '%27'
        query_list.append(word)
    return line, query, query_list, target

if __name__ =="__main__":
    line, query, query_list, target = getQuery()
    original_query = line
    round = 0
    while True:
        flag = True
        result = getResult(query)
        rel = display(result)
        round = round + 1

        if len(result) < 10:
            print "# of results less than 10"
        elif rel >= target*len(result):
            print "succeed!"
            print '<<<<<<<<<<<<<Query Feedback>>>>>>>>>>>>>>>'
            print "Original Query : " + line
            print "target : " + str(target)
            print "precision achieved : " + str( float(rel)/len(result) )
            print "Total rounds before success : " + str(round)
            print '<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>'

        else:
            flag = False
            best_query = rocchio(result, query_list)
            print '=========================================='
            print 'FEEDBACK SUMMARY'
            print "This Query : "
            print query_list
            print 'target : ' + str(target)
            print 'precision : ' + str( float(rel)/len(result) ) + " | still below the target"
            print "Next Query : "
            print best_query
            print '=========================================='
        
        if flag:
            line, query, query_list, target = getQuery()
            original_query = line
            round = 0
        else:
            query_list = best_query
            query = ''
            for word in query_list:
                query = query + word + '%27'

