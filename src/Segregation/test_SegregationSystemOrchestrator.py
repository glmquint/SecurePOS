import ipaddress
import random
from threading import Thread
from time import sleep

import numpy as np
import requests

from src.DataObjects.Session import PreparedSession
from src.Segregation.SegregationSystemOrchestrator import SegregationSystemOrchestrator


def produce():  # FIXME just for debug
    # recive
    label = ["normal", "moderate", "high"]
    test_array = np.array(label)
    random_num = np.random.choice(test_array)
    d = {'mean_abs_diff_transaction': random.uniform(0, 100),
         'mean_abs_diff_transaction_amount': random.uniform(0, 100),
         'median_longitude': random.uniform(0, 360) - 180,
         'median_latitude': random.uniform(0, 180) - 90,
         'median_target_ip': int(ipaddress.IPv4Address(
             str(random.randint(0, 255)) + "." + str(random.randint(0, 255)) + "." + str(
                 random.randint(0, 255)) + "." + str(random.randint(0, 255)))),
         'median_dest_ip': int(ipaddress.IPv4Address(
             str(random.randint(0, 255)) + "." + str(random.randint(0, 255)) + "." + str(
                 random.randint(0, 255)) + "." + str(random.randint(0, 255)))),
         'label': random_num
         }

    p = PreparedSession(**d)
    return p


def send_label():
    for i in range(50):
        r = requests.post('http://127.0.0.1:5002/segregationSystem', json=produce().__dict__)
        print(r.json())


def test_run():
    segregation_system_orchestrator = SegregationSystemOrchestrator()
    thread1 = Thread(target=segregation_system_orchestrator.run())
    # this will allow the main thread to exit even if the server is still running
    thread1.daemon = True
    thread1.start()

    thread2 = Thread(target=send_label())
    # this will allow the main thread to exit even if the server is still running
    sleep(3)
    thread2.daemon = True
    thread2.start()

    assert True

