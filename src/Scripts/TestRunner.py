#!/usr/bin/env python
import os
import unittest

import sys
import libs.LoggingUtils


def __runTests(suite, reportTitle="report"):
    from Test import setConfigurationFilesForTest
    from Test.HTMLTestRunner import HTMLTestRunner
    from libs.PathsManager import PathsManager
    setConfigurationFilesForTest.run()
    reportPath = PathsManager.RES_PATH + os.sep + reportTitle + '.html'
    runner = HTMLTestRunner(stream=file(reportPath, 'wb'), title=" Web2Board " + reportTitle, verbosity=1)
    # runner = unittest.TextTestRunner(verbosity=1)
    runner.run(suite)


def runUnitTests():
    from Test.unit.Updaters.testUpdater import TestUpdater
    from Test.unit.Updaters.testWeb2boardUpdater import TestWeb2boardUpdater
    from Test.unit.WSCommunication.Hubs.testCodeHub import TestCodeHub
    from Test.unit.WSCommunication.Hubs.testSerialMonitorHub import TestSerialMonitorHub
    from Test.unit.WSCommunication.Hubs.testVersionsHandlerHub import TestVersionsHandlerHub
    from Test.unit.testConfig import TestConfig
    from Test.unit.testDownloader import TestDownloader
    from Test.unit.testUtils import TestUtils

    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestUpdater))
    suite.addTests(unittest.makeSuite(TestWeb2boardUpdater))
    suite.addTests(unittest.makeSuite(TestCodeHub))
    suite.addTests(unittest.makeSuite(TestSerialMonitorHub))
    suite.addTests(unittest.makeSuite(TestVersionsHandlerHub))
    suite.addTests(unittest.makeSuite(TestConfig))
    suite.addTests(unittest.makeSuite(TestDownloader))
    suite.addTests(unittest.makeSuite(TestUtils))
    __runTests(suite, "unitTestReport")


def runIntegrationTests():
    from Test.integration.testCompilerUploader import TestCompilerUploader
    from Test.integration.testUtils import TestUtils
    from Test.integration.Updaters.testBitbloqLibsUpdater import TestBitbloqLibsUpdater
    from Test.integration.testSerialConnection import TestSerialConnection
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestCompilerUploader))
    suite.addTests(unittest.makeSuite(TestUtils))
    suite.addTests(unittest.makeSuite(TestBitbloqLibsUpdater))
    suite.addTests(unittest.makeSuite(TestSerialConnection))
    __runTests(suite, "integrationTestReport")


def runAllTests():
    runUnitTests()
    runIntegrationTests()


if __name__ == '__main__':
    log = libs.LoggingUtils.init_logging(__name__)
    if len(sys.argv) > 1:
        testing = sys.argv[1]
    else:
        testing = ""
    if testing == "unit":
        runUnitTests()
    elif testing == "integration":
        runIntegrationTests()
    elif testing == "all":
        runAllTests()
    # log.warning("exiting program...")
    os._exit(1)
