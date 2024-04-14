from pprint import pprint
from typing import Union

import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials

import config

# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = 'creds.json'
# ID Google Sheets документа (можно взять из его URL)
spreadsheet_id = config.spreadsheet_id

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

"""
def getRange(list_:str, range_:str) -> list[list[str]]:
    global service, spreadsheet_id
    return service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f"'{list_}'!{range_}",
        majorDimension='COLUMNS'
    ).execute()
"""

def saveGetValues(entered: dict) -> list[list[str]]:
    if "values" in entered.keys():
        return entered["values"]
    return [[]]

def getRange(range_:str) -> list[list[str]]:
    '''
    :param range_: For example 'A1:E10'
    :return: 2D String List [Y][X]
    '''
    global service, spreadsheet_id

    return saveGetValues(service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_,
        majorDimension='COLUMNS'
    ).execute())


def setRange(range_:str, values: list[list[str]]):
    '''
    :param range_: For example 'A1:E10'
    :param values: 2D String List [Y][X]
    '''
    global service, spreadsheet_id
    service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": range_,
                 "majorDimension": "COLUMNS",
                 "values": values}
            ]
        }
    ).execute()