# OSCER Tutorial  Running Python on OSCER

> **Who is this for?** Anyone in the lab who wants to run Python scripts on the OU supercomputer (OSCER/Schooner). No prior HPC experience required.

> **Sample project folder used throughout this guide:** `tutorial_oscer_project/`

You will need the terminal to run all OSCER commands. Every step in this guide is a shell command you type in Terminal and run on your local machine or on the OSCER login node after you connect.



## Table of Contents

1. [What is OSCER?](#what-is-oscer)
2. [Connecting via SSH](#connecting-via-ssh)
3. [Navigating the Filesystem](#navigating-the-filesystem)
4. [Uploading Your Files](#uploading-your-files)
5. [Setting Up a Python Environment](#setting-up-a-python-environment)
6. [Understanding SLURM (the Job Scheduler)](#understanding-slurm-the-job-scheduler)
7. [Submitting Your First Job](#submitting-your-first-job)
8. [Checking Job Status & Reading Output](#checking-job-status-and-reading-output)
9. [Downloading Results to Your Computer](#downloading-results-to-your-computer)
10. [The Full Walkthrough (Start to Finish)](#the-full-walkthrough-start-to-finish)
11. [Tips & Troubleshooting](#tips-and-troubleshooting)



<a id="what-is-oscer"></a>
## 1. What is OSCER?

OSCER stands for the **OU Supercomputing Center for Education & Research**. The actual machine is called **Schooner**. It's a big cluster of computers (nodes) that we can submit jobs to. Instead of running code on your laptop, you send it to Schooner and it runs on powerful hardware  sometimes with GPUs, lots of RAM, and many CPU cores.

**Why use it?**
 Your script takes hours on your laptop → might take minutes on Schooner
 You need a GPU and don't have one locally
 You need more RAM or disk space than your machine has

**Key concepts:**
 **Node**  One computer in the cluster
 **SLURM**  The job scheduler that manages the queue (you submit jobs, SLURM decides when and where they run)
 **Partition**  A group of nodes (e.g., `normal` for CPUonly, `gpu` for GPU work)



<a id="connecting-via-ssh"></a>
## 2. Connecting via SSH

SSH (Secure Shell) is how you connect to Schooner from your terminal.

### FirstTime Setup

1. **Get an OSCER account**  talk to your PI or visit [oscer.ou.edu](https://www.oscer.ou.edu/) to request one
2. **Open your terminal** (Terminal on Mac, PowerShell or WSL on Windows)
3. **Connect:**

```bash
ssh YOUR_USERNAME@schooner.oscer.ou.edu
```

Replace `YOUR_USERNAME` with your actual OSCER username. You'll be prompted for your password.

> **Example:** If your username is `jsmith`, you'd type:
> ```bash
> ssh jsmith@schooner.oscer.ou.edu
> ```



<a id="navigating-the-filesystem"></a>
## 3. Navigating the Filesystem

When you log in, you're dropped into your **home directory**: `/home/YOUR_USERNAME/`

OSCER has two main storage areas you should know about:

| Location | Path | Space | Speed | Persistence |
||||||
| **Home** | `/home/YOUR_USERNAME/` | Small (~25 GB) | Slower | Permanent  backed up |
| **Scratch** | `/scratch/YOUR_USERNAME/` | Large (~10 TB) | Faster | Temporary  files deleted after ~30 days of inactivity |

### Rules of Thumb

 **Store code and small files** in `/home/`
 **Store large data, virtual environments, and model weights** in `/scratch/`
 **Never run jobs from `/home/`** if they generate lots of output  use `/scratch/`

### Useful Linux Commands

If you're not familiar with the Linux terminal, here's a quick cheat sheet:

```bash
pwd                    # Print current directory (where am I?)
ls                     # List files in current directory
ls -la                 # List ALL files with details (including hidden ones)
cd /scratch/$USER      # Change to your scratch directory
mkdir tutorial_oscer_project       # Create a new folder
cp file.py backup.py   # Copy a file
mv old.py new.py       # Rename/move a file
rm file.py             # Delete a file (careful, no undo!)
rm -r folder/          # Delete a folder and everything in it (be very careful)
cat file.txt           # Print file contents to screen
less file.txt          # View file contents (press q to quit)
du -sh folder/         # Check how much space a folder uses
quota                  # Check your disk quota
```



<a id="uploading-your-files"></a>
## 4. Uploading Your Files

You need to get your Python scripts (and any data) from your local computer onto OSCER. There are two common tools: `scp` and `rsync`.

### Using `scp` (Simple Copy)

`scp` works like `cp`, but over the network.

```bash
# Upload a single file:
scp tutorial_oscer_project/hello_oscer.py YOUR_USERNAME@schooner.oscer.ou.edu:/home/YOUR_USERNAME/tutorial_oscer_project/

# Upload an entire folder:
scp -r tutorial_oscer_project/ YOUR_USERNAME@schooner.oscer.ou.edu:~/
```

### Using `rsync` (Smarter Sync)

`rsync` is better for syncing folders because it only transfers files that changed:

```bash
# Sync the sample project folder to OSCER:
rsync -avh tutorial_oscer_project/ YOUR_USERNAME@schooner.oscer.ou.edu:~/tutorial_oscer_project/
```

**Flags:**
 `a` = archive mode (preserves permissions, timestamps, etc.)
 `v` = verbose (shows what's being transferred)
 `h` = humanreadable sizes

> **Pro tip:** The trailing `/` on the source folder matters!
>  `tutorial_oscer_project/` → copies the *contents* into the destination
>  `tutorial_oscer_project` (no slash) → copies the *folder itself* into the destination



<a id="setting-up-a-python-environment"></a>
## 5. Setting Up a Python Environment

OSCER has system Python, but you should **always** create a virtual environment (venv) for your project. This avoids version conflicts and gives you full control over your packages.

### Step 1: SSH into OSCER

```bash
ssh YOUR_USERNAME@schooner.oscer.ou.edu
```

### Step 2: Create a Virtual Environment on Scratch

We put the venv on `/scratch/` because it can get large:

```bash
# Navigate to your scratch space
cd /scratch/$USER

# Create the virtual environment using Python 3
python3 -m venv tutorial-venv
```

> **If `python3` doesn't work**, try loading a module first:
> ```bash
> module load Python/3.10.4GCCcore11.3.0
> python3 m venv tutorialvenv
> ```
> You can see available Python modules with: `module avail Python`

### Step 3: Activate the Virtual Environment

```bash
source /scratch/$USER/tutorial-venv/bin/activate
```

Your prompt should now show `(tutorialvenv)` at the beginning  that means it's active!

### Step 4: Install Packages

```bash
# Upgrade pip first (always a good idea)
pip install --upgrade pip

# Install from the requirements.txt file
pip install -r ~/tutorial_oscer_project/requirements.txt
```

Or install packages individually:

```bash
pip install numpy pandas requests
```

### Step 5: Verify It Works

```bash
python -c "import numpy; print(f'NumPy {numpy.__version__} is working!')"
```

### Deactivating

When you're done, you can deactivate the venv:

```bash
deactivate
```

> **Remember:** You'll need to reactivate the venv every time you log in, or your SLURM job script needs to activate it (we'll cover this next).



<a id="understanding-slurm-the-job-scheduler"></a>
## 6. Understanding SLURM (the Job Scheduler)

You **cannot** run `python my_script.py` directly on the login node  it's not allowed and your process will get killed (this is how I crashed the supercomputer, so DON'T DO IT!!!). Instead, you write a **SLURM job script** that tells the scheduler:

 How much time your job needs
 How much memory and how many CPUs
 Whether you need a GPU
 What commands to run

### Anatomy of a SLURM Job Script

Here's the `sample_job.slurm` file included in this tutorial:

```bash
#!/usr/bin/env bash

#SBATCH jobname=hello_oscer          # Name shown in the queue
#SBATCH partition=normal              # "normal" = CPU, "gpu" = GPU
#SBATCH time=00:10:00                 # Max runtime: 10 minutes
#SBATCH cpuspertask=1               # Number of CPU cores
#SBATCH mem=1G                        # Memory (RAM)
#SBATCH output=slurm_%j.out           # Stdout file (%j = job ID)
#SBATCH error=slurm_%j.err            # Stderr file (%j = job ID)

# Activates your virtual environment
source /scratch/YOUR_USERNAME/tutorial-venv/bin/activate

# Runs your script
python hello_oscer.py
```

### Key `#SBATCH` Options

| Option | What It Does | Example |
||||
| `jobname` | Name your job (for `squeue`) | `jobname=my_analysis` |
| `partition` | Which queue to use | `normal`, `gpu`, `debug` |
| `time` | Max walltime (HH:MM:SS) | `time=04:00:00` (4 hours) |
| `cpuspertask` | Number of CPU cores | `cpuspertask=8` |
| `mem` | Total memory | `mem=64G` |
| `gres` | GPUs (only for `gpu` partition) | `gres=gpu:1` |
| `output` | Where stdout goes | `output=logs/out_%j.log` |
| `error` | Where stderr goes | `error=logs/err_%j.log` |

> **`%j` gets replaced with the job ID**  so if your job ID is `1234567`, the output file will be `slurm_1234567.out`. This lets you run the same script multiple times without overwriting logs.

### How Much Should I Request?

 **Start small**, then increase if your job fails
 If you request **too much time** → your job might wait in the queue longer
 If you request **too little time** → your job gets killed when time runs out
 If you request **too much memory** → same queue delay
 If you request **too little memory** → your job crashes with an outofmemory error

A good starting strategy: start with 1 hour, 4 GB RAM, 1 CPU. Adjust based on what actually happens.



<a id="submitting-your-first-job"></a>
## 7. Submitting Your First Job

Once your files are on OSCER and your venv is set up, here's how to submit:

### Submit the Job

```bash
# Make sure you're in the directory with your script and the .slurm file
cd ~/tutorial_oscer_project

# Submit it
sbatch sample_job.slurm
```

SLURM will respond with something like:

```
Submitted batch job 1234567
```

That number is your **job ID**  remember it!



<a id="checking-job-status-and-reading-output"></a>
## 8. Checking Job Status & Reading Output

### Check If Your Job Is Running

```bash
# See all YOUR jobs:
squeue -u $USER

# See just one job:
squeue -j 1234567
```

The output looks something like:

```
  JOBID  PARTITION     NAME     USER  ST  TIME  NODES  NODELIST(REASON)
1234567    normal  hello_os  jsmith   R  0:05      1  c001
```

**Status codes (`ST`):**
 `PD` = Pending (waiting in queue)
 `R` = Running
 `CG` = Completing (finishing up)
 If it's gone from `squeue`, it's done (or failed)

### Cancel a Job

```bash
scancel 1234567
```

### Read the Output

After the job finishes, check the log files:

```bash
# Your stdout (print statements etc.):
cat slurm_1234567.out

# Errors (if any):
cat slurm_1234567.err
```

If you ran `hello_oscer.py`, you should also see an `output.txt` file:

```bash
cat output.txt
```

It should say: **"Successfully created a text file on OSCER!"**

### Check Past Jobs

```bash
# See info about a completed job (including exit code, resources used, etc.):
sacct -j 1234567 --format=JobID,JobName,State,ExitCode,Elapsed,MaxRSS
```

This is super useful  `MaxRSS` tells you how much memory your job actually used, so you can tune your request for next time.



<a id="downloading-results-to-your-computer"></a>
## 9. Downloading Results to Your Computer

After your job finishes, you'll want to pull the results back to your local machine.

### Using `scp`

```bash
# From your LOCAL terminal (not OSCER):

# Download a single file:
scp YOUR_USERNAME@schooner.oscer.ou.edu:~/tutorial_oscer_project/output.txt ./

# Download an entire output folder:
scp -r YOUR_USERNAME@schooner.oscer.ou.edu:~/tutorial_oscer_project/results/ ./local_results/
```

### Using `rsync`

```bash
# Sync results from OSCER to a local folder:
rsync -avh YOUR_USERNAME@schooner.oscer.ou.edu:~/tutorial_oscer_project/output.txt ./
rsync -avh YOUR_USERNAME@schooner.oscer.ou.edu:~/tutorial_oscer_project/results/ ./local_results/
```



<a id="the-full-walkthrough-start-to-finish"></a>
## 10. The Full Walkthrough (Start to Finish)

Here is every step in order, using the files in this tutorial. Follow this and you'll have a working job on OSCER.

### On Your Local Machine

```bash
# 1. Open sample_job.slurm in your text editor and change YOUR_USERNAME
#    to your actual OSCER username, then save it

# 2. Upload the tutorial files to OSCER
scp -r tutorial_oscer_project/ YOUR_USERNAME@schooner.oscer.ou.edu:~/
```

### On OSCER (SSH In)

```bash
# 3. Connect to OSCER
ssh YOUR_USERNAME@schooner.oscer.ou.edu

# 4. Verify your files made it
ls ~/tutorial_oscer_project/
#   hello_oscer.py  requirements.txt  sample_job.slurm

# 5. Create a Python virtual environment (onetime setup)
cd /scratch/$USER
python3 -m venv tutorial-venv

# 6. Activate the venv
source /scratch/$USER/tutorial-venv/bin/activate

# 7. Install dependencies
pip install --upgrade pip
pip install -r ~/tutorial_oscer_project/requirements.txt

# 8. Submit the job
cd ~/tutorial_oscer_project
sbatch sample_job.slurm
#   "Submitted batch job 1234567"

# 9. Watch the queue until it finishes
squeue -u $USER
#   Wait until your job disappears from the list

# 10. Check the output
cat slurm_*.out
cat output.txt
#   "Successfully created a text file on OSCER!"
```

### Back on Your Local Machine

```bash
# 11. Download the results
scp YOUR_USERNAME@schooner.oscer.ou.edu:~/tutorial_oscer_project/output.txt ./
scp YOUR_USERNAME@schooner.oscer.ou.edu:~/tutorial_oscer_project/slurm_*.out ./
scp YOUR_USERNAME@schooner.oscer.ou.edu:~/tutorial_oscer_project/slurm_*.err ./

# BETTER ALTERNATIVE: copy the whole project folder back in one command
# The destination path after the space is where the folder will be copied
scp -r YOUR_USERNAME@schooner.oscer.ou.edu:~/tutorial_oscer_project ./tutorial_oscer_project_copy/

# 12. Read them locally
cat output.txt
```

### What `slurm_*.out` and `output.txt` mean

`slurm_*.out` is the job log from your scheduler run.
Slurm directs that log output to the file name set by `#SBATCH --output`, but the messages inside come from `hello_oscer.py` and the commands in the job script.
It shows what your job did on the compute node, including environment details and normal print statements.
That file is where you check startup issues, scheduling context, or Python runtime messages from the job run.

`output.txt` is your script output file.
It is created by `hello_oscer.py` and contains the task result you asked the script to write.
When you see the success text in `output.txt`, your script logic executed and reached completion.

Use this rule of thumb after the run:
`slurm_*.out` tells you whether the job ran correctly on the cluster.
`output.txt` tells you whether your script produced the expected result.

**That's it!** You've now uploaded code, created a venv, submitted a SLURM job, and downloaded the results.



<a id="tips-and-troubleshooting"></a>
## 11. Tips & Troubleshooting

### Common Issues

| Problem | Likely Cause | Fix |
||||
| `python3: command not found` | Python module not loaded | `module load Python/3.10.4GCCcore11.3.0` |
| `ModuleNotFoundError: No module named 'numpy'` | Venv not activated or package not installed | Activate venv, then `pip install numpy` |
| Job stuck in `PD` forever | Requested too many resources or cluster is busy | Reduce `time`, `mem`, or `cpuspertask` |
| `slurmstepd: error: Exceeded job memory limit` | Your script used more RAM than requested | Increase `mem` in your `.slurm` file |
| `CANCELLED` due to time limit | Script took longer than `time` | Increase `time` |
| `Permission denied` on the `.slurm` file | File isn't executable (usually fine, `sbatch` doesn't need it) | Not actually a problem for `sbatch` |

### Interactive Sessions

Sometimes you want to poke around on a compute node without writing a SLURM script (useful for debugging):

```bash
# Get an interactive session (1 hour, 4GB RAM):
srun --partition=normal --time=01:00:00 --mem=4G --pty bash

# With a GPU:
srun --partition=gpu --time=01:00:00 --mem=8G --gres=gpu:1 --pty bash
```

You'll get dropped into a shell on a compute node. Run your script, test things out, then type `exit` to leave.

### Useful Module Commands

OSCER uses the `module` system to manage preinstalled software:

```bash
module avail               # See all available software
module avail Python        # See available Python versions
module load Python/3.10.4-GCCcore-11.3.0   # Load a specific version
module list                # See what you have loaded
module purge               # Unload everything
```

### Checking Your Disk Usage

```bash
# How much home space am I using?
du -sh /home/$USER

# How much scratch space?
du -sh /scratch/$USER

# Official quota check (if available):
quota
```

### Transferring Large Files

For very large files (multiGB datasets), consider:
 **Compress first:** `tar czf data.tar.gz data/`, transfer the `.tar.gz`, then decompress on OSCER
 **Use rsync** over scp  it can resume interrupted transfers
 **Be patient**  large transfers take time, especially from offcampus

### Editing Files on OSCER

You can edit files directly on OSCER using terminal editors:

```bash
nano filename.py          # Easy to use, shows keyboard shortcuts at bottom
vim filename.py           # Powerful but has a steep learning curve (type :q! to escape)
```

Or use **VS Code Remote SSH**  install the "Remote  SSH" extension, and you can edit files on OSCER as if they were local. This is amazing for development.



## Files in This Folder

| File | What It Is |
|||
| `README.md` | This tutorial (you're reading it!) |
| `tutorial_oscer_project/` | The selfcontained sample project folder used in all command examples |
| `tutorial_oscer_project/hello_oscer.py` | A simple Python script that prints system info and creates `output.txt` |
| `tutorial_oscer_project/requirements.txt` | Python packages to install (`numpy`, `pandas`, `requests`) |
| `tutorial_oscer_project/sample_job.slurm` | A SLURM job script ready to submit (edit your username first!) |



## Quick Reference Card

```bash
# ── Connect ───────────────────────────────
ssh YOUR_USERNAME@schooner.oscer.ou.edu

# ── Upload files ──────────────────────────
scp tutorial_oscer_project/hello_oscer.py YOUR_USERNAME@schooner.oscer.ou.edu:~/tutorial_oscer_project/
rsync -avh tutorial_oscer_project/ YOUR_USERNAME@schooner.oscer.ou.edu:~/tutorial_oscer_project/

# ── Environment setup (onetime) ─────────
python3 -m venv /scratch/$USER/my-venv
source /scratch/$USER/my-venv/bin/activate
pip install -r ~/tutorial_oscer_project/requirements.txt

# ── Submit & monitor ─────────────────────
cd ~/tutorial_oscer_project
sbatch sample_job.slurm   # Submit
squeue -u $USER           # Check status
scancel JOBID             # Cancel
sacct -j JOBID            # Job history

# ── Download results ─────────────────────
scp YOUR_USERNAME@schooner.oscer.ou.edu:~/tutorial_oscer_project/results.txt ./
```



*Made for the Mika Fish Lab  if you get stuck, ask Ty!*
