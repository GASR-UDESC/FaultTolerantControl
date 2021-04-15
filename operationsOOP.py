# -*- coding: utf-8 -*-
'''
Code for Python 3
Author: Herbert Leitão
Date Version: 12/03/2021
Comments: DES operations in OOP
Comments: Updating synchronous composition operation with NF automata
Comments: Creation of the observer function
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

def unb_reach(NFA, classIndex):	# Unobservable reach
	state_info1 = NFA[3][classIndex]	#State
	chains = list()
	state1Index = None
	#flagCheck = False
	if state_info1.id not in visited_states:
		#print(state_info1.id)
		visited_states.add(state_info1.id)
		for OUTtransition_info in state_info1.output_transitions:
			if OUTtransition_info[1] in set_of_UNOBSevents: # transition_info[1] = event label
				#flagCheck = True
				# print('encontrado!')
				# print(state_info1.id)
				# print(state_info1.label)
				# print(OUTtransition_info)
				if state_info1.id not in grpStates:
					grpStates.append(state_info1.id)
					state1Index = grpStates.index(state_info1.id)
					partial_groups.append(list())
				# self-loop
				if OUTtransition_info[0] == state_info1.label:
					print('Self-loop')
					partial_groups[state1Index].append([state_info1.id])
					#chains += [state_info1.id]
				# the target state is other state
				else:				
					for state_info2 in NFA[3]:
						class2Index = NFA[3].index(state_info2)							
						if state_info2.label == OUTtransition_info[0]: # transition_info[1] = state label
							#print(state_info2.id)
							# the other state is a visited state
							if state_info2.id in visited_states:
								# the other state is either a visited and grouped state
								if state_info2.id in grpStates:
									print('Visited and grouped state')
									state2Index = grpStates.index(state_info2.id)									
									for groups in partial_groups[state2Index]:
										partial_groups[state1Index].append([state_info1.id] + groups)										
								# the other state is a visited state but does not belong to a group
								else:
									print('Visited and not grouped state')
									partial_groups[state1Index].append([state_info1.id, state_info2.id])
									grpStates.append(state_info2.id)
									partial_groups.append(list())
							# the other state is not a visited state	
							else:
								print('Not visited state')
								chains = unb_reach(NFA, class2Index)
								# print(chains)
								# print(state1Index)
								if not chains:
									partial_groups[state1Index].append([state_info1.id, state_info2.id])
									grpStates.append(state_info2.id)
									partial_groups.append(list())
								else:
									for x in chains:										
										partial_groups[state1Index].append([state_info1.id] + x)
							break
	if state1Index != None:
		chains = partial_groups[state1Index]

	return chains

def observer(automataID, NFA):
	global visited_states, grpStates, partial_groups, set_of_UNOBSevents
	set_of_UNOBSevents = set()
	list_of_results = [automataID,'NaN',[],[],[],[]]	#[automataID, automata class, [states ID], ...
												# ...[classes of states], [events ID], [classes of events]
	list_of_states = []
	list_of_events = []
	# # Checking output transitions
	# for x in NFA[3]:
	# 	print('STATE')
	# 	for y in x.output_transitions:
	# 		print(y)
	# Creating a set of unobservable events
	for event_info in NFA[5]:
		if not event_info.is_observable:
			set_of_UNOBSevents.add(event_info.label)
		else:
			list_of_events.append(NFA[4][NFA[5].index(event_info)])
			list_of_results[5].append(event_info)
	#print(set_of_UNOBSevents)	
	visited_states = set()	# Set of visited states
	grpStates = list()		# List of states belonging to groupings
							# grpStates = [stateID, ...]
	partial_groups = list()	# List composed by partial groups of states

	# joining states - Step 1 (Unobservable Events)
	for classIndex in range(len(NFA[3])):
		unb_reach(NFA, classIndex)
	# print('-'*25)
	print('Grouped States')
	print(grpStates)	
	# print('-'*25)
	# print('partial_groups')
	# print(partial_groups)

	# Checking output transitions
	print('-'*25)
	for x in grpStates:
		stateIndex = NFA[2].index(x)
		print('')
		print('-'*25)
		print('STATE ' + str(x))
		print(NFA[3][stateIndex].label)
		print('Input Transitions')
		for y in NFA[3][stateIndex].input_transitions:
			print(y)
			print('-'*25)
		print('Output Transitions')
		for y in NFA[3][stateIndex].output_transitions:
			print(y)
			print('-'*25)

	step1Groups = list()
	for groups in partial_groups:
		for group in groups:
			step1Groups.append(group)

	# Converting step1Groups IDs in labels
	step1Labels = list()
	for group in step1Groups:
		step1Labels.append([])
		for stateID in group:
			for x in NFA[3]:
				if x.id == stateID:
					step1Labels[-1].append(x.label)

	print('')
	print('Step 1 - Groups')
	for x in step1Groups:
		print(x)
	print('')	
	print('Step 1 - Labels')
	for x in step1Labels:
		print(x)
	print('')
	
	flagContinue = True
	newGroups = list()

	while (flagContinue):		
		# Joining states - Step 2		
		step2Groups = list()
		set_of_events = set()
		list_of_states = list()
		tempInfo = list()
		print('')
		print('-'*25)
		print('###### NEW LOOP ######')
		print('List of Transitions')
		print('')
		newGroups += step1Groups

		print('')
		print('-'*25)
		print('New Group')
		print('')
		for x in newGroups:
			print(x)

		counter = 1
		for group in step1Groups:
			list_of_transitions = list()
			#itemZero = True				
			newTransitions = list()
			# Generating a list of transitions in order to evaluate new states for grouping
			for stateID in group:
				stateIndex = NFA[2].index(stateID)
				for transition_info in NFA[3][stateIndex].output_transitions:
					if transition_info[1] not in set_of_UNOBSevents:
						list_of_transitions.append(transition_info)
			# print('AQUI!!!')
			# print(list_of_transitions)
			print('')
			print('List of Transitions in Group ' + str(counter))
			counter += 1
			#print(counter)		
			for x in list_of_transitions:
				print(x)
			print('')
			for x in list_of_transitions:
				flagBreak = False
				for y in newTransitions:
					if x[1] == y[1]:
						if x[0] not in y[0]: 
							y[0].append(x[0])
						flagBreak = True
						break						
				if not flagBreak:
					newTransitions.append([[x[0]],x[1]])
			tempInfo.append(newTransitions)
		print('-'*25)
		print('')
		print('Step 2 - Groups')
		counter = 1
		for x in tempInfo:
			print('Group ' + str(counter))
			counter += 1
			for y in x:
				print(y)
		# Organizing and prospecting possible groups in tempInfo
		print('')
		print('-'*25)
		for x in tempInfo:
			for y in x:
				if len(y[0]) > 1:
					#print(y[0])
					print('OK')
					list_of_IDs = list()
					for item in range(len(y[0])):
						for state_info1 in NFA[3]:
							if state_info1.label == y[0][item]:
								list_of_IDs.append(state_info1.id)
								break
					#print(list_of_IDs)
					if list_of_IDs not in newGroups and list_of_IDs not in step2Groups:
						step2Groups.append(list_of_IDs)
		print('Step 2 Final Groups')
		for x in step2Groups:
			print(x)
		if step2Groups:
			step1Groups = step2Groups			
		else:
			step1Groups = list()			
			flagContinue = False

	for groups in newGroups:
		for stateID in groups:
			if stateID not in grpStates:
				grpStates.append(stateID)


	print('###### Partial Groups ######')
	for x in partial_groups:
		print(x)
	
	# mainGroups = list()
	# # Separating the main chains
	# for x1 in partial_groups:	# a list of lists of grouped states
	# 	for y1 in x1:			# a list of grouped states
	# 		flagBreak = False
	# 		for x2 in partial_groups:
	# 			if x1 == x2:
	# 				#break
	# 				continue
	# 			for y2 in x2:
	# 				if y1 in y2:
	# 					flagBreak = True
	# 					break
	# 			if flagBreak:
	# 				break
	# 		if flagBreak:
	# 			continue
	# 		mainGroups.append(y1)
	# print('-'*25)
	# print('Main Groups')
	# print(mainGroups)

	mainGroups = list()
	checkedStates = set()
	# Listing the groups	
	for y1 in newGroups:			
		if len(y1) == 1: # This is the case when a state has self-loop by unobservable event
			mainGroups.append(y1)
		else:
			state1Index = NFA[2].index(y1[0])
			#print(state1Index)
			if NFA[3][state1Index].is_initial:	# In this case the group is a state
				mainGroups.append(y1)			# in the observer
			else:
				for transition_info in NFA[3][state1Index].input_transitions:
					if transition_info[1] not in set_of_UNOBSevents: 	# In this case the group is a state
						mainGroups.append(y1)							# in the observer
						break				
			if y1[-1] not in checkedStates:			# This test is important because the last state in a 
				print(y1[-1])						# group can have a input transition by observable event
				checkedStates.add(y1[-1])			# and, at the same time, this state can be grouped
				state2Index = NFA[2].index(y1[-1])
				print(state2Index)
				for transition_info in NFA[3][state2Index].input_transitions:
					if transition_info[1] not in set_of_UNOBSevents:
						print(NFA[3][state2Index].label)
						print(transition_info)
						mainGroups.append([y1[-1]])
						break
	print('-'*25)
	print('Main Groups')
	for x in mainGroups:
		print(x)
	
	# Generating an empty list for including the IDs of the new states
	# and [stateID, state reference] for updating the new states later
	mainGroupsIDs = [[],[]]
	for x in range(len(mainGroups)):
		mainGroupsIDs[0].append(None)
		mainGroupsIDs[1].append([])
	print(mainGroupsIDs)
	
	#######################################
	# Generating a list of grouped labels for optimizing the process to generate the observer
	label_grpStates = list()
	label_mainGroups = list()
	grpReference = list()		# List of references State => Groups
	for x in range(len(grpStates)):
		label_grpStates.append([])
		grpReference.append([])
	for state_info1 in NFA[3]:
		if state_info1.id in grpStates:
			listIndex = grpStates.index(state_info1.id)
			label_grpStates[listIndex] += state_info1.label
	print('-'*25)
	print('Grouped Labels')
	print(label_grpStates)
	
	counterList = 0
	for sublist in mainGroups:
		label_mainGroups.append([])
		for stateID in sublist:
			listIndex = grpStates.index(stateID)
			label_mainGroups[-1] += label_grpStates[listIndex]
			grpReference[listIndex].append(counterList)
		counterList += 1
	print('-'*25)
	print('Label of the Grouped States')
	for x in label_mainGroups:
		print(x)
	print('-'*25)
	print('References of the States in Grouped States')
	print(grpReference)
	#######################################
	#######################################
	
	#######################################
	# Generating Observer Automata	
	flagFaultLabel = False	# Test to evaluate the fault diagnosability
	set_badStates = set()	# Information to support safe controllability test
	counterID = 0
	counterS = 0	
	newStatesEval = set() 	# intermediary states in grouped states that needs to be evaluated after
							# for including transitions in the new state
	for state_info1 in NFA[3]:
		# Not grouped states
		if state_info1.id not in grpStates:
			counterS += 1
			print('State ' + str(counterS) + ' => ' + str(state_info1.label))
			# New ID
			state_info1.id = automataID + '_S' + str(counterID)
			list_of_states.append(state_info1.id)
			# This attribute doesn't exist in the observer
			state_info1.is_marked = None
			# Evaluating the fault diagnosability
			if state_info1.label[1] == 'Y' or state_info1.label[1] == 'F':
				flagFaultLabel = True
			# Registering bad states
			if state_info1.label[2] == 'B':
				set_badStates.add(state_info1.id)
			######################################
			# Updating input transitions
			newTransitions = list()
			for transition_info in reversed(state_info1.input_transitions):
				# Option 1 => the source state belongs to grouped states
				if transition_info[0] in label_grpStates:
					stateIndex = label_grpStates.index(transition_info[0])					
					for ref in grpReference[stateIndex]:
						newTransition = [label_mainGroups[ref], transition_info[1]]
						if newTransition not in newTransitions:
							newTransitions.append(newTransition)
					state_info1.input_transitions.remove(transition_info)
				# Option 2 => the source state doesn't belong to grouped states
				# Nothing to do!

			#Updating input transitions list
			state_info1.input_transitions += newTransitions
			######################################

			######################################
			# Updating output transitions
			newTransitions = list()
			for transition_info in reversed(state_info1.output_transitions):
				# Option 1 => the source state belongs to grouped states
				if transition_info[0] in label_grpStates:
					stateIndex = label_grpStates.index(transition_info[0])					
					for ref in grpReference[stateIndex]:
						newTransition = [label_mainGroups[ref], transition_info[1]]
						if newTransition not in newTransitions:
							newTransitions.append(newTransition)						
					state_info1.output_transitions.remove(transition_info)
				# Option 2 => the source state doesn't belong to grouped states
				# Nothing to do!

			#Updating output transitions list
			state_info1.output_transitions += newTransitions
			######################################
			# print('-'*25)
			# print('Check New Single State')
			# print(state_info1.id)
			# print(state_info1.label)
			# print(state_info1.is_initial)
			# print('Input Transitions')
			# for x in state_info1.input_transitions:
			# 	print(x)
			# print('Output Transitions')
			# for x in state_info1.output_transitions:
			# 	print(x)
			globals()[state_info1.id] = state_info1		
			list_of_results[3].append(globals()[state_info1.id])
			# print('###### LABEL CHECK ######')
			# print(list_of_results[3][-1].label)
			counterID += 1
		
		# Grouped states
		else:
			for grp in mainGroups:
				grpIndex = mainGroups.index(grp)			
				if state_info1.id == grp[0]:					
					# New ID
					stateID = automataID + '_S' + str(counterID)
					list_of_states.append(stateID)
					mainGroupsIDs[0][grpIndex] = stateID
					# New label
					stateLabel = label_mainGroups[grpIndex]
					# Verifying if it is an initial state
					stateInitial = state_info1.is_initial
					# This attribute doesn't exist in the observer
					stateMarking = None			
					# Evaluating the fault diagnosability
					set_of_labels = set()
					for x in range(1,len(stateLabel),3):
						set_of_labels.add(x)
					if 'N' not in set_of_labels:
						flagFaultLabel = True
					# Registering bad states
					for x in range(2,len(stateLabel),3):
						if x == 'B':
							set_badStates.add(stateID)
							break
					######################################
					# Updating input transitions
					newInputTransitions = list()
					for transition_info in reversed(state_info1.input_transitions):
						# Option 1 => the source state belongs to grouped states
						if transition_info[0] in label_grpStates:
							stateIndex = label_grpStates.index(transition_info[0])					
							for ref in grpReference[stateIndex]:
								newTransition = [label_mainGroups[ref], transition_info[1]]
								if newTransition not in newInputTransitions:
									newInputTransitions.append(newTransition)							
						# Option 2 => the source state doesn't belong to grouped states
						else:
							newInputTransitions.append(transition_info)
					######################################
					######################################
					# Updating output transitions
					newOutputTransitions = list()
					for transition_info in reversed(state_info1.output_transitions):
						# Option 1 => the source state belongs to grouped states
						if transition_info[0] in label_grpStates:
							stateIndex = label_grpStates.index(transition_info[0])					
							for ref in grpReference[stateIndex]:
								newTransition = [label_mainGroups[ref], transition_info[1]]
								if newTransition not in newOutputTransitions:
									newOutputTransitions.append(newTransition)							
						# Option 2 => the source state doesn't belong to grouped states
						else:
							newOutputTransitions.append(transition_info)
					######################################
					#Generating the new state class
					globals()[stateID] = state(stateLabel, stateMarking, stateInitial, 
						input_transitions = newInputTransitions, output_transitions = newOutputTransitions)
					list_of_results[3].append(globals()[stateID])
					counterID += 1
					######################################
					# print('-'*25)
					# print('Check New Grouped State')
					# print(state_info1.id)
					# print(state_info1.label)
					# print(state_info1.is_initial)
					# print('Input Transitions')
					# for x in state_info1.input_transitions:
					# 	print(x)
					# print('Output Transitions')
					# for x in state_info1.output_transitions:
					# 	print(x)
				#
				elif state_info1.id in grp:
					mainGroupsIDs[1][grpIndex].append([state_info1.id, NFA[3].index(state_info1)])
	# Updating the new states
	for x in range(len(mainGroupsIDs[0])):
		updState = globals()[mainGroupsIDs[0][x]]
		for reference in mainGroupsIDs[1][x]:
			state_info1 = NFA[3][reference[1]]
			#print(reference)
			######################################
			# Updating input transitions			
			for transition_info in reversed(state_info1.input_transitions):
				# Option 1 => the source state belongs to grouped states
				if transition_info[0] in label_grpStates:
					stateIndex = label_grpStates.index(transition_info[0])					
					for ref in grpReference[stateIndex]:
						newTransition = [label_mainGroups[ref], transition_info[1]]	
						if newTransition not in updState.input_transitions:
							updState.input_transitions.append(newTransition)
							print(newTransition)						
				# Option 2 => the source state doesn't belong to grouped states
				else:
					if transition_info not in updState.input_transitions:
						updState.input_transitions.append(transition_info)
						print(transition_info)
			######################################
			######################################
			# Updating output transitions			
			for transition_info in reversed(state_info1.output_transitions):
				# Option 1 => the source state belongs to grouped states
				if transition_info[0] in label_grpStates:
					stateIndex = label_grpStates.index(transition_info[0])					
					for ref in grpReference[stateIndex]:
						newTransition = [label_mainGroups[ref], transition_info[1]]
						if newTransition not in updState.output_transitions:
							updState.output_transitions.append(newTransition)
							print(newTransition)							
				# Option 2 => the source state doesn't belong to grouped states
				else:
					if transition_info not in updState.output_transitions:
						updState.output_transitions.append(transition_info)
						print(transition_info)
			######################################
		

	#print(mainGroupsIDs)
	#Generating automata model
	#Labelling the automata
	automataLabel = automataID

	globals()[automataID] = automata(automataLabel, list_of_states, list_of_events, 'NaN')
	list_of_results[0] = automataID
	list_of_results[1] = globals()[automataID]
	list_of_results[2] = list_of_states
	list_of_results[4] = list_of_events

	print('')
	print('-'*25)
	print('SUMMARY REPORT')
	counterStates = 0
	counterTransitions = 0
	print('')
	print('States')
	for x in list_of_results[3]:
		counterStates+=1
		print(x.label)
		for y in x.output_transitions:
			counterTransitions+=1
	print('Number of States = ' + str(counterStates))
	print('Number of Transitions = ' + str(counterTransitions))
	
	return list_of_results
	# #######################################
	# ####################################

def syncLAB(automataID,FSA,NFA): 	# FSA = Automata (Fault + Supervisor)
									# NFA = Automata (BNB-NF Labeller)
	list_of_results = [automataID,'NaN',[],[],[],[]]	#[automataID, automata class, [states ID], ...
												# ...[classes of states], [events ID], [classes of events]
	# # str2list FSA label	
	# for state_info1 in NFA[3]:
	# 	newLabel = list()
	# 	#string1 = state_info1.label[0]
	# 	string = ''
	# 	print(state_info1.label)
	# 	for c in state_info1.label[0]:			
	# 		if c == ' ':
	# 			continue
	# 		elif c == ',':
	# 			newLabel.append(string)
	# 			string = ''				
	# 		else:
	# 			string += c
	# 	newLabel.append(string)
	# 	state_info1.label = newLabel
	# 	print(newLabel)

	##Reading Test
	##########################################################
	'''
	print('-'*25)
	print('##### Supervisor with fault information #####')
	print('-'*25)
	print(FSA[1].label)
	print('-'*25)
	print('Output Transitions')
	for x in FSA[3]:
		for y in x.output_transitions:
			print(str(x.label) + '=>' + str(y))
			#print(str(x.label) + '=>' + str(x.output_transitions))
	print('-'*25)
	print('Events')
	for x in FSA[5]:
		print(x.label)
	print('-'*25)

	print('-'*25)
	print('##### BNB-NY labeller #####')
	# print('-'*25)
	# print(NFA[1].label)
	print('-'*25)
	print('Output Transitions')
	for x in NFA[3]:
		for y in x.output_transitions:
			print(str(x.label) + '=>' + str(y))
			#print(str(x.label) + '=>' + str(x.output_transitions))
	print('-'*25)
	print('Events')
	for x in NFA[5]:
		print(x.label)
	print('-'*25)
	print("DONE READING TEST==============================")
	'''
	##########################################################
	##########################################################

	# Comment: It is not necessary to find the intersection set of events 
	# because set of events NF is contained within set of events SU

	# Intersection of events between SA and FA
	# Comment: The set of events NF is contained within the set of events SU
	intersectionSet = [] # eventos de falha e idle
	for eventNFA in NFA[5]:
		intersectionSet.append(eventNFA.label)
	# print('-'*25)
	# print('Intersection Set => ' + str(intersectionSet))
	# pegando as falhas que fazem o NY progredir

	#Declaring supporting variables
	global list_of_states
	global AC_states
	list_of_states = []
	list_of_events = []
	AC_states = []

	# nf_initial=None
	# for check_initial in NF[3]:
	# 	if check_initial.is_initial == True:
	# 		nf_initial=check_initial
	# 		break

	#Syncronizing states	
	counterID = 0
	for stateNFA in NFA[3]:
		for stateFSA in FSA[3]:
			stateID = automataID + '_S' + str(counterID)
			list_of_states.append(stateID)
			# print('########TEST#######')
			# print(stateNFA.label)
			stateLabel = stateFSA.label + stateNFA.label
			stateMarking = bool(stateFSA.is_marked * stateNFA.is_marked)
			stateInitial = bool(stateFSA.is_initial * stateNFA.is_initial)
			if stateInitial:
				initial_stateID = stateID 

			outputTransition = []
			for transition_infoFSA in stateFSA.output_transitions:
				if transition_infoFSA[1] not in intersectionSet:
					outputTransition.append([transition_infoFSA[0] + stateNFA.label, transition_infoFSA[1]])
				else:
					for transition_infoNFA in stateNFA.output_transitions:
						if transition_infoFSA[1] == transition_infoNFA[1]:
							outputTransition.append([transition_infoFSA[0] + transition_infoNFA[0], transition_infoFSA[1]])
							break			
			counterID += 1

			#Generating the state class
			globals()[stateID] = state(stateLabel, stateMarking, stateInitial, stateID = stateID,
				output_transitions = outputTransition, input_transitions = [])
			list_of_results[3].append(globals()[stateID])

	# #Updating input transitions
	# for source_state in list_of_states:
	# 	for transition_info in globals()[source_state].output_transitions:
	# 		for target_state in list_of_states:
	# 			if globals()[target_state].label == transition_info[0]:
	# 				globals()[target_state].input_transitions.append(
	# 					[globals()[source_state].label, transition_info[1]])
	# 				break

	#Removing states with empty input_transitions list (Accessible operation)
	#Accesible part of the automata
	#print(globals()[initial_stateID].label)
	AC_states.append(globals()[initial_stateID].label)
	for transition_info in globals()[initial_stateID].output_transitions:
		if transition_info[0] not in AC_states:
			AC_states.append(transition_info[0])
			AC_Function(transition_info[0])

	for stateID in reversed(list_of_states):
		stateIndex = list_of_states.index(stateID)
		if globals()[stateID].label not in AC_states:			
			del list_of_results[3][stateIndex]
			list_of_states.remove(stateID)
		else:
			# Updating attributes related to NY and BNB labels
			list_of_results[3][stateIndex].label_eval()
	list_of_results[2] = list_of_states

	#Updating input transitions
	for source_state in list_of_states:
		for transition_info in globals()[source_state].output_transitions:
			for target_state in list_of_states:
				if globals()[target_state].label == transition_info[0]:
					globals()[target_state].input_transitions.append(
						[globals()[source_state].label, transition_info[1]])
					break

	# counterID = 0
	# print('-'*5 + 'States after AC operation' + '-'*5)
	# print('-'*40)
	# for x in list_of_results[3]:		
	# 	print('(' + str(counterID) + ') ' + 'stateID = ' + str(x.label))
	# 	print('stateMarking = ' + str(x.is_marked))
	# 	print('stateInitial = ' + str(x.is_initial))
	# 	print('inputTransition = ' + str(x.input_transitions))
	# 	print('outputTransition = ' + str(x.output_transitions))
	# 	print('-'*25)
	# 	counterID += 1

	#Generating the event class
	counterID = 1
	listIndex = len(FSA[4])
	for n in range(listIndex):
		eventID = automataID + '_E' + str(counterID)
		list_of_events.append(eventID)
		counterID += 1

	list_of_results[4] = list_of_events
	list_of_results[5] += FSA[5]

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
	'''
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
	'''
	##########################################################
	##########################################################

	#Intersection of events between SA and FA
	intersectionSet = []
	for eventFA in FA[5]:
		for eventSA in SA[5]:	
			if eventFA.label == eventSA.label:
				intersectionSet.append(eventFA.label)
	# print('-'*25)
	# print('Intersection Set => ' + str(intersectionSet))

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
			# print('-'*25)
			# print('Fault Event => ' + str(faultEventLabel))
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
	#print(globals()[initial_stateID].label)
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

	# counterID = 0
	# print('-'*5 + 'States after AC operation' + '-'*5)
	# print('-'*40)
	# for x in list_of_results[3]:		
	# 	print('(' + str(counterID) + ') ' + 'stateID = ' + str(x.label))
	# 	print('stateMarking = ' + str(x.is_marked))
	# 	print('stateInitial = ' + str(x.is_initial))
	# 	print('inputTransition = ' + str(x.input_transitions))
	# 	print('outputTransition = ' + str(x.output_transitions))
	# 	print('-'*25)
	# 	counterID += 1

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
	


	



			



