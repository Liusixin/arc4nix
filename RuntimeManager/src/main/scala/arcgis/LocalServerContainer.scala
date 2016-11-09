package arcgis

import java.awt.{Container, EventQueue, Window}
import java.io.IOException
import javax.swing.{JButton, JDialog}

import akka.actor.Actor
import akka.event.Logging
import com.esri.client.local._
import com.esri.core.runtime.LicenseLevel
import com.esri.runtime.ArcGISRuntime
import main.GeoprocessingApp
import org.apache.http.HttpStatus
import org.apache.http.client.ResponseHandler
import org.apache.http.impl.client.DefaultHttpClient
import org.apache.http.client.methods.HttpGet

import scala.collection.JavaConversions._

/*
 * Currently, we could only start one local server PER NODE
 * We're working on start one local server PER CPU with actor model, but haven't finished yet
 */
class LocalServerContainer extends Actor{

  private var gpkPath: String = _

  private var _remote = false

  private val log = Logging.getLogger(context.system, this)

  def isUsingArcServer: Boolean = {
    if(_remote) {
      // If use remote, make sure local server is down
      assert(!server.isInitialized, "Local server is up, but we're using remote server. CHECK!")
    } else {
      assert(server.isInitialized, "Local server is down, but we're going to use it. CHECK!")
    }
    _remote
  }

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
      // Write out a CMD to tell python start to send commands
      val ac = context.actorSelection("/user/MainApp")
      ac ! GeoprocessingApp.messageUrl(event.getUrl)
      ac ! "[CMD]Service"
    }
  })


  // Workaround Developer license
  private def getButton(container: Container, text: String): JButton = {
    for(c <- container.getComponents) {
      println(c)
      c match {
        case p:JButton =>
          println(p.getText)
          if (p.getText == "OK") {
            return p
          }
        case p: Container =>
          val q = getButton(p, text)
          if(q != null) {
            return q
          }
        case _@p => println(p.toString)
      }
    }
    null
  }

  private def waitForDialog(title: String) : JDialog = {
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

  // Start server functions
  private def startDeveloperAutoClick(): Unit = {

    EventQueue.invokeLater(new Runnable {
      override def run(): Unit = server.initializeAsync() })

    val win = waitForDialog("ArcGIS Runtime")
    do {
      Thread.sleep(500)
      win.setVisible(true)
    } while (!win.isActive)
    var btn: JButton = null
    var counter = 0
    do {
      btn = getButton(win, "OK")
      if (btn == null) {
        Thread.sleep(250)
        counter += 1
        if (counter > 20)
          throw new NullPointerException("nya?!")
      }
      else
        btn.doClick()
    } while (btn == null)

  }


  private def startNormal(): Unit = {
    server.initializeAsync()
  }

  // Start the server, if it is the developer license, let's workaround it. We have no choice to keep compatibility on
  // headless Linux machines.
  private def startServerInternal(gpkPath: String): Unit = {
    // Pass this value so the event listener can use it.
    this.gpkPath = gpkPath
    // If server is initialized, return service url
    if(server.isInitialized) {
      context.actorSelection("/user/MainApp") ! GeoprocessingApp.messageUrl(localGP.getUrlGeoprocessingService)
    } else { // Otherwise, start the server and service.
      if (ArcGISRuntime.License.getLicenseLevel == LicenseLevel.DEVELOPER) {
        startDeveloperAutoClick()
      } else {
        startNormal()
      }
    }
  }

  private def setRemoteServiceUrl(serviceUrl: String): Unit = {
    // Check if it is a valid service url
    try {
      val httpclient = new DefaultHttpClient()
      val get = new HttpGet(serviceUrl + "/Execute Script")
      val response = httpclient.execute(get)
      val statusCode = response.getStatusLine.getStatusCode
      if (statusCode != HttpStatus.SC_OK) {
        log.error("Wrong service URL. Service not set, still in local mode")
      }
      log.info("Using remote service, shutdown local services and server")
      if (server.isInitialized) {
          val sc = server.getServices
          sc.foreach(p => p.stop())
          server.shutdown()
      }
      this._remote = true
    } catch {
      case x: IOException => log.error("Maybe network fail, still using local services")
      case x: Exception => throw x
    }


    if(!serviceUrl.endsWith("Execute Script")) {
      log.error("Wrong ArcGIS server service url!")
      return
    }
    // We will shutdown the local server if we use a remote url
    if(server.isInitialized) {
      server.shutdownAsync() // Shutdown server, if started!
      _remote = true
    }
    context.actorSelection("/user/MainApp") ! GeoprocessingApp.messageUrl(serviceUrl)
  }

  override def receive: Receive = {

    case LocalServerContainer.start(gpkPath: String) =>
      this.startServerInternal(gpkPath)
    case LocalServerContainer.setService(serviceUrl: String) =>
      this.setRemoteServiceUrl(serviceUrl)
    case LocalServerContainer.exit =>
      server.shutdown()
      context.system.shutdown()
    case _@x =>
      println(s"Unhandled command ${x}")

  }

}

object LocalServerContainer {
  case class start(gpkPath: String)
  case class setService(serviceUrl: String)
  case class execute(input: String, script: String, output: String)
  case class result(output: String)
  case object exit
}

