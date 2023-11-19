////
////  LocationManager.swift
////  MapKitTest
////
////  Created by Gordon on 2023-11-18.
////

import Foundation
import MapKit
import CoreLocation

class LocationManager: NSObject, ObservableObject {
    private let manager = CLLocationManager()
    @Published var userLocation: CLLocation?
    @Published var authorizationState = CLAuthorizationStatus.notDetermined
    static let shared = LocationManager()
    
    override init() {
        super.init()
        manager.delegate = self
        manager.desiredAccuracy = kCLLocationAccuracyBest
        manager.startUpdatingLocation()
    }
    
    func requestLocation() {
        manager.requestWhenInUseAuthorization()
    }
        
    func getAddressFromLatLon(lat: Double, lon: Double) async -> String {
        let geocoder = CLGeocoder()
        let location = CLLocation(latitude: lat, longitude: lon)
        
        do {
            let placemarks = try await geocoder.reverseGeocodeLocation(location)
            if let placemark = placemarks.first {
                let address = [
                    placemark.thoroughfare,
                    placemark.subThoroughfare,
                    placemark.locality,
                    placemark.administrativeArea,
                    placemark.postalCode,
                    placemark.country
                ].compactMap { $0 }.joined(separator: ", ")
                
                return address
            } else {
                return "Address not found"
            }
        } catch {
            print("Error in reverseGeocode: \(error)")
            return "Error retrieving address"
        }
    }
    
    func calculateTotalDistanceInMiles(coordinates: [(latitude: Double, longitude: Double)]) -> Double {
        guard coordinates.count == 3 else {
            fatalError("Exactly three pairs of coordinates are required")
        }

        let locations = coordinates.map { CLLocation(latitude: $0.latitude, longitude: $0.longitude) }

        let distance1to2 = locations[0].distance(from: locations[1]) / 1609.344 // Converting meters to miles
        let distance2to3 = locations[1].distance(from: locations[2]) / 1609.344

        return distance1to2 + distance2to3
    }
}

extension LocationManager: CLLocationManagerDelegate {
    
    func locationManager(_ manager: CLLocationManager, didChangeAuthorization status: CLAuthorizationStatus) {
        switch status {
            
        case .notDetermined:
            self.authorizationState = .notDetermined

            print("DEBUG: Not determined")
        case .restricted:
            self.authorizationState = .restricted

            print("DEBUG: Restricted")
        case .denied:
            self.authorizationState = .denied

            print("DEBUG: Denied")
        case .authorizedAlways:
            self.authorizationState = .authorizedAlways

            print("DEBUG: Auth always")
        case .authorizedWhenInUse:
            self.authorizationState = .authorizedWhenInUse
            print("DEBUG: Auth when in use")
        @unknown default:
            break
        }
    }
    
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        guard let location = locations.last else {return}
        self.userLocation = location
    }
}
