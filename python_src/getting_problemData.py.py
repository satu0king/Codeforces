
# coding: utf-8

# ## Extract Problem data
# 
# This is the first notebook which works on problem data.
# We use the raw problem data and augment some features which we get from scraping

# In[6]:


import json
import requests
from bs4 import BeautifulSoup


# In[7]:


'''

reading data for all the problems that is present in codeforces website. problemset.json contains data for each
problem with the following as keys:

-> contestId
-> index
-> name
-> type
-> tags

'''
with open('../data/problemset.json') as f:
    data = json.load(f)


# In[9]:


print(len(data["result"]['problems']))


# In[11]:


'''

now we are identifying each problem uniquely based on the string which is concatination of contestId + index, 
final_data is a dictionary containing all the information of the question with the key being the above mentioned
unique id.
'''
final_data = {}
for j, i in enumerate(data['result']['problems']):
    prob_id = str(i['contestId']) + str(i['index'])
    problem_data = {}
    problem_data['name'] = i['name']
    problem_data['tags'] = i['tags']
    if(prob_id not in final_data):
        final_data[prob_id] = {}
    final_data[prob_id] = problem_data


# In[ ]:


'''

since the diffuculy of the problem is not given in the api we scrape them from codeforces website.

'''
s = requests.Session()
for i in range(1, 48):
    r = s.get('http://codeforces.com/problemset/page/' + str(i))
    soup = BeautifulSoup(r.text)
    for j in soup.find_all("div", {"class" : "datatable"}):
        for k in j.find_all("tr")[1:]:
            try:
                name = k.find_all("td", {"class" : "id"})[0].text.strip()
                difficulty = k.find_all("span", {"class" : "ProblemRating"})[0].text.strip()
            except:
                continue
            final_data[name]['difficulty'] = difficulty


# In[15]:


'''
for the problems which does not have the difficulty we fill them with null values
'''
for i in final_data:
    if('difficulty' not in final_data[i]):
        final_data[i]['difficulty'] = None
        
'''
now the final_data is stored in the file problems.josn.
'''
with open('../data/problems.json', 'w') as fp:
    json.dump(final_data, fp)

