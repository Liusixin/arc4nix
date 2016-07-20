arc4nix
===================

## About This Project ##
arc4nix provides a set of [arcpy](http://desktop.arcgis.com/en/arcmap/10.3/analyze/arcpy/what-is-arcpy-.htm)-compatible APIs on both Windows and Linux platform.
arc4nix uses ArcGIS Java Runtime SDK to provide cross-platform functionality to execute many geospatial analytical [arcpy functions](https://developers.arcgis.com/java/guide/local-server-geoprocessing-tools-support.htm).

## How to use
Simply replace
```Python
import arcpy
```
with
```Python
import arc4nix as arcpy
```
That's all!

## Installation
1. Prerequisites:
 	- JDK
 	- Scala 2.10.x
 	- Python 2.7.x
 	- Git
	- ArcGIS Runtime Java SDK 10.2.4. You need obtain proper license from ESRI to deploy/redistribute it.
2. Compiling:
 	1. Install ArcGIS Runtime Java SDK 10.2.4
	2. Add `export ARCGISRUNTIMESDKJAVA_10_2_4=<ArcGIS_Runtime_Installation_folder>` environment variable to your shell environment if using Linux. *It is highly recommended `source init_sdk_java.sh` in `.bashrc` file*. ArcGIS Runtime Java SDK automatically sets it in Windows.
	3. Clone me, then:
		- Copy all jar files in ArcGIS Runtime Java SDK `sdk` folder to `RuntimeManager/lib`
		- In `runtimemanager` folder, execute
			```
			$ sbt
			> compile
			> assembly
			```
		- in `arcgis4nix` folder, excute
			```
			$ python setup.py build_gpk
			$ python setup.py build
			$ python setup.py install
			```
	4. Ensure in arc4nix.data, there is "ExecFile_v101.gpk" and "RuntimeManager-assembly-*.jar"

## Supported functions and types
arc4nix supports most geospatial analytical functions. Some functions not explicitly supported by ArcGIS Runtime might also work. A typical arcpy function is like
```python
result = arcpy.MinimumBoundingGeometry_management("parks.shp",
                                         "c:/output/output.gdb/parks_mbg",
                                         "RECTANGLE_BY_AREA", "NONE")
```
In this example, `arcpy.MinimumBoundingGeometry_management` will be `eval()` on ArcGIS Runtime Local Server and result will be serialized as JSON then saved in a dummpy `arc4nix.Result` object. The dummpy class `arc4nix.Result` provides compatible functions (e.g. `getOutput()`, `getMessage()`).

The arc4nix acutally `eval()` each arcpy function in a seperate process (actually, a completely different, isolated, odd Python environment). So it is not possible to share variables between your script and remote arcpy functions. arc4nix makes efforts to passthrough variables but not all cases could be supported.

Native Linux paths are acceptable. arc4nix will dynamically map them into correct *wine* path. However, it is highly recommended to use absolute path on Linux because this would be the easist way to let arc4nix know the variable is a path to be mapped to *wine* drivers (Z:). I am working in progress to tag each parameter in each function whether a path or not. Please be aware that ArcGIS Runtime Local Server has its own working directory, which is different from working directory of the native Python process. Using relative path in wine may cause unexpected result. 

If no license is set in `arc4nix.local_server`, ArcGIS Runtime will work in developer mode which pops up a dialog showing license notice. If you'd like to deploy this program in headless-linux environment (e.g. HPC cluster), you must obtain a stardard license from ESRI and proper extensions. To set license code, EDIT `arc4nix/local_server.py` then reinstall the python package.

The package is not extensively tested. Bug reports and contributes are extremely welcome.


## WARNING! WARNING! WARNING!
THIS PACKAGE WILL FAITHFULLY EXECUTE ANY PYTHON SCRIPTS PASSED TO IT. BAD GUYS CAN COMPLETELY CONTROL YOUR SYSTEM USING EXPOSED LOCAL SERVER INSTANCE. PLEASE ENSURE YOUR WORK ENVIRONMENT IS COMPLETELY SAFE AND TRUSTED.

## How it works:
The idea is very simple. For each arcpy call, we actually send that line of code to ArcGIS Runtime Local Server. The GPResult is dumped to a JSON `GPString` and captured by a dummpy `arc4nix.Result` instance. Most of work is to make transparent wrap of arcpy functions.

## Working with arcpy.sa.Raster:
*Working in progress now. Please check back later*
arc4nix.sa.Raster generally provides same functionality with arcpy.sa.Raster. expressions like `Raster('A') - Raster('B')` is supported. Conversion between numpy object and Raster object is not supported. ArcGIS Runtime on Linux runs under *wine*, for performance aspect, running numpy operations under *wine* is meaningless. Use GDAL to read raster as numpy locally is simpler.

## Known unsupported functions
Functions/Classes in following toolboxes are not implemented. It is possible to call them through arcgisscripting interface, namely `arcpy.gp.<function>`. However, one must use string representation of all input parameters. Wine path mapping might not work.
- Topology 
- Geostatistic
- Geocoding
- Networking
- Server
- Tracking

If you're using any of these functions, it is extremely welcomed to provide me some example how they work as python scripts. Some of them are not supported by ArcGIS Runtime. If you figured out how to call these functions via arc4nix (not through `send` function), please also let me know and I will add supports for them.

## Limitations
- Trying to call functions not listed in [supported function](https://developers.arcgis.com/java/guide/local-server-geoprocessing-tools-support.htm) will trigger a "Tool is not licensed" error. To run these tools with arcpy4nix, you have to set up an ArcGIS Server backend. (See future plan)
- Passing arc4nix.env to arcpy.env to server is not supported. You need manually set environments in "predefined block". WIP
- It it not possible to retrieve any vector dataset from "in_memory" workspace. If you work with "in_memory" workspace, remember save them to a physical path at the end.
- `Geometry`, `SpatialReferece`, `Extent` classes are not supported now. Implementation is planning.
- All classes in `arcpy.da` package are not supported. Implementation is nearly impossible. With best efforts, it is possible to implement a low-efficent SearchCursor dummy class. There is no benefits to CRUD geospatial data locally using `arcpy.da`. Please use [gdal/ogr] instead.

## License
arc4nix is licensed under GPLv3 with ESRI software excpetion. 

Copyright (C) 2016 Tropical Rainfall Research Group, Department of Geography, University of Florida

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses>.

Linking arc4nix statically or dynamically with other modules is making a combined work based on arc4nix. Thus, the terms and conditions of the GNU General Public License cover the whole combination.

In addition, as a special exception, the copyright holders of arc4nix give you permission to combine [name of your program] with free software programs or libraries that are released under the GNU LGPL and with code included in the standard release of ESRI licensed software under the your ESRI agreements (or modified versions of such code, with unchanged license). You may copy and distribute such a system following the terms of the GNU GPL for arc4nix and the licenses of the other code concerned{, provided that you include the source code of that other code when and as the GNU GPL requires distribution of source code}.

Note that people who make modified versions of arc4nix are not obligated to grant this special exception for their modified versions; it is their choice whether to do so. The GNU General Public License gives permission to release a modified version without this exception; this exception also makes it possible to release a modified version which carries forward this exception.

## Future Plan
Set up ArcGIS Server backend for arc4nix to run a wider range to geoprocessing functions. (WIP) The provided geoprocessing package is able to execute arbitrary arcpy functions. Unless ArcGIS Server and local clients are able to share same storage space (e.g. NAS, SDE database), a protocol to transfer data is essential. This might be very complex and very restricted.
