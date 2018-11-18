
# coding: utf-8

# In[1]:


import pandas as pd, numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


# In[2]:


data = pd.read_csv('../data/final.csv')


# In[3]:


data.describe()


# In[4]:


data.info()


# In[5]:


data.head()


# In[6]:


ax = data.plot.scatter(x='problem_count', y='max_rating', color='red', label='Problems')
data.plot.scatter(x='problem_count', y='rating', color='green', label='Problems')

ax.set_title("Scatter plot between problem_count and max_rating")
plt.show()


# In[7]:


ax = data.plot.scatter(x='contest_count', y='max_rating', color='red', label='Contests')
data.plot.scatter(x='contest_count', y='rating', color='green', label='Contests')

ax.set_title("Scatter plot between contest_count and max_rating")
plt.show()


# In[8]:


ax = data.plot.scatter(x='friends_count', y='max_rating', color='red', label='Contests')
data.plot.scatter(x='friends_count', y='rating', color='green', label='Contests')

ax.set_title("Scatter plot between friends_count and max_rating")
plt.show()


# In[9]:


get_ipython().run_line_magic('matplotlib', 'inline')

data[["avg_difficulty","contest_count","max_rating"]].hist(bins=40, figsize=(20,15))
plt.show()


# In[10]:


def top10(x):
    a = sorted(list(x),reverse=True)
    n=int(max(len(a)*0.1,1))
    return sum(a[:n])/n
    
data.pivot_table(values='max_rating', index='organization', 
                 aggfunc=top10).sort_values(by=['max_rating'], ascending=False, inplace=False)   


# In[11]:


ax = data[data.contribution>5].plot.scatter(x='contribution', y='max_rating', color='red', label='Contrubutions')
data[data.contribution>5].plot.scatter(x='contribution', y='rating', color='green', label='Contrubutions')

ax.set_title("Scatter plot between Contrubutions and max_rating")
plt.show()


# In[12]:


ax = data[data.duration<4000].plot.scatter(x='duration', y='max_rating', color='red', label='Contests')
data[data.duration<4000].plot.scatter(x='duration', y='rating', color='green', label='Contests')

ax.set_title("Scatter plot between friends_count and max_rating")
plt.show()


# In[13]:


# Problem tags

tags = ['implementation', 'greedy', 'math', 'brute force', 'dp', 'constructive algorithms', 'data structures',
        'sortings', 'dfs and similar', 'binary search', 'graphs', 'number theory', 
        'strings', 'trees', 'combinatorics', 'two pointers', 'bitmasks', 'dsu', 'geometry', 'shortest paths', 'probabilities', 'hashing', 'games', 'string suffix structures', 'divide and conquer', 'graph matchings', 'ternary search', 'matrices', 'Other']


# In[14]:


tags=list(map(lambda x:'tag_'+x,tags))


# In[15]:


corr_matrix = data.corr() # corr() : Pandas method, computes pairwise correlation of columns, excluding NA/null values
corr_matrix["max_rating"].sort_values(ascending=False)


# In[16]:


data[tags]

labels = tags
sizes = data[tags].sum()

fig1, ax1 = plt.subplots(figsize=(11, 7))
fig1.subplots_adjust(0.3,0,1,1)


theme = plt.get_cmap('YlOrRd')
ax1.set_prop_cycle("color", [theme(1. * i / len(sizes)) for i in range(len(sizes)-1,-1,-1)])

_, _ = ax1.pie(sizes, startangle=90)

ax1.axis('equal')

total = sum(sizes)
plt.legend(
    loc='upper left',
    labels=['%s, %1.1f%%' % (
        l, (float(s) / total) * 100) for l, s in zip(labels, sizes)],
    prop={'size': 11},
    bbox_to_anchor=(0.0, 1),
    bbox_transform=fig1.transFigure
)

plt.show()

