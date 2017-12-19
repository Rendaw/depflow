<table width="100%">
    <tr>
        <td>
            <a href="https://github.com/rendaw/qrcode-generator-es6"><img src="https://raw.githubusercontent.com/primer/octicons/master/lib/svg/mark-github.svg?sanitize=true"> Github</a>
        </td>
        <td>
            <a href="https://pypi.python.org/pypi/depflow"><img alt="PyPI" src="https://img.shields.io/pypi/v/depflow.svg"></a>
        </td>
        <td>
            <a href="https://circleci.com/gh/rendaw/depflow"><img alt="Build Status" src="https://circleci.com/gh/rendaw/depflow.svg?style=svg"></a>
        </td>
        <td>
            <a href="https://rendaw.github.io/depflow/depflow.m.html"><img src="https://raw.githubusercontent.com/primer/octicons/master/lib/svg/book.svg?sanitize=true"> Docs</a>
        </td>
</table>

# What is depflow?

depflow is a tool for process automation.  By defining dependencies between steps and arbitrary resources you can automatically skip steps that are already in the correct state.  depflow can be used as a build system but it can also be used for deployment, configuring and bringing up systems and other use cases.

depflow's strength lies in its flexibility.  Using `depflow.check` and `depflow.raw_check` you can define dependencies on any type of resource - api endpoint output, system calls, process states, docker image hashes, etc.  depflow isn't fast and it's only as reliable as your dependency definitions though.  If you're building software and need a fast, comprehensive tool I recommend `tup`.  Using depflow to manage other buildsystems is perfectly reasonable however.

Here is an example process using Plumbum:

```
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
```
