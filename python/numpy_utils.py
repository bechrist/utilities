""":code:`numpy` utilities

Copyright (c) 2024-, The University of Texas at Austin

All Rights reserved.
See file COPYRIGHT for details.

This file is part of :code:`bechrist`'s :code:`utilities`. For more information see
https://github.com/bechrist/utitlies

:code:`utilities` is free software; you can redistribute it and/or modify it under the
terms of the GNU General Public License (as published by the Free
Software Foundation) version 3.0 dated June 2007.
"""
from __future__ import annotations

__authors__ = ['Blake Christierson, UT Austin <bechristierson@utexas.edu>']
__all__ = ['LabeledNDArray']

import numpy as np
import numpy.typing as npt
import typing as typ


# %%
class LabeledNDArray(np.ndarray):
	""":code:`numpy.ndarray` subclass that contains named labels corresponding to array items.

	:param array: Array
	:type array: numpy.typing.ArrayLike

	:param label: Array label mapping
	:type label: dict[str, int | typing.Sequence[int] | slice], optional
	"""
	def __new__(cls, 
			array: npt.ArrayLike, 
			label: dict[str, int | typ.Sequence[int] | slice] | None = None) \
			-> LabeledNDArray:
		"""See: https://numpy.org/doc/stable/user/basics.subclassing.html"""
		obj = np.asarray(array).view(cls)
		obj.label = {} if label is None else label
		return obj

	def __array_finalize__(self, obj: np.ndarray | None):
		"""See: https://numpy.org/doc/stable/user/basics.subclassing.html"""
		if obj is None: return

		self.label = getattr(obj, 'label', {})

	def __getitem__(self, idx: int | typ.Sequence[int] | slice | str) -> np.ndarray | typ.Any: 
		"""Override indexing to first check label mapping"""
		if idx in self.label:
			return super(LabeledNDArray, self).__getitem__(self.label[idx])
		return super(LabeledNDArray, self).__getitem__(idx)