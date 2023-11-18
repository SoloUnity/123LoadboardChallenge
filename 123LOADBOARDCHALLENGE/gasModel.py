GAS_PRICE = 1.38 # $ per mile
AVG_MILES_PER_GALLON = 7 # miles per gallon

def getProfitMinusGas(miles_to_load, miles_to_destination, load_price):
    total_miles = miles_to_load + miles_to_destination
    return load_price - total_miles * GAS_PRICE

    