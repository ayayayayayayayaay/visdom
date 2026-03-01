import visdom
import numpy as np
import time

viz = visdom.Visdom()

# Strategy 1: Limit points (keep only last N points)
print("Strategy 1: Limiting points to last 5000")
max_points = 5000
x_data = []
y_data = []

win1 = None
for i in range(10000):
    x_data.append(i)
    y_data.append(np.sin(i * 0.01) + np.random.randn() * 0.1)
    
    # Keep only last max_points
    x_plot = x_data[-max_points:]
    y_plot = y_data[-max_points:]
    
    if i % 100 == 0:  # Update every 100 iterations
        win1 = viz.line(
            Y=np.array(y_plot),
            X=np.array(x_plot),
            win=win1,
            opts=dict(title="Limited Points (5000 max)")
        )

# Strategy 2: Periodic reset with replace
print("\nStrategy 2: Periodic reset every 1000 points")
win2 = None
for i in range(5000):
    y = np.sin(i * 0.01) + np.random.randn() * 0.1
    
    if i % 1000 == 0:  # Reset every 1000 iterations
        win2 = viz.line(
            Y=np.array([[y]]),
            X=np.array([[i]]),
            win=win2,
            update='replace',
            opts=dict(title="Periodic Reset (every 1000)")
        )
    else:
        viz.line(
            Y=np.array([[y]]),
            X=np.array([[i]]),
            win=win2,
            update='append'
        )

# Strategy 3: Downsample before plotting
print("\nStrategy 3: Downsample data (plot every 10th point)")
win3 = None
downsample_rate = 10
for i in range(5000):
    if i % downsample_rate == 0:  # Plot every 10th point
        y = np.sin(i * 0.01) + np.random.randn() * 0.1
        if win3 is None:
            win3 = viz.line(
                Y=np.array([[y]]),
                X=np.array([[i]]),
                opts=dict(title="Downsampled (every 10th point)")
            )
        else:
            viz.line(
                Y=np.array([[y]]),
                X=np.array([[i]]),
                win=win3,
                update='append'
            )

# Strategy 4: Combined approach - limit + downsample + log
print("\nStrategy 4: Combined (limit + downsample + save to file)")
import csv

max_points = 1000
downsample = 5
all_data = []
x_buffer = []
y_buffer = []

win4 = None
with open('visdom_data_log.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['iteration', 'value'])
    
    for i in range(5000):
        y = np.sin(i * 0.01) + np.random.randn() * 0.1
        
        # Log all data to file
        writer.writerow([i, y])
        
        # Only plot downsampled data
        if i % downsample == 0:
            x_buffer.append(i)
            y_buffer.append(y)
            
            # Keep only last max_points
            x_plot = x_buffer[-max_points:]
            y_plot = y_buffer[-max_points:]
            
            if i % 50 == 0:  # Update display every 50 iterations
                win4 = viz.line(
                    Y=np.array(y_plot),
                    X=np.array(x_plot),
                    win=win4,
                    opts=dict(title="Combined: Limited + Downsampled + Logged")
                )

print("\n✓ All strategies demonstrated!")
print("✓ Full data saved to 'visdom_data_log.csv'")
