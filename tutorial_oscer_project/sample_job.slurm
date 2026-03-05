#!/usr/bin/env bash

# Sample SLURM job script for OSCER
# Submit with:  sbatch sample_job.slurm
# Before submitting, replace YOUR_USERNAME below with your actual OSCER username.

# SLURM directives these lines look like comments but SLURM actually reads them!
#SBATCH --job-name=hello_oscer          # name that shows up in squeue
#SBATCH --partition=normal              # "normal" for CPU jobs, "gpu" for GPU jobs
#SBATCH --time=00:10:00                 # max walltime (HH:MM:SS) for 10 minutes here
#SBATCH --cpus-per-task=1               # number of CPU cores
#SBATCH --mem=1G                        # memory (RAM)
#SBATCH --output=slurm_%j.out           # stdout log (%j becomes the job ID)
#SBATCH --error=slurm_%j.err            # stderr log

# Uncomment these two lines if you need a GPU:
# #SBATCH --partition=gpu
# #SBATCH --gres=gpu:1

# IMPORTANT: change YOUR_USERNAME to your actual OSCER username!
VENV_PATH="/scratch/YOUR_USERNAME/tutorial-venv"

# Activate the virtual environment and run the script
echo "Activating venv at: ${VENV_PATH}"
source "${VENV_PATH}/bin/activate"

echo "Running hello_oscer.py..."
python hello_oscer.py

echo "Job complete!"
