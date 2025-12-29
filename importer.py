from csv import reader
from datetime import datetime
from distutils.util import strtobool
from os import getenv, listdir

import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

print(listdir("exports"))

# Input vars
csv_path = getenv("INPUT_CSV_PATH")
spreadsheet_id = getenv("INPUT_SPREADSHEET_ID")
worksheet_id = int(getenv("INPUT_WORKSHEET"))
append_content = strtobool(getenv("INPUT_APPEND_CONTENT", "False"))

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


def next_available_row(worksheet):
    """
    Return the next available row in the first column
    gspread doesn't have a method to return the last row used
    """
    str_list = list(filter(None, worksheet.col_values(1)))
    return len(str_list) + 1

csv = pd.read_csv(csv_path, header=0, index_col=None)
print(csv)
raise

# # Read csv file as a list of lists
# with open(csv_path, "r") as read_obj:
#     # pass the file object to reader() to get the reader object
#     csv_reader = reader(read_obj)
#     # Pass reader object to list() to get a list of lists
#     list_of_rows = list(csv_reader)

# # Insert update timestamp to the list
# current_time = datetime.now().replace(second=0, microsecond=0)
# current_time = current_time.timestamp()
# list_of_rows[0].append("update_time")
# for data_row in list_of_rows[1:]:
#     data_row.append(str(int(current_time)))

# creds = Credentials.from_service_account_info(
#     service_account_info, scopes=scopes
# )
# client = gspread.authorize(creds)
# spreadsheet = client.open_by_key(spreadsheet_id)

# # get csv worksheet
# ws = spreadsheet.get_worksheet(worksheet_id)
# print("Write to:", ws)

# if append_content:
#     start_from = next_available_row(ws)
#     list_of_rows = list_of_rows[1:]  # skip header row
# else:
#     ws.clear()
#     start_from = 1

# # ws.add_rows(len(list_of_rows))
# print(list_of_rows)
# ws.insert_rows(list_of_rows, row=start_from)