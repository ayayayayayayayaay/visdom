import visdom
import numpy as np

# Initialize Visdom
vis = visdom.Visdom()

# Configuration
max_points = 5000
reset_interval = 10000

# Data storage
x_data = []
y_data = []

for i in range(50000):
    # Generate data
    x = i * 0.1
    y = np.sin(x) + np.random.normal(0, 0.1)
    
    x_data.append(x)
    y_data.append(y)
    
    # Technique 1: Limit points (keep only last N points)
    if len(x_data) > max_points:
        x_data = x_data[-max_points:]
        y_data = y_data[-max_points:]
    
    # Technique 2: Downsample (plot every 10th point)
    if i % 10 == 0:
        vis.line(
            Y=np.array(y_data[-max_points:]),
            X=np.array(x_data[-max_points:]),
            win="data",
            opts=dict(
                title="Optimized Real-time Plot",
                legend=["signal"]
            )
        )
    
    # Technique 3: Periodic reset
    if i % reset_interval == 0 and i > 0:
        vis.line(
            Y=np.array(y_data[-max_points:]),
            X=np.array(x_data[-max_points:]),
            win="data",
            update='replace',
            opts=dict(
                title=f"Reset Plot (Iteration {i})",
                legend=["signal"]
            )
        )