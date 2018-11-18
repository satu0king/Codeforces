
# coding: utf-8

# ## Final Feature Extraction
# 
# In this notebook we use the complete user data and problem data. We perform a join on both the datasets and extract features of the same. We finally save the data as csv.

# In[1]:


import requests
import json
import time;


# In[2]:


s=requests.Session()

# Get current time
current_time = int(time.time())

# Load user data and problems solved by user
with open('../data/user_filtered_problems.json') as f:
    userList=json.load(f)

# Load problems data
with open('../data/problems.json') as f:
    problemList=json.load(f)


# In[3]:


problemList['1077F2'] # Checking on problem code


# In[4]:


# Problem tags

tags = set(['implementation', 'greedy', 'math', 'brute force', 'dp', 'constructive algorithms', 'data structures',
        'sortings', 'dfs and similar', 'binary search', 'graphs', 'number theory', 
        'strings', 'trees', 'combinatorics', 'two pointers', 'bitmasks', 'dsu', 'geometry', 'shortest paths', 'probabilities', 'hashing', 'games', 'string suffix structures', 'divide and conquer', 'graph matchings', 'ternary search', 'matrices', 'Other'])


# In[5]:


# Given problem list, get data for all problems, extract stastical features from the data and solve the same

def getProblemsSolvedFeature(plist2):
    
    # We will bucket problem difficulties
    bucketSize=200
    startDifficulty=800 
    endDifficulty=3000 
    
    # Number of buckets
    bucketCount=(endDifficulty-startDifficulty)//bucketSize+2
    difficultyBuckets=[0]*bucketCount
    
    # Initializations
    plist=[]
    featureList={}
    avgDifficulty=0
    avgDifficulty20=0
    
    tagDictionary={}
    for tag in tags:
        tagDictionary[tag]=0
    
    # Extracting problem data
    for problem in plist2:
        if problem in problemList:
            d=problemList[problem]
            for tag in d['tags']:
                if tag in tags:
                    tagDictionary[tag]+=1 # increasing tag count
                else:
                    tagDictionary["Other"]+=1
            if d["difficulty"] is not None: # Consider only those problems which have difficulty
                plist.append({"code":problem,"difficulty":int(d["difficulty"])})
    
    # Number of problems
    n=len(plist)
    
    # If number of problems is 0, fatal error occured. 
    if n==0:
        raise Exception("no problems solved")
    
    # Top 20% of the problems
    top20=max(1,int(n*0.2))
    
    # Sort problems by difficulty
    plist.sort(key = lambda x:x["difficulty"],reverse=True)
    
    for i,prob in enumerate(plist):
        diff = prob["difficulty"]
        avgDifficulty+=diff
        if i<top20:
            avgDifficulty20+=diff
        
        if(diff<startDifficulty):
            difficultyBuckets[0]+=1
        
        elif(diff>=endDifficulty):
            difficultyBuckets[-1]+=1
        else:
            difficultyBuckets[(diff-startDifficulty)//bucketSize]+=1
            
    avgDifficulty20/=top20
    avgDifficulty/=n
    
    # Extracting features
    
    # Number of problems solved 
    featureList["problem_count"]=n 
    
    # Stats on difficulty of problems 
    featureList["avg_difficulty"]=avgDifficulty
    featureList["avg_difficulty20"]=avgDifficulty20
    featureList["median"]=plist[n//2]["difficulty"]
    
    # Features of problem tags
    for tag in tagDictionary:
        featureList["tag_"+tag]=tagDictionary[tag]
        
    # Features of difficultyBuckets
    for i,v in enumerate(difficultyBuckets):
        featureList["difficulty_bucket"+str(i)]=v
    
    # Debug print statements
    # print(tagDictionary)
    # print(plist)
    # print(difficultyBuckets)
    
    return featureList
    


# In[6]:


# List of problems
a=['371C', '351A', '364A', '246A', '279D', '246B', '1020C', '269B', '697D', '246D', '990C', '912B', '478D', '220A', '415D', '908B', '232A', '363C', '981D', '723C', '610D', '137C', '1006A', '289B', '691A', '1066C', '1029C', '92C', '822A', '287C', '85B', '276D', '266B', '1033C', '489B', '195D', '831B', '500C', '111B', '135A', '828B', '910C', '487A', '5C', '388A', '286B', '353B', '831E', '122B', '414A', '485C', '1051C', '913B', '868B', '358C', '205B', '1043B', '438B', '192D', '225C', '350C', '1066A', '384C', '257C', '738D', '4D', '920B', '359D', '1005E1', '8C', '765D', '109A', '1062D', '361B', '355E', '54C', '448C', '519A', '448A', '350B', '958C1', '366B', '339A', '339C', '673A', '519B', '77C', '498A', '1046H', '701D', '182B', '1043F', '255C', '817C', '145B', '311A', '365B', '357B', '742C', '750D', '41D', '131D', '432D', '1005C', '831C', '1006B', '1062A', '934C', '354A', '228B', '339D', '761D', '484B', '33C', '697B', '4A', '599B', '742A', '272C', '1015B', '1029A', '1003C', '1005D', '448D', '841C', '958D1', '472A', '242C', '1066E', '919D', '914A', '1047C', '435D', '229B', '272D', '214B', '912A', '907A', '472D', '19B', '934A', '948D', '669A', '962D', '918C', '822B', '490C', '442B', '429A', '1029D', '932B', '908A', '150A', '279C', '329A', '87A', '793B', '998D', '268C', '230A', '1013D', '261A', '1062C', '1010C', '1066D', '264B', '348A', '861A', '1033B', '67B', '243A', '1006D', '626C', '1000D', '831A', '333B', '283B', '1041D', '498B', '782B', '466D', '1023D', '327D', '208D', '282B', '542C', '405D', '766D', '990A', '989A', '1025D', '669D', '166A', '962C', '937D', '75D', '777E', '958F2', '283A', '231D', '106D', '1017C', '1036B', '1009F', '368A', '914D', '342B', '669B', '866A', '914B', '958A1', '83B', '519D', '255D', '322B', '948A', '479C', '155B', '869A', '494B', '314A', '913C', '828C', '346B', '779B', '466C', '279A', '126B', '1042C', '128B', '723A', '704A', '448B', '192B', '519C', '841A', '777D', '903B', '101510C', '673B', '990B', '915C', '1009E', '360A', '958B1', '225A', '1005B', '149C', '337D', '937B', '868C', '805D', '915B', '578A', '96B', '1016D', '849B', '382C', '319A', '920C', '142B', '168D', '1066B', '1003E', '314B', '854C', '1043A', '32D', '205D', '416B', '359B', '1015A', '948B', '495B', '485B', '1003A', '935D', '1075D', '577C', '990E', '407A', '110B', '723D', '478C', '225B', '463C', '766B', '1016A', '1028B', '231A', '1028E', '436C', '689B', '489C', '669E', '37B', '932A', '1028A', '6D', '1016C', '1003D', '1043E', '898D', '385C', '455A', '910A', '341C', '915A', '321B', '958E1', '919A', '408B', '437B', '938A', '962B', '1062B', '300C', '960D', '960A', '18C', '294C', '510C', '500B', '982B', '486C', '1006F', '348B', '234D', '757A', '203D', '496C', '104C', '937A', '922B', '368C', '990D', '4B', '1005A', '750A', '18B', '118D', '464A', '77B', '246C', '667C', '1003B', '451B', '817E', '427C', '1017D', '1037E', '1075C', '869C', '101510B', '486D', '313A', '204A', '213B', '30C', '217A', '182D', '474B', '1038C', '551B', '13C', '493B', '841B', '154A', '742B', '731C', '92D', '493D', '910B', '903C', '96C', '401C', '87B', '9D', '233B', '337C', '485A', '899A', '1004D', '864C', '1038B', '914C', '340D', '486B', '237C', '1058D', '673D', '766C', '357C', '922C', '358D', '817B', '319B', '669C', '509E', '1058C', '608B', '251B', '295B', '424C', '761B', '375A', '978G', '496D', '235A', '898A', '610C', '400D', '957B', '301B', '1006E', '750C', '1008C', '344D', '198A', '828D', '430D', '380C', '271D', '490B', '982A', '757B', '559C', '365A', '1036C', '219C', '339B', '919C', '121A', '745C', '318C', '960B', '1016B', '66B', '205A', '507B', '909B', '913A', '868A', '938C', '1005E2', '982C', '569C', '500A', '750B', '441C', '1063B', '25D', '1023A', '934B', '960C', '148D', '234B', '908C', '35D', '547C', '746D', '58A', '101510A', '1038A', '187B', '777B', '982D', '18A', '722C', '352B', '1006C', '899B', '479D', '213A', '1043D', '864D', '828A', '73C', '935C', '932C', '431C', '849C', '53C', '58B', '274B', '123B', '407B', '405C', '152C', '508D', '989B', '948C', '472B', '1033A', '31C', '1041E', '43D', '101B', '14D', '961B', '788A', '958F1', '920A', '377A', '196B', '978D', '334B', '107A', '264A', '446B', '702E', '701C', '1011D', '359C', '271B', '938B', '922A', '185B', '898E', '937C', '1043C', '451D', '201A', '238B', '251A', '831D', '189A', '527B', '133B', '244B', '459C', '1015C', '777C', '71C', '320B', '263C', '903A', '869B', '864A', '489D', '312B', '1036A', '780D', '118A', '742D', '697C', '231C', '266C', '879C', '474C', '155D', '343A', '298C', '766A', '1058B', '375B', '219B', '472C', '368B', '723B', '892B', '864B', '1029B', '817A', '451C', '822C', '777A', '817D', '474A', '38E', '1062E', '353D', '505B', '1028D', '474D', '822D', '899C', '673C', '779C', '898B', '9C', '1028C', '1058A', '919B', '909A', '329B']


# In[7]:


# Check
getProblemsSolvedFeature(a)


# In[8]:


# Get features of user

def getFeatures(user):
    
    featureList={}
    
    # Extracting user data
    featureList["country"]=user["country"]
    featureList["handle"]=user["handle"]
    featureList["contribution"]=int(user["contribution"])
    featureList["contest_count"]=int(user["contestCount"])
    featureList["organization"]=user["organization"]
    featureList["rating"]=user["rating"]
    featureList["max_rating"]=user["maxRating"]
    featureList["friends_count"]=user["friendOfCount"]
    featureList["rank"]=user["rank"]
    featureList["duration"]=int((current_time-user["registrationTimeSeconds"])//(3600*24))
    
    # Features extracted from problems
    pfeatures=getProblemsSolvedFeature(user["problemsSolved"])
    for f in pfeatures:
        featureList[f]=pfeatures[f]
        
    return featureList
        
    
    


# In[9]:


# Extract features for all users
dataList=[]
for org in userList:
    for user in userList[org]:
         if "problemsSolved" in user:
            try:
                dataList.append(getFeatures(user))
            except:
                pass


# In[10]:


dataList[0]


# In[11]:


# Store data as CSV

import unicodecsv as csv

keys = dataList[0].keys()

with open('../data/final.csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(dataList)


# In[12]:


print(len(dataList))

