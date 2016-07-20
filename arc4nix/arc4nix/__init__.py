import os
import sys
import pkg_resources
from .wrap_base import *
from .wrap_class import Result, Geoprocessor
import local_server

import time
time.sleep(5)

gpk_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data",
    "ExecFile_v101.gpk"
)
assert os.path.exists(gpk_path), "Geoprocessing Runtime Packages not exists at %s" % gpk_path

# Dummpy gp class
gp = Geoprocessor()


