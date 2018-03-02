import sys
import subprocess
import time
import os
import signal

subp = None

def run_subprocess_check():
  global subp
  subp = subprocess.Popen('echo Hello', stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

def kill_subprocess_check():

  os.killpg(os.getpgid(subp.pid), signal.SIGTERM)


if __name__ == "__main__":
  run_subprocess_check()
  print('Ran subprocess with pid: {}'.format(subp.pid))
  kill_subprocess_check()
  print('Killed subprocess')