#!/usr/bin/python
#coding: utf-8

'''
Code for Python 3
Author: Herbert Leitão
Date Version 1: 12/02/2021
Comments: Module created for importing and organizing data obtained from IDES files
'''

'''
STANDARD FOR automata_information/AUTOMATA (REPRESENTATION IN 'ELEMENTCLASSES.PY' LIBRARY)
automata_information = 
    ['sensor',							# SYSTEM NAME
    [[['A'],True/False,True/False]...	# [["LABEL"], "MARKING", "INITIAL"]
    [['Son',True/False,True/False]...	# ["LABEL", "CONTROLLABLE", "OBSERVABLE"]
    [[['A'],'Son',['B']]...				# ["SOURCE STATE", "EVENT", "TARGET STATE"]
    ]
'''

from copy import deepcopy as dcp, copy as cp
import xml.etree.ElementTree as ET
import re

def str2list(string):
	string1 = string
	string2 = ''
	for c in string1:
	    if c != '(':
	        if c != ')':
	            string2 += c
	return string2

def str2listB(string):
	string1 = string
	#print(string1)	
	newLabel = list()	
	string2 = ''	
	for c in string1:
		if c != '(' and c != ')':			
			if c == ' ':
				continue
			elif c == ',':
				newLabel.append(string2)
				string2 = ''				
			else:
				string2 += c
	newLabel.append(string2)
	return newLabel

def xmlAutomataImport (filename, **kwargs):
	label = kwargs.get('label')

	TREE = ET.parse(filename)
	if (TREE is None):
		return None

	#Obtaining XML root (<model>)
	root = TREE.getroot()
	if (root is None):
		return None	

	#Creating an empty automata_information list
	automata_information = [] 
	temporaryList = []

	#Adding automata_information name (<model id=*>)
	automata_information.append(root.get('id'))

	
	for data in root.findall('data'):
		#Adding automata_information states
		automata_information.append([])
		temporaryList.append([])
		stateNumber = 0
		for state in data.findall('state'):
			#Creating a new sublist in states list
			automata_information[1].append([])
			#Adding automata_information state name
			if label == 'list':
				stateName = str2listB(state.find('name').text)
				automata_information[1][stateNumber].append(stateName)
				#print(stateName)
			else:
				stateName = str2list(state.find('name').text)
				automata_information[1][stateNumber].append([stateName])
			temporaryList[0].append([int(state.get('id')),stateName])
			#Adding information about state (Initial/Marked)
			for properties in state.findall('properties'):
				if properties.find('marked') is not None:
					automata_information[1][stateNumber].append(True) 
				else:					
					automata_information[1][stateNumber].append(False) 

				if properties.find('initial') is not None:
					automata_information[1][stateNumber].append(True) 
				else:					
					automata_information[1][stateNumber].append(False)

			stateNumber += 1

		#Adding automata_information events
		automata_information.append([])
		temporaryList.append([])
		eventNumber = 0
		for event in data.findall('event'):
			#Creating a new sublist in events list
			automata_information[2].append([])
			#Adding automata_information event name
			automata_information[2][eventNumber].append(event.find('name').text)
			temporaryList[1].append([int(event.get('id')),event.find('name').text])
			#Adding information about state (Initial/Marked)
			for properties in event.findall('properties'):
				if properties.find('controllable') is not None:
					automata_information[2][eventNumber].append(True) 
				else:					
					automata_information[2][eventNumber].append(False) 

				if properties.find('observable') is not None:
					automata_information[2][eventNumber].append(True) 
				else:					
					automata_information[2][eventNumber].append(False)

			eventNumber += 1
		# print(automata_information[1])
		# print(automata_information[2])
		# print(temporaryList)
		# #Adding automata_information transitions
		# automata_information.append([])
		# transitionNumber = 0
		# for transition in data.findall('transition'):
		# 	#Creating a new sublist in transitions list
		#  	automata_information[3].append([])

		#  	sourceID = int(transition.get('source'))
		#  	targetID = int(transition.get('target'))
		#  	eventID = int(transition.get('event'))
		 	
		#  	for stateInfo in temporaryList[0]:
		#  		if stateInfo[0] == sourceID:
	 # 				automata_information[3][transitionNumber].append([stateInfo[1]])	 	
	 # 				break

	 # 		for eventInfo in temporaryList[1]:
		#  		if eventInfo[0] == eventID:
	 # 				automata_information[3][transitionNumber].append(eventInfo[1])	 	
	 # 				break

	 # 		for stateInfo in temporaryList[0]:
		#  		if stateInfo[0] == targetID:
	 # 				automata_information[3][transitionNumber].append([stateInfo[1]])	 	
	 # 				break

		#New Adding automata_information transitions		
		#automata_information.append([])
		group = []
		# for x in range(automata_information[1].index(automata_information[1][-1])+1):
		# 	group.append([])
		for x in range(len(automata_information[1])):
			group.append([])	

		last_sourceID = -1		
		for transition in data.findall('transition'):
			listIndex = -1
			sourceID = int(transition.get('source'))
			targetID = int(transition.get('target'))
			eventID = int(transition.get('event'))

			if sourceID != last_sourceID:		 			 		
				last_sourceID = sourceID
				counterIndex = 0
				for stateInfo in temporaryList[0]: # temporaryList[0] = [[state_ID, label_ID]...
					if stateInfo[0] == sourceID:
						sourceLabel = stateInfo[1]
						stateIndex = temporaryList[0].index(stateInfo)
						# print(sourceLabel)
						# print('encontrou!') 	
						break
				# #### eliminar
				# for sublist in automata_information[3]:		 			
				# 	if sourceLabel == sublist[0][0][0]:
				# 		listIndex = automata_information[3].index(sublist)
				# 		break
				# 	counterIndex += 1
				# if listIndex == -1:		
				# 	#Creating a new sublist in transitions list
				# 	automata_information[3].append([])
				# 	listIndex = counterIndex
				# #### fim eliminar

			for stateInfo in temporaryList[0]:
				if stateInfo[0] == sourceID:
					#automata_information[3][listIndex].append([[stateInfo[1]]])
					if label == 'list':
						group[stateIndex].append([stateInfo[1]])
						break
					else:
						group[stateIndex].append([[stateInfo[1]]])
						break

			for eventInfo in temporaryList[1]:
				if eventInfo[0] == eventID:
					#automata_information[3][listIndex][-1].append(eventInfo[1])
					group[stateIndex][-1].append(eventInfo[1])	 	
					break

			for stateInfo in temporaryList[0]:
				if stateInfo[0] == targetID:
					#automata_information[3][listIndex][-1].append([stateInfo[1]])
					if label == 'list':
						group[stateIndex][-1].append(stateInfo[1])
						break
					else:
						group[stateIndex][-1].append([stateInfo[1]])
						break
	automata_information.append(group)
	# print('')
	# print('automata_information[3]')
	# for x in automata_information[3]:
	# 	print(x)
	# print('')
	# print('group')
	# for x in group:
	# 	print(x)

	return automata_information 