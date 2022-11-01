import pandas as pd
import requests
import json
import time

#help: https://medium.com/swlh/using-python-to-connect-to-stravas-api-and-analyse-your-activities-dummies-guide-5f49727aac86

## Get the tokens from file to connect to Strava
with open('strava_tokens.json') as json_file:
    strava_tokens = json.load(json_file)
## If access_token has expired then use the refresh_token to get the new access_token
if strava_tokens['expires_at'] < time.time():
    # Make Strava auth API call with current refresh token
    response = requests.post(
        url='https://www.strava.com/oauth/token',
        data={
            'client_id': 96221,
            'client_secret': '31e20ec9a15ada8ac83b6b8539be504d9699b51d',
            'grant_type': 'refresh_token',
            'refresh_token': strava_tokens['refresh_token']
        }
    )
    # Save response as json in new variable
    new_strava_tokens = response.json()
    # Save new tokens to file
    with open('strava_tokens.json', 'w') as outfile:
        json.dump(new_strava_tokens, outfile)
    # Use new Strava tokens from now
    strava_tokens = new_strava_tokens

page = 1
url = "https://www.strava.com/api/v3/activities"
access_token = strava_tokens['access_token']

## Create the dataframe ready for the API call to store your activity data
'''

'''

activities = pd.DataFrame(
    columns=[
        "id",
        "name",
        "start_date_local",
        "type",
        "distance",
        "elapsed_time",
        "moving_time",
        "total_elevation_gain",
        "kudos_count",
        "average_speed",
        "average_heartrate",
        "max_heartrate",
        "average_cadence"
    ]
)
while True:

    # get page of activities from Strava
    r = requests.get(url + '?access_token=' + access_token + '&per_page=200' + '&page=' + str(page))
    r = r.json()
    # if no results then exit loop
    if (not r):
        break

    # otherwise add new data to dataframe
    for x in range(len(r)):
        activities.loc[x + (page - 1) * 200, 'id'] = r[x]['id']
        activities.loc[x + (page - 1) * 200, 'name'] = r[x]['name']
        activities.loc[x + (page - 1) * 200, 'start_date_local'] = r[x]['start_date_local']
        activities.loc[x + (page - 1) * 200, 'type'] = r[x]['type']
        activities.loc[x + (page - 1) * 200, 'distance'] = r[x]['distance']
        activities.loc[x + (page - 1) * 200, 'elapsed_time'] = r[x]['elapsed_time']
        activities.loc[x + (page - 1) * 200, 'moving_time'] = r[x]['moving_time']
        activities.loc[x + (page - 1) * 200, 'total_elevation_gain'] = r[x]['total_elevation_gain']
        activities.loc[x + (page - 1) * 200, 'kudos_count'] = r[x]['kudos_count']
        activities.loc[x + (page - 1) * 200, 'average_speed'] = r[x]['average_speed']
        try:
            activities.loc[x + (page - 1) * 200, 'average_heartrate'] = r[x]['average_heartrate']
            activities.loc[x + (page - 1) * 200, 'max_heartrate'] = r[x]['max_heartrate']
        except KeyError:
            activities.loc[x + (page - 1) * 200, 'average_heartrate'] = 0
            activities.loc[x + (page - 1) * 200, 'max_heartrate'] = 0
        try:
            activities.loc[x + (page - 1) * 200, 'average_cadence'] = r[x]['average_cadence']
        except KeyError:
            activities.loc[x + (page - 1) * 200, 'average_cadence'] = 0

    # increment page
    page += 1
activities.to_csv('strava_activities.csv')

#adjust code so it only updates with new activities and doesn't have to load 800+ activities every time