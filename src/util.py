# log decorator
import json
import time
from threading import Thread

import requests

from src.MessageBus.MessageBus import MessageBus

nesting_level = 0
def log(func):
    def wrapper(*args, **kwargs):
        global nesting_level
        # get current time with milliseconds
        try:
            arg = [a.__dict__ for a in args]
        except:
            arg = args
        with open(f"{func.__name__}.log", 'a') as f:
            f.write(f"[{time.time()}]: Calling {func.__name__} with args {arg} and kwargs {kwargs}\n")
        #print(" " * nesting_level + f"[{time.time():.7f}]: Calling {func.__name__} with args {arg} and kwargs {kwargs}")
        nesting_level += 1
        result = func(*args, **kwargs)
        nesting_level -= 1
        return result
    return wrapper


class PerformanceSample:
    def __init__(self, **kwargs):
        self.timestamp     = kwargs.get('timestamp')
        self.function_name = kwargs.get('function_name')
        self.class_name    = kwargs.get('class_name')
    def to_json(self):
        return self.__dict__

class Message:
    def __init__(self, msg:str):
        self.msg = msg
    def to_json(self):
        return self.__dict__

def continous_sending():
    sampler_endpoint = "http://127.0.0.1:6000/performance_sampler"
    while True:
        performanceSample = message_bus.popTopic("performance_sample")
        requests.post(sampler_endpoint, json=performanceSample.to_json())


message_bus = MessageBus(['performance_sample'])
thread = Thread(target=continous_sending)

def monitorPerformance(should_sample_after: bool):
    # TODO: make it configurable from a config file
    if not thread.is_alive():
        thread.start()
    def decorator(func):
        def wrapper(*args, **kwargs):
            if should_sample_after:
                result = func(*args, **kwargs)
                timestamp = time.time()
            else:
                timestamp = time.time()
                result = func(*args, **kwargs)
            sample = {"timestamp": timestamp, "function_name": func.__name__, "class_name": str(args[0].__class__).split("'>", maxsplit=1)[0].split('.')[-1]}
            performanceSample = PerformanceSample(**sample)
            message_bus.pushTopic("performance_sample", performanceSample)
            return result
        return wrapper
    return decorator

