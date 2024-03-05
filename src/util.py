# log decorator
import time

nesting_level = 0
def log(func):
    def wrapper(*args, **kwargs):
        global nesting_level
        # get current time with milliseconds
        current_time = str(time.time())
        print(" " * nesting_level + f"[{current_time}]: Calling {func.__name__} with args {args} and kwargs {kwargs}")
        nesting_level += 1
        result = func(*args, **kwargs)
        nesting_level -= 1
        return result
    return wrapper
