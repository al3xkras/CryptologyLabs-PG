from Lab6 import *
from random import randint
from numpy import array,inf
from time import time
from threading import Thread
import threading

def compareExecutionTime(A, B, reps=1, timelimit=3, **kwargs):
    t1 = []
    t2 = []
    res=None
    r1=None
    r2=None
    def f1(**kwargs):
        nonlocal r1,t1
        r1=A(**kwargs)
        t1.append(time() - time1)
    def f2(**kwargs):
        nonlocal r2,t2
        r2=B(**kwargs)
        t2.append(time() - time2)
    for i in range(reps):
        r1,r2=None,None
        time1 = time()
        
        l=len(t1)
        
        p1 = Thread(target = f1, kwargs = kwargs)
        p1.start()
        p1.join(timeout = timelimit)
        
        if len(t1)==l:
            t1.append(inf)
        
        l=len(t2)
        time2 = time()
        p2 = Thread(target = f2, kwargs = kwargs)
        p2.start()
        p2.join(timeout = timelimit)
        if len(t2)==l:
            t2.append(inf)
        
        assert r1 is None or r2 is None or r1==r2
        if res is None:
            res=r1
        r1=None
        r2=None
    t11 = array(t1, dtype=float)
    t21 = array(t2, dtype=float)
    
    return [(t11.mean(), t11.std()), (t21.mean(), t21.std()), res]

prime=[
    3,
    17,
    101,
    1013,
    10099,
    103141,
    1016783,
    10103099,
    107707549,
    10770592813,
    107705911723,
    4547337172376300111955330758342147474062293202868155909489
]
composite=[
    2,
    3*17,
    556,
    800001,
    1007*101,
    103141*1016783,
    245709213523*5299871829441939,
    5059489012128901*1298582838728545,
    4547337172376300111955330758342147474062293202868155909393
]
def execFor(n, expected):
    A=is_prime_miller_rabin
    p=n
    print("n =",p)
    k=min(10000,max(5,p//1000))
    print("k =",k)
    time1,time2,res=compareExecutionTime(A,A,timelimit=3, reps=3,n=p,k=k)
    
    print("Mean exec. time of %s:        %.12f" % (A.__name__, time1[0]))
    print("Std. of the exec. time of %s: %.12f" % (A.__name__, time1[1]))
    print("Result (is prime):",res)
    assert res==expected
    print()
    print()

    
if __name__=="__main__":
    for p in prime:
        execFor(p, True)

    for c in composite:
        execFor(c, False)