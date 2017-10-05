[![Build Status](https://circleci.com/gh/Rendaw/depflow.svg?style=svg)](https://circleci.com/gh/Rendaw/depflow)

# What is depflow?

While you can think of depflow as a build system like `make` or `tup` it's implementation and use are a bit different.  Suppose you have a Python script that performs some process.  Using depflow you can easily skip parts of the process when rerunning if their inputs haven't changed.  depflow is a library which can be integrated with multiple workflows.  depflow defines an interface for creating new dependency types (`check`s) such as api responses, program output, and dates.  Like `make` and `tup`, you can use it for assembling software, but for large projects that are primarily filesystem based I'd recommend `tup` instead of this.

Here is an example process using Plumbum:

```
#!/bin/env python
import logging

logging.basicConfig(level=logging.DEBUG)

import depflow
from plumbum.cmd import cp, cat


@depflow.depends(depflow.file('a.txt'))
def step_a():
    cp('a.txt', 'a')


@depflow.depends(depflow.file('b.txt'))
def step_b():
    cp('b.txt', 'b')


@depflow.depends(step_a, step_b, depflow.file('c.txt'))
def step_c():
    cp('c.txt', 'c')
    (cat['a', 'b', 'c'] > 'done')()
```

# Installation

Run
```
pip install depflow
```

# Reference

Look at `depfile.py` for reference documentation.  It may be more up to date than this readme.

# Defining a process

Define steps in the process as nullary functions decorated with `@depflow.depends(*dependencies)`.  Dependencies can either be other steps or checks such as `depflow.file(path)` and `depflow.file_hash(path)`.  Steps are run as they are defined.

# Creating new checks

Depflow accounts for two different types of dependency checks.

### Cached checks

Use `@depflow.check` to decorate a function that returns a value representing the state of some resource, where a dependent step only needs to be updated if the state of the resource changes.

Example:

```
@depflow.check
def kernel_version():
    return 'kernel-version', subprocess.check_output('uname -r')
```

or to account for command line arguments:

```
parser = argparse.ArgumentParser()
...
args = parser.parse_args()

@depflow.check
def args_hash(*keys):
    cs = hashlib.md5()
    for k in keys:
        cs.update(str(getattr(args, k)))
    return 'args {}'.format(','.join(keys)), cs.hexdigest()

@depflow.depends(arg_hash('output_dir', 'author'))
def step_a():
    build_file('a.dat', args.output_dir, author=args.author)

@depflow.depends(arg_hash('output_dir'))
def step_b():
    build_file('b.dat', args.output_dir, author='system')
```

Cached state is stored and compared based on a unique id generated from the first return value, the step name and the ids of its other dependencies.

### Uncached checks

Use `@depflow.raw_check` to decorate a function that returns a boolean indicating that the dependent step needs to be updated.

Example: 

```
@depflow.raw_check
def server_down(uri):
    return uri, not is_server_up(uri)

@depflow.depends(server_down('http://server1/state')):
    start_server('server1')
```
