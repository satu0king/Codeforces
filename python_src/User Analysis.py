
# coding: utf-8

# ## Extract User data
# 
# This is the first notebook which works on user data.
# In this notebook we do analysis of raw user data and filter based on country and organization.
# 

# In[23]:


import json
import requests


# In[24]:


# Loading raw user data
with open('../data/users.json') as f:
    data=json.load(f)


# In[25]:


print(len(data["result"])) # Total number of users (158K users)


# In[26]:


print(data["result"][0]) # Checking user 1 (tourist)


# In[27]:


# Filtering only Indian users

indianUsers=[]
for user in data["result"]:
    if "country" in user and user["country"]=='India':
        indianUsers.append(user)
    
len(indianUsers) # Total number of user in India (11.5K Indian users)


# In[28]:



# Total number of organisations in India

organizationList=dict()
for user in indianUsers:
    if "organization" in user and user["organization"]!='':
        organization = user["organization"]
        if organization not in organizationList:
            organizationList[organization]=[user]
        else:
            organizationList[organization].append(user)
            
# number of organisations (959 organizations)
print(len(organizationList))


# In[29]:


# Filtering on organizations

filteredListNames=[]
filteredList={}
for organization in organizationList:
    if len(organizationList[organization])>20: # Filtering organisations with > 20 users
        filteredList[organization]=organizationList[organization]
        filteredListNames.append(organization)

# Organizations with size > 20 
print(len(filteredListNames))


# In[30]:


filteredListNames # List of organizations 


# In[31]:


filteredList['IIIT Bangalore'] # Sanity check of IIIT-Bangalore data


# In[32]:


# Number of users in filtered organizations

# We want to know the number of contests the user has participated.
# This requires several API calls which sometimes fail. Hence they are wrapped in a try except block
# We need to run this till all the data is loaded

userCount=0
s=requests.Session()
for org in filteredList:
    for user in filteredList[org]:
        userCount+=1
        if "contestCount" not in user:
            try:
                user["contestCount"]= len(json.loads(s.get("https://codeforces.com/api/user.rating?handle=" +user["handle"]).text)["result"])
                print(user["handle"],userCount)
            except:
                print("FAIL",user["handle"])


# In[33]:


print(userCount) # Total users


# In[34]:


# Soring final list of users

with open('../data/user_filtered.json', 'w') as fp:
    json.dump(filteredList, fp)

