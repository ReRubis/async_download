from datetime import datetime
import time

new_update_time = datetime.now()
time.sleep(0.2354)
last_update_time = datetime.now()

last_update_time_delta = new_update_time - last_update_time
print(float(str(last_update_time_delta.seconds) + '.' +
      str(last_update_time_delta.microseconds)))
