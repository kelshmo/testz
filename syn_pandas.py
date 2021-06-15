import synapseclient
import csv
import pandas as pd
import numpy as np

syn = synapseclient.Synapse()
syn = synapseclient.login()

## ____________________
# provenance
# set activity

## ____________________

# two data sets
entity = syn.get('syn1899498',downloadFile=True, downloadLocation='.')
entity2 = syn.get('syn1899498',downloadFile=True, downloadLocation='.')# this can be a different data set
#print(entity2.path)
#print(entity.path)

## this code will create n pandas data frame object
## this time 2

df1 = pd.read_csv(entity.path, sep='\t')
df2 = pd.read_csv(entity.path, sep='\t')
 
## if we run the folowing code it will display the
## wanted amount of exemples of the dataframe object
## we dont want to .tail() method will show last 5
# df1.head()
# df2.head()

## this technique  let us know the shape

print(df1.shape)
print(df2.shape)

## the folowing code if for statistical descriptors
## it will include counts, mean, std, min, 0.25 0.5 and 0.75 
## quantiles

print(df1.describe())
print(df2.describe())

## the folowing code will display a list object
## with the name of the columns

print(df1.columns)
print(df2.columns)

## the folowing code will display range index, class of the object
## data type, also null values and other important information

print(df1.info())
print(df2.info())

## concatenation of the dataframe objects.
## they are different methods to do this task and is recommended
## to explore the dfs, or have previous domain knowledge of the information
## as shape, dtypes.

## This method will concatenate data set at the end of the first
## one, creating a df with original columns and rows as addition
## of both rows. We define a list with the dataframe objects, the pass
## it to the concat function that recives one argumet (the list)
dfs = [df1, df2]
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

dfs = [df1, df2]
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
