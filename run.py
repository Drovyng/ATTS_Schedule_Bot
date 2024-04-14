from pprint import pprint

import sheets

# Пример чтения файла
values = sheets.service.spreadsheets().values().get(
    spreadsheetId=sheets.spreadsheet_id,
    range='A1:E10',
    majorDimension='COLUMNS'
).execute()
pprint(values)

# Пример записи в файл
values = sheets.service.spreadsheets().values().batchUpdate(
    spreadsheetId=sheets.spreadsheet_id,
    body={
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": "B3:C4",
             "majorDimension": "ROWS",
             "values": [["This is B3", "This is C3"], ["This is B4", "This is C4"]]},
            {"range": "D5:E6",
             "majorDimension": "COLUMNS",
             "values": [["This is D5", "This is D6"], ["This is E5", "=5+5"]]}
	    ]
    }
).execute()
