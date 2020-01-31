"""
Module for manipulating electrostatic potentials printed in VASP OUTCARS.

"""
#!/bin/env python
from math import ceil

def grab_esp(slab, outcar):
    """
    Finds electrostatic potentials printed in a VASP OUTCAR (`outcar`) corresponding
    to the system described by the `slab`.

    This function only works with atoms objects from ASE. Electrostatic potentials are
    indexed with the ASE atom indexes.

    Parameters
    ----------
    slab : An atoms object from ASE.

    outcar : Path to a VASP OUTCAR file of calculation done for slab.

    Returns
    -------
    esp : List of electrostatic potentials for each atom in slab.
    """

    #The following two variables are used to find the chunk of electrostatic
    #potentials at the end of the OUTCAR. They're printed in a table with size
    # of rows x 5.
    atoms = float(len(slab))
    rows = int(ceil(atoms/5))

    #A counter used to find the first line of electrostatic potentials after the
    #string "(electrostatic)" is found in the loop below
    add = 3

    esp = []

    with open(outcar, 'r') as out:

        lines = out.readlines()

    for i, line in enumerate(lines):

        line_split = line.split()

        for chunk in line_split:

            if chunk == '(electrostatic)':

                loc = i

    for k in range(loc + add, loc + add + rows):

        for num in lines[k].split()[1::2]:

            esp.append(float(num))

    return esp

def esp_diff(esp_1, esp_2, pairs):
    """
    Calculating differences in electrostatic potential per atom between systems 1 and 2.

    Diff = esp_2 - esp_1

    Obtain electrostatic potential array with `grab_esp()`.

    Parameters
    ----------
    esp_1 : List of electrostatic potentials for system 1 (see `grab_esp()`).

    esp_2 : List of electrostatic potentials for system 2 (see `grab_esp()`).

    pairs : List of lists that contains pairs of indexes for atoms that match
        between systems 1 and 2 (see `ads_slab_pairs.pairs()`).

    Returns
    -------
    diffs : List of electrostatic potential differences.
    """

    diffs = []

    for pair in pairs:

        diff = esp_2[pair[1]]-esp_1[pair[0]]
        diffs.append(diff)

    return diffs

def remove_duplicate_esp_diffs(dexlist, espdiffs, tol=0.01):
    """
    Filters and removes duplicate electrostatic potential differences from atoms
    supplied in dexlist.

    This functions first finds all values in espdiffs that are unique. Then the function
    removes espdiffs that differ from others by the tol.

    Parameters
    ----------
    dexlist : List of indexes of atoms with electrostatic potential differences to filter.

    espdiffs : List of all electrostatic potential differences for the desired system
        (see `espdiff()`).

    tol (default: 0.01): Tolerance used for removing similar values from unique
        electrostatic potential differences.

    Returns
    -------
    unique_dexes : List of atom indexes that match the filtered electrostatic potential
        differences.
    """

    #Pairing espdiff values with corresponding atom index in dexlist
    espd_dict = {}

    for i in dexlist:

        espd_dict[str(i)] = espdiffs[i]

    #Grabbing unique espdiff values
    unique_diffs = {}

    for dex, diff in espd_dict.items():

        if diff not in unique_diffs.values():

            unique_diffs[dex] = diff

    #print('Unique Electrostatic Potential Differences:')
    #print(unique_diffs.values())
    #print('')

    #Filtering out espdiffs that are differ to others within tol
    copy_unique_diffs = unique_diffs.copy()

    for dex, diff in copy_unique_diffs.items():

        counter = 0

        for diff2 in unique_diffs.values():

            if abs(diff2 - diff) < tol and abs(diff2 - diff) != 0:

                counter += 1

        if counter > 0:

            del unique_diffs[dex]

    #print('Unique Electrostatic Potential Differences WITHIN A TOLERANCE VALUE:')
    #unique_vals = [u for u in unique_diffs.values()]
    #print(unique_vals)
    #print(' ')

    unique_dexes = []

    for dex in unique_diffs:

        unique_dexes.append(int(dex))

    return unique_dexes

def heatmap(slab, espdiffs):
    """
    Assigns electrostatic potential differences to each atom in slab as an
    initial charge in ASE GUI to visualize.

    Parameters
    ----------
    slab : An atoms object from ASE.

    espdiffs : List of all electrostatic potential differences for slab (see `espdiff()`).

    Returns
    -------
    slab : An atoms object from ASE with updated initial charges (slab.get_initial_charges()).
    """

    slab.set_initial_charges(espdiffs)

    return slab
