import pandas as pd
import numpy as np

strava_activities1 = pd.read_csv('strava_activities.csv')

#print(strava_activities1.head(3))

#strava_activities1.info()
#no null values
#couldn't insert null values into table so had to convert to zeros

#strava_activities1.loc[strava_activities1['average_cadence'].isna(), :] -- how to do this with zeros
#select rows where average cadence is null/zero

#don't need to merge tables as only one

#print(strava_activities1['type'].dropna().unique()) #all unique sports

#print(strava_activities1.type.value_counts()) #number of all sports

#print(strava_activities1.dtypes) #feature datatypes

def find_column_types(df):
    #identifies categorical, boolean and numerical values
    all_cols = list(df.columns)
    numerical_cols_temp = df._get_numeric_data().columns
    categorical_cols = list(set(all_cols) - set(numerical_cols_temp))
    bool_cols = [col for col in all_cols if np.isin(df[col].dropna().unique(), [0, 1,0.0,1.0]).all()]
    numerical_cols = list(set(numerical_cols_temp)-set(bool_cols))
    return categorical_cols, bool_cols, numerical_cols

cat_cols, bool_cols, num_cols = find_column_types(strava_activities1)

#print(cat_cols)
#print(num_cols)

for col in cat_cols:
    print("{col}:{value}".format(col=col, value=pd.value_counts(strava_activities1[col],dropna=False)))
    #prints each column the value counts of entries

#elapsed time is in seconds

#should dates be categorical or numerical - currently categorical but would be good to convert so they can be compared
#convert to datetime type
#parse format in pandas
#pandas.to_datetime()
#activities['date_local'] = format = current format
#to_timedelta
#group by month/year to see trends

#combine with holly data/other csv files
#manually input splits?

#attribute information- establish units that are being used

#add a readme

#how to deal with zeros in data?
#value to replace zeros with depends on distribution

#data visuals:
#line graph of UT2 against average HR and max HR on the same graph
#against date

#put into functions
