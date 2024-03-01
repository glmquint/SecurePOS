from threading import *
import time

def signal_state(event):
   while True:
      time.sleep(5)
      print("Traffic Police Giving GREEN Signal")
      event.set()
      time.sleep(10)
      print("Traffic Police Giving RED Signal")
      event.clear()

def traffic_flow(event):
   num=0
   while num<10:
      print("Waiting for GREEN Signal")
      event.wait()
      print("GREEN Signal ... Traffic can move")
      while event.is_set():
         num=num+1
         print("Vehicle No:", num," Crossing the Signal")
         time.sleep(2)
      print("RED Signal ... Traffic has to wait")

event1=Event()
t1=Thread(target=signal_state, args=(event1,))
t2=Thread(target=traffic_flow, args=(event1,))
t1.start()
t2.start()
