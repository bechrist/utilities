""":code:`mpi4py` utilities

Copyright (c) 2024-, The University of Texas at Austin

All Rights reserved.
See file COPYRIGHT for details.

This file is part of :code:`bechrist`'s :code:`utilities`. For more information see
https://github.com/bechrist/utitlies

:code:`utilities` is free software; you can redistribute it and/or modify it under the
terms of the GNU General Public License (as published by the Free
Software Foundation) version 3.0 dated June 2007.
"""
__authors__ = ['Blake Christierson, UT Austin <bechristierson@utexas.edu>']
__all__ = ['mpi_print', 'mpi_serial']

import mpi4py.MPI as MPI
import sys


# %% 
def mpi_print(msg: str, comm: MPI.Intracomm = MPI.COMM_WORLD):
    if comm.rank == 0:
        print(f"Rank {comm.rank} | {msg}")
        sys.stdout.flush()

def mpi_serial(comm: MPI.Intracomm):
    """Asserts that provided MPI intracommunicator is size 1 (serial)

    :param comm: MPI intracommunicator
    :type comm: mpi4py.MPI.Intracomm

    :raises NotImplementedError: If provided communicator is not of size 1 
    """
    if comm.size != 1:
        raise NotImplementedError('Only worked out for serial computation')