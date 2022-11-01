import pandas as pd
import requests
import json
import time

#http://www.strava.com/oauth/authorize?client_id=96221&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=profile:read_all,activity:read_all

# Make Strava auth API call with your
# client_code, client_secret and code
response = requests.post(
                    url = 'https://www.strava.com/oauth/token',
                    data = {
                            'client_id': 96221,
                            'client_secret': '31e20ec9a15ada8ac83b6b8539be504d9699b51d',
                            'code': '1191693cba02a30eb5899ddc8c16e68c7489e971',
                            'grant_type': 'authorization_code'
                            }
                )
#Save json response as a variable
strava_tokens = response.json()
# Save tokens to file
with open('strava_tokens.json', 'w') as outfile:
    json.dump(strava_tokens, outfile)
# Open JSON file and print the file contents
# to check it's worked properly
with open('strava_tokens.json') as check:
  data = json.load(check)
print(data)
