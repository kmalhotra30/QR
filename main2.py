from helperFunctions import *
from State import State
from copy import deepcopy
import matplotlib.pyplot as plt
from graphviz import Digraph
import networkx as nx
import pygraphviz as pgv


sign_map = {'+':1,'Max':1,'0':0,'-':-1}
inverse_priority_sign_map = {1:'+',2:'Max',0:'0',-1:'-'}
interval_landmark_map = {'+':1,'Max':0,'0':0} 
unique_state_dict = {}
edges = {}
state_counter = [1]
influence_status_dict = {}

quantities_list = create_quantities_for_the_model()

initial_state = State(quantities_list)
initial_state.state_vals[0][0] = '0'
initial_state.state_vals[0][1] = '+'

initial_state.state_vals[1][0] = '0'
initial_state.state_vals[1][1] = '0'

initial_state.state_vals[2][0] = '0'
initial_state.state_vals[2][1] = '0'

def generate_transitions_and_states(current_state,quantities_list):

	# Doing only influences
	queue = []
	queue.append(current_state)
	while len(queue)!= 0:
		

		# Popping the top element from the queue
		current_state = deepcopy(queue[0])
		queue.pop(0)
		
		#Assign Id to state if not already

		if gen_state_tuple(current_state,quantities_list) not in unique_state_dict:
			unique_state_dict[gen_state_tuple(current_state,quantities_list)] = state_counter[0]
			state_counter[0] += 1
	
		# Dummy_list to check for interval / landmark ( -1 for interval , 0 for landmark)
		dummy_list = [0 for quantity in quantities_list]
		number_of_intervals = 0
		for index,quantity in enumerate(current_state.state_vals):

			curr_mag = quantity[0]
			if interval_landmark_map[curr_mag] == 1:

				dummy_list[index] = -1
				number_of_intervals += 1

		#Getting set of binary values to further map to intervals / landmarks
		binary_set = []
		for i in range(2 ** number_of_intervals):

			binary = bin(i)[2:]
			number_of_zeros_to_pad = number_of_intervals - len(binary)
			binary_set.append("0" * number_of_zeros_to_pad + binary)

		#Setting the transitions i.e interval -> interval, landmark or landmark -> landmark
		interval_transition_list = []
		for idx,b in enumerate(binary_set):

			pointer_for_b = 0
			interval_transition_list.append(deepcopy(dummy_list))
			for d in range(len(dummy_list)):

				if interval_transition_list[idx][d] ==-1:

					interval_transition_list[idx][d] = int(b[pointer_for_b])
					pointer_for_b += 1

		#Creating possible new states based on transitions i.e interval -> interval, landmark or landmark -> landmark
		new_state_list = []	

		for new_state_idx in range(len(interval_transition_list)):

			new_state = deepcopy(current_state)
			for index,quantity in enumerate(current_state.state_vals):


				if quantity[1] == '+':

					curr_mag = quantity[0]
					index_next_mag = findNextMag(index,quantity[0],quantities_list)

					if interval_transition_list[new_state_idx][index] == 0:

						if index_next_mag != -1:

							next_mag  = quantities_list[index].quantity_space[index_next_mag][0]
							new_state.state_vals[index][0] = next_mag
					else:
						# Interval , so continue
						continue


				if quantity[1] == '-':

					curr_mag = quantity[0]
					index_prev_mag = findPrevMag(index,quantity[0],quantities_list)
					if interval_transition_list[new_state_idx][index] == 0:
						
						if index_prev_mag != -1:

							prev_mag  = quantities_list[index].quantity_space[index_prev_mag][0]
							new_state.state_vals[index][0] = prev_mag
					else:
						#Interval , so continue

						continue
			if compare_state_in_dict(new_state_list,new_state) == 1:
				continue
			else:
				new_state_list.append(new_state)
					

		# Now to sort out influences , propotionalities

		if unique_state_dict[gen_state_tuple(current_state,quantities_list)] not in influence_status_dict:

			influence_status_dict[unique_state_dict[gen_state_tuple(current_state,quantities_list)]] = []

		current_state_influence_list = influence_status_dict[unique_state_dict[gen_state_tuple(current_state,quantities_list)]]

		new_states_with_grads = []
		for new_state_idx in range(len(new_state_list)):

			new_state = deepcopy(new_state_list[new_state_idx])
			influence_status_list = []
			ambiguity_flag = 0
			influence_status = 0
			if new_state.state_vals[0][0] == '+' and new_state.state_vals[2][0] == '+':
				ambiguity_flag = 1
				influence_status_list = [0 , 1 , -1]

			elif new_state.state_vals[0][0] == '+' and new_state.state_vals[2][0] == 'Max':
				ambiguity_flag = 1
				influence_status_list = [0 , 1 , -1]

			else :
				ambiguity_flag = 0
				influence_status = sign_map[new_state.state_vals[0][0]] * 1 + -1 * sign_map[new_state.state_vals[2][0]]

				influence_status_list = [influence_status]
			
			if len(influence_status_list) >=1 and len(current_state_influence_list)>=1:
			
				if -1 in influence_status_list and 1 in current_state_influence_list :

					influence_status_list.remove(-1)

				if 1 in influence_status_list and -1 in current_state_influence_list :

					influence_status_list.remove(1)


			for inf_status in influence_status_list:

				if inf_status == 0:

					new_state_with_zero_inf  = deepcopy(new_state)
					new_state_with_zero_inf.state_vals[1][1] = '0'
					new_state_with_zero_inf.state_vals[2][1] = '0'

					new_state_with_zero_inf_exo_1 = deepcopy(new_state_with_zero_inf)
					new_state_with_zero_inf_exo_2 = deepcopy(new_state_with_zero_inf)					
					if current_state.state_vals[0][1] == '+' or current_state.state_vals[0][1] == '-':

						new_state_with_zero_inf_exo_1.state_vals[0][1] = '0'
					
					elif current_state.state_vals[0][1] == '0':

						new_state_with_zero_inf_exo_1.state_vals[0][1] = '+'
						new_state_with_zero_inf_exo_2.state_vals[0][1] = '-'


					if compare_state_in_dict(new_states_with_grads,new_state_with_zero_inf) == 0:
						new_states_with_grads.append(new_state_with_zero_inf)

					if compare_state_in_dict(new_states_with_grads,new_state_with_zero_inf_exo_1) == 0:
						new_states_with_grads.append(new_state_with_zero_inf_exo_1)

					if compare_state_in_dict(new_states_with_grads,new_state_with_zero_inf_exo_2) == 0:
						new_states_with_grads.append(new_state_with_zero_inf_exo_2)

					
				if inf_status == 1:

					new_state_list_inf_status_1 = deepcopy(new_state)
					
					if current_state.state_vals[1][1] == '0' or current_state.state_vals[1][1]=='+':
						new_state_list_inf_status_1.state_vals[1][1] = '+'
						new_state_list_inf_status_1.state_vals[2][1] = '+'
						
					new_state_list_inf_status_1_exo_1 = deepcopy(new_state_list_inf_status_1)
					new_state_list_inf_status_1_exo_2 = deepcopy(new_state_list_inf_status_1)					
					if current_state.state_vals[0][1] == '+' or current_state.state_vals[0][1] == '-':

						new_state_list_inf_status_1_exo_1.state_vals[0][1] = '0'
					
					elif current_state.state_vals[0][1] == '0':

						new_state_list_inf_status_1_exo_1.state_vals[0][1] = '+'
						new_state_list_inf_status_1_exo_2.state_vals[0][1] = '-'


					if compare_state_in_dict(new_states_with_grads,new_state_list_inf_status_1) == 0:
						new_states_with_grads.append(new_state_list_inf_status_1)

					if compare_state_in_dict(new_states_with_grads,new_state_list_inf_status_1_exo_1) == 0:
						new_states_with_grads.append(new_state_list_inf_status_1_exo_1)

					if compare_state_in_dict(new_states_with_grads,new_state_list_inf_status_1_exo_2) == 0:
						new_states_with_grads.append(new_state_list_inf_status_1_exo_2)

				if inf_status == -1:

					new_state_list_inf_status_Neg_1 = deepcopy(new_state)
						
					if current_state.state_vals[1][1] == '0' or current_state.state_vals[1][1]=='-':
					
						new_state_list_inf_status_Neg_1.state_vals[1][1] = '-'
						new_state_list_inf_status_Neg_1.state_vals[2][1] = '-'

					new_state_list_inf_status_Neg_1_exo_1 = deepcopy(new_state_list_inf_status_Neg_1)
					new_state_list_inf_status_Neg_1_exo_2 = deepcopy(new_state_list_inf_status_Neg_1)					
					if current_state.state_vals[0][1] == '+' or current_state.state_vals[0][1] == '-':

						new_state_list_inf_status_Neg_1_exo_1.state_vals[0][1] = '0'
					
					elif current_state.state_vals[0][1] == '0':

						new_state_list_inf_status_Neg_1_exo_1.state_vals[0][1] = '+'
						new_state_list_inf_status_Neg_1_exo_2.state_vals[0][1] = '-'


					if compare_state_in_dict(new_states_with_grads,new_state_list_inf_status_Neg_1) == 0:
						new_states_with_grads.append(new_state_list_inf_status_Neg_1)

					if compare_state_in_dict(new_states_with_grads,new_state_list_inf_status_Neg_1_exo_1) == 0:
						new_states_with_grads.append(new_state_list_inf_status_Neg_1_exo_1)

					if compare_state_in_dict(new_states_with_grads,new_state_list_inf_status_Neg_1_exo_2) == 0:
						new_states_with_grads.append(new_state_list_inf_status_Neg_1_exo_2)



		new_state_list = deepcopy(new_states_with_grads)
		
		# Pruning by value correspondences
		for idx,new_state in enumerate(new_state_list):

			is_valid = check_validity_value_correspondences(new_state,quantities_list)
			if is_valid == 0:

				#Doesn't satisfy value correspondences
				new_state_list[idx] = -1

		
		#Removing -1s by copying other elements to another list

		new_state_list_dummy = deepcopy(new_state_list)

		new_state_list_dummy = list(filter(lambda a: a != -1, new_state_list_dummy))

		new_state_list = deepcopy(new_state_list_dummy)
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
			
			edges[current_state_id].append(unique_state_dict[gen_state_tuple(new_state,quantities_list)])

			influence_status_dict[unique_state_dict[gen_state_tuple(new_state,quantities_list)]] = influence_status_list

		print(unique_state_dict)
		print("\n\n\n")
		print(edges)
		print("\n\n\n")
		
generate_transitions_and_states(initial_state,quantities_list)
# print(unique_state_dict)
# print(edges)
print(influence_status_dict)
G=pgv.AGraph(strict=False,directed=True,size="50,50")
for node in unique_state_dict:

	state_tuple = node
	G.add_node(unique_state_dict[node],fontsize = 10,shape = 'box',width=0.002,label=str(state_tuple[0]) + "\n" + str(state_tuple[1]) + "\n" + str(state_tuple[2]))

for node in edges:

	for e in edges[node]:

		G.add_edge(node,e)

G.layout()
G.draw('file.png')

# dot = Digraph(comment='The State Graph',format='png')
# for node in unique_state_dict:

# 	dot.node(str(unique_state_dict[node]),str(node))

# dot_edges = []
# for node in edges:

# 	for e in edges[node]:
# 		dot_edges.append(str(node) + str(e))
# print(dot_edges[:16])
# dot.edges(dot_edges[:16])
# # dot.node('A', 'King Arthur')
# # dot.node('B', 'Sir Bedevere the Wise')
# # dot.node('L', 'Sir Lancelot the Brave')
# # dot.edges(['AB', 'AL','AA'])
# # dot.edge('B', 'L', constraint='false')
# #print(dot.source)
# dot.render()
# #dot.render('test-output/round-table.gv', view=True)

# G=nx.DiGraph()
# for node in unique_state_dict:
# 	G.add_node(unique_state_dict[node])
# G_edges = []
# for node in edges:

# 	for e in edges[node]:

# 		G_edges.append((node,e))
# G.add_edges_from(G_edges)
# nx.draw(G)
# plt.show()
