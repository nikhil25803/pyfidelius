from pyfidelius.requirement_check.requirement_check import RequirementCheck


def test_requirement_check_true():
    rcheck = RequirementCheck()
    assert rcheck.check() is True


def test_requirement_check_false():
    rcheck = RequirementCheck()
    assert rcheck.check() is False
