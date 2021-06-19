import synapseclient as sc
import csv
import pandas as pd
import numpy as np
from synapseclient import * 

syn = sc.Synapse() ## here is the personal log in of your synapse client log
syn = sc.login()

## ____________________
#    act = Activity(
#                name='merging_sets', 
#                description='union of data set on intersections'
#                )
#    act.used(['syn25878115','syn25878114', 'syn25878112'])
#    act.executed('')

## ____________________

## this code was used to upload the data locally 

#test_entity = File('acs2017_county_data.csv', 
#                    description='toy_data_wa', 
#                    parent='syn25878110')
#test_entity = syn.store(test_entity)
#test_entity2 = File('PovertyEstimates 2.csv', 
#                     description='toy_data_wa2', 
#                     parent='syn25878110')
#test_entity2 = syn.store(test_entity2)
#test_entity3 = File('County Voting.csv', 
#                     description='toy_data_wa3', 
#                     parent='syn25878110')
#test_entity3 = syn.store(test_entity3)


entity = syn.get('syn25878115',downloadFile=True, 
                  downloadLocation='.')
entity2 = syn.get('syn25878114',downloadFile=True, 
                  downloadLocation='.')
entity3 = syn.get('syn25878112',downloadFile=True, 
                  downloadLocation='.')

## Note that in some cases data can be is csv, but it 
## can be tab separate also defining the frames
df1 = pd.read_csv(entity.path)#, sep='\t')
df2 = pd.read_csv(entity2.path)#, sep='\t')
df3 = pd.read_csv(entity3.path)#, sep='\t')

## creating a list of the frames, so we can pass methods
## and get shape, data type information, max and min and 
## basic statistics

dfs = [df1, df2, df3]

for f in dfs:
    print(f.shape)
    print(f.info())
    print(f.head()) # or tail 
    print(f.describe())

## as we are going to manage to joint data frames, the
## columns should have as well similar format for easy access
## there is more especificatons that can be espressed here

for df in dfs:
    df.columns = df.columns.str.strip().str.lower()
    print(df.columns)

## After all that analysis we can notice than the information
## in fips is shared and we can joint the data there. 
## the columns names expressed differently fips, county_fips, 
## and countyid


df1.rename(columns = {'county_fips':'fips'}, inplace = True)
print(df1.columns)
df3.rename(columns = {'countyid':'fips'}, inplace = True)
print(df3.columns)


## missing data
for f in dfs:
    total_missing = f.isnull().sum().sort_values(ascending=False)
    percent_missing = (f.isnull().sum()/f.isnull().count()).sort_values(ascending=False)
    missing_data = pd.concat([total_missing, percent_missing], axis=1, keys=['Total', 'Percent'])
    print(missing_data.head(10))
    for i in range(0, len(total_missing)):
        if total_missing[i] != 0:
            print('\n\tERROR!!, We are missing data')
        else: pass

df3.dropna(inplace=True)

## if more than 80% of missing values we should consider dropping the 
## column. In this case is a very small fraction but is a good 
## oportunity to visit the problem. There is a lot to consider 
## when filling Null values, after this considerations,  we may use, 
## mean, medium, mode, interpolation or a random number. 

## here we will look into the fips of the missing area is null
## this code should coordenate the single Null (in this case)
 #   null_rows = df[df.isnull().any(axis=1)]
 #   if null_rows.shape() ###!= [0,0]:
 #       null_column = df[df.isnull().any(axis=0)]
 #       null_column

#  print(null_rows, null_column)
## 


## This method will merge the data set on the shared key column

concated_dfs = pd.merge(
                        left=df1,
                        right=df2, #list of dataframes
                        how='inner',
                        on='fips',
                        left_on=None, 
                        right_on=None, 
                        left_index=False, 
                        right_index=False, 
                        sort=False, 
                        suffixes=('_x', '_y'), 
                        copy=True, 
                        indicator='exist',# leave a mark
                        validate=None
                        )
                        
big_dfs = pd.merge(
                        left=concated_dfs,
                        right=df3, #list of dataframes
                        how='inner',
                        on='fips',
                        left_on=None, 
                        right_on=None, 
                        left_index=False, 
                        right_index=False, 
                        sort=False, 
                        suffixes=('_x', '_y'), 
                        copy=True, 
                        indicator=True,# leave a mark
                        validate=None
                        )


## the folowing code will show the merged dfs
## and basic information about it also missing values.

total_missing = big_dfs.isnull().sum().sort_values(ascending=False)
percent_missing = (big_dfs.isnull().sum()/big_dfs.isnull().count()).sort_values(ascending=False)
missing_data = pd.concat([total_missing, percent_missing], axis=1, keys=['Total', 'Percent'])
print(missing_data.head(10))
for i in range(0, len(total_missing)):
    if total_missing[i] != 0:
            print('\n\tERROR!!, We are missing data')
    else: pass

## the folowing code will show the merged dfs
print('big_df')
print(big_dfs)

print(big_dfs.shape)
print(big_dfs.info())
print(big_dfs.head()) # or tail 
print(big_dfs.describe())

big_dfs.to_csv('big_df.csv', sep='\t', index=False, header=True)

############################
## to upload to synapse
#version_1 = syn.store(File('big_df.csv', parentId='syn25878110'))
