//
//  LocationRequestView.swift
//  MapKitTest
//
//  Created by Gordon on 2023-11-18.
//

import SwiftUI
import MapKit

struct LocationRequestView: View {
    
    @EnvironmentObject private var locationModel : LocationManager
    
    var body: some View {
        Button {
            locationModel.requestLocation()
        } label: {
            Text("Request Location")
        }

    }
}

#Preview {
    LocationRequestView()
}
