#!/usr/bin/env python3

import sys
import os
import argparse

from Options import Options
'''
Main file for automated model checker. References several other files within this directory

Created by Josh Jeppson on Friday, May 20, 2022
'''

def processArgs(args):
	if args.verbose:
		print("[INFO] Processing arguments")
	# Use the default values in Options
	if args.all:
		return
	Options.storm = args.storm
	Options.prism = args.prism
	Options.stamina_storm = args.stamina_storm
	Options.stamina_prism = args.stamina_prism
	Options.stamina_prism_one = args.stamina_prism_one

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
	args = parser.parse_args()
	processArgs(args)
