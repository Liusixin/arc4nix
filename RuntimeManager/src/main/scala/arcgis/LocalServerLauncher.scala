package arcgis

import java.net.URLClassLoader

import akka.actor.Actor


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



