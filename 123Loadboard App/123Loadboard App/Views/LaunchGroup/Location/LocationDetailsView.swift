//
//  LocationDetailView.swift
//  MapKitTest
//
//  Created by Gordon on 2023-11-18.
//

import SwiftUI
import MapKit

struct LocationDetailsView: View {
    
    @Binding var mapSelection : MKMapItem?
    @Binding var show: Bool
    @State private var lookAroundScene: MKLookAroundScene?
    @Binding var getDirections: Bool
    
    var body: some View {
        VStack {
            HStack {
                VStack(alignment: .leading) {
                    Text(mapSelection?.placemark.name ?? "")
                        .font(.title2)
                        .fontWeight(.semibold)

                    Text(mapSelection?.placemark.title ?? "")
                        .font(.footnote)
                        .foregroundStyle(.gray)
                        .lineLimit(2)
                        .padding(.trailing)
                }
                
                Spacer()

            }
            .padding()
            
            if let scene = lookAroundScene {
                LookAroundPreview(initialScene: scene)
                    .frame(height: 200)
                    .cornerRadius(12)
                    .padding()
            } else {
                ContentUnavailableView("No preview available", systemImage: "eye.slash")
            }
                
            HStack(spacing: 24) {
                Button {
                    if let mapSelection {
                        mapSelection.openInMaps()
                    }
                } label: {
                    Text("Open in Maps")
                        .font(.headline)
                        .foregroundColor(.white)
                        .frame(width: 170, height: 48)
                        .background(Color.green)
                        .cornerRadius(12)
                }

                Button {
                    getDirections = true
                    show = false
                } label: {
                    Text("Get Directions")
                        .font(.headline)
                        .foregroundColor(.white)
                        .frame(width: 170, height: 48)
                        .background(Color.blue)
                        .cornerRadius(12)
                }
            }
            .padding(.horizontal)



        }
        .onAppear {
            print("Debg: did call onAppear")
            fetchLookAroundPreview()
        }
        .onChange(of: mapSelection) { oldValue, newValue in
            print("Debg: did call onChange")
            fetchLookAroundPreview()
        }
        .padding()
    }
}

extension LocationDetailsView {
    func fetchLookAroundPreview() {
        if let mapSelection {
            lookAroundScene = nil
            Task {
                let request = MKLookAroundSceneRequest(mapItem: mapSelection)
                lookAroundScene = try? await request.scene
            }
        }
    }
}


#Preview {
    LocationDetailsView(mapSelection: .constant(nil), show: .constant(false), getDirections: .constant(false))
}
