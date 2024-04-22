import time

from googleapiclient import errors

from run_saver import RunSaver
from colorama import init, Fore, Style

saver = RunSaver()

init(autoreset=True)

import traceback
try:
  print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "Запуск...")
  import main
  main.run_bot(saver)
except Exception as err:
  errType = str(err)
  if errType == "BotRestartCommand":
    print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "Рестартим...")
  elif errType.count("UpdateFile|") != 0:
    import versioner
    whatFile = errType.split("|")[1]
    print(Fore.LIGHTCYAN_EX + Style.BRIGHT + f"Запрос на обновление файла {whatFile}")
    
    success = versioner.downloadFile(whatFile)
    
    if success:
      print(Fore.LIGHTGREEN_EX + Style.BRIGHT + f"{whatFile} успешно обновлён!")
    else:
      print(Fore.LIGHTRED_EX + Style.BRIGHT + f"{whatFile} не обновлён!")
    
  else:
    print(Fore.LIGHTRED_EX + Style.BRIGHT + traceback.format_exc(chain=True))
time.sleep(4)
saver.running = False
quit()
