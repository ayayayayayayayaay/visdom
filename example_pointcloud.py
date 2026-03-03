#!/usr/bin/env python3
"""
Point Cloud Visualization Example for Visdom
Demonstrates WebGL-based 3D point cloud rendering for deep learning applications
"""

import numpy as np
import time
from visdom import Visdom

def generate_sample_point_cloud(n_points=1000, shape='sphere'):
    """Generate sample point clouds for demonstration"""
    if shape == 'sphere':
        # Generate points on a sphere
        phi = np.random.uniform(0, 2*np.pi, n_points)
        costheta = np.random.uniform(-1, 1, n_points)
        theta = np.arccos(costheta)
        
        x = np.sin(theta) * np.cos(phi)
        y = np.sin(theta) * np.sin(phi)
        z = np.cos(theta)
        
        points = np.column_stack([x, y, z])
        
    elif shape == 'cube':
        # Generate points in a cube
        points = np.random.uniform(-1, 1, (n_points, 3))
        
    elif shape == 'car':
        # Simulate a simple car-like point cloud
        # Car body
        body_points = np.random.uniform([-2, -0.5, 0], [2, 0.5, 1], (n_points//2, 3))
        # Wheels
        wheel_centers = [[-1.5, -0.8, 0], [-1.5, 0.8, 0], [1.5, -0.8, 0], [1.5, 0.8, 0]]
        wheel_points = []
        for center in wheel_centers:
            # Generate circular wheel points
            angles = np.random.uniform(0, 2*np.pi, n_points//8)
            radii = np.random.uniform(0, 0.3, n_points//8)
            x = center[0] + radii * np.cos(angles)
            y = center[1] + radii * np.sin(angles)
            z = np.full_like(x, center[2])
            wheel_points.extend(np.column_stack([x, y, z]))
        
        points = np.vstack([body_points, np.array(wheel_points)])
        
    return points

def generate_classification_colors(points, n_classes=5):
    """Generate class labels for point cloud classification demo"""
    n_points = len(points)
    
    # Simple spatial-based classification
    labels = np.zeros(n_points, dtype=int)
    
    # Classify based on height (z-coordinate)
    z_values = points[:, 2]
    z_min, z_max = z_values.min(), z_values.max()
    
    for i in range(n_classes):
        threshold_low = z_min + (z_max - z_min) * i / n_classes
        threshold_high = z_min + (z_max - z_min) * (i + 1) / n_classes
        mask = (z_values >= threshold_low) & (z_values < threshold_high)
        labels[mask] = i
    
    return labels

def generate_segmentation_colors(points):
    """Generate RGB colors for point cloud segmentation demo"""
    n_points = len(points)
    colors = np.zeros((n_points, 3))
    
    # Color based on position
    # Red component based on x
    colors[:, 0] = (points[:, 0] - points[:, 0].min()) / (points[:, 0].max() - points[:, 0].min())
    # Green component based on y  
    colors[:, 1] = (points[:, 1] - points[:, 1].min()) / (points[:, 1].max() - points[:, 1].min())
    # Blue component based on z
    colors[:, 2] = (points[:, 2] - points[:, 2].min()) / (points[:, 2].max() - points[:, 2].min())
    
    return colors

def demo_pointnet_classification():
    """Demonstrate point cloud classification (PointNet-style)"""
    print("🔍 PointNet Classification Demo")
    
    viz = Visdom()
    if not viz.check_connection():
        print("❌ Cannot connect to Visdom server!")
        print("Please start the server with: python -m visdom.server")
        return
    
    # Generate sample point cloud
    points = generate_sample_point_cloud(2000, 'sphere')
    labels = generate_classification_colors(points, n_classes=5)
    
    # Visualize with class-based coloring
    viz.pointcloud(
        points=points,
        colors=labels,
        win='pointnet_classification',
        opts={
            'title': 'PointNet Classification - 5 Classes',
            'point_size': 3.0,
            'colormap': 'viridis',
            'show_axes': True
        }
    )
    
    print("✅ PointNet classification visualization created!")
    return viz

def demo_autonomous_driving():
    """Demonstrate large-scale point cloud for autonomous driving"""
    print("🚗 Autonomous Driving Point Cloud Demo")
    
    viz = Visdom()
    if not viz.check_connection():
        print("❌ Cannot connect to Visdom server!")
        return
    
    # Generate large point cloud simulating LiDAR data
    n_points = 10000
    
    # Ground plane
    ground_points = np.random.uniform([-20, -20, -0.5], [20, 20, 0], (n_points//2, 3))
    
    # Buildings/obstacles
    building_points = []
    for _ in range(5):
        # Random building
        center = np.random.uniform([-15, -15], [15, 15], 2)
        size = np.random.uniform([2, 2, 3], [5, 5, 8], 3)
        building = np.random.uniform(
            [center[0]-size[0]/2, center[1]-size[1]/2, 0],
            [center[0]+size[0]/2, center[1]+size[1]/2, size[2]],
            (n_points//10, 3)
        )
        building_points.append(building)
    
    # Cars
    car_points = []
    for _ in range(3):
        car_center = np.random.uniform([-10, -10], [10, 10], 2)
        car = generate_sample_point_cloud(200, 'car')
        car[:, :2] += car_center
        car_points.append(car)
    
    # Combine all points
    all_points = [ground_points] + building_points + car_points
    points = np.vstack(all_points)
    
    # Generate semantic segmentation colors
    colors = np.zeros((len(points), 3))
    idx = 0
    
    # Ground - brown
    ground_size = len(ground_points)
    colors[idx:idx+ground_size] = [0.6, 0.4, 0.2]
    idx += ground_size
    
    # Buildings - gray
    for building in building_points:
        building_size = len(building)
        colors[idx:idx+building_size] = [0.5, 0.5, 0.5]
        idx += building_size
    
    # Cars - red
    for car in car_points:
        car_size = len(car)
        colors[idx:idx+car_size] = [1.0, 0.2, 0.2]
        idx += car_size
    
    viz.pointcloud(
        points=points,
        colors=colors,
        win='autonomous_driving',
        opts={
            'title': 'Autonomous Driving - LiDAR Point Cloud',
            'point_size': 2.0,
            'background_color': '#87CEEB',  # Sky blue
            'show_axes': True,
            'camera_position': {'x': 0, 'y': -10, 'z': 5}
        }
    )
    
    print("✅ Autonomous driving visualization created!")
    return viz

def demo_3d_reconstruction():
    """Demonstrate 3D reconstruction point cloud"""
    print("🏗️ 3D Reconstruction Demo")
    
    viz = Visdom()
    if not viz.check_connection():
        print("❌ Cannot connect to Visdom server!")
        return
    
    # Generate point cloud resembling a reconstructed object
    points = generate_sample_point_cloud(5000, 'cube')
    
    # Add noise to simulate reconstruction uncertainty
    noise = np.random.normal(0, 0.05, points.shape)
    points += noise
    
    # Color based on reconstruction confidence (distance from center)
    distances = np.linalg.norm(points, axis=1)
    confidence = 1.0 - (distances / distances.max())
    
    # Create color map: high confidence = green, low confidence = red
    colors = np.zeros((len(points), 3))
    colors[:, 0] = 1.0 - confidence  # Red component
    colors[:, 1] = confidence        # Green component
    colors[:, 2] = 0.2              # Blue component
    
    viz.pointcloud(
        points=points,
        colors=colors,
        win='3d_reconstruction',
        opts={
            'title': '3D Reconstruction - Confidence Mapping',
            'point_size': 2.5,
            'show_axes': True
        }
    )
    
    print("✅ 3D reconstruction visualization created!")
    return viz

def demo_interactive_features():
    """Demonstrate interactive features and real-time updates"""
    print("🎮 Interactive Features Demo")
    
    viz = Visdom()
    if not viz.check_connection():
        print("❌ Cannot connect to Visdom server!")
        return
    
    print("Creating animated point cloud...")
    
    # Create initial point cloud
    t = 0
    for frame in range(50):
        # Generate rotating point cloud
        n_points = 1000
        theta = np.linspace(0, 2*np.pi, n_points)
        
        # Create spiral
        r = np.linspace(0.1, 2, n_points)
        x = r * np.cos(theta + t)
        y = r * np.sin(theta + t)
        z = np.sin(theta * 3 + t) * 0.5
        
        points = np.column_stack([x, y, z])
        
        # Color based on height
        colors = np.zeros((n_points, 3))
        z_norm = (z - z.min()) / (z.max() - z.min())
        colors[:, 0] = z_norm
        colors[:, 1] = 1.0 - z_norm
        colors[:, 2] = 0.5
        
        viz.pointcloud(
            points=points,
            colors=colors,
            win='interactive_demo',
            opts={
                'title': f'Interactive Demo - Frame {frame+1}/50',
                'point_size': 3.0,
                'show_axes': True
            }
        )
        
        t += 0.2
        time.sleep(0.1)
    
    print("✅ Interactive demo completed!")
    return viz

def main():
    """Main demonstration function"""
    print("=" * 60)
    print("🎯 Visdom Point Cloud Visualization Demo")
    print("For Deep Learning & 3D Computer Vision")
    print("=" * 60)
    
    try:
        # Run all demos
        demo_pointnet_classification()
        time.sleep(1)
        
        demo_autonomous_driving()
        time.sleep(1)
        
        demo_3d_reconstruction()
        time.sleep(1)
        
        demo_interactive_features()
        
        print("\n" + "=" * 60)
        print("🎉 All demos completed successfully!")
        print("Check your Visdom browser window to see the visualizations.")
        print("Use mouse to rotate, zoom, and interact with the point clouds.")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error running demos: {e}")
        print("Make sure Visdom server is running: python -m visdom.server")

if __name__ == '__main__':
    main()