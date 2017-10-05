#!/usr/bin/env python3
import subprocess
import argparse
import re
from os.path import exists

parser = argparse.ArgumentParser()
parser.add_argument('version')
parser.add_argument('-f', '--force', action='store_true')
args = parser.parse_args()
if not args.force and subprocess.call(['git', 'diff-index', '--quiet', 'HEAD']) != 0:  # noqa
    raise RuntimeError('Working directory must be clean.')
if not re.match('\\d+\\.\\d+\\.\\d+', args.version):
    args.error('version must be in the format N.N.N')
subprocess.check_call(['python', 'setup.py', 'sdist'])
dist = 'dist/depflow-{}.tar.gz'.format(args.version)
if not exists(dist):
    args.error('Deploy version doesn\'t match source version.')
subprocess.check_call(['twine', 'upload', dist, '--user', 'rendaw'])
