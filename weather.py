import junit.framework.Test;
import junit.framework.TestSuite;

public class Weather {

  public static Test suite() {
    TestSuite suite = new TestSuite();
    suite.addTestSuite(weather.selenium-ide.class);
    suite.addTestSuite(Untitled 3.class);
    return suite;
  }

  public static void main(String[] args) {
    junit.textui.TestRunner.run(suite());
  }
}
