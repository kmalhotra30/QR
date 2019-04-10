def generate_intra_state_trace(state_tuple,quantities_list):

	trace = ""
	if state_tuple[1][1] == '+':

		trace += "There is more water flowing in than flowing out, which causes the volume and outflow to increase!"
	elif state_tuple[1][1] == '0':

		trace += "The amount of water flowing in is equal to the amount of water flowing out, which causes the volume and outflow to stay steady!"

	else:

		trace += "The amount of water flowing out is more than the amount of water flowing in, which causes the volume and outflow to decrease"

	return trace