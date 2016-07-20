import os
import sys
import pkg_resources
from .wrap_base import *
from .wrap_class import Result, Geoprocessor

gpk_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data",
    "ExecFile_v101.gpk"
)
assert os.path.exists(gpk_path), "Geoprocessing Runtime Packages not exists at %s" % gpk_path

# Start geoprocessing server.
java_exec = "java" if not "JAVA_HOME" in os.environ else os.path.join(os.environ["JAVA_HOME"], "bin", "java")

# Find the first jar.
print filter(lambda p: p.endswith(".jar"), pkg_resources.resource_listdir("arc4nix.data", ""))[0]



# Dummpy gp class
gp = Geoprocessor()


