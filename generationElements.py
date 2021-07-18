'''
Code for Python 3
Author: Herbert Leitão
Date Version: 17/02/2021
Comments: Generation of elements for supporting operations in automatas
'''

import copy
from xmlImportOOP import xmlAutomataImport
from elementClasses import automata, state, event

#automata_information = xmlAutomataImport('supervisor.xmd')

#Generating automata elements
def genElements(automataID, xmdFile, **kwargs):
	label = kwargs.get('label')

	list_of_results = ['NaN','NaN',[],[],[],[]]	#[automataID, automata class, [states ID], ...
												# ...[classes of states], [events ID], [classes of events]]

	#Reading xmd file
	automata_information = xmlAutomataImport(xmdFile, label = label)

	# print('=======Transicoes')
	# for x in automata_information[3]:
	# 	print(x)

	###############################################
	#Distributing automata information in classes

	#Declaring supporting variables
	list_of_states = []
	list_of_events = []
	#stateID_model = 'A1_S'	#class ID representation A1S0 (Automata 1 State 0)...
	#eventID_model = 'A1_E'	#class ID representation A1S0 (Automata 1 State 0)...

	#Extracting information of the states [[LABEL], MARKING, INITIAL]] and output transitions
	counterID = 0
	for state_info in automata_information[1]:
		stateID = automataID + '_S' + str(counterID)	 
		list_of_states.append(stateID)				
		stateLabel = state_info[0]
		stateMarking = state_info[1]
		stateInitial = state_info[2]
		outputTransition = []
		for transition_info in automata_information[3][counterID]:
			outputTransition.append([transition_info[2], transition_info[1]])
			#print('Update => ' + str(transition_info[2]) + str(transition_info[1]))
		counterID += 1

		# print('stateID = ' + str(stateID))
		# print('stateMarking = ' + str(stateMarking))
		# print('stateInitial = ' + str(stateInitial))
		# print('outputTransition = ' + str(outputTransition))

		#Generating the state class
		globals()[stateID] = state(stateLabel, stateMarking, stateInitial, 
			output_transitions = outputTransition, input_transitions = [])
		list_of_results[3].append(globals()[stateID])

	list_of_results[2] = list_of_states

	#Finding transition functions and filling input_transitions lists in states
	for sublist in automata_information[3]:
		for transition_info in sublist:
			targetState = transition_info[2]
			for stateID in list_of_states:
				if targetState == globals()[stateID].label:
					globals()[stateID].input_transitions.append([transition_info[0], transition_info[1]])
					break

	# print('-'*25)
	# print('A1_S0 = ' + str(A1_S0.label))
	# print('stateMarking = ' + str(A1_S0.is_marked))
	# print('stateInitial = ' + str(A1_S0.is_initial))
	# print('inputTransition = ' + str(A1_S0.input_transitions))
	# print('outputTransition = ' + str(A1_S0.output_transitions))
	# print('-'*25)

	#Extracting information of the events [LABEL, CONTROLLABLE, OBSERVABLE]
	counterID = 0
	for event_info in automata_information[2]:
		eventID = automataID + '_E' + str(counterID)	 
		list_of_events.append(eventID)				
		eventLabel = event_info[0]
		eventControl = event_info[1]
		eventObservation = event_info[2]	
		counterID += 1

		# print('eventID = ' + str(eventID))
		# print('eventLabel = ' + str(eventLabel))
		# print('eventControl = ' + str(eventControl))
		# print('eventObservation = ' + str(eventObservation))

		#Generating the event class
		###TEMPORARY###
		if not eventObservation:
			eventFault = True
		else:
			eventFault = False
		###############
		globals()[eventID] = event(eventLabel, eventControl, eventObservation, eventFault)
		list_of_results[5].append(globals()[eventID])

	list_of_results[4] = list_of_events

	#Generating automata model
	#Labelling the automata
	automataLabel = automata_information[0]

	globals()[automataID] = automata(automataLabel, list_of_states, list_of_events, 'NaN')
	list_of_results[0] = automataID
	list_of_results[1] = globals()[automataID]

	# print('-'*25)
	# print(automataID)
	# print('-'*25)
	# print(globals()[automataID].label)
	# print('-'*25)
	# for x in globals()[automataID].set_of_states:
	# 	print(globals()[x].label)
	# print('-'*25)
	# for x in globals()[automataID].set_of_events:
	# 	print(globals()[x].label)
	# print('-'*25)

	return list_of_results

###############################################
###############################################

