import logging
import os
import glob
import psutil

from natsort import natsorted
from slurmio import slurmio


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
    :param float ram_needed_per_process: Memory requirements per process. Set
    this to ensure that the number of processes isn't too high.
    :param float fraction_free_ram: Fraction of the ram to ensure stays free
    regardless of the current program.
    :param int n_max_processes: Maximum number of processes
    :param float max_ram_usage: Maximum amount of RAM (in bytes)
    to use (allthough available may be lower)
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

    n_processes = min(n_processes, n_max_processes)
    logging.debug(f"Setting number of processes to: {n_processes}")
    return int(n_processes)
