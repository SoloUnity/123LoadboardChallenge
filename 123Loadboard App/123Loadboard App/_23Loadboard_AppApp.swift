//
//  _23Loadboard_AppApp.swift
//  123Loadboard App
//
//  Created by Gordon on 2023-11-18.
//

import SwiftUI

@main
struct _23Loadboard_AppApp: App {
    var body: some Scene {
        WindowGroup {
            SplashScreenView()
                .environmentObject(AuthAPIModel())
                .environmentObject(LocationManager())
                .environmentObject(TruckModel())
                .environmentObject(LoadModel())
                .environmentObject(Websocket())
        }
        
    }
}
