import time

scriptStr = ""

with open("main.py", "r", encoding="UTF-8") as file:
    scriptStr = file.read()


while True:
    exec(scriptStr)
    time.sleep(10)