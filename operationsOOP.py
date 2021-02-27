# -*- coding: utf-8 -*-
'''
Code for Python 3
Author: Herbert Leitão
Date Version: 17/02/2021
Comments: DES operations in OOP
'''

from elementClasses import automata, state, event
#from goto import goto, label

def AC_Function(stateLabel):
	for stateID in list_of_states:
		if globals()[stateID].label == stateLabel:
			for transition_info in globals()[stateID].output_transitions:
				if transition_info[0] not in AC_states:
					AC_states.append(transition_info[0])
					AC_Function(transition_info[0])

def COAC_Function(stateLabel):
	for stateID in list_of_states:
		if globals()[stateID].label == stateLabel:
			for transition_info in globals()[stateID].input_transitions:
				if transition_info[0] not in COAC_states:
					COAC_states.append(transition_info[0])
					COAC_Function(transition_info[0])

def intersection(lst1, lst2): 
	lst3 = [value for value in lst1 if value in lst2] 
	return lst3 

def syncNF(automataID,SU,NF):
	list_of_results = [automataID,'NaN',[],[],[],[]]	#[automataID, automata class, [states ID], ...
												# ...[classes of states], [events ID], [classes of events]
	##Reading Test
	##########################################################
	print('-'*25)
	print('SA')
	print('-'*25)
	print(SU[1].label)
	print('-'*25)
	for x in SU[3]:
		print(str(x.label) + '=>' + str(x.output_transitions))
	print('-'*25)
	for x in SU[5]:
		print(x.label)
	print('-'*25)

	print('-'*25)
	print('FA')
	print('-'*25)
	print(NF[1].label)
	print('-'*25)
	for x in NF[3]:
		print(str(x.label) + '=>' + str(x.output_transitions))
	print('-'*25)
	for x in NF[5]:
		print(x.label)
	print('-'*25)
	print("DONE READING TEST==============================")
	##########################################################
	##########################################################

	#Intersection of events between SA and FA
	intersectionSet = [] #                                      eventos de falha e idle
	for eventNF in NF[5]:
		for eventSU in SU[5]:	
			if eventNF.label == eventSU.label:
				intersectionSet.append(eventNF.label)
	print('-'*25)
	print('Intersection Set => ' + str(intersectionSet))
	#                                                            pegando as falhas que fazem o NY progredir

	#Declaring supporting variables
	global list_of_states
	global AC_states
	#global COAC_states
	list_of_states = []
	list_of_events = []
	#marked_states = []
	AC_states = []
	#COAC_states = []

	nf_initial=None
	for check_initial in NF[3]:
		if check_initial.is_initial == True:
			nf_initial=check_initial
			break


	#isso aqui não vai mais
	'''
	#Finding the fault event
	for event in NF[5]:
		#print(event.is_a_fault)
		if event.is_a_fault:
			faultEventLabel = event.label		
			faultEventID = FA[4][FA[5].index(event)]
			print('-'*25)
			print('Fault Event => ' + str(faultEventLabel))
			# print(faultEventID)
			eventID = automataID + '_E0' #For the fault event
			list_of_events.append(eventID)
			list_of_results[5].append(event)
			break	
	'''

	counterID=0
	for stateSA in SU[3]:
		stateID = automataID + '_S' + str(counterID)
		list_of_states.append(stateID)
		stateLabel = stateSA.label + nf_initial.label
		stateMarking = bool(stateSA.is_marked * nf_initial.is_marked)
		stateInitial = bool(stateSA.is_initial * nf_initial.is_initial)
		# if stateMarking:
		# 	marked_states.append(stateID)
		if stateInitial:
			initial_stateID = stateID 

		outputTransition = []
		for transition_infoSA in stateSA.output_transitions:
			if transition_infoSA[1] not in intersectionSet:
				outputTransition.append([transition_infoSA[0] + nf_initial.label, transition_infoSA[1]])
			else:
				nf_initial=NF[3][1]
				for transition_infoFA in nf_initial.output_transitions:
					if transition_infoSA[1] == transition_infoFA[1]:
						outputTransition.append([transition_infoSA[0] + transition_infoFA[0], transition_infoSA[1]])
						break
		for transition_infoFA in nf_initial.output_transitions:
			if transition_infoFA[1] in intersectionSet:
				outputTransition.append([stateSA.label + transition_infoFA[0], transition_infoFA[1]])
				break
		counterID += 1

		#Generating the state class
		globals()[stateID] = state(stateLabel, stateMarking, stateInitial, output_transitions = outputTransition, input_transitions = [])
		list_of_results[3].append(globals()[stateID])

	#Syncronizing states	
	'''counterID = 0
	for stateFA in FA[3]:
		for stateSA in SA[3]:
			stateID = automataID + '_S' + str(counterID)
			list_of_states.append(stateID)
			stateLabel = stateSA.label + stateFA.label
			stateMarking = bool(stateSA.is_marked * stateFA.is_marked)
			stateInitial = bool(stateSA.is_initial * stateFA.is_initial)
			# if stateMarking:
			# 	marked_states.append(stateID)
			if stateInitial:
				initial_stateID = stateID 

			outputTransition = []
			for transition_infoSA in stateSA.output_transitions:
				if transition_infoSA[1] not in intersectionSet:
					outputTransition.append([transition_infoSA[0] + stateFA.label, transition_infoSA[1]])
				else:
					for transition_infoFA in stateFA.output_transitions:
						if transition_infoSA[1] == transition_infoFA[1]:
							outputTransition.append([transition_infoSA[0] + transition_infoFA[0], transition_infoSA[1]])
							break
			for transition_infoFA in stateFA.output_transitions:
				if transition_infoFA[1] == faultEventLabel:
					outputTransition.append([stateSA.label + transition_infoFA[0], faultEventLabel])
					break
			counterID += 1

			#Generating the state class
			globals()[stateID] = state(stateLabel, stateMarking, stateInitial, 
				output_transitions = outputTransition, input_transitions = [])
			list_of_results[3].append(globals()[stateID])'''

	#Updating input transitions
	for source_state in list_of_states:
		for transition_info in globals()[source_state].output_transitions:
			for target_state in list_of_states:
				if globals()[target_state].label == transition_info[0]:
					globals()[target_state].input_transitions.append(
						[globals()[source_state].label, transition_info[1]])
					break

	print(globals()[initial_stateID].label)
	AC_states.append(globals()[initial_stateID].label)
	for transition_info in globals()[initial_stateID].output_transitions:
		if transition_info[0] not in AC_states:
			AC_states.append(transition_info[0])
			AC_Function(transition_info[0])

	for stateID in reversed(list_of_states):
		if globals()[stateID].label not in AC_states:
			stateIndex = list_of_states.index(stateID)
			del list_of_results[3][stateIndex]
			list_of_states.remove(stateID)
	list_of_results[2] = list_of_states

	counterID = 0
	print('-'*5 + 'States after AC operation' + '-'*5)
	print('-'*40)
	for x in list_of_results[3]:		
		print('(' + str(counterID) + ') ' + 'stateID = ' + str(x.label))
		print('stateMarking = ' + str(x.is_marked))
		print('stateInitial = ' + str(x.is_initial))
		print('inputTransition = ' + str(x.input_transitions))
		print('outputTransition = ' + str(x.output_transitions))
		print('-'*25)
		counterID += 1

	#Generating the event class
	counterID = 1
	listIndex = len(SU[4])
	for n in range(listIndex):
		eventID = automataID + '_E' + str(counterID)
		list_of_events.append(eventID)
		counterID += 1

	list_of_results[4] = list_of_events
	list_of_results[5] += SU[5]

	#Generating automata model
	#Labelling the automata
	automataLabel = automataID

	globals()[automataID] = automata(automataLabel, list_of_states, list_of_events, 'NaN')
	list_of_results[0] = automataID
	list_of_results[1] = globals()[automataID]

	return list_of_results

def syncFault(automataID, SA, FA):
	list_of_results = [automataID,'NaN',[],[],[],[]]	#[automataID, automata class, [states ID], ...
												# ...[classes of states], [events ID], [classes of events]
	##Reading Test
	##########################################################
	print('-'*25)
	print('SA')
	print('-'*25)
	print(SA[1].label)
	print('-'*25)
	for x in SA[3]:
		print(str(x.label) + '=>' + str(x.output_transitions))
	print('-'*25)
	for x in SA[5]:
		print(x.label)
	print('-'*25)

	print('-'*25)
	print('FA')
	print('-'*25)
	print(FA[1].label)
	print('-'*25)
	for x in FA[3]:
		print(str(x.label) + '=>' + str(x.output_transitions))
	print('-'*25)
	for x in FA[5]:
		print(x.label)
	print('-'*25)
	##########################################################
	##########################################################

	#Intersection of events between SA and FA
	intersectionSet = []
	for eventFA in FA[5]:
		for eventSA in SA[5]:	
			if eventFA.label == eventSA.label:
				intersectionSet.append(eventFA.label)
	print('-'*25)
	print('Intersection Set => ' + str(intersectionSet))

	#Declaring supporting variables
	global list_of_states
	global AC_states
	#global COAC_states
	list_of_states = []
	list_of_events = []
	#marked_states = []
	AC_states = []
	#COAC_states = []

	#Finding the fault event
	for event in FA[5]:
		#print(event.is_a_fault)
		if event.is_a_fault:
			faultEventLabel = event.label		
			faultEventID = FA[4][FA[5].index(event)]
			print('-'*25)
			print('Fault Event => ' + str(faultEventLabel))
			# print(faultEventID)
			eventID = automataID + '_E0' #For the fault event
			list_of_events.append(eventID)
			list_of_results[5].append(event)
			break	

	#Syncronizing states	
	counterID = 0
	for stateFA in FA[3]:
		for stateSA in SA[3]:
			stateID = automataID + '_S' + str(counterID)
			list_of_states.append(stateID)				
			stateLabel = stateSA.label + stateFA.label
			stateMarking = bool(stateSA.is_marked * stateFA.is_marked)
			stateInitial = bool(stateSA.is_initial * stateFA.is_initial)
			# if stateMarking:
			# 	marked_states.append(stateID)
			if stateInitial:
				initial_stateID = stateID 

			outputTransition = []
			# for transition_infoFA in stateFA.output_transitions:
			# 	#print(transition_infoFA[1])
			# 	if transition_infoFA[1] == faultEventLabel:					
			# 		#print('fault')
			# 		outputTransition.append([stateSA.label + transition_infoFA[0], transition_infoFA[1]])
			for transition_infoSA in stateSA.output_transitions:
				if transition_infoSA[1] not in intersectionSet:
					outputTransition.append([transition_infoSA[0] + 
						stateFA.label, transition_infoSA[1]])					
				else:
					for transition_infoFA in stateFA.output_transitions:
						if transition_infoSA[1] == transition_infoFA[1]:
							outputTransition.append([transition_infoSA[0] + 
								transition_infoFA[0], transition_infoSA[1]])
							break
			for transition_infoFA in stateFA.output_transitions:
				if transition_infoFA[1] == faultEventLabel:
					outputTransition.append([stateSA.label + transition_infoFA[0], faultEventLabel])
					break			

			# print('-'*25)
			# print('(' + str(counterID) + ')' + 'State => ' + str(stateLabel))
			# #print('-'*25)
			# print('List of Transitions => ' + str(outputTransition))
			counterID += 1

			#Generating the state class
			globals()[stateID] = state(stateLabel, stateMarking, stateInitial, 
				output_transitions = outputTransition, input_transitions = [])
			list_of_results[3].append(globals()[stateID])

	#Updating input transitions
	for source_state in list_of_states:
		for transition_info in globals()[source_state].output_transitions:
			for target_state in list_of_states:
				if globals()[target_state].label == transition_info[0]:
					globals()[target_state].input_transitions.append(
						[globals()[source_state].label, transition_info[1]])
					break

	# print('-'*5 + 'Input Transitions' + '-'*5)
	# counterID = 0
	# for stateID in list_of_states:
	# 	print('(' + str(counterID) + ')' + str(globals()[stateID].label) + ' => ' 
	# 		+ str(globals()[stateID].input_transitions))
	# 	counterID += 1

	# print('-'*5 + 'Temporary states' + '-'*5)
	# counterClass = 0
	# for stateClass in list_of_results[3]:
	# 	print('(' + str(counterClass) + ')' + str(stateClass.label) + ' => ' + 
	# 		str(stateClass.output_transitions))
	# 	counterClass += 1
	# print('-'*30)

	#Removing states with empty input_transitions list (Accesible operation)
	#Accesible part of the automata
	print(globals()[initial_stateID].label)
	AC_states.append(globals()[initial_stateID].label)
	for transition_info in globals()[initial_stateID].output_transitions:
		if transition_info[0] not in AC_states:
			AC_states.append(transition_info[0])
			AC_Function(transition_info[0])
	# counterID = 0
	# print('-'*10 + 'Accesible part' + '-'*10)
	# for x in AC_states:
	# 	print('(' + str(counterID) + ') ' + str(x))
	# 	counterID += 1
	#Coaccesible part of the automata (not applicable)
	# for stateID in marked_states:
	# 	for transition_info in globals()[stateID].input_transitions:
	# 		if transition_info[0] not in COAC_states:
	# 			COAC_states.append(transition_info[0])
	# 			COAC_Function(transition_info[0])
	# counterID = 0
	# print('-'*10 + 'Coaccesible part' + '-'*10)
	# for x in COAC_states:
	# 	print('(' + str(counterID) + ') ' + str(x))
	# 	counterID += 1

	# Trim = intersection(AC_states, COAC_states) (not applicable)
	# counterID = 0
	# print('-'*10 + 'TRIM' + '-'*10)
	# for x in Trim:
	# 	print('(' + str(counterID) + ') ' + str(x))
	# 	counterID += 1

	for stateID in reversed(list_of_states):
		if globals()[stateID].label not in AC_states:
			stateIndex = list_of_states.index(stateID)
			del list_of_results[3][stateIndex]
			list_of_states.remove(stateID)
	list_of_results[2] = list_of_states

	counterID = 0
	print('-'*5 + 'States after AC operation' + '-'*5)
	print('-'*40)
	for x in list_of_results[3]:		
		print('(' + str(counterID) + ') ' + 'stateID = ' + str(x.label))
		print('stateMarking = ' + str(x.is_marked))
		print('stateInitial = ' + str(x.is_initial))
		print('inputTransition = ' + str(x.input_transitions))
		print('outputTransition = ' + str(x.output_transitions))
		print('-'*25)
		counterID += 1

	#Generating the event class
	counterID = 1
	listIndex = len(SA[4])
	for n in range(listIndex):
		eventID = automataID + '_E' + str(counterID)
		list_of_events.append(eventID)
		counterID += 1

	list_of_results[4] = list_of_events
	list_of_results[5] += SA[5]

	#Generating automata model
	#Labelling the automata
	automataLabel = automataID

	globals()[automataID] = automata(automataLabel, list_of_states, list_of_events, 'NaN')
	list_of_results[0] = automataID
	list_of_results[1] = globals()[automataID]

	return list_of_results
	


	



			




