import urllib2
import base64
import json

bingUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27gates%27&$top=10&$format=json'
#Provide your account key here
accountKey = 'wzQz8YO7jqhGSx1UpWwYRiVwlb3KuGOxavRpambmZY8'

accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
headers = {'Authorization': 'Basic ' + accountKeyEnc}
req = urllib2.Request(bingUrl, headers = headers)
response = urllib2.urlopen(req)
content = response.read()
#content contains the xml/json response from Bing. 
#print content
json_content = json.loads(content)
result = json_content["d"]["results"]
i = 0
for item in result:
	i = i+1
	print "--------------------"
	print i
	print "--------------------"
	
	print item
  