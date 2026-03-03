#!/usr/bin/env python3
"""
Test script for 3D scatter plot update functionality
Demonstrates the fix for 3D scatter append not working
"""

import numpy as np
import time
from visdom import Visdom

def test_2d_scatter_update():
    """Test 2D scatter with append - should work"""
    print("Testing 2D scatter with append...")
    viz = Visdom()
    
    # Initial plot
    win = viz.scatter(
        X=np.random.rand(10, 2),
        opts=dict(title='2D Scatter - Append Test', markersize=10)
    )
    
    time.sleep(1)
    
    # Append more points
    for i in range(3):
        viz.scatter(
            X=np.random.rand(5, 2),
            win=win,
            update='append',
            opts=dict(markersize=10)
        )
        print(f"  2D: Appended batch {i+1}")
        time.sleep(0.5)
    
    print("✓ 2D scatter append completed\n")
    return win

def test_3d_scatter_update():
    """Test 3D scatter with append - demonstrates the fix"""
    print("Testing 3D scatter with append...")
    viz = Visdom()
    
    # Initial plot
    win = viz.scatter(
        X=np.random.rand(10, 3),
        opts=dict(title='3D Scatter - Append Test', markersize=10)
    )
    
    time.sleep(1)
    
    # Append more points
    for i in range(3):
        viz.scatter(
            X=np.random.rand(5, 3),
            win=win,
            update='append',
            opts=dict(markersize=10)
        )
        print(f"  3D: Appended batch {i+1}")
        time.sleep(0.5)
    
    print("✓ 3D scatter append completed\n")
    return win

def test_3d_scatter_with_colors():
    """Test 3D scatter with colors and labels"""
    print("Testing 3D scatter with colors...")
    viz = Visdom()
    
    # Initial plot with labels
    X = np.random.rand(10, 3)
    Y = np.random.randint(1, 4, 10)
    
    win = viz.scatter(
        X=X,
        Y=Y,
        opts=dict(
            title='3D Scatter - Colors & Append',
            legend=['Class 1', 'Class 2', 'Class 3'],
            markersize=10
        )
    )
    
    time.sleep(1)
    
    # Append more points with labels
    for i in range(3):
        X_new = np.random.rand(5, 3)
        Y_new = np.random.randint(1, 4, 5)
        
        viz.scatter(
            X=X_new,
            Y=Y_new,
            win=win,
            update='append',
            opts=dict(markersize=10)
        )
        print(f"  3D with colors: Appended batch {i+1}")
        time.sleep(0.5)
    
    print("✓ 3D scatter with colors append completed\n")
    return win

if __name__ == '__main__':
    print("=" * 60)
    print("3D Scatter Update Test - Fixed Version")
    print("=" * 60)
    print()
    
    viz = Visdom()
    
    # Check connection
    if not viz.check_connection(timeout_seconds=3):
        print("ERROR: Cannot connect to Visdom server!")
        print("Please start the server with: python -m visdom.server")
        exit(1)
    
    print("✓ Connected to Visdom server\n")
    
    # Run tests
    test_2d_scatter_update()
    test_3d_scatter_update()
    test_3d_scatter_with_colors()
    
    print("=" * 60)
    print("All tests completed successfully!")
    print("Check your Visdom browser window to see the results")
    print("=" * 60)
