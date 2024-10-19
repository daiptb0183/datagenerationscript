from utils import dis_calc

class Request(object):
    request_id = int
    request_uuid = None
    location = None
    request_period = int
    possible_parts = list
    possible_parts_probability = dict
    completed = bool
    completed_period = int
    parts_defined = bool
    defined_parts = list
    total_waiting_period = int
    angle_with_depot = float
    parts_revealed_period = int
    request_score = float
    satisfied_part = list
    zone = None
    neighouring_zones = list

    def __init__(self, request_id, request_uuid, location, request_period,
                 possible_parts, possible_parts_probability, zone):
        self.request_id = request_id
        self.request_uuid = request_uuid
        self.location = location
        self.request_period = request_period
        self.possible_parts = possible_parts
        self.possible_parts_probability = possible_parts_probability
        self.completed = False
        self.completed_period = None
        self.parts_defined = False
        self.defined_parts = None
        self.total_waiting_period = 0
        self.satisfied_part = []
        self.zone = zone
        self.parts_revealed_period = 10000
        self.visited = False
        self.completed_on_first_visit = False

    def __repr__(self):
        return "Request ID " + str(self.request_id)

    def set_request_score(self, instance, period, score_multiplier_factor=1):
        self.request_score = self.calculate_additional_waiting_cost(
            instance, period, 1, score_multiplier_factor)

    def randomize_part(self, random_generator):
        assert not self.parts_defined, "Part Already Drawn Before"
        drawn_part = []
        for index, part in enumerate(self.possible_parts):
            selected = random_generator.binomial(
                1, self.possible_parts_probability[index])
            if selected == 1:
                drawn_part.append(part)
        self.randomized_part = drawn_part

    def set_parts(self, period):
        self.parts_defined = True
        self.defined_parts = self.randomized_part
        self.parts_revealed_period = period

    def draw_random_parts(self, period, random_generator):
        self.randomize_part(random_generator)
        self.parts_defined = True
        self.defined_parts = self.randomized_part
        self.parts_revealed_period = period

    def set_total_waiting_period(self):
        self.total_waiting_period = self.completed_period - self.request_period

    def calculate_additional_waiting_cost(self, instance, period, periods_ahead, \
        score_multiplier_factor=1):
        number_of_waiting_period = period - self.request_period

        if number_of_waiting_period > 0:
            old_cost = \
                (((number_of_waiting_period) *
                    (number_of_waiting_period+periods_ahead))/2) * \
                instance.parameters.lineEditPenaltyFactor
        else:
            old_cost = 0

        new_cost = (((number_of_waiting_period+periods_ahead)
                     * (number_of_waiting_period+periods_ahead+1))/2) * \
            instance.parameters.lineEditPenaltyFactor
        return score_multiplier_factor*(new_cost - old_cost)


class Vehicle(object):

    vehicle_id = int
    starting_location = None
    periods_visited_schedule = list  # of dict
    periods_visited_schedule_status = list  # of dict
    periods_revealed_carry_parts_list = list  # of dict
    periods_unrevealed_carry_parts_list = list  # of dict
    period_unable_to_visit = list
    periods_initial_parts_list = list

    def __init__(self, vehicle_id, starting_location, periods_visited_schedule,
                 periods_visited_schedule_status, periods_revealed_carry_parts_list,
                 periods_unrevealed_carry_parts_list,
                 period_unable_to_visit, periods_initial_parts_list):
        self.vehicle_id = vehicle_id
        self.starting_location = starting_location
        self.periods_visited_schedule = periods_visited_schedule
        self.periods_visited_schedule_status = periods_visited_schedule_status
        self.periods_revealed_carry_parts_list = periods_revealed_carry_parts_list
        self.periods_unrevealed_carry_parts_list = periods_unrevealed_carry_parts_list
        self.period_unable_to_visit = period_unable_to_visit
        self.periods_initial_parts_list = periods_initial_parts_list
        self.centroids_list = []

    def __repr__(self):
        return self.vehicle_id

    def possible_to_add_request(self, instance, request, visiting_period):
        try:
            self.periods_visited_schedule[visiting_period]
        except IndexError:
            current_missing_periods = visiting_period+1 - \
                len(self.periods_visited_schedule)
            for i in range(current_missing_periods):
                self.periods_visited_schedule.append([])

        new_schedule = \
            self.periods_visited_schedule[visiting_period] + [request]

        if self.calculate_schedule_duration(instance, new_schedule) <= instance.parameters.lineEditMaxWorkingDuration:
            return True
        else:
            return False

    def calculate_schedule_duration(self, instance, schedule):
        total_duration = 0
        first_trip_duration = dis_calc.compute_travel_time(instance,
                                                           self.starting_location, schedule[0].location)
        last_trip_duration = dis_calc.compute_travel_time(instance,
                                                          self.starting_location, schedule[-1].location)
        total_duration += first_trip_duration
        total_duration += last_trip_duration

        if len(schedule) >= 2:
            for index, request in enumerate(schedule):
                if index == len(schedule) - 1:
                    continue
                else:
                    travel_time = \
                        dis_calc.compute_travel_time(instance, schedule[index].location,
                                                     schedule[index+1].location)
                    total_duration += travel_time

        total_duration += len(schedule)*instance.parameters.lineEditServiceTime
        return total_duration

    def schedule_feasibility_check(self, schedule):
        if self.calculate_schedule_duration(schedule) <= instance.parameters.lineEditMaxWorkingDuration:
            return True
        else:
            return False

    def calculate_schedule_distance(self, schedule):
        if not schedule:
            return 0
        total_distance = 0
        first_trip_distance = dis_calc.compute_airdist(
            self.starting_location, schedule[0].location)
        last_trip_distance = dis_calc.compute_airdist(
            self.starting_location, schedule[-1].location)
        total_distance += first_trip_distance
        total_distance += last_trip_distance

        if len(schedule) >= 2:
            for index, request in enumerate(schedule):
                if index == len(schedule) - 1:
                    continue
                else:
                    travel_distance = \
                        dis_calc.compute_airdist(schedule[index].location,
                                                 schedule[index+1].location)
                    total_distance += travel_distance

        return total_distance

    def add_revealed_request(self, request, visiting_period):
        try:
            self.periods_visited_schedule_status[visiting_period]
        except IndexError:
            current_missing_periods = visiting_period+1 - \
                len(self.periods_visited_schedule_status)
            for i in range(current_missing_periods):
                self.periods_visited_schedule_status.append([])

        try:
            self.periods_visited_schedule[visiting_period]
        except IndexError:
            current_missing_periods = visiting_period+1 - \
                len(self.periods_visited_schedule)
            for i in range(current_missing_periods):
                self.periods_visited_schedule.append([])

        try:
            self.periods_revealed_carry_parts_list[visiting_period]
        except IndexError:
            current_missing_periods = visiting_period+1 - \
                len(self.periods_revealed_carry_parts_list)
            for i in range(current_missing_periods):
                self.periods_revealed_carry_parts_list.insert(0, [])

        for part in request.defined_parts:
            if part not in request.satisfied_part:
                self.periods_revealed_carry_parts_list[visiting_period][part] -= 1

        status = 'Success'
        self.periods_visited_schedule[visiting_period].append(request)
        self.periods_visited_schedule_status[visiting_period].append(
            status)
        return status

    def add_unreveal_request(self, request, visiting_period):
        try:
            self.periods_visited_schedule_status[visiting_period]
        except IndexError:
            current_missing_periods = visiting_period+1 - \
                len(self.periods_visited_schedule_status)
            for i in range(current_missing_periods):
                self.periods_visited_schedule_status.append([])

        try:
            self.periods_visited_schedule[visiting_period]
        except IndexError:
            current_missing_periods = visiting_period+1 - \
                len(self.periods_visited_schedule)
            for i in range(current_missing_periods):
                self.periods_visited_schedule.append([])

        try:
            self.periods_unrevealed_carry_parts_list[visiting_period]
        except IndexError:
            current_missing_periods = visiting_period+1 - \
                len(self.periods_unrevealed_carry_parts_list)
            for i in range(current_missing_periods):
                self.periods_unrevealed_carry_parts_list.insert(0, [])

        if request.defined_parts == []:
            status = 'Success'
            self.periods_visited_schedule_status[visiting_period].append(
                status)

        elif all([self.periods_unrevealed_carry_parts_list[visiting_period][part] >
                  0 for part in request.defined_parts]):
            status = 'Success'
            for part in request.defined_parts:
                self.periods_unrevealed_carry_parts_list[visiting_period][part] -= 1
            self.periods_visited_schedule_status[visiting_period].append(
                status)
        else:
            status = 'Failed'
            for part in request.defined_parts:
                if self.periods_unrevealed_carry_parts_list[visiting_period][part] > 0:
                    self.periods_unrevealed_carry_parts_list[visiting_period][part] -= 1
                    request.satisfied_part.append(part)
            self.periods_visited_schedule_status[visiting_period].append(
                status)

        self.periods_visited_schedule[visiting_period].append(request)
        return status

    def number_of_active_period(self):
        return len(self.periods_visited_schedule)

    def sufficient_stock_for_request(self, request, period):
        try:
            self.periods_revealed_carry_parts_list[period]
        except IndexError:
            current_missing_periods = period+1 - \
                len(self.periods_revealed_carry_parts_list)
            for i in range(current_missing_periods):
                self.periods_revealed_carry_parts_list.insert(0, [])

        if not request.parts_defined:
            return True
        elif all([self.periods_revealed_carry_parts_list[period][part] >
                  0 for part in request.defined_parts
                  if part not in request.satisfied_part]):
            return True
        else:
            return False


class Location(object):

    lat = 0.0
    lon = 0.0

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        assert self.validate()

    def __repr__(self):
        return "lat " + str(self.lat) + " " + "lon " + str(self.lon)

    def validate(self):
        if not self.lat >= - 90.0 and self.lat <= 90.0:
            return False
        if not self.lon >= - 180.0 and self.lon <= 180.0:
            return False
        return True


class ParametersReader(object):
    def __init__(self, spinBoxSeed, spinBoxMultiInstanceSeedStart, spinBoxMultiInstanceIndicator,
                 spinBoxMultiInstanceSeedEnd, lineEditDepotLat, lineEditDepotLon,
                 lineEditNumberOfPeriod, lineEditServiceArea,
                 lineEditMaxWorkingDuration, lineEditServiceTime,
                 lineEditTravelSpeed, lineEditTravelCost,
                 lineEditPenaltyFactor, lineEditNumberOfRequests,
                 lineEditNumberOfPartType, lineEditMatrixSize,
                 lineEditPartProbabilityLow, lineEditPartProbabilityHigh,
                 lineEditItemHoldingCostLow,
                 lineEditItemHoldingCostHigh, radioButtonMyopic,radioButtonSimheuristic,
                 radioButtonMIP, horizontalSliderZoneDivergingLevel,
                 comboBoxZoneStyle,
                 spinBoxLookAheadPeriods,
                 spinBoxBaseSimulationIterations,
                 lineEditShallowConfidenceLevel,
                 lineEditDeepConfidenceLevel,
                 lineEditMaxCIWidth,
                 spinSolutionPoolSize,
                 spinEliteSolutionPoolSize,
                 spinGeneticIterations):
        self.spinBoxSeed = spinBoxSeed
        self.spinBoxMultiInstanceSeedStart = spinBoxMultiInstanceSeedStart
        self.spinBoxMultiInstanceIndicator = spinBoxMultiInstanceIndicator
        self.spinBoxMultiInstanceSeedEnd = spinBoxMultiInstanceSeedEnd
        self.lineEditDepotLat = lineEditDepotLat
        self.lineEditDepotLon = lineEditDepotLon
        self.lineEditNumberOfPeriod = lineEditNumberOfPeriod
        self.lineEditServiceArea = lineEditServiceArea
        self.lineEditMaxWorkingDuration = lineEditMaxWorkingDuration
        self.lineEditServiceTime = lineEditServiceTime
        self.lineEditTravelSpeed = lineEditTravelSpeed
        self.lineEditTravelCost = lineEditTravelCost
        self.lineEditPenaltyFactor = lineEditPenaltyFactor
        self.lineEditNumberOfRequests = lineEditNumberOfRequests
        self.lineEditNumberOfPartType = lineEditNumberOfPartType
        self.lineEditMatrixSize = lineEditMatrixSize
        self.lineEditPartProbabilityLow = lineEditPartProbabilityLow
        self.lineEditPartProbabilityHigh = lineEditPartProbabilityHigh
        self.lineEditItemHoldingCostLow = lineEditItemHoldingCostLow
        self.lineEditItemHoldingCostHigh = lineEditItemHoldingCostHigh
        self.radioButtonMyopic = radioButtonMyopic
        self.radioButtonSimheuristic = radioButtonSimheuristic
        self.radioButtonMIP = radioButtonMIP
        self.horizontalSliderZoneDivergingLevel = horizontalSliderZoneDivergingLevel
        self.comboBoxZoneStyle = comboBoxZoneStyle
        self.spinBoxLookAheadPeriods = spinBoxLookAheadPeriods
        self.spinBoxBaseSimulationIterations = spinBoxBaseSimulationIterations
        self.lineEditShallowConfidenceLevel = lineEditShallowConfidenceLevel
        self.lineEditDeepConfidenceLevel = lineEditDeepConfidenceLevel
        self.lineEditMaxCIWidth = lineEditMaxCIWidth
        self.spinSolutionPoolSize = spinSolutionPoolSize
        self.spinEliteSolutionPoolSize = spinEliteSolutionPoolSize
        self.spinGeneticIterations = spinGeneticIterations
