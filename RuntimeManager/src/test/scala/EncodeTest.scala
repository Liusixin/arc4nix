/**
  * Created by sugar on 12/29/15.
  */

import main.GeoprocessingApp
import org.junit.Assert._
import org.junit.Test


class EncodeTest {

  @Test
  def TestEncode(): Unit = {
    val before = "/home/sugar/a.shp"
    val after = "H4sIAAAAAAAA/9PPyM9N1S8uTU8s0k/UK84oAAB/NrOuEQAAAA=="
    val result = GeoprocessingApp.encode(before, true)
    println(result.replace("\n", ""))
    assertTrue(result == after)
  }

  @Test
  def TestDecode(): Unit = {
    val before = "arcpy.env.workspace=\"c:/\""
    val after = GeoprocessingApp.decode("b64:" + GeoprocessingApp.encode(before, false))
    assertEquals(before, after)
  }

}
