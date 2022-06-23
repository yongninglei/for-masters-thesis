# -*- coding: utf-8 -*-
"""
Created on Sat May 14 17:31:38 2022

@author: alineware
"""

# this file is used for testing class

# class, object         
datafile='S001_DAY1_MINITWICE_4189-vOT_Triads_fMRI_I.log'
data=pd.read_csv(datafile,header=0, skiprows=3, delimiter="\t")

data['Filename']=datafile

test=data.iloc[1,4] # location and index location 
test2=data.loc[#this place should be the row index, and after the comma, is the column name]

class Circle:
    pass

circle1=Circle()
