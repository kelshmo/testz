import synapseclient as sc
from functools import reduce
import pandas as pd
import numpy as np
from synapseclient import * 

## log in with personal identification
syn = sc.Synapse() 
syn = sc.login()

## list of the files that we will use
## entity_list =['syn25878115', 'syn25878114', 'syn25878112']
## parentId = syn25878110
## adding interactivity with user  
entity_list = []
parent_id = str(input('Plese enter the parent ID folder in the syn12345678 format: '))
len_entity_list = int(input('how many data frames are you planning to joint?'))

for i in range(1, len_entity_list+1):
       entity_list.append(str(input('please enter syn num {}:'.format(i))))
print('\nlist of syns to joint: {},\nParent folder: {}'.format(entity_list, parent_id))

## Code to download selected in current location
## Defining the frame and assigning the path where the entity is
## lowering and striping of white spaces at the beggining and end of the column name
## renaming the columns where we will joint
## merging an inner joint on fips

li= [] # empty list to recive the list of frames to reduceAdd
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
df_merged.to_csv('big_df2.csv')# changing into csv
version_2 = syn.store(File('big_df2.csv', parentId=parent_id), used=entity_list)


