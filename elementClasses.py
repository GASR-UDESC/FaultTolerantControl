#!/usr/bin/python
#coding: utf-8

'''
Code for Python 3
Author: Herbert Leitão
Date Version 1: 12/02/2021
Comments: library created for generating states and events classes
'''

class state:
	"""docstring for state"""
	def __init__(self, label, is_marked, is_initial, **kwargs):
		input_transitions = kwargs.get('input_transitions')
		output_transitions = kwargs.get('output_transitions')
		self.label = label								#list		
		self.is_marked = is_marked						#bool
		self.is_initial = is_initial					#bool
		self.input_transitions = input_transitions		#list = [[state, event]...]
		self.output_transitions = output_transitions	#list = [[state, event]...]

class event:
	"""docstring for event"""
	def __init__(self, label, is_controllable, is_observable, is_a_fault):		
		self.label = label								#string
		self.is_controllable = is_controllable			#bool
		self.is_observable = is_observable				#bool
		self.is_a_fault = is_a_fault					#bool

class automata:
	"""docstring for ClassName"""
	def __init__(self, label, set_of_states, set_of_events, automata_type):		
		self.label = label								#string
		self.set_of_states = set_of_states				#list
		self.set_of_events = set_of_events				#list
		self.automata_type = automata_type				#string

	def __repr__(self):
		return self.label+"\n"+self.set_of_states+"\n"+self.set_of_events

# TEST
# class automata:
# 	"""docstring for ClassName"""
# 	def __init__(self, label):		
# 		self.label = label								#string
# 		# self.set_of_states = set_of_states				#list
# 		# self.set_of_transitions = set_of_transitions	#list
# 		# self.automata_type = automata_type
		
		
