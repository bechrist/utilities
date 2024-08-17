""":code:`torch` utilities

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
__all__ = ['split_validation_dataset']

import torch.utils.data as du


# %%
# Dataset Utilities
# %%
def split_validation_dataset(dataset: du.Dataset, batch_size: int | None, 
                             num_samples: int | None, num_sample_batches: int, 
                             num_validation: int | None, num_validation_batches: int) \
                            -> tuple[du.Subset, du.Subset]:
    """Splits dataset into sample and validation data

    :param dataset: Original dataset
    :type dataset: torch.utils.data.Dataset

    :param batch_size: Batch size
    :type batch_size: int | None

    :param num_samples: Number of samples
    :type num_samples: int | None

    :param num_sample_batches: Number of sample batches
    :type num_sample_batches: int

    :param num_validation: Number of validation samples
    :type num_validation: int | None

    :param num_validation_batches: Number of validation batches
    :type num_validation_batches: int

    :raises ValueError: If number of validation samples is not positive
    :raises ValueError: If number of validation samples exceeds available data
    :raises ValueError: If there is not enough data to create a full batch of samples
    :raises ValueError: If number of sample batches is not positive
    :raises ValueError: If number of samples and validation samples exceeds available data

    :return: Sample and validation datasets
    :rtype: tuple[torch.utils.data.Subset, torch.utils.data.Subset]
    """
    num_data = len(dataset)
    
    num_validation = (num_validation, num_validation_batches*batch_size)[num_validation == None]
    if num_validation < 0:
        raise ValueError(f"Number of validation samples ({num_validation}) must be positive")
    
    if num_samples == -1: 
        num_samples = num_data - num_validation
        if num_samples < 0: 
            raise ValueError((f"Validation samples ({num_validation}) exceeds "
                             f"available amount of data ({num_data})"))
    elif not (isinstance(num_samples, int) and num_samples > 0): 
        if num_sample_batches == -1:
            num_sample_batches = (num_data - num_validation) // batch_size
            if num_sample_batches <= 0:
                raise ValueError((f"Not enough data ({num_data}) " 
                                  f"to create a batch ({batch_size}) after "
                                  f"removing validation samples ({num_validation})"))
        if isinstance(num_sample_batches, int) and num_sample_batches > 0: # NOTE: yes `if`, not `elif`
            num_samples = num_sample_batches*batch_size
        else:
            raise ValueError(f"Invalid number of sample batches ({num_sample_batches}) requested")

    if num_samples + num_validation > num_data: 
        raise ValueError((f"Samples ({num_samples}) and validation ({num_validation}) "
                          f"exceed available amount of data ({num_data})"))
            
    return (du.Subset(dataset, range(num_samples)),
            du.Subset(dataset, range(num_samples, min(num_samples+num_validation, num_data))))


# %%
# Deprecated Argparse Utilities
# def str2optimizer(optimizer: str) -> opt.Optimizer:
#     """Retrieves optimizer from :code:`torch.optim`
#
#     :param optimizer: Optimizer name
#     :type optimizer: str
#
#     :raises TypeError: If retrieved attribute is not a :code:`torch.optim.Optimizer`
#
#     :return: Torch optimizer
#     :rtype: torch.optim.Optimizer
#     """
#     optimizer = getattr(opt, optimizer)
#     if not issubclass(optimizer, opt.Optimizer):
#         raise TypeError("Retrieved optimizer is not a subclass of `torch.optim.Optimizer")
#     return optimizer


# def str2lr_scheduler(lr_scheduler: str) -> opt.lr_scheduler.LRScheduler:
#     """Retrieves learning rate scheduler from :code:`torch.optim`
#
#     :param lr_scheduler: Learning rate scheduler name
#     :type lr_scheduler: str
#
#     :raises TypeError: If retrieved attribute is not a :code:`torch.optim.lr_scheduler.LRScheduler`
#
#     :return: Torch learning rate scheduler
#     :rtype: torch.optim.lr_scheduler.LRScheduler
#     """
#     lr_scheduler = getattr(opt.lr_scheduler, lr_scheduler)
#     if not issubclass(lr_scheduler, opt.lr_scheduler.LRScheduler):
#         raise TypeError("Retrieved learnign rate scheduler is not a subclass of `torch.optim.lr_scheduler.LRScheduler")
#     return lr_scheduler