#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import base64
import json
import sys
import string
import operator
import re

#Provide your account key here
accountKey = 'wzQz8YO7jqhGSx1UpWwYRiVwlb3KuGOxavRpambmZY8'
accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
headers = {'Authorization': 'Basic ' + accountKeyEnc}
top1=""
top2=""

#messages
search_promt = "Please type the search key words: "
target_promt = "Please input the target( 0.1 ~ 1 ): "
relevant_promt = "Is this result relevant? [Y/n]"
invalid_yes_no = "Please respond with 'yes' or 'no'"

stop_words_ini =["a","about","above","after","again","against","all","am","an","and",
             "any","are","aren't","as","at","be","because","been","before","being",
             "below","between","both","but","by","can't","cannot","could","couldn't",
             "did","didn't","do","does","doesn't","doing","don't","down","during",
             "each","few","for","from","further","had","hadn't","has","hasn't","have",
             "haven't","having","he","he'd","he'll","he's","her","here","here's","hers",
             "herself","him","himself","his","how","how's","i","i'd","i'll","i'm","i've",
             "if","in","into","is","isn't","it","it's","its","itself","let's","me","more",
             "most","mustn't","my","myself","no","nor","not","of","off","on","once",
             "only","or","other","ought","our","ours ","ourselves","out","over","own",
             "same","shan't","she","she'd","she'll","she's","should","shouldn't","so",
             "some","such","than","that","that's","the","their","theirs","them",
             "themselves","then","there","there's","these","they","they'd","they'll",
             "they're","they've","this","those","through","to","too","under","until",
             "up","very","was","wasn't","we","we'd","we'll","we're","we've","were",
             "weren't","what","what's","when","when's","where","where's","which","while",
             "who","who's","whom","why","why's","with","won't","would","wouldn't","you",
             "you'd","you'll","you're","you've","your","yours","yourself","yourselves"]
stop_words=[]
dic_q={};
dic_rel={}
dic_nonrel={}
des_list_rel=[]
des_list_nonrel=[]
dic_result={}
list_keys=[]

a=1
b=0.75
c=-0.25

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
        print item[u'Description'].encode('utf-8')
        print item[u'Url']
        item[u'relevant'] = bool_promt(relevant_promt)
        if item[u'relevant']:
            rel = rel + 1
            des_list_rel.append(item[u'Description'])
        else:
            des_list_nonrel.append(item[u'Description'])
        
    return rel



def store2Hash(str, dic, weight):
    term_list=re.split("[^a-zA-Z]",str)
    #delset = string.punctuation+"\n"
    for term in term_list:
        term=term.lower()
        if term!="":
            if dic.has_key(term):
                dic[term]+=weight
            else:
                dic[term]=weight
                
def addQuery(dic_result):
    global top1
    global top2
    coe=0.5
    top1=""
    top2=""
    value_top1 =0
    while len(dic_result)!=0:
        top1 = max(dic_result.iteritems(), key=operator.itemgetter(1))[0]
        value_top1 = dic_result[top1]
        del dic_result[top1]
        if top1 not in stop_words:
            break
    if len(dic_result)==0:
        top1=""
    else:
        value_top2=value_top1
        while(len(dic_result)!=0 and value_top2 >= value_top1 * coe):
            top2 = max(dic_result.iteritems(), key=operator.itemgetter(1))[0]
            value_top2 = dic_result[top2]
            del dic_result[top2]
            if top2 not in stop_words:
                break
        if len(dic_result)==0 or value_top2 <value_top1*coe:
            top2=""
    
                

if __name__ =="__main__":
    print search_promt
    line = sys.stdin.readline()
    target = float(raw_input(target_promt))

    while line:
        dic_q={};
        dic_rel={}
        dic_nonrel={}
        des_list_rel=[]
        des_list_nonrel=[]
        dic_result={}
        list_keys=[]
        words = line.split()
        query = ''
        stop_words=stop_words_ini[:]
        for word in words:
            query = query + word + '%27'
            stop_words.append(word)
        result = getResult(query)
        rel = display(result)
        if rel >= target*10:
            print "succeed!"
        
        if len(des_list_rel)!=0:
            b/=len(des_list_rel)
        for l in des_list_rel:   
            store2Hash(l,dic_rel,b)
        if len(des_list_nonrel)!=0:
            c/=len(des_list_nonrel)
        for l in des_list_nonrel:   
            store2Hash(l,dic_nonrel,c)
            
        store2Hash(line,dic_q,a)
        list_keys=list(set(dic_q.keys()+dic_rel.keys()+dic_nonrel.keys()))
        for key in list_keys:
            dic_result[key]=dic_q.get(key,0)+dic_rel.get(key,0)+dic_nonrel.get(key,0)
        print dic_result

        addQuery(dic_result)
        print "\n--------------------"
        if top1!="":
            print "\ntop1: "+top1
        if top2!="":
            print "\ntop2: "+top2
        print "\n--------------------\n"
    
        print search_promt
        line=sys.stdin.readline()
        target = float(raw_input(target_promt))
