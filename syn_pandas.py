import synapseclient
import csv
import pandas as pd
import numpy as np
from synapseclient import * 

syn = synapseclient.Synapse() ## here is the personal log in of your synapse client log
syn = synapseclient.login()

## ____________________
# provenance
# set activity

## ____________________

## this code was used to upload the data
#test_entity = File('acs2017_county_data.csv', description='toy_data_wa', parent='syn25878110')
#test_entity = syn.store(test_entity)
#test_entity2 = File('PovertyEstimates 2.csv', description='toy_data_wa2', parent='syn25878110')
#test_entity2 = syn.store(test_entity2)
#test_entity3 = File('County Voting.csv', description='toy_data_wa3', parent='syn25878110')
#test_entity3 = syn.store(test_entity3)



entity = syn.get('syn25878115',downloadFile=True, downloadLocation='.')
entity2 = syn.get('syn25878114',downloadFile=True, downloadLocation='.')
entity3 = syn.get('syn25878112',downloadFile=True, downloadLocation='.')

## Note that in some cases data can be is csv, but it can be tab separate also.
## Defining the frames
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

## more than 80% of missing values we should consider dropping the 
## column. In this case is a very small fraction but is a good 
## portunity to visit the problem. There is a lot to consider 
## when filling Null values, after this considerations,  we may use, 
## mean, medium, mode, interpolation or a random number. 

## here we will look into the fips of the missing area is null
null_rows = df[df.isnull().any(axis=1)]
if null_rows.item() != 0:
    null_column = df[df.isnull().any(axis=0)]
    null_column
#print(df3['childpoverty'])




## concatenation of the dataframe objects.
## they are different methods to do this task and is recommended
## to explore the dfs, or have previous domain knowledge of the information
## as shape, dtypes.

## This method will concatenate data set at the end of the first
## one, creating a df with original columns and rows as addition
## of both rows. We define a list with the dataframe objects, the pass
## it to the concat function that recives one argumet (the list)

concated_dfs = pd.concat(
                        dfs,
                        axis=0,     #the axis that we would like to concatenate
                        join="outer", #the type of joint
                        ignore_index=False, # important as if set to True, will reorganize the index 0 to n-1
                        keys=None, #construct herarchical indexes base on the keys passes (as a tuple if more than 1)
                        levels=None, #
                        names=None, #
                        verify_integrity=False, 
                        copy=True #
                        )
## the folowing code will show the dfs, take uncomment to show.
#print(concated_dfs)

## adding keys, it will help us keep track of the original dfs, 
## it will be and identification mark of the original data set


concated_dfs = pd.concat(
                        dfs,
                        axis=0,     #the axis that we would like to concatenate
                        join="outer", #the type of joint
                        ignore_index=False, # important as if set to True, will reorganize the index 0 to n-1
                        keys=['a','b'], #construct herarchical indexes base on the keys passes (as a tuple if more than 1)
                        levels=None, #
                        names=None, #
                        verify_integrity=False, 
                        copy=True # 
                        )
## the folowing code will show the dfs, take uncomment to show.
print('concatenated data frames')
print(concated_dfs)

## seting the key is great as we can refeer to the data original data set nicelly
## with the folowing code

## the folowing code will show the dfs, take uncomment to show.
## printing especific herarchical index, this case 'a' corresponding
## to the original df
print(concated_dfs.loc['a'])

############################

## creating a random df of similar characteristics
## it will be 3 columns by 100 rows and the random numbers
## will be normally distribuited and with the 
## reason to explore more concatenations

mean = 0
sd = 1
n = 100

random_df = pd.DataFrame({'A_':np.random.normal(mean, sd, n), 
                          'B_':np.random.normal(mean, sd, n),
                          'C_':np.random.normal(mean, sd, n),
                         })

print(random_df.head(100))
print(random_df.shape)

##############################
