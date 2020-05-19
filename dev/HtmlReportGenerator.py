"""
    Convert resutls of unit tests int XML format to HTML.

"""
from operator import attrgetter
import xml.etree.ElementTree as ET
import TestResult
import ntpath
import os
import shutil

def GenerateSummaryIndexHtml(ResultXmlPaths):
    """GenerateSummaryIndexHtml
        Convert summary of unit tests in XML format into HTML

    Args:
        ResultXmlPaths (list):  List of XML file paths the result of unit test is set.

    """
    summaries = list()
    for ResultXmlPath in ResultXmlPaths:
        testSummary = XmlToSummary(ResultXmlPath)
        summaries.append(testSummary)

    html_data = CreateIndexHtml(summaries)

    dstdir = r'./html/'

    os.makedirs(dstdir, exist_ok=True)

    indexhtml = r'index.html'
    idnexhtmlpath = dstdir + indexhtml
    ToHtml(idnexhtmlpath, html_data)
    SetupStyleSheet(dstdir)

def XmlToSummary(ResultXmlPath):
    """XmlToSummary
        Convert XML to list fo TestResult class objects, the class is defined in TestResult module.

    Args:
        ResultXmlPath (list): Path to XML file the result of test is set.

    Returns:
        list:   List of TestResult class.

    """
    result_tree = ET.parse(ResultXmlPath)
    result_root = result_tree.getroot()
    result_summary = result_root.find(".//{http://microsoft.com/schemas/VisualStudio/TeamTest/2010}ResultSummary")
    result_counters = result_root.find(".//{http://microsoft.com/schemas/VisualStudio/TeamTest/2010}Counters")

    testSummary = TestResult.TestSummary()

    xmlfilename = ntpath.basename(ResultXmlPath)   #ファイル名取得
    xmlfilename_without_ext = ntpath.basename(xmlfilename).split('.', 1)[0]
    testSummary.name = xmlfilename_without_ext
    testSummary.outcome = result_summary.attrib["outcome"]
    testSummary.total = result_counters.attrib["total"]
    testSummary.executed = result_counters.attrib["executed"]
    testSummary.passed = result_counters.attrib["passed"]
    testSummary.failed = result_counters.attrib["failed"]
    testSummary.error = result_counters.attrib["error"]
    testSummary.timeout = result_counters.attrib["timeout"]
    testSummary.aborted = result_counters.attrib["aborted"]
    testSummary.inconclusive = result_counters.attrib["inconclusive"]
    testSummary.passedButRunAborted = result_counters.attrib["passedButRunAborted"]
    testSummary.notRunnable = result_counters.attrib["notRunnable"]
    testSummary.notExecuted = result_counters.attrib["notExecuted"]
    testSummary.disconnected = result_counters.attrib["disconnected"]
    testSummary.warning = result_counters.attrib["warning"]
    testSummary.completed = result_counters.attrib["inProgress"]
    testSummary.pending = result_counters.attrib["pending"]

    return testSummary

def CreateIndexHtml(summaries):
    """CreateIndexHtml
        Create HTML data of index.html file for root of result.

    Args:
        summaries (list):   List of TestSummary class.

    Returns:
        HTML text data of index.html 
    """
    html_data = '<html><body>\n'
    html_data += '<title>テスト結果</title>\n'
    html_data += '<link rel="stylesheet" type="text/css" href="stylesheet.css">\n'
    html_data += '<html><body>\n'
    html_data += '<div class="container"><div class="containerleft">\n'
    html_data += '<h1>テスト結果(概要)</h1>\n'
    html_data += '<table class="overview">\n'
    html_data += '<tr><th>テスト名</th><th>結果</th><th>合計</th><th>実行</th><th>成功</th><th>失敗</th></tr>\n'
    for summary in summaries:
        html_data += '<tr>\n'
        html_data += '<td class="left"><a href="./summary/' + summary.name + '/index.html">' + summary.name + '</a></td>\n'
        if summary.name == "Passed":
            outcome_classname = "resutl_passed"
        else:
            outcome_classname = "resutl_failed"
        html_data += '<td class="center column60 ' + outcome_classname + '">' + summary.outcome + '</td>\n'
        html_data += '<td class="right column60">' + summary.total + '</td>\n'
        html_data += '<td class="right column60">' + summary.executed + '</td>\n'
        html_data += '<td class="right column60">' + summary.passed + '</td>\n'
        html_data += '<td class="right column60">' + summary.failed + '</td>\n'
        html_data += '</tr>'
    html_data += '</table></div></div></body></html>\n'

    return html_data

def GenerateResultIndexHtml(ResultXmlPaths):
    """GenerateResultIndexHtml
        Create HTML data of index.html file for resutl each test.

    Args:
        ResultXmlPaths (list):  List of paths the result of test is set.

    """
    for ResultXmlPath in ResultXmlPaths:
        testresults = XmlToResult(ResultXmlPath)
        htmldata = CreateResultHtml(testresults)
        testname = ntpath.basename(ResultXmlPath).split('.', 1)[0]
        
        htmldir = r'./html/summary/' + testname + r'/'
        indexhtml = r'index.html'
        htmlpath = htmldir + indexhtml
        os.makedirs(htmldir, exist_ok=True)
        ToHtml(htmlpath, htmldata)
        SetupStyleSheet(htmldir)

def XmlToResult(ResultXmlPaths):
    """XmlToResult
        Convert XML file to list of TestResult classes.

    Args:
        ResultXmlPath (list): List of paths the result of test is set.

    Retuns:
        List of TestResult class in TestResult module.

    """
    result_tree = ET.parse(ResultXmlPaths)
    result_root = result_tree.getroot()
    unittestresults = result_root.findall(".//{http://microsoft.com/schemas/VisualStudio/TeamTest/2010}UnitTestResult")
    testResults = list()
    for unittestresult in unittestresults:
        testResult = TestResult.TestResult()
        testResult.testname = unittestresult.attrib["testName"]
        testResult.outcome = unittestresult.attrib["outcome"]
        testResult.computernmae = unittestresult.attrib["computerName"]
        testResult.starttime = unittestresult.attrib["startTime"]
        testResult.endtime = unittestresult.attrib["endTime"]
        testResults.append(testResult)

    testresults_sorted = sorted(testResults, key=attrgetter("testname"))
    return testresults_sorted

def CreateResultHtml(results):
    """CreateResultHtml
        Create HTML data to show result of each test case in a test in table format.

    Args:
        result (list): HTML data for index.html of result of test.
    """
    html_data = '<html><body>\n'
    html_data += '<title>テスト結果</title>\n'
    html_data += '<link rel="stylesheet" type="text/css" href="stylesheet.css">\n'
    html_data += '<div class="container"><div class="containerleft">\n'
    html_data += '<h1>テスト結果(内訳)</h1>\n'
    html_data += '<table class="overview">\n'
    html_data += '<tr><th>テスト名</th><th>結果</th><th>実行日時</th>\n'
    for result in results:
        html_data += '<tr>\n'
        html_data += '<td class="left columnAuto">' + result.testname + '</td>\n'
        if result.outcome == "Passed":
            html_data += '<td class="resutl_passed center column60">OK</td>\n'
        else:
            html_data += '<td class="resutl_failed center column60">NG</td>\n'

        html_data += '<td class="center column160">' + result.starttime[:10] + '</td>\n'
        html_data += '</tr>\n'
    
    html_data += '</table></div></div></body></html>\n'

    return html_data

def ToHtml(htmlpath, htmldata):
    """ToHtml
        Write data, htmldata, into a file, htmlpath.

    Args:
        htmlpath (string) : Path to HTML file the htmldata to be written into.
        htmldata (string) : Text data to be written into the file. htmlpath.
    """
    with open(htmlpath, mode='w', encoding="utf-8") as f:
        f.write(htmldata)

def SetupStyleSheet(stylesheetdir):
    """SetupStyleSheet
        Copy style sheet file from template directory to target one.

    Args:
        stylesheetdir (string) : Path to directory to the style sheet template should be copied.

    """
    stylesheetname = 'stylesheet.css'
    stylesheetsrc = './template/' + stylesheetname
    stylesheetdst = stylesheetdir + stylesheetname
    if os.path.isfile(stylesheetsrc):
        #スタイルシートが存在した場合のみコピー実施
        shutil.copyfile(stylesheetsrc, stylesheetdst)

if __name__ == '__main__':
    print("HtmlReportGenerator.py.py")
    #resultxmlpath = \
    #    ["E:\\development\\CStubMk\\dev\\dev\\UnitTest_Param\\bin\\Debug\\netcoreapp3.0\\TestResults\\UnitTest_Param.xml"]
    #    r"E:\development\CStubMk\dev\dev\UnitTest_StubHeaderFile\bin\Debug\netcoreapp3.0\TestResults\UnitTest_StubHeaderFile.xml"]
    #GenerateSummaryIndexHtml(resultxmlpath)
    #GenerateResultIndexHtml(resultxmlpath)
