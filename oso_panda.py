import synapseclient
import csv
import pandas as pd
syn = synapseclient.Synapse()
syn = synapseclient.login()

entity = syn.get('syn1899498',downloadFile=True, downloadLocation='.')
print(entity)
print(entity.path)

## this code will create a pandas data frame object
df = pd.read_csv('matrix_100_by_4.tsv', sep='\t')
 
## if we run the folowing code it will display the
## wanted amount of exemples of the dataframe object
# df.head()

## this technique  let us know the shape

print(df.shape)

## the folowing code if for statistical descriptors
## it will include counts, mean, std, min, 0.25 0.5 and 0.75 
## quantile as well

print(df.describe())
## the folowing code will display a list object
## with the name of the columns

print(df.columns)

## the folowing code will display range index, class of the object
## data type, also null values and other important information

print(df.info())
