import ipaddress
import random
from threading import Thread
from time import sleep

import numpy as np
import requests

from src.DataObjects.Session import PreparedSession
from src.Segregation.SegregationSystemConfig import SegregationSystemConfig
from src.Segregation.SegregationSystemOrchestrator import SegregationSystemOrchestrator


def produce():  # FIXME just for debug
    # recive
    label = ["normal", "moderate", "high"]
    test_array = np.array(label)
    random_num = np.random.choice(test_array)
    d = {
        'uuid': "1",
        'mean_abs_diff_transaction': random.uniform(0, 100),
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
    segregationSystemConfig = SegregationSystemConfig()
    print("send")
    i = 0
    while True:
        try:
            r = requests.post('http://127.0.0.1:' +
                              str(segregationSystemConfig.get_segregation_system_port()) +
                              '/segregationSystem', json=produce().__dict__)
            if str(r.status_code) != str(200):
                print("user non attivo")
            else:
                i += 1
                if i == 200:
                    break
        except Exception:
            pass
    print("[+] OK")


def test_run():
    thread2 = Thread(target=send_label)
    # this will allow the main thread to exit even if the server is still
    # running
    print("Sender ON")
    thread2.daemon = True
    thread2.start()

    print("Orchestator ON")
    segregation_system_orchestrator = SegregationSystemOrchestrator()
    segregation_system_orchestrator.run()
    sleep(5) # let the computaion ends
    print("Orchestator ENDs")

test_run()
