import gspread
from google.oauth2.service_account import Credentials
import json

from gspread_dataframe import set_with_dataframe


SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

with open(".logins/gsheet_creds.json") as json_file:
    creds_data = json.load(json_file)

credentials = Credentials.from_service_account_info(
    creds_data,
    scopes=SCOPES,
)
gc = gspread.authorize(credentials)


def send_to_gsheet(df, file, sheet, row=1, col=1):
    sh =  gc.open(file)
    wks = sh.worksheet(sheet)

    set_with_dataframe(wks, df, row, col, include_index=False, include_column_header=True)

def clear_gsheet(file, sheet):
    sh =  gc.open(file)
    wks = sh.worksheet(sheet)
    wks.clear()