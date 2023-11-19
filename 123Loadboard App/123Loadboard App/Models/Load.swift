//
//  Load.swift
//  123Loadboard App
//
//  Created by Gordon on 2023-11-18.
//

import Foundation

class Load: Codable, Identifiable, ObservableObject {
    let id: Int
    let type, timestamp: String
    let originLatitude, originLongitude, destinationLatitude, destinationLongitude: Double
    let equipmentType: String
    let price, mileage: Int

    init(id: Int, type: String, timestamp: String, originLatitude: Double, originLongitude: Double, destinationLatitude: Double, destinationLongitude: Double, equipmentType: String, price: Int, mileage: Int) {
        self.id = id
        self.type = type
        self.timestamp = timestamp
        self.originLatitude = originLatitude
        self.originLongitude = originLongitude
        self.destinationLatitude = destinationLatitude
        self.destinationLongitude = destinationLongitude
        self.equipmentType = equipmentType
        self.price = price
        self.mileage = mileage
    }

    enum CodingKeys: String, CodingKey {
        case id = "loadId"
        case type, timestamp
        case originLatitude, originLongitude, destinationLatitude, destinationLongitude, equipmentType, price, mileage
    }
}
