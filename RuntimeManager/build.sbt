import sbtassembly.MergeStrategy

name := "RuntimeManager"

version := "1.0"

scalaVersion := "2.10.5"

libraryDependencies ++= Seq(
  "com.typesafe.akka" % "akka-actor_2.10" % "2.3.13",
  "com.github.nscala-time" %% "nscala-time" % "2.0.0",
  "org.apache.commons" % "commons-compress" % "1.10",
  // "commons-codec" % "commons-codec" % "1.10",
  "junit" % "junit" % "4.12" % Test
)

target in assembly := file("../arc4nix/arc4nix/data/")

assemblyMergeStrategy in assembly := {
  case PathList(ps @ _*) if ps.last.endsWith("LicenseLevel.class") || ps.last.endsWith("LicenseResult.class") => MergeStrategy.first
  case x =>
    val oldStrategy = (assemblyMergeStrategy in assembly).value
    oldStrategy(x)
}