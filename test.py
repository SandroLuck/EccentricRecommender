from timeit import default_timer
from contextlib import contextmanager


@contextmanager
def elapsed_timer():
    start = default_timer()
    elapser = lambda: default_timer() - start
    yield lambda: elapser()
    end = default_timer()
    elapser = lambda: end-start

a=range(10)
b=range(1000)
c=range(100000)
for i in c:
    e=5


with elapsed_timer() as eps:
    len(a)
    print(eps())

with elapsed_timer() as eps:
    len(b)
    print(eps())

with elapsed_timer() as eps:
    len(c)
    print(eps())
with elapsed_timer() as eps:
    len(a)
    print(eps())

with elapsed_timer() as eps:
    len(b)
    print(eps())

with elapsed_timer() as eps:
    len(c)
    print(eps())

