//
//  LoadModel.swift
//  123Loadboard App
//
//  Created by Gordon on 2023-11-18.
//

import Foundation

class LoadModel: ObservableObject {
    
    @Published var loads = [
        Load(
            id: 101,
            type: "Load",
            timestamp: "2023-11-17T11:31:35.0481646-05:00",
            originLatitude: 39.531354,
            originLongitude: -87.440632,
            destinationLatitude: 37.639,
            destinationLongitude: -121.0052,
            equipmentType: "Van",
            price: 3150,
            mileage: 2166
        ),
        Load(
            id: 201,
            type: "Load",
            timestamp: "2023-11-17T11:55:11.2311956-05:00",
            originLatitude: 41.621465,
            originLongitude: -83.605482,
            destinationLatitude: 37.639,
            destinationLongitude: -121.0052,
            equipmentType: "Van",
            price: 3300,
            mileage: 2334
        ),
        Load(
            id: 201,
            type: "Load",
            timestamp: "2023-11-17T11:55:11.2311956-05:00",
            originLatitude: 41.621465,
            originLongitude: -83.605482,
            destinationLatitude: 37.639,
            destinationLongitude: -121.0052,
            equipmentType: "Van",
            price: 3300,
            mileage: 2334
        )
    ]


    
    init() {
    }

    
}
