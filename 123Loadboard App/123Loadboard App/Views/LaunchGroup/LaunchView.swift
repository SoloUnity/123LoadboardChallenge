//
//  LaunchView.swift
//  123Loadboard App
//
//  Created by Gordon Ng on 2023-11-18.
//

import SwiftUI
import MapKit

struct LaunchView: View {
    
    @EnvironmentObject private var authAPIModel:AuthAPIModel
    @EnvironmentObject private var locationModel : LocationManager
    @AppStorage("isAuthenticated") var isAuthenticatedStored = false

    var body: some View {
        
        ZStack {
            
            
            
            // Displays login if the user is not authenticated
            if !isAuthenticatedStored && !authAPIModel.isAuthenticated  {
                
                LoginView()
//                // Detect authorization status of geolocating the user
//                if locationModel.authorizationState == CLAuthorizationStatus.notDetermined{
//                    LocationRequestView()
//                }
//                else if locationModel.authorizationState == CLAuthorizationStatus.authorizedAlways || locationModel.authorizationState == CLAuthorizationStatus.authorizedWhenInUse{
//                    // Approved -> Homeview
//                    LoginView()
//                }
        //        else{
        //            // Denied -> DeniedView
        //            LocationDeniedView()
        //        }

            }
            else {
                
                MapView()
                    .tint(Constants.Colours.loadboardGreen)

            }
            
        }
    }
}

struct LaunchView_Previews: PreviewProvider {
    static var previews: some View {
        LaunchView()
    }
}
