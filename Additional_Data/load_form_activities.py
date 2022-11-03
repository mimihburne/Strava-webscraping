import pandas as pd
import requests
import json
import time

form_activities1 = pd.read_csv('Form_activities.csv')

form_activities1.info()

#clean data
#combine with strava activities
#work on duplicates