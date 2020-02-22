"""
"""
from phystone.alchemical_derivative import calc_alc_deriv
from phystone.find_pairs import find_ads_slab_pairs
from phystone.elec_stat_pot import grab_esp, esp_diff, heatmap
from phystone.transmutations import index_transmuted, transmuter, transmuted_labels

from ase import Atom
from ase.io import read

from itertools import combinations

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

        self.slab_contcar = read(f'{slab_dir}CONTCAR')
        self.ads_contcar = read(f'{ads_dir}CONTCAR')

        self.slab_esp = grab_esp(self.slab, f'{self.slab_dir}OUTCAR')
        self.ads_esp = grab_esp(self.ads, f'{self.ads_dir}OUTCAR')

        self.esp_diff = esp_diff(self.slab_esp,
                                 self.ads_esp,
                                 find_ads_slab_pairs(self.slab,
                                                     self.ads))

    def do_alchemy(self, delta_nuclear_charge, number_of_transmutations, top_atom,
                   bottom_atom, transmute_num, counter_num, symmetric=False):
        """
        """
        (transmute_indexes,
         counter_indexes) = index_transmuted(self.slab, top_atom,
                                                  bottom_atom, transmute_num,counter_num,
                                                  symmetric)

        self.transmute_indexes = transmute_indexes
        self.counter_indexes = counter_indexes

        transmute_combinations = list(combinations(transmute_indexes, number_of_transmutations))
        counter_combinations = list(combinations(counter_indexes, number_of_transmutations))

        top_atom = Atom(symbol=top_atom)
        bottom_atom = Atom(symbol=bottom_atom)

        transmute_atom = top_atom
        transmute_atom.number += delta_nuclear_charge
        transmute_atom = [transmute_atom.symbol] * number_of_transmutations

        counter_atom = bottom_atom
        counter_atom.number -= delta_nuclear_charge
        counter_atom = [counter_atom.symbol] * number_of_transmutations

        all_atom = transmute_atom + counter_atom

        pairs = find_ads_slab_pairs(self.slab, self.ads)

        alc_data = pd.DataFrame(columns=['label','delta nuclear charge','transmute indexes',
                                         'transmute espdiff','counter indexes','counter espdiff',
                                         'alchemical derivative','slab atoms object',
                                         'ads atoms object'])

        for bottom_index, counter_index in enumerate(counter_combinations):

            counter_index = list(counter_index)

            ads_counter_index = [pairs[slab_index][1] for slab_index in counter_index]

            for top_index, transmute_index in enumerate(transmute_combinations):

                transmute_index = list(transmute_index)

                ads_transmute_index = [pairs[slab_index][1] for slab_index in transmute_index]

                all_index = transmute_index + counter_index

                ads_all_index = ads_transmute_index + ads_counter_index

                transmuted_slab = transmuter(self.slab_contcar, all_index, all_atom, symmetric)

                transmuted_ads = transmuter(self.ads_contcar, ads_all_index, all_atom, symmetric)

                transmuted_label = transmuted_labels(bottom_index, top_index, all_index, all_atom)

                alc_derivative = calc_alc_deriv(transmute_index, counter_index,
                                                self.esp_diff, delta_nuclear_charge)

                transmute_index_string = ''
                transmute_espdiff = ''
                counter_index_string = ''
                counter_espdiff = ''

                for t in transmute_index:

                    transmute_index_string += str(t) + ':'
                    transmute_espdiff += str(self.esp_diff[t]) + ':'

                for c in counter_index:

                    counter_index_string += str(c) + ':'
                    counter_espdiff += str(self.esp_diff[c]) + ':'

                transmute_index_string = transmute_index_string[:-1]
                transmute_espdiff = transmute_espdiff[:-1]
                counter_index_string = counter_index_string[:-1]
                counter_espdiff = counter_espdiff[:-1]

                alc_data = alc_data.append({'label' : transmuted_label,
                                            'delta nuclear charge' : delta_nuclear_charge,
                                            'transmute indexes' : transmute_index_string,
                                            'transmute espdiff' : transmute_espdiff,
                                            'counter indexes' : counter_index_string,
                                            'counter espdiff' : counter_espdiff,
                                            'alchemical derivative' : alc_derivative[1],
                                            'slab atoms object' : transmuted_slab,
                                            'ads atoms object' : transmuted_ads},
                                            ignore_index=True)

        return alc_data

#TEST

#from ase.visualize import view

#slab_dir = 'tests/vasp_files/slab/'
#ads_dir = 'tests/vasp_files/ads/'

#system = Alchemy(slab_dir, ads_dir)

#alc_data = system.do_alchemy(1,1,'Pt','Pt',1,1)
#print(alc_data['label'][0])
#view(alc_data['slab atoms object'][0])