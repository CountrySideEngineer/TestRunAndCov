
class TestResult:
    """TestResult
        Result of test.

    Attribute:
        outcome (string) : Result of test.
        testnaem (string) : Name of test.
        conputername (string) : Name of computer the test is run.
        starttime (string) : Date of time the test starts.
        endtime (string) : Date of time the test ends.
    """
    outcome = ""
    testname = ""
    computername = ""
    starttime = ""
    endtime = ""

    def __init__(self):
        """__init__
            Constructor.
        """
        super().__init__()

        self.outcome = ""
        self.testname = ""
        self.computername = ""
        self.starttime = ""
        self.endtime = ""

class TestSummary:
    """TestSummary
        Summary of test, the number of tests and the results.

    Attributes:
        name (string) : Name of test
        outcome (string) : Result of test.
        total (integer) : The total number of test.
        executed (integer) : The number ot test executed.
        passed (integer) : The number of test passed.
        failed (integer) : The number of test failed.
        error (integer) : IDK.
        ...
    """
    name = ""
    outcome = ""
    total = 0
    executed = 0
    passed = 0
    failed = 0
    error = 0
    timeout = 0
    aborted = 0
    inconclusive = 0
    passedButRunAborted = 0
    notRunnable = 0
    notExecuted = 0
    disconnected = 0
    warning = 0
    completed = 0
    pending = 0

    def __init__(self):
        """__init__
            Constructor.
        """
        super().__init__()
        self.name = ""
        self.outcome = ""
        self.total = 0
        self.executed = 0
        self.passed = 0
        self.failed = 0
        self.error = 0
        self.timeout = 0
        self.aborted = 0
        self.inconclusive = 0
        self.passedButRunAborted = 0
        self.notRunnable = 0
        self.notExecuted = 0
        self.disconnected = 0
        self.warning = 0
        self.completed = 0
        self.inProgress = 0
        self.pending = 0
