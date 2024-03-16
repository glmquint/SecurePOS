from random import random

import numpy as np
import requests

from src.DataObjects.PreparedSession import PreparedSession


def recive():  # FIXME just for debug
    # recive
    label = ["high", "medium", "low"]
    test_array = np.array(label)
    random_num = np.random.choice(test_array)
    d = {'UUID': "1",
         'MeanAbsoluteDifferencingTransactionTimestamps': random(),
         'MeanAbsoluteDifferencingTransactionAmount': random(),
         'MedianLongitude': random(),
         'MedianLatitude': random(),
         'MedianTargetIP': random(),
         'MedianDestIP': random(),
         'Label': random_num
         }

    # d = ["ciao": random(), random(), random(), random(), random(), random(), random_num]

    p = PreparedSession(d)
    return p


for i in range(100):
    r = requests.post('http://127.0.0.1:5000/segregationSystem', json=recive().__dict__)
    print(r.json())
