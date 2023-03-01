from datetime import datetime
import time

new_update_time = datetime.now()
time.sleep(0.2354)
last_update_time = datetime.now()

last_update_time_delta = last_update_time - new_update_time
print(str(last_update_time_delta.total_seconds()))
