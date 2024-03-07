# log decorator
import time

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
