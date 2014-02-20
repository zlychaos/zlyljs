#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Reorder the query based on results and relevance feedback
# Simply call set_order with parameters of current query and the query results( with relevance feedback ) 
# to get best query for next iteration( reordered query )

import urllib2
import base64
import json
import sys
import string
import operator
import re

def set_order(keywords, results):
    matrix = dict()
    for word1 in keywords:
        matrix[word1] = dict()
        for word2 in keywords:
            if word2 != word1:
                matrix[word1][word2] = 0
                for item in results:
                    #print word1.lower()+".{0,17}"+word2.lower()
                    remode = word1.lower()+".{1,5}"+word2.lower()
                    if re.search(remode,item[u'Description'].encode('utf-8').lower()) or re.search(remode,item[u'Title'].encode('utf-8').lower()):
                        #print "Got you!!!!"
                        if item[u'relevant']:
                            matrix[word1][word2] = matrix[word1][word2] + 1
                        else:
                            matrix[word1][word2] = matrix[word1][word2] - 1
    best_query = keywords
    score = 0
    #print keywords
    for word1 in keywords:
        words_list = keywords[:]
        query = [word1]
        words_list.remove(word1)
        curr_word = word1
        while len(query) < len(keywords):
            #print query
            #print words_list
            word_to_add = None
            for word2 in words_list:
                if word2 not in query and ( word_to_add==None or ( matrix[curr_word].has_key(word2) and  matrix[curr_word][word2]>matrix[curr_word][word_to_add] ) ):
                    word_to_add = word2
            #print word_to_add
            query.append(word_to_add)
            words_list.remove(word_to_add)
            curr_word = word_to_add
        the_score = 0
        for i in range(len(query)-1):
            #print i
            the_score = the_score + matrix[query[i]][query[i+1]]
        #print the_score
        if the_score > score:
            best_query = query
            score = the_score
    return best_query



if __name__ =="__main__":
    pass
