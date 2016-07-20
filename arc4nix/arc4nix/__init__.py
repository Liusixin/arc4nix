import os
import sys
import pkg_resources
from .wrap_base import *
from .wrap_class import Result, Geoprocessor, Envionment

import local_server
import time
import atexit


def kill_server_at_exit():
    local_server.shutdown()

atexit.register(kill_server_at_exit)

ready_msg = local_server.error_queue.get(True)
assert ready_msg == "[CMD]READY"
local_server.start()

service_msg = local_server.error_queue.get(True)
assert service_msg == "[CMD]Service"


# Dummpy gp class
gp = Geoprocessor()

env = Envionment()


