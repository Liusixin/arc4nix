import os

import arc4nix as arcpy


def relocate(old_path, new_folder, new_ext=None):
    """relocate file at ```old_path``` to ```new_folder``` and change its extension to ```new_ext```

    Parameters
    -----------------
    old_path: string
        old file path

    new_folder: string
        the folder new file will be stored

    new_ext: string
        the extension of new file will be replaced by ````new_ext````
    """
    ext = os.path.splitext(old_path)[-1]
    base = os.path.basename(old_path)
    if new_ext is None:
        return os.path.join(new_folder, base)
    else:
        # Add a "." in case forgotten
        return os.path.join(new_folder, base.replace(ext, new_ext if new_ext.startswith(".") else ".%s" % new_ext))


def list_folder_sorted_ext(folder=".", ext=None):
    if ext is not None:
        new_ext = ext if ext.startswith(".") else ".%s" % ext
        return sorted(filter(lambda p: p.endswith(ext), os.listdir(folder)))
    else:
        return sorted(os.listdir(folder))


pwd = "/home/sugar/Documents/TestData/ARWH_TiedtkeCu_WSM6/reflec_netcdf"
os.chdir(pwd)

cnt_folder = "/home/sugar/Documents/TestData/ARWH_TiedtkeCu_WSM6/reflec_netcdf/cnt"
cnt_polygon_folder = "/home/sugar/Documents/TestData/ARWH_TiedtkeCu_WSM6/reflec_netcdf/cnt_polygon"

arcpy.env.overwriteOutput = True
arcpy.env.workspace = "/home/sugar/Documents/TestData/ARWH_TiedtkeCu_WSM6/scratch"

for cntr in list_folder_sorted_ext(cnt_folder, ".shp"):

    print cntr

    in_cntr = os.path.join(pwd, cnt_folder, cntr)
    print in_cntr
    assert os.path.exists(in_cntr)

    out4 = relocate(cntr.replace(".shp", "_merge.shp").replace("-", "_"), cnt_polygon_folder)
    # if os.path.exists(out4):
    #    print "%s existed. Skip!" % out4
    #    continue

    # Maintain a list so we can easily merge them back
    fn_list = []
    temp_file = []

    for value in range(20, 45, 5):

        try:
            out1 = relocate(cntr.replace(".shp", "_%d.shp" % value).replace("-", "_"), arcpy.env.workspace)
            print out1

            arcpy.Select_analysis(in_cntr, out1, where_clause="CONTOUR=%d" % value)
            # temp_file.append(out1)
            #
            # out2 = out1.replace(".shp", "_p.shp")
            # arcpy.FeatureToPolygon_management(out1, out2)
            # arcpy.AddField_management(out2, "AREA1", field_type="DOUBLE")
            # arcpy.AddField_management(out2, "dBZ", field_type="DOUBLE")
            # arcpy.CalculateField_management(out2, "AREA1", "!shape.area!", "PYTHON")
            # arcpy.CalculateField_management(out2, "dBZ", "%d" % value, "PYTHON")
            # temp_file.append(out2)
            #
            # out3 = out2.replace("_p", "_l")
            # arcpy.Select_analysis(out2, out3, where_clause="AREA1>25000000")
            # temp_file.append(out3)
            # fn_list.append(out3)

        except Exception, ex:
            print ex.message
            continue

            # End of loop

    # print fn_list, "->", out4
    # arcpy.Merge_management(fn_list, out4)

    # map(arcpy.delete_management, temp_file)

    print "OK"

    break

print "Done"
