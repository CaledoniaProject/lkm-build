# Introdcution

Build LKM in batch, works for all kernel versions released in CentOS 6-8, Ubuntu 16.04 and 18.04. For security reasons, not all scripts are released alongside this repo.

# Usage

1. Fetch all kernel-devel RPMs/DEBs with [download-all-kernels.py](download-all-kernels.py), extract them to somewhere you like
2. Build docker base image
3. Start a container and mount the previously extracted folder
4. Add necessary symbolic links to /lib/modules/$(uname)
5. Build all kernel modules
6. Profit

