//
//  TruckModel.swift
//  123Loadboard App
//
//  Created by Gordon on 2023-11-18.
//

import Foundation

class LoadModel: ObservableObject {
    @Published var filteredLoads = [Load]() // Publicly exposed list of loads
    @Published var inputUsername: String = "" {
        didSet {
            updateFilteredLoads()
        }
    }

    private var truckId: Int? // This will store the numeric truckId
    private var allLoads = [Int: Load]() // Internal dictionary for all loads
    private var notifications = [Int: NotificationData]() // Internal dictionary for notifications
    private var webSocketTask: URLSessionWebSocketTask?

    init() {
        connectWebSocket()
    }

    private func updateTruckId() {
        truckId = Int(inputUsername) // Convert username to Int if possible
        updateLoadsFromDatabase()
    }
    
    private func updateLoadsFromDatabase() {
        
    }

    private func connectWebSocket() {
        guard let url = URL(string: "ws://your-websocket-url") else {
            print("Invalid WebSocket URL")
            return
        }
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

        // Update logic to accommodate the new internal structure
        if let load = try? JSONDecoder().decode(Load.self, from: data) {
            DispatchQueue.main.async {
                self.allLoads[load.id] = load
                self.updateFilteredLoads()
            }
        } else if let notification = try? JSONDecoder().decode(NotificationData.self, from: data) {
            DispatchQueue.main.async {
                self.notifications[notification.truckId] = notification
                self.updateFilteredLoads()
            }
        } else {
            print("Unknown JSON format")
        }
    }

    private func updateFilteredLoads() {
        guard let truckId = Int(inputUsername) else {
            DispatchQueue.main.async {
                self.filteredLoads.removeAll()
            }
            return
        }

        if let notification = notifications[truckId], let loadId = notification.loadId {
            DispatchQueue.main.async {
                self.filteredLoads = self.allLoads.values.filter { $0.id == loadId }
            }
        } else {
            DispatchQueue.main.async {
                self.filteredLoads.removeAll()
            }
        }
    }
}
