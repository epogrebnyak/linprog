import time
from contextlib import contextmanager
from dataclasses import dataclass


def peek(x):
    """
    Lookup into dict of pulp.LpVariable.
    """
    return [v.value() for v in x.values()]



@dataclass
class Timer:
    elapsed: float = 0

    def __str__(self):
        return "Timer(elapsed={})".format(self.elapsed)

@contextmanager
def timer():
    """
    Use as: 
    
    with timer() as t:
        import time
        time.sleep(3)
        
    print(t.elapsed)        
    """
    start = time.perf_counter()
    t = Timer()
    try:
        yield t
    finally:
        t.elapsed = time.perf_counter() - start
        

if __name__ == "__main__":
    with timer() as t:
        import time
        time.sleep(2)           
    assert t.elapsed > 2   
    print(t)
        