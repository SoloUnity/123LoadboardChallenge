from gasModel import getProfitMinusGas
import copy

def trucker_find_loads(KDTree, truck_id, truck):
    working_KD_Tree = copy.deepcopy(KDTree)
    potential_loads = working_KD_Tree.find_k_closest_loads(truck["coords"])
    greatest_profit = 0
    load_candidate = None
    for load in potential_loads:
        miles_to_load = load['distance'] #distance_matrix_api()
        trip_length = _classifier(float(load['load_details']['mileage']))
        net_profit = getProfitMinusGas(float(miles_to_load), float(load['load_details']['mileage']), load['load_details']['price'])
        if net_profit > greatest_profit:  #add positive
            greatest_profit = net_profit
            load_candidate = load["load_id"]
        
    
    if not load_candidate == None:
        return (load_candidate, truck_id, greatest_profit)
    else:
        return(load_candidate, truck_id, "negative profit")
    

def _classifier(distance):
    if distance <  200:
        return 'Short'
    return 'Long'