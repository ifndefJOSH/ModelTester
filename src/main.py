#!/usr/bin/env python3

import sys
import os
import argparse

from Options import Options
'''
Main file for automated model checker. References several other files within this directory

Created by Josh Jeppson on Friday, May 20, 2022
'''

def testStorm():
	if args.install:
		print("[INFO] Installing STORM", file=sys.stderr)
	print("[INFO] Testing against STORM", file=sys.stderr)

def testPrism():
	if args.install:
		print("[INFO] Installing PRISM", file=sys.stderr)
	print("[INFO] Testing against PRISM", file=sys.stderr)

def testStaminaStorm():
	if args.install:
		print("[INFO] Installing STAMINA-STORM", file=sys.stderr)
	print("[INFO] Testing against STAMINA-STORM", file=sys.stderr)


def testStaminaPrism():
	if args.install:
		print("[INFO] Installing STAMINA-PRISM", file=sys.stderr)
	print("[INFO] Testing against STAMINA-PRISM", file=sys.stderr)


def testStaminaOne():
	if args.install:
		print("[INFO] Installing STAMINA 1.0", file=sys.stderr)
	print("[INFO] Testing against STAMINA 1.0", file=sys.stderr)


def processArgs(args):
	if args.verbose:
		print("[INFO] Processing arguments", file=sys.stderr)

	Options.install = args.install
	# Use the default values in Options
	if args.all:
		testStorm()
		testPrism()
		testStaminaStorm()
		testStaminaPrism()
		testStaminaOne()
		return
	Options.storm = args.storm
	if Options.storm:
		testStorm()
	Options.prism = args.prism
	if Options.prism:
		testPrism()
	Options.stamina_storm = args.stamina_storm
	if Options.stamina_storm:
		testStaminaStorm()
	Options.stamina_prism = args.stamina_prism
	if Options.stamina_prism:
		testStaminaPrism()
	Options.stamina_prism_one = args.stamina_prism_one
	if Options.stamina_prism_one:
		testStaminaOne()

if __name__=='__main__':
	if len(sys.argv) == 1:
		print("Requires at least one argument! Perhaps you meant to use '-a'/'--all'?")
		sys.exit(1)
	parser = argparse.ArgumentParser()
	parser.add_argument('-v', '--verbose', help="Output verbose information", action="store_true")
	parser.add_argument('-a', '--all', help="Test against all TRUNCATED model checkers (not STORM and PRISM)", action="store_true")
	parser.add_argument('--storm', help="Check model using the STORM model checker", action="store_true")
	parser.add_argument('--prism', help="Check model using the PRISM model checker", action="store_true")
	parser.add_argument('--stamina_storm', help="Check model using the STAMINA 2.0 truncated model checker, integrated with STORM", action="store_true")
	parser.add_argument('--stamina_prism', help="Check model using the STAMINA 2.0 truncated model checker, integrated with PRISM", action="store_true")
	parser.add_argument('--stamina_prism_one', help="Check model using the STAMINA 1.0 truncated model checker, integrated with PRISM", action="store_true")
	parser.add_argument('--infamy', help="Check model using the INFAMY model checker", action="store_true")
	parser.add_argument('-i', '--install', help="Installs the tools that are needed", action="store_true")
	args = parser.parse_args()
	processArgs(args)
