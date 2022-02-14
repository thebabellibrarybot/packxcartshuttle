#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from IPython import get_ipython


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



fullpack_lst = list(zip(ldimlst, hdimlst, wdimlst, titles))


# In[5]:


from rectpack import newPacker
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from rectpack import PackingMode, PackingBin, SORT_LSIDE, PackerBBF
from rectpack import MaxRectsBssf

#%store -r fullpack_lst


# In[6]:


Cleanfulllst = []

Fitbasebin = []
Inbasebin = []
Outbasebin = []

Fitatticbin = []
Inatticbin = []
Outatticbin = []

Fitbigbin = []
Inbigbin = []
Outbigbin = []


Fullpack = []
Afterbase = []
Afterattic = []


# In[7]:


# packing args

def newPacker(mode=PackingMode.Offline, 
         bin_algo=PackingBin.BBF, 
        pack_algo=MaxRectsBssf,
        sort_algo=SORT_LSIDE, 
        rotation=False):
    packer_class = None

    # Offline Mode
    if mode == PackingMode.Offline:
        if bin_algo == PackingBin.BBF:
            packer_class = PackerBBF
            sort_algo=None
    if sort_algo:
        return packer_class(pack_algo=pack_algo, sort_algo=sort_algo, 
            rotation=rotation)
    else:
        return packer_class(pack_algo=pack_algo, rotation=rotation)


# In[8]:




# def rotatable and still 


# In[9]:


# clean full 

def clean_rotate(dirty_lst):
    
    ldims = []
    wdims = []
    rids = []
    
    if dirty_lst == fullpack_lst:
        for items in dirty_lst:
            if len(items) == 4:
                if items[0] <= items[1]:
                    ldima = items[0] + 2
                    ldims.append(ldima)
                elif items[0] > items[1]:
                    ldimb = items[1] +2
                    ldims.append(ldimb)
                wdim = items[2] +1
                wdims.append(wdim)
                name = items[3]
                rids.append(name) 
        cleanlst = list(zip(ldims, wdims, rids))     
        for items in cleanlst:
            Cleanfulllst.append(items)
            
    return print(len(cleanlst)), print('len of full clean lst')


# In[10]:




# make c bins


# In[11]:


# check what fits bins attic, base, bigbin

attic = (95, 71, 95)
base = (95, 41, 95)
bigbin = (185, 112, 95)

def checkbin(packing_lst, bin_dims):
    
    if bin_dims == base:
        for item in packing_lst:
            if item[0] <= 95 and item[1] <= 41:
                if item[1] <= 95 and item[0] <= 41:
                    Fitbasebin.append(item)
        print(len(Fitbasebin))
        print('Fitsbasebin len')
    if bin_dims == attic:
        for item in packing_lst:
            if item[0] <= 95 and item[1] <= 71:
                if item[1] <= 95 and item[0] <= 71:
                    Fitatticbin.append(item)
        print(len(Fitatticbin))
        print('Fitsatticbin len')
    elif bin_dims == bigbin:
        for item in packing_lst:
            if item[0] <= 185 or item[1] <= 112:
                Fitbigbin.append(item)
        print(len(Fitbigbin))
        print('Fitbigbin len')
        
    return


# In[12]:


# pack bin from rectlist aka cleanlst

def packbin(rectlist):
    
    bins = []
    rects = rectlist
    inbinone = []
    outbinone = []
    
    if rects == Fitbasebin:
        bindim = (95, 95, 2)
        bins.append(bindim)
    elif rects == Fitatticbin:
        bindim = (95 ,95 ,2)
        bins.append(bindim)
    elif rects == Fitbigbin:
        bindim = (185, 95, 2)
        bins.append(bindim)
        
    pack = newPacker()
    for r in rects:
        pack.add_rect(*r)
    for b in bins:
        pack.add_bin(*b)
    pack.pack()
    
    rectlst = pack.rect_list()
    for l in rectlst:
        if l[0] < 1:
            inbin = l
            inbinone.append(inbin)
        elif l[0] > 1:
            outbin = l
            outbinone.append(outbin)
            
    if rectlist == Fitbasebin:
        for items in inbinone:
            Inbasebin.append(items)
        print(len(Inbasebin)), print('inbin base len') 
    elif rectlist == Fitatticbin:
        for items in inbinone:
            Inatticbin.append(items)
        print(len(Inbasebin)), print('inbin attic len') 
    elif rectlist == Fitbigbin:
        for items in inbinone:
            Inbigbin.append(items)
        print(len(Inbasebin)), print('inbin bin len') 

    return 


# In[13]:


# model inbin 

def model(binlist):
    
    all_rects = binlist
    plt.figure(figsize=(10,10))
    
    for rect in all_rects:
        b, x, y, w, h, rid = rect
        x1, x2, x3, x4, x5 = x, x+w, x+w, x, x
        y1, y2, y3, y4, y5 = y, y, y+h, y+h, y

        if [w, h] == binlist:
            color = '--k'
        else:
            color = '--r'
        plt.plot([x1,x2,x3,x4,x5],[y1,y2,y3,y4,y5], color)
        plt.annotate(rid, (x, y))
    plt.show()
    
    return


# In[ ]:





# In[14]:


def cleanpacked(packedlst):
    
    ldims = []
    wdims = []
    rids = []
    
    print(len(packedlst))
    print('len of packed items to clean')
    for items in packedlst:
        ldim = items[3]
        ldims.append(ldim)
        wdim = items[4]
        wdims.append(wdim)
        rid = items[5]
        rids.append(rid)
    cleanedpack = list(zip(ldims, wdims, rids))
    print(len(cleanedpack))
    print('cleanedpack len')
    
    return cleanedpack


# In[15]:


def findunpacked(packed, total):
    
    
    allreadypacked = cleanpacked(packed)
    allpacks = total
    stillpack = list((set(allpacks)-set(allreadypacked)))
    print(len(stillpack))
    print('len of stillpack items')
    
    if total == Cleanfulllst:
        for items in stillpack:
            Afterbase.append(items)
        print(len(Afterbase))
        print('len of available items afterbasepacked')
    if total == Afterbase:
        for items in stillpack:
            Afterattic.append(items)
        print(len(Afterattic))
        print('len of available items afteratticpacked')
    
    #if total == Afteratticpack:


# In[16]:


def packtruck(bintype):
    
    
    
    if bintype == 1:
        clean_rotate(fullpack_lst)
        checkbin(Cleanfulllst, base)
        packbin(Fitbasebin)
        model(Inbasebin)
        findunpacked(Inbasebin, Cleanfulllst)
        
    if bintype == 2:
        checkbin(Afterbase, attic)
        packbin(Fitatticbin)
        model(Inatticbin)
        findunpacked(Inatticbin, Afterbase)
        
    if bintype == 3:
        checkbin(Afterattic, bigbin)
        packbin(Fitbigbin)
        model(Inbigbin)
        findunpacked(Inbigbin, Afterattic)


# In[17]:


x = input("Truck being Loaded: ")


# In[18]:


if x == 'Big Blue':
    packtruck(1)
    print('============================================================================')
    packtruck(2)
    print('============================================================================')
    packtruck(3)
    print('=========================================================================FIN')



# In[ ]:





# In[ ]:





# In[19]:


#checkbin(Afterattic, bigbin)
#packbin(Fitbigbin)
#model(Inbigbin)
#findunpacked(Inbigbin, Afterattic)

