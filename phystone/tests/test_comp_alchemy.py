"""
Unit and regression test for the comp_alchemy package.
"""

# Import package, test suite, and other packages as needed
import comp_alchemy
import pytest
import sys

def test_comp_alchemy_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "comp_alchemy" in sys.modules
