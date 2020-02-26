#!/bin/bash
#SBATCH --job-name=H_BE/ontop/2x2/Pt-slab-2x2-H-ontop
#SBATCH --nodes=2
#SBATCH --ntasks=28
#SBATCH --time=48:00:00
#SBATCH --cluster=mpi

set -v
cd H_BE/ontop/2x2/Pt-slab-2x2-H-ontop
module purge
module load intel/2017.1.132
module load intel-mpi/2017.1.132
module load mkl
module load fftw
module load vasp/5.4.4

srun --mpi=pmi2 vasp_std  >& stdout.prod
