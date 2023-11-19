//
//  WebSocketModel.swift
//  123Loadboard App
//
//  Created by Gordon on 2023-11-19.
//

import Foundation

class Websocket: ObservableObject {
    @Published var messages = [String]()

    private var webSocketTask: URLSessionWebSocketTask?

    init() {
        self.connect()
    }

    private func connect() {
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
                print(error.localizedDescription)
            case .success(let message):
                switch message {
                case .string(let text):
                    DispatchQueue.main.async {
                        self?.messages.append(text)
                        print(text)
                    }
                case .data(let data):
                    // Handle data message if needed
                    break
                @unknown default:
                    break
                }

                // Call receiveMessage again to listen for the next message
                self?.receiveMessage()
            }
        }
    }

    func sendMessage(_ message: String) {
        guard let data = message.data(using: .utf8) else { return }
        webSocketTask?.send(.string(message)) { error in
            if let error = error {
                print(error.localizedDescription)
            }
        }
    }
}
