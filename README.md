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

	2. Add `export ARCGISRUNTIMESDKJAVA_10_2_4=<ArcGIS_Runtime_Installation_folder>` environment variable to your shell environment if using Linux. *It is highly recommended `source init_sdk.sh` in `.bashrc` file*. ArcGIS Runtime Java SDK automatically sets it in Windows.

	3. Clone me, then:
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

## Supported fuctions and types
arc4nix supports most geospatial analytical functions. Some functions not explicitly supported by ArcGIS Runtime might also work. A typical arcpy function is like
```python
result = arcpy.MinimumBoundingGeometry_management("parks.shp",
                                         "c:/output/output.gdb/parks_mbg",
                                         "RECTANGLE_BY_AREA", "NONE")
```
In this example, `arcpy.MinimumBoundingGeometry_management` will be `eval()` on ArcGIS Runtime Local Server and result will be serialized as JSON then saved in a dummpy `arc4nix.Result` object. The dummpy class `arc4nix.Result` provides compatible functions (e.g. `getOutput()`, `getMessage()`).

The arc4nix acutally `eval()` each arcpy function in a seperate process (actually, a completely different, isolated, odd Python environment). So it is not possible to share variables between your script and remote arcpy functions. arc4nix makes efforts to passthrough variables but not all cases could be supported.

Native Linux paths are acceptable. arc4nix will dynamically map them into correct *wine* path. However, it is highly recommended to start path with "/", ".", ".." or "path:" because this would be the easist way to let arc4nix know the variable is a path to be mapped to *wine*. I am working in progress to tag each parameter in each function whether a path or not. Please be aware that ArcGIS Runtime Local Server has its own working directory, which is different from working directory of the native Python process. Using relative path in wine may cause unexpected result. 

If no license is set via `arc4nix.set_license`, ArcGIS Runtime will work in developer mode which pops up a dialog showing license notice. If you'd like to deploy this program in headless-linux environment (e.g. HPC cluster), you must obtain a stardard license from ESRI and proper extensions.
The package is not extensively tested. Bug reports and contributes are extremely welcome.


## WARNING! WARNING! WARNING!
THIS PACKAGE WILL FAITHFULLY EXECUTE ANY PYTHON SCRIPTS PASSED TO IT. BAD GUYS CAN COMPLETELY CONTROL YOUR SYSTEM USING EXPOSED LOCAL SERVER INSTANCE. PLEASE ENSURE YOUR WORKING ENVIRONMENT IS COMPLETELY SAFE.

## How it works:
*TODO*

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
- Passing arc4nix.env to arcpy.env on local server is not supported. You need manually set environments in "predefined block". WIP
- It it not possible to retrieve any vector dataset from "in_memory" workspace
- `Geometry`, `SpatialReferece`, `Extent` classes are not supported now. Implementation is planning.
- `arcpy.da` package is not supported. Implementation is nearly impossible. There is no benefits to CRUD geospatial data locally using `arcpy.da`. Please use [gdal/ogr] instead.

## License
arc4nix is licensed under GPLv3 with ESRI software excpetion. 

Copyright (C) 2016 Tropical Rainfall Research Group, Department of Geography, University of Florida

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses>.

Linking arc4nix statically or dynamically with other modules is making a combined work based on arc4nix. Thus, the terms and conditions of the GNU General Public License cover the whole combination.

In addition, as a special exception, the copyright holders of arc4nix give you permission to combine [name of your program] with free software programs or libraries that are released under the GNU LGPL and with code included in the standard release of ESRI licensed software under the your ESRI agreements (or modified versions of such code, with unchanged license). You may copy and distribute such a system following the terms of the GNU GPL for arc4nix and the licenses of the other code concerned{, provided that you include the source code of that other code when and as the GNU GPL requires distribution of source code}.

Note that people who make modified versions of arc4nix are not obligated to grant this special exception for their modified versions; it is their choice whether to do so. The GNU General Public License gives permission to release a modified version without this exception; this exception also makes it possible to release a modified version which carries forward this exception.