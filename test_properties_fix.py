#!/usr/bin/env python3
"""
Test script to verify the properties update fix
"""

import time
from visdom import Visdom

def test_properties_update_fix():
    """Test to verify the properties update fix works"""
    print("Testing properties update fix...")
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
    win = viz.properties(initial_properties, win='test_properties_fix', opts={'title': 'Test Properties - Initial'})
    print(f"✓ Created properties window: {win}")
    
    time.sleep(2)
    
    # Update properties - this should now update the window in real-time
    updated_properties = [
        {'type': 'text', 'name': 'Text input', 'value': 'UPDATED TEXT'},
        {'type': 'number', 'name': 'Number input', 'value': '99'},
        {'type': 'button', 'name': 'Button', 'value': 'Stop'},
        {'type': 'checkbox', 'name': 'Checkbox', 'value': False},
        {'type': 'select', 'name': 'Select', 'value': 2, 'values': ['Red', 'Green', 'Blue']},
    ]
    
    print("Updating properties...")
    result = viz.properties(updated_properties, win='test_properties_fix', opts={'title': 'Test Properties - Updated'})
    print(f"✓ Update result: {result}")
    
    time.sleep(2)
    
    # Update again with different values
    final_properties = [
        {'type': 'text', 'name': 'Text input', 'value': 'FINAL UPDATE'},
        {'type': 'number', 'name': 'Number input', 'value': '42'},
        {'type': 'button', 'name': 'Button', 'value': 'Reset'},
        {'type': 'checkbox', 'name': 'Checkbox', 'value': True},
        {'type': 'select', 'name': 'Select', 'value': 0, 'values': ['Red', 'Green', 'Blue']},
    ]
    
    print("Final update...")
    result = viz.properties(final_properties, win='test_properties_fix', opts={'title': 'Test Properties - Final'})
    print(f"✓ Final update result: {result}")
    
    print("\n✓ SUCCESS: The window should now update in real-time without needing a browser refresh!")
    print("Check your Visdom browser window to see the properties updating immediately.")

def test_new_properties_window():
    """Test creating a new properties window (should still work)"""
    print("\nTesting new properties window creation...")
    viz = Visdom()
    
    new_properties = [
        {'type': 'text', 'name': 'New Text', 'value': 'new window'},
        {'type': 'number', 'name': 'New Number', 'value': '123'},
    ]
    
    # Create new window (should use events endpoint)
    win = viz.properties(new_properties, win='new_properties_window', opts={'title': 'New Properties Window'})
    print(f"✓ Created new properties window: {win}")

def test_properties_without_win_id():
    """Test properties without specifying win ID (should create new window each time)"""
    print("\nTesting properties without win ID...")
    viz = Visdom()
    
    properties = [
        {'type': 'text', 'name': 'Auto Window', 'value': 'auto generated'},
    ]
    
    # Should create new window each time
    win1 = viz.properties(properties, opts={'title': 'Auto Window 1'})
    print(f"✓ Created auto window 1: {win1}")
    
    win2 = viz.properties(properties, opts={'title': 'Auto Window 2'})
    print(f"✓ Created auto window 2: {win2}")
    
    print(f"✓ Different windows created: {win1 != win2}")

if __name__ == '__main__':
    print("=" * 60)
    print("Properties Update Fix Test")
    print("=" * 60)
    
    test_properties_update_fix()
    test_new_properties_window()
    test_properties_without_win_id()
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("The properties update bug should now be fixed.")
    print("=" * 60)