# -*- coding: utf-8 -*-
'''
Code for Python 3
Author: Herbert Leitão
Date Version: 15/04/2021
Comments: Creating a new observer function
'''

from elementClasses import automata, state, event
import collections

def unb_reach(NFA, classIndex):	# Unobservable reach
	global initState_index
	state_info1 = NFA[3][classIndex]	#State
	if state_info1.is_initial:
		initState_index = classIndex
		print(initState_index)
		print('ENCONTRADO!')
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
								#print('Not visited state')
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
	# list_of_events = []
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
			list_of_results[4].append(NFA[4][NFA[5].index(event_info)])
			list_of_results[5].append(event_info)
	#print(set_of_UNOBSevents)	
	visited_states = set()	# Set of visited states
	grpStates = list()		# List of states belonging to groupings
							# grpStates = [stateID, ...]
	partial_groups = list()	# List composed by partial groups of states
	#initState_index = None

	# joining states - Step 1 (Unobservable Events)
	for classIndex in range(len(NFA[3])):
		unb_reach(NFA, classIndex)
	# print('-'*25)
	print('Grouped States')
	print(grpStates)
	print('-'*25)
	print('partial_groups')
	print(partial_groups)
	print('')
	print('Initial State = ' + str(initState_index))
	
	# # Checking output transitions
	# print('-'*25)
	# for x in grpStates:
	# 	stateIndex = NFA[2].index(x)
	# 	print('')
	# 	print('#'*25)
	# 	print('')
	# 	print('STATE ' + str(x) + ' => ' + str(NFA[3][stateIndex].label))
	# 	print('-'*25)
	# 	#print(NFA[3][stateIndex].label)
	# 	print('Input Transitions')
	# 	for y in NFA[3][stateIndex].input_transitions:
	# 		print(y)
	# 		print('-'*25)
	# 	print('Output Transitions')
	# 	for y in NFA[3][stateIndex].output_transitions:
	# 		print(y)
	# 	#print('-'*25)

	step1Groups = list()
	for groups in partial_groups:
		for group in groups:
			step1Groups.append(group)

	# Repositioning groups in the list by length
	flagPosition = True
	while (flagPosition):
		flagPosition = False
		for x in range(len(step1Groups)-1):
			if len(step1Groups[x]) < len(step1Groups[x+1]):
				tempGroup = list()
				tempGroup += step1Groups[x]
				step1Groups[x].clear()
				step1Groups += step1Groups[x+1]
				step1Groups[x+1].clear()
				step1Groups[x+1] += tempGroup
				flagPosition = True
	
	# Converting step1Groups IDs in labels
	step1Labels = list()
	step1LabelsInfo = list()
	for group in step1Groups:
		step1LabelsInfo.append([])
		for stateID in group:
			for x in NFA[3]:
				if x.id == stateID:
					step1LabelsInfo[-1].append(x.label)
					step1Labels.append(x.label)
					break

	print('')
	print('Step 1 - Groups')
	for x in step1Groups:
		print(x)
	print('')	
	print('Step 1 - Labels')
	for x in step1LabelsInfo:
		print(x)
	print(step1Labels)
	print('')
	
	#######################################
	# Generating Observer Automata	
	flagFaultLabel = False	# Test to evaluate the fault diagnosability
	set_badStates = set()	# Information to support safe controllability test
	obsStates = list()
	obsLabelStates = list()
	
	counterID = 0
	counterS = 0

	# Observer's Initial State
	evalState = NFA[3][initState_index] # Evaluated state in labelled automata
	counterS += 1
	outTransitions = list()
	new_outTransitions = list()
	print('State ' + str(counterS) + ' => ' + str(evalState.label))
	# New ID
	stateID = automataID + '_S' + str(counterID)
	list_of_results[2].append(stateID)
	stateLabel = None
	Option = None

	###################################################################################
	# Option 1 => The state does not belong a grouped state
	# Option 2 => The state either belongs and starts a grouped state
	# Option 3 => The state belongs a grouped state but it does not start the group
	if evalState.id not in grpStates:
		Option = 1
	else:
		flagCheck = False
		for group in step1Groups:
			firstState = group[0]
			if evalState.id == firstState:
				flagCheck = True
				Option = 2
				grpIndex = step1Groups.index(group)
				break
		if not flagCheck:
			Option = 3
	###################################################################################
	
	# New Label
	if Option == 1 or Option == 3:
		obsStates.append([evalState.id])		
		stateLabel = evalState.label
	elif Option == 2:
		obsStates.append(step1Groups[grpIndex])		
		# New Label
		for label in step1LabelsInfo[grpIndex]:
			stateLabel += label

	# Information about output transitions
	if Option == 1 or Option == 3:
		outTransitions = evalState.output_transitions
	elif Option == 2:
		for grpID in step1Groups[grpIndex]:
			for stateClass in NFA[3]:
				if stateClass.id == grpID:
					outTransitions += stateClass.output_transitions
					break
	print('')
	print('Output Transitions - BEFORE')
	for x in outTransitions:
		print(x)	

	# STEP 1 - EVALUATING OUTPUT TRANSITIONS (UNOBS EVENTS)		
	for transition_info in reversed(outTransitions):
		# Discarding the transition when it has an unobservable event
		if transition_info[1] in set_of_UNOBSevents:
			outTransitions.remove(transition_info)

	# STEP 2 - JOINING TRANSITIONS
	step2_outTransitions = list()
	outEvents = set()
	for transition_info1 in outTransitions:		
		event = transition_info1[1]		
		if event not in outEvents:
			newLabel = [transition_info1[0]]
			outEvents.add(event)
			for transition_info2 in outTransitions:
				if transition_info2[1] == event and transition_info2 != transition_info1:
					newLabel.append(transition_info2[0])
			step2_outTransitions.append([newLabel, event])

	print('')
	print('Output Transitions - AFTER')
	for x in step2_outTransitions:
		print(x)
	
	# STEP 3 - ADDING GROUPED STATES
	for group in step1LabelsInfo:
		startLabel = group[0]		
		for transition_info in step2_outTransitions:
			if startLabel in transition_info[0]:
				for label in group:
					if label not in transition_info[0]:
						transition_info[0].append(label)
	print('')
	print('Output Transitions - AFTER ADDING GROUPED STATES')
	for x in step2_outTransitions:
		print(x)

	if Option == 1 or Option == 3:
		obsLabelStates.append([stateLabel])
	else:
		obsLabelStates.append(stateLabel)
	
	# Generating the initial state in the observer automata
	globals()[stateID] = state(obsLabelStates[-1], False, True, stateID = stateID,
		output_transitions = step2_outTransitions, input_transitions = [])
	list_of_results[3].append(globals()[stateID])	

	print('-'*25)
	print('Initial State in the Observer')
	print(str(globals()[stateID].id) + ' => ' + str(globals()[stateID].label))
	print('Initial State = ' + str(globals()[stateID].is_initial))
	print('Output Transitions:')
	for x in globals()[stateID].output_transitions:
		print(x)

	evalList = list()
	for transition_info in step2_outTransitions:
		targetState = transition_info[0]
		if targetState not in obsLabelStates:
			evalList.append(targetState)

	print('List of Evaluation')
	print(evalList)

	while (evalList):
		# Separating labels in the first item of the evalList		
		evalState = evalList[0]
		evalID = list()
		for item in evalState:
			for stateClass in NFA[3]:
				if stateClass.label == item:
					evalID.append(stateClass.id)
					break
		
		flagEval = True
		for x in obsStates:
			if evalID in x:
				if len(evalID) == len(obsStates):
					flagEval = False
					break
		if flagEval:
			obsStates.append(evalID)
			del evalList[0]

			for x in obsStates:
				print(x)
			
			#######################################
			# Generating Observer Automata			
			counterID += 1
			counterS += 1
			outTransitions = list()
			#new_outTransitions = list()
			stateLabel = evalState
			print('')
			print('State ' + str(counterS) + ' => ' + str(evalState))
			# New ID
			stateID = automataID + '_S' + str(counterID)
			list_of_results[2].append(stateID)
			Option = None

			# Information about output transitions
			for item in obsStates[-1]:
				for stateClass in NFA[3]:
					if stateClass.id == item:
						outTransitions += stateClass.output_transitions
						break

			print('')
			print('Output Transitions - BEFORE')
			for x in outTransitions:
				print(x)	

			# STEP 1 - EVALUATING OUTPUT TRANSITIONS (UNOBS EVENTS)		
			for transition_info in reversed(outTransitions):
				# Discarding the transition when it has an unobservable event
				if transition_info[1] in set_of_UNOBSevents:
					outTransitions.remove(transition_info)

			# STEP 2 - JOINING TRANSITIONS
			step2_outTransitions = list()
			outEvents = set()
			for transition_info1 in outTransitions:		
				event = transition_info1[1]		
				if event not in outEvents:
					newLabel = [transition_info1[0]]
					outEvents.add(event)
					for transition_info2 in outTransitions:
						if transition_info2[1] == event and transition_info2 != transition_info1:
							newLabel.append(transition_info2[0])
					step2_outTransitions.append([newLabel, event])

			print('')
			print('Output Transitions - AFTER')
			for x in step2_outTransitions:
				print(x)

			# STEP 3 - ADDING GROUPED STATES
			for group in step1LabelsInfo:
				startLabel = group[0]		
				for transition_info in step2_outTransitions:
					if startLabel in transition_info[0]:
						for label in group:
							if label not in transition_info[0]:
								transition_info[0].append(label)
			print('')
			print('Output Transitions - AFTER ADDING GROUPED STATES')
			for x in step2_outTransitions:
				print(x)

			# Generating the state in the observer automata
			globals()[stateID] = state(stateLabel, False, False, stateID = stateID,
				output_transitions = step2_outTransitions, input_transitions = [])
			list_of_results[3].append(globals()[stateID])

			obsLabelStates.append(stateLabel)

			print('-'*25)
			print('Observer Label States')
			for x in obsLabelStates:
				print(x)

			print('-'*25)
			print('New state in the observer')
			print(str(globals()[stateID].id) + ' => ' + str(globals()[stateID].label))
			print('State = ' + str(globals()[stateID].is_initial))
			print('Output Transitions:')
			for x in globals()[stateID].output_transitions:
				print(x)
			
			for transition_info in step2_outTransitions:
				targetState = transition_info[0]
				if targetState not in obsLabelStates:
					evalList.append(targetState)

			print('List of Evaluation')
			print(evalList)
			
		#evalList.clear()


	# print('')
	# print('Evaluated State in the Observer')
	# print(evalStateList)

	#Updating input transitions
	print('Updating input transitions')
	
	for source_state in list_of_results[3]:
		# print(source_state.label)
		for transition_info in source_state.output_transitions:
			target_state = transition_info[0]
			# print(len(target_state))
			# break	
			for check_state in list_of_results[3]:
				# print(check_state.label)
				# break				
				if len(target_state) == len(check_state.label):					
					similarityCheck = 0
					for item in target_state:
						if item in check_state.label:
							similarityCheck += 1
					if len(target_state) == similarityCheck:						
						check_state.input_transitions.append([source_state.label, transition_info[1]])
						break

	# test = list_of_results[3][1] #State Class
	# print(test.label)
	# for transition_info1 in test.output_transitions:
	# 	target_state = transition_info1[0]			
	# 	print(transition_info1)
	# 	for checkState in list_of_results[3]:
	# 		if len(target_state) == len(checkState.label):
	# 			similarityCheck = 0
	# 			for item in target_state:
	# 				if item in checkState.label:
	# 					similarityCheck += 1
	# 			if len(target_state) == similarityCheck:
	# 				print(checkState.label)
	# 				checkState.input_transitions.append([test.label, transition_info1[1]])
	# 				print(checkState.input_transitions)

	# print('CHECKING INFORMATION')
	# for x in list_of_results[3]:
	# 	print(x.label)


	numStates = 0
	numTrans = 0
	for x in list_of_results[3]:
		numStates += 1
		for y in x.output_transitions:
			numTrans += 1

	print('')
	print('SUMMARY')
	print('Number of States = ' + str(numStates))
	print('Number of Transistions = ' + str(numTrans))

	# print('')
	# for stateClass in list_of_results[3]:
	# 	print(stateClass.label)
	# 	for x in stateClass.input_transitions:
	# 		print(x)

	return list_of_results
	# #######################################
	# ####################################
	