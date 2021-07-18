#!/usr/bin/python
#coding: utf-8

# 17Jul21 => Code for supporting the development of the switching module  

import inspect
import operationsOOP as operation
from observerOOP import observer
from generationElements import genElements
from elementClasses import automata, state, event
from xmlImportOOP import xmlAutomataImport

########################################################################
########################################################################
# Import of Supervisors
print('##### Importação de Supervisores #####')
print('')

classS1 = genElements('S1', 'xmd/supervisor_a.xmd') # S = Supervisor
print('-'*25)
print('=> Supervisor A')
print('-'*25)
print('*Estados*')
for x in classS1[3]:
	print(x.label)
print('-'*25)
print('*Eventos*')
for x in classS1[5]:
	print(x.label)
print('-'*25)
print('')

classS2 = genElements('S2', 'xmd/supervisor_b.xmd') # S = Supervisor
print('-'*25)
print('=> Supervisor B')
print('-'*25)
print('*Estados*')
for x in classS2[3]:
	print(x.label)
print('-'*25)
print('*Eventos*')
for x in classS2[5]:
	print(x.label)
print('-'*25)
print('')

########################################################################
########################################################################
# Import of Faulty Subsystems
print('##### Importação de Subsistemas com Falhas #####')
print('')

classF1 = genElements('F1', 'xmd/valve_a_fault.xmd') # F = Faulty Subsystem
print('-'*50)
print('=> Subsistema da Válvula A com Falha de Vazamento')
print('-'*50)
print('*Estados*')
for x in classF1[3]:
	print(x.label)
print('-'*25)
print('*Eventos*')
for x in classF1[5]:
	print(x.label)
print('-'*50)
print('')

classF2 = genElements('F2', 'xmd/valve_b_fault.xmd') # F = Faulty Subsystem
print('-'*50)
print('=> Subsistema da Válvula B com Falha de Vazamento')
print('-'*50)
print('*Estados*')
for x in classF2[3]:
	print(x.label)
print('-'*25)
print('*Eventos*')
for x in classF2[5]:
	print(x.label)
print('-'*50)
print('')

classF3 = genElements('F3', 'xmd/valve_d_fault.xmd') # F = Faulty Subsystem
print('-'*50)
print('=> Subsistema da Válvula D com Falha de Travamento Fechada')
print('-'*50)
print('*Estados*')
for x in classF3[3]:
	print(x.label)
print('-'*25)
print('*Eventos*')
for x in classF3[5]:
	print(x.label)
print('-'*50)
print('')

########################################################################
########################################################################
# List of Information Received from Observers

# OBS1 => Safe Controllability by Diagnosis of 'valve_a_fault' in Supervisor A
list_OBS1 = ['OBS1_S17',[['P1,VA1,VC1,VD1,1,VAF1', 'Y', 'NB']],
	[[[['P1,VA2,VC1,VD1,3,VAF2', 'Y', 'B']], 'VA_open']]]

# OBS2 => Safe Controllability by Diagnosis of 'valve_d_fault' in Supervisor A
list_OBS2 = ['OBS2_S18',[['P1,VA1,VC1,VD1,1,VAF1', 'Y', 'NB']],
	[[[['P2,VA1,VC1,VD3,3,VDF1', 'Y', 'B']], 'P_start']]]

# OBS3 => Safe Controllability by Diagnosis of 'valve_b_fault' in Supervisor B
list_OBS3 = ['OBS3_S17',[['P1,VB1,VC1,VD1,1,VBF1', 'Y', 'NB']],
	[[[['P1,VB2,VC1,VD1,3,VBF2', 'Y', 'B']], 'VB_open']]]

# OBS4 => Safe Controllability by Diagnosis of 'valve_d_fault' in Supervisor B
list_OBS4 = ['OBS4_S18',[['P1,VB1,VC1,VD1,1,VBF1', 'Y', 'NB']],
	[[[['P2,VB1,VC1,VD3,3,VDF1', 'Y', 'B']], 'P_start']]]