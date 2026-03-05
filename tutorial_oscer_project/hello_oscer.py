"""
hello_oscer.py: Simple test script for OSCER.

Run this to verify your Python environment works,
packages are installed, and you can write output files.

Usage (after activating your venv):
  python hello_oscer.py
"""

import os
import sys
import platform
from datetime import datetime

print("=" * 60)
print("  HELLO FROM OSCER!")
print("=" * 60)
print()
print(f"  Hostname:        {platform.node()}")
print(f"  Python version:  {platform.python_version()}")
print(f"  Python path:     {sys.executable}")
print(f"  Current dir:     {os.getcwd()}")
print(f"  Date/Time:       {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Test numpy
import numpy as np
random_array = np.random.rand(5)
print(f"  NumPy version:   {np.__version__}")
print(f"  Random array:    {random_array}")
print(f"  Mean:            {random_array.mean():.4f}")
print()

# Test pandas
import pandas as pd
df = pd.DataFrame({"values": random_array})
print(f"  Pandas version:  {pd.__version__}")
print(f"  DataFrame shape: {df.shape}")
print()

# Test requests
import requests
print(f"  Requests version: {requests.__version__}")
print()

# Create an output file to prove it worked
output_filename = "output.txt"
with open(output_filename, "w") as f:
    f.write("Successfully created a text file on OSCER!\n")
    f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Hostname:  {platform.node()}\n")
    f.write(f"Python:    {platform.python_version()}\n")
    f.write(f"NumPy:     {np.__version__}\n")
    f.write(f"Pandas:    {pd.__version__}\n")
    f.write(f"Requests:  {requests.__version__}\n")

print(f"  Created '{output_filename}' in {os.getcwd()}")
print()
print("=" * 60)
print("  ALL DONE - your OSCER environment is working!")
print("=" * 60)
