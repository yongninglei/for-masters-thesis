# -*- coding: utf-8 -*-
"""
Created on Tue May 31 16:00:02 2022

@author: alineware
"""
#------------ Preperation--------------------
import pandas as pd
import numpy as np
import glob
from unidecode import unidecode

# read the reference txt file, transfer the spanish word into english
wordfile='pyramidsandtrees.txt'
word=pd.read_csv(wordfile, sep='\t')
word.loc[:,'CUE']=word.loc[:,'CUE'].apply(unidecode) #change the spanish alphabet into English


# read the log files in the folder, compare the ID with excel documents online, print the 
# wrong file name for manual checking
SEGU = pd.read_csv('https://docs.google.com/spreadsheets/d/1LQnX8nsXr-lZQqOziO8qiiM_I1huGiCNxdUHCY7mybI/export?gid=0&format=csv',engine='python')
segu = SEGU.loc[SEGU['DO']==1, ['OsirixID', 'MINID','BIDS_sub','BIDS_ses']]

# ----------Data read & raw data cleaning------------------

files = glob.glob('*.log') #  * means all the str (is with some str processing strategy)  
tot_df=pd.DataFrame() # tot_df is the original df, store it for future reference 
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

#--------- Data cleaning--------------

#---------Merge the result with the response-------------

data['CUE']=np.nan
#at the lane demonstrate the type of cue presented, extract the cue and merge it with the answer txt file
data.loc[data['Code'].str.len()>10,'CUE']=data.loc[data['Code'].str.len()>10,'Code'].str.split('_').str[4] 

#check how many rows are the cue
CUE_num=data.loc[:,'CUE'].dropna().shape[0] #not all the cue are with response, using cue as target to get answer

''' get the index of cue
data2=data.reset_index() #why need to do this step
idx_og_CUE=data2.loc[data2['CUE'].notnull()].index.tolist()
CUE_og=data2.loc[data2['CUE'].notnull()]
'''

data2=pd.merge(data, word, how='left', on='CUE')
# first delete, delete the rows that are not Picture, and Response
clean_data2=data2.loc[~(data2['Code'].isin(["99","1",'98','endrest','rest']))]
# clean_data2['Trial']=clean_data2['Trial'].shift(-1)
clean_data2=clean_data2.reset_index()
'''
idx_all=data2.index.tolist()

idx_response_check=[i for i in idx_all if not i in idx_og_CUE]

response_og= data2.iloc[idx_response_check]
response_raw= response_og.loc[response_og['Event Type'].isin(['Response'])]

'''



'''
# first delete, delete the rows that are not Picture, and Response
drop_index1=data.loc[data['Code'].isin(["99","1",'98','endrest','rest'])].index #delete the irrelevant response

clean_data=data.drop(drop_index1)
clean_data=clean_data.reset_index()



SOL_row_bool=clean_data.iloc[:,-1].notnull()

SOL_sub_raw=clean_data.loc[SOL_row_bool] # in some trial, the cue were presented but maybe no response

idx_SOL=SOL_sub_raw.index.tolist()


idx_standard_trial=[i+2 for i in idx_SOL] # all the stadard trial should be P-P-R, so idx_p + 2 = idx_r

idx_standard_trial.pop()# the last one is out of bound(check by hand)

response_sub_raw=clean_data.iloc[idx_standard_trial] # if iloc[i+2] is not 51, 52, then will drop the trial

response_ctrl=response_sub_raw['Code'].isin(["51","52"])  & response_sub_raw['Event Type'].isin(['Response'])     

# Second delete, delete that trial that are not complete
response_sub=response_sub_raw[response_ctrl]  

idx_response=response_sub.index.tolist()

idx_SOL_update=[i-2 for i in idx_response]# the valid cue index

SOL_sub=clean_data.iloc[idx_SOL_update] 
'''

'''
# check the correctness of the response
response=response_sub.loc[:,'Code']
answer=SOL_sub.loc[:,'SOL']

compare=pd.concat([response, answer], axis=1)

compare['SOL']=compare['SOL'].shift(1)
 
compare['SOL']=compare['SOL'].apply(lambda x:x+50)

compare=compare.dropna()

compare['Result']=np.where(compare['Code'].astype(float)==compare['SOL'],'T','F') #the result comparasion is finished here

clean_data=pd.merge(clean_data, compare['Result'], how='left', left_index=True, right_index=True)
'''

# if ID larger than 40, means one day run, other wise it is two days run
ID_df=clean_data2.loc[:,['SubID','SesID','Run','Filename']].drop_duplicates() 

ID_lst=ID_df.loc[:,['SubID','SesID','Run']].apply(lambda x: tuple(x), axis=1).tolist() # maybe used the iterows 

result_df=ID_df.copy()

#group by the big DF into different run and make it callable
run_grp=clean_data2.groupby(['SubID','SesID','Run'])


#GET the RW split, PW split, FF split seperatly 
def get_trial_number(wordtype, df):
    return df.loc[df['Code']==wordtype,'Trial']


def trial_grpby(df):
    return df.groupby(df.Trial) # return the groupby trial 

def get_subdf(wordtype, df):
    complete=[]
    uncomplete=[]
    trial_number=get_trial_number(wordtype,df)
    trial_grp=trial_grpby(df)
    for item in trial_number:
        target_trial=trial_grp.get_group(item)
        if (target_trial.shape[0]==3) & (target_trial['CUE'].notnull().any()) & (target_trial['Event Type'].isin(['Response']).any()):
            complete.append(target_trial) 
        else:
            uncomplete.append(target_trial)  
    com=pd.concat(complete) if len(complete) > 0 else pd.DataFrame(columns=clean_data2.columns)
    uncom=pd.concat(uncomplete) if len(uncomplete) > 0 else pd.DataFrame(columns=clean_data2.columns)
            
    return [com,uncom]
  

#calculate their accurycy by using valuecounts() and choose the larger one 

def get_acc(wordtype_sub):
    wordtype=wordtype_sub[0]
    trial_number=wordtype['Trial'].drop_duplicates()
    trial_group=trial_grpby(wordtype)

    for items in trial_number:
        target_trial=trial_group.get_group(items)
        print (items)
        row_indexer= (wordtype['Trial']==items) & (wordtype['Event Type']=='Response')
        if int(target_trial['SOL'].apply(lambda x:x+50).loc[target_trial['SOL'].notnull()])==int(target_trial.loc[target_trial['Event Type']=='Response','Code']):
            wordtype.loc[row_indexer ,'Result']=1
        else:
            wordtype.loc[row_indexer,'Result']=0
    return wordtype["Result"].value_counts(1)[0]


    
    
# rr=get_acc(RW_sub)

# rr["Result"].value_counts(1)[1]


# RW_sub=get_subdf('RW',working_run)
# PW_sub=get_subdf('PW',working_run)
# FF_sub=get_subdf('FF',working_run)



# targ_trial.loc[targ_trial['Event Type'].isin(['Response']),'Code'].apply(pd.to_numeric, errors='coerce').iloc[0]==targ_trial['SOL'].apply(lambda x:x+50).dropna().reset_index(drop=True).apply(pd.to_numeric, errors='coerce').iloc[0]

# targ_trial['SOL'].apply(lambda x:x+50).loc[targ_trial['SOL'].notnull()].eq(targ_trial.loc[targ_trial['Event Type']=='Response','Code'])


#     targ_trial=trial_group.get_group(items)
#     print (items)
#     row_indexer= (RW['Trial']==items) & (RW['Event Type']=='Response')
#     if int(targ_trial['SOL'].apply(lambda x:x+50).loc[targ_trial['SOL'].notnull()])==int(targ_trial.loc[targ_trial['Event Type']=='Response','Code']):
    
#         RW.loc[row_indexer ,'Result']=1
#     else:
#         RW.loc[row_indexer,'Result']=0

for items in ID_lst:
    row_ctrl=result_df.loc[:,['SubID','SesID','Run']].apply(lambda x: tuple(x), axis=1)==items
    working_run=run_grp.get_group(items)
    
    RW_sub=get_subdf('RW',working_run)

    print(items)
    result_df.loc[row_ctrl,'Acc_of_RW']=get_acc(RW_sub)


    
    with pd.ExcelWriter(r'C:\Users\69580\Desktop\Output\ ' + working_run['Filename'].iloc[0] + '.xlsx') as writer:
        RW_sub[0].to_excel(writer, sheet_name='RW_complete_trial')
        RW_sub[1].to_excel(writer, sheet_name='RW_imcomplete_trial')
       
       
    result_df.loc[row_ctrl,'Acc_of_RW']=get_acc(RW_sub)
 

#problem_run=run_grp.get_group(('S041', 'T01', 'I'))    



# result_df.to_excel('reslut.xlsx')

# complete=[]
# uncomplete=[]
# trial_number=get_trial_number('PW',working_run)
# trial_grp=trial_grpby(working_run)
# for item in trial_number:
#     target_trial=trial_grp.get_group(item)
#     if (target_trial.shape[0]==3) & (target_trial['CUE'].notnull().any()) & (target_trial['Event Type'].isin(['Response']).any()):
#         complete.append(target_trial) 
#     else:
#         uncomplete.append(target_trial)
            
#     com=pd.concat(complete) if len(complete) > 0 else pd.DataFrame(columns=clean_data2.columns)
#     uncom=pd.concat(uncomplete) if len(uncomplete) > 0 else pd.DataFrame(columns=clean_data2.columns)

# working_run['Filename'].iloc[0]

# with pd.ExcelWriter(r'C:\Users\alineware\Desktop\Output\ ' + working_run['Filename'].iloc[0] + '.xls') as writer:
#     RW_sub[0].to_excel(writer, sheet_name='use')
#     RW_sub[1].to_excel(writer, sheet_name='notuse')