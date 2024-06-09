from pyfidelius.requirement_check import RequirementCheck


def test_check_jdk():
    req_check = RequirementCheck()
    assert req_check.check() == True


def test_check_os():
    req_check = RequirementCheck()
    assert req_check.identify_os() in ["linux", "windows", "mac"]
