import random

prng = None

# Vehicle config
depot_location = [49.1466811, 9.217546]
customer_request_radius = 10
max_working_time = 6
service_time = 0.5
travel_speed = 50
travel_cost_per_km = 2
additional_penalty_incresement_per_day = 5
item_holding_cost = 0.5


# Other configuration
large_constant = 10000000
earth_radius = 6371.0000785


# Simulation configuration
number_of_part_estimation_iter = 100
number_of_shallow_simulations = 100
number_of_deep_simulations = 1000
number_of_neighborhood_iterations = 0
number_of_elite_solutions = 10

# Distribution configuration
number_of_request_per_period = [6, 10]
zone_probability_low = 0
zone_probability_high = 0.15
average_number_of_customer_per_period = 8
number_of_part_type = 10
part_probability_low = 0.01
part_probability_hight = 0.15
item_holding_cost_low = 0.1
item_holding_cost_high = 1
number_of_period = 20

maxtrix_size = 7
zone_diverging_level = 1
zone_style = 'Center'


possible_colors = ['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightgrey',
                   'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'rebeccapurple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen']

possible_parts = random.sample(possible_colors, k=number_of_part_type)

items_holding_cost_dict = {key: 0.5 for key in possible_parts}

possible_parts_probability = [
    random.uniform(part_probability_low,
                   part_probability_hight) for i in possible_parts]

op_deviation = -10

max_two_opt_recursive_depth = 20

I_loops = 20
K_loops = 10

number_of_look_ahead_periods = 2
number_of_simulations = 3

simheuristic = True

solutions_pool_size = 5
