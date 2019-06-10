
#%%
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import collections
get_ipython().run_line_magic('matplotlib', 'inline')


#%%
job_df = pd.read_csv("job_trimmed.csv", index_col=0)
job_df.head()


#%%
job_df['state'].value_counts().plot.pie()


#%%
job_df.loc[job_df['description'].str.contains('bioengineering', case=False)]


#%%
job_df.loc[job_df['description'].str.contains('bioengineering', case=False)]['state'].value_counts().plot.pie(autopct='%1.1f%%')


#%%
job_df.loc[4648]['description']

#%% [markdown]
# # bring school lists

#%%
import json


#%%
with open('faculties_by_interests.json', 'r') as f:
    faculties_dic = json.load(f)


#%%
faculties_dic['Carnegie Mellon University']


#%%
faculties_dic.keys()


#%%
import difflib


#%%
difflib.SequenceMatcher(None, 'University of California-Berkeley', 'University of California - Berkeley').ratio()


#%%
difflib.SequenceMatcher(None, 'Columbia University', 'Coleman University').ratio()


#%%
difflib.SequenceMatcher(None, 'Columbia University', 'Columbia University in the City of New York').ratio()


#%%
difflib.SequenceMatcher(None, 'Columbia University', 'Columbia University in the City of New York').get_matching_blocks()


#%%
[a. for a in difflib.SequenceMatcher(None, 'Columbia University', 'Columbia University in the City of New York').get_matching_blocks()]


#%%
a = 'Columbia University'
b = 'Columbia University in the City of New York'
re.search(a, b)


#%%
from pprint import pprint


#%%
d = difflib.Differ()
pprint(list(d.compare(a, b)))


#%%
re.search('University of Pittsburgh','University of Pittsburgh-Bradford').string


#%%
re.search('University of California-Berkeley', 'University of California - Berkeley')


#%%
difflib.get_close_matches('Columbia University', school_df['Name'].values)


#%%
all([b in 'University of California-Berkeley' for b in 'University of California - Berkeley'.split(' ')])


#%%
srs = school_df['Name'].apply(lambda x: difflib.SequenceMatcher(None, 'University of California - Berkeley', x).ratio())


#%%
srs.idxmax()


#%%
for uni in faculties_dic.keys():
    temp = school_df['Name'].apply(lambda x: difflib.SequenceMatcher(None, uni, x).ratio())
    uni_match = school_df.loc[temp.idxmax()]['Name']
    print(uni, ' >>> ', uni_match)


#%%
school_trimmed_df = school_df.dropna(subset=['Enrolled total'])


#%%
school_trimmed_df.loc[school_trimmed_df['Name'].apply(lambda x: 'Carnegie Mellon University' in x)]


#%%
for uni in faculties_dic.keys():
    temp = np.array([1, 0])
    uni_match1 = school_trimmed_df.loc[school_trimmed_df['Name'].apply(lambda x: True if re.search(uni, x) else False)]
    if len(uni_match1) > 1:
        uni_match = school_trimmed_df.loc[uni_match1['Graduate enrollment'].idxmax()]['Name']
        temp = np.array([0.01, 0])
    elif len(uni_match1) == 0:
        temp = school_trimmed_df['Name'].apply(lambda x: difflib.SequenceMatcher(None, uni, x).ratio())
        uni_match = school_trimmed_df.loc[temp.idxmax()]['Name']
    else:
        uni_match = uni_match1['Name'].values
    if temp.max() < 0.9:
        print('================================================================++')
    print(uni, ' >>> ', uni_match, temp.max())


#%%
pitts_df = school_trimmed_df.loc[school_trimmed_df['Name'].apply(lambda x: True if re.search('University of Pittsburgh', x) else False)]
pitts_df


#%%
pitts_df['Graduate enrollment'].idm


#%%
ids = school_trimmed_df['Name'].apply(lambda x: difflib.SequenceMatcher(None, 'University of North Carolina', x).ratio()).sort_values(ascending=False)[:5]
school_df.loc[ids.index]


#%%
school_df.loc[ids.index]['Graduate enrollment']


#%%
school_df = pd.read_excel('IPEDS_data.xlsx', index_col=0)
school_df.head()


#%%
list(school_df.columns)


#%%
school_df['State abbreviation'].value_counts()


#%%
def get_school_info(uni):
    uni_match1 = school_trimmed_df.loc[school_trimmed_df['Name'].apply(lambda x: True if re.search(uni, x) else False)]
    if len(uni_match1) > 1:
        uni_match = school_trimmed_df.loc[uni_match1['Graduate enrollment'].idxmax()]
    elif len(uni_match1) == 0:
        temp = school_trimmed_df['Name'].apply(lambda x: difflib.SequenceMatcher(None, uni, x).ratio())
        uni_match = school_trimmed_df.loc[temp.idxmax()]
    else:
        uni_match = uni_match1.iloc[0]
    return uni_match


#%%
faculties_dic.keys()


#%%
get_school_info('Carnegie Mellon University')['State abbreviation'].values[0]


#%%
li = []
for univ in faculties_dic.keys():
    li.append(get_school_info(univ)['State abbreviation'])


#%%
pd.DataFrame(collections.Counter(li), index=['counter']).T.sort_values(ascending=False, by=['counter'])


#%%
pd.DataFrame(collections.Counter(li), index=['counter']).T.sort_values(ascending=False, by=['counter']).plot.barh(figsize=(10,10))


#%%
faculties_dic.keys()


#%%
univ_by_states = {}
for univ, dic in faculties_dic.items():
    sc_info = get_school_info(univ)
    state = sc_info['State abbreviation']
    if state not in univ_by_states:
        univ_by_states[state] = {}
    univ_by_states[state][univ] = {}
    univ_by_states[state][univ]['info'] = sc_info.to_dict()
    univ_by_states[state][univ]['faculties'] = dic


#%%
univ_by_states['Pennsylvania']['Carnegie Mellon University']['info']


#%%
univ_by_states['Pennsylvania']['Carnegie Mellon University']['info'].values()


#%%
json.dumps(univ_by_states['Pennsylvania']['Carnegie Mellon University']['info'], allow_nan=False)


#%%
import pickle


#%%
with open('univ_by_states.pickle', 'wb') as f:
    pickle.dump(univ_by_states, f)


#%%
with open('univ_by_states.pickle', 'rb') as f:
    data = pickle.load(f)
data.keys()


#%%



