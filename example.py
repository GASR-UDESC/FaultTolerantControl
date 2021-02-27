#!/usr/bin/python
#coding: utf-8

import inspect
import operationsOOP as operation
from generationElements import genElements
from elementClasses import automata, state, event
from xmlImportOOP import xmlAutomataImport

automata_information = xmlAutomataImport('valve_a_fault.xmd')

# print('Transicoes')
# for x in automata_information[3]:
#     print(x)

classS1 = genElements('SU1', 'vaf_supervisor_a.xmd')

classF1 = genElements('NY1', 'ny_vaf.xmd')

# print('-'*25)
# print('TEST valve_a_fault')
# print('-'*25)
# print(classF1[1].label)
# print('-'*25)
# for x in classF1[3]:
#     print(str(x.label) + '=>' + str(x.output_transitions))
# print('-'*25)
# for x in classF1[5]:
#     print(x.label)
# print('-'*25)

classF1S1 = operation.syncNF('F1S1', classS1, classF1)



for x in classF1S1:
    print('-'*25)
    print(x)

#print(T[3][0].label)
# a=1
# print(T[0])
# print(isinstance(T[0], state))
# print(type(a))
# print(type(a) is int)