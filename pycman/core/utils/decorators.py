
import time
import functools


def timer(function):
    @functools.wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print("Total time running {:s}: {:.4n} seconds".format(function.__name__, t1 - t0))
        return result
    return function_timer
