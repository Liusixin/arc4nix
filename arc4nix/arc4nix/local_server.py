# coding=utf-8

import sys
import os
import subprocess
import pkg_resources
import threading
import Queue
import time

client_id = ""
license_codes = []

ON_POSIX = 'posix' in sys.builtin_module_names

java_exec = "java" if "JAVA_HOME" not in os.environ else os.path.join(os.environ["JAVA_HOME"], "bin", "java")

data_dir = os.path.join(os.path.split(__file__)[0], "data")

local_server_jar = os.path.join(data_dir,
                                filter(lambda p: p.endswith(".jar"), os.listdir(data_dir))[0])
assert os.path.exists(local_server_jar) and os.path.isfile(local_server_jar)

exec_file_gpk = os.path.join(data_dir,
                             filter(lambda p: p.endswith(".gpk"), os.listdir(data_dir))[0])
assert os.path.exists(exec_file_gpk) and os.path.isfile(exec_file_gpk)

error_queue = Queue.Queue()

# We send command through stdin and receive information from stderr, write stdout to stderr.
proc_cmd =  [java_exec, "-jar", local_server_jar, exec_file_gpk] + [client_id] + [license_codes]
print " ".join(proc_cmd)
local_server_process = subprocess.Popen(proc_cmd, stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        bufsize=1, close_fds=ON_POSIX)


def enqueue_error(err, err_queue):
    for line in iter(err.readline, b''):
        err_queue.put(line.rstrip())
    err.close()


def redirect_output(out):
    for line in iter(out.readline, b''):
        sys.stderr.write(line)
    sys.stderr.flush()
    out.close()


local_server_err_thread = threading.Thread(target=enqueue_error, args=(local_server_process.stderr, error_queue))
local_server_err_thread.daemon = True
local_server_out_thread = threading.Thread(target=redirect_output, args=(local_server_process.stdout,))
local_server_out_thread.daemon = True

local_server_out_thread.start()
local_server_err_thread.start()


def start():
    local_server_process.stdin.write("start" + os.linesep)


def shutdown():
    local_server_process.stdin.write("shutdown" + os.linesep)
    local_server_process.stdin.flush()
    time.sleep(3)
    local_server_process.stdin.write("exit" + os.linesep)
    local_server_process.stdin.close()
    local_server_process.kill()
    local_server_err_thread.join()
    local_server_out_thread.join()
