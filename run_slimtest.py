#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright © 2012 Mozilla Corporation

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import argparse
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), "benchtester")))

execfile(os.path.join(os.path.dirname(sys.argv[0]), "slimtest_config.py"))

# First parse the args, just looking for a log file.
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-l', '--logfile', default=None)
args, _ = parser.parse_known_args()
logfile = args.logfile

# Load
import BenchTester
tester = BenchTester.BenchTester(logfile)

# Load modules for tests we have
for test in AreWeSlimYetTests.values():
  if not tester.load_module(test['type']):
    sys.exit(1)

# Parse command line arguments now that all the modules are loaded.
args = tester.parse_args(sys.argv[1:])
if not args or not tester.setup(args):
  sys.exit(1)

# Run tests
for testname, testinfo in AreWeSlimYetTests.items():
  if not tester.run_test(testname, testinfo['type'], testinfo['vars']):
    sys.stderr.write("SlimTest: Failed at test %s -- Errors: %s -- Warnings: %s\n" % (testname, tester.errors, tester.warnings))
    sys.exit(1)

if len(tester.warnings):
  sys.stderr.write("SlimTest: Generated %u warnings: %s" % (len(tester.warnings), tester.warnings))
if len(tester.errors):
  sys.stderr.write("!! SlimTest: Completed with %u errors: %s" % (len(tester.errors), tester.errors))
  sys.exit(1)

sys.stderr.write("SlimTest: Test run successful")
