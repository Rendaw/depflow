#!/usr/bin/env python3
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--force', action='store_true')
args = parser.parse_args()
if not args.force and subprocess.call(['git', 'diff-index', '--quiet', 'HEAD']) != 0:  # noqa
    raise RuntimeError('Working directory must be clean.')
subprocess.check_call([
    'pdoc',
    '--html',
    '--html-no-source',
    '--overwrite',
    'depflow',
])
subprocess.call([
    'git', 'commit',
    '-a',
    '-m', 'Updated docs',
])
subprocess.check_call(['git', 'push'])
subprocess.check_call(['git', 'checkout', 'gh-pages'])
subprocess.check_call(['git', 'reset', '--hard', 'master'])
subprocess.check_call(['git', 'push', '-f'])
subprocess.check_call(['git', 'checkout', 'master'])
