import time
from colorama import init, Fore, Style

init(autoreset=True)

while True:
    import traceback
    try:
      print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "Запуск...")
      import main
    except Exception as err:
      if str(err) == "BotRestartCommand":
        print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "Рестартим...")
      else:
        print(Fore.LIGHTRED_EX + Style.BRIGHT + traceback.format_exc(chain=True))
    time.sleep(10)