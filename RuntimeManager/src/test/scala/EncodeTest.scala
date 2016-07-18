/**
  * Created by sugar on 12/29/15.
  */

import java.io.File

import main.GeoprocessingApp
import org.junit.Assert._
import org.junit.Test

import scala.io.Source


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
  def TestReadInput(): Unit = {
    val inputVariablePath = "/home/sugar/gpk_test/input.txt"
    println(GeoprocessingApp.encodeInputParameterFile(inputVariablePath))
  }

  @Test
  def TestReadScript(): Unit = {
    val script = "/home/sugar/gpk_test/script.txt"
    println(Source.fromFile(script).mkString)
  }

}
