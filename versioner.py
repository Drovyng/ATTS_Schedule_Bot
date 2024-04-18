import requests, os

import requests.utils


def downloadFile(name:str) -> bool:
    if name == "run.py" or name == "versioner.py" or name == "START.bat" or name == "TEST START.bat":
        return False
    url = f"https://github.com/Drovyng/ATTS_Schedule_Bot/raw/main/{name}"
    if name.count("^") > 0:
        splitted = name.split("^")
        name = splitted[0]
        url = splitted[1]
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    }
    getted = requests.get(url, headers=headers)
    if getted.ok:
        with open(name, "w", encoding="UTF-8") as file:
            file.write(getted.text)
        return True
    return False