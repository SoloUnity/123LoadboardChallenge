//
//  LogoView.swift
//  123Loadboard App
//
//  Created by Gordon on 2023-11-18.
//

import SwiftUI

struct LogoView: View {
    var body: some View {
        Image("logo")
            .resizable()
            .scaledToFit()
            .shadow(color: Constants.Colours.loadboardGreen, radius: 2)
            .frame(height: 204)
    }
}

#Preview {
    LogoView()
}
