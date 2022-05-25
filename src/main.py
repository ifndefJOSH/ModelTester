#!/usr/bin/env python3

import sys
import os
import argparse
import time

from Options import Options
'''
Main file for automated model checker. References several other files within this directory

Created by Josh Jeppson on Friday, May 20, 2022
'''

RST = "\x1B[0m"
BLU = "\x1B[34m"
RED = "\x1B[31m"
YEL = "\x1B[33m"
BLD = "\x1B[1m"

testTable = [
			["Model File", "Properties File"]
		]

commands = []

# The line that the results string starts with
resultString = []

def info(msg, isVerbose=False):
	if Options.silent or (isVerbose and not Options.verbose):
		return
	print(f"{BLD}{BLU}[INFO]:{RST} {msg}", file=sys.stderr)

def warn(msg, isVerbose=False):
	if Options.silent or (isVerbose and not Options.verbose):
		return
	print(f"{BLD}{YEL}[WARNING]:{RST} {msg}", file=sys.stderr)

def err(msg, isVerbose=False, shouldExit=False, exitCode=1):
	if Options.silent or (isVerbose and not Options.verbose):
		return
	print(f"{BLD}{RED}[ERROR]:{RST} {msg}", file=sys.stderr)
	if shouldExit:
		sys.exit(exitCode)

def testStorm():
	if args.install:
		info("Installing STORM")
		os.system('./installScripts/storm.sh')
	info("Adding the following model checker to the test suite: STORM")
	testTable[0].append("STORM")
	commands.append('storm --prism $MODEL_FILE --prop $PROPERTIES_FILE -pc')
	err("STORM does not support infinite state space!", True)

def testPrism():
	if args.install:
		info("Installing PRISM")
		os.system('./installScripts/prism.sh')
	info("Adding the following model checker to the test suite: PRISM")
	testTable[0].append("PRISM")
	commands.append('prism $MODEL_FILE $PROPERTIES_FILE')
	err("PRISM does not support infinite state space truncation!", True)

def testStaminaStorm():
	if args.install:
		info("Installing STAMINA-STORM")
		os.system('./installScripts/stamina.sh')
	info("Adding the following model checker to the test suite: STAMINA-STORM")
	testTable[0].append("STAMINA/STORM")
	commands.append('sstamina $MODEL_FILE $PROPERTIES_FILE')
	resultsString.append(
		{"min":"Probability Minimum:", "max":"Probability Maximum"
	)

def testStaminaPrism():
	if args.install:
		info("Installing STAMINA-PRISM")
		os.system('./installScripts/stamina_p.sh')
	info("Adding the following model checker to the test suite: STAMINA-PRISM")
	testTable[0].append("STAMINA/PRISM")
	commands.append('pstamina $MODEL_FILE $PROPERTIES_FILE')
	resultsString.append(
		{"min":"ProbMin:", "max":"ProbMax"}
	)


def testStaminaOne():
	if args.install:
		info("Installing STAMINA 1.0")
		os.system('./installScripts/stamina_p1.sh')
	info("Adding the following model checker to the test suite: STAMINA 1.0")
	testTable[0].append("STAMINA/PRISM 1.0")
	commands.append('stamina-v1 $MODEL_FILE $PROPERTIES_FILE')
	resultsString.append(
		{"min":"ProbMin:", "max":"ProbMax"}
	)


def processArgs(args):
	Options.folder = args.folder if args.folder is not None else "../models"
	Options.output = args.output if args.output is not None else "out"
	Options.silent = args.silent
	Options.verbose = args.verbose
	info("Processing arguments", True)
	info(f"Model and properties file is found at {Options.folder}/model_and_properties", True)
	info(f"Will write to output {Options.output}_times.csv and {Options.output}_results.csv", True)
	Options.install = args.install
	# Use the default values in Options
	if args.all:
		testStorm()
		testPrism()
		testStaminaStorm()
		testStaminaPrism()
		testStaminaOne()
		runTests()
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
	runTests()

def runTests():
	try:
		timeFile = open(f"{Options.output}_times.csv", 'w')
		resultsFile = open(f"{Options.output}_results.csv", 'w')
		with open(f"{Options.folder}/models_and_properties", 'r') as mps:
			for line in mps:
				if line.strip()[0] == '#':
					continue
				modelFile, propertiesFile = line.split(',')
				modelFile = modelFile.strip()
				propertiesFile = propertiesFile.strip()
				if not propertiesFile.endswith('.csl'):
					warn("Properties file may not be a CSL properties file.")
				if (not modelFile.endswith('.prism')) and (not modelFile.endswith('.sm')):
					warn("Modules file may not be a PRISM modules file.")
				info(f"Testing line {modelFile} and {propertiesFile}")
				i = 0
				for command in commands:
					start = time.time()
					info(f"Running command:\n\t{command}", True)
					try:
						currentCommand = command.replace("$MODEL_FILE", modelFile)
						currentCommand = currentCommand.replace("$PROPERTIES_FILE", propertiesFile)
						completedProcess = subprocess.run(currentCommand.split(' '), capture_output=True)
						retCode = completedProcess.returncode
						# retCode = os.system(f"export MODEL_FILE={modelFile} && export PROPERTIES_FILE={propertiesFile} && {command}")
						# Get the results
						pMin = None
						pMax = None
						outStream = completedProcess.stderr if command.startswith("sstamina") else completedProcess.stdout
						for line in outStream.split('\n'):
							if resultsString[i]["min"] in line:
								pMin = float(line.strip().replace(resultsString[i]["min"], ""))
							elif resultsString[i]["max"] in line:
								pMax = float(line.strip().replace(resultsString[i]["max"], ""))
						if retCode != 0:
							warn("Recieved non-zero exit code for command")
					except Exception as e:
						err("Unable to run command:\n\t{command}.\nGot error:\n\t{e}")
					end = time.time()
					timeFile.write(f"{end - start}")
					print(f"Took time {end - start} s", file=sys.stderr)
					i += 1
		timeFile.close()
		resultsFile.close()
	except Exception as e:
		err(f"Caught exception when trying to test:\n\t{e}")

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
	parser.add_argument('-f', '--folder', help="Folder where to find the file models_and_properties")
	parser.add_argument('-o', '--output', help="File to output results to. Will be suffixed with _times.csv and _results.csv (default output)")
	parser.add_argument('-s', '--silent', help="Emit no output", action="store_true")
	args = parser.parse_args()
	processArgs(args)
