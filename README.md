ADB Project 1
============

Liyuan Zheng ( lz2375 )
Jingsi Li ( jl4165 )

File List
---------
search.py
keyword_order.py
rocchio.py
README
akefile

How to Run the Program
----------------------
Simply type 'make' in the directory to run the program.
The program will prompt user to input queries and targets.

Internal Design
---------------
The program consists of three python file, search.py, rocchio.py and keyword_order.py. The main function is in search.py and what it does is to promt user to enter queries and targets, and to give a relevance feedback on results returned by calling Bing API. It will automatically iterate until the target is reached or some particular circumstances( number of results returned is less than 10, etc ) occur. It calls function rocchio in rocchio.py where modified rocchio algorithm is implemented. 

What is implemented in rocchio.py will be talked about in the next section. Dictionary of python is used to represent the vectors in rocchio algorithm. The original rocchio algorithm does not include optimization on order of terms in a query. So we developed a straightforward method for that in keyword_order.py, which will be introduced in 4(c). 

The results of queries have a consistant structure. We load the results from json object returned by Bing. Every result of a query will be assigned a 'Relevant' field when user provides feedback. With the consistancy, at each step of the processing ( adding terms using rocchio and reordering ), the program can recognize and use the results and the feedback. 

Query Modification Method
-------------------------        
We mainly referred to the Rocchio algorithm for relevance feedback to implement the query modification method. With this algorithm, we can find a query vector, denoted as q, that maximazes similarity with relevant documents while minimizing similarity with nonrelevant documents. 
Our program only analyzes the title and description of each result. Hashtables are created to store words from relevant results  (named rel_hashtable) and words from nonrelevant results  (named nonrel_hashtable). 

For each result, the program asks the user whether it is relevant. If it is, then all words in the title and description of this result are stored into the rel_hashtable with the specific weight. generally speaking, terms in titles are more important than those in the descriptions, thus we give the terms in descriptions weight b and those in titles weight 2b. Similarly, if a result is not relevant, words in it are stored into the nonrel_hashtable with weight of -2c and -c for words in title and description respectively. Then we combine the (key value) pairs of those two hashtables together to get our q. Two words with the highest value and second highest value are selected from q. If the second highest value is less than 2/3 of the highest value, only the word with the highest value will be returned, otherwise both words will be returned. The returned word(s) will appear in the expanded query.

We have done several enhancements to increace the quality of the expanded query.

* Title and desctiption have different weights.
This has already been introduced above. The reasoning is , in short, that titles can represent articles better. 
* Stop words are removed from results.        
We listed as many as 174 stop words which will not be considered as words of expand queries. By dropping those less meaningful words, number of iteration to achieve the target for queries become smaller.
* Order of terms in the query is taken into consideration.
After determining set of terms included in expansion query using modified rocchio algorithms mentioned above, we assign a weight to every permutation of two terms in the expanded query, which shows how frequently two terms appear in relevant documents very close to each other with certain order, and how infrequently that happens in unrelevant documents. And then we return the permutation of all terms that maximize the sum of weights of every two adjacent terms, which we suggest as best query for next iteration.


Bing Search Account Key
-----------------------
wzQz8YO7jqhGSx1UpWwYRiVwlb3KuGOxavRpambmZY8
