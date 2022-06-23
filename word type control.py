# -*- coding: utf-8 -*-
"""
Created on Thu May 19 22:08:52 2022

@author: alineware
"""

# for analysis the accuracy 
import pandas as pd

from unidecode import unidecode

wordfile='pyramidsandtrees.txt'
word=pd.read_csv(wordfile, sep='\t')

word['CUE'].apply(unidecode)
#get all the RW from datafile

data['Trial']=data['Trial'].shift(-1) # this shift -2 is manipulated, 

'''''

'''

data.insert(loc=4, column='Word',value=0)

word_indexer=data['Code'].str.len()>8

data['Word'][word_indexer]=data['Code'][word_indexer].str.split('_').str[4]


'''
check the correct answer of the word


'''
word['CUE'].isin(['plato']).value_counts()

del data['Correct answer']
data.insert(loc=5, column='Correct answer',value=0)



for words in data['Word'][word_indexer]:
    # the control condition
    if word['CUE'].apply(unidecode).isin([words]).value_counts()[0]==72:
        print(words)
    else:
        data.loc[data['Word']==words,'Correct answer']=word.loc[word["CUE"].apply(unidecode)==words,'SOL']

ddd=[]
for words in data['Word'][word_indexer]:
    # the control condition
    ddd.append(word.loc[word["CUE"].apply(unidecode)==words,'SOL'].tolist())

for i in range(len(ddd)):
    data.loc[word_indexer,'Correct answer'].iloc[i]=1


data['Word'][word_indexer]

for words in data['Word'][word_indexer]:
    # the control condition
    if word['CUE'].isin(['telefono']).value_counts()[0]==72:
        print(words)
    else:
        data['Correct answer'][word_indexer]=word['SOL'][word['CUE'].isin(['telefono'])]