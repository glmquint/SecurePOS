import ipaddress
import random

import numpy as np
import requests

from src.DataObjects.Session import PreparedSession


def recive():  # FIXME just for debug
    # recive
    label = ["normal", "moderate", "high"]
    test_array = np.array(label)
    random_num = np.random.choice(test_array)
    d = {'mean_absolute_differencing_transaction_timestamps': random.uniform(0,100),
         'mean_absolute_differencing_transaction_amount': random.uniform(0,100),
         'median_longitude': random.uniform(0,360)-180,
         'median_latitude': random.uniform(0,180)-90,
         'median_target_ip': int(ipaddress.IPv4Address(str(random.randint(0, 255))+"."+str(random.randint(0, 255))+"."+str(random.randint(0, 255))+"."+str(random.randint(0, 255)))),
         'median_dest_ip': int(ipaddress.IPv4Address(str(random.randint(0, 255))+"."+str(random.randint(0, 255))+"."+str(random.randint(0, 255))+"."+str(random.randint(0, 255)))),
         'label': random_num
         }

    # d = ["ciao": random(), random(), random(), random(), random(), random(), random_num]

    p = PreparedSession(d)
    return p


for i in range(50):
    r = requests.post('http://127.0.0.1:5002/segregationSystem', json=recive().__dict__)
    print(r.json())

