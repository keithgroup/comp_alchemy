from .alchemy import Alchemy
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

def read_vasp_energies(Alchemy, alc_data):

    for index, row in alc_data.iterrows():

        transmute_slab_dir = Alchemy.slab_dir + (f"{row['delta nuclear charge']}_deltaZ_" +
                                                 f"{len(row['transmute indexes'])}_Nt/" +
                                                 f"{row['label']}/")

        transmute_ads_dir = Alchemy.ads_dir + (f"{row['delta nuclear charge']}_deltaZ_" +
                                               f"{len(row['transmute indexes'])}_Nt/" +
                                               f"{row['label']}/")

        calc = Vasp2(directory=transmute_slab_dir)
        calc.read_energy()

        calc = Vasp2(directory=transmute_ads_dir)
        calc.read_energy()
