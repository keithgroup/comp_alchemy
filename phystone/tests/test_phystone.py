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

#Tests for transmutations.py
from ase import Atoms
from ase.build import fcc111, add_adsorbate
from ase.visualize import view

h = 1.85
d = 1.10

slab = fcc111('Cu', size=(2, 2, 4), vacuum=10.0)
#view(slab)

molecule = Atoms('2N', positions=[(0., 0., 0.), (0., 0., d)])

ads = slab.copy()
add_adsorbate(ads, molecule, h, 'ontop')
#view(ads)

transmutations.index_transmuted(slab, 'Cu', 'Cu', 8, 1)