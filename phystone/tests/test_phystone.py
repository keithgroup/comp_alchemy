"""
Unit and regression test for the phystone package.
"""

# Import package, test suite, and other packages as needed
from phystone import transmutations
import pytest
import sys

def test_phystone_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "phystone" in sys.modules

#Tests for transmutations.py
from ase import Atom, Atoms
from ase.build import fcc111, add_adsorbate
from ase.visualize import view

slab = fcc111('Cu', size=(2, 2, 4), vacuum=10.0)
transmute, counter = transmutations.index_transmuted(slab, 'Cu', 'Cu',
                                                              8, 1)
new_atom = Atom('Zn')
transmuted_slab = transmutations.transmuter(slab, transmute,
                                                     [new_atom]*len(transmute))

symmetric_slab = fcc111('Cu', size=(2, 2, 8), vacuum=10.0, orthogonal=True)
symmetric_transmute, symmetric_counter = transmutations.index_transmuted(
    slab,'Cu', 'Cu', 8, 1, symmetric=True)

symmetric_transmute