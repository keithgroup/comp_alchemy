#!/bin/bash
#SBATCH --job-name="0.3.Au15.Ir0-3"
#SBATCH --nodes=1
#SBATCH --ntasks=24
#SBATCH --cluster=smp
#SBATCH --partition=smp
#SBATCH --error=VASP-%j.err
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=cdg36@pitt.edu
#SBATCH --time=6:00:00

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
echo "The JOB ran for: $elapsed_seconds seconds" >> runstats.out