from helperFunctions import *

grad_MAP = {'+':'increasing','-':'decreasing','0':'steady'}
mag_MAP = {'+':'positive','-':'negative','Max':'maximum','0':'zero'}
inf_MAP = {'+':'a positive dominant','0':'no dominant','-':'a negative dominant'}

def generate_intra_state_trace(state_id,quantities_list,unique_state_dict):

    state_tuple = getKeyByValue(unique_state_dict,state_id)
    trace = ""
    for idx,quantity in enumerate(quantities_list):

        if quantity.is_exogenous == True:

            continue

        else:

            if is_ambigious(idx,state_tuple,quantities_list) == 1:

                trace+= quantity.name + " has " + inf_MAP[state_tuple[idx][1]] + " influence and is " + grad_MAP[state_tuple[idx][1]] + '.'


            else:

                influences_to_quantity = quantity.influences_to_quantity
                
                if len(influences_to_quantity) > 0:

                    trace+= quantity.name + " is " + grad_MAP[state_tuple[idx][1]] + " because of influences from"
                    for (inf_idx,inf) in enumerate(influences_to_quantity):

                        trace+= " " + str(quantities_list[inf[1]].name)
                        if inf_idx == len(influences_to_quantity) -1 :
                            continue
                        if inf_idx == len(influences_to_quantity) - 2:
                            trace+= " and"
                        else:
                            trace+= " ,"

                    trace += "."
                
                propotionalities_to_quantity = quantity.propotionalities_to_quantity
                
                if len(propotionalities_to_quantity) > 0:

                    trace+= quantity.name + " is " + grad_MAP[state_tuple[idx][1]] + " because of propotionality from"

                    for (prop_idx,prop) in enumerate(propotionalities_to_quantity):

                        trace+= " " + str(quantities_list[prop[1]].name)
                        if prop_idx == len(propotionalities_to_quantity) -1 :
                            continue
                        if prop_idx == len(propotionalities_to_quantity) - 2:
                            trace+= " and"
                        else:
                            trace+= " ,"

                    trace += "."

    return trace


def generate_inter_state_trace(state_id_from,state_id_to,unique_state_dict,quantities_list,exogenous_edges,exogenous_nodes):

    state_tuple_from = getKeyByValue(unique_state_dict,state_id_from)
    state_tuple_to = getKeyByValue(unique_state_dict,state_id_to)
    
    trace=""
    flag = 0
    for idx,quantity in enumerate(quantities_list):

        if quantity.is_exogenous == True:

            if state_tuple_from in exogenous_edges:

                if state_tuple_to in exogenous_nodes and state_tuple_to in exogenous_edges[state_tuple_from]:

                    flag = 1
                    trace+= "Due to exogenous factors, " + quantities_list[idx].name + " is " + grad_MAP[state_tuple_to[idx][1]] + "."


        if state_tuple_from[idx][0]!=state_tuple_to[idx][0]:

            flag = 1
            trace+= "Magnitude of " + quantity.name + " has changed from " + mag_MAP[state_tuple_from[idx][0]] + " to " + mag_MAP[state_tuple_to[idx][0]] + "."

    if flag == 0:

        trace += "There is no change in Magnitude, but due to Influences and Propotionality, "
        for idx,quantity in enumerate(quantities_list):

            if quantity.is_exogenous == False:

               if state_tuple_from[idx][1] != state_tuple_to[idx][1]:
               
                    trace+= quantity.name +" is " + grad_MAP[state_tuple_to[idx][1]] + ","

        trace = trace[:-1]
        trace = trace + "."            

    return trace


    