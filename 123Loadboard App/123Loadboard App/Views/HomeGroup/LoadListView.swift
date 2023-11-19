//
//  LoadListView.swift
//  123Loadboard App
//
//  Created by Gordon on 2023-11-18.
//

import SwiftUI
import MapKit

struct LoadListView: View {
    
    @EnvironmentObject var loadModel : LoadModel
    @EnvironmentObject var truckModel : TruckModel
    @EnvironmentObject var locationManager : LocationManager
    @Binding var route1: MKRoute?
    @Binding var route2: MKRoute?
    @Binding var routeDestination1: MKMapItem?
    @Binding var routeDestination2: MKMapItem?
    @Binding var routeDisplaying : Bool
    @Binding var cameraPosition : MapCameraPosition
    @Binding var originLocation : CLLocationCoordinate2D?
    @Binding var destinationLocation : CLLocationCoordinate2D?
    @Binding var showDetails : Bool
    @State private var isLoading = false
    
    
    var body: some View {
        ScrollView(showsIndicators: false) {
            VStack {
                ForEach(loadModel.filteredLoads) { load in
                    LoadView(load: load, isLoading: $isLoading)
                        .onTapGesture {
                            self.isLoading = true  // Start loading
                            self.originLocation = CLLocationCoordinate2D(latitude: load.originLatitude, longitude: load.originLongitude)
                            self.destinationLocation = CLLocationCoordinate2D(latitude: load.destinationLatitude, longitude: load.destinationLongitude)
                            fetchRoute(truckModel: truckModel, load: load)
                        }

                }
            }
        }
        .padding(.top)
    }
    
}

extension LoadListView {
    
    func fetchRoute(truckModel: TruckModel, load: Load) {
        let request1 = MKDirections.Request()
        request1.source = MKMapItem(placemark: MKPlacemark(coordinate: getLocation(truckModel: truckModel)))
        request1.destination = MKMapItem(placemark: MKPlacemark(coordinate: CLLocationCoordinate2D(latitude: load.originLatitude, longitude: load.originLongitude)))
        
        let request2 = MKDirections.Request()
        request2.source = MKMapItem(placemark: MKPlacemark(coordinate: CLLocationCoordinate2D(latitude: load.originLatitude, longitude: load.originLongitude)))
        request2.destination = MKMapItem(placemark: MKPlacemark(coordinate: CLLocationCoordinate2D(latitude: load.destinationLatitude, longitude: load.destinationLongitude)))
        
        Task {
            let result1 = try? await MKDirections(request: request1).calculate()
            let result2 = try? await MKDirections(request: request2).calculate()
            route1 = result1?.routes.first
            route2 = result2?.routes.first
            routeDestination1 = MKMapItem(placemark: MKPlacemark(coordinate: CLLocationCoordinate2D(latitude: load.originLatitude, longitude: load.originLongitude)))
            routeDestination2 = MKMapItem(placemark: MKPlacemark(coordinate: CLLocationCoordinate2D(latitude: load.destinationLatitude, longitude: load.destinationLongitude)))
            
            
            withAnimation(.snappy) {
                routeDisplaying = true
                
                if let rect1 = route1?.polyline.boundingMapRect,
                   let rect2 = route2?.polyline.boundingMapRect {
                    
                    // Combine the rects and zoom out
                    let combinedRect = rect1.union(rect2)
                    let zoomedOutRect = combinedRect.insetBy(dx: -combinedRect.size.width * 0.1, dy: -combinedRect.size.height * 0.1) // Zoom out by 10%
                    
                    cameraPosition = .rect(zoomedOutRect)
                }
            }
            
            DispatchQueue.main.async {
                self.isLoading = false  // Stop loading
            }
        }
    }
}

