'''

    CÓDIGO PARA CONVERTER O XML DO IDES EM UMA CLASSE DE AUTOMATO DO NADZORU
    
    BOA PARTE FOI RECICLADA DO CÓDIGO "IMPORT FROM IDES3"

'''

from elementClasses import automata,event,state

import xml.etree.ElementTree as ET

def createAutomaton(xml):
    tree = ET.parse(xml)
    root = tree.getroot()

    initial_state = None

    transitions_dictionary = dict()
    states_list = dict()
    events_list = dict()

    states = root.findall('./data/state') #MUITO IMPORTANTE, NÃO TIRE O ./ e nem o data!!!
    events = root.findall('./data/event')
    trans  = root.findall('./data/transition')

    for s in states:
        id =   s.attrib['id']
        name = s.findall('name')[0].text
        init = s.findall('properties')[0].findall('initial')
        mark = s.findall('properties')[0].findall('marked')

        if (mark): mark = True
        else: mark = False
        
        state_ = State(name,mark)
        states_list[id] = state_
        if (init): initial_state = state_

    for e in events:
        id =   e.attrib['id']
        name = e.findall('name')[0].text
        con  = e.findall('properties')[0].findall('controllable')
        obs  = e.findall('properties')[0].findall('observable')

        if (con): con = True
        else: con = False

        if (obs): obs = True
        else: obs = False
        
        events_list[id] = Event(name,con,obs)

    for t in trans:
        id = t.attrib['id']
        src = t.attrib['source']
        des = t.attrib['target']
        ev  = t.attrib['event']
        
        source, target, event = states_list[src],states_list[des],events_list[ev]
        
        #print("adding(",id,"): ",source," = (",event,",",target,")")
        if source in transitions_dictionary:
            transitions_dictionary[source][event] = target
        else:
            transitions_dictionary[source] = {event:target}
    return Automaton(transitions_dictionary,initial_state)