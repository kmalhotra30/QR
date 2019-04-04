from itertools import product
def remove_invalid_states(states,N):

	updated_states = []
	for state in states:

		#1. Remove states with ('Max','+') or ('0','-')

		flag = 0
		for j in range(N):

			quanitity = state[j]
			if quanitity[0] == 'Max' and quanitity[1] == '+' or quanitity[0] == '0' and quanitity[1] == '-':
				flag = 1
				break
		#2. If volume is 'Max' , then outflow should be 'Max' else remove the state.

		if state[1][0] != state[2][0]:
			flag = 1

		if state[1][1] != state[2][1]:
			flag = 1 	
		
		if state[0][0] == '+' and state[2][0] == '0' and state[1][1] !='+':
			flag = 1


		if state[0][0] == '0' and state[2][0] == '+' and state[1][1] != '-':
			flag = 1

		if state[0][0] == '0' and state[2][0] == 'Max' and state[1][1] != '-':
			flag = 1

		


		if flag == 0:
			updated_states.append(state)

	return updated_states

quantities = ['Inflow','Volume','Outflow'] # Defined quantities just for tracking.
N = len(quantities)
quantities_magnitude = [['+','-'],['Max','+','-'],['Max','+','-']] # Magnitude space for each quanitity
quantities_derivative = [['+','0','-']] * N # Derivative space for each quanitity

# Store and compute cross product between magnitude and derivative space of each quantity.
quanitity_mag_der_cross_product = [list(product(quantities_magnitude[i],quantities_derivative[i])) for i in range(N)]

# Compute cross product between the elements of quanitity_mag_der_cross_product to get all possible states
states = list(product(*quanitity_mag_der_cross_product)) # Total = 486 ( 2* 3 * 3 * 3 * 3 * 3)
# States is a list , each element of the list is a tuple , each tuple consists of N tuples of 2 elements , the first element is the current magnitude and second is the current derivative.
print(len(remove_invalid_states(states,N)))