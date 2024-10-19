class Instance(object):
    solutions = list
    requests = list
    current_period = int
    final_solution = None

    def __init__(self, requests, solutions, current_period, final_solution,
                 possible_parts, possible_parts_probability, items_holding_cost_dict,
                 parameters):
        self.requests = requests
        self.solutions = solutions
        self.current_period = current_period
        self.final_solution = final_solution
        self.possible_parts = possible_parts
        self.possible_parts_probability = possible_parts_probability
        self.items_holding_cost_dict = items_holding_cost_dict
        self.parameters = parameters

    def calculate_average_waiting_duration(self):
        total_waited_duration = 0
        for request in self.requests:
            if request.completed_period <= self.parameters.lineEditNumberOfPeriod - 1:
                total_waited_duration += request.completed_period - request.request_period
        number_of_completed_request_before_last_period = \
            len([request for request in self.requests if request.completed_period <=
                self.parameters.lineEditNumberOfPeriod - 1])
        return total_waited_duration/number_of_completed_request_before_last_period

    def calculate_average_duration_until_first_visit(self):
        total_waited_duration = 0
        for request in self.requests:
            if request.visited:
                if request.first_visit_period <= self.parameters.lineEditNumberOfPeriod - 1:
                    total_waited_duration += request.first_visit_period - request.request_period
        visited_requests = [
            request for request in self.requests if request.visited]
        number_of_visited_request_before_last_period = \
            len([request for request in visited_requests if request.first_visit_period <=
                self.parameters.lineEditNumberOfPeriod - 1])
        return total_waited_duration/number_of_visited_request_before_last_period

    def calculate_job_fill_rate_on_first_visit(self):
        total_number_of_visited_requests = \
            len([request for request in self.requests if request.visited and request.first_visit_period <=
                self.parameters.lineEditNumberOfPeriod - 1])
        total_number_success_first_visit = \
            len([request for request in self.requests if request.visited and request.completed_on_first_visit and request.first_visit_period <=
                self.parameters.lineEditNumberOfPeriod - 1])
        if total_number_of_visited_requests == 0:
            return 0
        else:
            return (total_number_success_first_visit/total_number_of_visited_requests)

    def calculate_probability_visited_immedimately(self):
        total_number_of_visited_requests = \
            len([request for request in self.requests if request.visited and request.first_visit_period <=
                self.parameters.lineEditNumberOfPeriod - 1])
        total_number_of_immediate_visits = \
            len([request for request in self.requests if request.visited and (
                request.first_visit_period - request.request_period) < 1
                and request.first_visit_period <=
                self.parameters.lineEditNumberOfPeriod - 1])

        if total_number_of_visited_requests == 0:
            return 0
        else:
            return total_number_of_immediate_visits/total_number_of_visited_requests
