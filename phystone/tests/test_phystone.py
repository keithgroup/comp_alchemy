"""
Unit and regression test for the phystone package.
"""

# Import package, test suite, and other packages as needed
import phystone
import pytest
import sys

def test_phystone_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "phystone" in sys.modules
