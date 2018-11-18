
# coding: utf-8

# ## Extract User-Problem data
# 
# This is the second notebook which works on user data.
# We get the problem id's of all problems solved by the user.

# In[70]:



import requests
import json


# In[76]:


s=requests.Session()

# Loading user data
with open('../data/user_filtered.json') as f:
    userList=json.load(f)

# Loading problem data    
with open('../data/problems.json') as f:
    problemList=json.load(f)


# In[51]:


'''
This function will retrieve problems given the user handle. 
This function uses api calls which can fail sometimes. 
Hence it is wrapped in a try except block. 
'''

def getProblems(s,handle):
    submissions=json.loads(s.get("http://codeforces.com/api/user.status?handle="+handle+"&from=1&count=100000").text)
    if (submissions["status"]!="OK"):
        raise Exception("FAIL")
    else:
        submissions=submissions["result"]
    l=set()
    for submission in submissions:
        if submission["verdict"]=='OK':
            try:
                l.add(str(submission["problem"]["contestId"])+submission["problem"]["index"])
            except:
                pass
    return list(l)


# In[74]:


print(getProblems(s,"toxic_hack")) # Sanity check on data


# In[75]:


# Get List of problems solved
# This function needs to be run until all user's problems pass

userCount=0
s=requests.Session()
for org in userList:
    for user in userList[org]:
        userCount+=1
        if "problemsSolved" not in user:
            try:
                user["problemsSolved"]= getProblems(s,user["handle"])
                print(user["handle"],userCount)
            except:
                print("FAIL",user["handle"])
            


# In[6]:


# Store the final users file
with open('../data/user_filtered_problems.json', 'w') as fp:
    json.dump(userList, fp)

