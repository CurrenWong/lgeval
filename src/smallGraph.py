################################################################
# smallGraph.py
#
# Simpler graph class for use with structure confusion 
# histograms.
#
# Author: Harold Mouchere
# Copyright (c) 2013 Richard Zanibbi and Harold Mouchere
################################################################


# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 04:13:40 2013

@author: Harold
"""

import itertools
import cmath
from math import sqrt
import compareTools

class SmallGraph(object):
	"""Class for small graphs. The individual nodes
	and edges have one associated label. 
	Only for small graphes because algorithms are not optimized.
	see igraph or graph_tool module for bigger graph"""

	# Define graph data elements ('data members' for an object in the class)
	__slots__ = ('nodes','edges', 'rednodes', 'rededges')

	##################################
	# Constructors (in __init__)
	##################################
	def __init__(self,*args): 
		""" init the small graph with 2 lists:
			- list of nodes (id, label)
			- list of edges (id,id, label)
		"""
		self.nodes = {}
		self.edges = {}
		self.rednodes = set()
		self.rededges = set()
		if(len(args) == 2 and isinstance(args[0],list) and isinstance(args[1],list)):
			for (i,l) in args[0]:
				self.nodes[i] = l
			for (i1,i2,l) in args[1]:
				self.edges[(i1,i2)] = l
	
	def printLG(self):
		for k in self.nodes.keys():
			print ("N,"+str(k)+","+(",".join(self.nodes[k])) + ",1.0")
		for (e1,e2) in self.edges.keys():
			print ("E,"+str(e1)+","+str(e2)+","+(",".join(self.edges[(e1,e2)])) + ",1.0")
	
	def __str__(self):
		"""returns a string with nodes and edges. Format:
			nbNodes,id1,lab1,id2,lab2... ,nbedges,from1,to1,label1, from2, to2, label2,..."""
		out = str(len(self.nodes.keys()))
		for k in self.nodes.keys():
			out = out + ","+str(k)+","+str(self.nodes[k])
		out = out + ","+str(len(self.edges.keys()))
		for (e1,e2) in self.edges.keys():
			out = out + ","+str(e1)+","+str(e2)+","+str(self.edges[(e1,e2)])
		return out
		
	def fromStr(self, inStr):
		tab = inStr.split(',')
		nnode = int(tab[0])
		i = nnode*2+1
		for n in range(1,i,2):
			self.nodes[str(tab[n])] = str(tab[n+1])
		nedg = int(tab[i])
		for n in range(i+1, i+1+nedg*3,3 ):
			a = str(tab[n])
			b = str(tab[n+1])			
			self.edges[(a,b)] = str(tab[n+2])
	def iso(self,osg):
		"""true if the two graphs are isomorphisms"""
		if(len(self.nodes.keys()) != len(osg.nodes.keys()) or \
			len(self.edges.keys()) != len(osg.edges.keys())):
				return False
		myLabels = self.nodes.values() + self.edges.values()
		hisLabels = osg.nodes.values() + osg.edges.values()
		#myLabels.sort()
		#hisLabels.sort()
		#if(myLabels != hisLabels):
		#print myLabels
		myLabelsFlat = [item for sublist in myLabels for item in sublist]
		hisLabelsFlat = [item for sublist in hisLabels for item in sublist]
		if compareTools.cmpNodes(myLabelsFlat, hisLabelsFlat) != (0,[]):
			return False
		#So they seems to be isomorphims (same label counts)
		#let's try all permutation of nodes
		for m in itertools.permutations(self.nodes.keys()):
			if self.equal(osg,m):
				return True
		return False

	def equal(self,osg, mapping):
		"""using the mapping list, check if the nodes and edges have the same labels
		The mapping is a list of self.nodes keys, the order give the mapping
		the number of nodes have to be same"""
		mynodes = self.nodes.keys()
		nb = len(mynodes)
		onodes = osg.nodes.keys()		
		if(nb != len(onodes) and nb != len(mapping)):
			return False
		hisNode = dict(zip(mapping, onodes))
		#print "Map : " + str(hisNode)
		#first check the node labels
		for (my,his) in hisNode.iteritems():
			#if(self.nodes[my] != osg.nodes[his]):
			if(compareTools.cmpNodes(self.nodes[my] ,osg.nodes[his]) != (0,[])):
				#print str((self.nodes[my] ,osg.nodes[his])) + ' are diff'
				return False
		#then check the edges
		for (a,b) in self.edges.iterkeys():
			#id from the other through the mapping
			(oa,ob) = (str(hisNode[a]),str(hisNode[b]))
			#print str((a,b)) + " <=> " + str((oa,ob))
			#if the edge does not exist or has a different label => missmatch
			if not (oa,ob) in osg.edges.keys():
				#print str((oa,ob)) + " not in osg"
				return False
			#if self.edges[(a,b)] != osg.edges[(oa,ob)]:
			if compareTools.cmpEdges(self.edges[(a,b)], osg.edges[(oa,ob)])!= (0,[]):
				#print self.edges[(a,b)] + " != " + osg.edges[(oa,ob)]	
				return False
		return True

	def __eq__(self,o):
		return self.iso(o)
	def toSVG(self, size = 200, withDef = True):
		""" Generate a SVG XML string which draw the nodes (spread on a circle)
		and edges with all label. 
		Param size : the size of svg image (square) 
		Param withDef : if True generate the definition of the arrow (needed only once in a HTML file)"""
		svg = '<svg xmlns="http://www.w3.org/2000/svg" width="'+str(size)+'" height="'+str(size)+'">\n'
		n = len(self.nodes)
		r = size / 10
		R = (size - 2*r) /2
		if withDef:
			svg = svg + '<defs>\
    <marker id="Triangle"\
      viewBox="0 0 10 10" refX="10" refY="5" \
      markerUnits="strokeWidth"\
      markerWidth="'+str(r/2)+'" markerHeight="'+str(r/2)+'"\
      orient="auto">\
      <path d="M 0 0 L 10 5 L 0 10 z" /> </marker>  </defs>'
		xy = [  (cmath.rect(R,2 * x* cmath.pi/n).real + size/2,cmath.rect(R,2 * x* cmath.pi/n).imag + size/2) for x in range(n)]
		i = 0
		findXY = {}
		for k in self.nodes.keys():
			color = 'blue'
			if(k in self.rednodes):
				color = 'red'
			svg = svg + '<circle cx="'+str(xy[i][0]) + '" cy="'+str(xy[i][1]) + '"r="'+str(r)+'" fill="none" stroke="'+color+'"/>\n'
			lab = ",".join(self.nodes[k])
			svg = svg + '<text 	x="'+str(xy[i][0]-0.75*r) + '" y="'+str(xy[i][1]+r/2) + '"	font-family="Arial"'+'font-size="'+str(1.5*r / sqrt(max([len(lab),1])))+'"'+'>' 
			svg = svg + lab + '</text>\n'
			findXY[k] = i
			i = i +1
		R = R - r #the edges start on a smaller circle
		xy = [  (cmath.rect(R,2 * x* cmath.pi/n).real + size/2,cmath.rect(R,2 * x* cmath.pi/n).imag + size/2) for x in range(n)]
		R = R - r #the labels are on a smaller circle
		#xyL = [  (cmath.rect(R,2 * x* cmath.pi/n).real + size/2,cmath.rect(R,2 * x* cmath.pi/n).imag + size/2) for x in range(n)]
		for (a,b) in self.edges.keys():
			ai = findXY[a]			
			bi = findXY[b]
			color = 'black'
			if((a,b) in self.rededges):
				color = 'red'
			svg = svg + '<line x1="'+str(xy[ai][0]) + '" y1="'+str(xy[ai][1]) + '" x2="'+str(xy[bi][0]) + '" y2="'+str(xy[bi][1]) + '" stroke="'+color+'" marker-end="url(#Triangle)" />\n'
			lab = ",".join(self.edges[(a,b)])
			svg = svg + '<text 	x="'+str((xy[ai][0] + xy[bi][0])/2) + '" y="'+str((xy[ai][1]+ xy[bi][1])/2) + '"	font-family="Arial"'+'font-size="'+str(r / sqrt(max([len(lab),1])))+'"'+'>' 
			svg = svg + lab + '</text>\n'
		return svg + '</svg>\n'
		
		
def test():
	sg=SmallGraph()
	sg.nodes["1"] = "A"
	sg.nodes["2"] = "B"
	sg.nodes["3"] = "C"
	sg.edges[("1","2")] = "R"
	sg.edges[("1","3")] = "U"
	sg.printLG()
	line = str(sg)
	print line
	sg2 = SmallGraph()
	sg2.fromStr(line)
	sg2.printLG()
	print "Are they Iso (Y) : " + (str(sg == sg2))
	sg2.edges[('2','3')] = 'R'
	print "Add an edge (2,3,R) on right side "
	print "Are they Iso (N) : " + (str(sg == sg2))
	sg.edges[('2','3')] = 'U'
	print "Add an edge (2,3,U) on left side "
	print "Are they Iso (N) : " + (str(sg == sg2))
	print "change edge (2,3) to R on left side "
	sg.edges[('2','3')] = 'R'	
	print "Are they Iso (Y) : " + (str(sg == sg2))
	print "New graph : "
	sg2 = SmallGraph([("1","B"),("2","C"), ("3","A")], [("3", "1", "R"), ("3", "2", "U")])
	sg2.printLG()
	print "Are they Iso (N) : " + (str(sg.iso(sg2)))
	sg2.edges[('1','2')] = 'U'
	print "Add an edge (2,1,U) on right side "
	print "Are they Iso (N) : " + (str(sg.iso(sg2))) + (str(sg2.iso(sg)))
	sg2.edges[('1','2')] = 'R'
	print "Change edge (2,1)  to R on right side "
	print "Are they Iso (Y) : " + (str(sg.iso(sg2)))+ (str(sg2.iso(sg)))
	print " SVG test : "
	sg.nodes["1"] = "Test"
	print sg.toSVG()
				
