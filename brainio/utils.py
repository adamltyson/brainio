import logging
import os
import glob
import psutil

import numpy as np
from scipy.ndimage import zoom

from natsort import natsorted
from slurmio import slurmio


class BrainIoLoadException(Exception):
    pass


def check_mem(img_byte_size, n_imgs):
    """
    Check how much memory is available on the system and compares it to the
    size the stack specified by img_byte_size and n_imgs would take
    once loaded

    Raises an error in case memory is insufficient to load that stack

    :param int img_byte_size: The size in bytes of an individual image plane
    :param int n_imgs: The number of image planes to load
    :raises: BrainLoadException if not enough memory is available
    """
    total_size = img_byte_size * n_imgs
    free_mem = psutil.virtual_memory().available
    if total_size >= free_mem:
        raise BrainIoLoadException(
            "Not enough memory on the system to complete loading operation"
            "Needed {}, only {} available.".format(total_size, free_mem)
        )


def scale_z(volume, scaling_factor, verbose=False):
    """
    Scale the given brain along the z dimension

    :param np.ndarray volume: A brain typically as a numpy array
    :param float scaling_factor:
    :param bool verbose:
    :return:
    """
    if verbose:
        print("Scaling z dimension")
    volume = np.swapaxes(volume, 1, 2)
    volume = zoom(volume, (1, scaling_factor, 1), order=1)
    return np.swapaxes(volume, 1, 2)


def get_sorted_file_paths(file_path, file_extension=None):
    """
    Sorts file paths with numbers "naturally" (i.e. 1, 2, 10, a, b), not
    lexiographically (i.e. 1, 10, 2, a, b).
    :param str file_path: File containing file_paths in a text file,
    or as a list.
    :param str file_extension: Optional file extension (if a directory
     is passed)
    :return: Sorted list of file paths
    """
    if isinstance(file_path, list):
        pass
    elif file_path.endswith(".txt"):
        with open(file_path, "r") as in_file:
            file_path = in_file.readlines()
            file_path = [p.strip() for p in file_path]
    elif os.path.isdir(file_path):
        if file_extension is None:
            file_path = glob.glob(os.path.join(file_path, "*"))
        else:
            file_path = glob.glob(
                os.path.join(file_path, "*" + file_extension)
            )
    else:
        message = (
            "Input file path is not a recognised format. Please check it "
            "is a list of file paths, a text file of these paths, or a "
            "directory containing image files."
        )

        logging.error(message)
        raise NotImplementedError(message)

    file_path = natsorted(file_path)
    return file_path


def get_num_processes(min_free_cpu_cores=2, n_max_processes=None):
    """
    Determine how many CPU cores to use, based on a minimum number of cpu cores
    to leave free, and an optional max number of processes.

    Cluster computing aware for the SLURM job scheduler, and not yet
    implemented for other environments.
    :param int min_free_cpu_cores: How many cpu cores to leave free
    :param int n_max_processes: Maximum number of processes
    :return: Number of processes to
    """
    logging.debug("Determining the maximum number of CPU cores to use")
    try:
        os.environ["SLURM_JOB_ID"]
        n_processes = (
            slurmio.SlurmJobParameters().allocated_cores - min_free_cpu_cores
        )
    except KeyError:
        n_processes = psutil.cpu_count() - min_free_cpu_cores

    if n_max_processes is not None:
        n_processes = min(n_processes, n_max_processes)

    logging.debug(f"Setting number of processes to: {n_processes}")
    return int(n_processes)
