import pathlib
import sys

cur = pathlib.Path(__file__).resolve().parent
sys.path.append("{}/".format(cur.parent))
sys.path.append("{}/jq".format(cur.parent))
sys.path.append("{}/test".format(cur.parent))

from rich import print

from jq import Queuer
from func import long_loop, long_task

qr = Queuer(long_loop, 4)

d = list(range(5))

for idx, i in enumerate(d):
    r = qr.submit({"data": i}, idx)
    print(f"loop {i}")

print('####')

qr2 = Queuer(long_loop, 4)

d = list(range(5))

for idx, i in enumerate(d):
    r = qr2.submit({"data": i}, idx)
    print(f"loop2 {i}")

print('####')
r = qr.get_result_util_finish(len(d))
print(r)
r = qr2.get_result_util_finish(len(d))
print(r)
