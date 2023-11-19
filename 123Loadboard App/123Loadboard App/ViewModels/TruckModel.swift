//
//  TruckModel.swift
//  123Loadboard App
//
//  Created by Gordon on 2023-11-18.
//

import Foundation
import SwiftUI
import MapKit


class TruckModel: ObservableObject {
    @Published var inputUsername = "" {
        didSet {
            updateTruckId()
            updateCoordinatesFromDatabase()
        }
    }
    @Published var latitude = 0.0
    @Published var longitude = 0.0

    private var webSocketTask: URLSessionWebSocketTask?
    private var truckId: Int? // This will store the numeric truckId
    private var truckDatabase = [Int: TruckData]() // Dictionary to store incoming trucks

    init() {
        self.latitude = 41.425058
        self.longitude = -87.33366
        connectWebSocket()
    }

    private func updateTruckId() {
        truckId = Int(inputUsername) // Convert username to Int if possible
        updateCoordinatesFromDatabase()
    }

    private func updateCoordinatesFromDatabase() {
        if let truckId = truckId, let truckData = truckDatabase[truckId] {
            DispatchQueue.main.async {
                self.latitude = truckData.positionLatitude
                self.longitude = truckData.positionLongitude
            }
        }
    }

    private func connectWebSocket() {
        guard let url = URL(string: "ws://localhost:8765/") else { return }
        let request = URLRequest(url: url)
        webSocketTask = URLSession.shared.webSocketTask(with: request)
        webSocketTask?.resume()
        receiveMessage()
    }

    private func receiveMessage() {
        webSocketTask?.receive { [weak self] result in
            switch result {
            case .failure(let error):
                print("WebSocket Error: \(error.localizedDescription)")
            case .success(let message):
                switch message {
                case .string(let text):
                    self?.processMessage(text)
                case .data(let data):
                    self?.processMessageData(data)
                @unknown default:
                    break
                }

                self?.receiveMessage()
            }
        }
    }

    private func processMessage(_ text: String) {
        guard let data = text.data(using: .utf8) else { return }
        processMessageData(data)
    }

    private func processMessageData(_ data: Data) {
            do {
                let truckData = try JSONDecoder().decode(TruckData.self, from: data)
                // Update the dictionary with new truck data
                truckDatabase[truckData.truckId] = truckData

                // If the incoming data matches the current truckId, update coordinates
                if truckData.type == "Truck", truckData.truckId == truckId {
                    DispatchQueue.main.async {
                        self.latitude = truckData.positionLatitude
                        self.longitude = truckData.positionLongitude
                    }
                }
            } catch {
                print("JSON Decoding Error: \(error)")
            }
        }
}


