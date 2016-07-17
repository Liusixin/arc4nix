import os
import sys
import subprocess

from setuptools import setup, find_packages, Command
from setuptools.command import build_py


class PackGpk(Command):

    description = "create gpk"
    user_options = []

    def initialize_options(self):
        """Set default values for options."""
        # Each user option must be listed here with their default value.
        self.cwd = None
        pass

    def finalize_options(self):
        """Post-process options."""
        self.cwd = os.getcwd()
        pass

    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        if sys.platform != "linux2" and sys.platform.find("win") == -1:
            raise OSError("arcpy4nix only supports Windows and Linux.")

        # Now we need copy exec_file.py to the gpk folder then pack it
        import shutil
        shutil.copy(
            src=os.path.join("arcpy4nix", "exec_file.py"),
            dst=os.path.join("gpk", "v101", "my_toolboxes", "exec_file.py")
        )

        shutil.make_archive("ExecFile", "zip", "gpk")
        shutil.move("ExecFile.zip", "ExecFile_v101.gpk")
        shutil.copy("ExecFile_v101.gpk", os.path.join("arcpy4nix", "data"))
        pass


class BuildPyAndPackGpk(build_py.build_py):
    def run(self):
        self.run_command('build_gpk')
        build_py.build_py.run(self)


setup(
    cmdclass={
        'build_gpk': PackGpk,
        'build_py': BuildPyAndPackGpk
    },

    name='arcpy4nix',
    version='0.0.1a0',
    packages=find_packages(),

    package_data={
        'arcpy4nix.data': ['*.gpk']
    },

    url='https://github.com/striges/arcpy4nix',
    license='MIT',
    author='sugar',
    author_email='sugar1987cn@gmail.com',
    description='cross-platform arcpy runtime'
)
