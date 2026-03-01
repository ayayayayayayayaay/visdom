# Visdom Performance Optimization Guide

## Problem: Slow performance when plotting many points

## Solutions:

### 1. Limit Points (Keep only last N)
```python
max_points = 5000
x_data = x_data[-max_points:]
y_data = y_data[-max_points:]
viz.line(Y=y_data, X=x_data, win="data")
```

### 2. Periodic Reset
```python
if iteration % 1000 == 0:
    viz.line(Y=y, X=x, win="data", update='replace')
else:
    viz.line(Y=y, X=x, win="data", update='append')
```

### 3. Downsample
```python
if iteration % 10 == 0:  # Plot every 10th point
    viz.line(Y=y, X=x, win="data", update='append')
```

### 4. Combined Approach
```python
max_points = 5000
downsample = 10

if i % downsample == 0:
    x_buffer.append(i)
    y_buffer.append(value)
    
    # Keep only last max_points
    viz.line(
        Y=y_buffer[-max_points:],
        X=x_buffer[-max_points:],
        win="data"
    )
    
    # Save full data separately
    with open('log.csv', 'a') as f:
        f.write(f"{i},{value}\n")
```

## Run the demo:
```bash
python example/optimize_large_data.py
```
