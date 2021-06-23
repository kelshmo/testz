import synapseclient as sc
from functools import reduce
import pandas as pd
import numpy as np
from synapseclient import * 

## log in with personal identification
syn = sc.Synapse() 
syn = sc.login()

## list of the files that we will use
entity_list =['syn25878115', 'syn25878114', 'syn25878112']

## Code to download selected in current location
## Defining the frame and assigning the path where the entity is
## lowering and striping of white spaces at the beggining and end of the column name
## renaming the columns where we will joint
## merging on fips and inner.
li= [] # empty list to recive the list of frames to reduce
for items in entity_list:
        entity = syn.get(items,downloadFile=True, 
                  downloadLocation='.')
        df = pd.read_csv(entity.path)  
        li.append(df)
        df.columns = df.columns.str.strip().str.lower()     
        df.rename(columns = {'county_fips':'fips'}, inplace = True)
        df.rename(columns = {'countyid':'fips'}, inplace = True)
        df_merged = reduce(lambda left, right:pd.merge(left, right, on=['fips'], how='inner'),li)
        # reduce a function to an iterable and reduce it to a single cumulative value.
df_merged.to_csv('big_df.csv')# changing into csv
version_1 = syn.store(File('big_df.csv', parentId='syn25878110'), used=entity_list)
# project = syn.store(version_1, used=entity_list, used)

############################
## to upload to synapse
## the folowing code was used to upload the merged df
## please remove hashtag if we need to run upload (uploaded already)
#version_1 = syn.store(File('big_df.csv', parentId='syn25878110', used=used_files))
#project = syn.store(version_1)# list of input files and IDS