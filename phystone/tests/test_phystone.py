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
from ase import Atom
from ase.build import fcc111
from ase.visualize import view

slab = fcc111('Cu', size=(2, 2, 4), vacuum=10.0)
#view(slab)

symmetric_slab_odd = fcc111('Cu', size=(2, 2, 9), vacuum=10.0, orthogonal=True)
#view(symmetric_slab_odd)
symmetric_slab_even = fcc111('Cu', size=(2, 2, 8), vacuum=10.0, orthogonal=True)
#view(symmetric_slab_even)
print(symmetric_slab_even.get_center_of_mass())

new_atom_1 = Atom('Zn')

new_atom_2 = Atom('Ni')

def test_index_transmuted():

    expected_transmute = [12, 13, 14, 15, 8, 9, 10, 11]

    expected_counter = [0, 1, 2, 3]

    transmute, counter = phystone.transmutations.index_transmuted(slab,
                                                                  'Cu',
                                                                  'Cu', 8, 4)

    assert (expected_transmute == transmute and
            expected_counter == counter)


def test_index_transmuted_with_symmetric():

    expected_even_transmute = [28, 29, 30, 31, 24, 25, 26, 27, 0, 1, 2, 3, 4, 5, 6, 7]

    expected_even_counter = [12, 13, 14, 15, 16, 17, 18, 19]

    even_symmetric_transmute, even_symmetric_counter = phystone.transmutations.index_transmuted(
        symmetric_slab_even,'Cu', 'Cu', 8, 4, symmetric=True)

    assert (expected_even_transmute == even_symmetric_transmute and
            expected_even_counter == even_symmetric_counter)

    expected_odd_transmute = [32, 33, 34, 35, 28, 29, 30, 31, 0, 1, 2, 3, 4, 5, 6, 7]

    expected_odd_counter = [16, 17, 18, 19]

    odd_symmetric_transmute, odd_symmetric_counter = phystone.transmutations.index_transmuted(
        symmetric_slab_odd,'Cu', 'Cu', 8, 4, symmetric=True)

    assert (expected_odd_transmute == odd_symmetric_transmute and
            expected_odd_counter == odd_symmetric_counter)

def test_transmuter():

    transmute, counter = phystone.transmutations.index_transmuted(slab,
                                                                  'Cu',
                                                                  'Cu', 8, 4)

    transmuted_slab = phystone.transmutations.transmuter(slab, [transmute[0],counter[0]],
                                                     [new_atom_1,new_atom_2])

    assert (transmuted_slab[transmute[0]].number - transmuted_slab[transmute[1]].number == 1 and
            transmuted_slab[counter[1]].number - transmuted_slab[counter[0]].number == 1)

def test_transmuter_with_symmetric():

    transmute, counter = phystone.transmutations.index_transmuted(symmetric_slab_even,
                                                                  'Cu',
                                                                  'Cu', 8, 4, symmetric=True)

    transmuted_symmetric_slab = phystone.transmutations.transmuter(symmetric_slab_even,
                                                                   [transmute[0],counter[0]],
                                                                   [new_atom_1,new_atom_2])

    #view(transmuted_symmetric_slab)
    print(transmute)
