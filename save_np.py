#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import os 
import sys

glove_dirname = sys.argv[1]
filename='glove.42B.300d.txt'

wordmodel = {}

with open(filename,'r', encoding='utf-8') as f:
    for line in f:
        linesplit=line.split(' ')
        word=linesplit[0]
        vector = np.array([float(value) for value in linesplit[1:]])
        wordmodel[word] = vector
        


# In[8]:


wordarray=np.array(list(wordmodel.keys()))
v=np.array(list(wordmodel.values()),dtype=np.float32)

doc_path=os.path.expanduser(glove_dirname)
np.savetxt(os.path.join(doc_path, 'glove.42B.300d.vocab.txt'),wordarray,fmt="%s")
np.save(os.path.join(doc_path,'glove.42B.300d.npy'),v)


# In[ ]:




