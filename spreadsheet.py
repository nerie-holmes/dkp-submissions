import os
import json
import gspread
import urllib.request
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import datetime, threading

# Path to kobotoolbox form
url = "https://kc.kobotoolbox.org/api/v1/data/546740?format=json"
# Use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']

# Local
#json_creds = os.environ.get('GSHEET')
#creds_dict = json.loads(json_creds)
#creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

# Global
json_creds = os.getenv("GSHEET")
creds = ServiceAccountCredentials.from_json_keyfile_name(json_creds, scope)

client = gspread.authorize(creds)

# Find sheet by url
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1h67jenbOxA9a8g4M2ow3OHCabA_4D1oGCNg-4ic7a8A/edit?usp=sharing")
sheet = spreadsheet.worksheet("Attendance")

def foo():
    # Get data from kobotoolbox
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    df = pd.json_normalize(data)

    # Do some clean up for submission to Google Sheet
    df.fillna('', inplace=True)
    df = df.applymap(str)
    dff = df[['_submission_time', 'Boss', 'Player', 'Toon', 'Comment']]
    dff = dff.rename(columns={'_submission_time': 'DateTime'})

    # Update the sheet
    sheet.update([dff.columns.values.tolist()] + dff.values.tolist())

    # Call function in a new thread with timer
    threading.Timer(60, foo).start()

foo()    
