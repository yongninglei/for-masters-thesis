# -*- coding: utf-8 -*-
"""
Created on Mon May 23 14:02:26 2022

@author: alinewar

# test for df assign value

"""

import pandas as pd
import numpy as np

dic1={'name':['A','B','C','D','E','a','b','c','d','e'],
      'salary':['123','241','671','390','231','454','267','550','361','699'],
      'attendance':np.random.rand(10)
      }
df1=pd.DataFrame(dic1)

dic2={'name':['a',"B","C",'d'],
      'penalty': [-10,-1,-200,-55]
      }

df2=pd.DataFrame(dic2)
'''
for ppl in df2['name']:
    if df1.loc[:,['name']]==ppl:
       df1.loc[df1['name']==ppl,['penalty']]==1
    
for ppl in df2['name']:
    print (df2.loc[df2['name']==ppl,["penalty"]])
  
#df2.loc[:,["penalty"]]
#df2['penalty']



df1['name'].isin(['a',"B",'C','d'])

df1['name'].isin(vv)
vv=df2['name'].tolist(); vv
''' 
df3=df1[df1['name'].isin(['a',"B",'C','d'])].copy()

df3.loc[df3['name']==df2['name'],['penalty']]=df2['penalty']

df3.equals(df2)
df3['name'].reset_index(drop=True) == df2['name'].reset_index(drop=True)

df2.iterrows()
for r1 in range(df2.shape[0]) :
    for r2 in range (df3.shape[0]):
        if 

df1.merge(df2, how='outer', on='name')

pd.concat([df1, df2], join='outer', axis=1)

df4=pd.concat([df3,df2],axis=1)
df4=pd.merge(df2,df3,left_on='name',right_on='name')
df5=pd.DataFrame()

dicn={'name':['A','B','C','D','E'],
      'salary':[123,241,671,390,231],
      'estimate salary for C':['nan','nan','nan','nan','666']
      }
dfn=pd.DataFrame(dicn)


dfn['estimate salary for C']=np.nan

dfn.iloc[-1,-1]=671    


dfn['accuracy'] = np.where((dfn.loc[dfn['name']=='c','salary'] == dfn['estimate salary for C']), True, False)

'''
如果我 drop掉那些 pulse 和 无聊的行， 完事之后 重新sort index，然后用iloc索引
'''


dic_index_test={'name':['A','B','C','D','E','F'],
                'money':[6,9,5,8,0,1]
    }
df_index_test=pd.DataFrame(dic_index_test)
df_index_test

df=df_index_test.drop(index=[3,5])
df
df_re=df.reset_index()
df_re
df==df_re
df.iloc[3,1]

df_re.iloc[3,1]
