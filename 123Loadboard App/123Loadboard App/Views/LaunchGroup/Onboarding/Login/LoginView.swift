//
//  LoginView.swift
//  123Loadboard App
//
//  Created by Gordon Ng on 2023-11-18.
//

import SwiftUI

struct LoginView: View {
    
    @EnvironmentObject private var authAPIModel : AuthAPIModel
    
    var body: some View {
        
        NavigationView {
            
            ZStack(alignment: .top) {
                
                
                
                LogoView()
                    .offset(y: -90)
                    .padding(50)
                
                
                VStack() {
                    
                    
                    Spacer()
                    
                    VStack(alignment: .leading) {
                        
                        Text("Claim Your Load!")
                            .font(.title)
                            .bold()
                            .padding(.top, 5)
                        
                        VStack {
                            LoginBoxView()
                        }
                        
                    }
                    .padding()
                    .background(.ultraThinMaterial)
                    .cornerRadius(20)
                    .padding()
                    
                    Spacer()
                    
                    
                    signInButton
                }
                .padding()
            }
        }
    }
    
    var signInButton: some View {
        Button {
            
            haptic()
            
            dismissKeyboard()
            
            DispatchQueue.main.async {
                                
                authAPIModel.authenticate()
                
            }
            
        } label: {
            
            ZStack{
                RectangleView()
                    .foregroundColor(Constants.Colours.loadboardGreen)
                    .shadow(color: Constants.Colours.loadboardGreen, radius: 3)
                    .cornerRadius(15)
                
                Text("Sign In")
                    .bold()
                    .padding(15)
                    .foregroundColor(.white)
                
                
            }
            .padding(.horizontal)
            .frame(height: 60)
        }
    }
}

struct LoginView_Previews: PreviewProvider {
    static var previews: some View {
        LoginView()
    }
}
