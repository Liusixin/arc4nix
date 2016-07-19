import arcpy4nix as arcpy

def gp_fixargs(args, strip_right_nones=False, string_results=True):
    """Adjusts arguments passed into a function to be arcgisscripting-friendly:
       pass in stringified result objects and unwrapped arc objects"""
    new_args = []
    for arg in args:
        if isinstance(arg, (tuple, list)):
            new_args.append(gp_fixargs(arg))
        else:
            new_args.append(arg)
        del arg
    if strip_right_nones:
        while new_args and new_args[-1] is None:
            new_args.pop()
    del args
    return new_args

#veg = "vegtype"
#suitableVeg = "/output/Output.gdb/suitable_vegetation"
#whereClause = "HABITAT = 1"
#arcpy.Select_analysis(veg, suitableVeg, whereClause, a=1, b="2", c=[3,"4"])

# Buffer areas of impact around major roads
roads = "majorrds"
roadsBuffer = "/output/Output.gdb/buffer_output"
distanceField = "Distance"
sideType = "FULL"
endType = "ROUND"
dissolveType = "LIST"
dissolveField = "Distance"
arcpy.Buffer_analysis(roads, roadsBuffer, distanceField, sideType, endType, dissolveType, dissolveField)

# Erase areas of impact around major roads from the suitable vegetation patches
eraseOutput = "/output/Output.gdb/suitable_vegetation_minus_roads"
xyTol = "1 Meters"
arcpy.Erase_analysis(suitableVeg, roadsBuffer, eraseOutput, xyTol)

# Union
inFeatures = [("/input/counties", 2),["/input/parcels", 1],["/input/state", 2]]
outFeatures = "state_landinfo" 
arcpy.Union_analysis (inFeatures, outFeatures)



# Union 2
inFeatures = ["/input/counties", "/input/parcels", ["/input/state", 2]]
outFeatures = "state_landinfo" 
arcpy.Union_analysis ("path:/something", in_features=inFeatures, out_feature=outFeatures)
