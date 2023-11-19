//
//  HapticFeedback.swift
//  123Loadboard App
//
//  Created by Gordon Ng on 2023-11-18.
//

import Foundation
import SwiftUI

func haptic() {
    let impactMed = UIImpactFeedbackGenerator(style: .soft)
    impactMed.impactOccurred()
}
