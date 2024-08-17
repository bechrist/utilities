""":code:`dolfin` utilities

Copyright (c) 2024-, The University of Texas at Austin

All Rights reserved.
See file COPYRIGHT for details.

This file is part of :code:`bechrist`'s :code:`utilities`. For more information see
https://github.com/bechrist/utilities

:code:`utilities` is free software; you can redistribute it and/or modify it under the
terms of the GNU General Public License (as published by the Free
Software Foundation) version 3.0 dated June 2007.
"""
__authors__ = ['Blake Christierson, UT Austin <bechristierson@utexas.edu>']
__all__ = ['set_function_vector']

import dolfin as dl

# %%
def set_function_vector(fcn: dl.Function, vec: dl.Vector, tol: float = 1e-10) -> bool:
    """Sets vector underlying :code:`dolfin.Function` with data from another vector 

    :param fcn: Function to be allocated
    :type fcn: dolfin.Function

    :param vec: Vector containing data
    :type vec: dolfin.Vector

    :param tol: Setting tolerance, defaults to :code:`1e-10`
    :type tol: float, optional

    :return: Boolean flag for whether function vector was updated
    :rtype: bool
    """
    if (fcn.vector() - vec).norm('l2') <= tol * fcn.vector().norm('l2') :
        return False
    
    fcn.vector().zero()
    fcn.vector().axpy(1., vec)
    return True