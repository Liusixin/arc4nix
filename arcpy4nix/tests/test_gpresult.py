import unittest
import arcpy
from arcpy4nix.exec_file import dump_gpresult
from arcpy4nix.result import Result


class GpResultTestCase(unittest.TestCase):

    def test_gpresult_dummy(self):
        arcpy.env.workspace = "in_memory"
        arcpy.env.overwriteOutput = True
        r = arcpy.CreateRandomPoints_management(out_path="in_memory", out_name="Guwu2",
                                                constraining_feature_class="#", constraining_extent="0 0 250 250",
                                                number_of_points_or_field="100", minimum_allowed_distance="0 Unknown",
                                                create_multipoint_output="POINT", multipoint_size="0")
        g = dump_gpresult(r)
        R = Result(g)
        self.assertEqual(r.outputCount, R.outputCount)
        self.assertEqual(r.inputCount, R.inputCount)
        # The output is the most important thing to ensure equality.
        self.assertListEqual([r.getOutput(i) for i in range(r.outputCount)],
                             [R.getOutput(i) for i in range(r.outputCount)])


if __name__ == '__main__':
    unittest.main()
