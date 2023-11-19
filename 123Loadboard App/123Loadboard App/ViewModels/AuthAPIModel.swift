//
//  AuthAPIModel.swift
//  123Loadboard App
//
//  Created by Gordon on 2023-11-18.
//

import Foundation
import SwiftUI

class AuthAPIModel: ObservableObject {
    
    @Published var isAuthenticated = false
    @AppStorage("isAuthenticated") var isAuthenticatedStored = false

    func authenticate() {
        self.isAuthenticated = true
        self.isAuthenticatedStored = true
    }
    
    func signOut() {
        // Unauthenticate user
        DispatchQueue.main.async {
            withAnimation(.easeOut(duration: 0.2)) {
                self.isAuthenticated = false
                self.isAuthenticatedStored = false
            }
        }
    }
    
}
