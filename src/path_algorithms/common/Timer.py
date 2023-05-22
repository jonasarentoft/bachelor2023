from functools import wraps
import time
import numpy as np

def timer(func):
    @wraps(func)
    def wrapper(*args):
        start_time = time.time()
        retval = func(*args)
        print(f'Took {np.round(time.time()-start_time, 2)} seconds to run path find algorithm')
        return retval
    return wrapper