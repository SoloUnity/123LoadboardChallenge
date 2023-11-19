//
//  ContentView.swift
//  MapKitTest
//
//  Created by Gordon on 2023-11-18.
//

import SwiftUI
import MapKit

struct MapView: View {
    
    @EnvironmentObject var truckModel : TruckModel
    @State var cameraPosition : MapCameraPosition = .region(.userRegion)
    @State private var searchText = ""
    @State private var results = [MKMapItem]()
    @State var mapSelection: MKMapItem?
    @State private var showDetails = true
    @State private var getDirections = false
    @State var routeDisplaying = false
    @State var route1: MKRoute?
    @State var route2: MKRoute?
    @State var routeDestination1: MKMapItem?
    @State var routeDestination2: MKMapItem?
    @State private var enlarged = false
    @State var originLocation : CLLocationCoordinate2D?
    @State var destinationLocation : CLLocationCoordinate2D?

    var body: some View {
        
        Map(position: $cameraPosition, selection: $mapSelection) {
//            Marker ("My location", systemImage: "truck.box.fill", coordinate: .userLocation)
//                .tint(.green)
            
//            UserAnnotation() {
//                ZStack {
//                    Circle()
//                        .frame(width: 32, height: 32)
//                        .foregroundColor(.blue.opacity(0.25))
//
//                    Circle()
//                        .frame(width: 20, height: 20)
//                        .foregroundColor(.white)
//
//                    Circle()
//                        .frame(width: 12, height: 12)
//                        .foregroundColor(.blue)
//                }
//            }
            
            Annotation("My Location", coordinate: getLocation(truckModel: truckModel)) {
                ZStack {
                    Circle()
                        .frame(width: 32, height: 32)
                        .foregroundColor(.blue.opacity(0.25))

                    Circle()
                        .frame(width: 20, height: 20)
                        .foregroundColor(.white)

                    Circle()
                        .frame(width: 12, height: 12)
                        .foregroundColor(.blue)
                }

            }
            
            if let originLocation, let destinationLocation, routeDisplaying {
                Marker ("Pickup", systemImage: "shippingbox.fill", coordinate: originLocation)
                    .tint(Constants.Colours.loadboardGreen)
                
                Marker ("Delivery", systemImage: "mappin", coordinate: destinationLocation)
                    .tint(.purple)
            }
            
            
//            ForEach(results, id: \.self) { item in
//                if routeDisplaying {
//                    if item == routeDestination {
//                        let placemark = item.placemark
//                        Marker(placemark.name ?? "", coordinate: placemark.coordinate)
//                    }
//                }
//                else {
//                    let placemark = item.placemark
//                    Marker(placemark.name ?? "", coordinate: placemark.coordinate)
//                }
//                
//            }
            
            if let route1, let route2 {
                MapPolyline(combinedPolyline(from: route1, and: route2))
                    .stroke(.green, lineWidth: 6)
            }
        }
//        .overlay(alignment: .top) {
//            
//            VStack {
//                Button {
//                    
//                    truckModel.changeLatitude(point: 39.195726)
//                    truckModel.changeLongitude(point: -84.665296)
//                } label: {
//                    
//                    Text("Change Location")
//
//                }
//                
//                Button {
//                    
//                    truckModel.changeLatitude(point: 41.425058)
//                    truckModel.changeLongitude(point: -87.33366)
//                } label: {
//                    
//                    Text("Change Location")
//
//                }
//            }
//            
//
//        }
        .onAppear {
            self.cameraPosition = .region(getRegion(truckModel: truckModel))
        }
        .onChange(of: truckModel.latitude, { _, _ in
            self.cameraPosition = .region(getRegion(truckModel: truckModel))
        })
        .onChange(of: truckModel.longitude, { _, _ in
            self.cameraPosition = .region(getRegion(truckModel: truckModel))
        })
        .overlay(alignment: .topLeading) {
            accountButton
                .padding([.leading], 5)
        }
        .onChange(of: showDetails, { oldValue, newValue in
            if !newValue {
                
                showDetails = true

            }
        })
//        .onChange(of: getDirections, { oldValue, newValue in
//            if newValue {
//                fetchRoute()
//            }
//        })
//        .onChange(of: mapSelection) { oldValue, newValue in
//            showDetails = newValue != nil
//        }
        .sheet(isPresented: $showDetails, content: {
//            LocationDetailsView(mapSelection: $mapSelection, show: $showDetails, getDirections: $getDirections)

            
            LoadListView(route1: $route1, route2: $route2, routeDestination1: $routeDestination1, routeDestination2: $routeDestination2, routeDisplaying: $routeDisplaying, cameraPosition: $cameraPosition, originLocation: $originLocation, destinationLocation: $destinationLocation, showDetails: $showDetails)
                .presentationDetents([.fraction(0.60), .fraction(0.25), .large])
                .presentationBackgroundInteraction(.enabled)
                .presentationCornerRadius(12)
                .presentationDragIndicator(.visible)
             
            
        })
        .mapControls {
            MapCompass()
            MapPitchToggle()
        }
    }
    
    var accountButton : some View {
        Image(systemName: "person.circle")
            .resizable()
            .scaledToFit()
            .frame(width: 35, height: 35)
            .foregroundColor(Constants.Colours.loadboardGreen)
            .padding(7)
            .background(.ultraThickMaterial)
            .clipShape(Circle())
    }
}

//extension MapView {
//    
//    func fetchRoute() {
//        if let mapSelection {
//            let request = MKDirections.Request()
//            request.source = MKMapItem(placemark: MKPlacemark(coordinate: .userLocation))
//            request.destination = mapSelection
//
//            Task {
//                let result = try? await MKDirections(request: request).calculate()
//                route = result?.routes.first
//                routeDestination = mapSelection
//
//                withAnimation(.snappy) {
//                    routeDisplaying = true
//                    showDetails = false
//
//                    if let rect = route?.polyline.boundingMapRect, routeDisplaying {
//                        cameraPosition = .rect(rect)
//                    }
//                }
//            }
//        }
//    }
//}

func getLocation(truckModel : TruckModel) -> CLLocationCoordinate2D {
    return CLLocationCoordinate2D(latitude: truckModel.latitude, longitude: truckModel.longitude)
}

func getRegion(truckModel : TruckModel) -> MKCoordinateRegion {
    
    let userLocation = getLocation(truckModel: truckModel)
    let userRegion = MKCoordinateRegion(center: userLocation,
                                        latitudinalMeters: 100000,
                                        longitudinalMeters: 100000)
    return userRegion
}

func combinedPolyline(from route1: MKRoute, and route2: MKRoute) -> MKPolyline {
    let points1 = route1.polyline.points()
    let points2 = route2.polyline.points()
    let combinedPoints = Array(UnsafeBufferPointer(start: points1, count: route1.polyline.pointCount)) + Array(UnsafeBufferPointer(start: points2, count: route2.polyline.pointCount))
    return MKPolyline(points: combinedPoints, count: combinedPoints.count)
}

extension CLLocationCoordinate2D {
    static var userLocation: CLLocationCoordinate2D {
        return .init(latitude: 41.425058, longitude: -87.33366)
    }
}

extension MKCoordinateRegion {
    static var userRegion: MKCoordinateRegion {
        return .init(center: .userLocation,
                     latitudinalMeters: 100000,
                     longitudinalMeters: 100000)
    }
}

#Preview {
    MapView()
}
