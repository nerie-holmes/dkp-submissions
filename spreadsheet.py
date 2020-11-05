import os
import json
import gspread
import urllib.request
import pandas
from oauth2client.service_account import ServiceAccountCredentials


url = "https://kc.kobotoolbox.org/api/v1/data/546740?format=json"
response = urllib.urlopen(url)
data = json.loads(response.read())
df = pd.json_normalize(data)

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']

json_creds = os.environ.get('GSHEET')
creds_dict = json.loads(json_creds)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

#json_creds = os.getenv("GOOGLE_SHEETS_CREDS_JSON")
#creds = ServiceAccountCredentials.from_json_keyfile_name(json_creds, scope)

client = gspread.authorize(creds)

# Find sheet by url
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1h67jenbOxA9a8g4M2ow3OHCabA_4D1oGCNg-4ic7a8A/edit?usp=sharing")
sheet = spreadsheet.sheet2

sheet.update([df.columns.values.tolist()] + df.values.tolist())

# Extract and print all of the values
#rows = sheet.get_all_records()
#print(rows)
