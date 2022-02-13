#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


#pull info from xlxs to dataframe

workbook = pd.read_excel('jan_pack.xlsx')
workbook = workbook.rename(columns={'Unnamed:0': 'view', 'Unnamed: 1': 'Pack_ID', 'Unnamed: 2': 'HM', 'Unnamed: 3': 'ARTnum', 'Unnamed: 6': 'dims'})


# In[3]:


# make list of xlxs data and format 
# as (l, h, w, float(rid)

HMlst = []
ARTlst = []
ldimlst = []
hdimlst = []
wdimlst = []


HMs = workbook.HM  
for HM in HMs:
    HMlst.append(HM)
ARTnums = workbook.ARTnum
for ARTnum in ARTnums:
    ARTlst.append(ARTnum)
dims = workbook.dims
for dim in dims:
    dim_ = dim.split(' x ')
    dimints = [float(dim) for dim in dim_]
    ldimlst.append(dimints[0])
    hdimlst.append(dimints[1])
    wdimlst.append(dimints[2])
Titlelst = list(zip(HMlst, ARTlst))   
titlelst = [' '.join(tups) for tups in Titlelst]
titlelsts = [title.replace('HM', '') for title in titlelst]
titlelstz = [title.replace('ART ', '') for title in titlelsts]
titleslst = [title.replace(' ', '.') for title in titlelstz]
titles = []
for title in titleslst:
    titlez = float(title)
    titles.append(titlez)
    


# In[4]:


# store info

fullpack_lst = list(zip(ldimlst, hdimlst, wdimlst, titles))
get_ipython().run_line_magic('store', 'fullpack_lst')


# In[ ]:




