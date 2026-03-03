#!/usr/bin/env python3
"""
Test script to reproduce the properties update bug
"""

import time
from visdom import Visdom

def test_properties_update_bug():
    """Test to reproduce the properties update bug"""
    print("Testing properties update bug...")
    viz = Visdom()
    
    # Check connection
    if not viz.check_connection(timeout_seconds=3):
        print("ERROR: Cannot connect to Visdom server!")
        print("Please start the server with: python -m visdom.server")
        return
    
    print("✓ Connected to Visdom server")
    
    # Initial properties
    initial_properties = [
        {'type': 'text', 'name': 'Text input', 'value': 'initial'},
        {'type': 'number', 'name': 'Number input', 'value': '12'},
        {'type': 'button', 'name': 'Button', 'value': 'Start'},
        {'type': 'checkbox', 'name': 'Checkbox', 'value': True},
        {'type': 'select', 'name': 'Select', 'value': 1, 'values': ['Red', 'Green', 'Blue']},
    ]
    
    # Create properties window
    win = viz.properties(initial_properties, win='test_properties', opts={'title': 'Test Properties'})
    print(f"✓ Created properties window: {win}")
    
    time.sleep(2)
    
    # Update properties - this should update the window but doesn't
    updated_properties = [
        {'type': 'text', 'name': 'Text input', 'value': 'UPDATED TEXT'},
        {'type': 'number', 'name': 'Number input', 'value': '99'},
        {'type': 'button', 'name': 'Button', 'value': 'Stop'},
        {'type': 'checkbox', 'name': 'Checkbox', 'value': False},
        {'type': 'select', 'name': 'Select', 'value': 2, 'values': ['Red', 'Green', 'Blue']},
    ]
    
    print("Updating properties...")
    result = viz.properties(updated_properties, win='test_properties', opts={'title': 'Test Properties - Updated'})
    print(f"✓ Update result: {result}")
    
    print("\nBUG: The window should now show updated values, but it doesn't update in real-time.")
    print("You need to refresh the browser to see the changes.")
    print("This is the bug we need to fix.")

if __name__ == '__main__':
    test_properties_update_bug()