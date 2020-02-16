"""
"""
import os
from ase.calculators.vasp.vasp2 import Vasp2

def setup_vasp_calcs(Alchemy, alc_data, nodes=1, cores=24, cluster='smp',
                     partition='smp', hours=6, **kwargs):

    for index, row in alc_data.iterrows():

        transmute_slab_dir = Alchemy.slab_dir + (f"{abs(int(row['delta nuclear charge']))}_deltaZ_" +
                                                 f"{len(row['transmute indexes'])}_Nt/" +
                                                 f"{row['label']}/")

        transmute_ads_dir = Alchemy.ads_dir + (f"{abs(int(row['delta nuclear charge']))}_deltaZ_" +
                                               f"{len(row['transmute indexes'])}_Nt/" +
                                               f"{row['label']}/")

        calc = Vasp2(directory=transmute_slab_dir, **kwargs)
        calc.write_input(row['slab atoms object'])
        write_job_script(transmute_slab_dir, row['label'], index, nodes, cores, cluster, partition,
                         hours)
        calc._run()

        calc = Vasp2(directory=transmute_ads_dir, **kwargs)
        calc.write_input(row['ads atoms object'])
        write_job_script(transmute_ads_dir, row['label'], index, nodes, cores, cluster, partition,
                         hours)
        calc._run()

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

def write_job_script(wdir, name, jobnum, nodes, cores, cluster, partition, hours):

    with open(f'{wdir}/job_sub.slurm', 'w') as job_script:

        job_script.write(f'''#!/bin/bash
#SBATCH --job-name="{name}-{jobnum}"
#SBATCH --nodes={nodes}
#SBATCH --ntasks={cores}
#SBATCH --cluster={cluster}
#SBATCH --partition={partition}
#SBATCH --error=VASP-%j.err
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=cdg36@pitt.edu
#SBATCH --time={hours}:00:00

set -v
ulimit -s unlimited

module purge
module load intel/2017.1.132
module load intel-mpi/2017.1.132
module load mkl
module load fftw
module load vasp/5.4.4

# BEFORE running section
echo "JOB_ID: $SLURM_JOB_ID JOB_NAME: $SLURM_JOB_NAME" >> runstats.out
before=$(date +%s)
echo "The JOB started on : $(date)" >> runstats.out

# RUN section
srun --mpi=pmi2 vasp_std  >& stdout.prod

# AFTER running section
after=$(date +%s)
elapsed_seconds=$(expr $after - $before)
echo "The JOB ended on: $(date)" >> runstats.out
echo "The JOB ran for: $elapsed_seconds seconds" >> runstats.out''')

#TEST
#from phystone.alchemy import Alchemy

#h = Alchemy('tests/vasp_files/slab/','tests/vasp_files/ads/')

#alc = h.do_alchemy(1,1,'Pt','Pt',1,1)

#from ase.visualize import view

#view(alc['slab atoms object'][0])

#from phystone.benchmark import setup_vasp_calcs

#setup_vasp_calcs(h, alc)