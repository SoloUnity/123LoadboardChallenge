//
//  SplashScreenView.swift
//  123Loadboard App
//
//  Created by Gordon Ng on 2023-11-18.
//

import SwiftUI

struct SplashScreenView: View {
    
    @State private var isActive = false
    @State private var size = 0.8
    @State private var opacity = 0.5
    
    var body: some View {
                
        if isActive {
            
            LaunchView()
                
            
        } else{
            
            GeometryReader { geo in
                VStack {
                    
                    Spacer()
                    
                    LogoView()
                    
                    Spacer()
                    
                }
                .scaleEffect(size)
                .opacity(opacity)
                .onAppear {
                    withAnimation(.easeIn(duration: 0.65)) {
                        self.size = 0.9
                        self.opacity = 1.0
                    }
                }
            }
            .onAppear {
                DispatchQueue.main.asyncAfter(deadline: .now() + 0.65) {   // Duration of splash screen
                    withAnimation {
                        
                        self.isActive = true
                        
                    }
                    
                }
            }
            
        }
    }
        
}

struct SplashScreenView_Previews: PreviewProvider {
    static var previews: some View {
        SplashScreenView()
    }
}
