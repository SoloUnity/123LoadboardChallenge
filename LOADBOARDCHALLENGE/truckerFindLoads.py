from gasModel import getProfitMinusGas
from googleDistanceMatrix import google_distance_matrix
import copy

def trucker_find_loads(KDTreeLong, KDTreeShort, truck_id, truck):
    if truck["next_trip_preference"] == "Short":
        working_KD_Tree = copy.deepcopy(KDTreeShort)
        short = True
    else:
        working_KD_Tree = copy.deepcopy(KDTreeLong)
        short = False
    
    def _helper():
        potential_loads = working_KD_Tree.find_k_closest_loads(truck["coords"])
        greatest_profit = 0
        load_candidate_id = None
        load_candidate = None
        info = None
        destination_ls = []
        for load in potential_loads:
            dest_coords = load["coords"]
            destination_ls.append(dest_coords)
        if len(destination_ls) != 0:
            google_distance_ls = google_distance_matrix(truck["coords"], destination_ls)
        for i,load in enumerate(potential_loads):
            miles_to_load = google_distance_ls[i]
            net_profit = getProfitMinusGas(float(miles_to_load[0]), float(load['load_details']['mileage']), load['load_details']['price'])
            if net_profit > greatest_profit:  
                greatest_profit = net_profit
                load_candidate_id = load["load_id"]
                load_candidate = load
                info = miles_to_load
        
        return (load_candidate_id, greatest_profit, load_candidate, info)
    
    load_candidate_id, greatest_profit, load_candidate, info = _helper()

    if not load_candidate_id == None:
        return (load_candidate_id, truck_id, greatest_profit)

    if short:
        working_KD_Tree = copy.deepcopy(KDTreeLong)
    else:
        working_KD_Tree = copy.deepcopy(KDTreeShort)
    load_candidate_id, greatest_profit, load_candidate, info = _helper()
    if not load_candidate_id == None:
        return (load_candidate_id, truck_id, greatest_profit)
    return(load_candidate_id, truck_id, "negative profit")
    
