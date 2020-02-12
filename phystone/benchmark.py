from alchemy import Alchemy
import os
from ase.calculators.vasp.vasp2 import Vasp2

def setup_vasp_calcs(Alchemy, alc_data, **kwargs):

    for index, row in alc_data.iterrows():

        transmute_slab_dir = Alchemy.slab_dir + (f"{row['delta nuclear charge']}_deltaZ_" +
                                                 f"{len(row['transmute indexes'])}_Nt/" +
                                                 f"{row['label']}/")

        transmute_ads_dir = Alchemy.ads_dir + (f"{row['delta nuclear charge']}_deltaZ_" +
                                               f"{len(row['transmute indexes'])}_Nt/" +
                                               f"{row['label']}/")

        calc = Vasp2(directory=transmute_slab_dir,**kwargs)
        calc.write_input(row['slab atoms object'])

        calc = Vasp2(directory=transmute_ads_dir,**kwargs)
        calc.write_input(row['ads atoms object'])

#TESTS

from ase import Atom
from ase.io import read
from ase.visualize import view

slab_dir = 'tests/vasp_files/slab/'
ads_dir = 'tests/vasp_files/ads/'

alc = Alchemy(slab_dir, ads_dir)

alc_data = alc.do_alchemy(1, 2, Atom('Pt'), Atom('Pt'), 4, 4)

setup_vasp_calcs(alc, alc_data, kpts=(5,5,5), encut=350, nsw=500)

#view(read('tests/vasp_files/slab/1_deltaZ_2_Nt/0.1.Au12.Au14.Ir0.Ir1/POSCAR'))

#view(read('tests/vasp_files/ads/1_deltaZ_2_Nt/0.1.Au12.Au14.Ir0.Ir1/POSCAR'))

#calc = test_vasp(directory='tests/vasp_files/',kpts=(5,5,5),encut=350,nsw=500)

#print(calc)

#calc.write_input(alc_data['slab atoms object'][0])