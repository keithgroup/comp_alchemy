"""
Unit and regression test for the comp_alchemy package.
"""

# Import package, test suite, and other packages as needed
#import comp_alchemy
import pytest
import sys

from phystone import transmutations

def test_comp_alchemy_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "comp_alchemy" in sys.modules

#transmutations.py test
from ase import Atoms
from ase.build import fcc111, add_adsorbate
from ase.visualize import view

slab = fcc111('Cu', size=(2, 2, 4), vacuum=10.0)
#view(slab)

h = 1.85
d = 1.10
molecule = Atoms('2N', positions=[(0., 0., 0.), (0., 0., d)])

ads = add_adsorbate(slab, molecule, h, 'ontop')