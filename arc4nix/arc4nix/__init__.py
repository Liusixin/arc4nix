import local_server

from .wrap_base import *
import atexit


def set_license(client_id, license_code=[]):
    local_server.client_id = client_id
    local_server.license_codes = license_code


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

env = Environment()


