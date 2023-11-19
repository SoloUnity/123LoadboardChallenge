//
//  TruckModel.swift
//  123Loadboard App
//
//  Created by Gordon on 2023-11-18.
//

import Foundation
import SwiftUI
import MapKit

class TruckModel: ObservableObject {

    @Published var latitude = 0.0
    @Published var longitude = 0.0

    init() {
        self.latitude = 41.425058
        self.longitude = -87.33366
    }
    
    func changeLatitude(point: Double) {
        self.latitude = point
    }
    
    func changeLongitude(point: Double) {
        self.longitude = point
    }

}
