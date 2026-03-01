import visdom
import numpy as np
import time
import csv
import json
from collections import deque

class OptimizedVisdomPlotter:
    def __init__(self, max_points=5000, reset_interval=10000, downsample_factor=10):
        self.vis = visdom.Visdom()
        self.max_points = max_points
        self.reset_interval = reset_interval
        self.downsample_factor = downsample_factor
        self.iteration = 0
        
        # Use deque for efficient append/pop operations
        self.x_data = deque(maxlen=max_points)
        self.y_data = deque(maxlen=max_points)
        
        # Full data storage for logging
        self.full_data = []
    
    def add_point(self, x, y):
        """Add a single point with all optimizations"""
        self.iteration += 1
        
        # Store full data for logging
        self.full_data.append({'x': x, 'y': y, 'iteration': self.iteration})
        
        # Add to limited buffer
        self.x_data.append(x)
        self.y_data.append(y)
        
        # Plot with optimizations
        if self.iteration % self.downsample_factor == 0:
            self._plot_optimized()
        
        # Periodic reset
        if self.iteration % self.reset_interval == 0:
            self._reset_plot()
        
        # Save data periodically
        if self.iteration % 1000 == 0:
            self._save_data()
    
    def _plot_optimized(self):
        """Plot with limited points and downsampling"""
        x_array = np.array(list(self.x_data))
        y_array = np.array(list(self.y_data))
        
        # Keep only last max_points
        x_plot = x_array[-self.max_points:]
        y_plot = y_array[-self.max_points:]
        
        self.vis.line(
            Y=y_plot,
            X=x_plot,
            win="optimized_data",
            opts=dict(
                title=f"Optimized Plot (Last {len(x_plot)} points)",
                legend=["data"]
            )
        )
    
    def _reset_plot(self):
        """Reset plot with fresh data"""
        x_array = np.array(list(self.x_data))
        y_array = np.array(list(self.y_data))
        
        self.vis.line(
            Y=y_array[-self.max_points:],
            X=x_array[-self.max_points:],
            win="optimized_data",
            update='replace',
            opts=dict(
                title=f"Reset Plot (Iteration {self.iteration})",
                legend=["data"]
            )
        )
    
    def _save_data(self):
        """Save full data to disk"""
        # Save as CSV
        with open('full_data.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['iteration', 'x', 'y'])
            writer.writeheader()
            writer.writerows(self.full_data)
        
        # Save as JSON
        with open('full_data.json', 'w') as f:
            json.dump(self.full_data, f)

# Example usage
def demo_optimized_plotting():
    plotter = OptimizedVisdomPlotter(max_points=5000, reset_interval=10000, downsample_factor=5)
    
    # Simulate real-time data
    for i in range(50000):
        x = i * 0.1
        y = np.sin(x) + np.random.normal(0, 0.1)
        
        plotter.add_point(x, y)
        time.sleep(0.01)  # Simulate real-time delay

if __name__ == "__main__":
    demo_optimized_plotting()