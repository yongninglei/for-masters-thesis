# -*- coding: utf-8 -*-
"""
Created on Thu May 19 04:10:11 2022

@author: alineware
"""

import pandas as pd
import numpy as np
import glob

'''
creating the large DF contains all the information

in the meantime, check with the EXCEL online 

'''
#load the excel file for checking
SEGU = pd.read_csv('https://docs.google.com/spreadsheets/d/1LQnX8nsXr-lZQqOziO8qiiM_I1huGiCNxdUHCY7mybI/export?gid=0&format=csv',engine='python')
segu = SEGU.loc[SEGU['DO']==1, ['OsirixID', 'MINID','BIDS_sub','BIDS_ses']]

#start to looping around the file, 
#compare the filename with Excel record, if not same, print the filename for correction
#else append columns as subID, sesID and Run

files = glob.glob('*.log')

tot_df=pd.DataFrame()
for file in files:
    df = pd.read_csv(file, header=0, skiprows=3, delimiter="\t")
    df['Filename'] = file
    section_info = segu.loc[segu['OsirixID']==file.split('-')[0],['BIDS_sub','BIDS_ses']]

    if section_info.empty:
      print(file)
    else:
      df['SubID'] = section_info.iloc[0,0]
      df['SesID'] = section_info.iloc[0,1]
      df['Run']   = file.split("_")[-1].split(".")[0]
      tot_df=pd.concat([tot_df,df])

data=tot_df.copy()

result=data.loc[:,('Subject','Trial','Event Type','Code','TTime','SubID','SesID','Run')].copy()
result['Trial']=result['Trial'].shift(-1)

'''
now, groupby the total DF with SubID, SesID and Run

run analysis on every run

put them together into the result DF

'''
# if ID larger than 40, means one day run, other wise it is two days run
ID_df=result.iloc[:,[0,-3,-2,-1]].drop_duplicates()

ID_lst=ID_df.loc[:,('SubID','SesID','Run')].apply(lambda x: tuple(x), axis=1).tolist() # maybe used the iterows 

result_df=ID_df.copy

#group by the big DF into different run and make it callable
run_grp=result.groupby(['SubID','SesID','Run'])

# before looping, get all the function that needed for the data analysis
# first we need acuracy calculator

def get_stimuli(df, stimuli):
    return df.loc[df['Code']==stimuli,:].Trial #return the trial # of the selected word type: RW PW or FF

def group_trial(df):
    return df.groupby(df.Trial) # return the grouped by trial 

def stimuli_type_split(stimuli_Trial_num_df, trial_gp):
    frames=[]
    for item in stimuli_Trial_num_df:
        grp=trial_gp.get_group(item)
        frames.append(grp)
    return pd.concat(frames) # return the df that contains all the trial that are testing the given word type

RW_split

working_run.loc[working_run['Code'].isin(['52','51']) ,'Code'].value_counts(0,sort=True)
working_run.loc[working_run['Code'].isin(['52','51']) ,'Code'].value_counts(1,False)
working_run.loc[working_run['Code'].isin(['52','51']) ,'Code'].value_counts([[1,2]],False)

action_count= working_run.loc[working_run['Code'].isin(['52','51']) ,'Code'].value_counts()
accuracy= working_run.loc[working_run['Code'].isin(['52','51']) ,'Code'].value_counts()
action_df=pd.DataFrame()
action_df['Count']=action_count


def left_count(stimuli_split):
    return stimuli_split.loc[stimuli_split['Code'].isin(['51']) ,'Code'].value_counts()

def right_count(stimuli_split):
    return stimuli_split.loc[stimuli_split['Code'].isin(['52']) ,'Code'].value_counts()

def get_acc(left_count, right_count):
    corr=left_count if left_count>right_count else right_count
    acc_per= 100*corr/(left_count+right_count)
    return round(acc_per,3)

def lable_correct(left,right,stimuli_type_df):   # the variable is the left_count, right_count
    if left>right:
        stimuli_type_df['Correct']=stimuli_type_df.Type=='51'
        return ['51']
    else:
        stimuli_type_df['Correct']=stimuli_type_df.Type=='52'
        return['52']

def lable_incorrect(left,right,stimuli_type_df):
    if left<right:
        stimuli_type_df['Correct']=stimuli_type_df.Type=='51'
        return ['51']
    else:
        stimuli_type_df['Correct']=stimuli_type_df.Type=='52'
        return['52']        

def RT_calc(stimuli_type_df):
    return 
# then call reaction time
# then call mean and std
"""
accuracy analysis, get the correct answer from wordfile

"""

from unidecode import unidecode

wordfile='pyramidsandtrees.txt'
word=pd.read_csv(wordfile, sep='\t')

word.loc[:,'CUE']=word.loc[:,'CUE'].apply(unidecode)

#get all the RW from datafile

#data['Trial']=data['Trial'].shift(-1) # this shift -2 is manipulated, 

'''''
prepare the new column for checking, store the correct answer in somecolumn and then compare them 
'''

result.insert(loc=4, column='CUE',value='nan')
#data.Word=np.nan

#data.rename(columns={"Word":"CUE"},inplace=True)


wordinfo_row_loc=result['Code'].str.len()>8

result.loc[wordinfo_row_loc,'CUE']=result.loc[wordinfo_row_loc,'Code'].str.split('_').str[4] #
# they provide a website to show the difference of .loc and ['column'] 




#word['CUE'].isin(['plato']).value_counts()


for words in data.loc[wordinfo_row_loc, 'CUE']:
    # the control condition
    if word['CUE'].apply(unidecode).isin([words]).value_counts()[0]==72:
        print(words)
    else:
        data.loc[data['CUE']==words,'Correct answer']=word.loc[word["CUE"].apply(unidecode)==words,'SOL']

df00=pd.merge(result, word, how='inner', on='CUE')

df11=pd.merge(result, word, how='outer', on='CUE')

df22=pd.merge(result, word, how='left', on='CUE')

#df22.iloc[:,(-3,-2,-1)]=data.iloc[:,(-3,-2,-1)] ????? TWO MANY INDEXER, WHEN USING MERGE, IT tells me 
# that there are no common columns very strange 

df22.insert(loc=2, column="Event Type", value=0)

Event=data.loc[:,"Event Type"]


df22["Event Type"]=Event

Event.index.is_unique

aaaa=Event.index.duplicated()

# something need to be checked here
'''

some try that takes me long time, will research them later on

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
'''

#looping!
for items in ID_lst:
    working_run=run_grp.get_group(items)
    RW_trial=
    
    row_indexer=result_df['Filename'].isin(working_run['Filename'].drop_duplicates().tolist())
    
    result_df.loc[row_indexer,'RW_Acc_per']=RW_split.get_acc()# inside the variables: left choice count and right choice count 
    # RW_split refers to the RW, trial information
    result_df.loc[row_indexer,'RW_RT_overall']=RW_split.get_RT_overall()
    result_df.loc[row_indexer,'RW_RT_correct']=RW_split.get_RT_correct()
    result_df.loc[row_indexer,'RW_RT_incorrect']=RW_split.get_RT_incorrect()
    result_df.loc[row_indexer,'RW_RT_sd']=RW_split.get_RT_sd()
    result_df.loc[row_indexer,'RW_Acc_per']=RW_split.get_acc()# inside the variables: left choice count and right choice count 
   
    # RW_split refers to the RW, trial information
    result_df.loc[row_indexer,'PW_RT_overall']=PW_split.get_RT_overall()
    result_df.loc[row_indexer,'PW_RT_correct']=PW_split.get_RT_correct()
    result_df.loc[row_indexer,'PW_RT_incorrect']=PW_split.get_RT_incorrect()
    result_df.loc[row_indexer,'PW_RT_sd']=PW_split.get_RT_sd()
    result_df.loc[row_indexer,'PW_Acc_per']=PW_split.get_acc()# inside the variables: left choice count and right choice count 
 
    # RW_split refers to the RW, trial information
    result_df.loc[row_indexer,'FF_RT_overall']=FF_split.get_RT_overall()
    result_df.loc[row_indexer,'FF_RT_correct']=FF_split.get_RT_correct()
    result_df.loc[row_indexer,'FF_RT_incorrect']=FF_split.get_RT_incorrect()
    result_df.loc[row_indexer,'FF_RT_sd']=FF_split.get_RT_sd()
    