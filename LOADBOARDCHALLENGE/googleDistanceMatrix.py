import googlemaps
gmaps = googlemaps.Client(key='AIzaSyD9tAFBsLY-TJV21XT2O9UtxxSOTYFqYSw')

def google_distance_matrix(origin, destinations):
    try:
        google_distance = []
        matrix = gmaps.distance_matrix(origin, destinations, mode='driving', units='imperial')

        for row in matrix['rows']:
            for element in row['elements']:
                distance = element['distance']['value']
                duration = element['duration']['value']
                #print(f'Distance: {distance}, Duration: {duration}')

                google_distance.append((distance * 0.6213712 / 1000, duration)) #convert to miles and append
        return google_distance
    except Exception as e:
        print(f'Error: {e}') 
