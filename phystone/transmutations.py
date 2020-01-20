"""Module for making alchemical transmutations to surface slab models.
"""
#!/usr/bin/env python

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

        for i in range(0, transmute_num):

            topmax = max(transmute_atom, key=transmute_atom.get)
            transmute.append(int(topmax))
            del transmute_atom[topmax]

        for j in range(0, transmute_num):

            botmin = min(transmute_atom, key=transmute_atom.get)
            transmute.append(int(botmin))
            del transmute_atom[botmin]

        for dex in transmute_atom:

            counter.append(int(dex))

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

def transmuter(slab, atom_index, new_atoms):
    """
    Transmutes atoms in `slab` with indexes given in `atom_index` into new atoms specified
    by an array of ASE atom objects (`new_atoms`).

    Parameters
    ----------
    slab : An atoms object from ASE.

    atom_index : List of indexes of atoms to be transmuted/counter-transmuted
        (see index_transmuted()).

    new_atoms : List of ASE atom objects. New atoms that atoms in slab will be transmuted into.
        This list must be equal length to `atom_index.`

    Returns
    -------
    slabcopy : An atoms object from ASE. This is an updated form of slab with all transmutations.
    """

    slabcopy = slab.copy()

    for i in enumerate(atom_index):

        slabcopy[atom_index[i]].symbol = new_atoms[i].symbol

    return slabcopy

def transmuted_labels(bottom_index, top_index, atom_index, new_atoms):

    label_tail = ''

    for i in enumerate(atom_index):

        label_tail = label_tail + '.' + new_atoms[i].symbol + str(atom_index[i])

    label = str(bottom_index) + '.' + str(top_index) + label_tail

    return label
