# from csv import reader
from datetime import datetime
from os import getenv

import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe

# Input vars
csv_path = getenv("INPUT_CSV_PATH")
spreadsheet_id = getenv("INPUT_SPREADSHEET_ID")
worksheet_id = int(getenv("INPUT_WORKSHEET"))

service_account_info = {
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_email": getenv("INPUT_GOOGLE_SERVICE_ACCOUNT_EMAIL"),
    "private_key": getenv("INPUT_GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY").replace(
        "\\n", "\n"
    ),
}
scopes = [
    "https://spreadsheets.google.com/feeds",
]


csv = pd.read_csv(csv_path, header=0, index_col=None)

# Insert update timestamp to the list
current_time = datetime.now().replace(second=0, microsecond=0)
current_time = current_time.timestamp()
csv['log_date'] = int(current_time)

# load existing csv file from google sheets
creds = Credentials.from_service_account_info(
    service_account_info, scopes=scopes
)
client = gspread.authorize(creds)
spreadsheet = client.open_by_key(spreadsheet_id)
ws = spreadsheet.get_worksheet(worksheet_id)
# get previous data
prev_data = get_as_dataframe(ws)

# append with new data
new_data = pd.concat([prev_data, csv], axis=0)
new_data = new_data.drop_duplicates()
set_with_dataframe(
    ws, new_data,
    include_index=False,
    resize=True
    )
