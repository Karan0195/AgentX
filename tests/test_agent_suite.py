"""
Pytest integration test suite for AgentX.
Verifies that benchmark pass rate exceeds 95% against pandas ground truth.
"""

import sys
import re
from pathlib import Path
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

def test_benchmark_pass_rate_exceeds_95_percent():
    """
    Verifies that the AgentX benchmark test suite pass rate exceeds 95% across all 8 datasets.
    """
    report_file = BASE_DIR / "tests" / "TEST_REPORT.md"
    assert report_file.exists(), "TEST_REPORT.md must exist."

    with open(report_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Match overall pass rate in executive summary
    m = re.search(r"Overall Pass Rate\*\* \| \*\*([\d\.]+)%\*\*", content)
    assert m is not None, "Could not find overall pass rate in TEST_REPORT.md"

    pass_rate = float(m.group(1))
    assert pass_rate >= 95.0, f"Expected pass rate >= 95%, but found {pass_rate}%"
