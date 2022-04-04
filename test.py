

import subprocess

#https://medium.com/@chaoren/how-to-timeout-in-python-726002bf2291
import time
from multiprocessing import Process


def Timeout():
    print('Start of function')
    while True:
        time.sleep(1)

process = Process(target=Timeout, name='Timeout')
process.start()
process.join(timeout=2)

process.terminate()
if process.exitcode is None:
    print(f'{process} Timeout!')


ls_call = subprocess.run(["ls"], stdout=subprocess.PIPE, text=True)
useless_call = subprocess.run(["cat"], stdout=subprocess.PIPE, text=True, input="Hello there?")
print(useless_call.stdout)  # Hello from the other side
print(ls_call.stdout)



