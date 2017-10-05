#!/usr/bin/env python3
from subprocess import check_call as cc
import argparse
import re
from os.path import exists

parser = argparse.ArgumentParser()
parser.add_argument('version')
args = parser.parse_args()
if not args.force and subprocess.call(['git', 'diff-index', '--quiet', 'HEAD']) != 0:  # noqa
    raise RuntimeError('Working directory must be clean.')
if not re.match('\\d+\\.\\d+\\.\\d+', args.version):
    args.error('version must be in the format N.N.N')
cc(['python', 'setup.py', 'sdist'])
dist = 'dist/depflow-{}.tar.gz'.format(args.version)
if not exists(dist):
    args.error('Deploy version doesn\'t match source version.')
cc(['twine', 'upload', dist, '--user', 'rendaw'])
