import time

while True:
    import traceback
    try:
      import main
    except Exception:
      print(traceback.format_exc(chain=True))
    time.sleep(10)