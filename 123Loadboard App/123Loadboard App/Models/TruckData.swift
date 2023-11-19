//
//  TruckData.swift
//  123Loadboard App
//
//  Created by Gordon on 2023-11-19.
//

import Foundation
struct TruckData: Codable {
    var seq: Int
    var type: String
    var timestamp: String
    var truckId: Int
    var positionLatitude: Double
    var positionLongitude: Double
    var equipType: String
    var nextTripLengthPreference: String
}
