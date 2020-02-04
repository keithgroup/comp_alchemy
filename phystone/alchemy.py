"""
"""
from alchemical_derivative import calc_alc_deriv
from find_pairs import find_ads_slab_pairs
from elec_stat_pot import grab_esp, esp_diff, heatmap
from transmutations import index_transmuted, transmuter, transmuted_labels

from ase.io import read

import pandas as pd

class Alchemy():
    """
    """

    def __init__(self, slab_dir, ads_dir):
        """
        """
        self.slab_dir = slab_dir
        self.ads_dir = ads_dir

        self.slab = read(f'{slab_dir}POSCAR')
        self.ads = read(f'{ads_dir}POSCAR')

        self.slab_esp = grab_esp(self.slab, f'{self.slab_dir}OUTCAR')
        self.ads_esp = grab_esp(self.ads, f'{self.ads_dir}OUTCAR')

        self.esp_diff = esp_diff(self.slab_esp,
                                 self.ads_esp,
                                 find_ads_slab_pairs(self.slab,
                                                     self.ads))

    def do_alchemy(self, delta_nuclear_charge, top_atom, bottom_atom,
                   transmute_num, counter_num, symmetric=False):
        """
        """
        (transmute_indexes,
         counter_indexes) = index_transmuted(self.slab, top_atom.symbol,
                                                  bottom_atom.symbol, transmute_num,counter_num,
                                                  symmetric)

        self.transmute_indexes = transmute_indexes
        self.counter_indexes = counter_indexes

        transmute_atom = top_atom
        transmute_atom.number += delta_nuclear_charge

        counter_atom = bottom_atom
        counter_atom.number -= delta_nuclear_charge

        alc_data = pd.DataFrame(columns=['label','delta nuclear charge','transmute indexes',
                                         'transmute espdiff','counter indexes','counter espdiff',
                                         'alchemical derivative','atoms object'])

        for bottom_index, counter_index in enumerate(counter_indexes):

            for top_index, transmute_index in enumerate(transmute_indexes):

                transmuted_slab = transmuter(self.slab, [transmute_index, counter_index],
                                             [transmute_atom, counter_atom],symmetric)

                transmuted_label = transmuted_labels(bottom_index, top_index,
                                                     [transmute_index, counter_index],
                                                     [transmute_atom, counter_atom])

                alc_derivative = calc_alc_deriv([transmute_index], [counter_index], self.esp_diff,
                                                delta_nuclear_charge)

                alc_data = alc_data.append({'label' : transmuted_label,
                                            'delta nuclear charge' : delta_nuclear_charge,
                                            'transmute indexes' : transmute_index,
                                            'transmute espdiff' : self.esp_diff[transmute_index],
                                            'counter indexes' : counter_index,
                                            'counter espdiff' : self.esp_diff[counter_index],
                                            'alchemical derivative' : alc_derivative[1],
                                            'atoms object' : transmuted_slab},
                                            ignore_index=True)

        return alc_data

slab_dir = 'tests/vasp_files/slab/'
ads_dir = 'tests/vasp_files/ads/'

alc = Alchemy(slab_dir, ads_dir)

from ase import Atom
from ase.visualize import view

p1 = alc.do_alchemy(1, Atom('Pt'), Atom('Pt'), 8, 1)

p2 = alc.do_alchemy(-1, Atom('Pt'), Atom('Pt'), 8, 1)

#view(p1['atoms object'][0])

#view(heatmap(alc.slab, alc.esp_diff))