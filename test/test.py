import pathlib
import sys

cur = pathlib.Path(__file__).resolve().parent
sys.path.append('{}/'.format(cur.parent))
sys.path.append('{}/jq'.format(cur.parent))
sys.path.append('{}/test'.format(cur.parent))

from jq import Queuer
from func import long_task

qr = Queuer(long_task, 3)

task_id = qr.submit({'data': 1})
print(task_id)
task_id = qr.submit({'data': 2})
print(task_id)

r = qr.get_result_util_finish(2)
print(r)
