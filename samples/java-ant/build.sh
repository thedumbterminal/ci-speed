ANT_VERSION="1.10.12"
JUNIT_VERSION="1.8.2"
mkdir -p downloads lib
curl "https://dlcdn.apache.org//ant/binaries/apache-ant-$ANT_VERSION-bin.tar.gz" -o downloads/ant.tar.gz
tar xvfz downloads/ant.tar.gz -C downloads/
export PATH=$PATH:"downloads/apache-ant-$ANT_VERSION/bin"
curl "https://repo1.maven.org/maven2/org/junit/platform/junit-platform-console-standalone/$JUNIT_VERSION/junit-platform-console-standalone-$JUNIT_VERSION.jar" -o lib/junit.jar
ant test