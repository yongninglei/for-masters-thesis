# -*- coding: utf-8 -*-
"""
Created on Tue May 31 16:00:02 2022

@author: alineware
"""
'''
the fixed procedure, import the necessay dataframe package

load the reference word txt as well as all the trial logs
'''
import pandas as pd
import numpy as np
import glob
from unidecode import unidecode

# read the reference txt file, transfer the spanish word into english
wordfile='pyramidsandtrees.txt'
word=pd.read_csv(wordfile, sep='\t')
word.loc[:,'CUE']=word.loc[:,'CUE'].apply(unidecode) #change the spanish alphabet into
# English


# read the log files in the folder, compare the ID with excel documents online, print the 
# wrong file name for manual checking
SEGU = pd.read_csv('https://docs.google.com/spreadsheets/d/1LQnX8nsXr-lZQqOziO8qiiM_I1huGiCNxdUHCY7mybI/export?gid=0&format=csv',engine='python')
segu = SEGU.loc[SEGU['DO']==1, ['OsirixID', 'MINID','BIDS_sub','BIDS_ses']]

#looping the log file in the folder
files = glob.glob('*.log') # the * is with some str processing strategy 
tot_df=pd.DataFrame()# tot_df is the original df, store it for future reference 
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

# add one column in the data df, decode the cue from the ['Code'] column and add it
# to the ['CUE'] column
data['CUE']=np.nan
#select the cue stimuli in the code column
data.loc[data['Code'].str.len()>8,'CUE']=data.loc[data['Code'].str.len()>8,'Code'].str.split('_').str[4] 

# have the final df with all the information
data=pd.merge(data, word, how='left', on='CUE')

#compare the response with sol, calculate the accuracy

'''
algothrim 1

the big DF first 

drop the rows that are not Picure, Picure, Response in the event type column
compare it using .iloc[n,'SOL']==.iloc[n+2,'Code']

this algothrim is failed, because there are more lines than pulse and port input, the iloc is not suitable
'''
data['Trial']=data['Trial'].shift(-1)
drop_index1=data.loc[data['Code'].isin(["99","1",'98','endrest','rest'])].index #delete the irrelevant response

clean_data=data.drop(drop_index1)
clean_data=clean_data.reset_index()

'''
response_condition1=clean_data['Code'].isin(["51","52"])  & clean_data['Event Type'].isin(['Response'])
response_sub1=clean_data[response_condition1]
idx_re=response_sub1.index.tolist()

idx_selec=[i-2 for i in idx_re]+[i-1 for i in idx_re]
idx_selec.sort()
idx_pd=pd.DataFrame(idx_selec)
idx_pd=idx_pd.drop_duplicates()
idx_ss=idx_pd.tolist
'''

SOL_condition=clean_data.iloc[:,-1].notnull()

SOL_raw_sub=clean_data.loc[SOL_condition] # in some trial, the cue were presented but maybe no response

idx_SOL=SOL_raw_sub.index.tolist()

idx_standard_trial=[i+2 for i in idx_SOL]

idx_standard_trial.pop()# the last one is out of bound

response_raw_sub=clean_data.iloc[idx_standard_trial].drop_duplicates() # if iloc[i+2] is not 51, 52, then will drop the trial
response_condition1=response_raw_sub['Code'].isin(["51","52"])  & response_raw_sub['Event Type'].isin(['Response'])     

response_sub1=response_raw_sub[response_condition1]

idx_response=response_sub1.index.tolist()
idx_SOL_update=[i-2 for i in idx_response]# the valid cue index
SOL_sub=clean_data.iloc[idx_SOL_update] 

response=response_sub1.loc[:,'Code']
answer=SOL_sub.loc[:,'SOL']

compare=pd.concat([response, answer], axis=1)

compare['SOL']=compare['SOL'].shift(1)

compare['SOL']=compare['SOL'].apply(lambda x:x+50)

compare=compare.dropna()
compare['Result']=np.where(compare['Code'].astype(float)==compare['SOL'], 1, 0)

clean_data=pd.merge(clean_data, compare['Result'], how='left', left_index=True, right_index=True)

# below is some random notes
'''
drop_index1=data.loc[data['Event Type'].isin(['Pulse','Port Input'])].index


data = data.drop(drop_index)

clean_data=data.reset_index()



conditions=clean_data.iloc[:,-1].notnull()

only_cue=clean_data.loc[conditions]

iloc_of_cue=only_cue.index.tolist()
iloc_of_response=[i+2 for i in iloc_of_cue]

only_response=clean_data.iloc[iloc_of_response,4]

clean_data.head(5)
clean_data
'''

# if ID larger than 40, means one day run, other wise it is two days run
ID_df=clean_data.loc[:,['SubID','SesID','Run','Filename']].drop_duplicates()

ID_lst=ID_df.loc[:,['SubID','SesID','Run']].apply(lambda x: tuple(x), axis=1).tolist() # maybe used the iterows 

result_df=ID_df.copy()

#group by the big DF into different run and make it callable
run_grp=clean_data.groupby(['SubID','SesID','Run'])
for items in ID_lst:
    row_ctrl=result_df.loc[:,['SubID','SesID','Run']].apply(lambda x: tuple(x), axis=1)==items
    working_run=run_grp.get_group(items)
    result_df.loc[row_ctrl,'Acc_of_RW']=working_run['Result'].value_counts(1,ascending=True)[1] # call [1] is by index, means the correct answer

# Try things on the working_run
working_run.head(5)

# count the 1 or 0 in each run
acc=run_grp.get_group(ID_lst[15])['Result'].value_counts(1,ascending=True)[1]


