#!/bin/env python
import logging
import depflow
from plumbum.cmd import cp, cat

logging.basicConfig(level=logging.DEBUG)


flow = depflow.Depflow()


@flow.depends(depflow.file('a.txt'))
def step_a():
    cp('a.txt', 'a')


@flow.depends(depflow.file('b.txt'))
def step_b():
    cp('b.txt', 'b')


@flow.depends(step_a, step_b, depflow.file('c.txt'))
def step_c():
    cp('c.txt', 'c')
    (cat['a', 'b', 'c'] > 'done')()
