import threading
import time
from global_count import cou
def increment_counter():
    global count
    while True:
        time.sleep(2)
        cou.counter+=1