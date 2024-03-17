from random import random

import numpy as np
import requests

from src.DataObjects.PreparedSession import PreparedSession


def recive():  # FIXME just for debug
    # recive
    label = ["high", "medium", "low"]
    test_array = np.array(label)
    random_num = np.random.choice(test_array)
    d = {'MeanAbsoluteDifferencingTransactionTimestamps': random()*100,
         'MeanAbsoluteDifferencingTransactionAmount': random()*100,
         'MedianLongitude': random()*100,
         'MedianLatitude': random()*100,
         'MedianTargetIP': random()*100,
         'MedianDestIP': random()*100,
         'Label': random_num
         }

    # d = ["ciao": random(), random(), random(), random(), random(), random(), random_num]

    p = PreparedSession(d)
    return p


for i in range(50):
    r = requests.post('http://127.0.0.1:5002/segregationSystem', json=recive().__dict__)
    print(r.json())
