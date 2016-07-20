# coding=utf-8

import sys
import os
import subprocess
import pkg_resources
import threading
import Queue

ON_POSIX = 'posix' in sys.builtin_module_names

java_exec = "java" if "JAVA_HOME" not in os.environ else os.path.join(os.environ["JAVA_HOME"], "bin", "java")

local_server_jar = os.path.join(os.path.split(__file__)[0],
                                filter(lambda p: p.endswith(".jar"),
                                       pkg_resources.resource_listdir("arc4nix.data", "")[0]))

exec_file_gpk = os.path.join(os.path.split(__file__)[0],
                             filter(lambda p: p.endswith(".gpk"),
                                    pkg_resources.resource_listdir("arc4nix.data", "")[0]))

# We send command through stdin and receive information from stderr, write stdout to stderr.
local_server_process = subprocess.Popen(["ls", "/"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        bufsize=1, close_fds=ON_POSIX)

error_queue = Queue.Queue()


def enqueue_output(out, err, err_queue):
    for line in iter(err.readline, b''):
        err_queue.put(line)
    err.close()
    for line in iter(out.readline, b''):
        print >>sys.stderr, ">>>", line,
    out.close()


local_server_thread = threading.Thread(target=enqueue_output,
                                       args=(local_server_process.stdout,
                                             local_server_process.stderr,
                                             error_queue))
local_server_thread.daemon = True
local_server_thread.start()


def start():
    local_server_process.stdin.write("start" + os.linesep)


def shutdown():
    local_server_process.stdin.write("shutdown" + os.linesep)
    local_server_process.stdin.flush()
    local_server_thread.join()
