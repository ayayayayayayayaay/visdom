#!/usr/bin/env python3
"""
Simple test for point cloud visualization
"""

import numpy as np
from visdom import Visdom

def test_basic_pointcloud():
    """Test basic point cloud functionality"""
    print("Testing basic point cloud visualization...")
    
    viz = Visdom()
    
    # Check connection
    if not viz.check_connection(timeout_seconds=3):
        print("ERROR: Cannot connect to Visdom server!")
        print("Please start the server with: python -m visdom.server")
        return False
    
    print("✓ Connected to Visdom server")
    
    # Create simple point cloud
    n_points = 100
    points = np.random.randn(n_points, 3)
    
    # Test 1: Basic point cloud (no colors)
    try:
        win1 = viz.pointcloud(
            points=points,
            win='test_basic',
            opts={'title': 'Test: Basic Point Cloud'}
        )
        print("✓ Basic point cloud created")
    except Exception as e:
        print(f"✗ Basic point cloud failed: {e}")
        return False
    
    # Test 2: Point cloud with RGB colors
    try:
        colors = np.random.rand(n_points, 3)  # RGB colors [0,1]
        win2 = viz.pointcloud(
            points=points,
            colors=colors,
            win='test_rgb',
            opts={'title': 'Test: RGB Colors', 'point_size': 4.0}
        )
        print("✓ RGB colored point cloud created")
    except Exception as e:
        print(f"✗ RGB colored point cloud failed: {e}")
        return False
    
    # Test 3: Point cloud with class labels
    try:
        labels = np.random.randint(0, 5, n_points)  # 5 classes
        win3 = viz.pointcloud(
            points=points,
            colors=labels,
            win='test_labels',
            opts={
                'title': 'Test: Class Labels',
                'point_size': 3.0,
                'colormap': 'plasma'
            }
        )
        print("✓ Class labeled point cloud created")
    except Exception as e:
        print(f"✗ Class labeled point cloud failed: {e}")
        return False
    
    print("✓ All tests passed!")
    return True

if __name__ == '__main__':
    print("=" * 50)
    print("Point Cloud Visualization Test")
    print("=" * 50)
    
    success = test_basic_pointcloud()
    
    if success:
        print("\n🎉 Point cloud visualization is working!")
        print("Check your Visdom browser window to see the test visualizations.")
    else:
        print("\n❌ Point cloud visualization test failed.")
        print("Make sure you have implemented the pointcloud method correctly.")