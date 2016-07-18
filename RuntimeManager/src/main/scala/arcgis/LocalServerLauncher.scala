package arcgis

import java.net.URLClassLoader

import akka.actor.Actor
import akka.actor.Actor.Receive
import com.esri.client.local._
import com.esri.core.tasks.ags.geoprocessing._


/**
 * Created by sugar on 5/23/15.
 */
class LocalServerLauncher extends Actor {

  val javaExec = Array(System.getProperty("java.home"), "bin", "java").mkString(System.getProperty("path.separator"))
  val classPath = Thread.currentThread().getContextClassLoader.asInstanceOf[URLClassLoader].getURLs.mkString(System.getProperty("path.separator"))

  val totalInstance = 1
  //Start server
  override def receive: Actor.Receive = {

    case LocalServerContainer.result(output: String) => ???

    case "start" => {

    }
  }
}



