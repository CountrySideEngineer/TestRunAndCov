import subprocess
from subprocess import PIPE
import xml.etree.ElementTree as ET
import LoadTargets
import HtmlReportGenerator

def RunProcess(testrunner, coverage, reportgene, targets):
    """RunProcess
        Run a process to execute test and get coverage of the test.

    Args:
        testrunner (string) : Path to application to run the test.
        coverage (string) : Path to application to calculate coverage of the test.
        reportgene (string) : Path to application to generate report of coverage in HTML format.
        targets (list) : List of target of test.

    Returns :
        List of path to XML files the resutl of this process is set.
    """
    resultXmls = list()
    for target in targets:
        logFileName = target.name + ".xml"
        runTestCode = [coverage, \
            "-register:user", \
            "-target:" + testrunner,\
            "-targetargs:" + target.name + "." + target.testType + " /logger:trx;LogFileName=" + logFileName, \
            "-output:" + target.name + ".xml", \
            "-targetdir:" + target.path, \
            ]
        subprocess.run(runTestCode, shell=True)

        reportGenCode = [reportgene, \
            "-reports:" + target.name + ".xml", \
            "-targetdir:.//html//coverage//" + target.name]
        subprocess.run(reportGenCode, shell=True)

        resultXml = target.path + "/TestResults/" + logFileName
        resultXmls.append(resultXml)

    return resultXmls

if __name__ == '__main__':

    #設定ファイルの読み込み
    configFileName = ".\\TestAutoRun_config.xml"
    config_tree = ET.parse(configFileName)
    config_root = config_tree.getroot()
    unittest_tools = config_root.find("Tools")
    unittest_runner_tag = config_root.find(".//Runner")
    unittest_coverage_tag = config_root.find(".//Coverage")
    unittest_reportgen_tag = config_root.find(".//ReportGenerator")

    unittest_runner = \
        unittest_runner_tag.attrib["path"] + unittest_runner_tag.attrib["name"]
    unittest_coverage = \
        unittest_coverage_tag.attrib["path"] + unittest_coverage_tag.attrib["name"]
    unit_test_report_gen = \
        unittest_reportgen_tag.attrib["path"] + unittest_reportgen_tag.attrib["name"]

    targets = LoadTargets.LoadTargetsFromConfig(configFileName)

    testResultXmls = RunProcess(unittest_runner, unittest_coverage, unit_test_report_gen, targets)

    HtmlReportGenerator.GenerateSummaryIndexHtml(testResultXmls)
    HtmlReportGenerator.GenerateResultIndexHtml(testResultXmls)