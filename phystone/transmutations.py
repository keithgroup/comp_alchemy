"""Module for making alchemical transmutations to surface slab models.
"""
#!/usr/bin/env python
from numpy import isclose
from ase import Atom
from phystone.find_pairs import find_symmetric_pairs

def index_transmuted(slab, transmute_atom_sym, counter_atom_sym,
                     transmute_num, counter_num, symmetric=False):
    """
    Identifies the indexes of atoms in slab to be transmuted at the top of the surface according
    to a given chemical symbol (transmute_atom_sym) and finds indexes of atoms to be counter
    transmuted at the bottom of the surface according to a given chemical symbol
    (counter_atom_sym).

    Parameters
    ----------
    slab : An atoms object from ASE.

    transmute_atom_sym : String. Chemical symbol for the target atom in slab to be transmuted.

    counter_atom_sym : String. Chemical symbol for the target atom in slab to be counter
        transmuted.

    transmute_num : Integer. Number of atoms to be transmuted in slab.

    counter_num : Integer. Number of atoms to be counter transmuted in slab.

    symmetric (default: False): Boolean. Indicates if using a symmetric slab.

    Returns
    -------
    transmute : List of indexes of atoms to be transmuted.

    counter : List of indexes of atoms to be counter transmuted.
    """

    #Dictionary of all metal atoms in the surface
    transmute_atom = {}
    counter_atom = {}

    for slab_atom in slab:

        #Identifying metal atoms
        if slab_atom.symbol == transmute_atom_sym:

            transmute_atom[str(slab_atom.index)] = slab_atom.position[2]

        if slab_atom.symbol == counter_atom_sym:

            counter_atom[str(slab_atom.index)] = slab_atom.position[2]

    #List of atom indexes transmuted at surface
    #List of atom indexes counter transmuted far from surface
    transmute = []
    counter = []

    if symmetric:

        transmute_top = []

        transmute_bottom = []

        counter_above = []

        counter_below = []

        for i in range(0, transmute_num):

            topmax = max(transmute_atom, key=transmute_atom.get)
            transmute_top.append(int(topmax))
            del transmute_atom[topmax]

        for j in range(0, transmute_num):

            botmin = min(transmute_atom, key=transmute_atom.get)
            transmute_bottom.append(int(botmin))
            del transmute_atom[botmin]

        center_of_mass = slab.get_center_of_mass()
        above_com = {}
        below_com = {}
        equal_to_com = {}

        for atom_index, atom_position in transmute_atom.items():

            if isclose([atom_position],[center_of_mass[2]]):

                equal_to_com[atom_index] = atom_position

            elif atom_position > center_of_mass[2]:

                above_com[atom_index] = atom_position

            elif atom_position < center_of_mass[2]:

                below_com[atom_index] = atom_position

        if equal_to_com:

            for k in range(0, counter_num):

                equal_max = max(equal_to_com, key=equal_to_com.get)
                counter.append(int(equal_max))
                del equal_to_com[equal_max]

        else:

            for l in range(0, counter_num):

                below_max = max(below_com, key=below_com.get)
                counter_below.append(int(below_max))
                del below_com[below_max]

            for m in range(0, counter_num):

                above_min = min(above_com, key=above_com.get)
                counter_above.append(int(above_min))
                del above_com[above_min]

        transmute = find_symmetric_pairs(slab, transmute_top, transmute_bottom)

        counter = find_symmetric_pairs(slab, counter_above, counter_below)

    else:

        for k in range(0, transmute_num):

            topmax = max(transmute_atom, key=transmute_atom.get)
            transmute.append(int(topmax))
            del transmute_atom[topmax]


        for l in range(0, counter_num):

            botmin = min(counter_atom, key=counter_atom.get)
            counter.append(int(botmin))
            del counter_atom[botmin]

    return transmute, counter

def transmuter(slab, atom_index, new_atoms, symmetric=False):
    """
    Transmutes atoms in `slab` with indexes given in `atom_index` into new atoms specified
    by an array of ASE atom objects (`new_atoms`).

    Parameters
    ----------
    slab : An atoms object from ASE.

    atom_index : List of indexes of atoms to be transmuted/counter-transmuted
        (see index_transmuted()).

    new_atoms : List of strings of atom symbols. New atoms that atoms in slab will be transmuted into.
        This list must be equal length to `atom_index.`

    symmetric (default: False): Boolean. Indicates if using a symmetric slab.

    Returns
    -------
    transmuted_slab : An atoms object from ASE. This is an updated form of slab with all transmutations.
    """

    new_atoms = [Atom(symbol=item) for item in new_atoms]

    transmuted_slab = slab.copy()

    if symmetric:

        pass

    else:

        for i,dex in enumerate(atom_index):

            transmuted_slab[dex].symbol = new_atoms[i].symbol

    return transmuted_slab

def transmuted_labels(bottom_index, top_index, atom_index, new_atoms):
    """
    Makes a label for a system created from `transmuter()`.

    Parameters
    ----------
    bottom_index : Index of element in `counter` list (produced from `index_transmuted`) that
        corresponds to the index of the atom counter transmuted.

    top_index : Index of element in `transmute` list (produced from `index_transmuted`) that
        corresponds to the index of the atom transmuted.

    atom_index : List of atom indexes from `transmute` and `counter` that correspond to the
        transmuted/counter transmuted atoms.

    new_atoms : List of ASE Atom objects used to transmute. Should be the same length as `atom_index`.
        `atom_index` and `new_atoms` should be defined in the same way they were defined for
        `transmuter()`.

    Returns
    -------
    label : String. Descripted label of the system created from `transmuter()`.

    """

    label_tail = ''

    for i, dex in enumerate(atom_index):

        label_tail = label_tail + '.' + new_atoms[i].symbol + str(atom_index[i])

    label = str(bottom_index) + '.' + str(top_index) + label_tail

    return label
