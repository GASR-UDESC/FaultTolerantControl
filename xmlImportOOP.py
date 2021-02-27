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
from elementClasses import automata,event,state
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


def xmlAutomataImport (filename):
	TREE = ET.parse(filename)
	if (TREE is None):
		return None

	#Obtaining XML root = 'data'
	root = TREE.getroot()
	if (root is None):
		return None

	#Creating an empty automata_information list
	automata_information = [] 
	temporaryList = []

	#Adding automata_information name
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

		#  	transitionNumber += 1

		#New Adding automata_information transitions
		automata_information.append([])
		#transitionNumber = 0
		last_sourceID = -1		
		for transition in data.findall('transition'):
			listIndex = -1
			sourceID = int(transition.get('source'))
			targetID = int(transition.get('target'))
			eventID = int(transition.get('event'))

			if sourceID != last_sourceID:		 			 		
				last_sourceID = sourceID
				counterIndex = 0
				for stateInfo in temporaryList[0]:
					if stateInfo[0] == sourceID:
						sourceLabel = stateInfo[1]
						# print(sourceLabel)
						# print('encontrou!') 	
						break
				for sublist in automata_information[3]:		 			
					if sourceLabel == sublist[0][0][0]:
						listIndex = automata_information[3].index(sublist)
						break
					counterIndex += 1
				if listIndex == -1:		
					#Creating a new sublist in transitions list
					automata_information[3].append([])
					listIndex = counterIndex

			for stateInfo in temporaryList[0]:
				if stateInfo[0] == sourceID:
					automata_information[3][listIndex].append([[stateInfo[1]]])	 	
					break

			for eventInfo in temporaryList[1]:
				if eventInfo[0] == eventID:
					automata_information[3][listIndex][-1].append(eventInfo[1])	 	
					break

			for stateInfo in temporaryList[0]:
				if stateInfo[0] == targetID:
					automata_information[3][listIndex][-1].append([stateInfo[1]])	 	
					break

	return automata_information 


def build_automata(automata_information):
	for x in automata1_information:
		print(x,"\n\nLINHA\n\n")

	###############################################
	#Distributing Automata 1 information in classes

	#Declaring supporting variables
	list_of_states = []
	list_of_events = []
	stateID_model = 'A1_S'	#class ID representation A1S0 (Automata 1 State 0)...
	eventID_model = 'A1_E'	#class ID representation A1S0 (Automata 1 State 0)...

	#Extracting information of the states [[LABEL], MARKING, INITIAL]
	counterID = 0
	for state_info in automata1_information[1]:
		stateID = stateID_model + str(counterID)	 
		list_of_states.append(stateID)				
		stateLabel = state_info[0]
		stateMarking = state_info[1]
		stateInitial = state_info[2]
		outputTransition = []
		for transition_info in automata1_information[3][counterID]:
			outputTransition.append([transition_info[2], transition_info[1]])
		counterID += 1