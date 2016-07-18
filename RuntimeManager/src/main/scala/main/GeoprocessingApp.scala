package main

import java.io.{ByteArrayOutputStream, File}
import java.nio.charset.Charset
import java.util

import akka.actor.{Actor, ActorSystem, Props}
import akka.event.Logging
import arcgis.LocalServerContainer
import com.esri.core.tasks.ags.geoprocessing._
import com.esri.runtime.ArcGISRuntime
import org.apache.commons.codec.binary.Base64
import org.apache.commons.compress.compressors.gzip.GzipCompressorOutputStream

import scala.io.Source

/**
  * Created by sugar on 12/26/15.
  */

class GeoprocessingApp(val gpkPath: String) extends Actor {

  var geoprocessingUrl: String = _

  val log = Logging.getLogger(context.system, this)

  override def receive: Receive = {

    // If a string is received, it is a command
    case x: String =>
      x match {
        case "shutdown" =>
          context.system.actorSelection("/user/LocalServerInstance") ! LocalServerContainer.exit
        case "exit" =>
          System.exit(0)
        case "start" =>
          context.system.actorSelection("/user/LocalServerInstance") ! LocalServerContainer.start(gpkPath)
        case s if s.startsWith("start ") =>
          val r = s.split(' ')
          // If the input is empty. Let us forget about it.
          if(r(1).trim.isEmpty || !new File(r(1)).exists()) {
            log.error("Cannot start an empty or non-existed package");
          } else
            context.system.actorSelection("/user/LocalServerInstance") ! LocalServerContainer.start(r(1))
        case s if s.startsWith("execute ") => // We put a " " here to ensure execute will be a complete command
          val r = s.split(' ')
          println(GeoprocessingApp.execute(r(1), r(2), r(3)))
          self ! GeoprocessingApp.execute(r(1), r(2), r(3))
        case _@s =>
          println(s"[MESSAGE]$s")
      }

    case GeoprocessingApp.execute(input: String, block: String, script: String) =>
      if (geoprocessingUrl != null) {
        val gp = new Geoprocessor(geoprocessingUrl + "/Execute Script")
        val globalVariables = new GPString("GlobalVars")
        globalVariables.setValue(input)
        val predefinedBlock = new GPString("PreBlock")
        predefinedBlock.setValue(block)
        val scriptBody = new GPString("ScriptBody")
        scriptBody.setValue(script)
        val parameters = new util.ArrayList[GPParameter]()
        parameters.add(globalVariables)
        parameters.add(scriptBody)

        gp.submitJobAndGetResultsAsync(parameters, Array("Result"), null, new GPJobResultCallbackListener {
          override def onError(throwable: Throwable): Unit = {
            Console.err.println(throwable.getMessage)
          }

          override def onCallback(gpJobResource: GPJobResource, gpParameters: Array[GPParameter]): Unit = {
            // Well actually we have no results to return....
            val result = gpParameters(0).asInstanceOf[GPString]
            println(result.getValue)
            log.info(gpJobResource.getMessages.map(p => p.getDescription).mkString("\n"))
          }
        })
      } else {
        log.error("Service is not ready. Try again later!")
      }

    case GeoprocessingApp.messageUrl(url: String) => {
      log.info(s"service is at $url")
      geoprocessingUrl = url
    }



  }

}


object GeoprocessingApp {

  case class messageUrl(url: String)

  case class execute(input: String, block: String, script: String)

  def encode(inputString: String, compressed: Boolean): String = {
    if (!compressed) {
      return new String(Base64.encodeBase64(inputString.getBytes(Charset.forName("UTF-8"))))
    }
    val r = new ByteArrayOutputStream()
    val b = new GzipCompressorOutputStream(r)
    b.write(inputString.getBytes(Charset.forName("UTF-8")))
    b.flush()
    b.finish()
    val s = r.toByteArray
    r.flush()
    val t = Base64.encodeBase64(s)
    b.close()
    r.close()
    new String(t)
  }

  def encodeInputParameterFile(inputVariablesPath: String): String = {
    val inputSource = Source.fromFile(inputVariablesPath)
    val encoded_input_args = inputSource.getLines.map(line => {
      val name_value_tuple = line.trim.split('=')
      val var_name = name_value_tuple(0)
      val r = name_value_tuple(1).split('|')
      val isPath = r(0).toLowerCase
      val var_value_raw = r(1)
      val var_value_encoded = GeoprocessingApp.encode(var_value_raw, true)
      s"$var_name<-$isPath|zlib+b64|$var_value_encoded"
    })
    encoded_input_args.mkString(";")
  }

  def main(args: Array[String]) {

    ArcGISRuntime.initialize()

    val system = ActorSystem("LocalGP")
    val app = system.actorOf(Props(new GeoprocessingApp(args(0))), "MainApp")
    val server = system.actorOf(Props[LocalServerContainer], "LocalServerInstance")

    while (!system.isTerminated) {
      app ! readLine()
    }
  }

}
