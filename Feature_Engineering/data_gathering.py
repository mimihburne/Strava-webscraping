import pandas as pd
import numpy as np

strava_activities1 = pd.read_csv('../Webscraping/strava_activities.csv')
form_activities1 = pd.read_csv('../Additional_Data/Form_activities.csv')

'Sorting by Date and Time'
strava_activities1["time_of_day"]=pd.to_datetime(strava_activities1["start_date_local"]).dt.time
strava_activities1["start_date_local"]=pd.to_datetime(strava_activities1["start_date_local"]).dt.date
form_activities1["start_date_local"]=pd.to_datetime(form_activities1["start_date_local"], format='%d/%m/%Y').dt.date
form_activities1["time_of_day"]=pd.to_datetime(form_activities1["time_of_day"]).dt.time
form_activities1 = form_activities1.sort_values(by=["start_date_local","time_of_day"], ascending=False)
strava_activities1 = strava_activities1.sort_values(by=["start_date_local","time_of_day"], ascending=False)

del strava_activities1['Unnamed: 0']
del strava_activities1['id']

'Remove elapsed or moving from strava - investigation'
#condition = [strava_activities1['elapsed_time']== strava_activities1['moving_time'],strava_activities1['elapsed_time']!= strava_activities1['moving_time']]
#choices = ['elapsed_time', 'moving_time']
#strava_activities1['same'] = np.select(condition, choices, default='equal')
#print(strava_activities1.head(100))
#print(strava_activities1['same'].value_counts())
#print(strava_activities1.loc[strava_activities1['same'] == 'moving_time'])
#strava_activities1['difference'] = strava_activities1['elapsed_time'] - strava_activities1['moving_time']
#strava_activities1 = strava_activities1.sort_values(by=["difference"], ascending=False)
#print(strava_activities1.head(40))
#decide to keep both, but compare form elapsed to strava elapsed

'Nulls'
#form_activities1["time_of_day"].replace('NaN','00:00:00') replace nulls? will be filled when merge
#no nulls in strava, many in form (couldn't insert null values into strava table so had to convert to zeros)
#strava_activities1.info()
#strava_activities1.loc[strava_activities1['average_cadence'].isna(), :] -- how to do this with zeros
#value to replace zeros with depends on distribution
#significant correlation between heart rate and cadence because for pre-garmin runs, there was no HR or
#cadence picked up so many activities have (0, 0, 0) for these values

'Stats'
#print(strava_activities1['max_heartrate'].describe()) stats
#print(strava_activities1.loc[strava_activities1['max_heartrate'] == 202]) row where one column equals certain value
#print(strava_activities1['type'].dropna().unique()) #all unique sports
#print(strava_activities1.type.value_counts()) #number of all sports
#print(strava_activities1.dtypes) #feature datatypes
#print(form_activities1.dtypes)

def find_column_types(df):
    #identifies categorical, boolean and numerical values
    all_cols = list(df.columns)
    numerical_cols_temp = df._get_numeric_data().columns
    categorical_cols = list(set(all_cols) - set(numerical_cols_temp))
    bool_cols = [col for col in all_cols if np.isin(df[col].dropna().unique(), [0, 1,0.0,1.0]).all()]
    numerical_cols = list(set(numerical_cols_temp)-set(bool_cols))
    return categorical_cols, bool_cols, numerical_cols

#cat_cols, bool_cols, num_cols = find_column_types(strava_activities1)
#for col in cat_cols:
#    print("{col}:{value}".format(col=col, value=pd.value_counts(strava_activities1[col],dropna=False)))
    #prints each column the value counts of entries

'Combining the 2'
#1) combine all rows with duplicates with all columns