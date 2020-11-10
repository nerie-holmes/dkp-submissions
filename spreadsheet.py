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

# Global
json_creds = os.environ.get('GSHEET')
creds_dict = json.loads(json_creds)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

# Local
#json_creds = os.getenv("GSHEET_FILE")
#creds = ServiceAccountCredentials.from_json_keyfile_name(json_creds, scope)

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
    col_names = ['_submission_time', 'Boss', 'Player', 'Toon', 'Comment']
    edf  = pd.DataFrame(columns = col_names)

    dff = df[df.columns & col_names]
    dff = pd.concat([edf,dff], axis=0, ignore_index=True)
    dff = dff.rename(columns={'_submission_time': 'DateTime'})
    dff = dff.sort_values(by=['DateTime'], ascending=False)
    dff = dff.applymap(str)

    # Update the sheet
    sheet.update([dff.columns.values.tolist()] + dff.values.tolist())

    # Call function in a new thread with timer
    threading.Timer(60, foo).start()

foo()
