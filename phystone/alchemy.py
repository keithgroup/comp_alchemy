"""
"""
from .alchemical_derivative import *
from .find_pairs import *
from .elec_stat_pot import *
from .transmutations import *

from ase.io import read

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

    def get_esp(self):
        """
        """
        self.slab_esp = grab_esp(self.slab, f'{self.slab_dir}OUTCAR')
        self.ads_esp = grab_esp(self.ads, f'{self.ads_dir}OUTCAR')

