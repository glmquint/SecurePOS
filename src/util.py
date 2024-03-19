# log decorator
import json
import time

import requests

nesting_level = 0
def log(func):
    def wrapper(*args, **kwargs):
        global nesting_level
        # get current time with milliseconds
        current_time = str(time.time())
        if nesting_level < 7:
            try:
                arg = [a.__dict__ for a in args]
            except:
                arg = args
            print(" " * nesting_level + f"[{current_time}]: Calling {func.__name__} with args {arg} and kwargs {kwargs}")
        nesting_level += 1
        result = func(*args, **kwargs)
        nesting_level -= 1
        return result
    return wrapper

def monitorPerformance(should_sample_after: bool):
    # TODO: make it configurable from a config file
    sampler_endpoint = "http://127.0.0.1:4000/monitoring"
    def decorator(func):
        def wrapper(*args, **kwargs):
            if should_sample_after:
                result = func(*args, **kwargs)
                timestamp = time.time()
            else:
                timestamp = time.time()
                result = func(*args, **kwargs)
            requests.post(sampler_endpoint, json={"timestamp": timestamp, "function_name": func.__name__, "class_name": str(args[0].__class__).split("'>")[0].split('.')[-1]})
            return result
        return wrapper
    return decorator
