from Quantity import Quantity


def create_quantities_for_the_model():

	#1 indicates interval , 0 indicates landmark , each quanitity has a priority


	quantity_space_inflow = [('0',[0],1),('+',[1,2,3,4],1)]
	influences_to_inflow = []
	influences_from_inflow = [('+',1,1)]
	propotionalities_from_inflow = []
	propotionalities_to_inflow = []
	value_correspondeces_from_inflow = []
	value_correspondences_to_inflow = []
	inflow_is_exogenous = True

	quantity_space_volume = [('0',[0],1),('+',[1,2],1),('Max',[3],1)]
	influences_to_volume = [('+',0,1),('-',2,-1)]
	influences_from_volume = []
	propotionalities_from_volume = [('+',2,1)]
	propotionalities_to_volume = []
	value_correspondences_from_volume = [(0,2),(1,2),(2,2)]
	value_correspondences_to_volume = [(0,2),(1,2),(2,2)]
	volume_is_exogenous = False

	quantity_space_outflow = [('0',[0],1),('+',[1,2],1),('Max',[3],1)]
	influences_to_outflow = []
	influences_from_outflow = [('-',1,-1)]
	propotionalities_from_outflow = []
	propotionalities_to_outflow = []
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
	index_of_current_mag = -1
	for i in range(len(quantity_space)):

		if quantity_space[i][0] == current_mag:

			index_of_current_mag = i
			break

	index_of_next_mag = index_of_current_mag + 1

	if index_of_next_mag >= len(quantity_space):
		return -1
	return index_of_next_mag

def findPrevMag(quantity_index,current_mag,quantities_list):

	quantity_space = quantities_list[quantity_index].quantity_space
	index_of_current_mag = -1
	for i in range(len(quantity_space)):

		if quantity_space[i][0] == current_mag:

			index_of_current_mag = i
			break

	index_of_prev_mag = index_of_current_mag -1

	if index_of_prev_mag < 0:
		return -1

	return index_of_prev_mag

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
		idx_of_mag = -1
		quantity_space = quantities_list[index].quantity_space

		for idx_mag,mag in enumerate(quantity_space):

			if mag[0] == current_mag:

				idx_of_mag = idx_mag
				break 

		for vc in value_correspondeces_from_quantity:

			if vc[0] == idx_of_mag:

				if state.state_vals[vc[1]][0] != current_mag:

					flag = 0
					break

	return flag

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

