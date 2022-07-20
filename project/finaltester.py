import os
import random
import argparse
import sut
import sys
import time


parser = argparse.ArgumentParser()
parser.add_argument("TIMEOUT", type=int, default=60)               #this will take timebudget
parser.add_argument("SEED", type=int, default=None)                    #this will take seed
parser.add_argument("DEPTH", type=int, default=100)                    #this will take depth
parser.add_argument("WIDTH", type=int, default=100)                    #this will take width
parser.add_argument("FAULT_CHECK", type=int, default=0)                #this will take fault check
parser.add_argument("COVERAGE_REPORT", type=int, default=0)            #this will take coverage report
parser.add_argument("DETAIL_OF_RUNNING", type=int, default=0)          #this will take detail of running

option = parser.parse_args()               # a object named pointer is made for this 
SEED  = option.SEED
TIMEOUT = option.TIMEOUT
DEPTH = option.DEPTH
WIDTH = option.WIDTH
FAULT_CHECK = option.FAULT_CHECK
COVERAGE_REPORT = option.COVERAGE_REPORT
DETAIL_OF_RUNNING = option.DETAIL_OF_RUNNING

#INITIAL_POP = option.INITIAL_POP
sut = sut.sut()
savedTest = None
failureCount = 0
actionCount = 0
countCover = {}
leastCover = None
vgoodTest = []
pCheck = 1
okTest = None
bugs = 0
bTest = False
width_actionCount = 0

rgen = random.Random()
rgen.seed(SEED)
			        #this will reset the system state
start = time.time()         #this will start the system time


while time.time() - start < TIMEOUT:
	sut.restart()
	
	
        for s in xrange(0, WIDTH):                                  #this will go till the width
		action = sut.randomEnabled(rgen)
		yes = sut.safely(action)
		width_actionCount = 1 + width_actionCount
		
		for s in xrange(0, DEPTH):                          #this will go till the depth
			action = sut.randomEnabled(rgen)
			yes = sut.safely(action)
			actionCount = 1+ actionCount


			if (not bTest) and (leastCover<>None) and (leastCover in sut.currStatements()):
				okTest = sut.state()
				vgoodTest.append(okTest)
			if len(sut.newStatements()) > 0:
				okTest = sut.state()
                        	bTest = True
              			print "New Statements Found",sut.newStatements()
			elapsed = time.time() - start
			if DETAIL_OF_RUNNING:
				if sut.newBranches() !=set([]):
					for b in sut.newBranches():
						print elapsed,len(sut.allBranches()),"New Branch",b

			if not yes:
                               

				bugs = bugs + 1
				print"This is a failure"
				print sut.failure()
				F = sut.reduce(sut.test(), sut.fails, True, True)
				sut.prettyPrintTest(F)
				print sut.failure()
				if FAULT_CHECK:
					filename = "failure" + str(bugs) + ".test"
					sut.saveTest(F,filename)

				

		
	if COVERAGE_REPORT:
		sut.internalReport()
		print "\n       **********  CS569 Final Report  **********       \n"
		print "Number of bugs found: " + str(bugs)
		print "Number of actions: " + str(actionCount)
		print "Number of width action count: " + str(width_actionCount)
		print "Total elapsed time: " + str(elapsed)
		print len(sut.allBranches()),"BRANCHES COVERED"
		print len(sut.allStatements()),"STATEMENTS COVERED"
		
	if (rgen.random()>pCheck) and (okTest <> None):
		sut.backtrack(okTest)
	        bTest = False

		
	





		



