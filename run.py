import time
from colorama import init, Fore, Style

init(autoreset=True)

import traceback
try:
  print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "Запуск...")
  import main
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