//
//  DismissKeyboard.swift
//  123Loadboard App
//
//  Created by Gordon on 2023-11-18.
//

import Foundation
import UIKit

func dismissKeyboard () {
    UIApplication.shared.sendAction(#selector(UIResponder.resignFirstResponder), to: nil, from: nil, for: nil)
}
