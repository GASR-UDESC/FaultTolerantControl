#!/usr/bin/python
#coding: utf-8

'''
Code for Python 3
Author: Herbert Leitão
Date Version: 19/03/2021
Comments: library created for generating states and events classes
Comments: updating state class
'''

class state:
	"""docstring for state"""
	def __init__(self, label=list(), is_marked=False, is_initial=False, **kwargs):
		stateID = kwargs.get('stateID')
		input_transitions = kwargs.get('input_transitions')
		output_transitions = kwargs.get('output_transitions')
		self.id = stateID								#string
		self.label = label								#list		
		self.is_marked = is_marked						#bool
		self.is_initial = is_initial					#bool
		# self.has_a_fault_label = None					#bool
		# self.has_a_bad_label = None						#bool
		self.input_transitions = input_transitions		#list = [[state, event]...]
		self.output_transitions = output_transitions	#list = [[state, event]...]

	def label_eval(self): # Method for updating attributes related to NY and BNB labels
		if self.label[1] == 'F' or self.label[1] == 'Y':
			self.has_a_fault_label = True
		else:
			self.has_a_fault_label = False
		if self.label[2] == 'B':
			self.has_a_bad_label = True
		else:
			self.has_a_bad_label = False

class event:
	"""docstring for event"""
	def __init__(self, label, is_controllable, is_observable, is_a_fault):		
		self.label = label								#string
		self.is_controllable = is_controllable			#bool
		self.is_observable = is_observable				#bool
		self.is_a_fault = is_a_fault					#bool

class automata:
	"""docstring for ClassName"""
	def __init__(self, label, set_of_states, set_of_events, automata_type, **kwargs):		
		self.label = label								#string
		self.set_of_states = set_of_states				#list
		self.set_of_events = set_of_events				#list
		self.set_of_bad_states = set()					#set
		self.automata_type = automata_type				#string
		self.is_diag = None								#bool
		self.is_safe_diag = None						#bool
		self.is_safe_control = None						#bool


		
