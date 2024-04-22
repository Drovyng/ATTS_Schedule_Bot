import os, time


def startRun() -> float:
    startTime = time.perf_counter()
    os.system("\"C:\\Program Files\\Python312\\python.exe\" run.py")                         # \"C:\\Program Files\\Python312\\python.exe\"
    return time.perf_counter() - startTime


def startEmergency():
    os.system("\"C:\\Program Files\\Python312\\python.exe\" main_emergency.py")


last1 = -1
last2 = -1
last3 = -1
last4 = -1

while True:
    last4 = last3
    last3 = last2
    last2 = last1
    last1 = startRun()
    if min([last1, last2, last3, last4]) != -1 and sum([last1, last2, last3, last4]) / 4 < 180:
        startEmergency()