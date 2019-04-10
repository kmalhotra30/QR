from helperFunctions import *
from State import State
from copy import deepcopy
from trace import *
import matplotlib.pyplot as plt
from graphviz import Digraph,Graph
from math import *



is_exogenous = True # To toggle exogenous behaviour on or off
unique_state_dict = {} # To store all states against their unique IDs
edges = {} # To store all edges
state_counter = [1] # Tracker for number of states , using a list to incur changes by reference
exogenous_edges = {}
quantities_list = create_quantities_for_the_model() #List of objects in the state
#quantities_list = create_quantities_for_the_model_extra()
exogenous_nodes = {}

initial_state = State(quantities_list) 


# Setting initial state

initial_state.state_vals[0][0] = '0'
initial_state.state_vals[0][1] = '0'

initial_state.state_vals[1][0] = '0'
initial_state.state_vals[1][1] = '0'

initial_state.state_vals[2][0] = '0'
initial_state.state_vals[2][1] = '0'

# initial_state.state_vals[3][0] = '0'
# initial_state.state_vals[3][1] = '0'

# initial_state.state_vals[4][0] = '0'
# initial_state.state_vals[4][1] = '0'
def generate_transitions_and_states(current_state,quantities_list):

	queue = [] 
	queue.append(current_state)
	while len(queue)!= 0:
		

		# Popping the top element from the queue
		current_state = deepcopy(queue[0])
		queue.pop(0)
		
		#Assign Id to state if not already

		state_obj_tuple = gen_state_tuple(current_state,quantities_list)
		if state_obj_tuple not in unique_state_dict:
			unique_state_dict[state_obj_tuple] = state_counter[0]
			state_counter[0] += 1
	
		

		#Creating possible new states based on transitions i.e interval -> interval, landmark or landmark -> landmark

		current_state = sanity_check_for_extrema_landmark(current_state,quantities_list)
		interval_transition_list = gen_iterval_transition_list(current_state,quantities_list)

		# Update Magnitudes based on gradients

		new_state_list = []	
		for new_state_idx in range(len(interval_transition_list)):

			new_state = deepcopy(current_state)
			for index,quantity in enumerate(current_state.state_vals):


				if quantity[1] == '+':

					curr_mag = quantity[0]
					if interval_transition_list[new_state_idx][index] == 0:

						next_mag  = findNextMag(index,curr_mag,quantities_list)
						#print(next_mag)
						new_state.state_vals[index][0] = next_mag

					else:
						# Interval , so continue
						continue


				if quantity[1] == '-':

					curr_mag = quantity[0]
					if interval_transition_list[new_state_idx][index] == 0:
						
						prev_mag  = findPrevMag(index,curr_mag,quantities_list)
						#print(prev_mag)
						new_state.state_vals[index][0] = prev_mag

					else:
						#Interval , so continue

						continue
			if compare_state_in_dict(new_state_list,new_state) == 1:
				continue
			else:
				new_state_list.append(new_state)

		# Now to sort out influences , propotionalities

		new_states_with_grads = []
		for new_state_idx in range(len(new_state_list)):

			new_state = deepcopy(new_state_list[new_state_idx])
			
			ambiguity_flag = 0
			influence_status = 0

			# for idx in range(len(quantities_list)):

			if sign_map[new_state.state_vals[0][0]]  * sign_map[new_state.state_vals[2][0]] == 1:
				ambiguity_flag = 1

				influence_status_list = [0 , 1 , -1]
				
				if new_state.state_vals[1][1] == '0' :

					influence_status_list = [sign_map[new_state.state_vals[0][1]]] # exogneous one
					
			else :
				ambiguity_flag = 0
				influence_status = sign_map[new_state.state_vals[0][0]] * 1 - 1 * sign_map[new_state.state_vals[2][0]]
				#influence_status = getInfluenceStatusNonAmbigious(idx,new_state,quantities_list)
				influence_status_list = deepcopy([influence_status])
			
			
			for inf_status in influence_status_list:

				if inf_status == 0:

					new_state_with_zero_inf  = deepcopy(new_state)
					new_state_with_zero_inf.state_vals[1][1] = '0'
					
					new_state_with_zero_inf = propogateChangesByPropotionalities(new_state_with_zero_inf,1,quantities_list)


					check_for_adding_state = check_validity_add(new_states_with_grads,new_state_with_zero_inf,quantities_list)

					if check_for_adding_state == True:

						new_state_with_zero_inf = sanity_check_for_extrema_landmark(new_state_with_zero_inf,quantities_list)
		
						new_states_with_grads.append(new_state_with_zero_inf)

					
				if inf_status == 1:

					new_state_list_inf_status_1 = deepcopy(new_state)
					
					new_state_list_inf_status_1.state_vals[1][1] = findNextDerivative(1,current_state.state_vals[1][1],quantities_list)


					new_state_list_inf_status_1 = propogateChangesByPropotionalities(new_state_list_inf_status_1,1,quantities_list)	
					
					check_for_adding_state = check_validity_add(new_states_with_grads,new_state_list_inf_status_1,quantities_list)

					if check_for_adding_state == True:

						new_state_list_inf_status_1 = sanity_check_for_extrema_landmark(new_state_list_inf_status_1,quantities_list)
		
						new_states_with_grads.append(new_state_list_inf_status_1)


					
				if inf_status == -1:

					new_state_list_inf_status_Neg_1 = deepcopy(new_state)
					
					new_state_list_inf_status_Neg_1.state_vals[1cd][1] = findPrevDerivative(1,current_state.state_vals[1][1],quantities_list)


					new_state_list_inf_status_Neg_1 = propogateChangesByPropotionalities(new_state_list_inf_status_Neg_1,1,quantities_list)


					check_for_adding_state = check_validity_add(new_states_with_grads,new_state_list_inf_status_Neg_1,quantities_list)

					if check_for_adding_state == True:

						new_state_list_inf_status_Neg_1 = sanity_check_for_extrema_landmark(new_state_list_inf_status_Neg_1,quantities_list)
		
						new_states_with_grads.append(new_state_list_inf_status_Neg_1)



		#Exogenous Changes
		if is_exogenous == True:

			exogneousChanges(current_state,new_states_with_grads,quantities_list)
			


		new_state_list = deepcopy(new_states_with_grads)
		
		# Pruning by value correspondences and Sanity check for extrema cases

		for idx,new_state in enumerate(new_state_list):

			is_valid = check_validity_value_correspondences(new_state,quantities_list) 
			if is_valid == 0:

				#Doesn't satisfy value correspondences
				new_state_list[idx] = -1

		
		#Removing -1s by copying other elements to another list

		new_state_list_dummy = deepcopy(new_state_list)

		new_state_list_dummy = list(filter(lambda a: a != -1, new_state_list_dummy))

		new_state_list = deepcopy(new_state_list_dummy)


		for idx,new_state in enumerate(new_state_list):

			new_state = sanity_check_for_extrema_landmark(new_state,quantities_list)
			
		#Add edges from the current_state to it's neighbours
		#Add new states to queue , except for the ones that are already in unique_state
		current_state_id = unique_state_dict[gen_state_tuple(current_state,quantities_list)]
		if current_state_id not in edges:
			edges[current_state_id] = []

		for new_state in new_state_list:

			if gen_state_tuple(new_state,quantities_list) not in unique_state_dict :

				unique_state_dict[gen_state_tuple(new_state,quantities_list)] = state_counter[0] 
				state_counter[0] +=1
				queue.append(new_state)
				
			#If condition to prevent self loops
			if current_state_id != unique_state_dict[gen_state_tuple(new_state,quantities_list)]:
			
				if unique_state_dict[gen_state_tuple(new_state,quantities_list)] not in edges[current_state_id]:
					edges[current_state_id].append(unique_state_dict[gen_state_tuple(new_state,quantities_list)])

			
def gen_iterval_transition_list(current_state,quantities_list):

	# Dummy_list to check for interval / landmark ( -1 for interval , 0 for landmark)
	dummy_list = [-2 for quantity in quantities_list]
	number_of_intervals = 0
	no_grad_count = 0
		
	for index,quantity in enumerate(current_state.state_vals):

		curr_mag = quantity[0]
		curr_grad = quantity[1]
		if curr_grad == '0':

			no_grad_count += 1
			continue

		if interval_landmark_map[curr_mag] == 1 and curr_grad!='0':

			dummy_list[index] = -1
			number_of_intervals += 1
		elif interval_landmark_map[curr_mag] == 0 and curr_grad!='0':
			dummy_list[index] = 0
		
		

	#Getting set of binary values to further map to intervals / landmarks
	binary_set = []
	interval_transition_list = []
	
	if number_of_intervals + no_grad_count != len(quantities_list):

		# Point transition before anything else
		interval_transition_list.append(deepcopy(dummy_list))
		for d in range(len(dummy_list)):

			if interval_transition_list[0][d] ==-1:
				interval_transition_list[0][d] = 1
			else:
				interval_transition_list[0][d] = 0
		return interval_transition_list

	for i in range(2 ** (number_of_intervals + no_grad_count)):

		binary = bin(i)[2:]
		number_of_zeros_to_pad = number_of_intervals + no_grad_count - len(binary)
		binary_set.append("0" * number_of_zeros_to_pad + binary)

	#Setting the transitions i.e interval -> interval, landmark or landmark -> landmark
	for idx,b in enumerate(binary_set):

		pointer_for_b = 0
		interval_transition_list.append(deepcopy(dummy_list))
		for d in range(len(dummy_list)):

			if interval_transition_list[idx][d] ==-1:

				interval_transition_list[idx][d] = int(b[pointer_for_b])
				pointer_for_b += 1	


	return interval_transition_list

# def update_magnitudes_based_on_gradients(interval_transition_list,current_state,quantities_list):

	new_state_list = []	
	for new_state_idx in range(len(interval_transition_list)):

		new_state = deepcopy(current_state)
		for index,quantity in enumerate(current_state.state_vals):


			if quantity[1] == '+':

				curr_mag = quantity[0]
				if interval_transition_list[new_state_idx][index] == 0:

					next_mag  = findNextMag(index,curr_mag,quantities_list)
					#print(next_mag)
					new_state.state_vals[index][0] = next_mag

				else:
					# Interval , so continue
					continue


			if quantity[1] == '-':

				curr_mag = quantity[0]
				if interval_transition_list[new_state_idx][index] == 0:
					
					prev_mag  = findPrevMag(index,curr_mag,quantities_list)
					#print(prev_mag)
					new_state.state_vals[index][0] = prev_mag

				else:
					#Interval , so continue

					continue
		if compare_state_in_dict(new_state_list,new_state) == 1:
			continue
		else:
			new_state_list.append(new_state)

		return new_state_list

def exogneousChanges(current_state,new_states_with_grads,quantities_list):

	dummy_new_list = []
	
	current_state_tuple = gen_state_tuple(current_state,quantities_list)
	for new_state in new_states_with_grads:


		new_state_tuple = gen_state_tuple(new_state,quantities_list)
		if new_state.state_vals[0][1] == '+' or new_state.state_vals[0][1] =='-':

			new_state_exo_1 = deepcopy(new_state)
			new_state_exo_1.state_vals[0][1] = '0'
			new_state_exo_1_tuple = gen_state_tuple(new_state_exo_1,quantities_list)


			curr_grad = current_state.state_vals[0][1]
			next_grad = new_state_exo_1.state_vals[0][1]
			if compare_state_in_dict(new_states_with_grads,new_state_exo_1) == 0 and abs(sign_map[next_grad] - sign_map[curr_grad]) <=1:

				dummy_new_list.append(new_state_exo_1)

				if new_state_exo_1_tuple not in exogenous_nodes:

					exogenous_nodes[new_state_exo_1_tuple] = 1

				if current_state_tuple not in exogenous_edges:
					exogenous_edges[current_state_tuple] = []

				
				exogenous_edges[current_state_tuple].append(new_state_exo_1_tuple)

		if new_state.state_vals[0][1] == '0':

			new_state_exo_1 = deepcopy(new_state)
			new_state_exo_1.state_vals[0][1] = '+'
			new_state_exo_1_tuple = gen_state_tuple(new_state_exo_1,quantities_list)


			curr_grad = current_state.state_vals[0][1]
			next_grad = new_state_exo_1.state_vals[0][1]
			if compare_state_in_dict(new_states_with_grads,new_state_exo_1) == 0 and abs(sign_map[next_grad] - sign_map[curr_grad]) <=1 :

				dummy_new_list.append(new_state_exo_1)

				if new_state_exo_1_tuple not in exogenous_nodes:

					exogenous_nodes[new_state_exo_1_tuple] = 1

				if current_state_tuple not in exogenous_edges:
					exogenous_edges[current_state_tuple] = []

				exogenous_edges[current_state_tuple].append(new_state_exo_1_tuple)


			
			new_state_exo_2 = deepcopy(new_state)
			new_state_exo_2.state_vals[0][1] = '-'
			new_state_exo_2_tuple = gen_state_tuple(new_state_exo_2,quantities_list)


			curr_grad = current_state.state_vals[0][1]
			next_grad = new_state_exo_2.state_vals[0][1]
			if compare_state_in_dict(new_states_with_grads,new_state_exo_2) == 0 and abs(sign_map[next_grad] - sign_map[curr_grad]) <=1:

				dummy_new_list.append(new_state_exo_2)

				if new_state_exo_2_tuple not in exogenous_nodes:

					exogenous_nodes[new_state_exo_2_tuple] = 1

				if current_state_tuple not in exogenous_edges:
					exogenous_edges[current_state_tuple] = []

				exogenous_edges[current_state_tuple].append(new_state_exo_2_tuple)


	new_states_with_grads.extend(dummy_new_list)


	

	


def check_validity_add(list_to_be_added_into,new_state,quantities_list):

	if compare_state_in_dict(list_to_be_added_into,new_state) == 0 and determineInfluenceSanity(new_state,quantities_list) == True:

		return True

	return False	


generate_transitions_and_states(initial_state,quantities_list)

dot = Digraph(comment='The State Graph',format='pdf')
dot.attr(layout='dot',splines='true')
for node in unique_state_dict:

	state_tuple = node
	dot.node(str(unique_state_dict[node]),"State : " + str(str(unique_state_dict[node])) + "\n"+ str(str(state_tuple[0]) + "\n" + str(state_tuple[1]) + "\n" + str(state_tuple[2])),shape='box',color="black",tooltip = generate_intra_state_trace(state_tuple,quantities_list))

count_edge = 0
for node in edges:

	node_tuple = list(unique_state_dict.keys())[list(unique_state_dict.values()).index(node)]
	for e in edges[node]:

		edge_tuple = list(unique_state_dict.keys())[list(unique_state_dict.values()).index(e)]
		if node_tuple in exogenous_edges:

			if edge_tuple in exogenous_nodes and edge_tuple in exogenous_edges[node_tuple]:

				count_edge += 1
				dot.edge(str(node), str(e), constraint='true',color='blue')
			else:

				count_edge += 1
				dot.edge(str(node), str(e), constraint='true',color='black')
		else:

			count_edge += 1
			dot.edge(str(node), str(e), constraint='true',color='black')
#dot.render()
dot.render('test-output/spaghetti.gv', view=True)

# for state_tuple in unique_state_dict:

# 	generate_intra_state_trace(state_tuple,quantities_list)

print(count_edge)