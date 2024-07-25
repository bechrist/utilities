""":code:`matplotlib` utilities

Copyright (c) 2024-, The University of Texas at Austin

All Rights reserved.
See file COPYRIGHT for details.

This file is part of :code:`bechrist`'s :code:`utilities`. For more information see
https://github.com/bechrist/utitlies

:code:`utilities` is free software; you can redistribute it and/or modify it under the
terms of the GNU General Public License (as published by the Free
Software Foundation) version 3.0 dated June 2007.
"""
__authors__ = ['Blake Christierson, UT Austin <bechristierson@utexas.edu>',
               'Jack Walton, <jwalton3141@gmail.com>']
__all__ = ['set_fig_size']


# %%
def set_fig_size(width, fraction=1, subplots=(1, 1)):
    """Set figure dimensions to avoid scaling in LaTeX. 
    
    Refer to: https://jwalton.info/Embed-Publication-Matplotlib-Latex/

    :param width: Document width in points, or string of predined document type
    :type width: float or string
            
    :param fraction: Fraction of the width which you wish the figure to occupy,
        defaults to 1
    :type fraction: float, optional
            
    :param subplots: The number of rows and columns of subplots, defaults to (1,1)
    :type subplots: tuple[int, ...], optional
            
    :return: Dimensions of figure in inches
    :rtype: tuple[float, float] 
    """
    if width == 'thesis':
        width_pt = 426.79135
    elif width == 'beamer':
        width_pt = 307.28987
    else:
        width_pt = width

    fig_width_pt = width_pt * fraction
    inches_per_pt = 1 / 72.27
    golden_ratio = (1 + 5**.5)/2      

    fig_width_in = fig_width_pt * inches_per_pt
    
    if subplots[1] <= subplots[0]: 
        fig_height_in = fig_width_in * (subplots[0] / subplots[1]) / golden_ratio
    else:
        fig_height_in = fig_width_in * (subplots[0] / subplots[1]) * golden_ratio

    return (fig_width_in, fig_height_in)