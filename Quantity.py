class Quantity:

	def __init__(self,name,quantity_space,is_exogenous,influences_to_quantity,influences_from_quantity,propotionalities_to_quantity,propotionalities_from_quantity,value_correspondences_list_from_quantity,value_correspondences_list_to_quantity):


		self.name = name
		self.derivative_space = ['+','0','-']
		self.quantity_space = quantity_space
		self.is_exogenous = is_exogenous


		self.influences_to_quantity = influences_to_quantity

		self.influences_from_quantity = influences_from_quantity

		self.propotionalities_to_quantity = propotionalities_to_quantity

		self.propotionalities_from_quantity = propotionalities_from_quantity

		self.value_correspondences_list_from_quantity = value_correspondences_list_from_quantity

		self.value_correspondences_list_to_quantity = value_correspondences_list_to_quantity

