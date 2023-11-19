//
//  LoginBoxView.swift
//  123Loadboard App
//
//  Created by Gordon on 2023-11-18.
//

import SwiftUI

struct LoginBoxView: View {
    
    enum Field: Hashable {
        case usernameField
    }
    
    @EnvironmentObject private var authAPIModel : AuthAPIModel
    
    var body: some View {
        
        VStack {
            // MARK: Username Box
            ZStack {
                
                HStack {
                    Image(systemName: "truck.box.fill")
                    
                    TextField("Truck ID" , text: $authAPIModel.inputUsername)
                        .keyboardType(.default)
                        .disableAutocorrection(true)
                        .submitLabel(.continue)


                }
                .padding(.horizontal).frame(maxWidth:.infinity , minHeight:45, maxHeight: 45)
                
                RoundedRectangle(cornerRadius: 10)
                    .stroke(lineWidth: 1)
                    .frame(maxWidth:.infinity , minHeight:45, maxHeight: 45)
                    .frame(maxWidth:.infinity , minHeight:45, maxHeight: 45)
                
            }
        }
  
    }
}

struct LoginBoxView_Previews: PreviewProvider {
    static var previews: some View {
        LoginBoxView()
    }
}
