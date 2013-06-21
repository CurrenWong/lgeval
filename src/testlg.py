################################################################
# testlg.py
#
# Test program for label graph class.
#
# Authors: R. Zanibbi, H. Mouchere
#	June, 2012
# Copyright (c) 2012, Richard Zanibbi and Harold Mouchere
################################################################
from lg import Lg
#import smallGraph
import SmGrConfMatrix

#from bestBG import *

def loadFiles(testfiles):
	for nextFile in testfiles:
		print('[ FILE: ' + nextFile + ' ]')
		n = Lg(nextFile)
		print(n)
		print(n.csv())

def testInvalidFiles(testfiles):
	print("--TESTING INVALID FILE INPUT")
	loadFiles(testfiles)

def testInput(testfiles):
	print("-- TESTING FILE INPUT")
	loadFiles(testfiles)

def testshortCuts(compareFiles):
	print('\n--TESTING SHORTCUTS')
	for next in compareFiles:
		n1 = Lg(next[0])
		n2 = Lg(next[1])
		print('>> ' + next[0] + ' vs. ' + next[1])
		out1 = n1.compare(n2)
		if out1[0][8][1] == 0:
			print ("OK")
		else:
			print str(out1)

def labelComparison(file1,file2):
	print('\n[ Comparing Labels for FILE: ' + file1 + ' and ' + file2 + ' ]')
	n1 = Lg(file1)
	n2 = Lg(file2)
	print('>> ' + file1 + ' vs. ' + file2)
	out1 = n1.compare(n2)
	for el in out1[0]:
		print('  ' + str(el))
	print('  Node diffs: ' + str(out1[1]))
	print('  Edge diffs: ' + str(out1[2]))
	print('  SegEdge diffs: ' + str(out1[3]))
	print('  Correct Segments: ' + str(out1[4]))

	print('>> ' + file2 + ' vs. ' + file1)
	out2 = n2.compare(n1)
	for el in out2[0]:
		print('  ' + str(el))
	print('  Node diffs: ' + str(out2[1]))
	print('  Edge diffs: ' + str(out2[2]))
	print('  SegEdge diffs: ' + str(out2[3]))
	print('  Correct Segments: ' + str(out1[4]))

def testLabelComparisons(compareFiles):
	print('\n--TESTING METRICS AND ERROR LOCALIZATON')
	for next in compareFiles:
		labelComparison(next[0],next[1])

def testEmpty(emptyFiles):
	print('\n--TESTING EMPTY FILES')
	for next in emptyFiles:
		print("* " + next[0] + " vs. " + next[1])
		labelComparison(next[0],next[1])

	print('\n--TEST NON-EXISTENT FILE')
	notAFile = Lg('thisfiledoesnotexist')
	print("\nError flag set for missing file:" + str(notAFile.error))
	print(notAFile)


def testSegments(segFiles):
	print('\n--TESTING SEGMENTATION')
	for file in segFiles:
		print('\n[ Segmentation for FILE: ' + file + ' ]')
		n = Lg(file)
		(segmentPrimitiveMap, primitiveSegmentMap, noparentSegments, segmentEdges) = \
				n.segmentGraph()
		print('  SEGMENTS -> PRIMITIVES:\n\t' + str(segmentPrimitiveMap))
		print('  PRIMITIVES -> SEGMENTS:\n\t' + str(primitiveSegmentMap))
		print('  NON-PARENT SEGMENTS: ' + str(noparentSegments))
		print('  SEGMENT EDGES:\n\t' + str(segmentEdges))

def testTreeEdges(treeFiles):
	print('\n--TESTING TREE EDGE/LAYOUT TREE EXTRACTION')
	for file in treeFiles:
		print('\n[ Tree Edges for FILE: ' + file + ' ]')
		n = Lg(file)
		(rootNodes,tEdges,oEdges) = n.separateTreeEdges()
		print('  ROOT NODES: ' + str(rootNodes))
		print('  TREE EDGES: ' + str(tEdges))
		print('  NON-TREE EDGES:' + str(oEdges))

def testSummingGraphs(mergeFiles):
	print('\n--TESTS FOR ADDING NODE/EDGE LABEL VALUES')
	for ( file1, file2 ) in mergeFiles:
		print('\n[ Merging ' + file1 + ' and ' + file2 + ']')
		lg1 = Lg(file1)
		lg2 = Lg(file2)
		lg1.addWeightedLabelValues(lg2)
		print(lg1)
		print(lg1.csv())

		print('-- with graph weights 0.25 and 0.75')
		lg1 = Lg(file1)
		lg1.gweight = 0.25
		lg2 = Lg(file2)
		lg2.gweight = 0.75
		lg1.addWeightedLabelValues(lg2)
		print(lg1)
		print(lg1.csv())

def testMaxLabel(mergeFiles):
	print('\n--TESTS FOR SELECTING MAX. VALUE LABELS')
	for ( file1, file2 ) in mergeFiles:
		print('\n[ Selecting max labels from combined ' + file1 + \
				' and ' + file2 + ']')
		lg1 = Lg(file1)
		lg2 = Lg(file2)
		lg1.addWeightedLabelValues(lg2)
		lg1.selectMaxLabels()
		print(lg1)
		print(lg1.csv())

		print('-- with graph weights 0.25 and 0.75')
		lg1 = Lg(file1)
		lg1.gweight = 0.25
		lg2 = Lg(file2)
		lg2.gweight = 0.75
		lg1.addWeightedLabelValues(lg2)
		lg1.selectMaxLabels()
		print(lg1)
		print(lg1.csv())

def testGenAllBG(files):
	print('\n--TESTING GENERATION OF K BEST BG')
	for file in files:
		print('\n[ FILE: ' + file + ' ]')
		lg1 = Lg(file)
		blg = BestBG(lg1,5)
		blg.afficheDP()
		for i in range(5):
			print("BG top "+str(i))
			print(blg.getBG(i).csv())
		
	print ("END")
		
def testInvertValues(files):
	print('\n--TESTING INVERTING LABEL VALUES')
	for file in files:
		print('\n[ FILE: ' + file + ' ]')
		lg1 = Lg(file)
		print(lg1)
		print(lg1.csv())

		# Invert values.
		lg1.invertValues()
		print(lg1)
		print(lg1.csv())
		
		# And back to original values.
		lg1.invertValues()
		print(lg1)
		print(lg1.csv())

def testStructCompare(files):
	print('\n--TESTING STRUCT COMPARE')
	print " sub iterator (sizes 1 and 3): "
	g1 = Lg(files[0][0])
	for s in g1.subStructIterator([1,3]):
		print(s)
	print " sub iterator (sizes 2): "
	for s in g1.subStructIterator(2):
		print(s)
	print " sub comparision :"
	for ( file1, file2 ) in files:		
		g1 = Lg(file1) # ground-truth
		g2 = Lg(file2) # output
		print (str(g2.compareSubStruct(g1,4)))

def testSubGraphCounting(files):
	stat = SmGrConfMatrix.SmDict()
	mat = SmGrConfMatrix.ConfMatrix()
        segMat = SmGrConfMatrix.ConfMatrixObject()
	for ( fileGT, fileOUT ) in files:		
		gGT = Lg(fileGT)
		for s in gGT.subStructIterator([1,2,3,4]):
			stat.get(s,SmGrConfMatrix.Counter).incr()
		gOUT = Lg(fileOUT)
		for (gt,er) in gOUT.compareSubStruct(gGT,[2,3]):
			mat.incr(gt,er,("../"+fileOUT))
		for (seg,gt,er) in gOUT.compareSegmentsStruct(gGT,[2,3]):
                        segMat.incr(seg,gt,er,("../"+fileOUT))
	print "stat from left side expressions:"
	#print stat
	print "generate HTML in test.html" 
	out=open('Tests/test.html','w')
        out.write('<html xmlns="http://www.w3.org/1999/xhtml">')
	out.write('<h1> Substructure Stat </h1>')
	out.write(stat.toHTML())
	print "Confusion matrix when compared with right side ME"
	print mat
	out.write('<h1> Substructure Confusion </h1>')
	mat.toHTML(out)
	out.write('<h1> Substructure Confusion with at least 1 error </h1>')
	mat.toHTML(out,1)
	out.write('<h1> Substructure Confusion at oject level with 1 error or more </h1>')
	segMat.toHTML(out)
	out.write('</html>')
	out.close()


def main():
	validfiles = [ \
			'Tests/infile1', \
			'Tests/infile2', \
			'Tests/infile3', \
			'Tests/infile4', \
			'Tests/infile5', \
			'Tests/infile10'
		]

	shortCutFiles = [ \
			('Tests/segment3','Tests/segment3sc'), \
			('Tests/segment1','Tests/segment1sc'), \
			('Tests/segment2','Tests/segment2sc')
		]

	invalidfiles = [ \
			'Tests/infile6', \
			'Tests/infile7', \
			'Tests/infile8', \
			'Tests/infile9'
		]

	compareFiles = [ \
                #only errors with labels
			#('Tests/infile1','Tests/infile1a'), \
			('Tests/infile4','Tests/infile4a')
			#('Tests/infile4','Tests/infile4b'), \
                        # only errors with seg and layout
                        #('Tests/segment6','Tests/segment6erra'),\
                        #('Tests/segment6','Tests/segment6errb'),\
                        #('Tests/segment5','Tests/segment5erra'),\
                        #('Tests/segment5','Tests/segment5errb')
			#('Tests/res_001-equation006.lg','Tests/001-equation006.lg')
		]

	segFiles = [ \
			'Tests/infile1', \
			'Tests/infile4', \
			'Tests/infile5', \
			'Tests/segment1', \
			'Tests/segment2', \
			'Tests/segment3', \
			'Tests/segment4', \
			'Tests/segment5', \
			'Tests/segment6'
		]

	compareFilespaper = [ \
			('Tests/paperExampleGT','Tests/paperExampleErrA'), \
			('Tests/paperExampleGT','Tests/paperExampleErrB'), \
			('Tests/paperExampleGT','Tests/paperExampleErrC'), \
			('Tests/paperExampleGT','Tests/paperExampleErrD')
		]

	compareEmpty = [ \
			('Tests/infile1','Tests/emptyfile'),
			('Tests/infile11','Tests/emptyfile'),
			('Tests/infile1','Tests/infile11'),
			('Tests/infile1','Tests/infile3'),
			('Tests/emptyfile','Tests/paperExampleGT'),
		]

	mergeFiles = [ \
			('Tests/infile1','Tests/infile1'),
			('Tests/infile1','Tests/infile11'),
			('Tests/infile4','Tests/infile4a'),
			('Tests/infile4','Tests/infile4b'),
			('Tests/infile1', 'invalidfile')
		]
		
	filesForBestBG = [ \
			'Tests/infile4', \
			'Tests/infile5', \
			'Tests/infile5b'
		]
	# Input file tests.	
	# testInput(validfiles)
	#testInvalidFiles(invalidfiles)

	# Segmentation tests.
	# testSegments(segFiles)
	#testshortCuts(shortCutFiles)
	# Comparison tests.
	#testLabelComparisons(compareFiles)
	#testLabelComparisons(compareFilespaper)
	#testEmpty(compareEmpty)
	#testStructCompare([('Tests/2p2.lg','Tests/2p2a.lg')])
	testSubGraphCounting(compareFiles) #[('Tests/2p2.lg','Tests/2p2a.lg')])
	# Extracting trees (layout trees)
	# testTreeEdges(segFiles)

	# Merging label graphs
	#testSummingGraphs( mergeFiles )
	#testMaxLabel( mergeFiles )
	
	# generate all best BG
	#testGenAllBG(filesForBestBG)

	#testInvertValues( validfiles + [ 'Tests/invalidEdgeValue' ] )

main()
