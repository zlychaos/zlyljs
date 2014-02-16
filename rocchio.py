#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import operator
import re
import keyword_order

top1=""
top2=""

stop_words = []
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
    coe=0.667
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
    
def rocchio(results, query_list):
    
    global stop_words

    a=1
    b=0.75
    c=-0.25

    dic_q={};
    dic_rel={}
    dic_nonrel={}
    des_list_rel=[]
    des_list_nonrel=[]
    title_list_rel=[]
    title_list_nonrel=[]
    dic_result={}
    list_keys=[]

    stop_words=stop_words_ini[:]
    for word in query_list:
        stop_words.append(word)

    for item in results:
        if item[u'relevant']:
            des_list_rel.append(item[u'Description'])
            title_list_rel.append(item[u'Title'])
        else:
            des_list_nonrel.append(item[u'Description'])
            title_list_nonrel.append(item[u'Title'])

    if len(des_list_rel)!=0:
        b/=len(des_list_rel)
        for l in des_list_rel:   
            store2Hash(l,dic_rel,b)
        for l in title_list_rel:   
            store2Hash(l,dic_rel,2*b)
        
    if len(des_list_nonrel)!=0:
        c/=len(des_list_nonrel)
        for l in des_list_nonrel:   
            store2Hash(l,dic_nonrel,c)
        for l in title_list_nonrel:   
            store2Hash(l,dic_nonrel,2*c)
            
    #store2Hash(line,dic_q,a)
    #list_keys=list(set(dic_q.keys()+dic_rel.keys()+dic_nonrel.keys()))
    
    list_keys=list(set(dic_rel.keys()+dic_nonrel.keys()))
    for key in list_keys:
        dic_result[key]=dic_rel.get(key,0)+dic_nonrel.get(key,0)
    #print dic_result

    addQuery(dic_result)
    #print "\n--------------------"
    if top1!="":
        #print "\ntop1: "+top1
        query_list.append(top1)
    if top2!="":
        #print "\ntop2: "+top2
        query_list.append(top2)
    #print "\n--------------------\n"
    best_query = keyword_order.set_order(query_list, results)
    #print "suggested best query"
    #print best_queriy
    return best_query

