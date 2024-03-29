# -*- coding: utf-8 -*-
"""
Created on Tue May 10 17:05:36 2022

@author: alineware
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import glob

#no need
#files = glob.glob('*.log')

#for file in files:
    #df = pd.read_csv(file, delimiter=r"\s+", header=None, names=list(range(20)))
    #df.to_excel(file+'.xlsx', index=False)
 #####################   


#demand 0, build an empty dataframe with certain column for futher append
outputdf=pd.DataFrame(columns=["Subject ID", "Section ID", "Run",'Filename',
 'RW_acc_per','RW_RT_overall','RW_RT_correct','RW_RT_incorrect','RW_RT_sd',
 'PW_acc_per','PW_RT_overall','PW_RT_correct','PW_RT_incorrect','PW_RT_sd',
 'FF_acc_per','FF_RT_overall','FF_RT_correct','FF_RT_incorrect','FF_RT_sd' ])

# description
# The output data frame is for 194 documents in the file     
    #there should be a for loop to loop around all the .log or .xlsx documents  in the file
    #every line of the output dataframe should be respond to 1 document, the whole df should be responsible for the whole file

# testing algorithm for single document
# data loading

datafile='S001_DAY1_MINITWICE_4189-vOT_Triads_fMRI_I.log'
data2=pd.read_csv(datafile,header=0, skiprows=3, delimiter="\t")

data['Filename']=datafile

test=data.iloc[1,4] # location and index location 
test2=data.loc[#this place should be the row index, and after the comma, is the column name]

               
######################

SEGU = pd.read_csv('https://docs.google.com/spreadsheets/d/1LQnX8nsXr-lZQqOziO8qiiM_I1huGiCNxdUHCY7mybI/export?gid=0&format=csv',engine='python')
segu = SEGU.loc[SEGU['DO']==1, ['OsirixID', 'MINID','BIDS_sub','BIDS_ses']]
ss=SEGU

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
      df['Run']   = file[-5:-4]
      tot_df=pd.concat([tot_df,df])



#data cleanning, delete useless column
data=tot_df
#data cleanning, delete useless rows 
#data = data.drop(data[data.Event=="Port"].index)
#data = data.drop(data[data.Event=="Pulse"].index) # drop two useless rows, how to implement them in 1 line code? 
'''
i have question on this drop step, maybe implement it later
'''

#data split, firstly get the indexer or pointer to all the RW, PW, FF stimuli
def get_stimuli1(df,stimuli_type):
    return df[df['Code']==stimuli_type]

get_RW=get_stimuli1(data,"RW")
get_PW=get_stimuli1(data,"PW")
get_FF=get_stimuli1(data,"FF")

def get_stimuli2(df,stimuli_type): #the same thing from the previous one, i just found it and implement again
    type_group=df.groupby(df['Code'])
    return type_group.get_group(stimuli_type)

#get_RW2=get_stimuli2(data, "RW")
def get_stimuli3(df, stimuli_type):
    return df.loc[df['Code']==stimuli_type,:]

#RW_get=get_stimuli3(data2,'RW')
# secondly, groupby trial, and then can use getgroup to get all the trial that correspond to RW, PW. FF

'''
this step is to groupby the data into : subject, section, run 
for subject 1, at day1 section 1

'''


ID_df=data.iloc[:,[-3,-2,-1]]

ID_df=ID_df.drop_duplicates()

ID_lst=ID_df.apply(lambda x: tuple(x), axis=1).tolist()
'''''
'''
result_df=ID_df

''''
hhhhh
'''


run_gb=data.groupby(['SubID','SesID','Run'])
run_gb.get_group(("S041", "T01", "I"))

def get_run(SubID, SesID, Run):
    return run_gb.get_group()

	SubID	SesID	Run
0	S041	T01	I


for items in ID_lst:
    working_run=run_gb.get_group(items)
    


get_trial=data.groupby(data.Trial)

def word_type_split(stimulus_trial, trial_group):
    frames=[]
    for item in stimulus_trial:
        grp=trial_group.get_group(item)
        frames.append(grp)
    return pd.concat(frames)

RW_split=word_type_split(get_stimuli1(data,"RW").Trial, tiral_group)
PW_split=word_type_split(get_PW.Trial, tiral_group)
FF_split=word_type_split(get_FF.Trial, tiral_group)

#by now, we have perfectly seperate the who dataframe into valid RW, PW, and FF sub dataframe, next step is for data analysis

# output preparation

# firstly, seperate the id into subject name, run, section......
#def id_sep(datafile):
    #id_lst=datafile.split('_')
    #id_lst+=(id_lst[-1].split('.'))
# the needed index: 0,-3, 1~-7   
   # return [id_lst[0],id_lst[1:-7],id_lst[-3],datafile]   # out put the key component: Subject name: S001, Section:Day1,run:1


#secondly, for RW, PW, FF, calculate the acc. RT, seperatly 

def left_count(stimulitype):
    return len(stimulitype[stimulitype.Type=='51'].Type.tolist())

RW_opt_left=left_count(RW_split)

def right_count(stimulitype):
    return len(stimulitype[stimulitype.Type=='52'].Type.tolist())

RW_opt_right=right_count(RW_split)

def acc_calc(left_count, right_count):
    corr=left_count if left_count>right_count else right_count
    acc_per= 100*corr/(left_count+right_count)
    return round(acc_per,3)

RW_acc_per=acc_calc(RW_opt_left,RW_opt_right)

RW_acc_per

outputsubj1.extend([RW_acc_per])
outputsubj1

# reaction time calculation: overall RT avg, right decision avg, wrong decision avg


RW_split["RT"]=RW_split.Code.shift(-1)-RW_split.Code
RW_split["RT"]=RW_split["RT"].shift(1) # for this step, i create a new column on the dataframe, can we achieve this by def ?
#data[data["Type"].isin(["51",'52'])] omggggg i just found isin attribute, so helpful

#  RT avg
def get_RT(stimulitype,ctrl_lst):
    return stimulitype[stimulitype.Type.isin(ctrl_lst)]
    
#RW_split[RW_split.Type.isin(["51","52"])]

RW_RT_overall=get_RT(RW_split,["51","52"]).RT.mean()
RW_RT_std=get_RT(RW_split,["51","52"]).RT.std()
def lable_correct(left,right,df):
    if left>right:
        df['Correct']=df.Type=='51'
        return ['51']
    else:
        df['Correct']=df.Type=='52'
        return['52']

def lable_incorrect(left,right,df):
    if left<right:
        df['Correct']=df.Type=='51'
        return ['51']
    else:
        df['Correct']=df.Type=='52'
        return['52']        

RW_corr=lable_correct(RW_opt_left, RW_opt_right, RW_split)

RW_incorr=lable_incorrect(RW_opt_left, RW_opt_right, RW_split)

RW_RT_correct=get_RT(RW_split,RW_corr).RT.mean()

RW_RT_incorrect=get_RT(RW_split,RW_incorr).RT.mean()

outputsubj1.extend([RW_RT_overall,RW_RT_correct,RW_RT_incorrect,RW_RT_std])
outputsubj1

# same for PW, and FF
#looping for all files, how to make the code better that can be more automatic?



class Bwhavirour_Ana():
    #I want to use python oop to do this, so I can call do this
    # dataframe.get_acc ---- to get the accuracy for one certain file
    # dataframse.get_RT
    # and so on 
    # maybe set a class, called Behavirour_Ana
    # Behavirour_Ana.RW return RW_split
    # Behavirour_Ana.RW.get_RT
    
    #first step function, I want the class can help me seperate the dataframe in
    # to different stimuli sub split
    
    RW= 0 #get the dataframe of the RW split 
    PW= 0 #get the dataframe of the PW split 
    FF= 0 #get the dataframe of the FF split 

    # second, I want the class help me achieve B_a.RW.get_acc()
    
    get_acc= 0 #get the accuracy percent
    get_RT_overall=0 # get the overall reaction time avg
    get_RT_correct=0 # get the correct reaction time avg
    get_RT_incorrect=0 # get the incorrect reaction time avg
    get_RT_sd=0 ## get the overall reaction time std
    
    # other side function, I want the class can be used to store some key data 
    # for check the result are correct or not
    
    def __init__(self):