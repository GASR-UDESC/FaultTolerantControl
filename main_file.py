'''
Code for Python 3
Author: Herbert Leitão
Date Version 1: 12/02/2021
Comments: Main file operation
'''

from xmlImportOOP import xmlAutomataImport
from elementClasses import automata, state, event

automata1_information = xmlAutomataImport('supervisor.xmd')

# for x in automata1_information:
# 	print(x)

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

	print('stateID = ' + str(stateID))
	print('stateMarking = ' + str(stateMarking))
	print('stateInitial = ' + str(stateInitial))
	print('outputTransition = ' + str(outputTransition))

	globals()[stateID] = state(stateLabel, stateMarking, stateInitial, 
		output_transitions = outputTransition, input_transitions = [])

#Finding transition functions and filling input_transitions lists in states
for sublist in automata1_information[3]:
	for transition_info in sublist:
		targetState = transition_info[2]
		for stateID in list_of_states:
			if targetState == globals()[stateID].label:
				globals()[stateID].input_transitions.append([transition_info[0], transition_info[1]])
				break

print('-'*25)
print('A1_S0 = ' + str(A1_S0.label))
print('stateMarking = ' + str(A1_S0.is_marked))
print('stateInitial = ' + str(A1_S0.is_initial))
print('inputTransition = ' + str(A1_S0.input_transitions))
print('outputTransition = ' + str(A1_S0.output_transitions))
print('-'*25)

#Extracting information of the events [LABEL, CONTROLLABLE, OBSERVABLE]
counterID = 0
for event_info in automata1_information[2]:
	eventID = eventID_model + str(counterID)	 
	list_of_events.append(eventID)				
	eventLabel = event_info[0]
	eventControl = event_info[1]
	eventObservation = event_info[2]	
	counterID += 1

	print('eventID = ' + str(eventID))
	print('eventLabel = ' + str(eventLabel))
	print('eventControl = ' + str(eventControl))
	print('eventObservation = ' + str(eventObservation))

	globals()[eventID] = event(eventLabel, eventControl, eventObservation, False)

#Generating Automata 1 model
#Labelling Automata 1
automataLabel = automata1_information[0]
#print(type(A1.label)) # string OK

A1 = automata(automataLabel, list_of_states, list_of_events, 'NaN')

print('-'*25)
for x in A1.set_of_states:
	print(globals()[x].label)
print('-'*25)
for x in A1.set_of_events:
	print(globals()[x].label)
print('-'*25)

###############################################
###############################################

