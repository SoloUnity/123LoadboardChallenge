//
//  LoadView.swift
//  123Loadboard App
//
//  Created by Gordon on 2023-11-18.
//

import SwiftUI

struct LoadView: View {
    
    @ObservedObject var load : Load
    @EnvironmentObject var locationManager : LocationManager
    @EnvironmentObject var truckModel : TruckModel
    @State var originAddress = ""
    @State var destinationAddress = ""
    @State var finalDistance = ""
    @Binding var isLoading : Bool

    var body: some View {
        
        HStack() {
            
            VStack (alignment: .center) {
                Image("box")
                    .resizable()
                    .scaledToFit()
                    .frame(width: 80, height: 80)
                    .padding(.leading)
                
                Text("\(self.finalDistance) miles")
                    .font(.footnote)
            }
            
            
            
            VStack(alignment: .leading) {
                
                HStack {
                    
                    Image(systemName: "dollarsign.circle")
                        .foregroundColor(.white)
                        .padding(3)
                        .background(.orange)
                        .clipShape(Circle())
                    
                    Text("Price: $\(load.price)")
                    
                    Spacer()

                }
                
                HStack {
                    
                    Image(systemName: "shippingbox.fill")
                        .foregroundColor(.white)
                        .padding(3)
                        .background(Constants.Colours.loadboardGreen)
                        .clipShape(Circle())
                    
                    Text("Pickup: \(self.originAddress)")

                    Spacer()

                }
                
                HStack {
                    
                    Image(systemName: "mappin")
                        .foregroundColor(.white)
                        .padding(3)
                        .background(.purple)
                        .clipShape(Circle())
                    
                    Text("Delivery: \(self.destinationAddress)")

                    Spacer()
                }
                
            }
            .padding(.vertical)
            
            
            Spacer()
        }
        .background(.ultraThickMaterial)
        .cornerRadius(12)
        .padding([.horizontal], 10)
        .shadow(color: .black, radius: 1, x: 1, y: 1)
        .onAppear {
            Task {
                self.originAddress = await locationManager.getAddressFromLatLon(lat: load.originLatitude, lon: load.originLongitude)
                self.destinationAddress = await locationManager.getAddressFromLatLon(lat: load.destinationLatitude, lon: load.destinationLongitude)
            }
            
            self.finalDistance = String(Int(locationManager.calculateTotalDistanceInMiles(coordinates: [(latitude: truckModel.latitude, longitude: truckModel.longitude), (latitude: load.originLatitude, longitude: load.originLongitude), (latitude: load.destinationLatitude, longitude: load.destinationLongitude)])))
        }
        .opacity(isLoading ? 0.5 : 1)
        .overlay(alignment: .center) {
            if isLoading {
                ProgressView()
                    .foregroundColor(.white)
            }
        }
    }
}
