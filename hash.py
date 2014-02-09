'''
Created on Feb 8, 2014

@author: Jocelyn, zlychaos
'''
import string
import operator
import re

'''
def store2Hash(s, dic, weight):
    term_list=re.split("[^a-zA-Z]",s)
    #delset = string.punctuation+"\n"
    for i in range(len(term_list)):
        term_list[i]=term_list[i].lower()#.translate(None,delset)
        if term_list[i]!="":
            if dic.has_key(term_list[i]):
                dic[term_list[i]]+=weight
            else:
                dic[term_list[i]]=weight
'''

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

if __name__ =="__main__":
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
    
    q0="apple service media solutions"
    
    des1="""Apple Inc. (Apple) designs, manufactures and markets mobile 
    communication and media devices, personal computers, and portable
     digital music players, and sells a variety of related software, 
     services, peripherals, networking solutions, and third-party digital
      content and applications. The Company products and services 
      include iPhone, iPad, Mac, iPod, Apple TV, a portfolio of consumer
       and professional software applications, the iOS and OS X operating
        systems, iCloud, and a variety of accessory, service and support 
        offerings."""
    des2="""Apple has removed the bitcoin app Blockchain from its iOS App Store,
         underscoring the belief that the company has an unstated policy against 
         such services."""
    
    des3="""Apple has previously said that it intends to spend $60 billion on repurchasing
     its own shares. This reduces the number of shares in circulation, providing a boost
      to remaining investors as their shares rise in value."""
      
    des4="""The apple is the pomaceous fruit of the apple tree, species Malus 
        domestica in the rose family (Rosaceae). It is one of the most widely 
        cultivated tree fruits, and the most widely known of the many members 
        of genus Malus that are used by humans. Apples grow on small, deciduous trees. 
        The tree originated in Central Asia, where its wild ancestor, Malus sieversii, 
        is still found today."""
    des5="""Apples are obtained from the medium-sized tree belonging to the Rosaceae
         family. The apple tree is originated in the mineral-rich mountain ranges of
          Kazakhstan, and now being cultivated in many parts of the world."""
    
    des6="""The apple is the most diverse food plant in the world. According to food 
        journalist and apple expert Rowan Jacobsen, there used to be 16,000 types of
         apples in the U.S. alone. A current review of USDA data puts the variety 
         diversity at 2,450 types jingsi."""
    des_list_rel.append(des1)
    des_list_rel.append(des2)
    des_list_rel.append(des3)
    des_list_nonrel.append(des4)
    des_list_nonrel.append(des5)
    des_list_nonrel.append(des6)
    
    b/=len(des_list_rel)
    print "b is "+str(b)+"\n"
    for l in des_list_rel:   
        store2Hash(l,dic_rel,b)
   
    c/=len(des_list_nonrel)
    print "c is "+str(c)+"\n"
    for l in des_list_nonrel:   
        store2Hash(l,dic_nonrel,c)
        
    store2Hash(q0,dic_q,a)
    
    print dic_q
    print dic_rel
    print dic_nonrel
    
    list_keys=list(set(dic_q.keys()+dic_rel.keys()+dic_nonrel.keys()))

    for key in list_keys:
        dic_result[key]=dic_q.get(key,0)+dic_rel.get(key,0)+dic_nonrel.get(key,0)
    
    
    print dic_result
    
    top1 = max(dic_result.iteritems(), key=operator.itemgetter(1))[0]
    del dic_result[top1]
    top2 = max(dic_result.iteritems(), key=operator.itemgetter(1))[0]
    print top1 +", "+top2




    
