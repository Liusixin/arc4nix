import os

import unittest
import arc4nix as arcpy


class GpFuncionGenTestCase(unittest.TestCase):
    def test_select(self):
        veg = "vegtype"
        suitableVeg = "/output/Output.gdb/suitable_vegetation"
        whereClause = "HABITAT = 1"
        arcpy.Select_analysis(veg, suitableVeg, whereClause, a=1, b="2", c=[3, "4"])

    def test_select_buffer_erase(self):
        veg = "vegtype"
        suitableVeg = "/output/Output.gdb/suitable_vegetation"
        whereClause = "HABITAT = 1"
        arcpy.Select_analysis(veg, suitableVeg, whereClause, a=1, b="2", c=[3, "4"])

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

    def test_union1(self):
        # Union with rank
        inFeatures = [("/input/counties", 2), ["../input/parcels", 1], ["./input/state", 2]]
        outFeatures = "state_landinfo"
        arcpy.Union_analysis(inFeatures, outFeatures)

    def test_union2(self):
        # Union 2 with partial rank
        inFeatures = ["/input/counties", "input/parcels", ["/input/state", 2]]
        outFeatures = "state_landinfo"
        arcpy.Union_analysis(inFeatures, out_feature=outFeatures)

    def test_union3(self):
        # Union with string list
        inFeatures = "'/input path/counties' #;'input/parcels' #;'/input path/state', 3"
        outFeatures = "state_landinfo"
        arcpy.Union_analysis(in_features=inFeatures, out_feature=outFeatures)


if __name__ == '__main__':
    unittest.main()
