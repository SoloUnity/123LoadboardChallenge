//
//  NotificationData.swift
//  123Loadboard App
//
//  Created by Gordon on 2023-11-19.
//

import Foundation
struct NotificationData: Codable {
    var truckId: Int
    var loadId: Int?
    var type: String

    enum CodingKeys: String, CodingKey {
        case truckId = "truck_id"
        case loadId = "load_id"
        case type
    }
}
