#!/usr/bin/env python3
import argparse
import subprocess
import re

parser = argparse.ArgumentParser()
parser.add_argument('version')
parser.add_argument('-f', '--force', action='store_true')
args = parser.parse_args()
if not args.force and subprocess.call(['git', 'diff-index', '--quiet', 'HEAD']) != 0:  # noqa
    raise RuntimeError('Working directory must be clean.')
if not re.match('\\d+\\.\\d+\\.\\d+', args.version):
    args.error('version must be in the format N.N.N')
subprocess.check_call([
    'sed',
    '-e',
    's'
    '/\\(version=\'\\)[[:digit:]]\\+\\.[[:digit:]]\\+\\.[[:digit:]]\\+\\(\'\\)'
    '/\\1{}\\2'
    '/g'.format(
        args.version
    ),
    '-i',
    'setup.py',
])
subprocess.call([
    'git', 'commit',
    '-a',
    '-m', 'VERSION {}'.format(args.version),
])
subprocess.check_call([
    'git', 'tag',
    '-a', 'v{}'.format(args.version),
    '-m', 'v{}'.format(args.version),
    '-f',
])
subprocess.check_call(['git', 'push'])
subprocess.check_call([
    'git', 'push',
    '--tags',
    '-f',
])
subprocess.check_call(['git', 'checkout', 'gh-pages'])
subprocess.check_call(['git', 'reset', '--hard', 'master'])
subprocess.check_call(['git', 'push', '-f'])
subprocess.check_call(['git', 'checkout', 'master'])
