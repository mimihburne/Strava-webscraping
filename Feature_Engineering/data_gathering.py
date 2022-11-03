import pandas as pd
import numpy as np

strava_activities1 = pd.read_csv('../Webscraping/strava_activities.csv')

del strava_activities1['Unnamed: 0']
del strava_activities1['id']

strava_activities1["Date"]=pd.to_datetime(strava_activities1["start_date_local"]).dt.date
strava_activities1["Time"]=pd.to_datetime(strava_activities1["start_date_local"]).dt.time

strava_activities1.index = strava_activities1.start_date_local
#3 columns, date,time and datetime. df indexed by datetime

#strava_activities1.info()
#no null values
#couldn't insert null values into table so had to convert to zeros

#strava_activities1.loc[strava_activities1['average_cadence'].isna(), :] -- how to do this with zeros
#select rows where average cadence is null/zero

#don't need to merge tables as only one
#print(strava_activities1['max_heartrate'].describe())

#print(strava_activities1['type'].dropna().unique()) #all unique sports

#print(strava_activities1.type.value_counts()) #number of all sports

print(strava_activities1.dtypes) #feature datatypes

def find_column_types(df):
    #identifies categorical, boolean and numerical values
    all_cols = list(df.columns)
    numerical_cols_temp = df._get_numeric_data().columns
    categorical_cols = list(set(all_cols) - set(numerical_cols_temp))
    bool_cols = [col for col in all_cols if np.isin(df[col].dropna().unique(), [0, 1,0.0,1.0]).all()]
    numerical_cols = list(set(numerical_cols_temp)-set(bool_cols))
    return categorical_cols, bool_cols, numerical_cols

cat_cols, bool_cols, num_cols = find_column_types(strava_activities1)

#for col in cat_cols:
#    print("{col}:{value}".format(col=col, value=pd.value_counts(strava_activities1[col],dropna=False)))
    #prints each column the value counts of entries

#----------------------------------------
#input splits - image reader

#add a readme

#if rowing speed =0,is erg, if not, is water
#write a data dictionary with units
#elapsed time is in seconds
#attribute information- establish units that are being used

#how to deal with zeros in data?
#value to replace zeros with depends on distribution
#significant correlation between heart rate and cadence because for pre-garmin runs, there was no HR or
#cadence picked up so many activities have (0, 0, 0) for these values