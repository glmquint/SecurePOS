# log decorator
import json
import time

import requests

nesting_level = 0
def log(func):
    def wrapper(*args, **kwargs):
        global nesting_level
        # get current time with milliseconds
        if nesting_level < 7:
            try:
                arg = [a.__dict__ for a in args]
            except:
                arg = args
            print(" " * nesting_level + f"[{time.time():.7f}]: Calling {func.__name__} with args {arg} and kwargs {kwargs}")
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


def monitorPerformance(should_sample_after: bool):
    # TODO: make it configurable from a config file
    sampler_endpoint = "http://localhost:6000/performance_sampler"
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
            requests.post(sampler_endpoint, json=performanceSample)
            return result
        return wrapper
    return decorator

