#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import sys
import os
import re

def analogies(gloves, x, y, z, n):
    vec=list(gloves.values())
    wordlist=list(gloves.keys())
    movement=gloves[y]-gloves[x]+gloves[z]
    
    gap=[np.linalg.norm(vector-movement) for vector in vec]
    distance_vec=list(zip(wordlist,gap))
    distance_vec_sorted=sorted(distance_vec, key=lambda tup: tup[1])
    
    returnvalue=[]
    
    i=n
    start=0
    while i>0:
        if distance_vec_sorted[start][0]==z:
            start=start+1
            continue
        returnvalue.append(distance_vec_sorted[start][0])
        start=start+1
        i=i-1
        
    return returnvalue

def closest_words(gloves, word, n):
    #similar words
    #calculate all distance to the word we want to find
    vec=list(gloves.values())
    wordlist=list(gloves.keys())
    
    distance=[np.linalg.norm(wordvec-gloves[word]) for wordvec in vec]
    
    distance_vec=list(zip(wordlist,distance))
    
    distance_vec_sorted=sorted(distance_vec, key=lambda tup: tup[1])
    
    returnvalue=[]
    
    for i in range(n):
        returnvalue.append(distance_vec_sorted[i+1][0])
        
    return returnvalue
    

def plot_words(gloves, words, n):
    posall=[]
    nearestpointsall=[]
    for i in range(len(words)):
        word=words[i]
        nearestpoints=closest_words(gloves,word,n)
        pos=[gloves[value] for value in nearestpoints]
        pos.append(gloves[word])
        nearestpoints.append(word)
        posall=posall+pos
        nearestpointsall=nearestpointsall+nearestpoints
    
    pca = PCA(n_components=2)
    pca.fit(posall)
    vec_transform=pca.transform(posall)
    x=[vec_transform[i][0] for i in range(len(vec_transform))]
    y=[vec_transform[i][1] for i in range(len(vec_transform))]
    plt.scatter(x, y)
    print(nearestpointsall)

    for i, txt in enumerate(nearestpointsall):
        plt.text(x[i],y[i],txt,fontsize=9)
        
    plt.show()
    
def load_glove(glove_dirname):
    print(1)
    completedicitonary={}
    dictionaryweneed={}
    doc_path=os.path.expanduser(glove_dirname)
    
    vecs =np.load(os.path.join(doc_path,'glove.42B.300d.npy'))
    
    with open(os.path.join(doc_path,'glove.42B.300d.vocab.txt'))as f:
        lines=f.readlines()
        word=[line.strip('\n').lower() for line in lines]
        
    
    with open('/usr/share/dict/words') as f:
        lines=f.readlines()
        wordweneed=[line.strip('\n').lower() for line in lines]
        
    completedictionary = dict(zip(word, vecs))
    
    
    for i in range(len(wordweneed)):
        try:
            dictionaryweneed[wordweneed[i]]=completedictionary[wordweneed[i]]
        except:
            pass
            
    
    return dictionaryweneed


# In[ ]:


if __name__ == '__main__':
    glove_dirname = sys.argv[1]
    gloves = load_glove(glove_dirname='~/data')

    plot_words(gloves,['petal','love','king', 'cat'], 3)

    print("Enter a word or 'x:y as z:' (type 'exit' to quit)")
    cmd = ''
    while cmd!=None:
        cmd = input("> ")
        if cmd.strip()=='exit':
            break
        match = re.search(r'(\w+):(\w+) as (\w+):', cmd)
        if match is not None and len(match.groups())==3:
            x = match.group(1).lower()
            y = match.group(2).lower()
            z = match.group(3).lower()
            if x not in gloves:
                print(f"{x} is not a word that I know")
                continue
            if y not in gloves:
                print(f"{y} is not a word that I know")
                continue
            if z not in gloves:
                print(f"{z} is not a word that I know")
                continue
            words = analogies(gloves, x, y, z, 5)
            print("%s is to %s as %s is to {%s}" % (x,y,z,' '.join(words)))
        elif re.match(r'\w+', cmd) is not None:
            if cmd not in gloves:
                print(f"{cmd} is not a word that I know")
                continue
            words = closest_words(gloves, cmd.lower(), 5)
            print("%s is similar to {%s}" % (cmd,' '.join(words)))
        else:
            print("Enter a word or 'x:y as z:'")


# In[ ]:




