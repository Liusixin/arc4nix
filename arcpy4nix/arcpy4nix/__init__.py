import os
from .wrap_base import *
from .result import Result

gpk_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data",
    "ExecFile_v101.gpk"
)
assert os.path.exists(gpk_path), "Geoprocessing Runtime Packages not exists at %s" % gpk_path




