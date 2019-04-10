from Quantity import Quantity

sign_map = {'+':1,'Max':1,'0':0,'-':-1}
inverse_priority_sign_map = {1:'+',2:'Max',0:'0',-1:'-'}
interval_landmark_map = {'+':1,'Max':0,'0':0} 



def create_quantities_for_the_model():

	#1 indicates interval , 0 indicates landmark , each quanitity has a priority


	quantity_space_inflow = [('0',0,1),('+',1,1)]
	influences_to_inflow = []
	influences_from_inflow = [('+',1,1)]
	propotionalities_from_inflow = []
	propotionalities_to_inflow = []
	value_correspondeces_from_inflow = []
	value_correspondences_to_inflow = []
	inflow_is_exogenous = True

	quantity_space_volume = [('0',0,1),('+',1,1),('Max',2,1)]
	influences_to_volume = [('+',0,1),('-',2,-1)]
	influences_from_volume = []
	propotionalities_from_volume = [('+',2,1)]
	propotionalities_to_volume = []
	value_correspondences_from_volume = [(0,2),(1,2),(2,2)]
	value_correspondences_to_volume = [(0,2),(1,2),(2,2)]
	volume_is_exogenous = False

	quantity_space_outflow = [('0',0,1),('+',1,1),('Max',2,1)]
	influences_to_outflow = []
	influences_from_outflow = [('-',1,-1)]
	propotionalities_from_outflow = []
	propotionalities_to_outflow = [('+',1,1)]
	value_correspondences_from_outflow = [(0,1),(1,1),(2,1)]
	value_correspondences_to_outflow = [(0,1),(1,1),(2,1)]
	outflow_is_exogenous = False

	inflow_obj = Quantity('Inflow',quantity_space_inflow,inflow_is_exogenous,influences_to_inflow,influences_from_inflow,propotionalities_to_inflow,propotionalities_from_inflow,value_correspondeces_from_inflow,value_correspondences_to_inflow)

	volume_obj = Quantity('Volume',quantity_space_volume,volume_is_exogenous,influences_to_volume,influences_from_volume,propotionalities_to_volume,propotionalities_from_volume,value_correspondences_from_volume,value_correspondences_to_volume)

	outflow_obj = Quantity('Outflow',quantity_space_outflow,outflow_is_exogenous,influences_to_outflow,influences_from_outflow,propotionalities_to_outflow,propotionalities_from_outflow,value_correspondences_from_outflow,value_correspondences_to_outflow)


	quantities_list = [inflow_obj,volume_obj,outflow_obj]
	return quantities_list
					

def findNextMag(quantity_index,current_mag,quantities_list):

	quantity_space = quantities_list[quantity_index].quantity_space
	index_of_current_mag = find_idx_curr_mag(quantity_index,current_mag,quantities_list)

	index_of_next_mag = index_of_current_mag + 1

	if index_of_next_mag >= len(quantity_space):
		return current_mag



	return quantities_list[quantity_index].quantity_space[index_of_next_mag][0]


def findNextDerivative(quantity_index,current_der,quantities_list):

	derivative_space = quantities_list[quantity_index].derivative_space
	index_of_current_der = -1
	for i in range(len(derivative_space)):

		if derivative_space[i] == current_der:

			index_of_current_der = i
			break

	index_of_next_der = index_of_current_der + 1

	
	if index_of_next_der > len(derivative_space) - 1:
		return current_der

	
	return quantities_list[quantity_index].derivative_space[index_of_next_der][0]

def findPrevDerivative(quantity_index,current_der,quantities_list):

	derivative_space = quantities_list[quantity_index].derivative_space
	index_of_current_der = -1
	for i in range(len(derivative_space)):

		if derivative_space[i] == current_der:

			index_of_current_der = i
			break

	index_of_prev_der = index_of_current_der -1 

	if index_of_prev_der < 0:
		return current_der

	return quantities_list[quantity_index].derivative_space[index_of_prev_der][0]

def findPrevMag(quantity_index,current_mag,quantities_list):

	quantity_space = quantities_list[quantity_index].quantity_space
	index_of_current_mag = find_idx_curr_mag(quantity_index,current_mag,quantities_list)
	
	index_of_prev_mag = index_of_current_mag -1

	if index_of_prev_mag < 0:
		return current_mag

	return quantities_list[quantity_index].quantity_space[index_of_prev_mag][0]

def check_validity_value_correspondences(state,quantities_list):

	# Essentially checking for value correspondences
	flag = 1
	for index,quanitity in enumerate(quantities_list):


		if flag == 0:
			break

		value_correspondeces_from_quantity = quantities_list[index].value_correspondences_list_from_quantity
		if len(value_correspondeces_from_quantity) == 0 :

			continue


		current_mag = state.state_vals[index][0]
		idx_of_mag = find_idx_curr_mag(index,current_mag,quantities_list)
		for vc in value_correspondeces_from_quantity:

			if vc[0] == idx_of_mag:

				if state.state_vals[vc[1]][0] != current_mag:

					flag = 0
					break

	return flag

def find_idx_curr_mag(index,current_mag,quantities_list):

	idx_of_mag = -1
	quantity_space = quantities_list[index].quantity_space

	for idx_mag,mag in enumerate(quantity_space):

		if mag[0] == current_mag:

			idx_of_mag = idx_mag
			break 

	return idx_of_mag


def gen_state_tuple(state_obj,quantities_list):

	state_view = []
	for idx,quanitity in enumerate(quantities_list):

		state_view.append((state_obj.state_vals[idx][0],state_obj.state_vals[idx][1]))
	
	return tuple(state_view)

def print_state(state_obj,quantities_list):

	print(gen_state_tuple(state_obj,quantities_list))

	
def compare_states(state_1,state_2):

	flag = 1
	if state_1.state_vals != state_2.state_vals:
		flag = 0
	return flag

def compare_state_in_dict(dictionary,state):

	flag = 0

	for state_in_dict in dictionary:

		if compare_states(state,state_in_dict) == 1:

			flag = 1
			break

	return flag

def sanity_check_for_extrema_landmark(state,quantities_list):

	flag = 1
	for idx,quantity in enumerate(state.state_vals):

		if quantity[0] == 'Max' and quantity[1] == '+':
			quantity[1] = '0'
		if quantity[0] == '0' and quantity[1] == '-':
			quantity[1] = '0'
		# current_mag = quantity[0]
		# if interval_landmark_map[current_mag] == 0:
			
		# 	idx_of_mag = find_idx_curr_mag(idx,current_mag,quantities_list)
		# 	quantity_space = quantities_list[idx].quantity_space 
		# 	if quantity_space[idx_of_mag][1] == len(quantity_space) - 1 :

		# 		if quantity[1] == '+':

		# 			quantity[1] = '0'
		# 			flag = 0
		# 			#break

		# 	elif quantity_space[idx_of_mag][1] == 0:

		# 		if quantity[1] == '-':

		# 			quantity[1] = '0'
		# 			flag = 0
		# 			#break
		#state.state_vals[idx] = quantity

	return state

def determineInfluenceSanity(state,quantities_list):

	if sign_map[state.state_vals[0][0]] == 0 and sign_map[state.state_vals[2][0]]!=0 or  sign_map[state.state_vals[2][0]] == 0 and sign_map[state.state_vals[0][0]]!=0:

			#print(gen_state_tuple(state,quantities_list))
			if sign_map[state.state_vals[1][1]] == 0:
				return False

	return True

def propogateChangesByPropotionalities(new_state,index,quantities_list):

	propotionalities_from_quantity = quantities_list[index].propotionalities_from_quantity

	for prop in propotionalities_from_quantity :

		prop_quantity_index = prop[1]
		prop_type = prop[2] # -1 or 1

		if prop_type * sign_map[new_state.state_vals[index][1]] == 1:

			new_state.state_vals[prop_quantity_index][1] = findNextDerivative(prop_quantity_index,new_state.state_vals[prop_quantity_index][1],quantities_list)

		elif prop_type * sign_map[new_state.state_vals[index][1]] == -1:

			new_state.state_vals[prop_quantity_index][1] = findPrevDerivative(prop_quantity_index,new_state.state_vals[prop_quantity_index][1],quantities_list)

		else:
			# No change in derivative
			new_state.state_vals[prop_quantity_index][1] = new_state.state_vals[index][1]

		new_state = propogateChangesByPropotionalities(new_state,prop_quantity_index,quantities_list)

	return new_state

def create_quantities_for_the_model_extra():

	#1 indicates interval , 0 indicates landmark , each quanitity has a priority


	quantity_space_inflow = [('0',0,1),('+',1,1)]
	influences_to_inflow = []
	influences_from_inflow = [('+',1,1)]
	propotionalities_from_inflow = []
	propotionalities_to_inflow = []
	value_correspondeces_from_inflow = []
	value_correspondences_to_inflow = []
	inflow_is_exogenous = True

	quantity_space_volume = [('0',0,1),('+',1,1),('Max',2,1)]
	influences_to_volume = [('+',0,1),('-',2,-1)]
	influences_from_volume = []
	propotionalities_from_volume = [('+',3,1)]
	propotionalities_to_volume = []
	value_correspondences_from_volume = [(0,3),(1,3),(2,3)]
	value_correspondences_to_volume = [(0,3),(1,3),(2,3)]
	volume_is_exogenous = False

	quantity_space_outflow = [('0',0,1),('+',1,1),('Max',2,1)]
	influences_to_outflow = []
	influences_from_outflow = [('-',1,-1)]
	propotionalities_from_outflow = []
	propotionalities_to_outflow = [('+',4,1)]
	value_correspondences_from_outflow = [(0,4),(1,4),(2,4)]
	value_correspondences_to_outflow = [(0,4),(1,4),(2,4)]
	outflow_is_exogenous = False

	quantity_space_height = [('0',0,1),('+',1,1),('Max',2,1)]
	influences_to_height = []
	influences_from_height = []
	propotionalities_from_height = [('+',4,1)]
	propotionalities_to_height = [('+',1,1)]
	value_correspondences_from_height = [(0,1),(1,1),(2,1),(0,4),(1,4),(2,4)]
	value_correspondences_to_height = [(0,1),(1,1),(2,1),(0,4),(1,4),(2,4)]
	height_is_exogenous = False

	quantity_space_pressure = [('0',0,1),('+',1,1),('Max',2,1)]
	influences_to_pressure = []
	influences_from_pressure = []
	propotionalities_from_pressure = [('+',2,1)]
	propotionalities_to_pressure = [('+',3,1)]
	value_correspondences_from_pressure = [(0,3),(1,3),(2,3),(0,2),(1,2),(2,2)]
	value_correspondences_to_pressure = [(0,2),(1,2),(2,2),(0,3),(1,3),(2,3)]
	pressure_is_exogenous = False

	inflow_obj = Quantity('Inflow',quantity_space_inflow,inflow_is_exogenous,influences_to_inflow,influences_from_inflow,propotionalities_to_inflow,propotionalities_from_inflow,value_correspondeces_from_inflow,value_correspondences_to_inflow)

	volume_obj = Quantity('Volume',quantity_space_volume,volume_is_exogenous,influences_to_volume,influences_from_volume,propotionalities_to_volume,propotionalities_from_volume,value_correspondences_from_volume,value_correspondences_to_volume)

	outflow_obj = Quantity('Outflow',quantity_space_outflow,outflow_is_exogenous,influences_to_outflow,influences_from_outflow,propotionalities_to_outflow,propotionalities_from_outflow,value_correspondences_from_outflow,value_correspondences_to_outflow)

	height_obj = Quantity('Height',quantity_space_height,height_is_exogenous,influences_to_height,influences_from_height,propotionalities_to_height,propotionalities_from_height
		,value_correspondences_from_height,value_correspondences_to_height)

	pressure_obj = Quantity('Height',quantity_space_pressure,pressure_is_exogenous,influences_to_pressure,influences_from_pressure,propotionalities_to_pressure,propotionalities_from_pressure
		,value_correspondences_from_pressure,value_correspondences_to_pressure)


	quantities_list = [inflow_obj,volume_obj,outflow_obj,height_obj,pressure_obj]
	return quantities_list

def is_ambigious(idx,new_state,quantities_list):

	flag = 0
	influences_to_quantity = quantities_list[idx].influences_to_quantity
	if len(influences_to_quantity) <= 0:
		return flag
	prev_inf = influences_to_quantity[0][2] * new_state.state_vals[influences_to_quantity[0][1]][0]
	for index in range(1,len(influences_to_quantity)):
		new_inf = influences_to_quantity[index][2] * new_state.state_vals[influences_to_quantity[index][1]][0]

		if new_inf!=prev_inf:

			flag = 1
			break

		prev_inf = new_inf

	return flag

def getInfluenceStatusNonAmbigious(idx,new_states,quantities_list):

	influences_to_quantity = quantities_list[idx].influences_to_quantity
	inf_status = []
	if len(influences_to_quantity) <= 0:
		return inf_status

	print(idx)
	inf_status[0] = 0
	for inf in influences_to_quantity:

		inf_status[0]+= inf[2] * sign_map[new_state.state_vals[inf[1]][0]]

	return inf_status	
	



