"""
Python module for calculating alchemical derivatives for transmuted systems.
"""
#!/bin/env python
from numpy import dot, zeros

def calc_alc_deriv(transmute, counter, espdiffs, charge):
    """
    Calculates the alchemical derivative for a transmuted system (see `transmutations.py`).

    This function must take an array of electrostatic potential differences (`espdiffs`). Then an
    array of nuclear charge differences equal in length to `espdiffs` is made. Every element in this
    array is a zero except for those at indexes that match those supplied in `transmute` and
    `counter.` This function takes a dot product of these two arrays to calculate the alchemical
    derivative.

    Parameters
    ----------
    transmute : List of indexes of atoms transmuted (see `transmutations.index_transmuted()`).

    counter : List of indexes of atoms counter transmuted (see `transmutations.index_transmuted()`).

    espdiffs : List of electrostatic potential differences (see `elec_stat_pot.espdiff()`).

    charge : Integer change in nuclear charge for transmuted atoms.

    Returns
    -------
    delta_nuc_charges : Array of nuclear charge differences for transmuted and counter transmuted
        atoms. Elements at indexes where atoms were transmuted equal `charge`. Elements at indexes
        where atoms were counter transmuted equal -`charge`. All other elements equal zero.

    alc_deriv : Float. Alchemical derivative that is the result of taking the dot product between
        `espdiffs` and `delta_nuc_charges`.
    """
    transmute_charges = [charge for i in range(len(transmute))]
    counter_charges = [-charge for j in range(len(counter))]

    delta_nuc_charges = zeros(len(espdiffs))

    for k, transmute_dex in enumerate(transmute):
        delta_nuc_charges[transmute_dex] = transmute_charges[k]

    for l, counter_dex in enumerate(counter):
        delta_nuc_charges[counter_dex] = counter_charges[l]

    alc_deriv = dot(espdiffs, delta_nuc_charges)

    return [delta_nuc_charges, alc_deriv]
