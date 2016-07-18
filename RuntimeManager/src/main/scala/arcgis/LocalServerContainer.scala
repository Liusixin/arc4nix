/**
  * Created by sugar on 5/23/15.
  * License MIT.
  */

package arcgis

import java.awt.{Container, EventQueue, Window}
import javax.swing.{JButton, JDialog}

import akka.actor.Actor
import com.esri.client.local._
import com.esri.core.runtime.LicenseLevel
import com.esri.runtime.ArcGISRuntime
import main.GeoprocessingApp

/*
 * Currently, we could only start one local server PER NODE
 * We're working on start one local server PER CPU with actor model, but haven't finished yet
 */
class LocalServerContainer extends Actor{

  private var gpkPath: String = _

  val server = LocalServer.getInstance()
  // Add server listener
  server.addServerLifetimeListener(new ServerLifetimeListener {

    override def serverLifetimeShutdown(event: ServerLifetimeEvent): Unit = {
    }

    override def serverLifetimeInitialized(event: ServerLifetimeEvent): Unit = {
      // Immediately start gpk after server started.
      localGP.setServiceType(GPServiceType.SUBMIT_JOB)
      localGP.setPath(gpkPath)
      localGP.startAsync()
    }

  })

  val localGP = new LocalGeoprocessingService()
  // Add service listener
  localGP.addLocalServiceStartCompleteListener(new LocalServiceStartCompleteListener {
    override def localServiceStartComplete(event: LocalServiceStartCompleteEvent): Unit = {
      context.actorSelection("/user/MainApp") ! GeoprocessingApp.messageUrl(event.getUrl)
    }
  })

  // Start server functions
  private def startDeveloperAutoClick(): Unit = {
    def getButton(container: Container, text: String): JButton = {
      for(c <- container.getComponents) {
        // println(c)
        c match {
          case p:JButton =>
            // println(p.getText)
            if (p.getText == "OK") {
              return p
            }
          case p: Container => {
            val q = getButton(p, text)
            if(q != null) {
              return q
            }
          }
          case _@p => println(p.toString)
        }
      }
      null
    }
    def waitForDialog(title: String) : JDialog = {
      var win: JDialog = null
      do {
        val p = Window.getWindows.find(p => p.isInstanceOf[JDialog])
        if(p.isEmpty) {
          Thread.sleep(250)
        } else {
          win = p.get.asInstanceOf[JDialog]
          println(win.getTitle)
        }
      } while (win == null)
      win
    }
    EventQueue.invokeLater(new Runnable {
      override def run(): Unit = server.initializeAsync() })
    val win = waitForDialog("ArcGIS Runtime")
    do {
      Thread.sleep(5000)
      win.setVisible(true)
    } while (!win.isActive)
    var btn: JButton = null
    var counter = 0
    do {
      btn = getButton(win, "OK")
      if (btn == null) {
        Thread.sleep(250)
        counter += 1
        if(counter > 20)
          throw new NullPointerException("nya?!")
        else
          btn.doClick()
      }
    } while (btn == null)
  }
  private def startNormal(): Unit = {
    server.initializeAsync()
  }

  /*
   * Start the server, if it is the developer license, let's workaround it. We have no choice to keep compatibility on
   * headless Linux machines.
   */
  private def startServerInternal(gpkPath: String): Unit = {
    // Pass this value so the event listener can use it.
    this.gpkPath = gpkPath
    // If server is initialized, return service url
    if(server.isInitialized) {
      context.actorSelection("/user/MainApp") ! GeoprocessingApp.messageUrl(localGP.getUrlGeoprocessingService)
    } else { // Otherwise, start the service and service.
      if (ArcGISRuntime.License.getLicenseLevel == LicenseLevel.DEVELOPER) {
        startDeveloperAutoClick()
      } else {
        startNormal()
      }
    }
  }

  override def receive: Receive = {

    case LocalServerContainer.start(gpkPath: String) =>
      this.startServerInternal(gpkPath)
    case LocalServerContainer.exit =>
      server.shutdown()
      context.system.shutdown()
    case _@x =>
      println(s"Unhandled command ${x}")

  }

}

object LocalServerContainer {
  case class start(gpkPath: String)
  case class execute(input: String, script: String, output: String)
  case class result(output: String)
  case object exit
}

